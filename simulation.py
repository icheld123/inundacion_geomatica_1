import rasterio
from rasterio.windows import from_bounds
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# ================================================================
# CONFIGURACIÓN
# ================================================================
dem_path = "n41_e140_1arc_v3.tif"

# --- Recorte específico de Hakodate ---
LON_MIN, LON_MAX = 140.60, 140.85
LAT_MIN, LAT_MAX = 41.73, 41.92

water_levels = list(range(0, 86, 5))  # 0 a 85 m

frames_dir = "frames_hakodate"
frames3d_dir = "frames_hakodate_3d"
gif2d = "simulacion_hakodate_2d.gif"
gif3d = "simulacion_hakodate_3d.gif"

# ================================================================
# 1) CARGAR Y RECORTAR DEM
# ================================================================
with rasterio.open(dem_path) as src:
    window = from_bounds(LON_MIN, LAT_MIN, LON_MAX, LAT_MAX, src.transform)
    dem = src.read(1, window=window).astype("float32")
    transform = src.window_transform(window)
    nodata = src.nodata

# --- Limpieza ---
dem = np.where((dem == nodata) | (dem <= -30000) | (dem == 0), np.nan, dem)

print("Rango DEM después del recorte:", np.nanmin(dem), "a", np.nanmax(dem))

# ================================================================
# 2) GENERAR 2D
# ================================================================
os.makedirs(frames_dir, exist_ok=True)
extent = (LON_MIN, LON_MAX, LAT_MIN, LAT_MAX)
frames = []

for i, lvl in enumerate(water_levels):
    flooded = (dem <= lvl) & (~np.isnan(dem))

    plt.figure(figsize=(7, 7))
    plt.imshow(dem, cmap="terrain", extent=extent)
    plt.imshow(np.where(flooded, 1, np.nan),
               cmap="Blues",
               alpha=0.55,
               extent=extent)

    plt.title(f"Inundación Hakodate – {lvl} m")
    plt.axis("off")

    path = os.path.join(frames_dir, f"frame_{i:03}.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", pad_inches=0)
    plt.close()

    frames.append(imageio.imread(path))

imageio.mimsave(gif2d, frames, fps=1.5)
print("GIF 2D generado:", gif2d)

# ================================================================
# 3) GENERAR 3D (MEJORADO)
# ================================================================
os.makedirs(frames3d_dir, exist_ok=True)
frames3d = []

ny, nx = dem.shape
xs = np.linspace(LON_MIN, LON_MAX, nx)
ys = np.linspace(LAT_MIN, LAT_MAX, ny)
X, Y = np.meshgrid(xs, ys)
Z = dem.copy()

# --- Ajuste de relieves para evitar agua sobre montañas ---
# (Esto mejora la visualización del plano de agua)
z_min = np.nanmin(Z)
z_max = np.nanmax(Z)

for i, lvl in enumerate(water_levels):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    # --- Terreno ---
    ax.plot_surface(
        X, Y, Z,
        cmap="terrain",
        rstride=3, cstride=3,
        linewidth=0,
        antialiased=True
    )

    # --- Capa de agua ---
    # Ahora el agua es un plano horizontal, solo visible donde corresponde.
    Zwater = np.where(Z <= lvl, lvl, np.nan)

    ax.plot_surface(
        X, Y, Zwater,
        facecolors=cm.Blues(0.85 * np.ones_like(Zwater)),
        alpha=0.45,
        rstride=3, cstride=3,
        linewidth=0
    )

    # --- Configuración visual ---
    ax.set_title(f"Inundación 3D – {lvl} m")
    ax.set_zlabel("Altitud (m)")

    # Límites Z realistas (evita que el agua ‘suba’ montañas)
    ax.set_zlim(z_min, z_max)

    # Vista fija (no rotar)
    ax.view_init(elev=45, azim=230)

    # Establece el área de los ejes para evitar recortes
    ax.set_position([0, 0, 1, 1])

    path = os.path.join(frames3d_dir, f"frame3d_{i:03}.png")
    plt.savefig(path, dpi=120, bbox_inches=None, pad_inches=0)  # <-- cambio aquí
    plt.close()

    frames3d.append(imageio.imread(path))

# --- Redimensiona todas las imágenes a la misma forma ---
from PIL import Image

# Obtén el tamaño de la primera imagen
base_shape = frames3d[0].shape[:2]

# Redimensiona todas las imágenes al mismo tamaño
frames3d_resized = []
for img in frames3d:
    if img.shape[:2] != base_shape:
        pil_img = Image.fromarray(img)
        pil_img = pil_img.resize((base_shape[1], base_shape[0]), Image.LANCZOS)
        img = np.array(pil_img)
    frames3d_resized.append(img)

imageio.mimsave(gif3d, frames3d_resized, fps=2)
print("GIF 3D generado:", gif3d)

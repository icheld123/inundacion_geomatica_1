# Simulación de inundación — Bahía de Hakodate

Este repositorio contiene `simulation.py`, un script que genera dos animaciones (GIF):

- `simulacion_hakodate.gif` — vista 2D de la inundación para niveles de agua 0–85 m (paso 5 m).
- `simulacion_hakodate_3d.gif` — vista 3D reducida del mismo proceso.

Archivos y carpetas generadas:

- `frames/` — contiene los PNG 2D por paso.
- `frames/3d/` — contiene los PNG 3D por paso.

Requisitos
---------

Se necesita Python 3.8+ y las librerías listadas en `requirements.txt`.

Recomendación de instalación (recomendado: conda):

```bash
# crear entorno (ejemplo con conda)
conda create -n inundacion python=3.10 -y
conda activate inundacion
conda install -c conda-forge rasterio matplotlib imageio numpy pillow -y
```

Si prefieres pip (puede fallar al instalar `rasterio` si faltan dependencias del sistema):

```bash
pip install -r requirements.txt
```

Uso
---

Ejecuta el script desde la carpeta del proyecto (donde está el TIFF `n41_e140_1arc_v3.tif`):

```bash
python3 simulation.py
```

Salida
-----

Al terminar tendrás `simulacion_hakodate.gif` (2D) y `simulacion_hakodate_3d.gif` en el directorio.

Notas
-----

- Si tu TIFF no está en coordenadas geográficas (lon/lat), el recorte por bounds podría no funcionar. En ese caso indica el sistema de referencia o ajusta el recorte manualmente.
- Para centrar aún más la zona de interés, puedes editar los parámetros `LON_MIN/LON_MAX` y `LAT_MIN/LAT_MAX` en `simulation.py`.
- La creación de la versión 3D reduce la resolución interna para acelerar el render; ajusta `step` dentro del script si quieres más detalle (pero tardará más).

Si quieres, puedo ajustar el recorte exactamente a los límites de la imagen que me enviaste o mejorar la estética de los GIFs (leyenda, escala de colores, marca de escala, rotación 3D animada, etc.).

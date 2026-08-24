# Assets — datos de entrada / input data

Todos los insumos de las prácticas viven aquí. **Ningún notebook debe leer datos desde su propia carpeta de día** — así los archivos pesados quedan en un solo lugar y son fáciles de mover a Git LFS o a un almacenamiento externo.

## Estructura

```
Assets/
├── shared/     capas usadas por más de un día (límites de cuenca, DEM, máscaras)
├── Day1/       WEAP: series climáticas, catchments, demandas
├── Day2/       hidroeconomía + detección de agua superficial
├── Day3/       JRC GSW, altimetría, calidad de agua
├── Day4/       LULC: muestras de entrenamiento, mosaicos, productos climáticos
└── Day5/       salinidad de suelos, muestreos de campo, riego por goteo
```

> **Nota:** git no versiona carpetas vacías. Estas subcarpetas aparecerán en GitHub recién cuando contengan al menos un archivo.

## Formatos aceptados

| Tipo | Formato | Nota |
|---|---|---|
| Vectorial | `.zip` con el shapefile completo (`.shp .shx .dbf .prj .cpg`) | un `.zip` por capa, nunca los componentes sueltos |
| Vectorial ligero | `.geojson` | preferido si < 5 MB; siempre en EPSG:4326 |
| Tabular | `.csv` (UTF-8, separador `,`) o `.xlsx` | primera fila = encabezados, sin celdas combinadas |
| Ráster | `.tif` (COG) | comprimido; si > 50 MB, usar Git LFS o enlace externo |
| Configuración | `.json` | parámetros, geometrías de AOI, listas de bandas |
| Modelos WEAP | `.zip` del área WEAP | incluir la versión de WEAP en el nombre |

## Convención de nombres

```
<dia>_<tema>_<detalle>_<año o cobertura>.<ext>

Day1_catchments_TDPS_v1.zip
Day3_JRC_GSW_occurrence_TDPS_1984_2021.tif
Day4_training_samples_altiplano_2024.geojson
Day5_soil_salinity_field_campaign_2025.xlsx
shared_TDPS_basin_boundary.zip
```

Todo en minúsculas salvo el prefijo `DayN`/`shared`, sin espacios ni acentos, `snake_case` para el resto.

## Cómo leer los assets desde un notebook

Los notebooks corren desde `SummerSchool/DayN/`, así que la raíz del repositorio está un nivel arriba:

```python
import pathlib
ROOT       = pathlib.Path.cwd().parent
DAY_ASSETS = ROOT / "Assets" / "Day1"      # ajustar el día
SHARED     = ROOT / "Assets" / "shared"
```

Ejemplo con un shapefile comprimido:

```python
import geopandas as gpd
catchments = gpd.read_file(f"zip://{DAY_ASSETS / 'Day1_catchments_TDPS_v1.zip'}")
```

Ejemplo con una tabla:

```python
import pandas as pd
df = pd.read_excel(DAY_ASSETS / "Day5_soil_salinity_field_campaign_2025.xlsx")
```

En Colab, clone el repositorio primero y apunte `ROOT` a la carpeta clonada.

## Límites de tamaño

GitHub rechaza archivos **> 100 MB** y advierte a partir de **50 MB**.

- **< 50 MB** → commit normal.
- **50–100 MB** → Git LFS (ya configurado en `.gitattributes` para `.tif`, `.zip`, `.nc`, `.h5`, `.xlsx`). Instalar con `git lfs install` antes del primer commit.
- **> 100 MB** → **no subir**. Deje aquí un archivo `NOMBRE.link.txt` con la URL de descarga (Drive, Zenodo, SharePoint) y la suma de verificación, y haga que el notebook lo descargue.

## Procedencia

Para cada archivo conviene registrar origen, fecha de descarga, sistema de referencia, licencia y responsable — en el README del día correspondiente o en la sección de referencias del notebook. Sin eso, el material no es reproducible después del curso.

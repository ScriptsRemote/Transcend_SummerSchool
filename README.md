# TRANSCEND — 2nd Summer School 2026

**Titicaca–Desaguadero–Poopó (TDPS) basins — water resources, remote sensing and irrigated agriculture**

📍 La Paz, Bolivia · 🗓️ 12–16 October 2026 · 🎓 SEI · University of Manchester (UoM) · IMDEA Agua · IIAREN–UMSA · PROSUCO

---

## Sobre / About

Las cuencas del Titicaca–Desaguadero–Poopó (TDPS) constituyen un recurso hídrico transfronterizo crítico y vulnerable, compartido por Bolivia y Perú. La agricultura es el principal usuario del agua, representando aproximadamente el **91 %** de las extracciones, junto con otros usos como abastecimiento doméstico, minería y energía, además de sostener ecosistemas altoandinos.

Esta escuela de verano entrena a ingenieros y profesionales del agua en el uso combinado de **modelación hidrológica (WEAP)**, **análisis hidroeconómico** y **observación de la Tierra** para monitorear y gestionar el agua en agricultura de riego.

> This repository holds all teaching material: one folder per day, one notebook per session, and a shared `Assets/` folder for the data used in the hands-on exercises.

---

## Estructura del repositorio / Repository structure

```
SummerSchool/
├── README.md                         ← este archivo / this file
├── requirements.txt                  ← dependencias Python / Python dependencies
├── .gitignore
├── .gitattributes                    ← reglas de Git LFS para datos pesados
│
├── 00_Programme_Overview.ipynb       ← introducción + cronograma completo
│
├── Day1_Hydrology_and_WEAP_Modeling/
│   ├── README.md
│   ├── 01_hydrology_fundamentals_weap_structure.ipynb
│   ├── 02_soil_moisture_method_and_calibration.ipynb
│   ├── 03_climate_data_interpolation_and_lulc.ipynb
│   └── 04_weap_model_consolidation.ipynb
│
├── Day2_Hydroeconomics_and_Water_Mapping/
├── Day3_Remote_Sensing_Fundamentals_and_Indices/
├── Day4_LULC_and_Climate_with_RS/
├── Day5_Soil_Monitoring_and_Irrigation_Efficiency/
│       (misma estructura: README + 4 notebooks)
│
├── Assets/                           ← datos de entrada / input data
│   ├── README.md                     ← convenciones de nombres y formatos
│   ├── shared/                       ← capas usadas por más de un día
│   └── Day1/ Day2/ Day3/ Day4/ Day5/
│
├── Docs/                             ← borradores .docx — IGNORADO por git
└── tools/
    └── split_master_notebook.py      ← regenera los notebooks desde el Colab maestro
```

`Docs/` está en `.gitignore`: se mantiene en local para la planificación, pero no se publica en GitHub.

**Regla de oro / rule of thumb:** un notebook = un bloque horario de 90 minutos. Cada notebook es autocontenido y puede abrirse directamente en Colab.

---

## Cronograma / Schedule

| Hora | Day 1 · 12 Oct | Day 2 · 13 Oct | Day 3 · 14 Oct | Day 4 · 15 Oct | Day 5 · 16 Oct |
|---|---|---|---|---|---|
| | **Hydrology & WEAP**<br>`SEI` | **Hydroeconomics & Water Mapping**<br>`SEI / IMDEA` | **RS Fundamentals & Indices**<br>`UoM` | **LULC & Climate with RS**<br>`UoM` | **Soil & Irrigation Efficiency**<br>`IIAREN / PROSUCO` |
| 09:00–10:30 | Hydrology fundamentals, WEAP structure | Agricultural demand & economic modeling | Long-term surface water (JRC) | Classification fundamentals | Soil salinity models (part 1) |
| 10:40–12:10 | Soil-moisture method & calibration | Sensors & spectral behaviour | Water-quality proxies | Building the classification input | Soil salinity models (part 2) |
| 14:00–15:30 | Climate data & interpolation | Vegetation & water indices | Satellite altimetry | Training, mapping & accuracy | Automated drip irrigation |
| 15:40–17:10 | WEAP model consolidation | Platforms: GEE, Colab, QGIS | Digital image processing in GEE | Climate products, ET & water balance | Integration & water-use efficiency |

Coffee breaks: 10:30–10:40 y 15:30–15:40 · Almuerzo / lunch: 12:10–14:00

Días 6–9 (17–20 Oct): viaje de campo, workshop y retorno — fuera del alcance de este repositorio.

---

## Cómo usar / How to use

### Opción A — Google Colab (recomendado)

Abra cualquier notebook directamente desde GitHub:

```
https://colab.research.google.com/github/ScriptsRemote/Transcend_SummerSchool/blob/main/<ruta-del-notebook>
```

Para leer los datos de `Assets/` desde Colab, clone el repositorio en la primera celda:

```python
!git clone --depth 1 https://github.com/ScriptsRemote/Transcend_SummerSchool.git
```

### Opción B — Local

```bash
git clone https://github.com/ScriptsRemote/Transcend_SummerSchool.git
cd Transcend_SummerSchool
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

### Google Earth Engine

Los notebooks de los días 2–4 usan GEE. Antes del curso, cada participante debe:

1. Registrarse en [Earth Engine](https://earthengine.google.com/) (cuenta *noncommercial / Community*).
2. Crear un Cloud Project y anotar su ID.
3. Autenticarse al inicio del notebook con su propio project ID:

```python
import ee
ee.Authenticate()
ee.Initialize(project="<tu-cloud-project>")
```

### Software adicional

- **WEAP** (días 1–2) — licencia e instalación gestionadas por SEI.
- **QGIS 3.44 LTR** (día 2 en adelante).

---

## Convenciones / Conventions

| Tema | Regla |
|---|---|
| Notebooks | `NN_titulo_en_snake_case.ipynb`, numerados por bloque horario |
| Carpetas de día | `DayN_Tema_Principal` |
| Datos | siempre bajo `Assets/`, nunca junto al notebook |
| Salidas | no versionar; escribir en `outputs/` (ignorado por git) |
| Idioma | títulos y estructura en inglés; explicaciones EN/ES según el instructor |
| Antes del push | limpiar las salidas de las celdas (`nbstripout` o *Edit → Clear all outputs*) |

---

## Regenerar los notebooks / Regenerating the notebooks

El notebook maestro vive en Colab y define el programa. Para volver a fragmentarlo tras un cambio de temario:

```bash
# Colab: Archivo → Descargar → Descargar .ipynb
python tools/split_master_notebook.py --master ruta/al/master.ipynb --dry-run
python tools/split_master_notebook.py --master ruta/al/master.ipynb
```

⚠️ Sin `--dry-run` el script **sobrescribe** los 20 notebooks y los 5 `DayN/README.md`, porque su contenido se deriva por completo del maestro. Este README raíz, `Assets/` y `Docs/` nunca se tocan.

---

## Equipo / Team

| Rol | Personas |
|---|---|
| Coordinación general | Gustavo Ayala (SEI) |
| Hidrología / WEAP | Gustavo Ayala, Camilo González (SEI) |
| Hidroeconomía | Francesco Sapino (IMDEA Agua) |
| Teledetección | Christhian Santana Cunha, Sebastián Palomino, Tim Foster (UoM) |
| Suelos y riego | Roberto Miranda, Fanny Arragan Tancara, Wara Yampara (IIAREN–UMSA), PROSUCO |

**Audiencia:** ingenieros y profesionales que trabajan o estudian temas relacionados con recursos hídricos (ALT, Univ. Puno, UGCK, UMSA–Facultad de Agronomía, SENAMHI, SENARI, IRD, PROSUCO, entre otros).

---

## Licencia / License

Por definir antes de publicar el repositorio. Sugerencia: **CC BY 4.0** para el material didáctico y **MIT** para el código.

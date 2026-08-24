# Day 4 — Land Use / Land Cover & Climate with RS

**2026-10-15 (Thursday / Jueves)** · UoM

> Classification algorithms, change detection, climate products, ET and water balance

## Sesiones / Sessions

| Horario | Notebook | Instructores |
|---|---|---|
| 09:00 - 10:30 | [`01_classification_fundamentals_and_algorithms.ipynb`](01_classification_fundamentals_and_algorithms.ipynb) | Christian, Sebastian integra WETSAT |
| 10:40 - 12:10 | [`02_building_the_classification_input.ipynb`](02_building_the_classification_input.ipynb) | Crhistian |
| 14:00 - 15:30 | [`03_training_mapping_and_accuracy.ipynb`](03_training_mapping_and_accuracy.ipynb) | Crhistian, Gustavo |
| 15:40 - 17:10 | [`04_climate_products_et_and_water_balance.ipynb`](04_climate_products_et_and_water_balance.ipynb) | Crhisthian |

## Detalle / Detail

### 1. Classification Fundamentals and Algorithms

`09:00 - 10:30` · Christian, Sebastian integra WETSAT

Classification fundamentals and algorithms. Spectral patterns; K-Means, PCA, CART, Random Forest, SVM. Sampling strategy, spatial autocorrelation, training vs test samples

### 2. Building the Classification Input

`10:40 - 12:10` · Crhistian

Building the classification input. Spatial/temporal filtering, seasonal/annual cloudless mosaics, sample collection and training geometries, pixel-by-pixel extraction

### 3. Training Mapping and Accuracy

`14:00 - 15:30` · Crhistian, Gustavo

Training, mapping and accuracy assessment. Supervised classifiers in GEE; thematic map export; confusion matrix, overall accuracy, Kappa and K-fold validation. Change detection and irrigated areas (map algebra, dry/rainy season dynamics, rainfed vs irrigated signatures) - Se puede Integrar una introduccion de AquaCROP - Tim

### 4. Climate Products ET and Water Balance

`15:40 - 17:10` · Crhisthian

Earth Observation climate products (CHIRPS, GSMaP, ERA5). MODIS MOD16 ET product (structure, scaling, resolution). Time-series processing, simplified water balance (P–ET), zonal statistics, LULC cross-referencing and trend analysis

## Datos / Data

Los insumos de este dia van en [`../Assets/Day4/`](../Assets/Day4/).
Las capas compartidas con otros dias estan en [`../Assets/shared/`](../Assets/shared/).

## Antes de la sesion / Before the session

- [ ] Instalar las dependencias de `requirements.txt`
- [ ] Verificar el acceso a los datos en `Assets/Day4/`
- [ ] Revisar las referencias de cada notebook

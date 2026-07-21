# Groundwater 2d potential for Punjab/Potohar area.

An end-to-end geospatial machine learning project whose core objective is to generate a 2D groundwater potential grid map of the Potohar Plateau/Punjab region. The pipeline achieves this by training a predictive model on historical survey data and satellite-derived surface metrics, surfacing the final inference engine through a local API endpoint.

## The Real Life Challenges
In drought-prone regions like the Potohar Plateau and Punjab, communities and farmers face severe water security risks. Traditional hydrological surveys often rely on expensive, blind physical drilling with low success rates, driving up exploration costs and wasting resources in areas with zero groundwater potential. This is where Machine learning can help by utilizing past datasets such as the one used for this model along with remote sensing datasets to generate maps and accurately point towards viable geological aquifers.

---
## Project Overview
This repository demonstrates a complete, end-to-end machine learning workflow. By combining a century of historical regional groundwater measurements with modern remote sensing data, the pipeline extracts key environmental features and trains a Random Forest classifier. The ultimate goal of this pipeline is the spatial rendering of a 2D grid matrix to map localized aquifer potential across structurally complex terrain.

---

## Project Architecture & Workflow

The pipeline is split into distinct steps, transitioning from raw historical logs to a locally deployed machine learning service:

1. **`dataset_for_groundwater`**: Ingestion, localized spatial filtering (Punjab/Potohar region in Pakistan), and cleaning of a 100-year BGS historical dataset, featuring KD-Tree distance modeling to generate balanced pseudo-absence (zero) points for model training.

2. **`gee_feature`**: Programmatic connection to the Google Earth Engine (GEE) API using `geemap`. This stage extracts target topographic features including Elevation (`NASADEM`), Slope, Topographic Position Index (TPI), and soil textures (USDA surface and subsurface classes) based on geographic coordinates.
3. **`training_the_model`**: Preprocessing of the combined geospatial dataset and optimization of a Random Forest classification model using `scikit-learn`.
4. **`2d_grid_generator`**: Interpolation logic using scipy griddata interpolator with method selected as nearest that sets up a 2-dimensional inference grid across the targeted regional zones along with matplotlib to generate continuous spatial asset maps. 
5. **Model Deployment (`app.py`)**: A local API service built with **FastAPI** and **Uvicorn** to serve instant model predictions.

---
## Dataset overview

**Raw Input:** Ingested the official British Geological Survey (BGS) dataset (`India_Pakistan_WL_NGDC.xlsx`), containing **68,782 historical observation logs** across 4,028 monitoring wells spanning 1884–2020.
   - **Spatial Filtering & Aggregation:** Filtered raw coordinates specifically to the Punjab / Potohar Plateau region ( Longitude 71.50 - 74.00 ,   Latitude 29.09 - 32.50 ) and aggregated temporal measurements into mean water table depths (`WL_MBGL`).
   - **Pseudo-Absence Modeling:** Applied **KD-Tree spatial distance modeling** to generate 1,197 balanced zero-potential (absence) points across non-aquifer bedrock zones.
   - **Final Dataset & Features:** Produced a clean, balanced dataset (`Final_Punjab_And_Potohar_Training_Data.csv`) of **2,725 spatial samples** (1,528 Class 1 vs. 1,197 Class 0). Attributes include:
     - 'LONG' & 'LAT'
     - `elevation`
     - `slope`
     - `tpi`
     - `soil_surface`
     - `soil_subsurface`
     - `potential`
---

##  Model Performance & Importances

Multiple classification algorithms (Logistic Regression, Decision Tree, and Random Forest) were evaluated on the combined geospatial dataset. A baseline **Random Forest Classifier** was selected for hyperparameter tuning due to its slightly superior f1-score.

### 1. Class 1 (Groundwater Potential) Tuning Improvements
By optimizing hyperparameters, the model's sensitivity (**Recall**) improved dramatically while maintaining high **Precision**:

- **Recall:** Improved from **0.70 → 0.82** (0.82 score)
- **F1-Score:** Improved from **0.68 → 0.73** (0.73 score)
- **Precision:** Remained stable at low false-positive rates (0.66 score).

> ** Real-World Significance:** 
> Maintaining high precision keeps false positives low, while the boosted recall (**0.82**) minimizes false negatives. In practical terms, this ensures farmers and regional planners in drought-prone areas are far less likely to overlook viable groundwater locations.


### 2. Key Feature Importance
Here are the importances of the features.
1. **TPI (Topographic Position Index):** Primary indicator for identifying catchment depressions, valleys, and drainage lines where water naturally accumulates.
2. **Elevation :** Critical baseline terrain metric influencing hydrostatic pressure and regional runoff.
3. **Slope:** Governs surface runoff velocity versus water infiltration rates into underlying aquifers
4. **Soil_subsurface :** Determines deeper soil permeability and groundwater percolation capability.
5. **Soil_surface :** Dictates immediate surface runoff absorption and initial water infiltration rates.

---
## Continuous Spatial Grid Output

This is the 2d generated grid. It's a continous map of Voronoi Patchwork appearance because of the nearet method utilized. The prediction probabilities were used for this instead of binary predictions.
<img width="2475" height="2179" alt="groundwater_potential_map" src="https://github.com/user-attachments/assets/a14f9e5b-f756-4bde-8876-a59f69d1492c" />


---

##  Real-World Ramifications & Impact

The ability to accurately categorize groundwater potential zones using remote sensing data carries significant real-world utility:

- **Targeted Hydrological Surveys:** Instead of conducting expensive, blind physical drilling across massive areas, environmental agencies can use  predictive models such as this to prioritize high-potential zones, reducing field exploration costs.
- **Agricultural Planning:** Regional policymakers can utilize the continuous spatial asset maps generated using this concept to guide sustainable farming, ensuring water-heavy crops are aligned with resilient aquifers.


---

##  Tech Stack & Frameworks

- **Data Engineering & GIS:** `pandas`, `geopandas`, `geemap`, Google Earth Engine API
- **Machine Learning:** `scikit-learn`, `joblib`
- **Model Deployment:** `FastAPI`, `Uvicorn`, `Pydantic`

---

##  Local Deployment (Proof of Concept)

The model deployment is built using FastAPI and Pydantic validation to serve as a functional proof of an end-to-end machine learning system. 

###  Run the API locally
 **Clone the repository:**
   ```bash
   git clone https://github.com/Zeerak113/ground-water-potential-model.git
   cd ground-water-potential-model
   pip install -r requirements.txt

   python app.py
   ```
### Interactive API Interface (Swagger UI)

Once the Uvicorn server is running, navigate to `http://127.0.0.1:8000/docs` in your browser.

<img width="1637" height="726" alt="swaggerui-1" src="https://github.com/user-attachments/assets/e7d5fb16-29b1-4f7c-b05d-118be9cfba9b" />
<img width="1518" height="753" alt="swaggerui-3" src="https://github.com/user-attachments/assets/1586757f-43f4-4873-8c1c-8e4d3c4ed742" />
<img width="1515" height="581" alt="swaggerui-2" src="https://github.com/user-attachments/assets/154ad3a1-73d8-494f-8986-78a642b61603" />

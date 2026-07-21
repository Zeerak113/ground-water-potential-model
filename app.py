from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import joblib
import numpy as np


app = FastAPI()


model = joblib.load("groundwater_rf_model.joblib")

@app.get("/")
def read_root():
    return{"message":"Hello world lmao"}

class Input(BaseModel):
    elevation: int
    slope: float
    soil_subsurface: int
    soil_surface: int
    tpi: float


@app.post("/predict")
def predict(data: Input):
    
    features = [[
        data.elevation,
        data.slope,
        data.soil_subsurface,
        data.soil_surface,
        data.tpi
    ]]
    
   
    prediction = model.predict(features)
    
    
    return {"prediction": int(prediction[0])}

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)

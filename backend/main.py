from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from io import BytesIO
from PIL import Image

from weather_service import fetch_weather
from ml_models import predict_image
from predictor import adjust_prediction_with_weather
from market_analysis import suggest_crop

app = FastAPI(title="AgriCare API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define API routes first

@app.post("/predict")
async def predict(
    location: str = Form(...),
    crop_name: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        contents = await image.read()
        img = Image.open(BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file.")
        
    weather_data = fetch_weather(location)
    
    base_prediction = predict_image(img, crop_name)
    if "error" in base_prediction:
        raise HTTPException(status_code=400, detail=base_prediction["error"])
        
    final_result = adjust_prediction_with_weather(base_prediction, weather_data)
    
    return {
        "weather": weather_data,
        "base_prediction": base_prediction,
        "adjusted_result": final_result
    }

@app.get("/suggest")
def suggest(location: str):
    weather_data = fetch_weather(location)
    suggestion = suggest_crop(weather_data)
    
    return {
        "weather": weather_data,
        "suggestion": suggestion
    }

# Mount frontend static files
# Ensure the directory exists to avoid errors
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

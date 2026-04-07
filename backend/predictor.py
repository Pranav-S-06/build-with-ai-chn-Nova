def adjust_prediction_with_weather(base_prediction: dict, weather_data: dict):
    prediction = base_prediction["prediction"]
    confidence = base_prediction["base_confidence"]
    
    adjusted_confidence = confidence
    heuristics_applied = []
    
    temp = weather_data.get("temperature", 25)
    humidity = weather_data.get("humidity", 60)
    
    # Fungal diseases
    if "Fungal" in prediction:
        if humidity < 40:
            adjusted_confidence -= 0.3
            heuristics_applied.append("Low humidity reduces likelihood of fungal infection.")
        elif humidity > 80:
            adjusted_confidence += 0.2
            heuristics_applied.append("High humidity increases likelihood of fungal infection.")
            
    # Bacterial diseases
    if "Bacterial" in prediction:
        if temp > 35:
            adjusted_confidence -= 0.3
            heuristics_applied.append("High temperatures reduce likelihood of bacterial infection.")
        elif 20 <= temp <= 30 and humidity > 70:
            adjusted_confidence += 0.2
            heuristics_applied.append("Moderate temperatures with high humidity favor bacterial infections.")
            
    # Healthy
    if "Healthy" in prediction:
        if 20 <= temp <= 30 and 40 <= humidity <= 70:
            adjusted_confidence += 0.1
            heuristics_applied.append("Optimal weather conditions favor plant health.")
            
    adjusted_confidence = max(0.01, min(0.99, adjusted_confidence))
    
    final_prediction = prediction
    if adjusted_confidence < 0.3 and "Healthy" not in final_prediction:
        final_prediction = prediction.split()[0] + " Healthy"
        adjusted_confidence = 0.6 # Reverted to healthy due to overriding weather conditions
        heuristics_applied.append("Weather strongly counter-indicates disease; predicted Healthy instead.")
        
    return {
        "final_prediction": final_prediction,
        "confidence": adjusted_confidence,
        "heuristics_applied": heuristics_applied
    }

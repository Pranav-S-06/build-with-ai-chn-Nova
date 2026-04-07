def suggest_crop(weather_data: dict):
    temp = weather_data.get("temperature", 25)
    humidity = weather_data.get("humidity", 60)
    
    # Hardcoded definitions
    CROPS = {
        "Potato": {
            "ideal_temp": (15, 25),
            "ideal_humidity": (50, 70),
            "market_demand": "High",
            "profit_margin": "Moderate",
            "description": "Potatoes grow best in cool climates. High market demand makes it a stable choice."
        },
        "Tomato": {
            "ideal_temp": (20, 30),
            "ideal_humidity": (60, 80),
            "market_demand": "Very High",
            "profit_margin": "High",
            "description": "Tomatoes thrive in warm weather. Extremely profitable if diseases can be managed."
        },
        "Wheat": {
            "ideal_temp": (10, 24),
            "ideal_humidity": (40, 60),
            "market_demand": "High",
            "profit_margin": "Low",
            "description": "A staple crop requiring less humidity. Reliable but lower profit margins."
        },
        "Rice": {
            "ideal_temp": (20, 35),
            "ideal_humidity": (80, 100),
            "market_demand": "Very High",
            "profit_margin": "Moderate",
            "description": "Requires very high humidity and water. Essential global staple."
        }
    }
    
    best_crop = None
    best_score = -1
    
    for crop_name, details in CROPS.items():
        score = 0
        
        t_min, t_max = details["ideal_temp"]
        if t_min <= temp <= t_max:
            score += 10
        elif abs(temp - t_min) < 5 or abs(temp - t_max) < 5:
            score += 5
            
        h_min, h_max = details["ideal_humidity"]
        if h_min <= humidity <= h_max:
            score += 10
        elif abs(humidity - h_min) < 10 or abs(humidity - h_max) < 10:
            score += 5
            
        if details["market_demand"] == "Very High":
            score += 5
        if details["profit_margin"] == "High":
            score += 5
            
        if score > best_score:
            best_score = score
            best_crop = crop_name
            
    if not best_crop:
        best_crop = "Potato"
        
    return {
        "suggested_crop": best_crop,
        "details": CROPS[best_crop],
        "match_score": best_score,
        "reasoning": f"Current weather ({temp}°C, {humidity}% humidity) is a good match for {best_crop} requirements. Market demand is {CROPS[best_crop]['market_demand']}."
    }

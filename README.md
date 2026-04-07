# build-with-ai-chn-[Nova]

## Problem Statement
Farmers and agricultural workers often struggle with timely and accurate identification of crop diseases, leading to reduced yield and profitability. Additionally, predicting the most profitable crop based on changing local weather patterns and market demand is difficult without centralized, data-driven insights.

## Project Description
**AgriCare** is a full-stack Smart Crop Disease & Market Insights platform. It allows users to:
1. Input their current location to pull real-time weather data.
2. Upload a leaf image of their crop (e.g., Potato, Tomato) to instantly predict potential diseases.
3. Obtain automated crop recommendations based on their exact local climate conditions and hardcoded market analysis for maximum profitability.

**How AI is Integrated:**
The project uses a PyTorch deep learning pipeline (based off ResNet-18) configured for image classification to detect crop diseases (like potato fungal, tomato bacterial, etc.). Furthermore, an intelligent heuristic engine combines the AI's confidence scores with live meteorological data (like humidity and temperature) to refine predictions—for instance, aggressively flagging bacterial infections when high humidity and specific temperatures converge.

## Proof of Google AI Usage
Attach screenshots in a `/proof` folder:

```
/proof
  - ai_usage_1.png
  - ai_usage_2.png
```

## Screenshots
Add project screenshots:
*(Add your UI screenshots here)*

## Demo Video
Upload your demo video to Google Drive and paste the shareable link here(max 3 minutes). 
[Watch Demo](INSERT_GOOGLE_DRIVE_LINK_HERE)

## Installation Steps
```bash
# 1. Clone the repository
git clone https://github.com/your-username/build-with-ai-chn-[your-team-name].git

# 2. Go to project folder
cd build-with-ai-chn-[your-team-name]/backend

# 3. Create Virtual Environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up Environment Variables
# Create a .env file inside backend/ and add your OpenWeatherMap API Key
# OPENWEATHERMAP_API_KEY=your_key_here

# 6. Run the project
uvicorn main:app --reload

# 7. Visit http://localhost:8000 in your browser
```

# Getaround_Pricing_Optimization

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/framework-FastAPI-green.svg)
![Dashboard](https://img.shields.io/badge/UI-Streamlit-red.svg)
![Docker](https://img.shields.io/badge/deployment-Docker-blue.svg)
![ML](https://img.shields.io/badge/Machine_Learning-Random_Forest-gold.svg)

## 📋 Business Overview
Getaround is a peer-to-peer car-sharing platform. This project addresses two critical challenges identified by the Product team:
1. **Late Checkouts**: 18% of consecutive rentals are impacted by a previous driver's delay, causing friction and cancellations.
2. **Pricing Strategy**: Owners often struggle to set the right daily price. We provide a Machine Learning solution to suggest competitive prices.

## 🚀 Live Demonstrations
Explore the project's interactive features hosted on **Hugging Face Spaces**:

* **📊 Decision Dashboard (Streamlit)
* **🔌 Pricing API (FastAPI/Docker)

## 🛠️ Tech Stack
* **Analysis:** Python, Pandas, Plotly.
* **Dashboarding:** Streamlit.
* **Machine Learning:** Scikit-Learn (Random Forest Regressor), Pipelines, Joblib.
* **Production:** FastAPI, Uvicorn, Docker, Hugging Face.

## 📈 Key Insights & Strategic Recommendation
Based on the data analysis:
* **Connect Cars:** Extremely punctual (Median delay = 0 min). Automating the checkout process eliminates human friction.
* **Mobile Check-ins:** Slower and prone to a "long tail" of significant delays due to physical key exchanges.
* **Final Recommendation:** Implement a **120-minute minimum delay** between rentals **only for Mobile check-ins**. This resolves the majority of problematic cases without impacting the revenue of the highly efficient Connect fleet.

## 🤖 Pricing Model
The **Random Forest** model achieves an **R² score of 67%**. It evaluates features such as engine power, mileage, and premium options (GPS, AC, etc.) to predict the optimal daily rental price.

### API Usage
You can request a prediction by sending a POST request to the `/predict` endpoint:

**Request Body Example:**
```json
{
  "input": [
    ["BMW", 50000, 150, "diesel", "black", "convertible", true, true, false, false, true, true, true]
  ]
}

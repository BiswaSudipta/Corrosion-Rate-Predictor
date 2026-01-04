import streamlit as st
import pandas as pd
import pickle

# Load model
with open("corrosion_model.pkl", "rb") as file:
    model = pickle.load(file)

# App title
st.set_page_config(page_title="Corrosion Rate Predictor", layout="centered")

st.title("🛢️ Refinery Pipeline Corrosion Predictor")
st.write("Predict corrosion rate (mm/year) using operational and material parameters")

st.divider()

# User Inputs
material = st.selectbox(
    "Pipeline Material",
    ["Carbon Steel", "SS304", "SS316", "Alloy Steel", "Inconel"]
)

temperature = st.number_input("Operating Temperature (°C)", 50.0, 400.0, 200.0)
pressure = st.number_input("Operating Pressure (bar)", 1.0, 100.0, 40.0)
ph = st.number_input("Fluid pH", 1.0, 14.0, 5.5)
sulfur = st.number_input("Sulfur Content (ppm)", 0.0, 2000.0, 500.0)
velocity = st.number_input("Flow Velocity (m/s)", 0.1, 10.0, 3.0)
service_years = st.number_input("Service Years", 0, 30, 8)

# Prediction button
if st.button("Predict Corrosion Rate"):
    input_df = pd.DataFrame({
        "material": [material],
        "temperature_c": [temperature],
        "pressure_bar": [pressure],
        "ph": [ph],
        "sulfur_ppm": [sulfur],
        "flow_velocity_ms": [velocity],
        "service_years": [service_years]
    })

    prediction = model.predict(input_df)[0]

    # Risk Classification
    if prediction < 0.3:
        risk = "🟢 Low Risk"
    elif prediction < 0.7:
        risk = "🟡 Medium Risk"
    elif prediction < 1.0:
        risk = "🟠 High Risk"
    else:
        risk = "🔴 Critical Risk"


    st.success(f"Predicted Corrosion Rate: **{prediction:.3f} mm/year**")
    st.warning(f"Corrosion Risk Level: **{risk}**")

st.divider()

st.caption(
    "This tool supports predictive maintenance and risk-based inspection "
    "planning for refinery pipelines."
)

import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ── LOAD MODEL ──
with open('tobacco_model.pkl', 'rb') as file:
    model = pickle.load(file)

# ── TITLE ──
st.set_page_config(page_title="Tobacco Yield Predictor", layout="centered")
st.title("Farm-Level Tobacco Yield Predictor")
st.markdown("### Mashonaland West Province, Zimbabwe")
st.write("Enter your farm details to get a predicted yield.")
st.divider()

# ── INPUTS ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("Environment")
    rainfall = st.slider("Rainfall (mm)", 400, 900, 650, 10)
    temperature = st.slider("Temperature (°C)", 18, 30, 24, 1)
    st.subheader("Farm Size")
    area = st.slider("Area under tobacco (ha)", 1.0, 5.0, 2.7, 0.1)
    irrigation = st.slider("Irrigation (days)", 0, 40, 20, 1)

with col2:
    st.subheader("Fertilizer (kg)")
    n = st.slider("Nitrogen (N)", 50, 400, 230, 5)
    p = st.slider("Phosphorus (P)", 20, 150, 84, 5)
    k = st.slider("Potassium (K)", 30, 200, 118, 5)
    st.subheader("Pest & Disease")
    pest = st.slider("Pest Index (0-5)", 0, 5, 2, 1)
    disease = st.slider("Disease Index (0-3)", 0, 3, 0, 1)

st.divider()

# ── PREDICT ──
if st.button("Predict My Yield", type="primary", use_container_width=True):
    
    total_fert = n + p + k
    fert_per_ha = total_fert / area
    
    input_data = pd.DataFrame({
        'rainfall_mm': [rainfall],
        'avg_temp_c': [temperature],
        'area_ha': [area],
        'irrigation_days': [irrigation],
        'fertilizer_n_kg': [n],
        'fertilizer_p_kg': [p],
        'fertilizer_k_kg': [k],
        'pest_index': [pest],
        'disease_index': [disease],
        'total_fertilizer': [total_fert],
        'fertilizer_per_ha': [fert_per_ha],
        'pest_disease_interaction': [pest * disease],
        'N_P_ratio': [n / (p + 0.01)],
        'rainfall_squared': [rainfall ** 2],
        'stress_index': [pest + disease]
    })
    
    prediction = model.predict(input_data)[0]
    lower = prediction - 490
    upper = prediction + 490
    
    st.success(f"### Predicted Yield: {prediction:,.0f} kg")
    st.info(f"Expected range (68% confidence): **{lower:,.0f} kg** to **{upper:,.0f} kg**")
    
    st.divider()
    st.markdown("### Recommendation")
    if pest >= 3:
        st.warning("High pest pressure. Prioritize integrated pest management.")
    elif pest >= 1:
        st.info("Moderate pest pressure. Maintain regular scouting.")
    else:
        st.success("Low pest pressure. Continue current practices.")

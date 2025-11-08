import streamlit as st
import requests

st.set_page_config(page_title="Heart Disease Prediction Chatbot")

st.title("Heart Disease Prediction Chatbot 🤖")
st.write("Enter health features, and I'll predict the heart disease risk!")

# List all features as required by API
fields = [
    ('age', 'Age', 50.0),
    ('sex', 'Sex (1=male, 0=female)', 1),
    ('cp', 'Chest Pain Type (1-4)', 1),
    ('trestbps', 'Resting Blood Pressure', 120.0),
    ('chol', 'Serum Cholesterol (mg/dl)', 200.0),
    ('fbs', 'Fasting Blood Sugar >120mg/dl (1=true, 0=false)', 0),
    ('restecg', 'Resting Electrocardiographic Results (0-2)', 0),
    ('thalach', 'Max Heart Rate Achieved', 150.0),
    ('exang', 'Exercise Angina (1=yes, 0=no)', 0),
    ('oldpeak', 'Oldpeak (ST depression)', 1.0),
    ('slope', 'Slope of Peak Exercise ST Segment (1-3)', 2),
    ('ca', 'Number of Major Vessels (0-3)', 0),
    ('thal', 'Thalassemia (3=normal, 6=fixed_defect, 7=reversible_defect)', 3)
]

inputs = {}
for key, label, default in fields:
    if isinstance(default, float):
        value = st.number_input(label, value=default)
    else:
        value = st.number_input(label, value=default, step=1)
    inputs[key] = value

if st.button("Predict Risk"):
    with st.spinner("Contacting prediction model..."):
        try:
            res = requests.post("http://127.0.0.1:8000/predict", json=inputs)
            if res.ok:
                result = res.json()
                if result["label"]:
                    st.warning(f"High risk of heart disease (probability={result['probability']:.2f})")
                else:
                    st.success(f"Low risk of heart disease (probability={result['probability']:.2f})")
            else:
                st.error(f"API error: {res.status_code} {res.text}")
        except Exception as e:
            st.error(f"Could not contact model: {e}")

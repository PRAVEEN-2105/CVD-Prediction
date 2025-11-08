import requests

sample_data = {
    "age": 63, "trestbps": 145, "chol": 233, "thalach": 150, "oldpeak": 2.3, "ca": 0,
    "sex": 1, "cp": 3, "fbs": 1, "restecg": 0, "exang": 0, "slope": 0, "thal": 1
}

res = requests.post("http://127.0.0.1:8000/predict", json=sample_data)
print(res.json())

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import joblib

# 1. Load the CSV (rename your file to 'cleveland.csv', add headers)
df = pd.read_csv("cleveland.csv")

# 2. Replace '?' with np.nan for missing values
df.replace("?", np.nan, inplace=True)

# 3. Define column groups
numeric = ["age", "trestbps", "chol", "thalach", "oldpeak", "ca"]
categorical = ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal"]

# 4. Convert numeric columns to float and fill missing with median
for col in numeric:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].median())

# 5. Convert categorical columns to int and fill missing with mode
for col in categorical:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].mode()[0])

# 6. Prepare target label (0 = no disease, 1 = disease)
df["num"] = pd.to_numeric(df["num"], errors='coerce')  # Ensure last column is numeric
df["target"] = (df["num"] > 0).astype(int)

# 7. Select features and target
X = df[numeric + categorical]
y = df["target"]

# 8. Data pipeline
preprocess = ColumnTransformer([
    ("num", StandardScaler(), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)
])
model = LogisticRegression(max_iter=200, class_weight="balanced")
clf = Pipeline([("preprocess", preprocess), ("model", model)])

# 9. Train/test split and model train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
clf.fit(X_train, y_train)

# 10. Evaluation and save
proba = clf.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, proba)
print(f"ROC-AUC: {auc:.3f}")

joblib.dump(clf, "heart_pipeline.joblib")
print("Training/saving complete! Model saved")

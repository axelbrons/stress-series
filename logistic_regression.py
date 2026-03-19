import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier
from catboost import CatBoostClassifier

df = pd.read_csv("dataset_final.csv")

df = df.sample(n=100000, random_state=42) 

X = df[["EDA", "ECG"]]
y = df["y"]

kf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)  

scoring = {
    "accuracy": "accuracy",
    "precision": "precision_macro",
    "recall": "recall_macro",
    "f1": "f1_macro"
}

models = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ]),
    
    "Decision Tree": DecisionTreeClassifier(),
    
    "Random Forest": RandomForestClassifier(
        n_estimators=20,    # moins d'arbres
        max_depth=10,       # limite profondeur
        n_jobs=-1,
        random_state=42
    ),
    
    "XGBoost": XGBClassifier(
        n_estimators=50,
        max_depth=6,
        use_label_encoder=False,
        eval_metric="mlogloss",
        n_jobs=-1
    ),
    
    "CatBoost": CatBoostClassifier(verbose=0, iterations=100) 
}

# Evaluation
print("\n=== Résultats K-Fold ===\n")

for name, model in models.items():
    scores = cross_validate(model, X, y, cv=kf, scoring=scoring)
    
    print(f"--- {name} ---")
    print(f"Accuracy  : {scores['test_accuracy'].mean():.4f}")
    print(f"Precision : {scores['test_precision'].mean():.4f}")
    print(f"Recall    : {scores['test_recall'].mean():.4f}")
    print(f"F1-score  : {scores['test_f1'].mean():.4f}")
    print("-" * 40)
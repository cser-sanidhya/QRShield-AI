import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import joblib


# Load dataset
df = pd.read_csv("dataset/upi_fraud_dataset.csv")

# Features
X = df[
    [
        "amount",
        "merchant_verified",
        "suspicious_keyword"
    ]
]

# Target
y = df["fraud"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Save model
joblib.dump(model, "fraud_model.pkl")

print("Model trained successfully!")
print("fraud_model.pkl created")
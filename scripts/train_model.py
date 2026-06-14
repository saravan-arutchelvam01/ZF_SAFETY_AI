import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

df = pd.read_csv("data/production_data.csv")

X = df[
    [
        "temperature",
        "vibration",
        "pressure",
        "motor_current",
        "production_speed",
        "defect_count",
        "humidity",
        "torque",
        "sensor_accuracy"
    ]
]

y = df["risk_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Accuracy:", accuracy)

joblib.dump(
    model,
    "models/safety_model.pkl"
)

print("Model Saved")

print(
    classification_report(
        y_test,
        predictions
    )
)

print(
    confusion_matrix(
        y_test,
        predictions
    )
)
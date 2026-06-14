import pandas as pd
import joblib

model = joblib.load(
    "models/safety_model.pkl"
)

features = [
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

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print(importance)
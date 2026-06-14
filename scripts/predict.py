import joblib
import pandas as pd

model = joblib.load(
    "models/safety_model.pkl"
)

sample = pd.DataFrame(
    [[
        85,
        4.5,
        180,
        45,
        150,
        7,
        65,
        250,
        90
    ]],
    columns=[
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
)

prediction = model.predict(sample)

print("Predicted Risk:", prediction[0])
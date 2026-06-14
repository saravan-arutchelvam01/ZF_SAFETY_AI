import pandas as pd
import random

records = []

for i in range(50000):

    component = random.choice([
        "Seat Belt",
        "Airbag",
        "Steering",
        "Occupant Safety"
    ])

    # ==========================================
    # PRODUCT SPECIFIC DATA
    # ==========================================

    if component == "Seat Belt":

        machine_id = f"SB-{random.randint(101,125)}"

        temperature = round(random.uniform(30,60),2)
        vibration = round(random.uniform(0.5,2.5),2)
        pressure = round(random.uniform(80,120),2)
        motor_current = round(random.uniform(10,25),2)

        production_speed = round(random.uniform(80,180),2)

        humidity = round(random.uniform(30,70),2)

        torque = round(random.uniform(80,150),2)

        sensor_accuracy = round(
            random.uniform(92,100),
            2
        )

    elif component == "Airbag":

        machine_id = f"AB-{random.randint(101,125)}"

        temperature = round(random.uniform(40,75),2)
        vibration = round(random.uniform(1,3),2)
        pressure = round(random.uniform(180,300),2)

        motor_current = round(random.uniform(15,30),2)

        production_speed = round(random.uniform(60,150),2)

        humidity = round(random.uniform(30,75),2)

        torque = round(random.uniform(120,220),2)

        sensor_accuracy = round(
            random.uniform(90,100),
            2
        )

    elif component == "Steering":

        machine_id = f"ST-{random.randint(101,125)}"

        temperature = round(random.uniform(45,85),2)
        vibration = round(random.uniform(1,4),2)
        pressure = round(random.uniform(100,180),2)

        motor_current = round(random.uniform(20,45),2)

        production_speed = round(random.uniform(50,120),2)

        humidity = round(random.uniform(30,80),2)

        torque = round(random.uniform(250,400),2)

        sensor_accuracy = round(
            random.uniform(88,100),
            2
        )

    else:

        machine_id = f"OS-{random.randint(101,125)}"

        temperature = round(random.uniform(35,70),2)
        vibration = round(random.uniform(1,3.5),2)
        pressure = round(random.uniform(90,160),2)

        motor_current = round(random.uniform(15,35),2)

        production_speed = round(random.uniform(60,140),2)

        humidity = round(random.uniform(30,80),2)

        torque = round(random.uniform(120,250),2)

        sensor_accuracy = round(
            random.uniform(85,100),
            2
        )

    # ==========================================
    # DEFECT CALCULATION
    # ==========================================

    defect_count = 0

    if vibration > 3:
        defect_count += random.randint(1,4)

    if temperature > 75:
        defect_count += random.randint(1,3)

    if motor_current > 40:
        defect_count += random.randint(1,3)

    # Occupant Safety produces more quality issues

    if component == "Occupant Safety":

        defect_count += random.randint(0,3)

    # ==========================================
    # PRODUCT SPECIFIC RISK LOGIC
    # ==========================================

    risk_score = 0

    if component == "Seat Belt":

        if temperature > 55:
            risk_score += 2

        if vibration > 2:
            risk_score += 2

    elif component == "Airbag":

        if pressure > 260:
            risk_score += 2

        if temperature > 70:
            risk_score += 2

    elif component == "Steering":

        if torque > 350:
            risk_score += 2

        if motor_current > 40:
            risk_score += 2

    else:

        if defect_count > 4:
            risk_score += 3

        if sensor_accuracy < 88:
            risk_score += 2

    # Common Risk Factors

    if defect_count > 5:
        risk_score += 2

    if sensor_accuracy < 90:
        risk_score += 1

    # ==========================================
    # RISK LEVEL
    # ==========================================

    if risk_score <= 2:

        risk_level = 0

    elif risk_score <= 5:

        risk_level = 1

    else:

        risk_level = 2

    # ==========================================
    # SAVE RECORD
    # ==========================================

    records.append([
        component,
        machine_id,
        temperature,
        vibration,
        pressure,
        motor_current,
        production_speed,
        defect_count,
        humidity,
        torque,
        sensor_accuracy,
        risk_level
    ])

# ==========================================
# DATAFRAME
# ==========================================

df = pd.DataFrame(
    records,
    columns=[
        "component_type",
        "machine_id",
        "temperature",
        "vibration",
        "pressure",
        "motor_current",
        "production_speed",
        "defect_count",
        "humidity",
        "torque",
        "sensor_accuracy",
        "risk_level"
    ]
)

# ==========================================
# SAVE CSV
# ==========================================

df.to_csv(
    "data/production_data.csv",
    index=False
)

print("ZF Production Dataset Generated Successfully")
import pandas as pd
import random
import time
from sqlalchemy import create_engine

# ==========================================
# DATABASE CONNECTION
# ==========================================

engine = create_engine(
    "mysql+pymysql://root:root123@localhost/zf_safety_ai"
)

# ==========================================
# REAL-TIME DATA GENERATOR
# ==========================================

while True:

    component = random.choice([
        "Seat Belt",
        "Airbag",
        "Steering",
        "Occupant Safety"
    ])

    # ==========================================
    # SEAT BELT
    # ==========================================

    if component == "Seat Belt":

        machine_id = f"SB-{random.randint(101,125)}"

        temperature = round(random.uniform(40,100),2)
        vibration = round(random.uniform(1,5),2)
        pressure = round(random.uniform(80,120),2)

        motor_current = round(
            random.uniform(10,35),
            2
        )

        production_speed = round(
            random.uniform(80,180),
            2
        )

        humidity = round(
            random.uniform(30,70),
            2
        )

        torque = round(
            random.uniform(80,150),
            2
        )

        sensor_accuracy = round(
            random.uniform(92,100),
            2
        )

        defect_count = random.randint(0,8)

        risk_score = 0

        if temperature > 80:
            risk_score += 3

        if vibration > 4:
            risk_score += 3

        if defect_count > 5:
            risk_score += 4

    # ==========================================
    # AIRBAG
    # ==========================================

    elif component == "Airbag":

        machine_id = f"AB-{random.randint(101,125)}"

        temperature = round(random.uniform(25,70),2)

        vibration = round(
            random.uniform(1,3),
            2
        )

        pressure = round(
            random.uniform(100,250),
            2
        )

        motor_current = round(
            random.uniform(15,30),
            2
        )

        production_speed = round(
            random.uniform(60,150),
            2
        )

        humidity = round(
            random.uniform(30,75),
            2
        )

        torque = round(
            random.uniform(120,220),
            2
        )

        sensor_accuracy = round(
            random.uniform(80,100),
            2
        )

        defect_count = random.randint(0,5)

        risk_score = 0

        if pressure > 220:
            risk_score += 4

        if sensor_accuracy < 85:
            risk_score += 4

        if defect_count > 3:
            risk_score += 2

    # ==========================================
    # STEERING
    # ==========================================

    elif component == "Steering":

        machine_id = f"ST-{random.randint(101,125)}"

        temperature = round(
            random.uniform(40,80),
            2
        )

        vibration = round(
            random.uniform(1,5),
            2
        )

        pressure = round(
            random.uniform(100,180),
            2
        )

        motor_current = round(
            random.uniform(20,50),
            2
        )

        production_speed = round(
            random.uniform(50,120),
            2
        )

        humidity = round(
            random.uniform(30,80),
            2
        )

        torque = round(
            random.uniform(150,400),
            2
        )

        sensor_accuracy = round(
            random.uniform(88,100),
            2
        )

        defect_count = random.randint(0,5)

        risk_score = 0

        if torque > 350:
            risk_score += 4

        if motor_current > 40:
            risk_score += 3

        if vibration > 4:
            risk_score += 3

    # ==========================================
    # OCCUPANT SAFETY
    # ==========================================

    else:

        machine_id = f"OS-{random.randint(101,125)}"

        temperature = round(
            random.uniform(25,90),
            2
        )

        vibration = round(
            random.uniform(1,3),
            2
        )

        pressure = round(
            random.uniform(90,160),
            2
        )

        motor_current = round(
            random.uniform(15,35),
            2
        )

        production_speed = round(
            random.uniform(60,140),
            2
        )

        humidity = round(
            random.uniform(30,80),
            2
        )

        torque = round(
            random.uniform(120,250),
            2
        )

        sensor_accuracy = round(
            random.uniform(80,100),
            2
        )

        defect_count = random.randint(0,10)

        risk_score = 0

        if defect_count > 5:
            risk_score += 5

        if sensor_accuracy < 90:
            risk_score += 3

        if temperature > 85:
            risk_score += 2

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
    # INSERT RECORD
    # ==========================================

    row = {
        "component_type": component,
        "machine_id": machine_id,
        "temperature": temperature,
        "vibration": vibration,
        "pressure": pressure,
        "motor_current": motor_current,
        "production_speed": production_speed,
        "defect_count": defect_count,
        "humidity": humidity,
        "torque": torque,
        "sensor_accuracy": sensor_accuracy,
        "risk_level": risk_level
    }

    pd.DataFrame([row]).to_sql(
        "production_data",
        engine,
        if_exists="append",
        index=False
    )

    print(
        f"Inserted: {component} | "
        f"{machine_id} | "
        f"Risk={risk_level}"
    )

    time.sleep(5)
def get_recommendation(row):

    if row["temperature"] > 80:
        return "Inspect Cooling System"

    elif row["vibration"] > 4:
        return "Check Bearings"

    elif row["motor_current"] > 40:
        return "Inspect Motor"

    else:
        return "Normal Operation"
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:root123@localhost/zf_safety_ai"
)

query = """
SELECT *
FROM production_data
WHERE risk_level = 2
"""

df = pd.read_sql(query, engine)

alerts = []

for _, row in df.iterrows():

    alert_message = (
        f"Critical Safety Risk Detected in "
        f"{row['component_type']} "
        f"Machine {row['machine_id']}"
    )

    alerts.append([
        row["machine_id"],
        row["component_type"],
        row["risk_level"],
        alert_message
    ])

alert_df = pd.DataFrame(
    alerts,
    columns=[
        "machine_id",
        "component_type",
        "risk_level",
        "alert_message"
    ]
)

alert_df.to_sql(
    "alerts",
    engine,
    if_exists="append",
    index=False
)

print("Alerts Generated Successfully")
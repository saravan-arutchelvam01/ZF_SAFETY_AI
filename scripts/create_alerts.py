
import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.append(project_root)




import pandas as pd

from scripts.db_connection import engine

query = """
SELECT *
FROM prediction_history
WHERE predicted_risk = 2
"""

df = pd.read_sql(query, engine)

alerts = []

for _, row in df.iterrows():

    alerts.append({
        "machine_id": "UNKNOWN",
        "component_type": "MANUAL ENTRY",
        "risk_level": 2,
        "alert_message":
        "Critical Safety Risk Detected"
    })

alerts_df = pd.DataFrame(alerts)

alerts_df.to_sql(
    "alerts",
    engine,
    if_exists="append",
    index=False
)

print("Alerts Created")
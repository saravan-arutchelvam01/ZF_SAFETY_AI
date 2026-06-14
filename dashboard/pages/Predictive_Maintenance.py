import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# ==========================================
# PROJECT PATH
# ==========================================

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)

from scripts.db_connection import engine

# ==========================================
# AZURE SPECTRUM THEME
# ==========================================

st.markdown("""
<style>

.page-title{
    font-size:36px;
    font-weight:700;
    color:#1E3A8A;
}

.page-subtitle{
    color:#64748B;
    margin-bottom:25px;
}

.section-title{
    color:#1E3A8A;
    font-size:22px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

query = """
SELECT * FROM production_data
"""

df = pd.read_sql(
    query,
    engine
)


product = st.selectbox(
    "Select Product Line",
    [
        "All Products",
        "Seat Belt",
        "Airbag",
        "Steering",
        "Occupant Safety"
    ]
)

if product != "All Products":

    df = df[
        df["component_type"] == product
    ]


    
# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class='page-title'>
Predictive Maintenance
</div>

<div class='page-subtitle'>
Machine Health, Failure Forecasting and Maintenance Planning
</div>
""", unsafe_allow_html=True)

# ==========================================
# HEALTH CALCULATIONS
# ==========================================

results = []

for _, row in df.tail(200).iterrows():

    component = row["component_type"]

    # ==========================================
    # SEAT BELT
    # ==========================================

    if component == "Seat Belt":

        health_score = 100

        health_score -= (
            row["temperature"] / 100
        ) * 40

        health_score -= (
            row["vibration"] / 5
        ) * 35

        health_score -= (
            row["defect_count"] / 10
        ) * 25

    # ==========================================
    # AIRBAG
    # ==========================================

    elif component == "Airbag":

        health_score = 100

        health_score -= (
            row["pressure"] / 300
        ) * 45

        health_score -= (
            (100 - row["sensor_accuracy"]) / 20
        ) * 35

        health_score -= (
            row["defect_count"] / 10
        ) * 20

    # ==========================================
    # STEERING
    # ==========================================

    elif component == "Steering":

        health_score = 100

        health_score -= (
            row["torque"] / 400
        ) * 40

        health_score -= (
            row["motor_current"] / 50
        ) * 35

        health_score -= (
            row["vibration"] / 5
        ) * 25

    # ==========================================
    # OCCUPANT SAFETY
    # ==========================================

    else:

        health_score = 100

        health_score -= (
            row["defect_count"] / 10
        ) * 50

        health_score -= (
            (100 - row["sensor_accuracy"]) / 20
        ) * 30

        health_score -= (
            row["temperature"] / 100
        ) * 20

    health_score = max(
        0,
        round(health_score, 2)
    )

    failure_probability = round(
        100 - health_score,
        2
    )

    remaining_life = round(
        health_score * 10,
        0
    )

    results.append({

        "Machine ID":
            row["machine_id"],

        "Component":
            row["component_type"],

        "Health Score (%)":
            health_score,

        "Failure Probability (%)":
            failure_probability,

        "Remaining Life (Hours)":
            remaining_life
    })

result_df = pd.DataFrame(
    results
)

# ==========================================
# KPI SECTION
# ==========================================

avg_health = round(
    result_df[
        "Health Score (%)"
    ].mean(),
    2
)

avg_failure = round(
    result_df[
        "Failure Probability (%)"
    ].mean(),
    2
)

avg_life = round(
    result_df[
        "Remaining Life (Hours)"
    ].mean(),
    2
)

critical_count = len(
    df[
        df["risk_level"] == 2
    ]
)

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Plant Health",
    f"{avg_health}%"
)

col2.metric(
    "Failure Risk",
    f"{avg_failure}%"
)

col3.metric(
    "Remaining Life",
    f"{avg_life} hrs"
)

col4.metric(
    "Critical Machines",
    critical_count
)

if critical_count > 100:

    st.error(
        f"""
        {critical_count} critical machines detected.

        Immediate maintenance action required.
        """
    )

elif critical_count > 50:

    st.warning(
        f"""
        {critical_count} machines require
        preventive maintenance review.
        """
    )

else:

    st.success(
        "Predictive maintenance indicators are stable."
    )

# ==========================================
# MACHINE HEALTH
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>Machine Health Ranking</div>",
    unsafe_allow_html=True
)

attention = result_df.sort_values(
    by="Health Score (%)"
)

st.dataframe(
    attention.head(15),
    use_container_width=True,
    hide_index=True,
    height=400
)

# ==========================================
# HEALTH DISTRIBUTION + FAILURE FORECAST
# ==========================================

days = [
    "Day 1",
    "Day 2",
    "Day 3",
    "Day 4",
    "Day 5",
    "Day 6",
    "Day 7"
]

forecast = []

for i in range(7):

    predicted = int(
        critical_count *
        (
            1 +
            np.random.uniform(
                -0.05,
                0.15
            )
        )
    )

    forecast.append(predicted)

forecast_df = pd.DataFrame({
    "Day": days,
    "Predicted Critical Machines": forecast
})

st.markdown("---")

left, right = st.columns(2)

with left:

    st.markdown(
        "<div class='section-title'>Health Distribution</div>",
        unsafe_allow_html=True
    )

    st.bar_chart(
        result_df["Health Score (%)"]
    )

with right:

    st.markdown(
        "<div class='section-title'>7-Day Failure Forecast</div>",
        unsafe_allow_html=True
    )

    st.line_chart(
        forecast_df.set_index("Day")
    )

# ==========================================
# HIGH RISK MACHINES
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>High Risk Machines</div>",
    unsafe_allow_html=True
)

high_risk = df[
    df["risk_level"] == 2
]

if len(high_risk) > 0:

    st.dataframe(
        high_risk[
            [
                "machine_id",
                "component_type",
                "temperature",
                "vibration",
                "motor_current",
                "defect_count"
            ]
        ],
        use_container_width=True
    )

else:

    st.success(
        "No high-risk machines detected."
    )

# ==========================================
# AI RECOMMENDATION
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>AI Recommendation</div>",
    unsafe_allow_html=True
)

if critical_count > 100:

    st.error(
        """
        High risk trend detected.

        Immediate inspection required.
        Increase maintenance frequency.
        """
    )

elif critical_count > 50:

    st.warning(
        """
        Moderate risk trend detected.

        Schedule preventive maintenance.
        """
    )

else:

    st.success(
        """
        Plant operating within safe limits.

        Continue routine monitoring.
        """
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Predictive Maintenance • Health & Forecasting"
)
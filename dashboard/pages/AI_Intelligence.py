import streamlit as st
import pandas as pd
import joblib
import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)


model = joblib.load(
    "models/safety_model.pkl"
)

st.set_page_config(
    page_title="AI Intelligence",
    layout="wide"
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Intelligence",
    layout="wide"
)

# ==========================================
# AZURE SPECTRUM THEME
# ==========================================

st.markdown("""
<style>

.page-title{
    font-size:38px;
    font-weight:700;
    color:#1E3A8A;
}

.page-subtitle{
    color:#64748B;
    margin-bottom:25px;
}

.result-card{
    background:white;
    padding:20px;
    border-radius:16px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.05);
}

.info-card{
    background:#DBEAFE;
    padding:18px;
    border-radius:12px;
    border-left:5px solid #2563EB;
    margin-top:15px;
}

.normal{
    color:#22C55E;
    font-size:30px;
    font-weight:700;
}

.warning{
    color:#F59E0B;
    font-size:30px;
    font-weight:700;
}

.critical{
    color:#DC2626;
    font-size:30px;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <div class='page-title'>
        AI Intelligence
    </div>

    <div class='page-subtitle'>
        Product-Level Risk Intelligence & AI Decision Analysis
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# PRODUCT SELECTOR
# ==========================================

product = st.selectbox(
    "Select Product Line",
    [
        "Seat Belt",
        "Airbag",
        "Steering",
        "Occupant Safety"
    ]
)

df = pd.read_csv("data/production_data.csv")

product_df = df[
    df["component_type"] == product
]

if len(product_df) == 0:

    st.warning(
        f"No records found for {product}"
    )

    st.stop()

# ==========================================
# KPI SECTION
# ==========================================

healthy = len(
    product_df[
        product_df["risk_level"] == 0
    ]
)

warning = len(
    product_df[
        product_df["risk_level"] == 1
    ]
)

critical = len(
    product_df[
        product_df["risk_level"] == 2
    ]
)

health_score = round(
    healthy / len(product_df) * 100,
    1
)

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Health Score",
    f"{health_score}%"
)

col2.metric(
    "Machines",
    product_df["machine_id"].nunique()
)

col3.metric(
    "Warnings",
    warning
)

col4.metric(
    "Critical",
    critical
)

# ==========================================
# AI SUMMARY
# ==========================================

st.markdown("---")

if critical > 50:

    st.error(
        f"""
        AI Alert

        {product} production line is showing
        elevated operational risk.

        Immediate inspection recommended.
        """
    )

elif warning > 100:

    st.warning(
        f"""
        AI Warning

        {product} production line requires
        preventive maintenance review.
        """
    )

else:

    st.success(
        f"""
        AI Assessment

        {product} production line is operating
        within safe limits.
        """
    )

# ==========================================
# RISK DISTRIBUTION
# ==========================================

st.markdown("---")

st.subheader(
    f"{product} Risk Distribution"
)

risk_chart = pd.DataFrame({
    "Status":[
        "Healthy",
        "Warning",
        "Critical"
    ],
    "Count":[
        healthy,
        warning,
        critical
    ]
})

st.bar_chart(
    risk_chart.set_index(
        "Status"
    )
)

# ==========================================
# TOP RISK MACHINES
# ==========================================

st.markdown("---")

st.subheader(
    "Top Risk Machines"
)

if product == "Seat Belt":

    top_risk = product_df.sort_values(
        by=[
            "temperature",
            "vibration",
            "defect_count"
        ],
        ascending=False
    )

elif product == "Airbag":

    top_risk = product_df.sort_values(
        by=[
            "pressure",
            "sensor_accuracy",
            "defect_count"
        ],
        ascending=[False, True, False]
    )

elif product == "Steering":

    top_risk = product_df.sort_values(
        by=[
            "torque",
            "motor_current",
            "vibration"
        ],
        ascending=False
    )

else:

    top_risk = product_df.sort_values(
        by=[
            "defect_count",
            "temperature"
        ],
        ascending=False
    )

st.dataframe(
    top_risk[
        [
            "machine_id",
            "temperature",
            "vibration",
            "motor_current",
            "defect_count"
        ]
    ].head(10),
    use_container_width=True,
    hide_index=True
)

# ==========================================
# AI RECOMMENDATIONS
# ==========================================

st.markdown("---")

st.subheader(
    "AI Recommendations"
)

for _, row in top_risk.head(5).iterrows():

    st.info(
        f"""
Machine {row['machine_id']}

Temperature : {round(row['temperature'],1)}°C

Vibration : {round(row['vibration'],2)}

Defects : {row['defect_count']}

Recommended Action :
Inspect immediately and schedule preventive maintenance.
"""
    )

# ==========================================
# AI DECISION FACTORS
# ==========================================

st.markdown("---")

st.subheader(
    "AI Decision Factors"
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
    "Importance":
    model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

# ==========================================
# PRODUCT SPECIFIC RISK DRIVER
# ==========================================

if product == "Seat Belt":

    top_feature = "Temperature"
    impact = 40

elif product == "Airbag":

    top_feature = "Pressure"
    impact = 45

elif product == "Steering":

    top_feature = "Torque"
    impact = 40

else:

    top_feature = "Defect Count"
    impact = 50

c1,c2,c3 = st.columns(3)

c1.metric(
    "Top Risk Driver",
    top_feature.title()
)

c2.metric(
    "Impact Score",
    f"{impact}%"
)

c3.metric(
    "Features Analysed",
    len(features)
)

if product == "Seat Belt":

    factor_df = pd.DataFrame({
        "Factor":[
            "Temperature",
            "Vibration",
            "Defect Count"
        ],
        "Impact":[
            40,
            35,
            25
        ]
    })

elif product == "Airbag":

    factor_df = pd.DataFrame({
        "Factor":[
            "Pressure",
            "Sensor Accuracy",
            "Defect Count"
        ],
        "Impact":[
            45,
            35,
            20
        ]
    })

elif product == "Steering":

    factor_df = pd.DataFrame({
        "Factor":[
            "Torque",
            "Motor Current",
            "Vibration"
        ],
        "Impact":[
            40,
            35,
            25
        ]
    })

else:

    factor_df = pd.DataFrame({
        "Factor":[
            "Defect Count",
            "Sensor Accuracy",
            "Temperature"
        ],
        "Impact":[
            50,
            30,
            20
        ]
    })

st.bar_chart(
    factor_df.set_index(
        "Factor"
    )
)

st.dataframe(
    importance,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "AI Intelligence • Product Risk Intelligence Dashboard"
)
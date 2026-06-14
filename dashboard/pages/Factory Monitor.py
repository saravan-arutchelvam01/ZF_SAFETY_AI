import streamlit as st
import pandas as pd
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

from scripts.db_connection import engine

# ==========================================
# AZURE SPECTRUM THEME
# ==========================================

st.markdown("""
<style>

.monitor-title{
    font-size:34px;
    font-weight:700;
    color:#1E3A8A;
}

.monitor-subtitle{
    color:#64748B;
    margin-bottom:25px;
}

.machine-card{
    background:white;
    padding:18px;
    border-radius:16px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom:15px;
}

.health-good{
    color:#22C55E;
    font-weight:bold;
}

.health-warning{
    color:#F59E0B;
    font-weight:bold;
}

.health-critical{
    color:#DC2626;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

query = """
SELECT * FROM production_data
"""

df = pd.read_sql(query, engine)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <div class='monitor-title'>
        Factory Monitor
    </div>

    <div class='monitor-subtitle'>
        Real-Time Production Line Monitoring
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# COMPONENT FILTER
# ==========================================

component = st.selectbox(
    "Select Production Line",
    df["component_type"].unique()
)

filtered = df[
    df["component_type"] == component
]

# ==========================================
# COMPONENT HEALTH
# ==========================================

critical = len(
    filtered[
        filtered["risk_level"] == 2
    ]
)

warning = len(
    filtered[
        filtered["risk_level"] == 1
    ]
)

healthy = len(
    filtered[
        filtered["risk_level"] == 0
    ]
)

health_score = round(
    (
        healthy /
        len(filtered)
    ) * 100,
    1
)

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Health Score",
    f"{health_score}%"
)

col2.metric(
    "Healthy",
    healthy
)

col3.metric(
    "Warning",
    warning
)

col4.metric(
    "Critical",
    critical
)

if critical > 0:

    st.error(
        f"""
        {critical} critical machine records detected
        in the {component} production line.
        """
    )

elif warning > 0:

    st.warning(
        f"""
        {warning} warning records detected
        in the {component} production line.
        """
    )

else:

    st.success(
        f"""
        {component} production line operating normally.
        """
    )

    

st.markdown("---")

# ==========================================
# LIVE MACHINE STATUS
# ==========================================

st.subheader(
    "Live Machine Status"
)

machines = (
    filtered
    .groupby("machine_id")
    .tail(1)
)

status_table = machines[
    [
        "machine_id",
        "temperature",
        "vibration",
        "motor_current",
        "defect_count",
        "risk_level"
    ]
].copy()

status_table["Status"] = (
    status_table["risk_level"]
    .map({
        0: "🟢 Healthy",
        1: "🟡 Warning",
        2: "🔴 Critical"
    })
)

status_table = status_table[
    [
        "machine_id",
        "Status",
        "temperature",
        "vibration",
        "motor_current",
        "defect_count"
    ]
]

st.dataframe(
    status_table,
    use_container_width=True,
    hide_index=True,
    height=450
)

st.markdown("---")

# ==========================================
# TEMPERATURE TREND
# ==========================================

left,right = st.columns(2)

with left:

    st.subheader(
        "Temperature Trend"
    )

    st.line_chart(
        filtered["temperature"].tail(100)
    )

with right:

    st.subheader(
        "Vibration Trend"
    )

    st.line_chart(
        filtered["vibration"].tail(100)
    )

# ==========================================
# RISK DISTRIBUTION
# ==========================================

st.subheader(
    "Risk Distribution"
)

risk_df = pd.DataFrame({
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
    risk_df.set_index(
        "Status"
    )
)

# ==========================================
# ATTENTION REQUIRED
# ==========================================

st.subheader(
    "Attention Required"
)

attention = filtered[
    filtered["risk_level"] == 2
]

if len(attention) > 0:

    st.dataframe(
        attention[
            [
                "machine_id",
                "temperature",
                "vibration",
                "motor_current",
                "defect_count"
            ]
        ].head(10),
        use_container_width=True
    )

else:

    st.success(
        "No machines require immediate attention."
    )
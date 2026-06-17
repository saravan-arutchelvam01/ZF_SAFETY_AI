import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)

import streamlit as st
import pandas as pd

from streamlit_autorefresh import st_autorefresh

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="ZF Safety Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# AUTO REFRESH
# ==========================================

st_autorefresh(
    interval=5000,
    key="refresh"
)

# ==========================================
# AZURE SPECTRUM THEME
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #F8FAFC;
}

.block-container {
    padding-top: 1rem;
}

.dashboard-title {
    font-size: 38px;
    font-weight: 700;
    color: #1E3A8A;
    margin-bottom: 0;
}

.dashboard-subtitle {
    color: #64748B;
    margin-bottom: 10px;
}

.kpi-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.06);
    border-top: 5px solid #2563EB;
}

.kpi-label {
    color: #64748B;
    font-size: 14px;
}

.kpi-value {
    font-size: 34px;
    font-weight: 700;
    color: #0F172A;
}

.action-card {
    background: white;
    padding: 12px;
    border-radius: 16px;
    border-left: 6px solid #DC2626;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 12px;
}

.section-header {
    color: #1E3A8A;
    font-size: 24px;
    font-weight: 600;
}

.status-banner {
    background: #DBEAFE;
    padding: 12px;
    border-radius: 12px;
    border-left: 6px solid #2563EB;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("data/production_data.csv")

# ==========================================
# CALCULATIONS
# ==========================================

critical = len(
    df[df["risk_level"] == 2]
)

warning = len(
    df[df["risk_level"] == 1]
)

healthy = len(
    df[df["risk_level"] == 0]
)

machines = df["machine_id"].nunique()

components = df["component_type"].nunique()

plant_health = round(
    (healthy / len(df)) * 100,
    1
)

production_efficiency = round(
    100 - ((critical + warning) / len(df) * 100),
    1
)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <div class='dashboard-title'>
        ZF Safety Analytics
    </div>

    <div class='dashboard-subtitle'>
        AI-Driven Predictive Safety Analytics for Industry 4.0
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Seat Belt Systems • Airbag Systems • Steering Systems • Occupant Safety Components"
)
# ==========================================
# STATUS BANNER
# ==========================================

if critical > 0:

    st.markdown(
        f"""
        <div class='status-banner'>
            <strong>Attention Required</strong><br>
            {critical} critical production records detected.
            Review priority actions below.
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.success(
        "Plant operating within safe limits."
    )

# ==========================================
# KPI CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>
                Plant Health
            </div>
            <div class='kpi-value'>
                {plant_health}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>
                Critical Alerts
            </div>
            <div class='kpi-value'>
                {critical}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>
                Machines
            </div>
            <div class='kpi-value'>
                {machines}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>
                Production Efficiency
            </div>
            <div class='kpi-value'>
                {production_efficiency}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# PLANT HEALTH STATUS
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-header'>Plant Health Status</div>",
    unsafe_allow_html=True
)

st.progress(
    plant_health / 100
)

st.caption(
    f"Current Plant Health Score : {plant_health}%"
)

# ==========================================
# FACTORY CONTROL ROOM
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-header'>Factory Control Room</div>",
    unsafe_allow_html=True
)

component_health = []

for component in [
    "Seat Belt",
    "Airbag",
    "Steering",
    "Occupant Safety"
]:

    temp_df = df[
        df["component_type"] == component
    ]

    if len(temp_df) == 0:

        score = 0

    else:

        healthy_count = len(
            temp_df[
                temp_df["risk_level"] == 0
            ]
        )

        score = round(
            healthy_count /
            len(temp_df) * 100,
            1
        )

    component_health.append(
        [component, score]
    )

c1, c2, c3, c4 = st.columns(4)

cards = [c1, c2, c3, c4]

for i, (component, score) in enumerate(component_health):

    if score >= 90:

        cards[i].success(
            f"""
            {component}

            🟢 Healthy

            Health Score: {score}%
            """
        )

    elif score >= 75:

        cards[i].warning(
            f"""
            {component}

            🟡 Warning

            Health Score: {score}%
            """
        )

    else:

        cards[i].error(
            f"""
            {component}

            🔴 Critical

            Health Score: {score}%
            """
        )   

# ==========================================
# MAIN SECTION
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    "<div class='section-header'>Production Risk Overview</div>",
    unsafe_allow_html=True
)

risk_col1, risk_col2, risk_col3 = st.columns(3)

risk_col1.metric(
    "Healthy",
    healthy
)

risk_col2.metric(
    "Warning",
    warning
)

risk_col3.metric(
    "Critical",
    critical
)

# ==========================================
# FACTORY STATUS
# =========================================

st.markdown(
        "<div class='section-header'>Production Risk Overview</div>",
        unsafe_allow_html=True
    )

risk_df = pd.DataFrame({
        "Status": [
            "Healthy",
            "Warning",
            "Critical"
        ],
        "Count": [
            healthy,
            warning,
            critical
        ]
    })

st.bar_chart(
        risk_df.set_index("Status")
    )

# ==========================================
# ACTION CENTER
# ==========================================



st.markdown(
        "<div class='section-header'>Priority Actions</div>",
        unsafe_allow_html=True
    )

critical_df = df[
        df["risk_level"] == 2
    ].sort_values(
        by="temperature",
        ascending=False
    )

action1, action2, action3 = st.columns(3)

top_machines = critical_df.head(3)

for idx, (_, row) in enumerate(top_machines.iterrows()):

    cols = [action1, action2, action3]

    with cols[idx]:

        st.markdown(
            f"""
            <div class='action-card'>

            <strong>
            Machine {row['machine_id']}
            </strong><br><br>

            Component:
            {row['component_type']}<br>

            Temperature:
            {round(row['temperature'],1)}°C<br>

            Defects:
            {row['defect_count']}<br><br>

            Recommended Action:
            Immediate Inspection

            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================
# MACHINE ATTENTION TABLE
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    "<div class='section-header'>Operational Review Queue</div>",
    unsafe_allow_html=True
)

attention = df.sort_values(
    by=[
        "risk_level",
        "temperature",
        "vibration"
    ],
    ascending=False
)

st.dataframe(
    attention[
        [
            "machine_id",
            "component_type",
            "temperature",
            "vibration",
            "motor_current",
            "defect_count"
        ]
    ].head(10),
    use_container_width=True
)

# ==========================================
# TREND
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    "<div class='section-header'>Live Production Trend</div>",
    unsafe_allow_html=True
)

st.line_chart(
    df["temperature"].tail(100)
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "ZF Safety Analytics • Executive Dashboard"
)
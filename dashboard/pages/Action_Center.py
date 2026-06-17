import streamlit as st
import pandas as pd
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

.priority-card{
    background:white;
    padding:20px;
    border-radius:16px;
    border-left:6px solid #DC2626;
    box-shadow:0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom:15px;
}

.action-card{
    background:#DBEAFE;
    padding:18px;
    border-radius:12px;
    border-left:5px solid #2563EB;
    margin-bottom:12px;
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

from scripts.db_connection import load_data

df = load_data()


critical_df = df[
    df["risk_level"] == 2
].copy()

critical_df["risk_score"] = (
    critical_df["temperature"] * 0.4 +
    critical_df["vibration"] * 20 +
    critical_df["defect_count"] * 5
)

critical_df["risk_score"] = (
    critical_df["risk_score"]
    .clip(0,100)
    .round(0)
)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class='page-title'>
Action Center
</div>

<div class='page-subtitle'>
Critical Conditions, Recommended Actions and Maintenance Priorities
</div>
""", unsafe_allow_html=True)

# ==========================================
# KPI SECTION
# ==========================================

critical_count = len(
    critical_df
)

affected_machines = (
    critical_df["machine_id"]
    .nunique()
)

critical_components = (
    critical_df["component_type"]
    .nunique()
)

col1,col2,col3 = st.columns(3)

col1.metric(
    "Critical Events",
    critical_count
)

col2.metric(
    "Affected Machines",
    affected_machines
)

col3.metric(
    "Affected Components",
    critical_components
)

# ==========================================
# STATUS BANNER
# ==========================================

if critical_count > 0:

    st.error(
        f"""
        Immediate Attention Required

        {affected_machines} machines are currently
        operating under critical conditions.
        """
    )

else:

    st.success(
        "No critical machine conditions detected."
    )

# ==========================================
# PRIORITY QUEUE
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>Priority Queue</div>",
    unsafe_allow_html=True
)

priority = critical_df.sort_values(
    by=["risk_score"],
    ascending=False
)

st.dataframe(
    priority[
        [
            "machine_id",
            "component_type",
            "risk_score",
            "temperature",
            "vibration",
            "defect_count"
        ]
    ].head(10),
    use_container_width=True,
    hide_index=True
)

# ==========================================
# AI RECOMMENDATION ENGINE
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>AI Recommendation Engine</div>",
    unsafe_allow_html=True
)

ai_table = priority.head(10).copy()

ai_table["recommended_action"] = (
    ai_table["risk_score"]
    .apply(
        lambda x:
        "Immediate Inspection"
        if x >= 90
        else "Preventive Maintenance"
    )
)

st.dataframe(
    ai_table[
        [
            "machine_id",
            "component_type",
            "risk_score",
            "recommended_action"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ==========================================
# MAINTENANCE RECOMMENDATIONS
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>Maintenance Recommendations</div>",
    unsafe_allow_html=True
)

maintenance_data = []

for _, row in df.tail(100).iterrows():

    if row["temperature"] > 80:

        action = "Inspect Cooling System"

    elif row["vibration"] > 4:

        action = "Check Bearings"

    elif row["motor_current"] > 40:

        action = "Inspect Motor"

    elif row["defect_count"] > 5:

        action = "Quality Inspection"

    else:

        continue

    maintenance_data.append(
        [
            row["machine_id"],
            row["component_type"],
            action
        ]
    )

maintenance_df = pd.DataFrame(
    maintenance_data,
    columns=[
        "Machine",
        "Component",
        "Recommended Action"
    ]
)

st.dataframe(
    maintenance_df.head(15),
    use_container_width=True,
    hide_index=True
)

# ==========================================
# CRITICAL DISTRIBUTION
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>Critical Distribution</div>",
    unsafe_allow_html=True
)

critical_distribution = (
    critical_df["component_type"]
    .value_counts()
)

st.bar_chart(
    critical_distribution
)

# ==========================================
# DETAILED REVIEW
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>Detailed Review</div>",
    unsafe_allow_html=True
)

st.dataframe(
    critical_df[
        [
            "machine_id",
            "component_type",
            "temperature",
            "vibration",
            "motor_current",
            "defect_count",
            "risk_score"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Action Center • Operational Decision Support"
)
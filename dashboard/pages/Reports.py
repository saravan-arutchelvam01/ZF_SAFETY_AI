import streamlit as st
import pandas as pd
import sys
import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

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
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Reports",
    layout="wide"
)

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
SELECT *
FROM production_data
"""

df = pd.read_sql(
    query,
    engine
)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class='page-title'>
Reports
</div>

<div class='page-subtitle'>
Executive Reporting & Operational Summary
</div>
""", unsafe_allow_html=True)

# ==========================================
# KPI SECTION
# ==========================================

total_records = len(df)

critical_records = len(
    df[
        df["risk_level"] == 2
    ]
)

machines = (
    df["machine_id"]
    .nunique()
)

components = (
    df["component_type"]
    .nunique()
)

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Records",
    total_records
)

col2.metric(
    "Critical",
    critical_records
)

col3.metric(
    "Machines",
    machines
)

col4.metric(
    "Components",
    components
)

# ==========================================
# RISK DISTRIBUTION
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>Risk Distribution</div>",
    unsafe_allow_html=True
)

risk_df = pd.DataFrame({
    "Status":[
        "Healthy",
        "Warning",
        "Critical"
    ],
    "Count":[
        len(df[df["risk_level"] == 0]),
        len(df[df["risk_level"] == 1]),
        len(df[df["risk_level"] == 2])
    ]
})

st.bar_chart(
    risk_df.set_index(
        "Status"
    )
)

# ==========================================
# LATEST CRITICAL MACHINES
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>Latest Critical Machines</div>",
    unsafe_allow_html=True
)

critical_df = df[
    df["risk_level"] == 2
]

if len(critical_df) > 0:

    st.dataframe(
        critical_df[
            [
                "machine_id",
                "component_type",
                "temperature",
                "vibration",
                "motor_current",
                "defect_count"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No critical machines detected."
    )

# ==========================================
# PDF GENERATOR
# ==========================================

def generate_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "ZF Safety Analytics",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "Executive Maintenance Report",
            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"Total Records : {total_records}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Critical Records : {critical_records}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Machines : {machines}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Components : {components}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            "Top Critical Machines",
            styles["Heading2"]
        )
    )

    for _, row in critical_df.head(10).iterrows():

        content.append(
            Paragraph(
                f"""
                {row['machine_id']} |
                {row['component_type']} |
                Temp: {round(row['temperature'],1)} |
                Vibration: {round(row['vibration'],1)}
                """,
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            "AI Recommendation",
            styles["Heading2"]
        )
    )

    if critical_records > 100:

        recommendation = (
            "Immediate maintenance action required."
        )

    elif critical_records > 50:

        recommendation = (
            "Preventive maintenance recommended."
        )

    else:

        recommendation = (
            "Plant operating within safe limits."
        )

    content.append(
        Paragraph(
            recommendation,
            styles["BodyText"]
        )
    )

    doc.build(content)

    buffer.seek(0)

    return buffer



# ==========================================
# EXPORT SECTION
# ==========================================

st.markdown("---")

st.markdown(
    "<div class='section-title'>Export Report</div>",
    unsafe_allow_html=True
)

col1,col2 = st.columns(2)

with col1:

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name="ZF_Report.csv",
        mime="text/csv"
    )

with col2:

    pdf_file = generate_pdf()

    st.download_button(
        label="Download PDF Report",
        data=pdf_file,
        file_name="ZF_Executive_Report.pdf",
        mime="application/pdf"
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Reports • Executive Reporting Dashboard"
)
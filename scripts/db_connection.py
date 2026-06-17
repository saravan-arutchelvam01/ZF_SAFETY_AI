import pandas as pd
import os

# ==========================================
# DATA PATH
# ==========================================

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

DATA_FILE = os.path.join(
    project_root,
    "data",
    "production_data.csv"
)

# ==========================================
# LOAD DATA
# ==========================================

def load_data():

    return pd.read_csv(DATA_FILE)
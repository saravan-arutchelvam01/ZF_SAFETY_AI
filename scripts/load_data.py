import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("data/production_data.csv")

engine = create_engine(
    "mysql+pymysql://root:root123@localhost/zf_safety_ai"
)

df.to_sql(
    "production_data",
    con=engine,
    if_exists="append",
    index=False
)

print("Data Inserted Successfully")
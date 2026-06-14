from sqlalchemy import create_engine

DB_USER = "root"
DB_PASSWORD = "root123"
DB_HOST = "localhost"
DB_NAME = "zf_safety_ai"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:Loria%402022@localhost:5432/Food_wastage_db"
)
python3.11 -m venv venv
python generate_data.py
python create_schema.py
python etl_pipeline.py




import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from config import DATABASE_URL


def standardize_state(state):
    state_mapping = {
        "DL": "Delhi"
    }
    return state_mapping.get(state, state)


def run_etl():
    try:
        print("Starting ETL Process...")

        # READ
        df = pd.read_csv("data/raw_patient_data.csv")
        print(f"Loaded {len(df)} records from CSV")

        # TRANSFORM
        df["State"] = df["State"].apply(standardize_state)
        df["Ingestion_Timestamp"] = datetime.now()

        print("Transformation complete")

        # CONNECT DATABASE
        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            # Check which database we are connected to
            result = conn.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print("Connected to database:", db_name)

        # LOAD
        df.to_sql(
            name="patients",
            con=engine,
            if_exists="append",
            index=False,
            method="multi"
        )

        print(f"Successfully inserted {len(df)} records into database!")

        # VERIFY INSERTION
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM patients;"))
            total = result.fetchone()[0]
            print("Total records now in table:", total)

    except Exception as e:
        print("ETL Failed:", e)


if __name__ == "__main__":
    run_etl()


    DATABASE_URL = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
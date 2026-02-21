import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import uuid
from config import DATABASE_URL


def standardize_state(state):
    state_mapping = {
        "DL": "Delhi"
    }
    return state_mapping.get(state, state)


def run_etl():
    try:
        print("🔄 Starting ETL Process...")

        # READ
        df = pd.read_csv("data/raw_patient_data.csv")
        print(f"📥 Loaded {len(df)} records from CSV")

        # TRANSFORM
        df["State"] = df["State"].apply(standardize_state)
        df["Ingestion_Timestamp"] = datetime.now()

        # Convert Patient_ID to UUID type
        df["Patient_ID"] = df["Patient_ID"].astype(str)

        df["Ingestion_Timestamp"] = datetime.now()

        print("✅ Transformation complete")

        engine = create_engine(DATABASE_URL)

        # Insert in smaller chunks (safer)
        df.to_sql(
            name="patients",
            con=engine,
            if_exists="append",
            index=False,
            chunksize=1000
        )

        print(f"🚀 Successfully inserted {len(df)} records!")

        # Verify count
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM patients;"))
            total = result.fetchone()[0]
            print("📊 Total records in DB:", total)

    except Exception as e:
        print("❌ ETL Failed:", e)


if __name__ == "__main__":
    run_etl()
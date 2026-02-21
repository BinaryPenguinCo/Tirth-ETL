import pandas as pd #CSV READING
from sqlalchemy import create_engine, text #DB CONNECTION
from datetime import datetime #TIMESTAMP
import uuid #UNIQUE ID HANDLE KRVA JE PATIENT NI ID ASSSIGN KRELI HOY AE
import traceback
import io #MODULE CREATE IN-MEMORY FILE OBJECT FOR COPY JO TERMINAL COPY COMMAND MA USE THAY CHE
import psycopg2 #PYTHON LIBRARY TO TALK TO POSTGRESQL DATABASE
from config import DATABASE_URL, DB_CONFIG #DB_CONFIG is for psycopg2 connection parameters


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

        # Convert Patient_ID to UUID type
        df["Patient_ID"] = df["Patient_ID"].astype(str)

        df["Last_Visit_Date"] = pd.to_datetime(df["Last_Visit_Date"]).dt.date

        print("Transformation complete")

        engine = create_engine(DATABASE_URL)

        # Try a standard pandas insert first, but capture full errors
        try:
            print("Attempting to insert via pandas.to_sql()...")
            df.to_sql(
                name="patients",
                schema="public",
                con=engine,
                if_exists="append",
                index=False,
                chunksize=1000,
                method="multi"
            )
            print(f"Successfully inserted {len(df)} records via to_sql()!")

        except Exception as e_to_sql:
            print("to_sql() failed — will attempt fast COPY fallback. Error:\n", e_to_sql)
            traceback.print_exc()

            # Fallback: use psycopg2 COPY from an in-memory CSV created from the transformed DataFrame
            try:
                print("Attempting COPY fallback using psycopg2...")
                csv_buffer = io.StringIO()
                # Write DataFrame to csv in memory (include header)
                df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)

                # connect using DB_CONFIG
                with psycopg2.connect(**DB_CONFIG) as conn:
                    with conn.cursor() as cur:
                        # Use COPY with header; table in public schema
                        copy_sql = "COPY public.patients FROM STDIN WITH CSV HEADER"
                        cur.copy_expert(sql=copy_sql, file=csv_buffer)
                    conn.commit()

                print(f"Successfully inserted {len(df)} records via COPY fallback!")

            except Exception as e_copy:
                print("COPY fallback also failed:", e_copy)
                traceback.print_exc()
                raise

        # Verify count
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM patients;"))
                total = result.fetchone()[0]
                print("Total records in DB:", total)
        except Exception:
            print("Could not verify count via SQLAlchemy engine; check DB directly.")

    except Exception as e:
        print("ETL Failed:", e)
        traceback.print_exc()


if __name__ == "__main__":
    run_etl()
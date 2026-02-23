import psycopg2
from config import DB_CONFIG
import pandas as pd


def create_database():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            database="postgres",  # connect to default DB
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"]
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'healthcare_db'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("CREATE DATABASE healthcare_db")
            print("Database created successfully!")
        else:
            print("Database already exists.")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error creating database:", e)


def create_table():

    # read csv
    df = pd.read_csv("data/raw_patient_data.csv")

    columns = df.columns #COLUMN NAMES FROM CSV

    column_list = []

    for col in columns: #HAR COLUMN PR LOOP CHALEGA
        column_list.append(f"{col} VARCHAR(255)")

    columns_sql = ",".join(column_list)

    query = f"""
    CREATE TABLE IF NOT EXISTS patients (
    {columns_sql}
    );
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query)

    conn.commit()

    cursor.close()
    conn.close()

    print("Table created dynamically")


if __name__ == "__main__":
    create_database()
    create_table()
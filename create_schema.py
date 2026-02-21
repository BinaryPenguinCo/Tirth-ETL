import psycopg2
from psycopg2 import sql
from config import DB_CONFIG

def create_database():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
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
            print("ℹ Database already exists.")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error creating database:", e)


def create_table():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS patients (
            Patient_ID UUID PRIMARY KEY,
            Full_Name VARCHAR(150) NOT NULL,
            Age INTEGER,
            Gender VARCHAR(20),
            State VARCHAR(100),
            Blood_Group VARCHAR(5),
            Last_Visit_Date DATE,
            Ingestion_Timestamp TIMESTAMP
        );
        """

        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'patients' created successfully!")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error creating table:", e)


if __name__ == "__main__":
    create_database()
    create_table()
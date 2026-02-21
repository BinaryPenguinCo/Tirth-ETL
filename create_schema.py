import psycopg2
from config import DB_CONFIG


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
    try:
        conn = psycopg2.connect(**DB_CONFIG)  # must include database
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            Patient_ID VARCHAR(50) PRIMARY KEY,
            Full_Name VARCHAR(150) NOT NULL,
            Age INTEGER,
            Gender VARCHAR(20),
            State VARCHAR(100),
            Blood_Group VARCHAR(5),
            Last_Visit_Date DATE,
            Ingestion_Timestamp TIMESTAMP
        );
        """)

        conn.commit()
        print("Table created successfully!")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error creating table:", e)


if __name__ == "__main__":
    create_database()
    create_table()
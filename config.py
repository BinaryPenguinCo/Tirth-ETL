import os

DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "healthcare_db",
    "user": "postgres",
    "password": "admin"
}

DATABASE_URL = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"


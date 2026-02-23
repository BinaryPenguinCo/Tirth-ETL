import uuid #FOR UNIQUE PATIENT ID
import os #CREATE DATA FOLER MATE
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta


fake = Faker(["hi_IN", "en_IN"]) #CREATE FAKER OBJ.                                                                                                                                                              f=o F=c

NUM_RECORDS = 100

# Function to generate one patient record
def generate_patient():
    return {
        "Patient_ID": str(uuid.uuid4()),
        "Full_Name": fake.name(),
        "Age": fake.random_int(),
        "Gender": fake.random_element(),
        "State": fake.state(),
        "Blood_Group": fake.blood_group(),
        "Last_Visit_Date": fake.date(),
        "Doctor_Name": fake.name()
    }


# Function to generate dataset
def generate_dataset(n):
    return [generate_patient() for _ in range(n)]


# Function to save CSV
def save_csv(data):
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/raw_patient_data.csv", index=False)
    print(f"{len(df)} records generated successfully!")


if __name__ == "__main__":
    data = generate_dataset(NUM_RECORDS)
    save_csv(data)
import uuid #FOR UNIQUE PATIENT ID
import random #FOR RANDOM AGE MATE
import os #CREATE DATA FOLER MATE
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta


fake = Faker(["hi_IN", "en_IN"]) #CREATE FAKER OBJ

NUM_RECORDS = 10000

INDIAN_STATES = [
    "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu",
    "Gujarat", "Rajasthan", "Uttar Pradesh", "West Bengal",
    "Punjab", "Kerala", "DL"  
] #LIST

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

data = []

for _ in range(NUM_RECORDS):
    record = {
        "Patient_ID": str(uuid.uuid4()),
        "Full_Name": fake.name(),
        "Age": random.randint(1, 90),
        "Gender": random.choice(["Male", "Female", "Other"]),
        "State": random.choice(INDIAN_STATES),
        "Blood_Group": random.choice(BLOOD_GROUPS),
        "Last_Visit_Date": fake.date_between(start_date="-2y", end_date="today")
    }
    data.append(record)

df = pd.DataFrame(data)

os.makedirs("data", exist_ok=True)
df.to_csv("data/raw_patient_data.csv", index=False)

print("Generated 10,000 Indian patient records successfully!")
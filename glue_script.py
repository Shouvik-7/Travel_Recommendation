import redshift_connector
import pandas as pd
import boto3
import io

s3 = boto3.client('s3')

# Configurations
s3_bucket = 'members-trips-bucket'
s3_key = 'trip_records.csv'
s3_path = f's3://{s3_bucket}/{s3_key}'

# Step 1: Download CSV from S3
response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
csv_data = response['Body'].read()
df = pd.read_csv(io.BytesIO(csv_data))

# Redshift connection and insert
try:
    with redshift_connector.connect(
        host='redshiftwg-member-trips.124849090263.us-east-1.redshift-serverless.amazonaws.com',
        database='dev',
        user='awsuser',
        password='Awsuser13',
        port=5439
    ) as conn:
        with conn.cursor() as cursor:
            # Create table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS member_trips (
                MemberID VARCHAR(10),
                Name VARCHAR(50),
                Age INT,
                Location VARCHAR(100),
                TripDestination VARCHAR(100),
                TripDate TIMESTAMP,
                TripDuration INT,
                TripCost DECIMAL(10, 2),
                TripActivities VARCHAR(255),
                UpdatedAt TIMESTAMP
            )
            """)
            
            # Prepare data
            data = list(df.itertuples(index=False, name=None))
            
            # Insert data
            cursor.executemany("""
                INSERT INTO member_trips (
                    MemberID, Name, Age, Location, TripDestination,
                    TripDate, TripDuration, TripCost, TripActivities, UpdatedAt
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, data)

        conn.commit()
except Exception as e:
    print("Error:", e)

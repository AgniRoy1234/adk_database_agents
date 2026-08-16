import os 
import psycopg2
from google.cloud import bigquery
from dotenv import load_dotenv
load_dotenv()

def connect_to_aws_rds():
    """Establishes and returns a secure connection to the AWS RDS PostgreSQL database."""
    password = os.getenv("AWS_RDS_PASSWORD")
    return psycopg2.connect(
        host=os.getenv("AWS_RDS_HOST"),
        port=os.getenv("AWS_RDS_PORT"),
        database=os.getenv("AWS_RDS_DATABASE"),
        user=os.getenv("AWS_RDS_USER"),
        password=password,
        sslmode="require",
    )

def connect_to_bigquery():
    """Establishes and returns a BigQuery client using project ID from environment variables."""
    project_id = os.getenv("GCP_PROJECT_ID")
    # BigQuery uses application default credentials (ADC). 
    # Ensure GOOGLE_APPLICATION_CREDENTIALS path environment variable is set if running locally.
    return bigquery.Client(project=project_id)
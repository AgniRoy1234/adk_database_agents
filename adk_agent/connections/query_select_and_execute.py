from google.cloud import bigquery
from dotenv import load_dotenv
load_dotenv()

from adk_agent.connections.connections import connect_to_aws_rds, connect_to_bigquery


def execute_select_aws(query, params=None):
  """Executes a SELECT query and returns the results as a list of dictionaries."""
  conn = None
  try:
    conn = connect_to_aws_rds()
    with conn.cursor() as cur:
      cur.execute(query, params or ())
      # Fetch column names from description
      columns = [desc[0] for desc in cur.description]
      rows = cur.fetchall()

      # Map each row to a dictionary
      return [dict(zip(columns, row)) for row in rows]
  except Exception as e:
    print(f"Database select error: {e}")
    raise
  finally:
    if conn:
      conn.close()


def execute_write_aws(query, params=None):
  """Executes an INSERT, UPDATE, or DELETE statement and commits the transaction."""
  conn = None
  try:
    conn = connect_to_aws_rds()
    with conn.cursor() as cur:
      cur.execute(query, params or ())
      conn.commit()
  except Exception as e:
    if conn:
      conn.rollback()  # Rollback transaction on error
    print(f"Database write error: {e}")
    raise
  finally:
    if conn:
      conn.close()


def execute_select_bigquery(query, params=None):
    """Executes a SELECT query on BigQuery and returns the results as a list of dictionaries."""
    try:
        client = connect_to_bigquery()
        
        # Configure query parameters if passed (BigQuery uses QueryJobConfig for params)
        job_config = None
        if params:
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()  
        
        # BigQuery Row objects can be directly converted or mapped to dicts
        return [dict(row.items()) for row in results]
    except Exception as e:
        print(f"BigQuery select error: {e}")
        raise


def execute_write_bigquery(query, params=None):
    """Executes an INSERT, UPDATE, or DDL statement (Data Manipulation Language) in BigQuery."""
    try:
        client = connect_to_bigquery()
        
        job_config = None
        if params:
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            
        query_job = client.query(query, job_config=job_config)
        query_job.result()  # Waits for the write/DML job to finish executing
    except Exception as e:
        print(f"BigQuery write error: {e}")
        raise
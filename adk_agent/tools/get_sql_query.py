import os 
from adk_agent.llm.llm_provider import client , model_name
from dotenv import load_dotenv
load_dotenv() 

def get_big_query_table():
    GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID")
    GCP_DATABASE=os.getenv("GCP_DATABASE")
    GCP_TABLE=os.getenv("GCP_TABLE") 

    big_query_table = f"{GCP_PROJECT_ID}.{GCP_DATABASE}.{GCP_TABLE}"
    return big_query_table

big_query_table = get_big_query_table()

def get_aws_table():

    aws_table = os.getenv("AWS_RDS_TABLE")
    return aws_table

aws_table = get_aws_table()

prompt_path = os.path.join("adk_agent", "prompts", "column_description.txt") 

with open(prompt_path, "r") as f:
    column_description_prompt = f.read() 

def get_big_query_sql(user_query: str):

    prompt = f"""You are a BigQuery SQL generator. Your task is to output ONLY a valid BigQuery SQL query that answers the user query based on the provided schema.

RULES:
1. Output ONLY the raw SQL code.
2. Do NOT wrap the SQL in markdown code blocks (e.g., do not use ```sql ... ```).
3. Do NOT include any explanations, greetings, or extra text.
4. The query must be directly executable in BigQuery.

Table: {big_query_table}
Column Descriptions: {column_description_prompt}
User Query: {user_query}

SQL Query:""" 
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    sql_query = response.text.strip()
    return sql_query

def get_rds_postgres_sql(user_query: str) -> str:
    
    prompt = f"""You are an expert AWS RDS PostgreSQL database administrator and SQL generator. Your task is to output ONLY a valid PostgreSQL SQL query that answers the user query based on the provided schema.

RULES:
1. Output ONLY the raw SQL code.
2. Do NOT wrap the SQL in markdown code blocks (e.g., do not use ```sql ... ```).
3. Do NOT include any explanations, greetings, or extra text.
4. Use standard PostgreSQL syntax (e.g., proper casting, string concatenations, or limit clauses if needed) that is directly executable.

Table: {aws_table}
Column Descriptions: {column_description_prompt}
User Query: {user_query}

SQL Query:""" 
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    # Clean up output just in case stray markdown or whitespace is returned
    sql_query = response.text.strip().removeprefix("```sql").removesuffix("```").strip()
    return sql_query
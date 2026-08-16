# Database Query Agent

A **Google ADK-based multi-database agent** that allows users to query **AWS RDS PostgreSQL** and **Google BigQuery** using natural language.

## Architecture

```text
User Query
    │
    ▼
Database Coordinator
    │
    ├──► AWS RDS Agent ──► PostgreSQL
    │
    └──► BigQuery Agent ──► BigQuery
                │
                ▼
         Raw DB Results
                │
                ▼
        Formatter Agent
                │
                ▼
          User Response
```

## Features

* Natural-language to SQL conversion.
* Supports **AWS RDS PostgreSQL** and **Google BigQuery**.
* Automatically selects the appropriate database.
* Can query both databases when required.
* Limits database tool calls to **3 per invocation**.
* Returns small result sets directly.
* Exports larger result sets as downloadable **CSV artifacts**.
* Dedicated formatter agent for clean, user-friendly responses.
* Uses ADK `ToolContext` for state and artifact management.

## Project Structure

```text
.
├── .gitignore
├── README.md
├── requirements.txt
└── adk_agent/
    ├── agent.py
    ├── connections/
    │   ├── connections.py
    │   └── query_select_and_execute.py
    ├── llm/
    │   └── llm_provider.py
    ├── prompts/
    │   └── column_description.txt
    └── tools/
        ├── db_agents.py
        ├── get_sql_query.py
        └── save_artefacts.py
```

## Result Handling

| Records | Action                       |
| ------: | ---------------------------- |
|       0 | No data found                |
|     1–2 | Return data directly         |
|      >2 | Save results as CSV artifact |

## Example Queries

```text
Show me customers from PostgreSQL with balance greater than 10000.
```

```text
Show total sales by product category for 2024.
```

```text
Compare customer data from AWS with sales data from BigQuery.
```

## Installation

```bash
git clone <YOUR_REPOSITORY_URL>
cd <REPOSITORY_DIRECTORY>

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

On Windows:

```cmd
.venv\Scripts\activate
```

Configure the required environment variables and database credentials before running the agent.

## Running

Using Google ADK:

```bash
adk web
```

The root agent is:

```python
root_agent
```

## Technology Stack

* Python
* Google ADK
* Google Gemini / GenAI
* AWS RDS PostgreSQL
* Google BigQuery
* Pandas
* ADK Artifacts

> **Note:** Do not commit `.env`, credentials, `.adk/`, `__pycache__/`, `*.pyc`, databases, or logs to the repository.

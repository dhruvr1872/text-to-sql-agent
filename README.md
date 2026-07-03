# Text-to-SQL Agent

A ReAct-style AI agent that converts natural language questions into SQL, executes them against your database, and self-corrects on failure — up to N retries.

## How it works

```
Natural language question
    └── Schema extraction (SQLAlchemy introspection)
        └── SQL generation (GPT-4o-mini)
            └── Execution (SQLAlchemy)
                └── On error: fix_sql() → retry (up to 3x)
                    └── Structured results (columns + rows)
```

## Features

- **Schema-aware** — reads your actual table structure before generating SQL
- **Self-correction loop** — feeds SQL errors back to the LLM and retries automatically
- **Multi-dialect** — SQLite, Postgres, MySQL, BigQuery via SQLAlchemy
- **Structured output** — typed columns, rows, row count
- **FastAPI server** — REST endpoint for integration into other services
- **Sample F1 database** — seed and test instantly, no setup required

## Quickstart

```bash
git clone https://github.com/dhruvr1872/text-to-sql-agent
cd text-to-sql-agent
pip install -r requirements.txt
cp .env.example .env
# Add OPENAI_API_KEY to .env

# Seed sample database
python main.py --seed

# Ask questions
python main.py "Which driver has the most wins in 2024?"
python main.py "Show total points per team, sorted descending"
python main.py "Which races did Lando Norris finish on the podium?"

# Use your own database
python main.py "How many users signed up last week?" --db postgresql://user:pass@host/db

# Start API server
python main.py --serve
# POST http://localhost:8001/query  {"question": "..."}
```

## Example output

```
Question: Which driver has the most wins in 2024?
SQL (1 attempt):
  SELECT d.name, COUNT(r.winner_id) AS wins
  FROM drivers d JOIN races r ON d.id = r.winner_id
  WHERE r.year = 2024
  GROUP BY d.name ORDER BY wins DESC LIMIT 1

Results (1 rows):
name           | wins
---            | ---
Max Verstappen | 3
```

## Stack

| Component | Tech |
|---|---|
| LLM | GPT-4o-mini (OpenAI) |
| Orchestration | LangChain |
| DB interface | SQLAlchemy |
| API | FastAPI + uvicorn |
| Config | pydantic-settings |

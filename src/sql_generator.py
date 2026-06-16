"""Generate and repair SQL using an LLM."""
from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import settings

_SYSTEM = """You are an expert SQL query generator.
Given a database schema and a natural language question, write a valid SQL query.

Rules:
- Return ONLY the SQL query — no explanation, no markdown fences
- Prefer simple, readable queries
- Use table aliases for joins
- Never use SELECT * — name each column explicitly"""

_USER = """Schema:
{schema}

Question: {question}

SQL:"""

_FIX_USER = """The following SQL query failed:
{sql}

Error: {error}

Schema:
{schema}

Write a corrected SQL query:"""


def _llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0,
    )


def _clean(sql: str) -> str:
    sql = sql.strip()
    if sql.startswith("```"):
        parts = sql.split("```")
        sql = parts[1] if len(parts) > 1 else sql
        if sql.startswith("sql"):
            sql = sql[3:]
    return sql.strip()


def generate_sql(question: str, schema: str) -> str:
    prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _USER)])
    result = (prompt | _llm()).invoke({"schema": schema, "question": question})
    return _clean(result.content)


def fix_sql(bad_sql: str, error: str, schema: str) -> str:
    prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _FIX_USER)])
    result = (prompt | _llm()).invoke({"sql": bad_sql, "error": error, "schema": schema})
    return _clean(result.content)

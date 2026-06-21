"""
ReAct-style text-to-SQL agent.
Loop: generate SQL -> execute -> on error, fix and retry up to max_retries.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass

from src.config import settings
from src.schema_extractor import extract_schema
from src.sql_generator import generate_sql, fix_sql
from src.executor import execute_sql, QueryResult

logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    question: str
    sql: str
    result: QueryResult | None
    error: str | None
    attempts: int


def run(question: str, database_url: str | None = None) -> AgentResponse:
    db_url = database_url or settings.database_url
    schema = extract_schema(db_url)
    sql = generate_sql(question, schema)
    logger.info("Generated SQL: %s", sql)

    last_error: str | None = None
    for attempt in range(1, settings.max_retries + 1):
        try:
            result = execute_sql(sql, db_url)
            logger.info("Succeeded on attempt %d (%d rows)", attempt, result.row_count)
            return AgentResponse(question=question, sql=sql, result=result, error=None, attempts=attempt)
        except Exception as exc:
            last_error = str(exc)
            logger.warning("Attempt %d failed: %s", attempt, last_error)
            if attempt < settings.max_retries:
                sql = fix_sql(sql, last_error, schema)
                logger.info("Retry SQL: %s", sql)

    return AgentResponse(question=question, sql=sql, result=None, error=last_error, attempts=settings.max_retries)

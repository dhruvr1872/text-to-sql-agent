"""Execute SQL and return structured results."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from sqlalchemy import create_engine, text


@dataclass
class QueryResult:
    columns: list[str]
    rows: list[tuple[Any, ...]]
    row_count: int
    sql: str

    def to_markdown(self) -> str:
        if not self.rows:
            return "(no results)"
        header = " | ".join(self.columns)
        sep = " | ".join("---" for _ in self.columns)
        body = "\n".join(" | ".join(str(v) for v in row) for row in self.rows)
        return f"{header}\n{sep}\n{body}"


def execute_sql(sql: str, database_url: str) -> QueryResult:
    engine = create_engine(database_url)
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        columns = list(result.keys())
        rows = result.fetchall()
    return QueryResult(columns=columns, rows=rows, row_count=len(rows), sql=sql)

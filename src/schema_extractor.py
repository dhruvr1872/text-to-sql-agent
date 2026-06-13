"""Extract database schema to inject as LLM context."""
from __future__ import annotations

from sqlalchemy import create_engine, inspect, text


def extract_schema(database_url: str) -> str:
    """Return a human-readable schema for all tables in the database."""
    engine = create_engine(database_url)
    inspector = inspect(engine)

    lines: list[str] = []
    for table_name in inspector.get_table_names():
        lines.append(f"Table: {table_name}")
        for col in inspector.get_columns(table_name):
            nullable = "" if col["nullable"] else " NOT NULL"
            lines.append(f"  - {col['name']} ({col['type']}){nullable}")
        for fk in inspector.get_foreign_keys(table_name):
            lines.append(
                f"  FK: {fk['constrained_columns']} -> "
                f"{fk['referred_table']}.{fk['referred_columns']}"
            )
        lines.append("")
    return "\n".join(lines)


def sample_rows(database_url: str, table: str, n: int = 3) -> str:
    """Return n sample rows from table as a formatted string."""
    engine = create_engine(database_url)
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table} LIMIT {n}"))
        rows = result.fetchall()
        cols = list(result.keys())
    if not rows:
        return f"(no rows in {table})"
    header = " | ".join(cols)
    body = "\n".join(" | ".join(str(v) for v in row) for row in rows)
    return f"{header}\n{body}"

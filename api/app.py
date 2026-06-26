"""FastAPI server for the text-to-SQL agent."""
from fastapi import FastAPI
from pydantic import BaseModel

from src.agent import run

app = FastAPI(title="Text-to-SQL Agent", version="1.0.0")


class QueryRequest(BaseModel):
    question: str
    database_url: str | None = None


class QueryResponse(BaseModel):
    question: str
    sql: str
    columns: list[str] | None
    rows: list[list] | None
    row_count: int | None
    error: str | None
    attempts: int


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest) -> QueryResponse:
    r = run(req.question, req.database_url)
    return QueryResponse(
        question=r.question,
        sql=r.sql,
        columns=r.result.columns if r.result else None,
        rows=[list(row) for row in r.result.rows] if r.result else None,
        row_count=r.result.row_count if r.result else None,
        error=r.error,
        attempts=r.attempts,
    )


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

#!/usr/bin/env python3
"""CLI for the text-to-SQL agent."""
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Text-to-SQL Agent")
    parser.add_argument("question", nargs="?", help="Natural language question")
    parser.add_argument("--db", help="SQLAlchemy database URL")
    parser.add_argument("--serve", action="store_true", help="Start API server")
    parser.add_argument("--seed", action="store_true", help="Seed sample database")
    args = parser.parse_args()

    if args.seed:
        from data.seed import seed
        seed()
        return

    if args.serve:
        import uvicorn
        uvicorn.run("api.app:app", host="0.0.0.0", port=8001, reload=True)
        return

    if not args.question:
        parser.print_help()
        return

    from src.agent import run
    r = run(args.question, args.db)
    print(f"\nQuestion: {r.question}")
    print(f"SQL ({r.attempts} attempt(s)):\n  {r.sql}")
    if r.result:
        print(f"\nResults ({r.result.row_count} rows):")
        print(r.result.to_markdown())
    else:
        print(f"\nError: {r.error}")


if __name__ == "__main__":
    main()

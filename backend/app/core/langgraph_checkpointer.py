"""LangGraph checkpointer initialization (Postgres-backed).

Goal:
- Use durable Postgres-backed checkpointing for LangGraph conversations.
- Create a single app-lifetime saver instance (avoid per-request MemorySaver).

Configuration:
- Uses `LANGGRAPH_CHECKPOINTER_URL` if set, else falls back to `DATABASE_URL`.
- Only initializes when using PostgreSQL.

Notes:
- The saver uses psycopg (v3) under the hood, separate from SQLAlchemy.
"""

from __future__ import annotations

import inspect
import logging
import os
from typing import Any, Optional

from app.database import DATABASE_URL

logger = logging.getLogger(__name__)

_checkpointer: Optional[Any] = None
_pool: Optional[Any] = None


def _to_postgres_dsn(url: str) -> str:
    """Convert a SQLAlchemy async URL to a psycopg-compatible Postgres DSN."""
    # SQLAlchemy async URLs like: postgresql+asyncpg://user:pass@host/db
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql://", 1)
    if url.startswith("postgresql+psycopg://"):
        return url.replace("postgresql+psycopg://", "postgresql://", 1)
    if url.startswith("postgresql+psycopg2://"):
        return url.replace("postgresql+psycopg2://", "postgresql://", 1)
    return url


async def init_langgraph_checkpointer() -> Optional[Any]:
    global _checkpointer

    if _checkpointer is not None:
        return _checkpointer

    raw_url = os.getenv("LANGGRAPH_CHECKPOINTER_URL") or DATABASE_URL
    dsn = _to_postgres_dsn(raw_url)

    if not dsn.startswith("postgresql://"):
        logger.info("LangGraph checkpointer not initialized (non-Postgres DATABASE_URL)")
        _checkpointer = None
        return None

    try:
        from psycopg_pool import AsyncConnectionPool
        from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
    except Exception:
        logger.warning(
            "LangGraph Postgres saver or psycopg_pool not available. Install 'langgraph-checkpoint-postgres' and 'psycopg[pool]'.",
            exc_info=True,
        )
        _checkpointer = None
        return None

    try:
        # Create a connection pool for the checkpointer to handle reconnects
        _pool = AsyncConnectionPool(
            conninfo=dsn,
            max_size=20,
            min_size=2,
            max_idle=300,
            kwargs={"autocommit": True, "prepare_threshold": None},
        )
        
        # AsyncPostgresSaver can be used with a pool
        _checkpointer = AsyncPostgresSaver(_pool)
        
        # Run setup
        await _checkpointer.setup()

        logger.info("✅ LangGraph Postgres checkpointer initialized with connection pool")
        return _checkpointer
    except Exception:
        logger.error("Failed to initialize LangGraph Postgres checkpointer", exc_info=True)
        _checkpointer = None
        if _pool:
            await _pool.close()
            _pool = None
        return None



def get_langgraph_checkpointer() -> Optional[Any]:
    return _checkpointer


async def close_langgraph_checkpointer() -> None:
    global _checkpointer, _pool
    _checkpointer = None
    pool = _pool
    _pool = None

    if pool is not None:
        try:
            await pool.close()
            logger.info("✅ LangGraph Postgres checkpointer pool closed")
        except Exception:
            logger.warning("Failed to close LangGraph checkpointer pool cleanly", exc_info=True)


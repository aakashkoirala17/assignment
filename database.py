import os
import dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from logger import get_logger
from urllib.parse import quote_plus

# ── Bootstrap ────────────────────────────────────────────────────────────────
dotenv.load_dotenv()
logger = get_logger(__name__)

# ── Read config from environment (Factor III) ─────────────────────────────────
POSTGRES_USER     = os.getenv("POSTGRES_USER",     "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB       = os.getenv("POSTGRES_DB",       "mydatabase")
POSTGRES_PORT     = os.getenv("POSTGRES_PORT",     "5432")
POSTGRES_HOST     = os.getenv("POSTGRES_HOST",     "127.0.0.1")

# URL-encode components to handle special characters (like '@' in password)
USER = quote_plus(POSTGRES_USER)
PWD  = quote_plus(POSTGRES_PASSWORD)
DB   = quote_plus(POSTGRES_DB)

DATABASE_URL = (
    f"postgresql+asyncpg://{USER}:{PWD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB}"
)

# ── Engine (Factor IV) ────────────────────────────────────────────────────────
try:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,        # Set True to log every SQL statement (dev only)
        pool_size=5,
        max_overflow=10,
    )
    logger.info("Database engine created successfully (host=%s db=%s)", POSTGRES_HOST, POSTGRES_DB)
except Exception as exc:
    logger.error("Failed to create database engine: %s", exc)
    raise

# ── Session factory ───────────────────────────────────────────────────────────
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ── Declarative base shared by all models ─────────────────────────────────────
Base = declarative_base()


# ── Dependency injected into every FastAPI route ──────────────────────────────
async def get_db():
    """
    Yield an async database session and guarantee it is closed afterwards.
    FastAPI's dependency-injection system calls this for every request.
    """
    async with AsyncSessionLocal() as session:
        logger.info("Database session opened")
        try:
            yield session
        finally:
            logger.info("Database session closed")

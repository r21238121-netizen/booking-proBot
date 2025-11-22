import asyncpg
from loguru import logger
from config import settings
from .models import init_tables


async def init_db():
    """Initialize the database connection and create tables"""
    try:
        # Create connection pool
        pool = await asyncpg.create_pool(settings.DATABASE_URL)
        
        # Initialize tables
        await init_tables(pool)
        
        logger.info("Database initialized successfully")
        return pool
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def get_db_connection():
    """Get a database connection from the pool"""
    try:
        pool = await init_db()
        return pool
    except Exception as e:
        logger.error(f"Error getting database connection: {e}")
        raise
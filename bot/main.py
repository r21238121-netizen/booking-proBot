import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import settings
from handlers import setup_handlers
from database.database import init_db

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Initialize bot with token from settings
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Initialize Redis storage for FSM (Finite State Machine)
    redis = Redis.from_url(settings.REDIS_URL)
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)
    
    # Initialize database
    db_pool = await init_db()
    
    # Add database pool to dispatcher for global access
    dp['db_pool'] = db_pool
    
    # Setup handlers
    setup_handlers(dp)
    
    logger.info(f"Bot is starting in {'production' if settings.is_production else 'development'} mode...")
    
    if settings.WEBHOOK_URL and not settings.is_production:
        logger.info(f"Webhook URL set to: {settings.WEBHOOK_URL}")
    
    # Start polling
    try:
        if settings.is_production and settings.WEBHOOK_URL:
            # Use webhook in production
            await bot.set_webhook(settings.WEBHOOK_URL)
            await dp.start_webhook(bot, webhook_path='/webhook')
        else:
            # Use polling in development
            await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise
    finally:
        await bot.session.close()
        if 'db_pool' in dp.workflow_data:
            await dp.workflow_data['db_pool'].close()

if __name__ == "__main__":
    asyncio.run(main())
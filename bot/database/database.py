import asyncpg
from loguru import logger
from config import settings


async def init_db():
    """Initialize the database connection and create tables"""
    try:
        # Create connection pool
        pool = await asyncpg.create_pool(
            settings.DATABASE_URL,
            min_size=5,
            max_size=20,
            command_timeout=60
        )
        
        # Initialize tables
        await init_tables(pool)
        
        logger.info("Database initialized successfully")
        return pool
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def get_db_pool():
    """Get the database connection pool"""
    try:
        pool = await init_db()
        return pool
    except Exception as e:
        logger.error(f"Error getting database connection: {e}")
        raise


async def init_tables(pool):
    """Create all required tables in the database"""
    async with pool.acquire() as conn:
        # Create users table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_id BIGINT UNIQUE NOT NULL,
                username VARCHAR(255),
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                balance DECIMAL(15, 8) DEFAULT 0,
                total_deposited DECIMAL(15, 8) DEFAULT 0,
                total_won DECIMAL(15, 8) DEFAULT 0,
                total_played BIGINT DEFAULT 0,
                level INTEGER DEFAULT 1,
                experience BIGINT DEFAULT 0,
                referred_by BIGINT,
                is_banned BOOLEAN DEFAULT FALSE,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create transactions table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                transaction_type VARCHAR(50) NOT NULL, -- deposit, withdrawal, game_win, game_loss, bonus
                amount DECIMAL(15, 8) NOT NULL,
                currency VARCHAR(10) DEFAULT 'TON',
                status VARCHAR(20) DEFAULT 'completed', -- pending, completed, failed
                reference_id VARCHAR(255), -- for external transaction ID
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        """)
        
        # Create games table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id SERIAL PRIMARY KEY,
                game_type VARCHAR(50) NOT NULL, -- dice, roulette, slots, etc.
                user_id BIGINT NOT NULL,
                bet_amount DECIMAL(15, 8) NOT NULL,
                win_amount DECIMAL(15, 8) DEFAULT 0,
                game_result JSONB, -- store game-specific results
                is_win BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        """)
        
        # Create deposits table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS deposits (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                amount DECIMAL(15, 8) NOT NULL,
                ton_tx_hash VARCHAR(255) UNIQUE, -- TON transaction hash
                status VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, failed
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        """)
        
        # Create withdrawals table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS withdrawals (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                amount DECIMAL(15, 8) NOT NULL,
                ton_address VARCHAR(255) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, failed
                fee DECIMAL(15, 8) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        """)
        
        # Create referral table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                id SERIAL PRIMARY KEY,
                referrer_id BIGINT NOT NULL,
                referee_id BIGINT NOT NULL,
                reward_amount DECIMAL(15, 8) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referrer_id) REFERENCES users(user_id),
                FOREIGN KEY (referee_id) REFERENCES users(user_id)
            );
        """)
        
        # Create indexes for better performance
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_games_user_id ON games(user_id);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_games_type ON games(game_type);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_deposits_user_id ON deposits(user_id);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_withdrawals_user_id ON withdrawals(user_id);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_referrals_referee ON referrals(referee_id);")
        
        logger.info("All tables created successfully")
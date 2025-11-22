import asyncpg
from loguru import logger


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


async def create_user_if_not_exists(pool, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
    """Create a new user if they don't exist, otherwise update their info"""
    async with pool.acquire() as conn:
        # Check if user already exists
        existing_user = await conn.fetchrow(
            "SELECT user_id FROM users WHERE user_id = $1", user_id
        )
        
        if existing_user:
            # Update user info
            await conn.execute("""
                UPDATE users 
                SET username = $2, first_name = $3, last_name = $4, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = $1
            """, user_id, username, first_name, last_name)
        else:
            # Create new user with starting balance
            await conn.execute("""
                INSERT INTO users (user_id, username, first_name, last_name, balance)
                VALUES ($1, $2, $3, $4, 1000)  -- Starting with 1000 chips
            """, user_id, username, first_name, last_name)


async def get_user_balance(pool, user_id: int):
    """Get user's current balance"""
    async with pool.acquire() as conn:
        result = await conn.fetchrow(
            "SELECT balance FROM users WHERE user_id = $1", user_id
        )
        return result['balance'] if result else 0


async def update_user_balance(pool, user_id: int, amount: float, is_win: bool = False):
    """Update user's balance"""
    async with pool.acquire() as conn:
        if is_win:
            await conn.execute("""
                UPDATE users 
                SET balance = balance + $2, total_won = total_won + $2, total_played = total_played + 1
                WHERE user_id = $1
            """, user_id, amount)
        else:
            await conn.execute("""
                UPDATE users 
                SET balance = balance - $2, total_played = total_played + 1
                WHERE user_id = $1 AND balance >= $2
            """, user_id, amount)
import asyncpg
from loguru import logger
from decimal import Decimal
from typing import Optional, Dict, Any


async def create_user_if_not_exists(pool, user_id: int, username: str = None, first_name: str = None, last_name: str = None, referred_by: int = None):
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
            starting_balance = 1000  # Starting with 1000 chips
            await conn.execute("""
                INSERT INTO users (user_id, username, first_name, last_name, balance, referred_by)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, user_id, username, first_name, last_name, starting_balance, referred_by)

            # If user was referred, record the referral
            if referred_by:
                try:
                    await conn.execute("""
                        INSERT INTO referrals (referrer_id, referee_id, reward_amount)
                        VALUES ($1, $2, 0)
                    """, referred_by, user_id)
                except Exception as e:
                    logger.error(f"Error recording referral: {e}")


async def get_user_balance(pool, user_id: int) -> Decimal:
    """Get user's current balance"""
    async with pool.acquire() as conn:
        result = await conn.fetchrow(
            "SELECT balance FROM users WHERE user_id = $1", user_id
        )
        return result['balance'] if result else Decimal('0')


async def update_user_balance(pool, user_id: int, amount: Decimal, is_win: bool = False) -> bool:
    """Update user's balance, returns True if successful"""
    async with pool.acquire() as conn:
        try:
            if is_win:
                await conn.execute("""
                    UPDATE users 
                    SET balance = balance + $2, total_won = total_won + $2, total_played = total_played + 1
                    WHERE user_id = $1
                """, user_id, amount)
            else:
                # Check if user has enough balance before deducting
                current_balance = await get_user_balance(pool, user_id)
                if current_balance < amount:
                    return False  # Not enough balance
                
                await conn.execute("""
                    UPDATE users 
                    SET balance = balance - $2, total_played = total_played + 1
                    WHERE user_id = $1 AND balance >= $2
                """, user_id, amount)
            
            return True
        except Exception as e:
            logger.error(f"Error updating user balance: {e}")
            return False


async def get_user_stats(pool, user_id: int) -> Dict[str, Any]:
    """Get user's statistics"""
    async with pool.acquire() as conn:
        result = await conn.fetchrow("""
            SELECT user_id, username, first_name, last_name, balance, 
                   total_deposited, total_won, total_played, level, experience
            FROM users 
            WHERE user_id = $1
        """, user_id)
        
        if result:
            return dict(result)
        return None


async def add_transaction(pool, user_id: int, transaction_type: str, amount: Decimal, 
                         currency: str = 'TON', status: str = 'completed', reference_id: str = None):
    """Add a transaction record"""
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO transactions (user_id, transaction_type, amount, currency, status, reference_id)
            VALUES ($1, $2, $3, $4, $5, $6)
        """, user_id, transaction_type, amount, currency, status, reference_id)


async def record_game_result(pool, game_type: str, user_id: int, bet_amount: Decimal, 
                           win_amount: Decimal, game_result: Dict[str, Any], is_win: bool):
    """Record a game result in the database"""
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO games (game_type, user_id, bet_amount, win_amount, game_result, is_win)
            VALUES ($1, $2, $3, $4, $5, $6)
        """, game_type, user_id, bet_amount, win_amount, game_result, is_win)


async def get_top_players(pool, limit: int = 10) -> list:
    """Get top players by balance"""
    async with pool.acquire() as conn:
        results = await conn.fetch("""
            SELECT user_id, username, first_name, last_name, balance, total_won
            FROM users
            ORDER BY balance DESC
            LIMIT $1
        """, limit)
        
        return [dict(row) for row in results]


async def get_user_referrals(pool, user_id: int) -> list:
    """Get user's referrals"""
    async with pool.acquire() as conn:
        results = await conn.fetch("""
            SELECT r.referee_id, u.username, u.first_name, u.last_name, r.reward_amount
            FROM referrals r
            JOIN users u ON r.referee_id = u.user_id
            WHERE r.referrer_id = $1
        """, user_id)
        
        return [dict(row) for row in results]


async def update_user_level_and_xp(pool, user_id: int, xp_gained: int):
    """Update user's experience and level"""
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE users 
            SET experience = experience + $2,
                level = FLOOR((experience + $2) / 1000) + 1
            WHERE user_id = $1
        """, user_id, xp_gained)


async def get_user_by_id(pool, user_id: int):
    """Get user by their Telegram ID"""
    async with pool.acquire() as conn:
        result = await conn.fetchrow(
            "SELECT * FROM users WHERE user_id = $1", user_id
        )
        return result
import random
from typing import Dict, Any
from decimal import Decimal

from database.models import get_user_balance, update_user_balance, record_game_result
from database.database import get_db_pool


class DiceGame:
    """Implementation of the TonDice game"""
    
    def __init__(self):
        self.min_bet = Decimal('10')
        self.max_bet = Decimal('1000')
        self.multiplier = 5  # 5x for correct number, house edge factored in
    
    async def place_bet(self, user_id: int, bet_amount: Decimal, chosen_number: int) -> Dict[str, Any]:
        """
        Place a bet on the dice game
        
        Args:
            user_id: Telegram user ID
            bet_amount: Amount to bet
            chosen_number: Number from 1 to 6 that user chose
            
        Returns:
            Dict with game result
        """
        if not 1 <= chosen_number <= 6:
            return {
                'success': False,
                'message': 'Выберите число от 1 до 6'
            }
        
        if bet_amount < self.min_bet:
            return {
                'success': False,
                'message': f'Минимальная ставка: {self.min_bet}'
            }
        
        if bet_amount > self.max_bet:
            return {
                'success': False,
                'message': f'Максимальная ставка: {self.max_bet}'
            }
        
        # Get database pool
        pool = await get_db_pool()
        
        # Get user balance
        user_balance = await get_user_balance(pool, user_id)
        
        if user_balance < bet_amount:
            return {
                'success': False,
                'message': 'Недостаточно средств на балансе'
            }
        
        # Deduct bet amount from user balance
        success = await update_user_balance(pool, user_id, bet_amount, is_win=False)
        if not success:
            return {
                'success': False,
                'message': 'Ошибка при списании средств'
            }
        
        # Roll the dice
        rolled_number = random.randint(1, 6)
        
        # Check if user won
        is_win = (rolled_number == chosen_number)
        
        result = {
            'success': True,
            'rolled_number': rolled_number,
            'chosen_number': chosen_number,
            'is_win': is_win,
            'bet_amount': bet_amount,
            'win_amount': Decimal('0')
        }
        
        if is_win:
            win_amount = bet_amount * Decimal(str(self.multiplier))
            result['win_amount'] = win_amount
            
            # Add win amount to user balance
            await update_user_balance(pool, user_id, win_amount, is_win=True)
            
            result['message'] = f'🎉 Поздравляем! Выпало {rolled_number}, вы выиграли {win_amount} фишек!'
        else:
            result['message'] = f'😞 Увы! Выпало {rolled_number}, вы поставили на {chosen_number}. Повезет в следующий раз!'
        
        # Store game result in database
        await record_game_result(
            pool, 
            'dice', 
            user_id, 
            bet_amount, 
            result['win_amount'], 
            {'rolled_number': rolled_number, 'chosen_number': chosen_number}, 
            is_win
        )
        
        return result


# Example usage:
# dice_game = DiceGame()
# result = await dice_game.place_bet(user_id=123456789, bet_amount=Decimal('100'), chosen_number=3)
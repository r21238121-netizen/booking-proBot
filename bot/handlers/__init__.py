from .start import setup_start_handlers
from .menu import setup_menu_handlers
from .games import setup_game_handlers


def setup_handlers(dp):
    """Setup all handlers for the bot"""
    setup_start_handlers(dp)
    setup_menu_handlers(dp)
    setup_game_handlers(dp)
# bot/states.py
from aiogram.fsm.state import State, StatesGroup

class MasterApplication(StatesGroup):
    waiting_for_city = State()
    waiting_for_services = State()
    waiting_for_portfolio = State()
    waiting_for_source = State()
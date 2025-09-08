from aiogram.fsm.state import StatesGroup, State

class RegUser(StatesGroup):
    name = State()
    phone = State()
    username = State()

class OrderPackage(StatesGroup):
    category = State()
    city = State()
    package = State()
    description = State()


class BroadcastState(StatesGroup):
    waiting_for_broadcast_text = State()
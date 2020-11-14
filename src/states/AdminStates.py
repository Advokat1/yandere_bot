from aiogram.dispatcher.filters.state import State, StatesGroup


class RemoveConfirmation(StatesGroup):
    need_confirming = State()

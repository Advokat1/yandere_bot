import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
import config.database
from models import User


class ValidateUserMiddleware(BaseMiddleware):
    """
    Middleware для проверки юзеров на существование в базе
    """

    def __init__(self):
        super(ValidateUserMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message

        :param message:
        """
        user = await config.app.storage.get_data(chat=message.chat.id, user=message.from_user.id, default=False)
        print(user)
        if not user:
            user = User.find(message.from_user.id)
            print(user)
            if not user:
                user = User()
                user.id = message.from_user.id
                user.first_name = message.from_user.first_name
                user.last_name = message.from_user.last_name
                user.username = message.from_user.username
                user.save()

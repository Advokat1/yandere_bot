from aiogram import types


async def is_admin(message: types.Message) -> bool:
    from models import User

    user = User.find(message.from_user.id)
    if not user.is_admin:
        await message.answer('Ты не админ!')
        return False

    return True

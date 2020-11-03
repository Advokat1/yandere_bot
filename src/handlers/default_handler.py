from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from config.app import dp


class OrderStates(StatesGroup):
    test_state1 = State()
    test_state2 = State()


@dp.message_handler(commands=['start'], content_types=types.ContentTypes.TEXT, state="*")
async def all_other_messages(message: types.Message):
    await message.answer('Welcome!')


@dp.message_handler(commands=['test_states'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    await message.answer('Start testing states!\nSend any text to continue.')
    await OrderStates.test_state1.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=OrderStates.test_state1)
async def all_other_messages(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await message.reply("You enter in 'test_state1'")
        await OrderStates.next()
    else:
        await message.reply("WHAT IS IT?! I don't understand anything but a text.")


@dp.message_handler(content_types=types.ContentTypes.ANY, state=OrderStates.test_state2)
async def all_other_messages(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await message.reply("You enter in 'test_states2' and finish state group.")
        await state.finish()
    else:
        await message.reply("WHAT IS IT?! I don't understand anything but a text.")


@dp.message_handler(content_types=types.ContentTypes.ANY, state='*')
async def all_other_messages(message: types.Message):
    if message.content_type == "text":
        await message.reply("I don't know what it means...")
    else:
        await message.reply("WHAT IS IT?! I don't understand anything but a text.")

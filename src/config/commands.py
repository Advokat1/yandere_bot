from aiogram.types import BotCommand

list_of_commands = [
    {
        command: "test_states",
        description: "Проверяет работу 'состояний'"
    }
]

commands = [BotCommand(i.command, d.description) for i in list_of_commands]

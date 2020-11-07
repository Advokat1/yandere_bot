from aiogram.types import BotCommand

list_of_commands = [
    {
        'command': 'take',
        'description': '{count=1} Присылает случайные картинки'
    },
    {
        'command': 'admin',
        'description': '[ADMIN ONLY]'
    },
]

commands = [BotCommand(i['command'], i['description']) for i in list_of_commands]

from aiogram.types import BotCommand

list_of_commands = [
    {
        'command': 'give_random_images',
        'description': 'Присылает случайные картинки'
    },
    {
        'command': 'make_admin',
        'description': '[ADMIN ONLY]'
    },
    {
        'command': 'update_list',
        'description': '[ADMIN ONLY]'
    },
    {
        'command': 'init_img',
        'description': '[ADMIN ONLY]'
    },
]

commands = [BotCommand(i['command'], i['description']) for i in list_of_commands]

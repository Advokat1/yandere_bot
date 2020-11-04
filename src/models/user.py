from orator import Model

__all__ = ['User']


class User(Model):
    __table__ = 'users'
    __incrementing__ = False
    __timestamps__ = True
    __fillable__ = ['id', 'first_name', 'last_name', 'username', 'is_admin']
    __casts__ = {
        'id': 'int',
        'is_admin': 'bool'
    }

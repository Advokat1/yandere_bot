from orator import DatabaseManager, Model
from db import DATABASES

__all__ = ['db', 'DATABASES']

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)

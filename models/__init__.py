#!/usr/bin/python3
"""
    All classes for the AirBnB clone are in this module
"""
from os import getenv

storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()  # Load data from the database
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()

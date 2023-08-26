#!/usr/bin/python3
"""This module defines the DBStorage class for database storage."""
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.state import State
from models.city import City


class DBStorage:
    """This class manages storage for the application using SQLAlchemy."""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage instance."""
        db_user = getenv("HBNB_MYSQL_USER")
        db_pwd = getenv("HBNB_MYSQL_PWD")
        db_host = getenv("HBNB_MYSQL_HOST")
        db_name = getenv("HBNB_MYSQL_DB")
        db_env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}:3306/{}'.
            format(db_user, db_pwd, db_host, db_name),
            pool_pre_ping=True)

        if db_env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending on the class name."""
        objs = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objs[key] = obj
        else:
            for cl in Base.__subclasses__():
                for obj in self.__session.query(cl).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objs[key] = obj
        return objs

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a session."""
        from models.base_model import Base
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

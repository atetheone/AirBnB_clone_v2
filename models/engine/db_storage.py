#!/usr/bin/python3
""" This module defines DBStorage class database """
import os
from models.base_model import Base
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """ Class that manages storage of hbnb models in MySQL db """
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the db engine"""
        from sqlalchemy import create_engine
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(os.environ.get('HBNB_MYSQL_USER'),
                                             os.environ.get('HBNB_MYSQL_PWD'),
                                             os.environ.get('HBNB_MYSQL_HOST'),
                                             os.environ.get('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        objs = []
        if cls:
            objs.extend(self.__session.query(cls).all())
        else:
            for cls in [State, City]:
                objs.extend(self.__session.query(cls).all())
        return {obj.to_dict()['__class__'] + '.' + obj.id: obj
                for obj in objs}

    def new(self, obj):
        """ Adds new object to the current database session """
        self.__session.add(obj)
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete object from current database session """
        if not obj:
            return
        self.__session.delete(obj)

    def reload(self):
        """ Reloads data from the database """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()

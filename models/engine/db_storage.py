#!/usr/bin/python3
""" engine DBstorage"""

import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine


class DBStorage():
    """ private class atttributes """
    __engine = None
    __session = None

    def __init__(self):
        """ iconstructer"""
        from models.base_model import Base

        user = os.environ.get('HBNB_MYSQL_USER')
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST')
        db_name = os.environ.get('HBNB_MYSQL_DB')
        mode = os.environ.get('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user,
                                             password, host,
                                             db_name), pool_pre_ping=True)
        if (mode == "test"):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session depeding on the class """

        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        from console import HBNBCommand

        object_dict = {}
        if cls is None:
            for key in HBNBCommand.classes:
                if key != "BaseModel":
                    val = HBNBCommand.classes[key]
                    for row in self.__session.query(val).all():
                        object_dict.update({'{}.{}'.format(key, row.id): row})
            return object_dict
        else:
            if cls is not BaseModel:
                for row in self.__session.query(cls).all():
                    object_dict.update({'{}.{}'.format(cls, row.id): row})
            return object_dict

    def new(self, obj):
        """ add the object to the current db session"""
        self.__session.add(obj)

    def save(self):
        """ add db to the current db session """
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes object from the current session """
        if not obj:
            return
        
        self.__session.delete(obj)

    def reload(self):
        """ creates table in the db """
        from models.base_model import BaseModel, Base
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(bind=self.__engine,
                                     expire_on_commit=False)
        Session = scoped_session(session_maker)
        self.__session = Session()

    def close(self):
        """ connection reset """
        self.__session.close()
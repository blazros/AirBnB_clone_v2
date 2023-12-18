#!/usr/bin/python3
""" Preparing stuff for sqlAlchemy """
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from os import getenv


class DBStorage:
    """ Create the database storage """
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        pswd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, pswd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Returns a dictionary of __object """
        __dict = {}
        if cls:
            if type(str) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for element in query:
                key = "{}.{}".format(type(element).__name__, element.id)
                __dict[key] = element
        else:
            info_list = [State, City, User, Place, Review, Amenity]
            for item in info_list:
                query = self.__session.query(item)
                for element in  query:
                    key = "{}.{}".format(type(element).__name__, element.id)
                    __dict[key] = element
        return (__dict)

    def new(self, obj):
        """ Adds a new obj to the current DB session """
        self.__session.add(obj)

    def save(self):
        """ Commits all changes of current DB session """
        self.__session.commit()

    def delete(self, obj=None)
        """ deletes an obj from current DB session """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """ create all tables in the database """
        Base.metadata.create_all(self.__engine)
        _session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(_session)
        self.__session = Session()

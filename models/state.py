#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv


class State(BaseModel):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state", cascade="all, delete")

    @property
    def cities(self):
        """ Getter attribute that returns the list of City instances
        with state_id equals to the current State.id
        """

        city_list = []
        for city in list(storage.all(City).values()):
            if city.state_id == self.id:
                city_list.append(city)
        return city_list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import connector

class Restaurant(connector.Manager.Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    owner = Column(String(12), nullable=False)
    address = Column(String(120), nullable=False)
    phone_number = Column(String(120), nullable=False)

class Plate(connector.Manager.Base):
    __tablename__ = 'plate'
    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    ingredients = Column(String(12))
    price = Column(String(120))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship(Restaurant)

class Employee(connector.Manager.Base):
    __tablename__ = 'employers'
    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(12), nullable=False)
    position = Column(String(12), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship(Restaurant)

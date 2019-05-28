from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import connector

class Restaurant(connector.Manager.Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    name = Column(String(50))
    owner = Column(String(12))
    address = Column(String(120))
    phone_number = Column(String(120))

class Plate(connector.Manager.Base):
    __tablename__ = 'plate'
    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    name = Column(String(50))
    ingredients = Column(String(12))
    price = Column(String(120))
    restaurant = relationship(Restaurant)

class Employers(connector.Manager.Base):
    __tablename__ = 'employers'
    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    name = Column(String(50))
    lastname = Column(String(12))
    position = Column(String(12))
    restaurant = relationship(Restaurant)

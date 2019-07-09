from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import connector

class Restaurant(connector.Manager.Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, Sequence('restaurant_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    owner = Column(String(12), nullable=False)
    address = Column(String(120), nullable=False)
    phone_number = Column(String(120), nullable=False)

class Plate(connector.Manager.Base):
    __tablename__ = 'plate'
    id = Column(Integer, Sequence('plate_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    ingredients = Column(String(12))
    price = Column(String(120))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship(Restaurant, foreign_keys=[restaurant_id])

class Employee(connector.Manager.Base):
    __tablename__ = 'employers'
    id = Column(Integer, Sequence('employee_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(12), nullable=False)
    position = Column(String(12), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship(Restaurant, foreign_keys=[restaurant_id])

class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    password = Column(String(12))
    username = Column(String(12))
    employee_id = Column(Integer, ForeignKey('employers.id'))
    employee = relationship(Employee)

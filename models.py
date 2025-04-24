# models.py
from sqlalchemy import create_engine, Column, String, Float, Date, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///budget.db')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    transactions = relationship('Transaction', backref='user')
    budgets = relationship('Budget', backref='user')

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    description = Column(String)
    amount = Column(Float)
    type = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    period = Column(String)
    category = Column(String)
    budget = Column(Float)
    used = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

def create_tables():
    Base.metadata.create_all(engine)

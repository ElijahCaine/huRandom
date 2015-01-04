from sqlalchemy import Column, Integer, String
from huRandom.database import Base

class Submission(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    number = Column(String(255), unique=True)

    def __init__(self, name=None, email=None):
        self.id = id
        self.number = number

    def __repr__(self):
        return '<Number %r>' % (self.name)

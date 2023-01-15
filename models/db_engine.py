""" DB engine & models """

__all__ = [
    'Passwords',
    'session'
]

from sqlalchemy import create_engine
from sqlalchemy import Table, Column
from sqlalchemy import String, Integer, BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pathlib import Path

# DB Engine
db_path = Path(__file__).cwd() / 'models/passwords.db'
engine = create_engine(f"sqlite:////{db_path}", echo=False)

# Explicit DB model
Base = declarative_base()


# Model
class Passwords(Base):
    __table__ = Table(
        'passwords',
        Base.metadata,
        Column('id', Integer, primary_key=True, nullable=False),
        Column('parent', String(255), nullable=False),
        Column('child', String(255), nullable=False),
        Column('title', String(255), nullable=False),
        Column('login', String(255)),
        Column('email', String(255)),
        Column('password', BLOB(), nullable=False),
        Column('url', String(255)),
        Column('phone', String(255)),
        Column('created', String(255), nullable=False, server_default=func.now()),
        Column('modified', String(255), nullable=False, onupdate=func.now())
    )
    __mapper_args__ = {
        'polymorphic_identity': 'passwords',
        'with_polymorphic': '*'
    }


# Session
session = sessionmaker(bind=engine)()

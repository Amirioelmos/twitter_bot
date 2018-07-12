from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, MetaData, Integer, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import and_
from balebot.config import Config
from db.db_config import DatabaseConfig
from balebot.utils.logger import Logger

my_logger = Logger.get_logger()

db_string = DatabaseConfig.db_string
db = create_engine(db_string)
meta = MetaData(db)
Base = declarative_base()
Session = sessionmaker(db)
session = Session()


def create_all_table():
    Base.metadata.create_all(db)
    return True


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String)
    user_id = Column(Integer, nullable=False)
    access_hash = Column(String, nullable=False)
    phone_number = Column(String(13))
    oauth_verifier = Column(String, nullable=False)
    oauth_token = Column(String, nullable=False)
    oauth_token_secret = Column(String, nullable=False)
    is_premium = Column(Boolean, default=False)

    def __init__(self, name, user_id, access_hash, phone_number, oauth_verifier, oauth_token, oauth_token_secret):
        self.name = name
        self.user_id = user_id
        self.access_hash = access_hash
        self.phone_number = phone_number
        self.oauth_verifier = oauth_verifier
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    def __repr__(self):
        return "<User(name='%s',user_id='%i',access_hash='%s', phone_number='%s,oauth_verifier='%s'," \
               "oauth_token='%s',oauth_token_secret='%s',is_premium='%s')>" % (
                   self.name, self.user_id, self.access_hash, self.phone_number, self.is_premium, self.oauth_verifier,
                   self.oauth_token, self.oauth_token_secret)


def insert_user(name, user_id, access_hash, phone_number, oauth_verifier, oauth_token, oauth_token_secret):
    new_user = User(name, user_id, access_hash, phone_number, oauth_verifier, oauth_token, oauth_token_secret)
    try:
        session.add(new_user)
        session.commit()
        return new_user
    except ValueError:
        return False

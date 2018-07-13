from sqlalchemy import create_engine
from sqlalchemy import Column, String, MetaData, Integer, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.dialects.postgresql import insert
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
    user_id = Column(Integer, nullable=False, unique=True)
    access_hash = Column(String, nullable=False)
    phone_number = Column(String(13))
    final_oauth_token = Column(String, nullable=False)
    final_oauth_token_secret = Column(String, nullable=False)
    is_premium = Column(Boolean, default=False)

    def __init__(self, name, user_id, access_hash, phone_number, final_oauth_token, final_oauth_token_secret):
        self.name = name
        self.user_id = user_id
        self.access_hash = access_hash
        self.phone_number = phone_number
        self.final_oauth_token = final_oauth_token
        self.final_oauth_token_secret = final_oauth_token_secret

    def __repr__(self):
        return "<User(name='%s',user_id='%i',access_hash='%s', phone_number='%s," \
               "oauth_token='%s',oauth_token_secret='%s',is_premium='%s')>" % (
                   self.name, self.user_id, self.access_hash, self.phone_number,
                   self.final_oauth_token, self.final_oauth_token_secret, self.is_premium)


def insert_user(name, user_id, access_hash, phone_number, final_oauth_token, final_oauth_token_secret):
    insert_stmt = insert(User).values(name=name, user_id=user_id, access_hash=access_hash, phone_number=phone_number,
                                      final_oauth_token=final_oauth_token,
                                      final_oauth_token_secret=final_oauth_token_secret)
    on_update_stmt = insert_stmt.on_conflict_do_update(
        index_elements=['user_id'],
        set_=dict(name=name, phone_number=phone_number, final_oauth_token=final_oauth_token,
                  final_oauth_token_secret=final_oauth_token_secret))
    try:
        result = db.execute(on_update_stmt)
        session.commit()
        return result
    except ValueError:
        print(ValueError)
        return False


def get_user(user_id):
    return session.query(User).filter(User.user_id == user_id).one_or_none()

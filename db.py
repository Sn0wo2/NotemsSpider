from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DB_FILE

engine = create_engine(
    f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False}
)
Session = scoped_session(sessionmaker(bind=engine))


def get_session():
    return Session()

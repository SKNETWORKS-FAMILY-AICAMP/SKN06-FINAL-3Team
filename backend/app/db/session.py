
import os
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()

user = os.getenv("DB_USER")    
passwd = os.getenv("DB_PASSWD")
host = os.getenv("DB_HOST") 
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")    

Base = declarative_base()

DB_URL = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8'

engine = create_engine(DB_URL, echo=True)
# engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db  # 세션 반환
    finally:
        db.close()
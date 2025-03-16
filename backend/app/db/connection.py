import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),  
    "password": os.getenv("DB_PASSWD"),
    "database": os.getenv("DB_NAME"),
    "charset": "utf8mb4", 
    "cursorclass": pymysql.cursors.DictCursor
}

def get_connection():
    return pymysql.connect(**DB_CONFIG) 

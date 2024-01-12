from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import psycopg2
from psycopg2.extras import RealDictCursor
import time

password = "Sharma@123456"

# URL-encode the password
encoded_password = quote_plus(password)

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Sharma@123456',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database is connected")
#         break  
#     except Exception as error:
#         print("Databse is not connected")
#         print("Error :",error)
#         time.sleep(2)
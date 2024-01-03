from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from .routers import post, user, auth
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Sharma@123456',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database is connected")
        break  
    except Exception as error:
        print("Databse is not connected")
        print("Error :",error)
        time.sleep(2)
    
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


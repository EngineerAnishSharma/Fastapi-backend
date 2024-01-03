from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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

@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post:Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, 
                   (new_post.title, new_post.content,new_post.published))
    conn.commit()
    new_post = cursor.fetchone()
    
    return {"data":new_post}

@app.get("/posts/{id}")
def get_posts(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":f"Id:{id} is not found"})
    
    return {"post_details":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id doest not exists.")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found id :{id}")
    
    return {"data":updated_post}
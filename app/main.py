from fastapi import FastAPI
from . import models
from .database import engine, get_db
from .routers import post, user, auth
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
  
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


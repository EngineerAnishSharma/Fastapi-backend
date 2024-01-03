from fastapi import Response, status, HTTPException,Depends, APIRouter
from typing import List
from .. import models, schema,oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model= List[schema.Post])
def get_post(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post).all()
    return posts
    

@router.post("/",status_code=status.HTTP_201_CREATED, response_model= schema.Post)
def create_posts(new_post:schema.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = models.Post(owner_id = current_user.id, **new_post.dict())      #pydantic model have idea of dict property but dont have idea of sqlalchemy model
    db.add(post)
    db.commit()
    db.refresh(post)
    print(current_user.email)
    return post
   
@router.get("/{id}", response_model= schema.Post)
def get_posts(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":f"Id:{id} is not found"})
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id doest not exists.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found id :{id}")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    # post_query.update({'title':updated_post.title,"content":updated_post.content},synchronize_session=False)
    db.commit()
    return post_query.first()
from fastapi import status, HTTPException,Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schema, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
# def login(user_credentials: schema.UserLogin, db: Session = Depends(get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email ==user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!(email)")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    
    return {"access_token":access_token,"token_type":"bearer"}
    

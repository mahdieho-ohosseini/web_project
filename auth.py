
from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from db import schemas
from datetime import datetime, timedelta, timezone
from db import models
from db.engine import get_db
from db.models import USERS ,DOCTORS
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
oauth3_scheme = OAuth2PasswordBearer(tokenUrl="/doctor/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

#tanzimat jwt
SECRET_KEY = "YOMAMANOTAHOE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440




# ایجاد توکن

def create_access_token(username: str,user_id:int, role : str ,expires_delta: Optional[timedelta] = None):
    to_encode = {
        'sub' : username , 
        'id': user_id ,
        'role': role
    }
    expires = datetime.utcnow() + expires_delta
    to_encode.update({"exp":expires}) 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
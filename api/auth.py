from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from database.mongo import database
from app.core.security import (
    get_password_hash, verify_password, 
    create_access_token, create_refresh_token,
    SECRET_KEY, ALGORITHM
)
from app.schemas.token import Token

router = APIRouter(prefix="/auth", tags=["Auth"])
users_collection = database.get_collection("users")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"username": user_in.username})
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = get_password_hash(user_in.password)
    await users_collection.insert_one({
        "username": user_in.username,
        "password": hashed_password
    })
    return {"msg": "User created successfully"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    return {
        "access_token": create_access_token(user["username"]),
        "refresh_token": create_refresh_token(user["username"]),
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        username = payload.get("sub")
        new_access_token = create_access_token(username)
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate refresh token")
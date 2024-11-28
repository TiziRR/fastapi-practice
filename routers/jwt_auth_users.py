from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 5
SECRET = 'asfafafahapPOSajPS'

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    name: str
    email: str
    disabled : bool

class UserDB(User):
    password: str

users_db = {
    "facha": {
        "username": "facha",
        "name" : "Fachero",
        "email": "facha@hotmail.com",
        "disabled": False,
        "password": "$2a$12$jSFd0B5MRiHlX5mToRcggu4YKI9TYdpFNR9nWxQ58E5DuqAi4HXau"
    },
    "facha2": {
        "username": "facha2",
        "name" : "Fachero2",
        "email": "facha2@hotmail.com",
        "disabled": True,
        "password": "$2a$12$UyqK7mWLv15wIS6S7YcRPOv00mmQ./HG512NiIA5Jb48JZz4jjk06"
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])




def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])




async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas", headers={"WWW-Authenticate": "Bearer"}) 
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception

    return search_user(username)




async def current_user(user: User = Depends(auth_user)): ## token es parte de la Base de Datos
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario deshabilitado")
    return user




@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET,algorithm=ALGORITHM), "token_type": "bearer"}



@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
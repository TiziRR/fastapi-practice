from fastapi import APIRouter
from .models.user_model import User

router = APIRouter(prefix="/users", tags=["users"], responses={404:{"message": "No se encontraron usuarios"}})

users_list = [User(id=1, name="Tiziano", surname="Rossi", age=20),
            User(id=2, name="Facha", surname="Pipa", age=20),
            User(id=3, name="Te", surname="Puse", age=20)]


## GET todos los usuarios
@router.get("/")
async def users():
    return users_list
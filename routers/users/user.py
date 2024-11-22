from fastapi import APIRouter, HTTPException
from .models.user_model import User
from .users import users_list

router = APIRouter(prefix="/user", tags=["user"], responses={404:{"message": "Usuario no encontrado"}})

def search_users(id_func: int):
    users = filter(lambda user: user.id == id_func, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}

# GET
# Path -> Condicion Obligatoria
@router.get("/{id}")
async def user(id: int):
    return search_users(id)

# Query -> Condicion Opcional
@router.get("/")
async def user(id: int):
    return search_users(id)


# POST
@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_users(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    users_list.append(user)
    return user


# PUT
@router.put("/")
async def user(user: User):
    found = False
    for index, usuario_guardado in enumerate(users_list):
        if usuario_guardado.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "El usuario no existe"}
    return user


# DELETE
@router.delete("/{id}")
async def user(id: int):
    found = False
    for index, usuario_guardado in enumerate(users_list):
        if usuario_guardado.id == id:
            del(users_list[index])
            found = True
    
    if not found:
        return {"error": "El usuario no existe"}
    return {"Usuario": "Eliminado con éxito"}

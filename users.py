from fastapi import FastAPI
from pydantic import BaseModel

### Para correr en la terminal -> uvicorn users:app --reload

app = FastAPI()

## Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_list = [User(id=1, name="Tiziano", surname="Rossi", age=20),
            User(id=2, name="Facha", surname="Pipa", age=20),
            User(id=3, name="Te", surname="Puse", age=20)]

def search_users(id_func: int):
    users = filter(lambda user: user.id == id_func, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}


# CRUD

## GET todos los usuarios
@app.get("/users")
async def users():
    return users_list

# POST user
@app.post("/user/")
async def user(user: User):
    if type(search_users(user.id)) == User:
        return {"error": "El usuario ya existe"}
    users_list.append(user)
    return user

# PUT user
@app.put("/user/")
async def user(user: User):
    found = False
    for index, usuario_guardado in enumerate(users_list):
        if usuario_guardado.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "El usuario no existe"}
    return user

# DELETE user
@app.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, usuario_guardado in enumerate(users_list):
        if usuario_guardado.id == id:
            del(users_list[index])
            found = True
    
    if not found:
        return {"error": "El usuario no existe"}
    return {"Usuario": "Eliminado con éxito"}

# Path -> Condicion Obligatoria
@app.get("/user/{id}")
async def user(id: int):
    return search_users(id)

# Query -> Condicion Opcional
@app.get("/user/")
async def user(id: int):
    return search_users(id)
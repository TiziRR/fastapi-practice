### pip install "fastapi[all]"
### Para correr en la terminal -> uvicorn main:app --reload
from fastapi import FastAPI
from routers import products
from routers.users import users, user

app = FastAPI()

# Routes
app.include_router(products.router)
app.include_router(users.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return "¡Hola, FastAPI!"

@app.get("/url")
async def url():
    return {"url_tizi":"https://tiziano-rossi-raczkoski-portfolio.vercel.app/"}
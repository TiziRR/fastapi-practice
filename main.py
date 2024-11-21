### pip install "fastapi[all]"
from fastapi import FastAPI

### Para correr en la terminal -> uvicorn main:app --reload

app = FastAPI()

@app.get("/")
async def root():
    return "¡Hola, FastAPI!"

@app.get("/url")
async def url():
    return {"url_tizi":"https://tiziano-rossi-raczkoski-portfolio.vercel.app/"}
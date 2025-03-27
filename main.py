from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Utilisation de FastAPI"}

@app.get("/bonjour/{name}")
async def say_bonjour(name: str):
    return {"message": f"Salut {name} !"}

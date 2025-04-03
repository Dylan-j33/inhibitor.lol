from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Servir les fichiers statiques (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Servir le fichier HTML principal
@app.get("/")
async def read_root():
    return FileResponse("static/templates/index.html")

@app.get("/api/data")
async def get_data():
    return {"message": "Bienvenue sur Inhibitor.lol", "rank": "Gold IV"}

from fastapi import FastAPI, HTTPException
import httpx
from config import RIOT_API_KEY  # Import de la clé API

app = FastAPI()

# Route pour récupérer un joueur par Riot ID (gameName + tagLine)
@app.get("/riotid/{game_name}/{tag_line}")
async def get_summoner_by_riot_id(game_name: str, tag_line: str):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": RIOT_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    print(response.status_code, response.text)  # Debug ici ⬅️

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)  # Montrer l'erreur exacte

    return response.json()

@app.get("/rank/{game_name}/{tag_line}")
async def get_summoner_rank(game_name: str, tag_line: str):
    riot_id_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": RIOT_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(riot_id_url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération du PUUID")
    
    puuid = response.json()["puuid"]

    # Étape 2 : Récupérer le summonerId à partir du PUUID
    summoner_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(summoner_url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération du summonerId")
    
    summoner_id = response.json()["id"]

    # Étape 3 : Récupérer le rank avec le summonerId
    rank_url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(rank_url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération du rank")
    
    return response.json()


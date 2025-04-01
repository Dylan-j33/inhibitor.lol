import json
import httpx
from fastapi import HTTPException
from config import RIOT_API_KEY  # Import de la clé API

# Fonction pour enregistrer les données dans un fichier JSON
def save_data_to_json(data):
    try:
        # Ouvrir le fichier JSON en mode lecture et écriture
        with open("rank_data.json", "r+") as file:
            # Charger les données existantes dans le fichier
            existing_data = json.load(file)
            # Ajouter les nouvelles données
            existing_data.append(data)
            # Revenir au début du fichier pour réécrire les données
            file.seek(0)
            # Sauvegarder les données mises à jour
            json.dump(existing_data, file, indent=4)
    except FileNotFoundError:
        # Si le fichier n'existe pas, créer un nouveau fichier avec les données
        with open("rank_data.json", "w") as file:
            json.dump([data], file, indent=4)

# Fonction pour récupérer le rank du joueur et l'enregistrer dans le JSON
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
    
    # Récupérer les données du rank
    rank_data = response.json()

    # Créer un objet avec les données importantes
    rank_info = {
        "leagueId": rank_data[0]["leagueId"],
        "queueType": rank_data[0]["queueType"],
        "tier": rank_data[0]["tier"],
        "rank": rank_data[0]["rank"],
        "summonerId": summoner_id,
        "puuid": puuid,
        "leaguePoints": rank_data[0]["leaguePoints"],
        "wins": rank_data[0]["wins"],
        "losses": rank_data[0]["losses"],
        "veteran": rank_data[0]["veteran"],
        "inactive": rank_data[0]["inactive"],
        "freshBlood": rank_data[0]["freshBlood"],
        "hotStreak": rank_data[0]["hotStreak"]
    }

    # Enregistrer les données dans le fichier JSON
    save_data_to_json(rank_info)
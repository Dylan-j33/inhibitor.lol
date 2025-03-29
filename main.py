import httpx
import json

# Remplace cette variable par ta propre clé API Riot
API_KEY = 'ta-cle-api-ici'

# Fonction pour récupérer l'ID d'un invocateur par son nom
async def get_summoner_id(summoner_name, region='na1'):
    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {
        'X-Riot-Token': API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        summoner_data = response.json()
        return summoner_data['id']
    else:
        print(f"Erreur lors de la récupération de l'ID : {response.status_code}")
        return None

# Fonction pour récupérer les données de ligue d'un invocateur
async def get_league_data(summoner_id, region='na1'):
    url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-account/{summoner_id}'
    headers = {
        'X-Riot-Token': API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        league_data = response.json()
        for entry in league_data:
            if entry['queueType'] == 'RANKED_SOLO_5x5':
                return entry
        return None
    else:
        print(f"Erreur lors de la récupération des données de ligue : {response.status_code}")
        return None

# Fonction principale
async def main():
    summoner_name = input("Entrez le nom de l'invocateur : ")
    region = 'na1'  # Remplace par la région de ton choix

    summoner_id = await get_summoner_id(summoner_name, region)
    if summoner_id:
        league_data = await get_league_data(summoner_id, region)
        if league_data:
            rank = league_data['tier']
            division = league_data['rank']
            lp = league_data['leaguePoints']
            print(f"Rank: {rank} {division}, LP: {lp}")
        else:
            print("Aucune donnée de ligue trouvée.")
    else:
        print("Impossible de récupérer l'ID de l'invocateur.")

# Exécuter le programme
import asyncio
asyncio.run(main())

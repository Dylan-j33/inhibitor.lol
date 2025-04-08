from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
import config
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")  # Permet le bon fonctionnement du CSS avec ngrok
templates = Jinja2Templates(directory="templates")

headers = {
    "X-Riot-Token": config.RIOT_API_KEY
}

rank_icons = {
    "IRON": "iron.png",
    "BRONZE": "bronze.png",
    "SILVER": "silver.png",
    "GOLD": "gold.png",
    "PLATINUM": "platinum.png",
    "DIAMOND": "diamond.png",
    "MASTER": "master.png",
    "GRANDMASTER": "grandmaster.png",
    "CHALLENGER": "challenger.png"
}

@app.get("/", response_class=HTMLResponse)
async def nouvelle_page(request: Request):
    return templates.TemplateResponse("listeProfils.html", {"request": request})

@app.get("/{pseudo}/{tagline}", response_class=HTMLResponse)
async def get_player_data(request: Request, pseudo: str, tagline: str):
    async with httpx.AsyncClient() as client:
        # 1. Get PUUID from Riot ID
        account_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{pseudo}/{tagline}"
        account_response = await client.get(account_url, headers=headers)
        if account_response.status_code != 200:
            return templates.TemplateResponse("profil.html", {
                "request": request,
                "error": "Joueur non trouvé"
            })

        puuid = account_response.json()["puuid"]

        # 2. Get summoner ID from PUUID
        summoner_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        summoner_response = await client.get(summoner_url, headers=headers)
        summoner = summoner_response.json()
        summoner_id = summoner["id"]
        profile_icon_id = summoner["profileIconId"]

        icon_url = f"http://ddragon.leagueoflegends.com/cdn/12.4.1/img/profileicon/{profile_icon_id}.png"

        # 3. Get ranked info
        ranked_url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        ranked_response = await client.get(ranked_url, headers=headers)
        ranked_data = ranked_response.json()

        soloq = next((entry for entry in ranked_data if entry["queueType"] == "RANKED_SOLO_5x5"), None)
        flexq = next((entry for entry in ranked_data if entry["queueType"] == "RANKED_FLEX_SR"), None)
        tftq = next((entry for entry in ranked_data if entry["queueType"] == "RANKED_TFT"), None)

        # Get rank icons based on rank
        rank_icon_solo = rank_icons.get(soloq["tier"], "unranked.png") if soloq else "unranked.png"
        rank_icon_flex = rank_icons.get(flexq["tier"], "unranked.png") if flexq else "unranked.png"
        rank_icon_tft = rank_icons.get(tftq["tier"], "unranked.png") if tftq else "unranked.png"

        return templates.TemplateResponse("profil.html", {
            "request": request,
            "pseudo": pseudo,
            "tagline": tagline,
            # SOLOQ
            "rankSoloQ": soloq["tier"] if soloq else "Non classé",
            "divisionSoloQ": soloq["rank"] if soloq else "",
            "lpSoloQ": soloq["leaguePoints"] if soloq else "",
            "rankIconSoloQ": f"/static/img/rank/{rank_icon_solo}",  # Image du rang SoloQ
            # FLEXQ
            "rankFlexQ": flexq["tier"] if flexq else "Non classé",
            "divisionFlexQ": flexq["rank"] if flexq else "",
            "lpFlexQ": flexq["leaguePoints"] if flexq else "",
            "rankIconFlexQ": f"/static/img/rank/{rank_icon_flex}",  # Image du rang FlexQ
            # TFTQ
            "rankTFTQ": tftq["tier"] if tftq else "Non classé",
            "divisionTFTQ": tftq["rank"] if tftq else "",
            "lpTFTQ": tftq["leaguePoints"] if tftq else "",
            "rankIconTFTQ": f"/static/img/rank/{rank_icon_tft}",  # Image du rang TFTQ
            # URL de l'icône d'invocateur
            "iconUrl": icon_url,
        })

# inhibitor.lol

----> Rassembler dpm.lol et mobalytics sur un seul site 

-le nom de l'invocateur
-le rank en classée solo/duo
-le rank des saisons précédentes
-les champions jouées, leur kda et leur winrate ainsi que les cs/mn et dmg/mn
-les autres invocateurs récemment joués avec (3 parties ou +)
-le winrate par role
-l'icone de profil

technos : python / FastAPI / jinja

lancer le site : python -m uvicorn main:app --reload

https://fastapi.tiangolo.com/fr/

TODO : unranked affichage, icone invocateur
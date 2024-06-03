# weerwolven
Werewolves for online. This repository is in dutch.

# inhoud
Deze repository bevat een fastAPI app die een REST API server draait en met een MySQLite database werkt.

# API
Deze app is gemaakt met FastAPI het biedt een documentatie van de API op de website. Om de server te runnen type
```console
fastapi run debug.py
```
(Pas op dat je fastapi moet hebben geinstalleerd bijvoorbeeld door `requirements.txt` te installeren)

Als je het wil gebruiken in development gebruik dan
```console
fastapi dev debug.py
```

# Depencies
Om alle depencies te installeren type
```console
pip install -r requirements.txt
```
Het is aangeraden om dit in een python virtual environment te doen.

# Database
De database is een SQLite database. Om deze lokaal te maken type
```console
alembic upgrade head
```
Deze command kan ook later worden gebruikt om de database up to date te houden.

(Pas op je moet alembic hebben geinstalleerd bijvoorbeeld door `requirements.txt` te installeren)

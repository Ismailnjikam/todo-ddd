from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

app = FastAPI(title="Todo DDD")

# 1. Le routeur de l'API d'abord
app.include_router(router)

# 2. Les fichiers statiques à la racine "/" EN DERNIER,
#    sinon ils interceptent les routes de l'API
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
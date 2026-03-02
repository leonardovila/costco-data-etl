import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from costco_etl.storage.paths import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

app = FastAPI(title="costco-data-etl api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "api ok"}
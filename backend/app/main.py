from fastapi import FastAPI
from sqlalchemy import text

from .database import engine


app = FastAPI(title="EvidenceLens API")


@app.get("/")
def root():
    return {
        "message": "EvidenceLens API is running"
    }

@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT PostGIS_Version();")
        )

        version = result.scalar()

    return {
        "database": "connected",
        "postgis_version": version
    }
import os
from fastapi import FastAPI
from sqlalchemy import text
import cloudinary
from .database import engine
from .cloudinary_config import cloudinary



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


    from .cloudinary_config import cloudinary


@app.get("/cloudinary-test")
def cloudinary_test():
    config = cloudinary.config()

    return {
        "cloudinary": "configured",
        "cloud_name": config.cloud_name,
    }
import os
from fastapi import FastAPI
from sqlalchemy import text
import cloudinary
from .database import engine
from .cloudinary_config import cloudinary
from fastapi import UploadFile, File, HTTPException
import cloudinary.uploader


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

@app.post("/media/upload")
async def upload_media(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        result = cloudinary.uploader.upload(
            contents,
            folder="org_demo/western-ghats",
            resource_type="auto",
        )

        return {
            "success": True,
            "filename": file.filename,
            "public_id": result.get("public_id"),
            "url": result.get("secure_url"),
            "resource_type": result.get("resource_type"),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

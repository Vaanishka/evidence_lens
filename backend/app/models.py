import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, DateTime, ForeignKey, Text, Float, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from .database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    datasets = relationship("Dataset", back_populates="organization")


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    organization_id = Column(UUID(as_uuid=False), ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    cloudinary_folder = Column(String, nullable=False)  # e.g. "org_demo/western-ghats"
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="datasets")
    projects = relationship("Project", back_populates="dataset")


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    dataset_id = Column(UUID(as_uuid=False), ForeignKey("datasets.id"), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)  # e.g. "restoration", "waste", "disaster"
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="projects")
    locations = relationship("Location", back_populates="project")


class Location(Base):
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    project_id = Column(UUID(as_uuid=False), ForeignKey("projects.id"), nullable=False)
    name = Column(String)
    geom = Column(Geometry(geometry_type="POINT", srid=4326, spatial_index=False))  # lat/lng point

    project = relationship("Project", back_populates="locations")
    assets = relationship("MediaAsset", back_populates="location")


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    location_id = Column(UUID(as_uuid=False), ForeignKey("locations.id"), nullable=True)
    cloudinary_public_id = Column(String, nullable=False, unique=True)
    media_type = Column(String, default="image")  # "image" or "video"
    capture_timestamp = Column(DateTime, nullable=True)
    status = Column(String, default="pending_enrichment")
    ai_tags = Column(Text)       # JSON string for now, keep it simple
    caption = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    location = relationship("Location", back_populates="assets")
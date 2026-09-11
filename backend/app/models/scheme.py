"""Scheme model"""
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True, nullable=False)
    department = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Multi-select fields (stored as JSON)
    sectors = Column(JSON, nullable=False)  # ["agriculture", "manufacturing"]
    states = Column(JSON, nullable=False)  # ["Delhi", "Punjab"] or ["all"]
    business_stages = Column(JSON, nullable=False)  # ["existing", "expanding"]
    support_types = Column(JSON, nullable=False)  # ["loan", "subsidy"]
    entrepreneur_types = Column(JSON, nullable=False)  # ["women", "sc", "st", "youth"]

    # Metadata
    benefits = Column(JSON, nullable=False)
    eligibility = Column(JSON, nullable=False)
    documents = Column(JSON, nullable=False)

    # Application
    application_url = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    saved_by = relationship("SavedScheme", back_populates="scheme", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scheme {self.name}>"

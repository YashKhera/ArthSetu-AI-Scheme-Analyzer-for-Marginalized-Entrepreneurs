"""Entrepreneur profile model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class EntrepreneurProfile(Base):
    __tablename__ = "entrepreneur_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Contact Info
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    # Location
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)

    # Demographics
    age_group = Column(String, nullable=False)  # "18-25", "26-35", etc.
    gender = Column(String, nullable=False)  # "male", "female", "other"
    social_category = Column(String, nullable=False)  # "general", "obc", "sc", "st"

    # Business Info
    business_name = Column(String, nullable=False)
    business_sector = Column(String, nullable=False)  # "agriculture", "manufacturing", etc.
    business_stage = Column(String, nullable=False)  # "idea", "planning", "operating", "expanding"

    # Financial
    annual_income_range = Column(String, nullable=False)  # "<10L", "10L-50L", etc.
    employee_range = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")
    requirements = relationship("Requirement", back_populates="profile", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<EntrepreneurProfile {self.full_name}>"

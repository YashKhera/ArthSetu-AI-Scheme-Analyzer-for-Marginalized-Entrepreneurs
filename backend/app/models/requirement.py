"""Requirement model"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("entrepreneur_profiles.id"), nullable=False)

    support_type = Column(String, nullable=False)  # "loan", "subsidy", "training", etc.
    description = Column(String, nullable=True)

    # Relationships
    profile = relationship("EntrepreneurProfile", back_populates="requirements")

    def __repr__(self):
        return f"<Requirement {self.support_type}>"

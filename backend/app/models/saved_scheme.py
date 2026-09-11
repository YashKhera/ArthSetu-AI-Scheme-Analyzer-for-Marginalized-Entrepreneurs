"""SavedScheme junction model"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class SavedScheme(Base):
    __tablename__ = "saved_schemes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="saved_schemes")
    scheme = relationship("Scheme", back_populates="saved_by")

    # Ensure a user can't save the same scheme twice
    __table_args__ = (UniqueConstraint('user_id', 'scheme_id', name='_user_scheme_uc'),)

    def __repr__(self):
        return f"<SavedScheme user={self.user_id} scheme={self.scheme_id}>"

"""Scheme service"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.scheme import Scheme

class SchemeService:

    @staticmethod
    def get_all_schemes(db: Session, skip: int = 0, limit: int = 50) -> List[Scheme]:
        """Fetch all schemes with pagination"""
        schemes = db.query(Scheme).offset(skip).limit(limit).all()
        return schemes

    @staticmethod
    def get_total_count(db: Session) -> int:
        """Get total scheme count"""
        return db.query(Scheme).count()

    @staticmethod
    def search_schemes(db: Session, query: str, skip: int = 0, limit: int = 50) -> List[Scheme]:
        """Search schemes by keyword"""
        search_term = f"%{query}%"

        schemes = db.query(Scheme).filter(
            or_(
                Scheme.name.ilike(search_term),
                Scheme.description.ilike(search_term),
                Scheme.department.ilike(search_term)
            )
        ).offset(skip).limit(limit).all()

        return schemes

    @staticmethod
    def filter_schemes(
        db: Session,
        sector: Optional[str] = None,
        state: Optional[str] = None,
        support_type: Optional[str] = None,
        business_stage: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Scheme]:
        """Filter schemes by criteria"""
        query = db.query(Scheme)

        # Filter by sector
        if sector:
            # JSON array contains check
            query = query.filter(Scheme.sectors.contains([sector]))

        # Filter by state
        if state:
            # Check for "all" or specific state
            query = query.filter(
                or_(
                    Scheme.states.contains(["all"]),
                    Scheme.states.contains([state])
                )
            )

        # Filter by support type
        if support_type:
            query = query.filter(Scheme.support_types.contains([support_type]))

        # Filter by business stage
        if business_stage:
            query = query.filter(Scheme.business_stages.contains([business_stage]))

        schemes = query.offset(skip).limit(limit).all()
        return schemes

    @staticmethod
    def get_scheme_by_id(db: Session, scheme_id: int) -> Scheme:
        """Get scheme details"""
        scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()

        if not scheme:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scheme not found"
            )

        return scheme

    @staticmethod
    def get_schemes_by_ids(db: Session, scheme_ids: List[int]) -> List[Scheme]:
        """Get multiple schemes by IDs"""
        schemes = db.query(Scheme).filter(Scheme.id.in_(scheme_ids)).all()
        return schemes

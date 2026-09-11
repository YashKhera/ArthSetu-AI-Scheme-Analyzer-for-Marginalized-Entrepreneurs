"""Schemes router - serves schemes in the Government Schemes Data Structure"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app.models.scheme_v2 import SchemeV2
from app.utils.serializers import (
    serialize_scheme_full,
    serialize_scheme_summary,
)
from app.schemas.scheme import SchemeListResponse

router = APIRouter()


def _apply_filters(query, search, sector, scheme_type, state, purpose):
    """Apply common filters to a SchemeV2 query."""
    if search:
        term = f"%{search}%"
        query = query.filter(
            or_(
                SchemeV2.name.ilike(term),
                SchemeV2.short_name.ilike(term) if hasattr(SchemeV2, "short_name") else SchemeV2.name.ilike(term),
                SchemeV2.description.ilike(term),
                SchemeV2.ministry.ilike(term),
            )
        )

    if sector:
        query = query.filter(
            (SchemeV2.primary_sector == sector) | (SchemeV2.primary_sector == "all")
        )

    if scheme_type:
        query = query.filter(SchemeV2.scheme_type == scheme_type)

    # Note: `state` filtering is done in Python after fetching because JSON
    # containment across SQLite/PostgreSQL differs.

    if purpose:
        query = query.filter(SchemeV2.supported_purposes.contains([purpose]))

    query = query.filter(SchemeV2.status == "active")
    return query


@router.get("/schemes", response_model=SchemeListResponse)
def get_schemes(
    search: Optional[str] = Query(None, description="Search by name/description/ministry"),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    scheme_type: Optional[str] = Query(None, description="Filter by scheme type (loan, subsidy, ...)"),
    state: Optional[str] = Query(None, description="Filter by state"),
    purpose: Optional[str] = Query(None, description="Filter by purpose"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List schemes (structured format) with optional filters."""
    query = _apply_filters(db.query(SchemeV2), search, sector, scheme_type, state, purpose)

    total = query.count()
    schemes = query.offset(skip).limit(limit).all()

    # Manual state filtering (JSON contains is unreliable across DBs)
    if state:
        schemes = [
            s for s in schemes
            if s.geographic_scope == "national" or not s.states or state in (s.states or [])
        ]

    return SchemeListResponse(
        schemes=[serialize_scheme_summary(s) for s in schemes],
        total=total,
    )


@router.get("/schemes/{scheme_id}")
def get_scheme_details(
    scheme_id: int,
    db: Session = Depends(get_db),
):
    """Get detailed scheme information in the full Government Data Structure."""
    scheme = db.query(SchemeV2).filter(
        SchemeV2.id == scheme_id,
        SchemeV2.status == "active",
    ).first()

    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheme not found",
        )

    return serialize_scheme_full(scheme)


@router.get("/schemes/all/{scheme_id}/raw")
def get_raw_scheme(
    scheme_id: int,
    db: Session = Depends(get_db),
):
    """Internal/diagnostic: return the raw SchemeV2 row for tooling and ingestion checks."""
    scheme = db.query(SchemeV2).filter(SchemeV2.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    from app.utils.serializers import serialize_scheme_recommendation
    return serialize_scheme_recommendation(scheme)
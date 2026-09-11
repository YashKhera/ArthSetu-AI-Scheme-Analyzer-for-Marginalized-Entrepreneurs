"""Saved schemes router (v2 schemes)"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from app.database import get_db
from app.models.saved_scheme import SavedScheme
from app.models.scheme_v2 import SchemeV2
from app.schemas.common import SuccessResponse
from app.utils.serializers import serialize_scheme_summary
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/saved-schemes")
def get_saved_schemes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all saved schemes for current user (v2 structured summaries)."""

    saved = db.query(SavedScheme).filter(
        SavedScheme.user_id == current_user.id
    ).all()

    scheme_ids = [s.scheme_id for s in saved]
    schemes = db.query(SchemeV2).filter(SchemeV2.id.in_(scheme_ids)).all()
    scheme_map = {s.id: s for s in schemes}

    saved_schemes = []
    for s in saved:
        scheme = scheme_map.get(s.scheme_id)
        if scheme:
            saved_schemes.append({
                "saved_at": s.created_at.isoformat(),
                "scheme": serialize_scheme_summary(scheme),
            })

    # Keep newest saves first
    saved_schemes.reverse()

    return {
        "saved_schemes": saved_schemes,
        "total": len(saved_schemes),
    }


@router.post("/saved-schemes/{scheme_id}", status_code=status.HTTP_201_CREATED)
def save_scheme(
    scheme_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save a scheme to user's saved list."""

    # Check if scheme exists in the canonical (v2) table
    scheme = db.query(SchemeV2).filter(
        SchemeV2.id == scheme_id,
        SchemeV2.status == "active",
    ).first()

    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheme not found",
        )

    # Check if already saved
    existing = db.query(SavedScheme).filter(
        SavedScheme.user_id == current_user.id,
        SavedScheme.scheme_id == scheme_id,
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Scheme already saved",
        )

    saved_scheme = SavedScheme(
        user_id=current_user.id,
        scheme_id=scheme_id,
    )

    db.add(saved_scheme)

    try:
        db.commit()
        db.refresh(saved_scheme)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Scheme already saved",
        )

    return SuccessResponse(
        message="Scheme saved successfully",
        data={"saved_at": saved_scheme.created_at.isoformat()},
    )


@router.delete("/saved-schemes/{scheme_id}")
def remove_saved_scheme(
    scheme_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove a scheme from user's saved list."""

    saved_scheme = db.query(SavedScheme).filter(
        SavedScheme.user_id == current_user.id,
        SavedScheme.scheme_id == scheme_id,
    ).first()

    if not saved_scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved scheme not found",
        )

    db.delete(saved_scheme)
    db.commit()

    return SuccessResponse(
        message="Scheme removed from saved",
    )
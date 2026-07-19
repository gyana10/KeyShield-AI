from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import User, UserProfile, Enrollment
from backend.db.schemas import ProfileResponse
from backend.core.dependencies import get_current_email

router = APIRouter(prefix="", tags=["User Profile"])


@router.get("/profile", response_model=ProfileResponse)
def get_profile(
    email: str = Depends(get_current_email),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    enrollment_count = db.query(Enrollment).filter(Enrollment.user_id == user.id).count()

    is_complete = enrollment_count >= 3

    if not profile:
        # Return fallback zero profile if user hasn't completed enrollment
        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "enrollment_complete": is_complete,
            "sample_count": enrollment_count,
            "drift_score": 0.0,
            "hold_mean": 0.0,
            "hold_std": 0.0,
            "flight_mean": 0.0,
            "flight_std": 0.0,
            "total_duration": 0.0,
            "backspaces": 0.0,
            "last_updated": user.created_at
        }

    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "enrollment_complete": is_complete,
        "sample_count": profile.sample_count or enrollment_count,
        "drift_score": profile.drift_score or 0.0,
        "hold_mean": profile.hold_mean,
        "hold_std": profile.hold_std,
        "flight_mean": profile.flight_mean,
        "flight_std": profile.flight_std,
        "total_duration": profile.total_duration,
        "backspaces": profile.backspaces,
        "last_updated": profile.last_updated or profile.created_at
    }

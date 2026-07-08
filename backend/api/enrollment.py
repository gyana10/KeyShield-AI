from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import User
from backend.db.enrollment_model import Enrollment
from backend.db.profile_model import UserProfile
from backend.core.dependencies import get_current_email
from backend.ml.profile_builder import create_profile

import json

router = APIRouter()


@router.post("/enroll")
def enroll(
    data: dict,
    email: str = Depends(get_current_email),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    enrollment = Enrollment(
        user_id=user.id,
        hold_times=json.dumps(data["holdTimes"]),
        flight_times=json.dumps(data["flightTimes"]),
        total_duration=data["totalDuration"],
        backspaces=data["backspaces"]
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    # ---------- PROFILE CREATION ----------
    profile_data = create_profile(data)

    existing_profile = db.query(UserProfile).filter(
        UserProfile.user_id == user.id
    ).first()

    if existing_profile:
        existing_profile.hold_mean = profile_data["hold_mean"]
        existing_profile.hold_std = profile_data["hold_std"]

        existing_profile.flight_mean = profile_data["flight_mean"]
        existing_profile.flight_std = profile_data["flight_std"]

        existing_profile.total_duration = profile_data["total_duration"]
        existing_profile.backspaces = profile_data["backspaces"]

    else:
        profile = UserProfile(
            user_id=user.id,
            **profile_data
        )

        db.add(profile)

    db.commit()

    return {
        "message": "Enrollment Saved",
        "user": user.username,
        "id": enrollment.id
    }
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import User, Enrollment, UserProfile
from backend.db.schemas import KeystrokeData, EnrollmentResponse
from backend.core.dependencies import get_current_email
from backend.ml.profile_engine.builder import ProfileBuilder

router = APIRouter(prefix="", tags=["Enrollment"])

REQUIRED_ENROLLMENT_SAMPLES = 3


@router.post("/enroll", response_model=EnrollmentResponse)
def enroll(
    data: KeystrokeData,
    email: str = Depends(get_current_email),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # Get user's existing enrollments
    existing_enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == user.id
    ).order_by(Enrollment.id.asc()).all()

    current_sample_idx = len(existing_enrollments) + 1

    # Save new enrollment sample
    new_enrollment = Enrollment(
        user_id=user.id,
        sample_index=current_sample_idx,
        hold_times=json.dumps(data.holdTimes),
        flight_times=json.dumps(data.flightTimes),
        total_duration=data.totalDuration,
        backspaces=data.backspaces
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    all_enrollments = existing_enrollments + [new_enrollment]
    total_samples = len(all_enrollments)
    is_complete = total_samples >= REQUIRED_ENROLLMENT_SAMPLES

    # Build/Update UserProfile baseline if >= 3 samples
    if is_complete:
        profile_stats = ProfileBuilder.build_from_enrollments(all_enrollments)

        existing_profile = db.query(UserProfile).filter(
            UserProfile.user_id == user.id
        ).first()

        if existing_profile:
            existing_profile.hold_mean = profile_stats["hold_mean"]
            existing_profile.hold_std = profile_stats["hold_std"]
            existing_profile.flight_mean = profile_stats["flight_mean"]
            existing_profile.flight_std = profile_stats["flight_std"]
            existing_profile.total_duration = profile_stats["total_duration"]
            existing_profile.backspaces = profile_stats["backspaces"]
            existing_profile.sample_count = total_samples
        else:
            new_profile = UserProfile(
                user_id=user.id,
                sample_count=total_samples,
                **profile_stats
            )
            db.add(new_profile)

        db.commit()

    return {
        "message": f"Enrollment sample {current_sample_idx}/{REQUIRED_ENROLLMENT_SAMPLES} saved successfully.",
        "user": user.username,
        "sample_index": current_sample_idx,
        "total_samples": total_samples,
        "enrollment_complete": is_complete
    }
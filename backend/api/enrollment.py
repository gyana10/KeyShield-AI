from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from backend.db.database import get_db
from backend.db.models import User
from backend.db.enrollment_model import Enrollment
from backend.core.dependencies import get_current_email

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

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

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

    return {
        "message": "Enrollment Saved Successfully",
        "user_id": user.id,
        "username": user.username,
        "enrollment_id": enrollment.id
    }
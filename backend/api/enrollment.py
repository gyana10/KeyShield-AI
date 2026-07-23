import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import User, UserProfile, Enrollment
from backend.db.schemas import EnrollmentRequest, EnrollmentResponse
from backend.ml.feature_engineering import extract_keystroke_features, create_behavioral_profile

router = APIRouter(tags=["Enrollment"])


@router.post("/enroll", response_model=EnrollmentResponse)
def enroll_profile(request: EnrollmentRequest, db: Session = Depends(get_db)):
    """
    Processes 5 enrollment raw typing samples of the fixed paragraph.
    Extracts 17 features per sample, builds 1 user behavioral profile, and saves to database.
    """
    raw_samples = request.samples
    if len(raw_samples) < 5:
        raise HTTPException(status_code=400, detail="5 enrollment samples of the fixed paragraph are required.")

    # Ensure default User record exists in DB
    user_record = db.query(User).filter(User.id == 1).first()
    if not user_record:
        user_record = User(id=1, username="demo_user", email="demo@keyshield.ai", password_hash="demo_hash")
        db.add(user_record)
        db.commit()

    # 1. Extract 17 statistical feature vectors for all 5 samples
    extracted_features = []
    for idx, raw_events in enumerate(raw_samples):
        events_list = [e.model_dump() for e in raw_events]
        feat_vector = extract_keystroke_features(events_list)
        extracted_features.append(feat_vector)

        db_sample = Enrollment(
            user_id=1,
            sample_index=idx + 1,
            hold_times=json.dumps(events_list),
            flight_times=json.dumps(feat_vector),
            total_duration=feat_vector.get("typing_duration", 0.0),
            backspaces=int(feat_vector.get("backspaces", 0))
        )
        db.add(db_sample)

    # 2. Build 1 Behavioral Profile from 5 samples
    behavioral_profile = create_behavioral_profile(extracted_features)

    # 3. Store/Update UserProfile in Database
    profile_record = db.query(UserProfile).filter(UserProfile.user_id == 1).first()
    if not profile_record:
        profile_record = UserProfile(
            user_id=1,
            sample_count=5,
            hold_mean=behavioral_profile.get("hold_mean", {}).get("mean", 112.0),
            hold_std=behavioral_profile.get("hold_mean", {}).get("std", 12.0),
            flight_mean=behavioral_profile.get("flight_mean", {}).get("mean", 145.0),
            flight_std=behavioral_profile.get("flight_mean", {}).get("std", 18.0),
            total_duration=behavioral_profile.get("typing_duration", {}).get("mean", 2.85),
            backspaces=behavioral_profile.get("backspaces", {}).get("mean", 0.0),
            drift_score=0.0,
            profile_blob=json.dumps(behavioral_profile)
        )
        db.add(profile_record)
    else:
        profile_record.sample_count = 5
        profile_record.hold_mean = behavioral_profile.get("hold_mean", {}).get("mean", 112.0)
        profile_record.hold_std = behavioral_profile.get("hold_mean", {}).get("std", 12.0)
        profile_record.flight_mean = behavioral_profile.get("flight_mean", {}).get("mean", 145.0)
        profile_record.flight_std = behavioral_profile.get("flight_mean", {}).get("std", 18.0)
        profile_record.total_duration = behavioral_profile.get("typing_duration", {}).get("mean", 2.85)
        profile_record.backspaces = behavioral_profile.get("backspaces", {}).get("mean", 0.0)
        profile_record.profile_blob = json.dumps(behavioral_profile)

    db.commit()

    return {
        "message": "Behavioral Profile created successfully from 5 enrollment samples.",
        "enrollment_complete": True,
        "total_samples": 5,
        "profile_summary": {
            "hold_mean": behavioral_profile.get("hold_mean", {}).get("mean", 112.0),
            "flight_mean": behavioral_profile.get("flight_mean", {}).get("mean", 145.0),
            "typing_speed": behavioral_profile.get("typing_speed", {}).get("mean", 180.0),
            "rhythm_score": behavioral_profile.get("rhythm_score", {}).get("mean", 92.0)
        }
    }
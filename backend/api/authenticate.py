from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import User

from backend.db.authentication_log import AuthenticationLog
from backend.db.schemas_auth import AuthenticationRequest

from backend.core.dependencies import get_current_email

from backend.ml.feature_adapter import build_features
from backend.ml.models.predictor import predict

from backend.db.profile_model import UserProfile
from backend.ml.profile_similarity import calculate_similarity

router = APIRouter()


@router.post("/authenticate")
def authenticate(

    data: AuthenticationRequest,

    email: str = Depends(get_current_email),

    db: Session = Depends(get_db)

):

    # Get current user
    user = db.query(User).filter(
        User.email == email
    ).first()

    # Build statistical features
    features = build_features(
        data.model_dump()
    )

    # Load user profile
    profile = db.query(
        UserProfile
    ).filter(
        UserProfile.user_id == user.id
    ).first()

    # Calculate similarity if profile exists
    if profile:

        profile_result = calculate_similarity(
            profile,
            features
        )

    else:

        profile_result = {
            "similarity": 0,
            "explanations": []
        }

    # ML Prediction
    result = predict(
        features
    )

    # Save authentication event
    log = AuthenticationLog(

        user_id=user.id,

        decision=result["decision"],

        anomaly_score=result["anomaly_score"],

        risk=result["risk"],

        profile_similarity=profile_result["similarity"]

    )

    db.add(log)

    db.commit()

    # Return API response
    return {

        "user": user.username,

        "decision": result["decision"],

        "risk": result["risk"],

        "anomaly_score": result["anomaly_score"],

        "profile_similarity": profile_result["similarity"],

        "explanations": profile_result["explanations"]

    }
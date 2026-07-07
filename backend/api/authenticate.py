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

router = APIRouter()


@router.post("/authenticate")
def authenticate(

    data: AuthenticationRequest,

    email: str = Depends(get_current_email),

    db: Session = Depends(get_db)

):

    user = db.query(User).filter(

        User.email == email

    ).first()

    features = build_features(

        data.model_dump()

    )

    result = predict(

        features

    )

    log = AuthenticationLog(

        user_id=user.id,

        decision=result["decision"],

        anomaly_score=result["anomaly_score"],

        risk=result["risk"]

    )

    db.add(log)

    db.commit()

    return {

        "user": user.username,

        **result

    }
from fastapi import APIRouter
from fastapi import Depends

from backend.core.dependencies import get_current_email

from backend.ml.models.predictor import predict

router = APIRouter()


@router.post("/authenticate")
def authenticate(

    data: dict,

    email: str = Depends(get_current_email)

):

    result = predict(data)

    if result["prediction"] == 1:

        decision = "GENUINE"

    else:

        decision = "SUSPICIOUS"

    return {

        "user": email,

        "decision": decision,

        "score": round(result["score"],4)

    }
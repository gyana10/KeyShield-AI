import json
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import User, AuthenticationLog
from backend.db.schemas import HistoryResponse, LogItem
from backend.core.dependencies import get_current_email

router = APIRouter(prefix="", tags=["Authentication History"])


@router.get("/history", response_model=HistoryResponse)
def get_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    email: str = Depends(get_current_email),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    query = db.query(AuthenticationLog).filter(
        AuthenticationLog.user_id == user.id
    ).order_by(AuthenticationLog.created_at.desc())

    total = query.count()
    logs = query.offset(offset).limit(limit).all()

    log_items = []
    for log in logs:
        contribs = json.loads(log.model_contributions) if log.model_contributions else {}
        shap_exp = json.loads(log.shap_explanation) if log.shap_explanation else {}

        log_items.append(
            LogItem(
                id=log.id,
                decision=log.decision,
                risk=log.risk,
                anomaly_score=log.anomaly_score or 0.0,
                profile_similarity=log.profile_similarity or 0.0,
                probability=log.probability or 0.0,
                confidence_score=log.confidence_score or 0.0,
                model_contributions=contribs,
                shap_explanation=shap_exp,
                created_at=log.created_at
            )
        )

    return {
        "total": total,
        "logs": log_items
    }

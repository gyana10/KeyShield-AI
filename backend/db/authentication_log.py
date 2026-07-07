from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from backend.db.database import Base


class AuthenticationLog(Base):

    __tablename__ = "authentication_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    decision = Column(String(30))

    anomaly_score = Column(Float)

    risk = Column(String(20))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
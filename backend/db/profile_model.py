from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from backend.db.database import Base


class UserProfile(Base):

    __tablename__ = "user_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    hold_mean = Column(Float)
    hold_std = Column(Float)

    flight_mean = Column(Float)
    flight_std = Column(Float)

    total_duration = Column(Float)

    backspaces = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
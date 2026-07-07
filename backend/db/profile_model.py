from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from backend.db.database import Base


class BehaviorProfile(Base):

    __tablename__ = "behavior_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    avg_hold_time = Column(Float)

    avg_flight_time = Column(Float)

    avg_duration = Column(Float)

    avg_backspaces = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
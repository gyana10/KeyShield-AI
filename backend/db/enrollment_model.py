from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from backend.db.database import Base


class Enrollment(Base):

    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    hold_times = Column(Text)

    flight_times = Column(Text)

    total_duration = Column(Float)

    backspaces = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
from backend.db.database import engine
from backend.db.models import Base
from backend.db.models import User
from backend.db.enrollment_model import Enrollment
from backend.db.profile_model import BehaviorProfile

Base.metadata.create_all(bind=engine)

print("=" * 50)
print("Database Initialized Successfully")
print("=" * 50)
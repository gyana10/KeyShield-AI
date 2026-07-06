from backend.db.database import engine
from backend.db.models import Base

Base.metadata.create_all(bind=engine)

print("=" * 50)
print("Database Initialized Successfully")
print("=" * 50)
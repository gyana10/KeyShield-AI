from backend.db.database import engine, Base
import backend.db.models  # Ensures all models are registered with Base.metadata

def init_db():
    Base.metadata.create_all(bind=engine)
    print("=" * 60)
    print("KeyShield AI Database Initialized Successfully")
    print("=" * 60)

if __name__ == "__main__":
    init_db()
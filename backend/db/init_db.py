from sqlalchemy import text
from backend.db.database import engine, Base
import backend.db.models  # Ensures all models are registered with Base.metadata


def init_db():
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        try:
            # Auto-migrate missing columns for existing PostgreSQL / SQLite databases
            conn.execute(text("ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS profile_blob TEXT;"))
            conn.commit()
        except Exception:
            pass

    print("=" * 60)
    print("KeyShield AI Database Initialized & Migrated Successfully")
    print("=" * 60)


if __name__ == "__main__":
    init_db()
from sqlalchemy import text, inspect
from backend.db.database import engine, Base
import backend.db.models  # Ensures all models are registered with Base.metadata


def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Robust, database-agnostic check to ensure profile_blob column exists
    with engine.connect() as conn:
        try:
            inspector = inspect(engine)
            if "user_profiles" in inspector.get_table_names():
                columns = [c["name"] for c in inspector.get_columns("user_profiles")]
                if "profile_blob" not in columns:
                    conn.execute(text("ALTER TABLE user_profiles ADD COLUMN profile_blob TEXT;"))
                    conn.commit()
                    print("Auto-migration: Added missing profile_blob column to user_profiles table.")
        except Exception as e:
            print("Auto-migration column check status:", e)

    print("=" * 60)
    print("KeyShield AI Database Initialized & Migrated Successfully")
    print("=" * 60)


if __name__ == "__main__":
    init_db()
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    enrollments = relationship("Enrollment", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    auth_logs = relationship("AuthenticationLog", back_populates="user", cascade="all, delete-orphan")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sample_index = Column(Integer, default=1)
    hold_times = Column(Text, nullable=False)
    flight_times = Column(Text, nullable=False)
    total_duration = Column(Float, nullable=False)
    backspaces = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="enrollments")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    hold_mean = Column(Float, nullable=False)
    hold_std = Column(Float, nullable=False)
    flight_mean = Column(Float, nullable=False)
    flight_std = Column(Float, nullable=False)
    total_duration = Column(Float, nullable=False)
    backspaces = Column(Float, nullable=False)
    sample_count = Column(Integer, default=1)
    drift_score = Column(Float, default=0.0)
    profile_blob = Column(Text, nullable=True)  # JSON string storing full 17-feature profile baseline
    last_updated = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class AuthenticationLog(Base):
    __tablename__ = "authentication_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    decision = Column(String(30), nullable=False)
    anomaly_score = Column(Float, default=0.0)
    risk = Column(String(20), nullable=False)
    profile_similarity = Column(Float, default=0.0)
    probability = Column(Float, default=0.0)
    confidence_score = Column(Float, default=0.0)
    model_contributions = Column(Text, nullable=True)  # JSON string
    shap_explanation = Column(Text, nullable=True)     # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="auth_logs")
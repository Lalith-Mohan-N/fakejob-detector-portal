import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    predictions = relationship("PredictionLog", back_populates="user")


class JobPost(Base):
    __tablename__ = "job_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    location = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    salary_range = Column(String(255), nullable=True)
    company_profile = Column(Text, nullable=True)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    telecommuting = Column(Boolean, default=False)
    has_company_logo = Column(Boolean, default=False)
    has_questions = Column(Boolean, default=False)
    employment_type = Column(String(100), nullable=True)
    required_experience = Column(String(100), nullable=True)
    required_education = Column(String(100), nullable=True)
    industry = Column(String(255), nullable=True)
    function = Column(String(255), nullable=True)
    fraudulent = Column(Boolean, default=False)
    source = Column(String(50), default="manual")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    predictions = relationship("PredictionLog", back_populates="job_post")


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    job_post_id = Column(Integer, ForeignKey("job_posts.id"), nullable=True)

    is_fraudulent = Column(Boolean, nullable=False)
    confidence_score = Column(Float, nullable=False)
    risk_percentage = Column(Float, nullable=False)
    model_used = Column(String(50), nullable=False)
    suspicious_phrases = Column(JSON, default=list)
    explanation = Column(JSON, nullable=True)
    raw_input = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="predictions")
    job_post = relationship("JobPost", back_populates="predictions")

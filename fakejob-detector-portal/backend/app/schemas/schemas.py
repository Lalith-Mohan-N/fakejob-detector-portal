from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class JobPostBase(BaseModel):
    title: str
    location: Optional[str] = None
    department: Optional[str] = None
    salary_range: Optional[str] = None
    company_profile: Optional[str] = None
    description: str
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    telecommuting: bool = False
    has_company_logo: bool = False
    has_questions: bool = False
    employment_type: Optional[str] = None
    required_experience: Optional[str] = None
    required_education: Optional[str] = None
    industry: Optional[str] = None
    function: Optional[str] = None
    fraudulent: Optional[bool] = None


class JobPostCreate(JobPostBase):
    pass


class JobPostUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    fraudulent: Optional[bool] = None


class JobPostOut(JobPostBase):
    id: int
    source: str
    created_at: datetime

    class Config:
        from_attributes = True


class PredictIn(BaseModel):
    title: str
    location: Optional[str] = None
    department: Optional[str] = None
    company_profile: Optional[str] = None
    description: str
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    telecommuting: bool = False
    has_company_logo: bool = False
    has_questions: bool = False
    employment_type: Optional[str] = None
    required_experience: Optional[str] = None
    required_education: Optional[str] = None
    industry: Optional[str] = None
    function: Optional[str] = None


class PredictOut(BaseModel):
    is_fraudulent: bool
    confidence_score: float
    risk_percentage: float
    model_used: str
    suspicious_phrases: List[dict]
    explanation: Optional[dict] = None


class PredictUrlIn(BaseModel):
    url: str = Field(..., pattern=r"^https?://")

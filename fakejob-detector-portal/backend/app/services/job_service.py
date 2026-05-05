from sqlalchemy.orm import Session
from app.models.models import JobPost
from app.schemas.schemas import JobPostCreate, JobPostUpdate


def create_job(db: Session, job: JobPostCreate) -> JobPost:
    db_job = JobPost(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(JobPost).offset(skip).limit(limit).all()


def get_job(db: Session, job_id: int):
    return db.query(JobPost).filter(JobPost.id == job_id).first()


def update_job(db: Session, job_id: int, job_update: JobPostUpdate):
    db_job = db.query(JobPost).filter(JobPost.id == job_id).first()
    if not db_job:
        return None
    update_data = job_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job, field, value)
    db.commit()
    db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int):
    db_job = db.query(JobPost).filter(JobPost.id == job_id).first()
    if db_job:
        db.delete(db_job)
        db.commit()
        return True
    return False

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import JobPost
from app.schemas.schemas import JobPostCreate, JobPostOut, JobPostUpdate
from app.services.job_service import create_job, get_jobs, get_job, update_job, delete_job

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/", response_model=JobPostOut)
def create(job: JobPostCreate, db: Session = Depends(get_db)):
    return create_job(db, job)


@router.get("/", response_model=List[JobPostOut])
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_jobs(db, skip=skip, limit=limit)


@router.get("/{job_id}", response_model=JobPostOut)
def retrieve(job_id: int, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobPostOut)
def update(job_id: int, job_update: JobPostUpdate, db: Session = Depends(get_db)):
    job = update_job(db, job_id, job_update)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.delete("/{job_id}")
def remove(job_id: int, db: Session = Depends(get_db)):
    if delete_job(db, job_id):
        return {"detail": "Job deleted"}
    raise HTTPException(status_code=404, detail="Job not found")

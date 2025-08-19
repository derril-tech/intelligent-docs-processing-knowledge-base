from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_superuser
from app.models.user import User
from app.models.processing_queue import ProcessingQueue, ProcessingTask, TaskStatus
from app.schemas.processing import (
    ProcessingTaskResponse,
    ProcessingQueueStatus,
    ProcessingTaskDetail
)
from app.services.processing import ProcessingService

logger = structlog.get_logger()
router = APIRouter()

@router.get("/queue/status", response_model=ProcessingQueueStatus)
async def get_processing_queue_status(
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get processing queue status (superuser only)"""
    try:
        processing_service = ProcessingService()
        status = await processing_service.get_queue_status()
        return status
        
    except Exception as e:
        logger.error("Failed to get queue status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get queue status"
        )

@router.get("/tasks", response_model=List[ProcessingTaskResponse])
async def get_processing_tasks(
    skip: int = 0,
    limit: int = 20,
    status: Optional[TaskStatus] = None,
    task_type: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get processing tasks"""
    query = db.query(ProcessingQueue)
    
    if status:
        query = query.filter(ProcessingQueue.status == status)
    if task_type:
        query = query.filter(ProcessingQueue.task_type == task_type)
    
    # Users can only see their own tasks unless they're superuser
    if not current_user.is_superuser:
        query = query.join(ProcessingQueue.document).filter(
            ProcessingQueue.document.has(uploaded_by=current_user.id)
        )
    
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=ProcessingTaskResponse)
async def get_processing_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get processing task by ID"""
    task = db.query(ProcessingQueue).filter(ProcessingQueue.id == task_id).first()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Processing task not found")
    
    # Users can only see their own tasks unless they're superuser
    if not current_user.is_superuser:
        if task.document.uploaded_by != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return task

@router.get("/tasks/{task_id}/details", response_model=List[ProcessingTaskDetail])
async def get_processing_task_details(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed processing tasks for a queue entry"""
    queue_entry = db.query(ProcessingQueue).filter(ProcessingQueue.id == task_id).first()
    
    if queue_entry is None:
        raise HTTPException(status_code=404, detail="Processing task not found")
    
    # Users can only see their own tasks unless they're superuser
    if not current_user.is_superuser:
        if queue_entry.document.uploaded_by != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    tasks = db.query(ProcessingTask).filter(
        ProcessingTask.queue_entry_id == task_id
    ).all()
    
    return tasks

@router.post("/tasks/{task_id}/retry")
async def retry_processing_task(
    task_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Retry a failed processing task (superuser only)"""
    try:
        processing_service = ProcessingService()
        await processing_service.retry_task(task_id)
        
        logger.info("Processing task retried", task_id=task_id, user_id=current_user.id)
        return {"message": "Task queued for retry"}
        
    except Exception as e:
        logger.error("Failed to retry task", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retry task"
        )

@router.post("/tasks/{task_id}/cancel")
async def cancel_processing_task(
    task_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Cancel a processing task (superuser only)"""
    try:
        processing_service = ProcessingService()
        await processing_service.cancel_task(task_id)
        
        logger.info("Processing task cancelled", task_id=task_id, user_id=current_user.id)
        return {"message": "Task cancelled successfully"}
        
    except Exception as e:
        logger.error("Failed to cancel task", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel task"
        )

@router.get("/workers/status")
async def get_worker_status(
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get worker status (superuser only)"""
    try:
        processing_service = ProcessingService()
        worker_status = await processing_service.get_worker_status()
        return worker_status
        
    except Exception as e:
        logger.error("Failed to get worker status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get worker status"
        )

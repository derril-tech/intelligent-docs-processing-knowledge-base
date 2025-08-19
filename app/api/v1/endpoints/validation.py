from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.validation_queue import ValidationQueue, ValidationTask, ValidationStatus
from app.schemas.validation import (
    ValidationTaskResponse,
    ValidationQueueStatus,
    ValidationResult
)
from app.services.validation import ValidationService

logger = structlog.get_logger()
router = APIRouter()

@router.get("/queue", response_model=List[ValidationTaskResponse])
async def get_validation_queue(
    skip: int = 0,
    limit: int = 20,
    status: Optional[ValidationStatus] = None,
    validation_type: Optional[str] = None,
    assigned_to_me: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get validation queue tasks"""
    query = db.query(ValidationQueue)
    
    if status:
        query = query.filter(ValidationQueue.status == status)
    if validation_type:
        query = query.filter(ValidationQueue.validation_type == validation_type)
    if assigned_to_me:
        query = query.filter(ValidationQueue.assigned_to == current_user.id)
    
    tasks = query.order_by(ValidationQueue.priority.desc(), ValidationQueue.created_at.asc())
    tasks = tasks.offset(skip).limit(limit).all()
    
    return tasks

@router.get("/queue/status", response_model=ValidationQueueStatus)
async def get_validation_queue_status(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get validation queue status"""
    try:
        validation_service = ValidationService()
        status = await validation_service.get_queue_status()
        return status
        
    except Exception as e:
        logger.error("Failed to get validation queue status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get queue status"
        )

@router.get("/tasks/{task_id}", response_model=ValidationTaskResponse)
async def get_validation_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get validation task by ID"""
    task = db.query(ValidationQueue).filter(ValidationQueue.id == task_id).first()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Validation task not found")
    
    return task

@router.post("/tasks/{task_id}/assign")
async def assign_validation_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Assign validation task to current user"""
    try:
        validation_service = ValidationService()
        await validation_service.assign_task(task_id, current_user.id)
        
        logger.info("Validation task assigned", task_id=task_id, user_id=current_user.id)
        return {"message": "Task assigned successfully"}
        
    except Exception as e:
        logger.error("Failed to assign validation task", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign task"
        )

@router.post("/tasks/{task_id}/validate")
async def validate_task(
    task_id: int,
    validation_result: ValidationResult,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit validation result for a task"""
    try:
        validation_service = ValidationService()
        await validation_service.submit_validation(
            task_id=task_id,
            user_id=current_user.id,
            validation_result=validation_result
        )
        
        logger.info("Validation submitted", task_id=task_id, user_id=current_user.id)
        return {"message": "Validation submitted successfully"}
        
    except Exception as e:
        logger.error("Failed to submit validation", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit validation"
        )

@router.post("/tasks/{task_id}/escalate")
async def escalate_validation_task(
    task_id: int,
    reason: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Escalate a validation task"""
    try:
        validation_service = ValidationService()
        await validation_service.escalate_task(task_id, current_user.id, reason)
        
        logger.info("Validation task escalated", task_id=task_id, user_id=current_user.id, reason=reason)
        return {"message": "Task escalated successfully"}
        
    except Exception as e:
        logger.error("Failed to escalate validation task", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to escalate task"
        )

@router.get("/my-tasks", response_model=List[ValidationTaskResponse])
async def get_my_validation_tasks(
    skip: int = 0,
    limit: int = 20,
    status: Optional[ValidationStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get validation tasks assigned to current user"""
    query = db.query(ValidationQueue).filter(ValidationQueue.assigned_to == current_user.id)
    
    if status:
        query = query.filter(ValidationQueue.status == status)
    
    tasks = query.order_by(ValidationQueue.priority.desc(), ValidationQueue.created_at.asc())
    tasks = tasks.offset(skip).limit(limit).all()
    
    return tasks

@router.get("/stats")
async def get_validation_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get validation statistics for current user"""
    try:
        # Get user's validation statistics
        total_assigned = db.query(ValidationQueue).filter(
            ValidationQueue.assigned_to == current_user.id
        ).count()
        
        completed_tasks = db.query(ValidationQueue).filter(
            ValidationQueue.assigned_to == current_user.id,
            ValidationQueue.status.in_([ValidationStatus.APPROVED, ValidationStatus.REJECTED])
        ).count()
        
        pending_tasks = db.query(ValidationQueue).filter(
            ValidationQueue.assigned_to == current_user.id,
            ValidationQueue.status == ValidationStatus.IN_PROGRESS
        ).count()
        
        overdue_tasks = db.query(ValidationQueue).filter(
            ValidationQueue.assigned_to == current_user.id,
            ValidationQueue.is_overdue == True
        ).count()
        
        return {
            "total_assigned": total_assigned,
            "completed": completed_tasks,
            "pending": pending_tasks,
            "overdue": overdue_tasks,
            "completion_rate": (completed_tasks / total_assigned * 100) if total_assigned > 0 else 0
        }
        
    except Exception as e:
        logger.error("Failed to get validation stats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get statistics"
        )

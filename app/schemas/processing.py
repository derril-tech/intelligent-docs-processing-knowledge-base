from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class ProcessingTaskBase(BaseModel):
    task_type: str
    priority: TaskPriority = TaskPriority.NORMAL
    task_metadata: Optional[Dict[str, Any]] = None

class ProcessingTaskCreate(ProcessingTaskBase):
    document_id: int

class ProcessingTaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    error_message: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None
    assigned_worker: Optional[str] = None
    worker_pid: Optional[int] = None

class ProcessingTaskResponse(ProcessingTaskBase):
    id: int
    document_id: int
    status: TaskStatus
    retry_count: int
    max_retries: int
    queued_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None
    assigned_worker: Optional[str] = None
    worker_pid: Optional[int] = None

    class Config:
        from_attributes = True

class ProcessingStatus(BaseModel):
    id: int
    document_id: int
    task_type: str
    status: TaskStatus
    progress: Optional[float] = None  # 0-100
    current_step: Optional[str] = None
    total_steps: Optional[int] = None
    estimated_completion: Optional[datetime] = None

class ProcessingTaskDetail(BaseModel):
    id: int
    queue_entry_id: int
    task_name: str
    status: TaskStatus
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    task_config: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time: Optional[int] = None
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    depends_on_task_id: Optional[int] = None

    class Config:
        from_attributes = True

class ProcessingQueueStatus(BaseModel):
    total_tasks: int
    pending_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int
    average_processing_time: Optional[float] = None
    active_workers: int
    queue_health: str  # "healthy", "warning", "critical"

class ProcessingConfig(BaseModel):
    max_concurrent_tasks: int
    task_timeout: int
    retry_policy: Dict[str, Any]
    worker_config: Dict[str, Any]

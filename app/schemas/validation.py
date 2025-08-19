from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ValidationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"

class ValidationType(str, Enum):
    DOCUMENT_CLASSIFICATION = "document_classification"
    DATA_EXTRACTION = "data_extraction"
    ENTITY_RECOGNITION = "entity_recognition"
    RELATIONSHIP_VALIDATION = "relationship_validation"
    CONFIDENCE_THRESHOLD = "confidence_threshold"

class ValidationTaskBase(BaseModel):
    validation_type: ValidationType
    priority: int = 1
    original_data: Dict[str, Any]
    suggested_corrections: Optional[Dict[str, Any]] = None
    validation_metadata: Optional[Dict[str, Any]] = None

class ValidationTaskCreate(ValidationTaskBase):
    document_id: int
    knowledge_entry_id: Optional[int] = None

class ValidationTaskUpdate(BaseModel):
    status: Optional[ValidationStatus] = None
    assigned_to: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class ValidationTaskResponse(ValidationTaskBase):
    id: int
    document_id: int
    knowledge_entry_id: Optional[int] = None
    status: ValidationStatus
    assigned_to: Optional[int] = None
    assigned_at: Optional[datetime] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    sla_deadline: Optional[datetime] = None
    is_overdue: bool

    class Config:
        from_attributes = True

class ValidationTaskDetail(BaseModel):
    id: int
    queue_entry_id: int
    task_name: str
    field_name: Optional[str] = None
    field_value: Optional[str] = None
    suggested_value: Optional[str] = None
    is_correct: Optional[bool] = None
    corrected_value: Optional[str] = None
    confidence_score: Optional[int] = None
    validation_notes: Optional[str] = None
    validation_metadata: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    validated_by: Optional[int] = None

    class Config:
        from_attributes = True

class ValidationResult(BaseModel):
    task_id: int
    is_approved: bool
    corrections: Optional[Dict[str, Any]] = None
    confidence_score: Optional[int] = None
    validation_notes: Optional[str] = None
    validation_metadata: Optional[Dict[str, Any]] = None

class ValidationQueueStatus(BaseModel):
    total_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completed_tasks: int
    overdue_tasks: int
    average_validation_time: Optional[float] = None
    assigned_tasks: int
    unassigned_tasks: int

class ValidationConfig(BaseModel):
    confidence_threshold: float
    auto_approval_enabled: bool
    sla_hours: int
    escalation_rules: Dict[str, Any]
    validation_workflow: Dict[str, Any]

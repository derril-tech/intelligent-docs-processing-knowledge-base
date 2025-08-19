from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class ValidationStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"

class ValidationType(enum.Enum):
    DOCUMENT_CLASSIFICATION = "document_classification"
    DATA_EXTRACTION = "data_extraction"
    ENTITY_RECOGNITION = "entity_recognition"
    RELATIONSHIP_VALIDATION = "relationship_validation"
    CONFIDENCE_THRESHOLD = "confidence_threshold"

class ValidationQueue(Base):
    __tablename__ = "validation_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    knowledge_entry_id = Column(Integer, ForeignKey("knowledge_base_entries.id"), nullable=True)
    
    # Validation information
    validation_type = Column(Enum(ValidationType), nullable=False)
    status = Column(Enum(ValidationStatus), default=ValidationStatus.PENDING)
    priority = Column(Integer, default=1)  # Higher number = higher priority
    
    # Data to validate
    original_data = Column(JSON, nullable=False)  # AI-extracted data
    suggested_corrections = Column(JSON)  # AI-suggested corrections
    validation_metadata = Column(JSON)  # Additional validation context
    
    # Assignment
    assigned_to = Column(Integer, ForeignKey("users.id"))
    assigned_at = Column(DateTime(timezone=True))
    
    # Timing
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # SLA tracking
    sla_deadline = Column(DateTime(timezone=True))
    is_overdue = Column(Boolean, default=False)
    
    # Relationships
    validation_tasks = relationship("ValidationTask", back_populates="queue_entry")
    
    def __repr__(self):
        return f"<ValidationQueue(id={self.id}, document_id={self.document_id}, type='{self.validation_type}', status='{self.status}')>"

class ValidationTask(Base):
    __tablename__ = "validation_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    queue_entry_id = Column(Integer, ForeignKey("validation_queue.id"), nullable=False)
    
    # Task details
    task_name = Column(String(100), nullable=False)
    field_name = Column(String(100))  # Specific field being validated
    field_value = Column(Text)  # Current value
    suggested_value = Column(Text)  # Suggested correction
    
    # Validation result
    is_correct = Column(Boolean)
    corrected_value = Column(Text)
    confidence_score = Column(Integer)  # Validator's confidence (0-100)
    
    # Validation metadata
    validation_notes = Column(Text)
    validation_metadata = Column(JSON)
    
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Validator information
    validated_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    queue_entry = relationship("ValidationQueue", back_populates="validation_tasks")
    
    def __repr__(self):
        return f"<ValidationTask(id={self.id}, task_name='{self.task_name}', field='{self.field_name}')>"

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class TaskStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(enum.Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class ProcessingQueue(Base):
    __tablename__ = "processing_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Task information
    task_type = Column(String(100), nullable=False)  # e.g., "ocr", "classification", "extraction"
    priority = Column(Enum(TaskPriority), default=TaskPriority.NORMAL)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    
    # Task metadata
    task_metadata = Column(JSON)  # Task-specific configuration
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    # Timing
    queued_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Error handling
    error_message = Column(Text)
    error_details = Column(JSON)
    
    # Worker information
    assigned_worker = Column(String(100))
    worker_pid = Column(Integer)
    
    # Relationships
    tasks = relationship("ProcessingTask", back_populates="queue_entry")
    
    def __repr__(self):
        return f"<ProcessingQueue(id={self.id}, document_id={self.document_id}, task_type='{self.task_type}', status='{self.status}')>"

class ProcessingTask(Base):
    __tablename__ = "processing_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    queue_entry_id = Column(Integer, ForeignKey("processing_queue.id"), nullable=False)
    
    # Task execution
    task_name = Column(String(100), nullable=False)  # Specific task name
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    
    # Task parameters
    input_data = Column(JSON)  # Input data for the task
    output_data = Column(JSON)  # Output data from the task
    task_config = Column(JSON)  # Task configuration
    
    # Execution tracking
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    execution_time = Column(Integer)  # Execution time in seconds
    
    # Error handling
    error_message = Column(Text)
    error_traceback = Column(Text)
    
    # Task dependencies
    depends_on_task_id = Column(Integer, ForeignKey("processing_tasks.id"))
    
    # Relationships
    queue_entry = relationship("ProcessingQueue", back_populates="tasks")
    dependent_tasks = relationship("ProcessingTask", remote_side=[id])
    
    def __repr__(self):
        return f"<ProcessingTask(id={self.id}, task_name='{self.task_name}', status='{self.status}')>"

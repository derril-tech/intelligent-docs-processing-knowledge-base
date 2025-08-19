from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class DocumentType(enum.Enum):
    INVOICE = "invoice"
    CONTRACT = "contract"
    MEDICAL_RECORD = "medical_record"
    FINANCIAL_STATEMENT = "financial_statement"
    FORM = "form"
    REPORT = "report"
    OTHER = "other"

class ProcessingStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    VALIDATION_REQUIRED = "validation_required"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    
    # Document classification
    document_type = Column(Enum(DocumentType), nullable=True)
    confidence_score = Column(Integer)  # AI confidence in classification (0-100)
    
    # Processing status
    status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING)
    processing_started_at = Column(DateTime(timezone=True))
    processing_completed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    # User who uploaded the document
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    metadata = relationship("DocumentMetadata", back_populates="document", uselist=False)
    processing_status = relationship("DocumentProcessingStatus", back_populates="document")
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', status='{self.status}')>"

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Extracted text content
    extracted_text = Column(Text)
    ocr_text = Column(Text)
    
    # AI-extracted data
    extracted_data = Column(JSON)  # Structured data extracted by AI
    entities = Column(JSON)  # Named entities found in document
    key_value_pairs = Column(JSON)  # Key-value pairs extracted
    
    # Document properties
    page_count = Column(Integer)
    language = Column(String(10))
    processing_metadata = Column(JSON)  # Processing pipeline metadata
    
    # Relationships
    document = relationship("Document", back_populates="metadata")
    
    def __repr__(self):
        return f"<DocumentMetadata(id={self.id}, document_id={self.document_id})>"

class DocumentProcessingStatus(Base):
    __tablename__ = "document_processing_status"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Processing step tracking
    step_name = Column(String(100), nullable=False)  # e.g., "ocr", "classification", "extraction"
    status = Column(Enum(ProcessingStatus), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    # Step-specific metadata
    step_metadata = Column(JSON)
    
    # Relationships
    document = relationship("Document", back_populates="processing_status")
    
    def __repr__(self):
        return f"<DocumentProcessingStatus(id={self.id}, document_id={self.document_id}, step='{self.step_name}')>"

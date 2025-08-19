from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class DocumentType(str, Enum):
    INVOICE = "invoice"
    CONTRACT = "contract"
    MEDICAL_RECORD = "medical_record"
    FINANCIAL_STATEMENT = "financial_statement"
    FORM = "form"
    REPORT = "report"
    OTHER = "other"

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    VALIDATION_REQUIRED = "validation_required"

class DocumentBase(BaseModel):
    original_filename: str
    document_type: Optional[DocumentType] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpload(BaseModel):
    file: Any  # Will be handled by FastAPI File upload
    document_type: Optional[DocumentType] = None
    metadata: Optional[Dict[str, Any]] = None

class DocumentResponse(DocumentBase):
    id: int
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    confidence_score: Optional[int] = None
    status: ProcessingStatus
    processing_started_at: Optional[datetime] = None
    processing_completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

class DocumentStatus(BaseModel):
    id: int
    status: ProcessingStatus
    processing_started_at: Optional[datetime] = None
    processing_completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

class DocumentMetadata(BaseModel):
    id: int
    document_id: int
    extracted_text: Optional[str] = None
    ocr_text: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None
    entities: Optional[List[Dict[str, Any]]] = None
    key_value_pairs: Optional[Dict[str, Any]] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
    processing_metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int
    page: int
    size: int
    pages: int

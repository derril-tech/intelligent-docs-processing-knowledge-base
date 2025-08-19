from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.document import Document, DocumentMetadata, ProcessingStatus
from app.schemas.document import DocumentResponse, DocumentListResponse, DocumentStatus
from app.services.file_storage import FileStorageService
from app.services.processing import ProcessingService

logger = structlog.get_logger()
router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a document for processing"""
    try:
        # Validate file type
        if file.content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file.content_type} not allowed"
            )
        
        # Validate file size
        if file.size and file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large"
            )
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Save file
        file_storage = FileStorageService()
        file_path = await file_storage.save_file(file, unique_filename)
        
        # Create document record
        db_document = Document(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size or 0,
            mime_type=file.content_type,
            uploaded_by=current_user.id
        )
        
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Queue for processing
        processing_service = ProcessingService()
        await processing_service.queue_document_processing(db_document.id)
        
        logger.info("Document uploaded", document_id=db_document.id, user_id=current_user.id)
        return db_document
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Document upload failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Upload failed"
        )

@router.get("/", response_model=DocumentListResponse)
async def get_documents(
    skip: int = 0,
    limit: int = 20,
    status: Optional[ProcessingStatus] = None,
    document_type: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's documents"""
    query = db.query(Document).filter(Document.uploaded_by == current_user.id)
    
    if status:
        query = query.filter(Document.status == status)
    if document_type:
        query = query.filter(Document.document_type == document_type)
    
    total = query.count()
    documents = query.offset(skip).limit(limit).all()
    
    return DocumentListResponse(
        documents=documents,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get document by ID"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.uploaded_by == current_user.id
    ).first()
    
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

@router.get("/{document_id}/status", response_model=DocumentStatus)
async def get_document_status(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get document processing status"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.uploaded_by == current_user.id
    ).first()
    
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return DocumentStatus(
        id=document.id,
        status=document.status,
        processing_started_at=document.processing_started_at,
        processing_completed_at=document.processing_completed_at,
        error_message=document.error_message
    )

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete document"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.uploaded_by == current_user.id
    ).first()
    
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file from storage
    file_storage = FileStorageService()
    await file_storage.delete_file(document.file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    logger.info("Document deleted", document_id=document_id, user_id=current_user.id)
    return {"message": "Document deleted successfully"}

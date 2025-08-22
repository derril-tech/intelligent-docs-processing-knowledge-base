# Services Layer Instructions

## Purpose
This folder contains business logic services that abstract complex operations and external integrations. Services handle the core business logic and coordinate between different components.

## File Structure
- `file_storage.py` - File upload, storage, and management services
- `processing.py` - Document processing orchestration and AI/ML integration
- `search.py` - Knowledge base search and indexing services
- `validation.py` - Validation workflow and human-in-the-loop services

## Implementation Guidelines

### Service Class Pattern
```python
import structlog
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse

logger = structlog.get_logger()

class DocumentService:
    """Service for document-related business logic"""
    
    def __init__(self):
        self.config = settings
    
    async def create_document(
        self, 
        db: Session, 
        document_data: DocumentCreate,
        user_id: int
    ) -> DocumentResponse:
        """
        Create a new document and initiate processing.
        
        Args:
            db: Database session
            document_data: Document creation data
            user_id: ID of the user creating the document
            
        Returns:
            DocumentResponse: Created document information
            
        Raises:
            ValidationError: If document data is invalid
            ProcessingError: If document processing fails
        """
        try:
            # Business logic implementation
            logger.info("Creating document", user_id=user_id, title=document_data.title)
            
            # Create document record
            document = Document(
                title=document_data.title,
                filename=document_data.filename,
                user_id=user_id,
                status="uploaded"
            )
            db.add(document)
            db.commit()
            db.refresh(document)
            
            # Initiate processing
            await self._initiate_processing(document.id)
            
            return DocumentResponse.from_orm(document)
            
        except Exception as e:
            logger.error("Failed to create document", error=str(e), user_id=user_id)
            db.rollback()
            raise
    
    async def _initiate_processing(self, document_id: int) -> None:
        """Initiate background processing for a document"""
        # Implementation for processing initiation
        pass
```

### Service Responsibilities
- **Business Logic**: Implement core business rules and workflows
- **Data Validation**: Validate business rules beyond schema validation
- **External Integration**: Handle API calls to external services
- **Error Handling**: Provide meaningful error messages and logging
- **Transaction Management**: Handle database transactions properly

### Service Dependencies
- Use dependency injection for external services
- Keep services stateless when possible
- Use async/await for I/O operations
- Implement proper error handling and logging

### File Storage Service
- Handle file upload validation
- Manage file storage (local/S3)
- Implement file security measures
- Handle file format conversion

### Processing Service
- Orchestrate document processing workflow
- Integrate with AI/ML services
- Manage processing queue
- Handle processing errors and retries

### Search Service
- Implement knowledge base indexing
- Handle search queries and filters
- Manage search result ranking
- Optimize search performance

### Validation Service
- Manage validation workflows
- Handle human-in-the-loop processes
- Track validation status
- Implement validation rules

## TODO Items
- [ ] Implement file storage service
- [ ] Create document processing service
- [ ] Add knowledge base search service
- [ ] Implement validation workflow service
- [ ] Add AI/ML integration services
- [ ] Create caching service
- [ ] Implement notification service
- [ ] Add analytics service
- [ ] Create export service
- [ ] Implement backup service

## Notes
- Keep services focused on single responsibility
- Use dependency injection for testability
- Implement comprehensive error handling
- Add detailed logging for debugging
- Write unit tests for all services

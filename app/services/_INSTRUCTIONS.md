# Services Layer Development Instructions

## Overview
The services layer contains business logic for the DocuMind™ application. Services handle complex operations, coordinate between different components, and implement the core functionality of the platform.

## CLAUDE_TASK: Service Development Guidelines

### 1. Service Architecture
- Services should be stateless and thread-safe
- Use dependency injection for external dependencies
- Implement proper error handling and logging
- Follow single responsibility principle

### 2. Database Operations
- Use SQLAlchemy ORM for database operations
- Implement proper transaction handling
- Use service methods for complex queries
- Handle database errors gracefully

### 3. External Integrations
- Implement retry logic for external API calls
- Use async/await for I/O operations
- Handle rate limiting and timeouts
- Implement proper error handling

### 4. Business Logic
- Implement domain-specific business rules
- Validate business constraints
- Handle edge cases and error conditions
- Maintain data consistency

## File Structure
```
services/
├── document_service.py    # Document management logic
├── rag_service.py        # RAG pipeline orchestration
├── validation_service.py # Validation workflow logic
├── search_service.py     # Search and indexing
├── file_storage.py       # File storage operations
├── processing.py         # Document processing pipeline
└── user_service.py       # User management logic
```

## Example Service Pattern
```python
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.core.logging import logger

class DocumentService:
    """Service for document management operations."""
    
    @staticmethod
    async def create_document(
        db: Session,
        document_data: DocumentCreate,
        user_id: int,
        tenant_id: int
    ) -> Document:
        """
        Create a new document with business logic validation.
        
        Args:
            db: Database session
            document_data: Document creation data
            user_id: ID of the user creating the document
            tenant_id: ID of the tenant
            
        Returns:
            Document: Created document instance
            
        Raises:
            ValidationError: If document data is invalid
            ProcessingError: If document processing fails
        """
        try:
            # Business logic validation
            await DocumentService._validate_document_data(document_data)
            
            # Create document instance
            document = Document(
                **document_data.dict(),
                user_id=user_id,
                tenant_id=tenant_id
            )
            
            # Save to database
            db.add(document)
            db.commit()
            db.refresh(document)
            
            # Trigger background processing
            await DocumentService._schedule_processing(document.id)
            
            logger.info(f"Document created successfully", 
                       document_id=document.id, user_id=user_id)
            
            return document
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create document: {e}")
            raise
    
    @staticmethod
    async def get_user_documents(
        db: Session,
        user_id: int,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None
    ) -> List[Document]:
        """
        Retrieve documents for a specific user with filtering.
        
        Args:
            db: Database session
            user_id: ID of the user
            tenant_id: ID of the tenant
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by document status
            
        Returns:
            List[Document]: List of documents
        """
        query = db.query(Document).filter(
            Document.user_id == user_id,
            Document.tenant_id == tenant_id
        )
        
        if status:
            query = query.filter(Document.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    async def _validate_document_data(document_data: DocumentCreate) -> None:
        """Validate document data according to business rules."""
        # Implement validation logic
        pass
    
    @staticmethod
    async def _schedule_processing(document_id: int) -> None:
        """Schedule document processing in background."""
        # Implement background task scheduling
        pass
```

## CLAUDE_TASK: Implementation Checklist

### Document Service
- [ ] Document creation with validation
- [ ] Document retrieval and filtering
- [ ] Document update and deletion
- [ ] Document processing orchestration
- [ ] File storage integration
- [ ] Metadata extraction and management

### RAG Service
- [ ] Document chunking and embedding
- [ ] Vector similarity search
- [ ] Hybrid search (vector + keyword)
- [ ] Answer generation with citations
- [ ] Confidence scoring
- [ ] Multi-model support

### Validation Service
- [ ] Validation task creation
- [ ] Task assignment logic
- [ ] Validation result processing
- [ ] Confidence threshold management
- [ ] Batch validation operations
- [ ] Audit trail management

### Search Service
- [ ] Elasticsearch integration
- [ ] Index management
- [ ] Search query processing
- [ ] Result ranking and filtering
- [ ] Faceted search
- [ ] Search analytics

### File Storage Service
- [ ] Local file storage
- [ ] S3 integration
- [ ] File validation and processing
- [ ] Storage quota management
- [ ] File cleanup and maintenance
- [ ] Backup and recovery

### Processing Service
- [ ] OCR processing
- [ ] Text extraction
- [ ] Document classification
- [ ] Entity extraction
- [ ] Quality assessment
- [ ] Processing pipeline orchestration

## Error Handling Patterns

### Service-Level Errors
```python
class ServiceError(Exception):
    """Base exception for service errors."""
    pass

class ValidationError(ServiceError):
    """Raised when validation fails."""
    pass

class ProcessingError(ServiceError):
    """Raised when processing fails."""
    pass

class NotFoundError(ServiceError):
    """Raised when resource is not found."""
    pass
```

### Error Handling in Services
```python
try:
    result = await external_api_call()
except ExternalAPIError as e:
    logger.error(f"External API call failed: {e}")
    raise ProcessingError(f"Failed to process document: {e}")
except TimeoutError as e:
    logger.error(f"Operation timed out: {e}")
    raise ProcessingError("Operation timed out")
```

## Testing Requirements
- Unit tests for all service methods
- Mock external dependencies
- Test error conditions and edge cases
- Integration tests with database
- Performance tests for critical operations

## Performance Considerations
- Use async/await for I/O operations
- Implement caching where appropriate
- Optimize database queries
- Use background tasks for heavy operations
- Monitor and log performance metrics

## Security Considerations
- Validate all inputs
- Sanitize data before processing
- Implement proper access controls
- Log security-relevant events
- Handle sensitive data appropriately

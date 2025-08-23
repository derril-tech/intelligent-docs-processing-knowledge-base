# API Endpoints Development Instructions

## Overview
This directory contains FastAPI route handlers for the DocuMind™ API. Each endpoint should follow the established patterns for authentication, validation, and error handling.

## CLAUDE_TASK: Endpoint Development Guidelines

### 1. Authentication & Authorization
- All endpoints (except auth endpoints) require JWT authentication
- Use `get_current_user` dependency for user authentication
- Use `get_current_tenant` dependency for multi-tenant context
- Implement role-based access control where needed

### 2. Request/Response Models
- Use Pydantic models from `app/schemas/` for request/response validation
- Include proper type hints and documentation
- Handle file uploads with proper validation

### 3. Error Handling
- Use appropriate HTTP status codes
- Return structured error responses
- Log errors with context for debugging

### 4. Database Operations
- Use dependency injection for database sessions
- Implement proper transaction handling
- Use service layer for business logic

## File Structure
```
endpoints/
├── auth.py              # Authentication endpoints
├── documents.py         # Document management
├── rag.py              # RAG pipeline endpoints
├── validation.py       # Validation workflow
├── knowledge_base.py   # Knowledge base operations
├── users.py            # User management
└── processing.py       # Document processing
```

## Example Endpoint Pattern
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.tenant_middleware import get_current_tenant
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter()

@router.post("/documents/", response_model=DocumentResponse)
async def create_document(
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
) -> DocumentResponse:
    """
    Create a new document.
    
    Args:
        document_data: Document creation data
        db: Database session
        current_user: Authenticated user
        current_tenant: Current tenant context
        
    Returns:
        DocumentResponse: Created document information
        
    Raises:
        HTTPException: If document creation fails
    """
    try:
        document = await DocumentService.create_document(
            db=db,
            document_data=document_data,
            user_id=current_user.id,
            tenant_id=current_tenant.id
        )
        return DocumentResponse.from_orm(document)
    except Exception as e:
        logger.error(f"Failed to create document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create document"
        )
```

## CLAUDE_TASK: Implementation Checklist

### Authentication Endpoints
- [ ] User registration with validation
- [ ] User login with JWT token generation
- [ ] Token refresh endpoint
- [ ] Password reset functionality
- [ ] Multi-tenant user management

### Document Endpoints
- [ ] Document upload with file validation
- [ ] Document listing with pagination and filters
- [ ] Document details retrieval
- [ ] Document update and deletion
- [ ] Document processing status tracking

### RAG Endpoints
- [ ] Question asking with RAG pipeline
- [ ] Answer history retrieval
- [ ] Document chunk search
- [ ] Document processing for RAG
- [ ] Citation management

### Validation Endpoints
- [ ] Validation task creation
- [ ] Task assignment and management
- [ ] Validation result submission
- [ ] Task status tracking
- [ ] Batch validation operations

### Knowledge Base Endpoints
- [ ] Knowledge base entry creation
- [ ] Entry search and retrieval
- [ ] Entry categorization
- [ ] Knowledge base management
- [ ] Import/export functionality

## Testing Requirements
- Unit tests for each endpoint
- Integration tests with database
- Authentication and authorization tests
- Error handling tests
- Performance tests for critical endpoints

## Security Considerations
- Input validation and sanitization
- Rate limiting implementation
- CORS configuration
- PII handling and redaction
- Audit logging for sensitive operations

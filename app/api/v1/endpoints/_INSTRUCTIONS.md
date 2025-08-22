# API Endpoints Instructions

## Purpose
This folder contains FastAPI route handlers for all API endpoints. Each file represents a specific domain or resource.

## File Structure
- `auth.py` - Authentication endpoints (login, register, refresh token)
- `documents.py` - Document management endpoints (upload, list, get, update, delete)
- `knowledge_base.py` - Knowledge base search and analytics endpoints
- `processing.py` - Processing queue management endpoints
- `users.py` - User management endpoints
- `validation.py` - Validation task management endpoints

## Implementation Guidelines

### Standard Endpoint Pattern
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter()

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[DocumentResponse]:
    """
    Retrieve a list of documents with optional filtering.
    """
    return DocumentService.get_user_documents(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status
    )
```

### Authentication Requirements
- All endpoints except auth endpoints require authentication
- Use `get_current_active_user` dependency for user authentication
- Use `get_current_superuser` dependency for admin-only endpoints
- Check user permissions for resource access

### Error Handling
- Use appropriate HTTP status codes
- Provide clear error messages
- Log errors for debugging
- Handle validation errors gracefully

### File Upload Endpoints
- Use `UploadFile` for file uploads
- Validate file types and sizes
- Store files securely
- Return processing status

### Response Format
- Use Pydantic schemas for response models
- Include pagination for list endpoints
- Provide consistent error responses
- Include metadata when appropriate

## TODO Items
- [ ] Implement authentication endpoints
- [ ] Add document upload and management endpoints
- [ ] Create knowledge base search endpoints
- [ ] Add processing queue management
- [ ] Implement validation task endpoints
- [ ] Add user management endpoints
- [ ] Include comprehensive error handling
- [ ] Add request/response logging
- [ ] Implement rate limiting
- [ ] Add API documentation

## Notes
- Follow FastAPI best practices
- Use dependency injection for services
- Implement proper validation
- Add comprehensive tests
- Document all endpoints

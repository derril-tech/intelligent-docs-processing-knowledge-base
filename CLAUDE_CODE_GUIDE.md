# Claude Code Implementation Guide

This guide is specifically designed to help Claude Code understand and work effectively with the Intelligent Document Processing backend codebase.

## Codebase Patterns and Conventions

### 1. Project Structure Understanding

**Key Directories and Their Purpose:**
- `app/core/` - Core infrastructure (config, database, security, logging)
- `app/models/` - SQLAlchemy database models
- `app/schemas/` - Pydantic data validation schemas
- `app/api/v1/endpoints/` - FastAPI route handlers
- `app/services/` - Business logic abstraction layer
- `app/tasks/` - Celery background task definitions

**File Naming Conventions:**
- Models: `snake_case.py` (e.g., `user.py`, `document.py`)
- Schemas: `snake_case.py` (e.g., `user.py`, `document.py`)
- Endpoints: `snake_case.py` (e.g., `auth.py`, `documents.py`)
- Services: `snake_case.py` (e.g., `file_storage.py`, `processing.py`)

### 2. Database Model Patterns

**Standard Model Structure:**
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ModelName(Base):
    __tablename__ = "table_name"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Standard fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="items")
    
    def __repr__(self):
        return f"<ModelName(id={self.id})>"
```

**Enum Usage:**
```python
import enum
from sqlalchemy import Enum

class StatusEnum(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ModelName(Base):
    __tablename__ = "table_name"
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
```

### 3. Pydantic Schema Patterns

**Standard Schema Structure:**
```python
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ModelBase(BaseModel):
    """Base schema with common fields"""
    pass

class ModelCreate(ModelBase):
    """Schema for creating new items"""
    pass

class ModelUpdate(BaseModel):
    """Schema for updating items (all fields optional)"""
    field1: Optional[str] = None
    field2: Optional[int] = None

class ModelResponse(ModelBase):
    """Schema for API responses"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # For SQLAlchemy model compatibility
```

**Enum Schemas:**
```python
from enum import Enum

class StatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ModelResponse(BaseModel):
    status: StatusEnum
    # ... other fields
```

### 4. FastAPI Endpoint Patterns

**Standard CRUD Endpoints:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.model import ModelCreate, ModelUpdate, ModelResponse

router = APIRouter()

@router.get("/", response_model=List[ModelResponse])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of items"""
    pass

@router.get("/{item_id}", response_model=ModelResponse)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get item by ID"""
    pass

@router.post("/", response_model=ModelResponse)
async def create_item(
    item: ModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create new item"""
    pass

@router.put("/{item_id}", response_model=ModelResponse)
async def update_item(
    item_id: int,
    item: ModelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update item"""
    pass

@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete item"""
    pass
```

**File Upload Endpoints:**
```python
from fastapi import File, UploadFile, Form
from typing import Optional

@router.post("/upload", response_model=ModelResponse)
async def upload_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload and process file"""
    pass
```

### 5. Service Layer Patterns

**Service Class Structure:**
```python
import structlog
from typing import Dict, Any, Optional
from app.core.config import settings

logger = structlog.get_logger()

class ServiceName:
    """Service for specific business logic"""
    
    def __init__(self):
        self.config = settings
    
    async def method_name(self, param1: str, param2: int) -> Dict[str, Any]:
        """Method description"""
        try:
            # Implementation logic
            logger.info("Operation performed", param1=param1, param2=param2)
            return {"status": "success", "data": result}
        except Exception as e:
            logger.error("Operation failed", error=str(e))
            raise
```

**Dependency Injection in Endpoints:**
```python
from app.services.service_name import ServiceName

def get_service():
    return ServiceName()

@router.post("/")
async def endpoint(
    service: ServiceName = Depends(get_service),
    current_user: User = Depends(get_current_active_user)
):
    """Endpoint using service"""
    result = await service.method_name(param1, param2)
    return result
```

### 6. Celery Task Patterns

**Task Structure:**
```python
from celery import current_task
from app.core.celery import celery_app
import structlog

logger = structlog.get_logger()

@celery_app.task(bind=True)
def task_name(self, param1: int, param2: str):
    """Task description"""
    try:
        logger.info("Task started", task_id=self.request.id, param1=param1)
        
        # Update task state
        self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100})
        
        # Task implementation
        # ...
        
        self.update_state(state='PROGRESS', meta={'current': 100, 'total': 100})
        
        logger.info("Task completed", task_id=self.request.id)
        return {"status": "completed", "result": result}
        
    except Exception as e:
        logger.error("Task failed", task_id=self.request.id, error=str(e))
        raise
```

**Task with Retry Logic:**
```python
@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def unreliable_task(self, data: Dict[str, Any]):
    try:
        # Task logic
        result = process_data(data)
        return result
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

### 7. Error Handling Patterns

**Standard Error Responses:**
```python
from fastapi import HTTPException, status

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not found"
)

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input data"
)

# 403 Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Insufficient permissions"
)

# 422 Validation Error (handled automatically by FastAPI)
# 500 Internal Server Error (handled automatically by FastAPI)
```

**Custom Exception Classes:**
```python
class CustomException(Exception):
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

# Usage in endpoints
try:
    # Operation
    pass
except CustomException as e:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=e.message
    )
```

### 8. Configuration Patterns

**Environment Variable Usage:**
```python
from app.core.config import settings

# Access configuration
database_url = settings.DATABASE_URL
api_key = settings.OPENAI_API_KEY
max_file_size = settings.MAX_FILE_SIZE
```

**Type-Safe Configuration:**
```python
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Required settings
    DATABASE_URL: str
    SECRET_KEY: str
    
    # Optional settings with defaults
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Optional settings
    OPENAI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
```

### 9. Logging Patterns

**Structured Logging:**
```python
import structlog

logger = structlog.get_logger()

# Info logging
logger.info("Operation performed", user_id=123, document_id=456)

# Error logging
logger.error("Operation failed", error=str(e), user_id=123)

# Debug logging
logger.debug("Processing step", step="ocr", document_id=456)

# Warning logging
logger.warning("Low confidence result", confidence=0.6, document_id=456)
```

### 10. Testing Patterns

**Test Structure:**
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import get_db
from app.models.user import User

client = TestClient(app)

def test_endpoint():
    """Test endpoint functionality"""
    # Arrange
    # Act
    response = client.get("/endpoint")
    # Assert
    assert response.status_code == 200
    assert "data" in response.json()

@pytest.fixture
def db_session():
    """Database session fixture"""
    # Setup
    db = next(get_db())
    yield db
    # Teardown
    db.close()
```

### 11. Database Query Patterns

**Standard Queries:**
```python
# Get by ID
item = db.query(Model).filter(Model.id == item_id).first()

# Get with relationships
item = db.query(Model).options(
    joinedload(Model.relationship)
).filter(Model.id == item_id).first()

# List with pagination
items = db.query(Model).offset(skip).limit(limit).all()

# Filter by user
items = db.query(Model).filter(Model.user_id == user_id).all()

# Complex filtering
items = db.query(Model).filter(
    Model.status == StatusEnum.COMPLETED,
    Model.created_at >= start_date
).all()
```

**Bulk Operations:**
```python
# Bulk create
db.bulk_save_objects(items)
db.commit()

# Bulk update
db.query(Model).filter(Model.status == StatusEnum.PENDING).update(
    {"status": StatusEnum.PROCESSING}
)
db.commit()
```

### 12. API Response Patterns

**Standard Response Structure:**
```python
# Success response
{
    "id": 123,
    "status": "completed",
    "data": {...},
    "created_at": "2024-01-01T00:00:00Z"
}

# List response
{
    "items": [...],
    "total": 100,
    "page": 1,
    "size": 20,
    "pages": 5
}

# Error response
{
    "detail": "Error message",
    "error_code": "VALIDATION_ERROR"
}
```

### 13. Security Patterns

**Authentication:**
```python
from app.core.security import get_current_active_user, get_current_superuser

# Require authentication
@router.get("/protected")
async def protected_endpoint(
    current_user: User = Depends(get_current_active_user)
):
    pass

# Require superuser
@router.get("/admin")
async def admin_endpoint(
    current_user: User = Depends(get_current_superuser)
):
    pass
```

**Permission Checking:**
```python
# Check ownership
if item.user_id != current_user.id and not current_user.is_superuser:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to access this resource"
    )
```

## Implementation Guidelines for Claude Code

### When Adding New Features:

1. **Start with the Model**: Define the database structure first
2. **Create Schemas**: Define input/output validation
3. **Implement Service**: Add business logic
4. **Create Endpoints**: Expose API functionality
5. **Add Tasks**: Implement background processing if needed
6. **Write Tests**: Ensure functionality works correctly

### When Modifying Existing Features:

1. **Check Dependencies**: Understand what depends on the code being modified
2. **Update Schemas**: Ensure data validation is updated
3. **Maintain Backward Compatibility**: Don't break existing API contracts
4. **Update Documentation**: Keep API docs current
5. **Test Changes**: Verify functionality still works

### Code Quality Standards:

1. **Type Hints**: Use type hints throughout the codebase
2. **Docstrings**: Document all public functions and classes
3. **Error Handling**: Handle errors gracefully with proper logging
4. **Performance**: Consider query optimization and caching
5. **Security**: Validate inputs and check permissions

### Common Pitfalls to Avoid:

1. **N+1 Queries**: Use eager loading for relationships
2. **Missing Error Handling**: Always handle potential exceptions
3. **Hard-coded Values**: Use configuration for environment-specific values
4. **Synchronous Operations**: Use async/await for I/O operations
5. **Missing Logging**: Log important operations and errors

This guide provides the essential patterns and conventions that Claude Code should follow when working with this codebase.

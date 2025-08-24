# Schemas Directory Instructions

## CLAUDE_TASK: Pydantic Schema Development

This directory contains Pydantic models for API request/response validation and serialization.

### Schema Guidelines
1. **Pydantic**: Use Pydantic v2+ with modern syntax
2. **Type Hints**: All fields must have proper type annotations
3. **Validation**: Implement field validators and custom validators
4. **Documentation**: Include field descriptions for OpenAPI docs
5. **Security**: Never include sensitive fields in response models
6. **Nesting**: Use nested models for complex data structures
7. **Optional Fields**: Mark optional fields appropriately

### Schema Structure
```python
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    VALIDATOR = "validator"
    VIEWER = "viewer"

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(..., min_length=1, max_length=255, description="User full name")
    role: UserRole = Field(default=UserRole.USER, description="User role")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password")
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserResponse(UserBase):
    id: int = Field(..., description="User ID")
    is_active: bool = Field(..., description="User active status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True
```

### Required Schemas
- **User**: User creation, update, and response schemas
- **Document**: Document upload, metadata, and response schemas
- **KnowledgeBase**: Knowledge base creation and query schemas
- **ProcessingJob**: Job creation, status, and result schemas
- **Authentication**: Login, register, and token schemas
- **Search**: Search query and result schemas
- **Admin**: Admin-specific schemas for management

### Schema Features
- **Field Validation**: Email, password strength, file size limits
- **Nested Models**: Complex data structures with proper nesting
- **Enum Support**: Use enums for constrained choice fields
- **Date/Time**: Proper datetime handling with timezone support
- **File Uploads**: File metadata and upload schemas
- **Pagination**: Standard pagination request/response schemas
- **Error Responses**: Standardized error response schemas

### Safe to Edit
- ✅ All schema files in this directory
- ✅ Field validators and custom validators
- ✅ Schema inheritance and composition
- ❌ Core Pydantic configuration (in core/config.py)

### Integration Points
- SQLAlchemy models for ORM integration
- FastAPI endpoints for request/response handling
- Service layer for business logic validation
- Background tasks for data processing

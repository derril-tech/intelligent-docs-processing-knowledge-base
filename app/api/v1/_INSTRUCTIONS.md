# API v1 Directory Instructions

## CLAUDE_TASK: FastAPI v1 Endpoint Development

This directory contains the FastAPI v1 API endpoints and routing structure.

### Directory Structure
- `api.py` - Main API router that includes all endpoint routers
- `endpoints/` - Individual endpoint modules organized by domain
- `__init__.py` - Package initialization

### API Guidelines
1. **FastAPI**: Use FastAPI decorators and dependency injection
2. **Pydantic**: All request/response models must use Pydantic
3. **Type Hints**: All functions must have proper type annotations
4. **Error Handling**: Use proper HTTP status codes and error responses
5. **Authentication**: Implement JWT authentication for protected endpoints
6. **Validation**: Use Pydantic validation for all inputs
7. **Documentation**: Include proper docstrings and OpenAPI documentation

### Endpoint Structure
```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth import get_current_user
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
async def get_users(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends()
):
    """Get all users (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return await user_service.get_all_users()
```

### Required Endpoints
- **Authentication**: `/auth/login`, `/auth/register`, `/auth/refresh`
- **Users**: `/users/`, `/users/{user_id}`, `/users/me`
- **Documents**: `/documents/`, `/documents/{doc_id}`, `/documents/upload`
- **Knowledge Base**: `/knowledge/`, `/knowledge/{kb_id}`, `/knowledge/query`
- **Processing**: `/processing/jobs/`, `/processing/jobs/{job_id}`
- **Admin**: `/admin/users/`, `/admin/stats/`, `/admin/settings/`

### Safe to Edit
- ✅ All endpoint files in this directory
- ✅ Router configurations and dependencies
- ❌ Core FastAPI app configuration (in main.py)

### Integration Points
- Database models from `app.models`
- Pydantic schemas from `app.schemas`
- Business logic from `app.services`
- Authentication from `app.core.auth`
- Background tasks via Celery

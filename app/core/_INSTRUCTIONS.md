# Core Directory Instructions

## CLAUDE_TASK: Core Application Configuration and Utilities

This directory contains core application configuration, database setup, authentication, and shared utilities.

### Core Components
- `config.py` - Application configuration and settings
- `database.py` - Database connection and session management
- `auth.py` - JWT authentication and security utilities
- `logging.py` - Structured logging configuration
- `celery.py` - Celery background task configuration
- `security.py` - Security utilities (password hashing, etc.)

### Configuration Guidelines
1. **Environment Variables**: Use Pydantic Settings for configuration
2. **Type Safety**: All configuration must be type-safe
3. **Validation**: Validate configuration on startup
4. **Security**: Never hardcode secrets or sensitive data
5. **Documentation**: Document all configuration options
6. **Testing**: Support different configurations for testing

### Configuration Structure
```python
from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL database URL")
    
    # Security
    SECRET_KEY: str = Field(..., description="JWT secret key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="JWT token expiry")
    
    # CORS
    ALLOWED_HOSTS: List[str] = Field(default=["*"], description="Allowed CORS origins")
    
    # External Services
    REDIS_URL: str = Field(default="redis://localhost:6379", description="Redis URL")
    ELASTICSEARCH_URL: str = Field(default="http://localhost:9200", description="Elasticsearch URL")
    
    # File Storage
    STORAGE_TYPE: str = Field(default="local", description="Storage backend type")
    LOCAL_STORAGE_PATH: str = Field(default="./uploads", description="Local storage path")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

### Required Core Components

#### Database Setup
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Authentication
```python
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # JWT token validation and user retrieval
    pass
```

### Safe to Edit
- ✅ Configuration settings and validation
- ✅ Database connection and session management
- ✅ Authentication utilities and security functions
- ✅ Logging configuration and utilities
- ❌ Core dependencies (import only)

### Integration Points
- Environment variables for configuration
- Database models and migrations
- API endpoints for authentication
- Background tasks via Celery
- External services (Redis, Elasticsearch)

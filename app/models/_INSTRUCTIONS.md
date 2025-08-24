# Models Directory Instructions

## CLAUDE_TASK: SQLAlchemy Model Development

This directory contains SQLAlchemy ORM models for the database schema.

### Model Guidelines
1. **SQLAlchemy**: Use SQLAlchemy 2.0+ declarative syntax
2. **Type Hints**: All models must have proper type annotations
3. **Relationships**: Define proper foreign key relationships
4. **Indexes**: Add appropriate database indexes for performance
5. **Constraints**: Implement database constraints and validations
6. **Audit Fields**: Include created_at, updated_at, created_by fields
7. **Multi-tenancy**: Implement row-level security for multi-tenant data

### Model Structure
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    documents: Mapped[List["Document"]] = relationship(back_populates="owner")
    
    # Indexes
    __table_args__ = (
        Index("idx_users_email", "email"),
        Index("idx_users_active", "is_active"),
    )
```

### Required Models
- **User**: User accounts and authentication
- **Document**: Document metadata and storage info
- **KnowledgeBase**: Knowledge base collections
- **ProcessingJob**: Document processing jobs and status
- **DocumentChunk**: Document chunks for vector search
- **Embedding**: Vector embeddings for similarity search
- **AuditLog**: Audit trail for compliance
- **Tenant**: Multi-tenant organization structure

### Model Features
- **Timestamps**: Automatic created_at/updated_at tracking
- **Soft Deletes**: Implement soft delete where appropriate
- **UUID Support**: Use UUIDs for external-facing IDs
- **JSON Fields**: Use JSONB for flexible data storage
- **Vector Fields**: pgvector integration for embeddings
- **Full-text Search**: PostgreSQL full-text search capabilities

### Safe to Edit
- ✅ All model files in this directory
- ✅ Model relationships and constraints
- ✅ Database indexes and optimizations
- ❌ Core database configuration (in core/database.py)

### Integration Points
- Database migrations via Alembic
- Pydantic schemas for API validation
- Service layer for business logic
- Background tasks for data processing

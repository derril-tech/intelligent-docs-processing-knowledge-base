# Claude AI Collaboration Guide

## Project Overview

The **Intelligent Document Processing and Knowledge Base** is a comprehensive, AI-powered platform designed to transform unstructured and semi-structured documents into a rich, accessible, and actionable knowledge base. This system eliminates manual data entry and document review processes, enabling organizations to unlock critical insights hidden within their documents and make smarter, data-driven decisions.

### Technology Stack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Redis, Celery
- **Frontend**: Next.js 13+, TypeScript, Tailwind CSS, React Hook Form
- **AI/ML**: OCR, NLP, Machine Learning for document processing
- **Infrastructure**: Docker, Docker Compose, AWS (production)
- **Testing**: pytest, Jest, Playwright

### Target Users
- Business analysts and data scientists
- Document processing teams
- Knowledge management professionals
- Compliance and audit teams
- Executive decision makers

### Project Goals
- Automate document processing workflows
- Create searchable knowledge bases from unstructured data
- Provide real-time processing and validation capabilities
- Enable data-driven insights and analytics
- Ensure data accuracy through human-in-the-loop validation

## Folder & File Structure

### Editable Files (Claude can modify)
- `app/api/v1/endpoints/` - API endpoint implementations
- `app/services/` - Business logic implementation
- `app/tasks/` - Background task implementations
- `app/schemas/` - Pydantic model definitions
- `frontend/app/` - Next.js pages and layouts
- `frontend/components/features/` - Feature-specific components
- `frontend/hooks/` - Custom React hooks
- `frontend/types/` - TypeScript type definitions
- `tests/` - Test files and fixtures

### Do-Not-Touch Files (Infrastructure only)
- `app/core/` - Core configuration and infrastructure
- `app/models/` - Database models (use migrations instead)
- `alembic/` - Database migration files
- `docker-compose.yml` - Container orchestration
- `Dockerfile` - Container definitions
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies
- Configuration files (`.env`, `alembic.ini`, etc.)

### Documentation Files (Reference only)
- `docs/` - All documentation files
- `README.md` - Project overview
- `PROJECT_BRIEF.md` - Project requirements

## Coding Conventions

### Python (Backend)
- **Style**: Follow PEP 8 with Black formatting
- **Naming**: snake_case for variables and functions, PascalCase for classes
- **Imports**: Group imports (standard library, third-party, local)
- **Documentation**: Use docstrings for all public functions and classes
- **Type Hints**: Use type hints for all function parameters and return values

```python
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse

def process_document(
    db: Session, 
    document_data: DocumentCreate,
    user_id: int
) -> DocumentResponse:
    """
    Process a new document and extract relevant information.
    
    Args:
        db: Database session
        document_data: Document creation data
        user_id: ID of the user uploading the document
        
    Returns:
        DocumentResponse: Processed document information
        
    Raises:
        ValidationError: If document data is invalid
        ProcessingError: If document processing fails
    """
    # Implementation here
    pass
```

### TypeScript/JavaScript (Frontend)
- **Style**: Follow ESLint and Prettier configurations
- **Naming**: camelCase for variables and functions, PascalCase for components
- **Components**: Use functional components with hooks
- **Types**: Define interfaces for all data structures
- **Error Handling**: Use try-catch blocks and error boundaries

```typescript
interface DocumentUploadProps {
  onUpload: (file: File) => Promise<void>;
  acceptedTypes: string[];
  maxSize: number;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onUpload,
  acceptedTypes,
  maxSize
}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    try {
      setIsUploading(true);
      setError(null);
      await onUpload(file);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-container">
      {/* Component implementation */}
    </div>
  );
};
```

### Database Models
- Use SQLAlchemy ORM with proper relationships
- Include created_at and updated_at timestamps
- Use enums for status fields
- Implement proper foreign key constraints

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class DocumentStatus(enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.UPLOADED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="documents")
```

## AI Collaboration Rules

### Response Format
- Use clear, structured responses with code examples
- Include explanations for complex logic
- Provide context for design decisions
- Use markdown formatting for readability

### Edit Rules
- **Full-file edits**: For new files or complete rewrites
- **Patch edits**: For specific function or component updates
- **Search and replace**: For simple text changes
- Always maintain existing code structure and conventions

### Ambiguity Handling
- Ask clarifying questions when requirements are unclear
- Provide multiple implementation options when appropriate
- Explain trade-offs and considerations
- Suggest improvements while maintaining existing patterns

### Code Generation Guidelines
- Generate complete, runnable code
- Include necessary imports and dependencies
- Add appropriate error handling
- Include comments for complex logic
- Follow established patterns in the codebase

## Dependencies & Setup

### Backend Dependencies
- FastAPI: Web framework
- SQLAlchemy: ORM
- Alembic: Database migrations
- Celery: Background tasks
- Redis: Caching and message broker
- Pydantic: Data validation
- Python-multipart: File uploads
- PyJWT: JWT authentication

### Frontend Dependencies
- Next.js: React framework
- TypeScript: Type safety
- Tailwind CSS: Styling
- React Hook Form: Form management
- Axios: HTTP client
- React Query: Data fetching
- Zustand: State management

### Environment Variables
```bash
# Backend
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

## Workflow & Tools

### Local Development Setup
1. Clone the repository
2. Copy `env.example` to `.env` and configure variables
3. Run `docker-compose up -d` for database and Redis
4. Install backend dependencies: `pip install -r requirements.txt`
5. Install frontend dependencies: `cd frontend && npm install`
6. Run database migrations: `alembic upgrade head`
7. Start backend: `uvicorn app.main:app --reload`
8. Start frontend: `cd frontend && npm run dev`

### Development Commands
```bash
# Backend
uvicorn app.main:app --reload          # Start development server
pytest tests/                          # Run tests
alembic revision --autogenerate        # Create migration
alembic upgrade head                   # Apply migrations

# Frontend
npm run dev                            # Start development server
npm run build                          # Build for production
npm run test                           # Run tests
npm run lint                           # Lint code
```

### Testing Strategy
- **Unit tests**: Test individual functions and components
- **Integration tests**: Test API endpoints and database operations
- **End-to-end tests**: Test complete user workflows
- **Performance tests**: Test system under load

## Contextual Knowledge

### Business Logic
- Document processing follows a specific workflow: upload → classify → extract → validate → store
- Validation tasks are created when confidence scores are below threshold
- Knowledge base search uses semantic similarity and keyword matching
- File storage supports multiple formats with automatic conversion

### Domain Rules
- Users can only access documents they uploaded or have been shared with
- Processing queue prioritizes documents based on user role and document type
- Validation tasks are automatically assigned to available users
- Search results are ranked by relevance and recency

### Technical Constraints
- File upload size limit: 50MB per file
- Supported formats: PDF, DOCX, JPG, PNG, TIFF
- Processing timeout: 30 minutes per document
- Rate limiting: 100 requests per minute per user
- Database connection pool: 20 connections

### Security Considerations
- All file uploads are scanned for malware
- Sensitive data is encrypted at rest
- API endpoints require authentication
- CORS is configured for specific origins only
- Audit logs track all user actions

## Examples

### Good AI Response
```typescript
// ✅ Good: Complete component with proper typing and error handling
interface DocumentCardProps {
  document: Document;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
}

export const DocumentCard: React.FC<DocumentCardProps> = ({
  document,
  onEdit,
  onDelete
}) => {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    try {
      setIsDeleting(true);
      await onDelete(document.id);
    } catch (error) {
      console.error('Failed to delete document:', error);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <h3 className="text-lg font-semibold">{document.title}</h3>
      <p className="text-gray-600 text-sm">{document.filename}</p>
      <div className="flex gap-2 mt-4">
        <button
          onClick={() => onEdit(document.id)}
          className="px-3 py-1 bg-blue-500 text-white rounded"
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className="px-3 py-1 bg-red-500 text-white rounded disabled:opacity-50"
        >
          {isDeleting ? 'Deleting...' : 'Delete'}
        </button>
      </div>
    </div>
  );
};
```

### Bad AI Response
```typescript
// ❌ Bad: Incomplete, no error handling, poor typing
export const DocumentCard = ({ document, onEdit, onDelete }) => {
  return (
    <div>
      <h3>{document.title}</h3>
      <button onClick={() => onEdit(document.id)}>Edit</button>
      <button onClick={() => onDelete(document.id)}>Delete</button>
    </div>
  );
};
```

### Good Backend Response
```python
# ✅ Good: Proper error handling, type hints, documentation
from typing import List, Optional
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

@router.get("/documents/", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[DocumentResponse]:
    """
    Retrieve a list of documents with optional filtering.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        status: Filter by document status
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of document responses
        
    Raises:
        HTTPException: If user is not authorized
    """
    try:
        documents = DocumentService.get_user_documents(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            status=status
        )
        return documents
    except Exception as e:
        logger.error(f"Failed to retrieve documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Bad Backend Response
```python
# ❌ Bad: No error handling, no type hints, no documentation
@router.get("/documents/")
def get_documents(db, user):
    documents = db.query(Document).filter_by(user_id=user.id).all()
    return documents
```

## Collaboration Guidelines

### When Working with Claude
1. **Be specific**: Provide clear requirements and context
2. **Show examples**: Reference existing code patterns
3. **Explain constraints**: Mention technical or business limitations
4. **Ask for clarification**: If requirements are unclear
5. **Review generated code**: Ensure it meets your needs

### Code Review Process
1. Check for adherence to coding conventions
2. Verify error handling and edge cases
3. Ensure proper testing coverage
4. Validate security considerations
5. Confirm performance implications

### Continuous Improvement
- Update documentation as code evolves
- Refactor code for better maintainability
- Add tests for new functionality
- Optimize performance bottlenecks
- Enhance security measures

This guide ensures consistent, high-quality code development and effective collaboration between human developers and AI assistants.

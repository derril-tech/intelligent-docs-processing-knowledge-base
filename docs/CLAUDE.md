# Claude AI Collaboration Guide

## Project Overview

**DocuMind™** is an AI Document Intelligence & RAG Knowledge OS designed to turn any document corpus into an always-on, trustworthy knowledge system with verifiable answers. The platform ingests messy PDFs, slides, emails, and code docs; enriches them with OCR, structure, entities, and citations; then serves grounded answers via a production-grade RAG pipeline. Designed for regulated teams that need correctness, speed, and scale.

### Core Jobs-to-be-Done
Upload → Clean/Extract → Index (RAG) → Ask/Automate → Cite & Export

### Key Differentiators
- Evidence-linked answers with source citations
- Policy-aware redaction and PII handling
- Human-in-the-loop validation for low-confidence results
- Multi-tenant isolation and enterprise security
- Production-grade RAG pipeline with LangChain + LangGraph

### Technology Stack
- **Backend**: FastAPI (async), SQLAlchemy 2.0, PostgreSQL 15+ (with pgvector), Redis 7+, Celery/Arq
- **Frontend**: Next.js 14+ (App Router), TypeScript 5+, Tailwind CSS 3+, React Hook Form, TanStack Query, Zustand
- **AI/ML**: LangChain (tooling & retrievers), LangGraph (stateful graph orchestration), CrewAI (multi-agent teams), RAG pipeline, OCR (Tesseract), NLP (spaCy)
- **Search**: Elasticsearch 8+ (hybrid search), pgvector (vector similarity)
- **Infrastructure**: Docker, Docker Compose, AWS (production), Vercel (frontend)
- **Testing**: pytest, Jest, Playwright, React Testing Library
- **Multi-Tenant**: Row-level security, tenant isolation, role-based access control

### Target Users
- **CX Teams**: Customer experience and support enablement
- **Legal Teams**: Contract analysis and compliance documentation
- **Operations Teams**: Process documentation and knowledge management
- **Revenue Operations**: Sales enablement and customer data
- **Product Teams**: Technical documentation and feature specs
- **Engineering Teams**: Code documentation and technical knowledge

### Project Goals
- **RAG Pipeline Excellence**: Build production-grade retrieval-augmented generation with ≥95% citation accuracy
- **Enterprise Security**: Multi-tenant isolation, AES-256 encryption, SOC2-ready controls
- **Performance & Scale**: <700ms retrieval latency, 10k concurrent chats, 1M+ documents
- **Evidence-Driven Answers**: Every answer includes verifiable citations and source spans
- **Human-in-the-Loop Validation**: Automated confidence scoring with manual review for low-confidence results
- **99.9% Uptime**: Enterprise-grade reliability with comprehensive monitoring and alerting

## Folder & File Structure

### Editable Files (Claude can modify)
- `app/api/v1/endpoints/` - API endpoint implementations (including new RAG endpoints)
- `app/services/` - Business logic implementation (RAG pipeline, validation, search)
- `app/schemas/` - Pydantic model definitions (including RAG schemas)
- `app/tasks/` - Background task implementations (ingestion, indexing, processing)
- `frontend/app/` - Next.js pages and layouts (Ingest Studio, Ask Workspace, Validation Queue, Admin Console)
- `frontend/components/features/` - Feature-specific components
- `frontend/hooks/` - Custom React hooks
- `frontend/types/` - TypeScript type definitions
- `tests/` - Test files and fixtures

### Do-Not-Touch Files (Infrastructure only)
- `app/core/` - Core configuration and infrastructure (including tenant middleware)
- `app/models/` - Database models (use migrations instead)
- `alembic/` - Database migration files
- `docker-compose.yml` - Container orchestration
- `Dockerfile` - Container definitions
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies
- Configuration files (`.env`, `alembic.ini`, etc.)
- `scripts/` - Database initialization and seeding scripts

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
- **FastAPI**: Web framework with async support
- **SQLAlchemy 2.0**: Modern ORM with async support
- **Alembic**: Database migrations
- **Celery/Arq**: Background task processing
- **Redis 7+**: Caching, message broker, rate limiting
- **Pydantic**: Data validation and serialization
- **LangChain**: RAG tooling and retrievers
- **LangGraph**: Stateful graph orchestration
- **CrewAI**: Multi-agent team coordination
- **Elasticsearch 8+**: Hybrid search and aggregations
- **pgvector**: Vector similarity search
- **Python-multipart**: File uploads
- **PyJWT**: JWT authentication
- **sentence-transformers**: Embedding generation
- **spacy**: NLP processing

### Frontend Dependencies
- **Next.js 14+**: React framework with App Router and server actions
- **TypeScript 5+**: Type safety and development experience
- **Tailwind CSS 3+**: Utility-first styling with design tokens
- **React Hook Form**: Form management and validation
- **TanStack Query**: Server state management and caching
- **Zustand**: Local UX state management
- **Socket.IO**: Real-time communication for streaming answers
- **Radix UI**: Accessible component primitives
- **shadcn/ui**: Component library with design tokens

### Environment Variables
```bash
# Backend
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379
ELASTICSEARCH_URL=http://localhost:9200
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AI/ML Providers
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
EMBEDDING_MODEL=text-embedding-3-large

# RAG Pipeline Configuration
DEFAULT_EMBEDDING_MODEL=text-embedding-3-large
DEFAULT_LLM_MODEL=gpt-4-turbo-preview
CITATION_CONFIDENCE_THRESHOLD=85
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Storage
S3_BUCKET=your-s3-bucket
S3_ACCESS_KEY=your-s3-key
S3_SECRET_KEY=your-s3-secret

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

## Workflow & Tools

### Local Development Setup
1. Clone the repository
2. Copy `env.example` to `.env` and configure variables
3. Run `docker-compose up -d` for database, Redis, and Elasticsearch
4. Install backend dependencies: `pip install -r requirements.txt`
5. Install frontend dependencies: `cd frontend && npm install`
6. Run database migrations: `alembic upgrade head`
7. Start backend: `uvicorn app.main:app --reload`
8. Start frontend: `cd frontend && npm run dev`
9. Access DocuMind™ at `http://localhost:3000`

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
- **End-to-end tests**: Test complete user workflows with Playwright
- **Performance tests**: Test system under load with Locust
- **RAG Pipeline tests**: Test retrieval accuracy and citation quality
- **Security tests**: Test authentication, authorization, and data isolation

## Contextual Knowledge

### Business Logic
- **RAG Pipeline**: Document processing follows: upload → OCR/layout → chunk → embed → index → retrieve → rerank → generate → cite
- **Validation Workflow**: Low-confidence spans trigger human-in-the-loop validation tasks
- **Hybrid Search**: Combines dense vector similarity (pgvector) with sparse BM25 (Elasticsearch) using reciprocal rank fusion
- **Multi-Agent Orchestration**: CrewAI coordinates specialized agents for complex workflows
- **Citation Management**: Every generated answer includes verifiable source citations with span references
- **Multi-Tenant Isolation**: Row-level security ensures complete tenant data isolation
- **Document Chunking**: Intelligent text splitting with metadata preservation and deduplication

### Domain Rules
- **Multi-Tenant Isolation**: Users can only access documents within their tenant/organization
- **Processing Priority**: Documents prioritized by user role, document type, and business criticality
- **Validation Assignment**: Low-confidence results automatically assigned to qualified validators
- **Search Ranking**: Results ranked by relevance (hybrid score), recency, and citation quality
- **Citation Requirements**: All generated answers must include ≥1 valid citation with source verification
- **Tenant Limits**: Configurable limits for users, documents, and storage per tenant
- **Role-Based Access**: Admin, User, Validator, and Viewer roles with different permissions

### Technical Constraints
- **File Upload**: 50MB per file, supports PDF, DOCX, JPG, PNG, TIFF, plus code docs and emails
- **Processing Timeout**: 30 minutes per document for complex workflows
- **Rate Limiting**: 100 requests per minute per user (Redis sliding window)
- **Database**: PostgreSQL 15+ with pgvector, 20 connection pool
- **Search**: Elasticsearch 8+ for hybrid search, pgvector for vector similarity
- **Performance Targets**: <700ms retrieval, <2.0s first token, P95 <4s end-to-end

### Security Considerations
- **Multi-Tenant Security**: Row-level security and schema isolation per tenant
- **Encryption**: AES-256 at rest, TLS 1.2+ in transit, KMS-managed keys
- **PII Handling**: Automatic detection and redaction of sensitive data
- **API Security**: JWT authentication, scoped API keys, rate limiting
- **Audit Logging**: Immutable audit trail with correlation IDs
- **Compliance**: SOC2-ready controls, GDPR compliance, enterprise SSO support

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

## Patch Protocol

### Diff Format Requirements
All code changes must be provided in unified diff format:

```diff
// File: path/to/file.ts
- // Old code or comment
+ // New code or comment
```

### Commit Message Format
Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

**Types**: feat, fix, docs, style, refactor, test, chore
**Scope**: frontend, backend, api, ui, auth, etc.

**Examples**:
```
feat(frontend): add document upload component
fix(api): resolve authentication token validation
docs(readme): update installation instructions
```

## Failure-Mode Playbook

### Common Issues and Solutions

#### Schema Mismatch
**Problem**: Frontend types don't match backend schemas
**Solution**: 
1. Update shared types in `packages/types/`
2. Regenerate API client types
3. Update both frontend and backend schemas

#### Failing Tests
**Problem**: Tests fail after code changes
**Solution**:
1. Run `npm test` or `pytest` locally
2. Check test environment setup
3. Update test fixtures if needed
4. Verify mock implementations

#### Missing Environment Variables
**Problem**: Application fails due to missing env vars
**Solution**:
1. Check `.env.example` for required variables
2. Copy missing variables to `.env.local`
3. Verify environment-specific configurations
4. Update documentation if new vars are needed

#### Database Migration Issues
**Problem**: Database schema out of sync
**Solution**:
1. Run `alembic upgrade head`
2. Check migration files for conflicts
3. Reset database if in development
4. Create new migration if needed

#### Build Failures
**Problem**: Frontend or backend build fails
**Solution**:
1. Check dependency versions in package.json/requirements.txt
2. Clear node_modules and reinstall
3. Check TypeScript compilation errors
4. Verify import paths and aliases

#### Docker Issues
**Problem**: Containerized environment not working
**Solution**:
1. Rebuild Docker images: `docker-compose build`
2. Check port conflicts
3. Verify volume mounts
4. Check container logs: `docker-compose logs`

## START/END Guardrails

### File Boundaries
Use these markers in editable files to define safe editing zones:

```typescript
// START: EDITABLE ZONE
// This section can be safely modified by Claude
export const MyComponent = () => {
  // Implementation here
};
// END: EDITABLE ZONE

// DO NOT EDIT BELOW THIS LINE
// Infrastructure and configuration code
```

### Protected Sections
- Database models (use migrations instead)
- Core configuration files
- Docker and deployment configs
- Package.json dependencies (discuss changes first)
- Environment-specific settings

### Safe Editing Zones
- API endpoint implementations
- Service layer business logic
- Frontend components and pages
- Test files and fixtures
- Documentation updates

This guide ensures consistent, high-quality code development and effective collaboration between human developers and AI assistants.

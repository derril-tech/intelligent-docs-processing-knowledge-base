# Backend Documentation - DocuMind™

## Overview

The DocuMind™ backend is built with FastAPI, providing a robust API for document processing, RAG pipeline management, and multi-tenant knowledge base operations. It features production-grade RAG with LangChain, LangGraph, and CrewAI integration.

## Tech Stack

- **Framework**: FastAPI (async/await)
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+ with pgvector
- **ORM**: SQLAlchemy 2.0
- **Cache/Queue**: Redis 7+
- **Search**: Elasticsearch 8+
- **AI/ML**: LangChain, LangGraph, CrewAI
- **Background Tasks**: Celery
- **Authentication**: JWT
- **Testing**: pytest, pytest-asyncio

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ with pgvector extension
- Redis 7+
- Elasticsearch 8+

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp env.example .env

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/doc_processing
REDIS_URL=redis://localhost:6379
ELASTICSEARCH_URL=http://localhost:9200

# Security
SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI/ML Providers
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
EMBEDDING_MODEL=text-embedding-3-large

# RAG Configuration
DEFAULT_EMBEDDING_MODEL=text-embedding-3-large
DEFAULT_LLM_MODEL=gpt-4-turbo-preview
CITATION_CONFIDENCE_THRESHOLD=85
```

## Project Structure

```
app/
├── api/                   # API layer
│   └── v1/
│       ├── endpoints/     # Route handlers
│       └── api.py         # Router configuration
├── core/                  # Core configuration
│   ├── config.py          # Settings management
│   ├── database.py        # Database connection
│   ├── security.py        # Authentication
│   └── tenant_middleware.py # Multi-tenant support
├── models/                # Database models
├── schemas/               # Pydantic models
├── services/              # Business logic
├── tasks/                 # Background tasks
└── main.py               # Application entry point
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/refresh` - Refresh token

### Documents
- `GET /documents/` - List documents
- `POST /documents/` - Upload document
- `GET /documents/{id}` - Get document details
- `PUT /documents/{id}` - Update document
- `DELETE /documents/{id}` - Delete document

### RAG Pipeline
- `POST /rag/ask` - Ask question with RAG
- `GET /rag/answers` - Get user's previous answers
- `GET /rag/search` - Search document chunks
- `POST /rag/process-document/{id}` - Process document for RAG

### Validation
- `GET /validation/tasks/` - List validation tasks
- `POST /validation/tasks/` - Create validation task
- `PUT /validation/tasks/{id}` - Update validation task
- `POST /validation/tasks/{id}/results` - Submit validation results

### Knowledge Base
- `GET /knowledge/` - List knowledge base entries
- `POST /knowledge/` - Create knowledge base entry
- `GET /knowledge/search` - Search knowledge base

## Development Guidelines

### API Structure
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter()

@router.post("/documents/", response_model=DocumentResponse)
async def create_document(
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> DocumentResponse:
    """Create a new document."""
    # Implementation
    pass
```

### Service Layer
```python
class DocumentService:
    @staticmethod
    async def create_document(
        db: Session,
        document_data: DocumentCreate,
        user_id: int
    ) -> Document:
        """Create document with business logic."""
        # Implementation
        pass
```

### Background Tasks
```python
from celery import Celery
from app.core.celery import celery_app

@celery_app.task
def process_document_task(document_id: int):
    """Process document in background."""
    # Implementation
    pass
```

## Database Models

### Core Models
- `User` - User accounts with roles
- `Tenant` - Multi-tenant organizations
- `Document` - Document metadata and status
- `DocumentChunk` - Text chunks with embeddings
- `Answer` - RAG-generated answers
- `Citation` - Source citations for answers

### Relationships
```python
class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="documents")
    user = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document")
```

## RAG Pipeline

### Components
1. **Document Processing**: OCR, text extraction, chunking
2. **Embedding Generation**: Vector embeddings for chunks
3. **Indexing**: Vector and keyword indexing
4. **Retrieval**: Hybrid search (vector + BM25)
5. **Generation**: LLM-based answer generation
6. **Citation**: Source verification and linking

### Usage
```python
from app.services.rag_service import RAGService

rag_service = RAGService()

# Process document
chunks = await rag_service.process_document(db, document, content)

# Ask question
result = await rag_service.ask_question(db, question, user_id, tenant_id)
```

## Multi-Tenant Security

### Row-Level Security
```sql
-- Enable RLS on tables
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Create tenant isolation policy
CREATE POLICY tenant_isolation ON documents
FOR ALL USING (tenant_id = current_setting('app.current_tenant_id')::integer);
```

### Middleware
```python
from app.core.tenant_middleware import get_current_tenant

@router.get("/documents/")
async def get_documents(
    current_tenant: Tenant = Depends(get_current_tenant)
):
    # Tenant context automatically applied
    pass
```

## Testing

### Unit Tests
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_documents.py
```

### Integration Tests
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_document():
    response = client.post("/documents/", json={"title": "Test"})
    assert response.status_code == 201
```

### Database Tests
```python
@pytest.fixture
def db_session():
    # Setup test database
    pass

def test_document_creation(db_session):
    # Test with database session
    pass
```

## Background Tasks

### Celery Configuration
```python
# app/core/celery.py
from celery import Celery

celery_app = Celery(
    "documind",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)
```

### Task Examples
```python
@celery_app.task
def process_document_task(document_id: int):
    """Process document with OCR and chunking."""
    pass

@celery_app.task
def generate_embeddings_task(chunk_ids: List[int]):
    """Generate embeddings for document chunks."""
    pass
```

## Monitoring & Logging

### Structured Logging
```python
import structlog

logger = structlog.get_logger()

logger.info("Document processed", 
    document_id=doc.id, 
    chunks_created=len(chunks))
```

### Health Checks
```python
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "elasticsearch": "connected"
    }
```

## Performance

### Database Optimization
- Connection pooling (20 connections)
- Indexed queries for common patterns
- Vector similarity search with pgvector

### Caching Strategy
- Redis for session storage
- Query result caching
- Embedding cache for repeated chunks

### API Performance
- Async/await for I/O operations
- Background task processing
- Pagination for large datasets

## Security

### Authentication
- JWT tokens with expiration
- Refresh token rotation
- Role-based access control

### Data Protection
- Multi-tenant isolation
- Row-level security
- PII detection and redaction

### API Security
- Rate limiting (100 req/min per user)
- Input validation with Pydantic
- CORS configuration

## Deployment

### Docker
```bash
# Build image
docker build -t documind-backend .

# Run container
docker run -p 8000:8000 documind-backend
```

### Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api
```

### Production
```bash
# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Run Celery worker
celery -A app.core.celery worker --loglevel=info
```

## Troubleshooting

### Common Issues

1. **Database Connection**
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - Check pgvector extension

2. **Redis Connection**
   - Verify Redis server is running
   - Check REDIS_URL format
   - Test with redis-cli

3. **Elasticsearch**
   - Check ELASTICSEARCH_URL
   - Verify cluster health
   - Check index mappings

4. **AI/ML Services**
   - Verify API keys are set
   - Check rate limits
   - Test with simple queries

## Contributing

1. Follow PEP 8 and Black formatting
2. Write tests for new features
3. Update API documentation
4. Use type hints throughout
5. Follow the coding conventions in `docs/CLAUDE.md`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [LangChain Documentation](https://python.langchain.com/)
- [Celery Documentation](https://docs.celeryproject.org/)

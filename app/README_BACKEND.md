# Backend - Intelligent Docs Processing Knowledge Base

## Overview
FastAPI-based backend application with PostgreSQL, Redis, Elasticsearch, and Celery for document processing and knowledge base management.

## Tech Stack
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis 7
- **Search**: Elasticsearch 8.11
- **Task Queue**: Celery
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT tokens
- **File Storage**: Local/S3 compatible

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15
- Redis 7
- Elasticsearch 8.11

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup
Copy `env.example` to `.env` and configure:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/doc_processing
REDIS_URL=redis://localhost:6379
ELASTICSEARCH_URL=http://localhost:9200
SECRET_KEY=your-secret-key
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=./uploads
```

### Database Setup
```bash
# Run migrations
alembic upgrade head

# Seed initial data (if available)
python -m app.scripts.seed_data
```

### Development
```bash
# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start Celery worker (in separate terminal)
celery -A app.core.celery worker --loglevel=info

# Start Celery beat (in separate terminal)
celery -A app.core.celery beat --loglevel=info
```

### Docker Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api
```

## Project Structure

```
app/
├── api/                   # API routes and endpoints
│   └── v1/
│       ├── endpoints/     # Feature-specific endpoints
│       └── api.py         # API router
├── core/                  # Core configuration
│   ├── config.py          # Settings management
│   ├── database.py        # Database connection
│   ├── security.py        # Authentication & authorization
│   └── celery.py          # Celery configuration
├── models/                # SQLAlchemy models
├── schemas/               # Pydantic schemas
├── services/              # Business logic
├── tasks/                 # Celery tasks
└── main.py                # FastAPI application
```

## API Documentation

### Interactive Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Health Check
```bash
curl http://localhost:8000/health
```

## Key Features

### Authentication & Authorization
- JWT-based authentication
- Role-based access control
- User management endpoints

### Document Processing
- File upload and validation
- Background processing with Celery
- Progress tracking and status updates

### Knowledge Base
- Document indexing in Elasticsearch
- Semantic search capabilities
- Knowledge graph construction

### Validation System
- Automated validation tasks
- Human-in-the-loop validation
- Quality assurance workflows

## Development Guidelines

### Code Style
- Follow PEP 8 standards
- Use type hints throughout
- Document all public functions
- Use Pydantic for data validation

### Database
- Use Alembic for migrations
- Follow SQLAlchemy 2.0 patterns
- Implement proper relationships
- Use async/await for database operations

### API Design
- Follow RESTful principles
- Use proper HTTP status codes
- Implement pagination for list endpoints
- Provide comprehensive error responses

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

## Monitoring & Observability

### Health Checks
- Database connectivity
- Redis connectivity
- Elasticsearch health
- External service status

### Logging
- Structured logging with JSON format
- Different log levels for different environments
- Request/response logging
- Error tracking and alerting

### Metrics
- API response times
- Database query performance
- Celery task metrics
- System resource usage

## Deployment

### Docker
```bash
# Build image
docker build -t api .

# Run container
docker run -p 8000:8000 api
```

### Production Considerations
- Use environment-specific configurations
- Implement proper logging and monitoring
- Set up database connection pooling
- Configure rate limiting and security headers
- Use HTTPS in production
- Implement backup strategies

## Troubleshooting

### Common Issues
1. **Database connection errors**: Check DATABASE_URL and PostgreSQL status
2. **Redis connection errors**: Verify Redis is running and accessible
3. **Elasticsearch issues**: Check cluster health and disk space
4. **Celery task failures**: Review worker logs and task queue status

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload --log-level debug
```

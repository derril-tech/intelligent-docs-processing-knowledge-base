# Intelligent Document Processing and Knowledge Base API

A comprehensive, AI-powered platform designed to transform unstructured and semi-structured documents into a rich, accessible, and actionable knowledge base. This system eliminates the manual, time-consuming, and error-prone process of data entry and document review, enabling organizations to unlock critical insights hidden within their documents and make smarter, data-driven decisions.

## 🚀 Features

- **Intelligent Document Ingestion**: Supports multiple document sources (emails, scanners, file uploads, APIs)
- **AI-Powered Data Extraction**: OCR, NLP, and ML for accurate information extraction
- **Dynamic Document Classification**: Automatic categorization and routing
- **Data Validation & Verification**: Rules-based validation with human-in-the-loop review
- **Knowledge Base Creation**: Searchable, structured, interconnected knowledge base
- **Seamless Integration**: Designed to integrate with existing business systems
- **Scalability & Security**: Built to handle high volumes with robust security measures

## 🏗️ Architecture

### Tech Stack

**Backend Framework:**
- **Python 3.11** with **FastAPI** for high-performance async API development
- **SQLAlchemy** with **Alembic** for ORM and database migrations
- **Celery** with **Redis** for background task processing

**Databases:**
- **PostgreSQL** - Primary database for structured data
- **Elasticsearch** - Full-text search and knowledge base queries
- **Redis** - Caching and session management

**File Storage:**
- **AWS S3** / **Google Cloud Storage** / **Local Storage** - Document storage
- **AWS Textract** / **Google Cloud Vision API** - OCR services

**AI/ML Services:**
- **OpenAI GPT-4** / **Anthropic Claude** - NLP processing
- **Hugging Face Transformers** - Document classification
- **AWS Comprehend** / **Google Cloud NLP** - Entity extraction

**Additional Services:**
- **JWT** for authentication
- **Docker** for containerization
- **Pytest** for testing
- **Prometheus/Grafana** for monitoring

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+
- Elasticsearch 8.11+

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd intelligent-docs-processing-knowledge-base
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
nano .env
```

### 3. Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f api
```

### 4. Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
alembic upgrade head

# Run the application
uvicorn app.main:app --reload
```

## 🗄️ Database Setup

### Using Docker Compose
The database is automatically set up when using Docker Compose.

### Manual Setup
```bash
# Create PostgreSQL database
createdb doc_processing

# Run migrations
alembic upgrade head

# Create initial data (optional)
python scripts/create_initial_data.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost:5432/doc_processing` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `ELASTICSEARCH_URL` | Elasticsearch URL | `http://localhost:9200` |
| `STORAGE_TYPE` | File storage type (local/s3/gcs) | `local` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `SECRET_KEY` | JWT secret key | - |

### File Storage Configuration

The system supports multiple storage backends:

- **Local Storage**: Files stored on local filesystem
- **AWS S3**: Cloud storage with S3
- **Google Cloud Storage**: Cloud storage with GCS

## 📚 API Documentation

### Authentication

The API uses JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/token` - OAuth2 token endpoint
- `GET /api/v1/auth/me` - Get current user info

#### Documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/` - List user documents
- `GET /api/v1/documents/{id}` - Get document details
- `GET /api/v1/documents/{id}/status` - Get processing status
- `DELETE /api/v1/documents/{id}` - Delete document

#### Knowledge Base
- `GET /api/v1/knowledge/search` - Search knowledge base
- `GET /api/v1/knowledge/entries` - List knowledge entries
- `GET /api/v1/knowledge/entries/{id}` - Get knowledge entry
- `GET /api/v1/knowledge/stats` - Get knowledge base statistics

#### Processing
- `GET /api/v1/processing/queue/status` - Get processing queue status
- `GET /api/v1/processing/tasks` - List processing tasks
- `POST /api/v1/processing/tasks/{id}/retry` - Retry failed task
- `POST /api/v1/processing/tasks/{id}/cancel` - Cancel task

#### Validation
- `GET /api/v1/validation/queue` - Get validation queue
- `POST /api/v1/validation/tasks/{id}/assign` - Assign validation task
- `POST /api/v1/validation/tasks/{id}/validate` - Submit validation result
- `GET /api/v1/validation/my-tasks` - Get user's validation tasks

### Interactive API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔄 Background Processing

The system uses Celery for background task processing:

### Start Celery Workers

```bash
# Start worker
celery -A app.core.celery worker --loglevel=info

# Start beat scheduler
celery -A app.core.celery beat --loglevel=info

# Monitor with Flower
celery -A app.core.celery flower --port=5555
```

### Using Docker Compose

Celery services are automatically started with Docker Compose:
- **Worker**: `celery_worker` service
- **Beat**: `celery_beat` service  
- **Flower**: Available at http://localhost:5555

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_documents.py

# Run with verbose output
pytest -v
```

## 📊 Monitoring

### Health Checks

- **API Health**: `GET /health`
- **Database**: Automatic health checks in Docker Compose
- **Celery**: Monitor via Flower at http://localhost:5555

### Logging

The application uses structured logging with JSON format. Logs include:
- Request/response logging
- Processing pipeline events
- Error tracking
- Performance metrics

## 🔒 Security

### Authentication & Authorization
- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- Token expiration and refresh

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- CORS configuration
- Rate limiting (configurable)

### File Security
- File type validation
- Size limits
- Secure file storage
- Access control

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   # Set production environment variables
   export ENVIRONMENT=production
   export DEBUG=false
   ```

2. **Database Migration**
   ```bash
   alembic upgrade head
   ```

3. **Static Files**
   ```bash
   # Collect static files (if any)
   python manage.py collectstatic
   ```

4. **Process Management**
   ```bash
   # Use Gunicorn for production
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Docker Production

```bash
# Build production image
docker build -t doc-processing-api .

# Run with production settings
docker run -d \
  -p 8000:8000 \
  --env-file .env.production \
  doc-processing-api
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the logs for error details

## 🔮 Roadmap

- [ ] Advanced AI model integration
- [ ] Real-time processing notifications
- [ ] Advanced analytics dashboard
- [ ] Multi-tenant support
- [ ] API rate limiting
- [ ] Advanced search capabilities
- [ ] Document versioning
- [ ] Workflow automation

# Repository Map

## Overview
This document provides a comprehensive breakdown of the Intelligent Document Processing and Knowledge Base repository structure, explaining the purpose and organization of each folder and file.

## Root Directory Structure

```
intelligent-docs-processing/
├── docs/                          # Documentation files
├── app/                           # Backend application
├── frontend/                      # Frontend application
├── alembic/                       # Database migrations
├── scripts/                       # Development and deployment scripts
├── tests/                         # Test files
├── docker-compose.yml            # Docker orchestration
├── Dockerfile                    # Backend container definition
├── requirements.txt              # Python dependencies
├── alembic.ini                   # Alembic configuration
├── env.example                   # Environment variables template
└── README.md                     # Project overview
```

## Backend Structure (`app/`)

### Core Infrastructure (`app/core/`)
**Purpose**: Core application configuration and infrastructure setup.

**Files**:
- `config.py` - Application configuration management
- `database.py` - Database connection and session management
- `security.py` - Authentication and authorization utilities
- `logging.py` - Logging configuration
- `celery.py` - Celery task queue configuration

**Responsibilities**:
- Environment variable management
- Database connection pooling
- JWT token handling
- Structured logging setup
- Background task configuration

### API Layer (`app/api/`)
**Purpose**: REST API endpoints and request/response handling.

**Structure**:
```
app/api/
├── __init__.py
├── v1/                           # API version 1
│   ├── __init__.py
│   ├── api.py                    # Main API router
│   └── endpoints/                # Route handlers
│       ├── __init__.py
│       ├── auth.py               # Authentication endpoints
│       ├── documents.py          # Document management
│       ├── knowledge_base.py     # Knowledge base search
│       ├── processing.py         # Processing queue
│       ├── users.py              # User management
│       └── validation.py         # Validation tasks
```

**Responsibilities**:
- HTTP request/response handling
- Input validation and sanitization
- Authentication middleware
- Rate limiting
- Error handling and logging

### Data Models (`app/models/`)
**Purpose**: SQLAlchemy database models and relationships.

**Files**:
- `user.py` - User account model
- `document.py` - Document storage and metadata
- `knowledge_base.py` - Knowledge base entries
- `processing_queue.py` - Processing job tracking
- `validation_queue.py` - Human validation tasks

**Responsibilities**:
- Database schema definition
- Model relationships and constraints
- Data validation rules
- Migration compatibility

### Data Schemas (`app/schemas/`)
**Purpose**: Pydantic models for API request/response validation.

**Files**:
- `user.py` - User-related schemas
- `document.py` - Document schemas
- `knowledge_base.py` - Knowledge base schemas
- `processing.py` - Processing schemas
- `validation.py` - Validation schemas

**Responsibilities**:
- Input data validation
- Response data serialization
- API documentation generation
- Type safety enforcement

### Business Logic (`app/services/`)
**Purpose**: Core business logic and external service integration.

**Files**:
- `file_storage.py` - File upload and storage management
- `processing.py` - Document processing orchestration
- `search.py` - Knowledge base search functionality
- `validation.py` - Validation workflow management

**Responsibilities**:
- Business rule implementation
- External API integration
- Data transformation
- Workflow orchestration

### Background Tasks (`app/tasks/`)
**Purpose**: Celery background task definitions.

**Files**:
- `document_processing.py` - Document processing tasks
- `ai_processing.py` - AI/ML processing tasks
- `validation_tasks.py` - Validation workflow tasks

**Responsibilities**:
- Asynchronous task execution
- Long-running process management
- Task retry and error handling
- Progress tracking

## Frontend Structure (`frontend/`)

### Application Shell (`frontend/app/`)
**Purpose**: Next.js 13+ app directory structure with routing.

**Structure**:
```
frontend/app/
├── (auth)/                       # Authentication routes
│   ├── login/
│   │   └── page.tsx
│   └── register/
│       └── page.tsx
├── dashboard/                    # Main dashboard
│   ├── layout.tsx
│   └── page.tsx
├── documents/                    # Document management
│   └── page.tsx
├── processing/                   # Processing queue
│   └── page.tsx
├── globals.css                   # Global styles
├── layout.tsx                    # Root layout
└── page.tsx                      # Home page
```

**Responsibilities**:
- Page routing and navigation
- Layout management
- Authentication flow
- Global state management

### UI Components (`frontend/components/`)
**Purpose**: Reusable UI components and feature-specific components.

**Structure**:
```
frontend/components/
├── ui/                          # Base UI components
│   ├── button.tsx
│   ├── input.tsx
│   ├── modal.tsx
│   ├── table.tsx
│   └── index.ts                 # Component exports
└── features/                    # Feature-specific components
    ├── document-upload.tsx
    ├── knowledge-base-search.tsx
    ├── processing-queue.tsx
    ├── validation-tasks.tsx
    └── index.ts
```

**Responsibilities**:
- Consistent UI design
- Component reusability
- Accessibility compliance
- Responsive design

### Utilities (`frontend/lib/`)
**Purpose**: Utility functions, configurations, and shared logic.

**Files**:
- `api.ts` - API client configuration
- `auth.ts` - Authentication utilities
- `utils.ts` - General utility functions
- `constants.ts` - Application constants

**Responsibilities**:
- API client setup
- Authentication state management
- Common utility functions
- Configuration management

### Custom Hooks (`frontend/hooks/`)
**Purpose**: Custom React hooks for shared logic.

**Files**:
- `use-auth.ts` - Authentication state management
- `use-api.ts` - API call management
- `use-debounce.ts` - Debounced input handling
- `use-websocket.ts` - Real-time updates

**Responsibilities**:
- State management logic
- API integration
- Real-time communication
- Performance optimization

### Type Definitions (`frontend/types/`)
**Purpose**: TypeScript type definitions and interfaces.

**Files**:
- `auth.ts` - Authentication types
- `document.ts` - Document-related types
- `api.ts` - API response types
- `validation.ts` - Validation types

**Responsibilities**:
- Type safety
- API contract definition
- Development experience
- Documentation

## Database Migrations (`alembic/`)

**Purpose**: Database schema version control and migrations.

**Files**:
- `env.py` - Alembic environment configuration
- `script.py.mako` - Migration template
- `versions/` - Migration files directory

**Responsibilities**:
- Schema version control
- Database migration management
- Rollback capabilities
- Environment-specific configurations

## Development Scripts (`scripts/`)

**Purpose**: Development, testing, and deployment automation.

**Files**:
- `dev.sh` - Development environment startup
- `test.sh` - Test execution
- `deploy.sh` - Deployment automation
- `setup.sh` - Environment setup

**Responsibilities**:
- Development workflow automation
- Testing orchestration
- Deployment processes
- Environment management

## Configuration Files

### Backend Configuration
- `requirements.txt` - Python package dependencies
- `alembic.ini` - Database migration configuration
- `env.example` - Environment variables template
- `Dockerfile` - Backend container definition

### Frontend Configuration
- `package.json` - Node.js dependencies and scripts
- `tsconfig.json` - TypeScript configuration
- `tailwind.config.js` - Tailwind CSS configuration
- `next.config.js` - Next.js configuration
- `.eslintrc.json` - ESLint configuration
- `.prettierrc` - Prettier configuration

### Docker Configuration
- `docker-compose.yml` - Multi-container orchestration
- `Dockerfile` - Backend container definition
- `.dockerignore` - Docker build exclusions

## Documentation Structure (`docs/`)

**Purpose**: Comprehensive project documentation.

**Files**:
- `API_SPEC.md` - API endpoint documentation
- `REPO_MAP.md` - This repository structure guide
- `CLAUDE.md` - AI collaboration guidelines
- `PROMPT_DECLARATION.md` - Development prompt specification

**Responsibilities**:
- API documentation
- Development guidelines
- Architecture documentation
- AI collaboration rules

## Testing Structure (`tests/`)

**Purpose**: Comprehensive test coverage for all components.

**Structure**:
```
tests/
├── unit/                        # Unit tests
│   ├── test_models.py
│   ├── test_services.py
│   └── test_api.py
├── integration/                 # Integration tests
│   ├── test_database.py
│   └── test_api_integration.py
├── e2e/                        # End-to-end tests
│   └── test_user_flows.py
└── fixtures/                   # Test data
    ├── sample_documents/
    └── test_data.json
```

**Responsibilities**:
- Unit test coverage
- Integration testing
- End-to-end testing
- Test data management

## Environment Management

### Development Environment
- Local database (PostgreSQL)
- Redis for caching and task queue
- File storage (local filesystem)
- Development server configurations

### Production Environment
- Cloud database (AWS RDS)
- Redis cluster for scalability
- Cloud storage (AWS S3)
- Load balancer and CDN
- Monitoring and logging

## Security Considerations

### Authentication & Authorization
- JWT token-based authentication
- Role-based access control
- API rate limiting
- Input validation and sanitization

### Data Protection
- File encryption at rest
- Secure file upload validation
- PII data handling compliance
- Audit logging

### Infrastructure Security
- HTTPS enforcement
- CORS configuration
- Environment variable security
- Container security best practices

## Performance Optimization

### Backend Optimization
- Database query optimization
- Caching strategies
- Background task processing
- API response optimization

### Frontend Optimization
- Code splitting and lazy loading
- Image optimization
- Bundle size optimization
- Caching strategies

## Monitoring and Logging

### Application Monitoring
- Health check endpoints
- Performance metrics
- Error tracking
- User analytics

### Infrastructure Monitoring
- Server resource monitoring
- Database performance
- Queue monitoring
- File storage monitoring

## Deployment Strategy

### Development Deployment
- Local development environment
- Docker Compose for services
- Hot reloading for development
- Debug mode enabled

### Production Deployment
- Containerized deployment
- Blue-green deployment strategy
- Database migration automation
- Rollback procedures

## Development Workflow

### Code Organization
- Feature-based folder structure
- Clear separation of concerns
- Consistent naming conventions
- Comprehensive documentation

### Version Control
- Git flow branching strategy
- Commit message conventions
- Pull request reviews
- Automated testing on commits

### Quality Assurance
- Automated testing pipeline
- Code quality checks
- Security scanning
- Performance testing

This repository structure is designed to support scalable development, maintainable code, and efficient collaboration between team members and AI assistants.

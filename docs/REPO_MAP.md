# Repository Map

## Overview
This document provides a comprehensive breakdown of the Intelligent Document Processing and Knowledge Base repository structure, reflecting the current infrastructure with WebSocket real-time communication, Advanced RAG pipeline, Source Connectors, and Multi-Agent orchestration.

## Root Directory Structure

```
intelligent-docs-processing/
├── docs/                          # Documentation files
├── app/                           # Backend application
├── frontend/                      # Frontend application
├── packages/                      # Shared packages (types, UI tokens)
├── alembic/                       # Database migrations
├── scripts/                       # Development and deployment scripts
├── tests/                         # Test files
├── docker-compose.yml            # Docker orchestration
├── Dockerfile                    # Backend container definition
├── requirements.txt              # Python dependencies
├── pnpm-workspace.yaml           # Monorepo workspace configuration
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
- `websocket.py` - **NEW**: WebSocket server infrastructure with connection management
- `tenant_middleware.py` - **NEW**: Multi-tenant isolation and row-level security

**Responsibilities**:
- Environment variable management
- Database connection pooling
- JWT token handling
- Structured logging setup
- Background task configuration
- **Real-time WebSocket communication**
- **Multi-tenant data isolation**

### API Layer (`app/api/`)
**Purpose**: REST API endpoints and request/response handling.

**Structure**:
```
app/api/
├── __init__.py
├── v1/                           # API version 1
│   ├── __init__.py
│   ├── api.py                    # Main API router (includes WebSocket endpoint)
│   └── endpoints/                # Route handlers
│       ├── __init__.py
│       ├── auth.py               # Authentication endpoints
│       ├── documents.py          # Document management
│       ├── knowledge_base.py     # Knowledge base search
│       ├── processing.py         # Processing queue
│       ├── users.py              # User management
│       ├── validation.py         # Validation tasks
│       └── rag.py                # **NEW**: Advanced RAG pipeline endpoints
```

**Responsibilities**:
- HTTP request/response handling
- Input validation and sanitization
- Authentication middleware
- Rate limiting
- Error handling and logging
- **WebSocket real-time communication**
- **Advanced RAG pipeline endpoints**

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
- `rag.py` - **NEW**: RAG pipeline schemas
- `websocket.py` - **NEW**: WebSocket event schemas

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
- `rag_service.py` - **NEW**: Basic RAG service implementation
- `advanced_rag.py` - **NEW**: LangGraph-based advanced RAG pipeline
- `connectors.py` - **NEW**: Source connectors for external services

**Responsibilities**:
- Business rule implementation
- External API integration
- Data transformation
- Workflow orchestration
- **Advanced RAG pipeline orchestration**
- **External service integrations**

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
**Purpose**: Next.js 14+ app directory structure with routing.

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
├── providers/                    # **NEW**: Context providers
│   ├── websocket-provider.tsx    # WebSocket real-time communication
│   └── index.tsx                 # Provider composition
├── globals.css                   # Global styles
├── layout.tsx                    # Root layout
└── page.tsx                      # Home page
```

**Responsibilities**:
- Page routing and navigation
- Layout management
- Authentication flow
- Global state management
- **Real-time WebSocket communication**

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
- `websocket.ts` - **NEW**: WebSocket client utilities

**Responsibilities**:
- API client setup
- Authentication state management
- Common utility functions
- Configuration management
- **WebSocket client management**

### Custom Hooks (`frontend/hooks/`)
**Purpose**: Custom React hooks for shared logic.

**Files**:
- `use-auth.ts` - Authentication state management
- `use-api.ts` - API call management
- `use-debounce.ts` - Debounced input handling
- `use-websocket.ts` - **NEW**: Real-time WebSocket updates

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
- `websocket.ts` - **NEW**: WebSocket event types
- `rag.ts` - **NEW**: RAG pipeline types

**Responsibilities**:
- Type safety
- API contract definition
- Development experience
- Documentation

## Shared Packages (`packages/`)

### Types Package (`packages/types/`)
**Purpose**: Shared TypeScript types across frontend and backend.

**Files**:
- `index.ts` - Type exports
- `api.ts` - API contract types
- `websocket.ts` - WebSocket event types
- `rag.ts` - RAG pipeline types

### UI Tokens (`packages/ui/`)
**Purpose**: Centralized design tokens for consistent styling.

**Files**:
- `tokens.ts` - Design tokens (colors, typography, spacing)

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

### Monorepo Configuration
- `pnpm-workspace.yaml` - **NEW**: Monorepo workspace configuration
- `package.json` - Root package configuration

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
- `INFRASTRUCTURE_PLAN.md` - **NEW**: 8-step infrastructure plan
- `PRODUCT_BRIEF.md` - **NEW**: Product requirements and features
- `BASELINE.md` - **NEW**: Project baseline and hygiene status
- `SCREEN_ENDPOINT_DTO_MATRIX.md` - **NEW**: Frontend-backend mapping

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

## Infrastructure Components

### WebSocket Infrastructure (`app/core/websocket.py`)
**Purpose**: Real-time communication for document processing updates and chat.

**Features**:
- Connection management with tenant isolation
- Event routing framework
- Authentication integration
- Broadcasting and notifications
- Error handling and cleanup

### Advanced RAG Pipeline (`app/services/advanced_rag.py`)
**Purpose**: LangGraph-based RAG pipeline with advanced retrieval and reranking.

**Features**:
- 5-step workflow (retrieve → rerank → generate → validate → cite)
- Hybrid retrieval (vector + keyword search)
- Cross-encoder reranking
- Reciprocal rank fusion
- Factuality verification
- Citation extraction

### Source Connectors (`app/services/connectors.py`)
**Purpose**: External service integrations for document synchronization.

**Supported Services**:
- Google Drive
- SharePoint
- Confluence
- Slack
- GitHub

**Features**:
- OAuth2 authentication
- Document synchronization
- Real-time status updates
- Rate limiting and retry logic

### Multi-Agent Orchestration (CrewAI)
**Purpose**: Complex document processing workflows with specialized agents.

**Features**:
- Agent coordination
- Task distribution
- Workflow orchestration
- Result aggregation

## Environment Management

### Development Environment
- Local database (PostgreSQL with pgvector)
- Redis for caching and task queue
- Elasticsearch for hybrid search
- File storage (local filesystem)
- Development server configurations

### Production Environment
- Cloud database (AWS RDS with pgvector)
- Redis cluster for scalability
- Elasticsearch cluster
- Cloud storage (AWS S3)
- Load balancer and CDN
- Monitoring and logging

## Security Considerations

### Authentication & Authorization
- JWT token-based authentication
- Role-based access control
- API rate limiting
- Input validation and sanitization
- **Multi-tenant isolation**

### Data Protection
- File encryption at rest
- Secure file upload validation
- PII data handling compliance
- Audit logging
- **Row-level security**

### Infrastructure Security
- HTTPS enforcement
- CORS configuration
- Environment variable security
- Container security best practices
- **WebSocket authentication**

## Performance Optimization

### Backend Optimization
- Database query optimization
- Caching strategies
- Background task processing
- API response optimization
- **Vector similarity search**
- **Hybrid search optimization**

### Frontend Optimization
- Code splitting and lazy loading
- Image optimization
- Bundle size optimization
- Caching strategies
- **Real-time updates optimization**

## Monitoring and Logging

### Application Monitoring
- Health check endpoints
- Performance metrics
- Error tracking
- User analytics
- **WebSocket connection monitoring**

### Infrastructure Monitoring
- Server resource monitoring
- Database performance
- Queue monitoring
- File storage monitoring
- **RAG pipeline performance**

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
- **80/20 development approach**

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

## AI/ML Framework Architecture

### Primary Framework: LangGraph
- **Purpose**: Main orchestration framework for RAG pipeline
- **Role**: Manages 5-step workflow
- **Location**: `app/services/advanced_rag.py`

### Supporting Framework: LangChain
- **Purpose**: RAG components and utilities
- **Role**: Provides retrievers, embeddings, document processing
- **Usage**: Used within LangGraph nodes

### Multi-Agent Framework: CrewAI
- **Purpose**: Complex document processing workflows
- **Role**: Coordinates specialized agents
- **Status**: Framework ready, agents need implementation

### RAG Pattern
- **Purpose**: Core AI pattern for generating answers with citations
- **Implementation**: LangGraph + LangChain + custom components

This repository structure is designed to support scalable development, maintainable code, and efficient collaboration between team members and AI assistants, with comprehensive real-time communication, advanced AI/ML capabilities, and enterprise-grade security.

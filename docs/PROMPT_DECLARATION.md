# Prompt Declaration

## Project Context

**DocuMind™** - A comprehensive AI-powered platform that transforms unstructured documents into searchable knowledge bases with real-time communication, advanced RAG pipeline, and multi-service integrations. The system automates document processing workflows, extracts data using OCR and NLP, provides human-in-the-loop validation capabilities, and delivers evidence-linked answers with verifiable citations.

## Technology Stack

### Backend
- **Framework**: FastAPI with async/await patterns
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0 ORM and pgvector extension
- **Task Queue**: Celery with Redis 7+ broker
- **Authentication**: JWT tokens with role-based access control
- **File Storage**: Local filesystem (dev) / AWS S3 (prod)
- **AI/ML**: OCR (Tesseract), NLP (spaCy), **LangChain for RAG components**, **LangGraph for orchestration**, **CrewAI for multi-agent workflows**
- **Search**: **Elasticsearch 8+ for hybrid search (BM25 + vector)**
- **Vector Database**: PostgreSQL with pgvector extension
- **Real-time Communication**: **WebSocket server with tenant isolation**
- **External Integrations**: **Source Connectors for Google Drive, SharePoint, Confluence, Slack, GitHub**
- **Monitoring**: Structured logging with structlog, Prometheus metrics

### Frontend
- **Framework**: Next.js 14+ with App Router and Server Components
- **Language**: TypeScript 5+ with strict mode enabled
- **Styling**: Tailwind CSS 3+ with custom design tokens
- **State Management**: Zustand for global state, React Context for auth/theme
- **Data Fetching**: TanStack Query (React Query) for server state
- **Forms**: React Hook Form with Zod validation
- **UI Components**: Custom component library with Radix UI primitives
- **Real-time**: **Socket.IO client for WebSocket connections with automatic reconnection**
- **Testing**: Jest, React Testing Library, Playwright for E2E

### Infrastructure
- **Containerization**: Docker and Docker Compose
- **CI/CD**: GitHub Actions with automated testing
- **Monitoring**: Structured logging with structlog
- **Security**: CORS, rate limiting, input validation, **multi-tenant isolation**

## Frontend/Backend Boundaries

### Frontend Responsibilities
- User interface and user experience
- Form validation and error handling
- **Real-time updates via WebSocket with event handling**
- File upload with progress tracking
- Search interface and result display
- **Chat interface with streaming responses**
- **Connector management and OAuth2 flows**
- Responsive design and accessibility

### Backend Responsibilities
- API endpoints and business logic
- Database operations and data validation
- File processing and storage
- Background task orchestration
- Authentication and authorization
- **AI/ML processing pipeline with LangGraph orchestration**
- **WebSocket server with connection management**
- **External service integrations via Source Connectors**

### Data Contracts
- All API responses use Pydantic schemas
- Frontend types mirror backend schemas
- **WebSocket events follow defined protocols with tenant isolation**
- File uploads use multipart/form-data
- Error responses follow standard format
- **Real-time streaming responses with citations**

## Real-time Infrastructure

### WebSocket Server (`app/core/websocket.py`)
- **Connection Management**: Tenant-isolated connections with JWT authentication
- **Event Routing**: Predefined event types for document processing, validation, chat, and sync
- **Broadcasting**: Utility functions for tenant-specific and system-wide notifications
- **Error Handling**: Automatic reconnection with exponential backoff
- **Integration**: Seamless integration with FastAPI router

### WebSocket Events
- **Document Processing**: Real-time progress updates and status changes
- **Validation Tasks**: Instant notifications for new validation tasks
- **Chat Responses**: Streaming responses with citations and confidence scores
- **Connector Sync**: Real-time sync progress and status updates
- **User Status**: Online/offline status and activity updates
- **System Notifications**: System-wide announcements and alerts

### Frontend WebSocket Integration
- **Provider Pattern**: WebSocket provider with React Context
- **Event Handlers**: Automatic state updates based on WebSocket events
- **Connection Management**: Automatic reconnection and error handling
- **Tenant Isolation**: Room-based message filtering

## Advanced RAG Pipeline

### LangGraph Orchestration (`app/services/advanced_rag.py`)
- **5-Step Workflow**: Retrieve → Rerank → Generate → Validate → Cite
- **Hybrid Retrieval**: Vector similarity + keyword search with fusion
- **Cross-Encoder Reranking**: Advanced reranking with domain-specific models
- **Reciprocal Rank Fusion**: Sophisticated result fusion algorithms
- **Factuality Verification**: Confidence scoring and validation
- **Citation Extraction**: Automatic span mapping and source verification

### RAG Components
- **Retrieval Methods**: Vector (pgvector), keyword (Elasticsearch), hybrid fusion
- **Reranking**: Cross-encoder models and lightweight LLM reranking
- **Generation**: LLM integration with context injection and citation formatting
- **Validation**: Confidence scoring and factuality verification
- **Analytics**: Performance metrics and user feedback tracking

### RAG Endpoints
- **Query Execution**: `/api/v1/rag/query` with advanced pipeline configuration
- **Configuration Management**: `/api/v1/rag/config` for pipeline settings
- **Analytics**: `/api/v1/rag/analytics` for performance insights

## Source Connectors Framework

### Connector Infrastructure (`app/services/connectors.py`)
- **Abstract Base Class**: Common interface for all external service connectors
- **Connector Manager**: Centralized registration and sync management
- **OAuth2 Integration**: Secure authentication flows for external services
- **Rate Limiting**: Intelligent rate limiting and retry logic
- **Real-time Updates**: WebSocket notifications for sync progress

### Supported Services
- **Google Drive**: Document synchronization with OAuth2
- **SharePoint**: Microsoft Graph API integration
- **Confluence**: Atlassian API with authentication
- **Slack**: Message and file synchronization
- **GitHub**: Repository and issue synchronization

### Connector Endpoints
- **Management**: `/api/v1/connectors` for connector listing and management
- **Authentication**: `/api/v1/connectors/{type}/auth/url` for OAuth2 flows
- **Connection**: `/api/v1/connectors/{type}/connect` for service setup
- **Sync**: `/api/v1/connectors/{id}/sync` for manual synchronization
- **Status**: `/api/v1/connectors/{id}/sync/{sync_id}/status` for progress tracking

## Multi-Agent Orchestration (CrewAI)

### Agent Framework
- **Specialized Agents**: Ingestion, Research, Synthesis, Compliance, Export
- **Coordinator**: CrewAI framework for complex workflow orchestration
- **Task Distribution**: Intelligent task assignment and result aggregation
- **Error Handling**: Circuit breakers and retry mechanisms
- **Integration**: Seamless integration with LangGraph nodes

### Agent Responsibilities
- **Ingestion Agent**: OCR, layout parsing, and metadata extraction
- **Research Agent**: Query planning and information gathering
- **Synthesis Agent**: Answer drafting and content generation
- **Compliance Agent**: Redaction, policy enforcement, and validation
- **Export Agent**: Report generation and data export

## UX Guidelines

### Design Principles
- **Modern and Clean**: Minimalist design with clear hierarchy
- **Accessible**: WCAG 2.1 AA compliance
- **Responsive**: Mobile-first design approach
- **Intuitive**: Clear navigation and user flows
- **Fast**: Optimized performance and loading states
- **Real-time**: Live updates and streaming responses

### Component States
- **Loading**: Skeleton screens and progress indicators
- **Error**: Clear error messages with recovery options
- **Empty**: Helpful empty states with call-to-action
- **Success**: Confirmation messages and next steps
- **Disabled**: Clear visual feedback for unavailable actions
- **Streaming**: Real-time content updates with progress indicators

### Interaction Patterns
- **Progressive Disclosure**: Show information as needed
- **Immediate Feedback**: Real-time validation and updates
- **Undo/Redo**: Allow users to reverse actions
- **Keyboard Navigation**: Full keyboard accessibility
- **Touch-Friendly**: Adequate touch targets for mobile
- **Real-time Collaboration**: Live updates and notifications

### Real-time Features
- **Streaming Responses**: Live chat responses with citations
- **Progress Tracking**: Real-time document processing updates
- **Sync Status**: Live connector synchronization status
- **Notifications**: Instant validation task assignments
- **User Presence**: Online/offline status indicators

### Design Tokens
```css
/* Colors */
--primary: #2563eb;
--secondary: #64748b;
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--background: #ffffff;
--surface: #f8fafc;
--text-primary: #1e293b;
--text-secondary: #64748b;

/* Typography */
--font-family: 'Inter', system-ui, sans-serif;
--font-size-xs: 0.75rem;
--font-size-sm: 0.875rem;
--font-size-base: 1rem;
--font-size-lg: 1.125rem;
--font-size-xl: 1.25rem;
--font-size-2xl: 1.5rem;

/* Spacing */
--spacing-xs: 0.25rem;
--spacing-sm: 0.5rem;
--spacing-md: 1rem;
--spacing-lg: 1.5rem;
--spacing-xl: 2rem;
--spacing-2xl: 3rem;

/* Animation */
--transition-fast: 150ms ease-in-out;
--transition-normal: 250ms ease-in-out;
--transition-slow: 350ms ease-in-out;
```

## Performance Requirements

### Response Times
- **API Endpoints**: < 200ms for standard operations
- **RAG Queries**: < 2s for complex queries with citations
- **File Upload**: < 5s for 50MB files
- **WebSocket Events**: < 100ms for real-time updates
- **Page Load**: < 1.5s for initial page load

### Scalability Targets
- **Concurrent Users**: 10,000+ simultaneous users
- **Document Processing**: 1M+ documents per month
- **RAG Queries**: 100,000+ queries per day
- **WebSocket Connections**: 5,000+ concurrent connections
- **File Storage**: Petabyte-scale storage capability

### Resource Optimization
- **Database**: Connection pooling, query optimization, indexing
- **Caching**: Redis for API responses, session data, and real-time state
- **CDN**: Static asset delivery and caching
- **Background Tasks**: Celery for long-running operations
- **Real-time**: Efficient WebSocket message broadcasting

## Security Requirements

### Authentication & Authorization
- **JWT Tokens**: Secure token handling with refresh mechanism
- **Multi-tenant Isolation**: Row-level security and tenant filtering
- **Role-based Access**: Admin, User, Validator, Viewer roles
- **API Rate Limiting**: Redis-based sliding window rate limiting
- **WebSocket Authentication**: JWT token validation for real-time connections

### Data Protection
- **Encryption**: AES-256 at rest, TLS 1.2+ in transit
- **File Upload Security**: MIME type validation + virus scan
- **PII Handling**: Automatic detection and redaction
- **Audit Logging**: Comprehensive audit trail with correlation IDs
- **Compliance**: SOC2-ready controls, GDPR compliance

### External Integrations
- **OAuth2 Security**: Secure OAuth2 flows for external connectors
- **API Key Management**: Secure storage and rotation of API keys
- **Rate Limiting**: Intelligent rate limiting for external APIs
- **Error Handling**: Graceful degradation for external service failures

## Testing Strategy

### Test Coverage Requirements
- **Frontend**: > 80% code coverage
- **Backend**: > 85% code coverage
- **Critical Paths**: 100% test coverage
- **Real-time Features**: Comprehensive WebSocket testing
- **RAG Pipeline**: End-to-end RAG workflow testing

### Testing Types
- **Unit Tests**: Individual component and function testing
- **Integration Tests**: API endpoint and database integration
- **E2E Tests**: Complete user workflow testing
- **Performance Tests**: Load testing and stress testing
- **Security Tests**: Authentication and authorization testing
- **Real-time Tests**: WebSocket connection and event testing

### Test Data Management
- **Fixtures**: Comprehensive test data for all scenarios
- **Mocking**: External service mocking for reliable tests
- **Isolation**: Test isolation with database transactions
- **Coverage**: Automated coverage reporting and monitoring

## Development Workflow

### Code Quality
- **Linting**: ESLint for frontend, Black for backend
- **Formatting**: Prettier for frontend, Black for backend
- **Type Safety**: TypeScript strict mode, mypy for Python
- **Documentation**: Comprehensive API documentation
- **Code Review**: Mandatory code review for all changes

### CI/CD Pipeline
- **Automated Testing**: Unit, integration, and E2E tests
- **Code Quality**: Linting, formatting, and type checking
- **Security Scanning**: Vulnerability scanning and dependency checks
- **Performance Testing**: Automated performance regression testing
- **Deployment**: Automated deployment with rollback capabilities

### Monitoring & Observability
- **Application Monitoring**: Health checks, performance metrics, error tracking
- **Infrastructure Monitoring**: Server resources, database performance, queue monitoring
- **Real-time Monitoring**: WebSocket connection monitoring and event tracking
- **User Analytics**: Usage patterns, feature adoption, and performance insights
- **Alerting**: Proactive alerting for critical issues and performance degradation

## Automation Gates & CI/CD Requirements

#### Required CI/CD Checks
```yaml
# .github/workflows/ci.yml
- name: Lint Check
  run: pnpm run lint

- name: Type Check
  run: pnpm run typecheck

- name: Test Coverage
  run: pnpm run test:coverage
  # Must maintain >80% coverage

- name: Build Check
  run: pnpm run build

- name: Security Scan
  run: npm audit --audit-level moderate

- name: Bundle Size Check
  run: pnpm run analyze-bundle
  # Must be <500KB gzipped
```

#### Performance Gates
- **Bundle Size**: < 500KB gzipped for main bundle
- **Test Coverage**: > 80% for frontend, > 85% for backend
- **Lighthouse Score**: > 90 for all metrics
- **Security**: No high/critical vulnerabilities
- **Type Safety**: 100% TypeScript strict mode compliance
- **Real-time Performance**: < 100ms WebSocket event latency

## Success Criteria

### Technical Metrics
- **Performance**: < 2s RAG query response time
- **Reliability**: 99.9% uptime with comprehensive monitoring
- **Security**: Zero security vulnerabilities in production
- **Scalability**: Support for 10,000+ concurrent users
- **Real-time**: < 100ms WebSocket event delivery

### User Experience Metrics
- **Usability**: Intuitive interface with clear navigation
- **Accessibility**: WCAG 2.1 AA compliance
- **Performance**: Fast loading times and responsive interactions
- **Real-time**: Seamless real-time updates and notifications
- **Integration**: Smooth external service connectivity

### Business Metrics
- **Adoption**: High user adoption and engagement
- **Efficiency**: Significant time savings in document processing
- **Accuracy**: High accuracy in document extraction and RAG responses
- **Compliance**: Full compliance with security and privacy requirements
- **Scalability**: Ability to handle enterprise-scale workloads

This comprehensive prompt declaration ensures consistent, high-quality development across all aspects of the DocuMind™ platform, from real-time communication to advanced AI/ML capabilities.

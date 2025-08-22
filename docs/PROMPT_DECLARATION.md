# Prompt Declaration

## Project Context

**Intelligent Document Processing and Knowledge Base** - A comprehensive AI-powered platform that transforms unstructured documents into searchable knowledge bases. The system automates document processing workflows, extracts data using OCR and NLP, and provides human-in-the-loop validation capabilities.

## Technology Stack

### Backend
- **Framework**: FastAPI with async/await patterns
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Task Queue**: Celery with Redis broker
- **Authentication**: JWT tokens with role-based access
- **File Storage**: Local filesystem (dev) / AWS S3 (prod)
- **AI/ML**: OCR, NLP, and machine learning for document processing

### Frontend
- **Framework**: Next.js 13+ with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Zustand for global state
- **Data Fetching**: React Query for server state
- **Forms**: React Hook Form with Zod validation

### Infrastructure
- **Containerization**: Docker and Docker Compose
- **CI/CD**: GitHub Actions with automated testing
- **Monitoring**: Structured logging with structlog
- **Security**: CORS, rate limiting, input validation

## Frontend/Backend Boundaries

### Frontend Responsibilities
- User interface and user experience
- Form validation and error handling
- Real-time updates via WebSocket
- File upload with progress tracking
- Search interface and result display
- Responsive design and accessibility

### Backend Responsibilities
- API endpoints and business logic
- Database operations and data validation
- File processing and storage
- Background task orchestration
- Authentication and authorization
- AI/ML processing pipeline

### Data Contracts
- All API responses use Pydantic schemas
- Frontend types mirror backend schemas
- WebSocket events follow defined protocols
- File uploads use multipart/form-data
- Error responses follow standard format

## UX Guidelines

### Design Principles
- **Modern and Clean**: Minimalist design with clear hierarchy
- **Accessible**: WCAG 2.1 AA compliance
- **Responsive**: Mobile-first design approach
- **Intuitive**: Clear navigation and user flows
- **Fast**: Optimized performance and loading states

### Component States
- **Loading**: Skeleton screens and progress indicators
- **Error**: Clear error messages with recovery options
- **Empty**: Helpful empty states with call-to-action
- **Success**: Confirmation messages and next steps
- **Disabled**: Clear visual feedback for unavailable actions

### Interaction Patterns
- **Progressive Disclosure**: Show information as needed
- **Immediate Feedback**: Real-time validation and updates
- **Undo/Redo**: Allow users to reverse actions
- **Keyboard Navigation**: Full keyboard accessibility
- **Touch-Friendly**: Adequate touch targets for mobile

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

/* Spacing */
--space-1: 0.25rem;
--space-2: 0.5rem;
--space-3: 0.75rem;
--space-4: 1rem;
--space-6: 1.5rem;
--space-8: 2rem;

/* Border Radius */
--radius-sm: 0.25rem;
--radius-md: 0.375rem;
--radius-lg: 0.5rem;
--radius-xl: 0.75rem;
```

## Performance Budgets

### Frontend Performance
- **Bundle Size**: < 500KB initial load
- **Time to Interactive**: < 3 seconds
- **Lighthouse Score**: > 90 for all metrics
- **Image Optimization**: WebP format with fallbacks
- **Code Splitting**: Route-based and component-based

### Backend Performance
- **API Response Time**: < 200ms for simple operations
- **File Upload**: < 30 seconds for 50MB files
- **Database Queries**: < 100ms for standard operations
- **Background Tasks**: Progress tracking with timeouts
- **Caching**: Redis for frequently accessed data

### Scalability Targets
- **Concurrent Users**: 1000+ simultaneous users
- **Document Processing**: 100+ documents per hour
- **Search Performance**: < 1 second for complex queries
- **File Storage**: Petabyte-scale storage capability

## Security Constraints

### Authentication & Authorization
- JWT tokens with 1-hour expiration
- Refresh tokens with 7-day expiration
- Role-based access control (user, admin, superuser)
- Session management with secure cookies
- Multi-factor authentication support

### Data Protection
- File encryption at rest (AES-256)
- Data encryption in transit (TLS 1.3)
- PII data handling compliance (GDPR, CCPA)
- Audit logging for all user actions
- Data retention and deletion policies

### Input Validation
- All inputs validated with Pydantic schemas
- File type and size restrictions
- SQL injection prevention with ORM
- XSS protection with content sanitization
- Rate limiting (100 requests/minute per user)

### API Security
- CORS configuration for specific origins
- API key authentication for external integrations
- Request signing for sensitive operations
- IP whitelisting for admin endpoints
- Security headers (HSTS, CSP, X-Frame-Options)

## Testing Expectations

### Frontend Testing
- **Unit Tests**: Jest for component testing
- **Integration Tests**: React Testing Library
- **E2E Tests**: Playwright for user workflows
- **Visual Regression**: Screenshot testing
- **Accessibility**: axe-core for a11y testing

### Backend Testing
- **Unit Tests**: pytest for function testing
- **Integration Tests**: FastAPI TestClient
- **Database Tests**: Test database with fixtures
- **API Tests**: OpenAPI specification validation
- **Performance Tests**: Load testing with locust

### Test Coverage Requirements
- **Frontend**: > 80% code coverage
- **Backend**: > 85% code coverage
- **Critical Paths**: 100% test coverage
- **API Endpoints**: All endpoints tested
- **Error Scenarios**: Comprehensive error testing

### Testing Strategy
- **Test-Driven Development**: Write tests first
- **Continuous Testing**: Automated on every commit
- **Test Data Management**: Fixtures and factories
- **Mocking Strategy**: External service mocking
- **Performance Testing**: Regular load testing

## Development Workflow

### Code Quality Standards
- **Linting**: ESLint (frontend) and flake8 (backend)
- **Formatting**: Prettier (frontend) and Black (backend)
- **Type Checking**: TypeScript strict mode
- **Documentation**: JSDoc and docstrings
- **Code Review**: Required for all changes

### Git Workflow
- **Branching**: Feature branches from main
- **Commits**: Conventional commit messages
- **Pull Requests**: Required with descriptions
- **Code Review**: At least one approval required
- **Merge Strategy**: Squash and merge

### Deployment Pipeline
- **Development**: Automatic deployment on main branch
- **Staging**: Manual deployment for testing
- **Production**: Manual deployment with approval
- **Rollback**: Automatic rollback on failure
- **Monitoring**: Health checks and alerting

## AI Collaboration Guidelines

### Code Generation Rules
- Follow established patterns and conventions
- Include comprehensive error handling
- Add appropriate logging and monitoring
- Write tests for new functionality
- Update documentation as needed

### Review Process
- Generated code must pass all tests
- Security review for sensitive operations
- Performance review for new features
- Accessibility review for UI components
- Documentation review for API changes

### Quality Assurance
- No hardcoded values or secrets
- Proper input validation and sanitization
- Error handling for all edge cases
- Performance considerations for all operations
- Security best practices implementation

## Success Criteria

### Functional Requirements
- Document upload and processing workflow
- Knowledge base search and retrieval
- Human-in-the-loop validation system
- Real-time processing status updates
- User authentication and authorization

### Non-Functional Requirements
- Sub-3-second page load times
- 99.9% uptime availability
- Secure data handling and storage
- Scalable architecture for growth
- Comprehensive audit logging

### User Experience Goals
- Intuitive and accessible interface
- Fast and responsive interactions
- Clear error messages and recovery
- Progressive disclosure of complexity
- Mobile-friendly design

### Technical Excellence
- Clean, maintainable codebase
- Comprehensive test coverage
- Secure and performant architecture
- Well-documented APIs and components
- Automated deployment and monitoring

This prompt declaration provides the foundation for consistent, high-quality development across the entire project stack.

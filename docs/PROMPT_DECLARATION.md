# Prompt Declaration

## Project Context

**Intelligent Document Processing and Knowledge Base** - A comprehensive AI-powered platform that transforms unstructured documents into searchable knowledge bases. The system automates document processing workflows, extracts data using OCR and NLP, and provides human-in-the-loop validation capabilities.

## Technology Stack

### Backend
- **Framework**: FastAPI with async/await patterns
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0 ORM
- **Task Queue**: Celery with Redis 7+ broker
- **Authentication**: JWT tokens with role-based access control
- **File Storage**: Local filesystem (dev) / AWS S3 (prod)
- **AI/ML**: OCR (Tesseract), NLP (spaCy), LangChain for RAG, LangGraph for orchestration
- **Search**: Elasticsearch 8+ for hybrid search (BM25 + vector)
- **Vector Database**: PostgreSQL with pgvector extension
- **Monitoring**: Structured logging with structlog, Prometheus metrics

### Frontend
- **Framework**: Next.js 14+ with App Router and Server Components
- **Language**: TypeScript 5+ with strict mode enabled
- **Styling**: Tailwind CSS 3+ with custom design tokens
- **State Management**: Zustand for global state, React Context for auth/theme
- **Data Fetching**: TanStack Query (React Query) for server state
- **Forms**: React Hook Form with Zod validation
- **UI Components**: Custom component library with Radix UI primitives
- **Real-time**: Socket.IO client for WebSocket connections
- **Testing**: Jest, React Testing Library, Playwright for E2E

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

### Security Implementation Table

| Security Aspect | Implementation | Location | Notes |
|----------------|----------------|----------|-------|
| **Authentication** | JWT tokens with refresh | `app/core/security.py` | 15min access, 7day refresh |
| **Authorization** | Role-based (admin, user, validator) | `app/models/user.py` | Granular permissions per endpoint |
| **Secrets Management** | Environment variables + KMS | `.env.example` | No hardcoded secrets in code |
| **Data Encryption** | AES-256 at rest, TLS 1.3 in transit | Database + API | Full encryption pipeline |
| **Input Validation** | Pydantic schemas + sanitization | `app/schemas/` | All inputs validated |
| **Rate Limiting** | Redis-based sliding window | `app/core/security.py` | 100 req/min per user |
| **Audit Logging** | Structured JSON logs | `app/core/logging.py` | All actions logged with user context |
| **CORS** | Configurable origins | `app/main.py` | Production: specific domains only |
| **File Upload** | MIME type validation + virus scan | `app/services/file_storage.py` | Whitelist + size limits |
| **SQL Injection** | SQLAlchemy ORM + parameterized queries | All database operations | No raw SQL |
| **XSS Prevention** | Content Security Policy + sanitization | Frontend + API responses | CSP headers enforced |
| **CSRF Protection** | SameSite cookies + CSRF tokens | Authentication system | Double submit pattern |

### Compliance Requirements
- **GDPR**: Data anonymization, right to deletion, consent management
- **SOC2**: Audit trails, access controls, data protection
- **HIPAA**: PHI handling, encryption, access logging
- **ISO 27001**: Information security management system

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

## Response Schema

### Claude Response Format
All Claude responses must follow this exact format:

```diff
// File: path/to/file.ts
- // Old code or comment
+ // New code or comment
```

### Response Rules
- **NO PROSE**: Do not include explanatory text outside of code blocks
- **DIFF ONLY**: Use diff format for all code changes
- **SINGLE FILE**: One file per response unless explicitly requested
- **CONTEXT**: Include 3-5 lines of context before and after changes
- **COMMENTS**: Use inline comments for complex logic explanations

### Example Response
**User Request**: "Add error handling to the document upload function"

```diff
// File: frontend/components/features/document-upload.tsx
  const handleFileUpload = async (file: File) => {
+   try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await apiClient.uploadDocument(formData);
      
      if (response.success) {
        setUploadStatus('success');
        onUploadComplete(response.data);
      }
+   } catch (error) {
+     console.error('Upload failed:', error);
+     setUploadStatus('error');
+     setErrorMessage(error.message || 'Upload failed. Please try again.');
+   }
  };
```

## Performance Budgets

### Frontend Performance
- **Bundle Size**: < 500KB gzipped for main bundle
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

### Backend Performance
- **API Response Time**: < 500ms (P95)
- **Database Query Time**: < 100ms (P95)
- **File Upload Time**: < 30s for 100MB files
- **Processing Queue**: < 5min for standard documents

### CI/CD Performance Gates
```yaml
# .github/workflows/performance.yml
- name: Performance Check
  run: |
    npm run build
    npm run analyze-bundle
    npm run lighthouse-ci
```

## Example Prompt and Response

### Example User Prompt
"Add a new API endpoint for bulk document deletion with proper validation and error handling"

### Ideal Claude Response
```diff
// File: app/api/v1/endpoints/documents.py
  from typing import List
  from fastapi import APIRouter, Depends, HTTPException
  from app.schemas.document import DocumentDeleteRequest
  from app.services.document import DocumentService
  
  router = APIRouter()
  
+ @router.delete("/bulk")
+ async def delete_documents_bulk(
+     request: DocumentDeleteRequest,
+     current_user = Depends(get_current_user),
+     document_service: DocumentService = Depends()
+ ):
+     """
+     Delete multiple documents with validation and error handling.
+     """
+     try:
+         # Validate user permissions
+         if not current_user.can_delete_documents():
+             raise HTTPException(status_code=403, detail="Insufficient permissions")
+         
+         # Validate document IDs
+         if not request.document_ids or len(request.document_ids) > 100:
+             raise HTTPException(status_code=400, detail="Invalid document count")
+         
+         # Delete documents
+         deleted_count = await document_service.delete_documents_bulk(
+             document_ids=request.document_ids,
+             user_id=current_user.id
+         )
+         
+         return {"deleted_count": deleted_count, "message": "Documents deleted successfully"}
+         
+     except HTTPException:
+         raise
+     except Exception as e:
+         logger.error(f"Bulk deletion failed: {e}")
+         raise HTTPException(status_code=500, detail="Internal server error")
```

```diff
// File: app/schemas/document.py
+ class DocumentDeleteRequest(BaseModel):
+     document_ids: List[str]
+     
+     @validator('document_ids')
+     def validate_document_ids(cls, v):
+         if not v:
+             raise ValueError('At least one document ID is required')
+         if len(v) > 100:
+             raise ValueError('Maximum 100 documents can be deleted at once')
+         return v
```

This prompt declaration provides the foundation for consistent, high-quality development across the entire project stack.

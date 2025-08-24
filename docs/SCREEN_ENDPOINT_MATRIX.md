# Screen ↔ Endpoint ↔ DTO Matrix

This document maps frontend screens to backend endpoints and their corresponding DTOs to ensure proper alignment between frontend and backend, including real-time WebSocket communication, Advanced RAG pipeline, and Source Connectors.

## Authentication Flow

### Login Screen (`/login`)
- **Endpoint**: `POST /api/v1/auth/login`
- **Request DTO**: `LoginRequest`
- **Response DTO**: `TokenResponse`
- **Frontend State**: `AuthState` (Zustand)

### Register Screen (`/register`)
- **Endpoint**: `POST /api/v1/auth/register`
- **Request DTO**: `UserCreate`
- **Response DTO**: `UserResponse`
- **Frontend State**: `AuthState` (Zustand)

## Dashboard Flow

### Main Dashboard (`/dashboard`)
- **Endpoint**: `GET /api/v1/dashboard/stats`
- **Response DTO**: `DashboardStats`
- **Frontend State**: `DashboardState` (TanStack Query)

### Document Upload (`/dashboard/ingest`)
- **Endpoint**: `POST /api/v1/documents/upload`
- **Request DTO**: `DocumentUpload`
- **Response DTO**: `DocumentResponse`
- **Frontend State**: `UploadState` (Zustand)
- **Real-time**: WebSocket updates for upload progress

### Document Processing (`/dashboard/processing`)
- **Endpoint**: `GET /api/v1/processing/jobs`
- **Response DTO**: `ProcessingJobList`
- **Frontend State**: `ProcessingState` (TanStack Query)
- **Real-time**: WebSocket updates for processing status

## Knowledge Base Flow

### Ask Interface (`/dashboard/ask`)
- **Endpoint**: `POST /api/v1/rag/query`
- **Request DTO**: `RAGQuery`
- **Response DTO**: `RAGResponse`
- **Frontend State**: `ChatState` (Zustand)
- **Real-time**: WebSocket streaming for chat responses

### Search Interface (`/dashboard/search`)
- **Endpoint**: `GET /api/v1/knowledge/search`
- **Request DTO**: `SearchQuery`
- **Response DTO**: `SearchResults`
- **Frontend State**: `SearchState` (TanStack Query)

### RAG Configuration (`/dashboard/rag-config`)
- **Endpoint**: `GET /api/v1/rag/config`
- **Response DTO**: `RAGConfig`
- **Frontend State**: `RAGConfigState` (TanStack Query)

- **Endpoint**: `PUT /api/v1/rag/config`
- **Request DTO**: `RAGConfigUpdate`
- **Response DTO**: `RAGConfig`
- **Frontend State**: `RAGConfigState` (TanStack Query)

### RAG Analytics (`/dashboard/rag-analytics`)
- **Endpoint**: `GET /api/v1/rag/analytics`
- **Response DTO**: `RAGAnalytics`
- **Frontend State**: `RAGAnalyticsState` (TanStack Query)

## Source Connectors Flow

### Connector Management (`/dashboard/connectors`)
- **Endpoint**: `GET /api/v1/connectors`
- **Response DTO**: `ConnectorList`
- **Frontend State**: `ConnectorState` (TanStack Query)

### Connector Setup (`/dashboard/connectors/[type]/setup`)
- **Endpoint**: `GET /api/v1/connectors/{type}/auth/url`
- **Response DTO**: `OAuthURL`
- **Frontend State**: `ConnectorSetupState` (Zustand)

- **Endpoint**: `POST /api/v1/connectors/{type}/connect`
- **Request DTO**: `ConnectorSetup`
- **Response DTO**: `ConnectorResponse`
- **Frontend State**: `ConnectorSetupState` (Zustand)

### Connector Sync (`/dashboard/connectors/[id]/sync`)
- **Endpoint**: `GET /api/v1/connectors/{id}/sync`
- **Response DTO**: `SyncResponse`
- **Frontend State**: `SyncState` (TanStack Query)
- **Real-time**: WebSocket updates for sync progress

- **Endpoint**: `GET /api/v1/connectors/{id}/sync/{sync_id}/status`
- **Response DTO**: `SyncStatus`
- **Frontend State**: `SyncState` (TanStack Query)
- **Real-time**: WebSocket updates for sync status

## Validation Flow

### Validation Queue (`/dashboard/validation`)
- **Endpoint**: `GET /api/v1/validation/queue`
- **Response DTO**: `ValidationQueue`
- **Frontend State**: `ValidationState` (TanStack Query)
- **Real-time**: WebSocket notifications for new tasks

### Validation Task (`/dashboard/validation/[id]`)
- **Endpoint**: `GET /api/v1/validation/tasks/{id}`
- **Response DTO**: `ValidationTask`
- **Frontend State**: `ValidationTaskState` (TanStack Query)

- **Endpoint**: `POST /api/v1/validation/tasks/{id}/approve`
- **Request DTO**: `ValidationApproval`
- **Response DTO**: `ValidationResponse`
- **Frontend State**: `ValidationTaskState` (TanStack Query)

- **Endpoint**: `POST /api/v1/validation/tasks/{id}/reject`
- **Request DTO**: `ValidationRejection`
- **Response DTO**: `ValidationResponse`
- **Frontend State**: `ValidationTaskState` (TanStack Query)

## Admin Flow

### Admin Dashboard (`/dashboard/admin`)
- **Endpoint**: `GET /api/v1/admin/stats`
- **Response DTO**: `AdminStats`
- **Frontend State**: `AdminState` (TanStack Query)

### User Management (`/dashboard/admin/users`)
- **Endpoint**: `GET /api/v1/admin/users`
- **Response DTO**: `UserList`
- **Frontend State**: `UserManagementState` (TanStack Query)

## Document Management Flow

### Document List (`/dashboard/documents`)
- **Endpoint**: `GET /api/v1/documents`
- **Response DTO**: `DocumentList`
- **Frontend State**: `DocumentState` (TanStack Query)

### Document Detail (`/dashboard/documents/[id]`)
- **Endpoint**: `GET /api/v1/documents/{id}`
- **Response DTO**: `DocumentDetail`
- **Frontend State**: `DocumentDetailState` (TanStack Query)

## Real-time Updates

### WebSocket Connections
- **Endpoint**: `WS /ws`
- **Authentication**: JWT token in query parameter
- **Events**:
  - `document_processing_update` - Document processing progress
  - `validation_task_created` - New validation tasks
  - `chat_response` - Streaming chat responses
  - `chat_response_complete` - Complete chat responses with citations
  - `connector_sync_update` - Connector sync progress
  - `user_status_update` - User status changes
  - `system_notification` - System-wide notifications

### WebSocket Event Handlers
- **Frontend State**: `WebSocketState` (Zustand)
- **Event Processing**: Real-time state updates
- **Error Handling**: Automatic reconnection with exponential backoff
- **Tenant Isolation**: Room-based message routing

## Health Monitoring

### System Health (`/dashboard/health`)
- **Endpoint**: `GET /health`
- **Response DTO**: `HealthStatus`
- **Frontend State**: `HealthState` (TanStack Query)
- **Real-time**: Periodic health checks

## Error Handling

### API Error Responses
- **Status Codes**: 400, 401, 403, 404, 422, 500, 503
- **Error DTO**: `ErrorResponse`
- **Frontend Handling**: Global error boundary + toast notifications
- **WebSocket Errors**: `WEBSOCKET_ERROR`, `RAG_PIPELINE_ERROR`, `CONNECTOR_ERROR`

## Data Flow Patterns

### Optimistic Updates
- Document upload progress
- Validation task completion
- Chat message sending
- Connector sync initiation

### Background Sync
- Processing job status
- Validation queue updates
- Real-time notifications
- Connector sync status

### Caching Strategy
- **TanStack Query**: API responses with 5-minute TTL
- **Zustand**: User preferences, form state, WebSocket state
- **Local Storage**: Authentication tokens, theme preferences
- **Session Storage**: Temporary form data, upload progress

## Type Safety

### Shared Types
- All DTOs defined in `packages/types`
- Frontend and backend use same type definitions
- Runtime validation with Zod schemas
- WebSocket event types shared across platforms

### API Contracts
- OpenAPI specification in `docs/openapi.yaml`
- Auto-generated TypeScript types
- Contract testing with example requests/responses
- WebSocket event schemas for real-time communication

## Real-time Features

### Streaming Responses
- **Chat Interface**: Real-time streaming with citations
- **Document Processing**: Live progress updates
- **Connector Sync**: Real-time sync status
- **Validation Queue**: Instant task notifications

### WebSocket State Management
- **Connection Status**: Connected, connecting, disconnected, error
- **Event Queuing**: Offline event queuing and replay
- **Authentication**: JWT token refresh handling
- **Tenant Isolation**: Room-based message filtering

## Performance Optimization

### Frontend Optimization
- **Code Splitting**: Route-based and component-based splitting
- **Lazy Loading**: Images, components, and routes
- **Caching**: Aggressive caching for static assets
- **Real-time Optimization**: Efficient WebSocket event processing

### Backend Optimization
- **Database**: Query optimization and indexing
- **Caching**: Redis for frequently accessed data
- **Background Tasks**: Celery for long-running operations
- **Real-time**: Efficient WebSocket message broadcasting

## Security Considerations

### Authentication & Authorization
- **JWT Tokens**: Secure token handling with refresh
- **Role-based Access**: Admin, User, Validator, Viewer roles
- **API Rate Limiting**: Redis-based sliding window
- **WebSocket Authentication**: JWT token validation for WebSocket connections

### Data Protection
- **Multi-tenant Isolation**: Row-level security and tenant filtering
- **File Upload Security**: MIME type validation and virus scanning
- **PII Handling**: Automatic detection and redaction
- **Audit Logging**: Comprehensive audit trail

### Real-time Security
- **WebSocket Authentication**: JWT token validation
- **Tenant Isolation**: Room-based message routing
- **Rate Limiting**: WebSocket connection limits
- **Input Validation**: All WebSocket messages validated

# API Specification

## Overview
This document outlines the API endpoints, data models, and integration patterns for the Intelligent Document Processing and Knowledge Base system, including real-time WebSocket communication, Advanced RAG pipeline, and Source Connectors.

## Base URL
- Development: `http://localhost:8000`
- Production: `https://api.yourdomain.com`

## Authentication
All API endpoints require authentication using JWT tokens.

### Authentication Flow
1. **Login**: `POST /api/v1/auth/login`
2. **Register**: `POST /api/v1/auth/register`
3. **Refresh Token**: `POST /api/v1/auth/refresh`

### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

## Core Endpoints

### Authentication Endpoints

#### POST /api/v1/auth/login
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user"
  }
}
```

#### POST /api/v1/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "password123",
  "full_name": "Jane Smith"
}
```

**Response:**
```json
{
  "id": 2,
  "email": "newuser@example.com",
  "full_name": "Jane Smith",
  "role": "user",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Document Management Endpoints

#### POST /api/v1/documents/upload
Upload a new document for processing.

**Request Body (multipart/form-data):**
```
file: <document_file>
metadata: {
  "title": "Sample Document",
  "description": "Optional description",
  "category": "invoice"
}
```

**Response:**
```json
{
  "id": 123,
  "filename": "sample_document.pdf",
  "title": "Sample Document",
  "status": "uploaded",
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processing_status": "pending"
}
```

#### GET /api/v1/documents
Retrieve list of documents with pagination and filtering.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20)
- `status`: Filter by status (uploaded, processing, completed, failed)
- `category`: Filter by document category
- `search`: Search in title and content

**Response:**
```json
{
  "items": [
    {
      "id": 123,
      "filename": "sample_document.pdf",
      "title": "Sample Document",
      "status": "completed",
      "category": "invoice",
      "uploaded_at": "2024-01-15T10:30:00Z",
      "processed_at": "2024-01-15T10:35:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 20,
  "pages": 3
}
```

#### GET /api/v1/documents/{document_id}
Retrieve specific document details and extracted data.

**Response:**
```json
{
  "id": 123,
  "filename": "sample_document.pdf",
  "title": "Sample Document",
  "status": "completed",
  "category": "invoice",
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed_at": "2024-01-15T10:35:00Z",
  "extracted_data": {
    "invoice_number": "INV-2024-001",
    "amount": 1500.00,
    "vendor": "ABC Company",
    "date": "2024-01-10",
    "line_items": [
      {
        "description": "Web Development Services",
        "quantity": 1,
        "unit_price": 1500.00,
        "total": 1500.00
      }
    ]
  },
  "confidence_score": 0.95
}
```

### Knowledge Base Endpoints

#### GET /api/v1/knowledge-base/search
Search the knowledge base using natural language queries.

**Query Parameters:**
- `q`: Search query
- `filters`: JSON object with filters
- `limit`: Maximum results (default: 20)

**Response:**
```json
{
  "results": [
    {
      "document_id": 123,
      "title": "Sample Document",
      "snippet": "Invoice for web development services...",
      "relevance_score": 0.95,
      "extracted_data": {
        "invoice_number": "INV-2024-001",
        "amount": 1500.00
      }
    }
  ],
  "total_results": 15,
  "query": "web development invoice"
}
```

#### GET /api/v1/knowledge-base/analytics
Get analytics and insights from the knowledge base.

**Response:**
```json
{
  "total_documents": 1250,
  "documents_by_category": {
    "invoice": 450,
    "contract": 300,
    "receipt": 200,
    "other": 300
  },
  "processing_stats": {
    "completed": 1200,
    "failed": 25,
    "pending": 25
  },
  "extraction_accuracy": 0.94
}
```

### Processing Queue Endpoints

#### GET /api/v1/processing/queue
Get current processing queue status.

**Response:**
```json
{
  "pending": 5,
  "processing": 2,
  "completed_today": 45,
  "failed_today": 3,
  "queue_items": [
    {
      "id": 456,
      "document_id": 123,
      "status": "processing",
      "started_at": "2024-01-15T10:30:00Z",
      "estimated_completion": "2024-01-15T10:32:00Z"
    }
  ]
}
```

### Validation Endpoints

#### GET /api/v1/validation/tasks
Get validation tasks requiring human review.

**Response:**
```json
{
  "tasks": [
    {
      "id": 789,
      "document_id": 123,
      "field_name": "amount",
      "extracted_value": "1500.00",
      "confidence_score": 0.75,
      "validation_type": "amount_verification",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total_pending": 15
}
```

#### POST /api/v1/validation/tasks/{task_id}/approve
Approve a validation task.

**Request Body:**
```json
{
  "approved_value": "1500.00",
  "notes": "Amount verified against original document"
}
```

#### POST /api/v1/validation/tasks/{task_id}/reject
Reject a validation task and provide corrected value.

**Request Body:**
```json
{
  "corrected_value": "1500.50",
  "reason": "Typo in original extraction"
}
```

## Advanced RAG Pipeline Endpoints

### RAG Query Endpoint

#### POST /api/v1/rag/query
Execute advanced RAG pipeline with hybrid retrieval and reranking.

**Request Body:**
```json
{
  "query": "What are the payment terms for web development services?",
  "filters": {
    "document_types": ["invoice", "contract"],
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    }
  },
  "pipeline_config": {
    "retrieval_method": "hybrid",
    "reranker_type": "cross_encoder",
    "fusion_method": "reciprocal_rank",
    "max_results": 10
  }
}
```

**Response:**
```json
{
  "answer": "Based on the analyzed documents, the payment terms for web development services are 50% upfront and 50% upon completion. This is consistent across multiple contracts and invoices.",
  "confidence_score": 0.92,
  "citations": [
    {
      "document_id": 123,
      "document_title": "Web Development Contract",
      "span": "Payment terms: 50% upfront, 50% upon completion",
      "page": 3,
      "relevance_score": 0.95
    },
    {
      "document_id": 456,
      "document_title": "Invoice INV-2024-001",
      "span": "Payment schedule: 50% deposit received",
      "page": 1,
      "relevance_score": 0.88
    }
  ],
  "retrieval_stats": {
    "total_documents_retrieved": 15,
    "reranked_documents": 10,
    "processing_time_ms": 750
  }
}
```

### RAG Pipeline Configuration

#### GET /api/v1/rag/config
Get current RAG pipeline configuration.

**Response:**
```json
{
  "embedding_model": "text-embedding-3-large",
  "reranker_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
  "fusion_method": "reciprocal_rank",
  "max_chunk_size": 1000,
  "chunk_overlap": 200,
  "citation_threshold": 0.85
}
```

#### PUT /api/v1/rag/config
Update RAG pipeline configuration.

**Request Body:**
```json
{
  "embedding_model": "text-embedding-3-large",
  "reranker_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
  "fusion_method": "weighted_sum",
  "max_chunk_size": 1000,
  "chunk_overlap": 200,
  "citation_threshold": 0.85
}
```

### RAG Analytics

#### GET /api/v1/rag/analytics
Get RAG pipeline performance analytics.

**Response:**
```json
{
  "query_stats": {
    "total_queries": 1250,
    "average_response_time_ms": 750,
    "success_rate": 0.98
  },
  "retrieval_stats": {
    "average_documents_retrieved": 12.5,
    "average_relevance_score": 0.87,
    "reranking_improvement": 0.15
  },
  "citation_stats": {
    "average_citations_per_answer": 2.3,
    "citation_accuracy": 0.94,
    "user_feedback_score": 4.2
  }
}
```

## Source Connectors Endpoints

### Connector Management

#### GET /api/v1/connectors
List all configured source connectors.

**Response:**
```json
{
  "connectors": [
    {
      "id": "google_drive",
      "name": "Google Drive",
      "type": "google_drive",
      "status": "connected",
      "last_sync": "2024-01-15T10:30:00Z",
      "documents_synced": 45
    },
    {
      "id": "sharepoint",
      "name": "SharePoint",
      "type": "sharepoint",
      "status": "disconnected",
      "last_sync": null,
      "documents_synced": 0
    }
  ]
}
```

#### POST /api/v1/connectors/{connector_type}/connect
Connect to a source connector.

**Request Body:**
```json
{
  "name": "My Google Drive",
  "credentials": {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret"
  },
  "sync_config": {
    "folders": ["/Documents", "/Invoices"],
    "file_types": ["pdf", "docx"],
    "sync_frequency": "hourly"
  }
}
```

#### GET /api/v1/connectors/{connector_id}/sync
Trigger manual sync for a connector.

**Response:**
```json
{
  "sync_id": "sync_123",
  "status": "started",
  "estimated_completion": "2024-01-15T11:30:00Z"
}
```

#### GET /api/v1/connectors/{connector_id}/sync/{sync_id}/status
Get sync status.

**Response:**
```json
{
  "sync_id": "sync_123",
  "status": "completed",
  "documents_processed": 15,
  "documents_added": 8,
  "documents_updated": 5,
  "documents_deleted": 2,
  "errors": []
}
```

### Connector Authentication

#### GET /api/v1/connectors/{connector_type}/auth/url
Get OAuth2 authorization URL.

**Response:**
```json
{
  "auth_url": "https://accounts.google.com/oauth2/authorize?...",
  "state": "random_state_string"
}
```

#### POST /api/v1/connectors/{connector_type}/auth/callback
Handle OAuth2 callback.

**Request Body:**
```json
{
  "code": "authorization_code",
  "state": "random_state_string"
}
```

## WebSocket Endpoints

### WebSocket Connection
**Endpoint**: `ws://localhost:8000/ws`

**Authentication**: JWT token in query parameter or header

**Connection URL**: `ws://localhost:8000/ws?token=<jwt_token>`

### WebSocket Events

#### Client to Server Events

**Join Room**
```json
{
  "event": "join_room",
  "data": {
    "room": "user_123",
    "tenant_id": "tenant_456"
  }
}
```

**Subscribe to Document Updates**
```json
{
  "event": "subscribe_document",
  "data": {
    "document_id": 123
  }
}
```

**Chat Message**
```json
{
  "event": "chat_message",
  "data": {
    "message": "What are the payment terms?",
    "session_id": "session_789"
  }
}
```

#### Server to Client Events

**Document Processing Update**
```json
{
  "event": "document_processing_update",
  "data": {
    "document_id": 123,
    "status": "processing",
    "progress": 75,
    "message": "Extracting text from page 3 of 4",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**Validation Task Created**
```json
{
  "event": "validation_task_created",
  "data": {
    "task_id": 789,
    "document_id": 123,
    "field_name": "amount",
    "priority": "high",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**Chat Response (Streaming)**
```json
{
  "event": "chat_response",
  "data": {
    "session_id": "session_789",
    "message_id": "msg_456",
    "content": "Based on the analyzed documents...",
    "is_complete": false,
    "citations": [],
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**Chat Response Complete**
```json
{
  "event": "chat_response_complete",
  "data": {
    "session_id": "session_789",
    "message_id": "msg_456",
    "citations": [
      {
        "document_id": 123,
        "span": "Payment terms: 50% upfront",
        "relevance_score": 0.95
      }
    ],
    "confidence_score": 0.92,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**Connector Sync Update**
```json
{
  "event": "connector_sync_update",
  "data": {
    "connector_id": "google_drive",
    "sync_id": "sync_123",
    "status": "processing",
    "progress": 60,
    "documents_processed": 9,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Health Check Endpoints

### GET /health
Comprehensive health check for all services.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1705312200.123,
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "elasticsearch": "healthy"
  }
}
```

## Data Models

### User Model
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "user",
  "tenant_id": "tenant_456",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Document Model
```json
{
  "id": 123,
  "filename": "sample_document.pdf",
  "title": "Sample Document",
  "description": "Optional description",
  "category": "invoice",
  "status": "completed",
  "file_size": 1024000,
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed_at": "2024-01-15T10:35:00Z",
  "user_id": 1,
  "tenant_id": "tenant_456"
}
```

### Processing Queue Model
```json
{
  "id": 456,
  "document_id": 123,
  "status": "processing",
  "priority": "normal",
  "started_at": "2024-01-15T10:30:00Z",
  "completed_at": null,
  "error_message": null
}
```

### Validation Task Model
```json
{
  "id": 789,
  "document_id": 123,
  "field_name": "amount",
  "extracted_value": "1500.00",
  "confidence_score": 0.75,
  "validation_type": "amount_verification",
  "status": "pending",
  "assigned_to": null,
  "created_at": "2024-01-15T10:30:00Z",
  "resolved_at": null
}
```

### RAG Query Model
```json
{
  "id": "query_123",
  "query": "What are the payment terms?",
  "filters": {
    "document_types": ["invoice", "contract"]
  },
  "pipeline_config": {
    "retrieval_method": "hybrid",
    "reranker_type": "cross_encoder",
    "fusion_method": "reciprocal_rank"
  },
  "result": {
    "answer": "Payment terms are 50% upfront...",
    "confidence_score": 0.92,
    "citations": []
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Connector Model
```json
{
  "id": "google_drive",
  "name": "My Google Drive",
  "type": "google_drive",
  "status": "connected",
  "credentials": {
    "access_token": "encrypted_token",
    "refresh_token": "encrypted_refresh_token"
  },
  "sync_config": {
    "folders": ["/Documents"],
    "file_types": ["pdf", "docx"],
    "sync_frequency": "hourly"
  },
  "last_sync": "2024-01-15T10:30:00Z",
  "documents_synced": 45
}
```

## Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

### Common Error Codes
- `AUTHENTICATION_ERROR`: Invalid or expired token
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `VALIDATION_ERROR`: Invalid input data
- `NOT_FOUND`: Resource not found
- `PROCESSING_ERROR`: Document processing failed
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_SERVER_ERROR`: Server error
- `WEBSOCKET_ERROR`: WebSocket connection error
- `RAG_PIPELINE_ERROR`: RAG pipeline processing error
- `CONNECTOR_ERROR`: Source connector error

## Rate Limiting
- Authentication endpoints: 5 requests per minute
- Document upload: 10 requests per minute
- Search endpoints: 60 requests per minute
- RAG endpoints: 30 requests per minute
- WebSocket connections: 100 per minute
- Other endpoints: 100 requests per minute

## Integration Examples

### Python Client Example
```python
import requests
import websockets
import json

class DocumentAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def upload_document(self, file_path, metadata):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'metadata': json.dumps(metadata)}
            response = requests.post(
                f"{self.base_url}/api/v1/documents/upload",
                files=files,
                data=data,
                headers=self.headers
            )
        return response.json()
    
    def rag_query(self, query, filters=None, pipeline_config=None):
        data = {"query": query}
        if filters:
            data["filters"] = filters
        if pipeline_config:
            data["pipeline_config"] = pipeline_config
        
        response = requests.post(
            f"{self.base_url}/api/v1/rag/query",
            json=data,
            headers=self.headers
        )
        return response.json()
    
    async def connect_websocket(self):
        uri = f"ws://{self.base_url.replace('http://', '')}/ws?token={self.token}"
        self.websocket = await websockets.connect(uri)
        
        # Subscribe to document updates
        await self.websocket.send(json.dumps({
            "event": "join_room",
            "data": {"room": f"user_{self.user_id}"}
        }))
        
        return self.websocket
```

### JavaScript Client Example
```javascript
class DocumentAPI {
    constructor(baseUrl, token) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }
    
    async uploadDocument(file, metadata) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('metadata', JSON.stringify(metadata));
        
        const response = await fetch(`${this.baseUrl}/api/v1/documents/upload`, {
            method: 'POST',
            headers: {
                'Authorization': this.headers.Authorization
            },
            body: formData
        });
        
        return response.json();
    }
    
    async ragQuery(query, filters = null, pipelineConfig = null) {
        const data = { query };
        if (filters) data.filters = filters;
        if (pipelineConfig) data.pipeline_config = pipelineConfig;
        
        const response = await fetch(`${this.baseUrl}/api/v1/rag/query`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        });
        
        return response.json();
    }
    
    connectWebSocket() {
        const wsUrl = this.baseUrl.replace('http', 'ws');
        this.ws = new WebSocket(`${wsUrl}/ws?token=${this.token}`);
        
        this.ws.onopen = () => {
            // Subscribe to document updates
            this.ws.send(JSON.stringify({
                event: 'join_room',
                data: { room: `user_${this.userId}` }
            }));
        };
        
        return this.ws;
    }
}
```

## Testing

### Health Check
```bash
curl -X GET http://localhost:8000/health
```

### Authentication Test
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Document Upload Test
```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@sample_document.pdf" \
  -F "metadata={\"title\": \"Test Document\"}"
```

### RAG Query Test
```bash
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the payment terms?",
    "filters": {"document_types": ["invoice", "contract"]}
  }'
```

### WebSocket Test
```bash
# Using wscat or similar WebSocket client
wscat -c "ws://localhost:8000/ws?token=YOUR_TOKEN"
```

## Security Considerations

1. **JWT Token Security**: Tokens expire after 1 hour, refresh tokens after 7 days
2. **File Upload Security**: Only PDF, DOCX, and image files allowed
3. **Rate Limiting**: Prevents abuse and ensures fair usage
4. **Input Validation**: All inputs are validated and sanitized
5. **CORS**: Configured for specific origins only
6. **HTTPS**: Required in production environments
7. **WebSocket Authentication**: JWT tokens required for WebSocket connections
8. **Multi-Tenant Isolation**: Row-level security ensures data isolation
9. **OAuth2 Security**: Secure OAuth2 flows for external connectors
10. **API Key Management**: Secure storage and rotation of API keys

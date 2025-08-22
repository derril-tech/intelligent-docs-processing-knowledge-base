# API Specification

## Overview
This document outlines the API endpoints, data models, and integration patterns for the Intelligent Document Processing and Knowledge Base system.

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

## Data Models

### User Model
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "user",
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
  "user_id": 1
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

## Rate Limiting
- Authentication endpoints: 5 requests per minute
- Document upload: 10 requests per minute
- Search endpoints: 60 requests per minute
- Other endpoints: 100 requests per minute

## WebSocket Events

### Real-time Processing Updates
```json
{
  "event": "processing_update",
  "data": {
    "document_id": 123,
    "status": "processing",
    "progress": 75,
    "message": "Extracting text from page 3 of 4"
  }
}
```

### Validation Task Notifications
```json
{
  "event": "validation_task_created",
  "data": {
    "task_id": 789,
    "document_id": 123,
    "field_name": "amount",
    "priority": "high"
  }
}
```

## Integration Examples

### Python Client Example
```python
import requests

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
    
    def search_knowledge_base(self, query, filters=None):
        params = {'q': query}
        if filters:
            params['filters'] = json.dumps(filters)
        
        response = requests.get(
            f"{self.base_url}/api/v1/knowledge-base/search",
            params=params,
            headers=self.headers
        )
        return response.json()
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
    
    async searchKnowledgeBase(query, filters = null) {
        const params = new URLSearchParams({ q: query });
        if (filters) {
            params.append('filters', JSON.stringify(filters));
        }
        
        const response = await fetch(
            `${this.baseUrl}/api/v1/knowledge-base/search?${params}`,
            { headers: this.headers }
        );
        
        return response.json();
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

## Security Considerations

1. **JWT Token Security**: Tokens expire after 1 hour, refresh tokens after 7 days
2. **File Upload Security**: Only PDF, DOCX, and image files allowed
3. **Rate Limiting**: Prevents abuse and ensures fair usage
4. **Input Validation**: All inputs are validated and sanitized
5. **CORS**: Configured for specific origins only
6. **HTTPS**: Required in production environments

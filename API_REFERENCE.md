# API Reference

This document provides comprehensive documentation for the Intelligent Document Processing and Knowledge Base API.

## Base URL

```
Development: http://localhost:8000
Production: https://api.yourdomain.com
```

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Getting a Token

```http
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

Common HTTP status codes:
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Authentication Endpoints

### Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Get Current User

```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## User Management Endpoints

### List Users (Superuser Only)

```http
GET /api/v1/users/
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "full_name": "John Doe",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Get User by ID

```http
GET /api/v1/users/{user_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Update User

```http
PUT /api/v1/users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_name": "John Smith",
  "default_document_type": "invoice"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Smith",
  "is_active": true,
  "is_superuser": false,
  "default_document_type": "invoice",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Document Management Endpoints

### Upload Document

```http
POST /api/v1/documents/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <file>
document_type: invoice
metadata: {"source": "email", "priority": "high"}
```

**Response:**
```json
{
  "id": 1,
  "filename": "document_123.pdf",
  "original_filename": "invoice.pdf",
  "file_path": "/uploads/document_123.pdf",
  "file_size": 1024000,
  "mime_type": "application/pdf",
  "document_type": "invoice",
  "confidence_score": null,
  "status": "pending",
  "processing_started_at": null,
  "processing_completed_at": null,
  "error_message": null,
  "uploaded_by": 1,
  "uploaded_at": "2024-01-01T00:00:00Z"
}
```

### List Documents

```http
GET /api/v1/documents/
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 100)
- `status` (string): Filter by processing status
- `document_type` (string): Filter by document type
- `uploaded_after` (datetime): Filter by upload date

**Response:**
```json
{
  "documents": [
    {
      "id": 1,
      "filename": "document_123.pdf",
      "original_filename": "invoice.pdf",
      "file_path": "/uploads/document_123.pdf",
      "file_size": 1024000,
      "mime_type": "application/pdf",
      "document_type": "invoice",
      "confidence_score": 95,
      "status": "completed",
      "processing_started_at": "2024-01-01T00:01:00Z",
      "processing_completed_at": "2024-01-01T00:02:00Z",
      "error_message": null,
      "uploaded_by": 1,
      "uploaded_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 100,
  "pages": 1
}
```

### Get Document

```http
GET /api/v1/documents/{document_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "filename": "document_123.pdf",
  "original_filename": "invoice.pdf",
  "file_path": "/uploads/document_123.pdf",
  "file_size": 1024000,
  "mime_type": "application/pdf",
  "document_type": "invoice",
  "confidence_score": 95,
  "status": "completed",
  "processing_started_at": "2024-01-01T00:01:00Z",
  "processing_completed_at": "2024-01-01T00:02:00Z",
  "error_message": null,
  "uploaded_by": 1,
  "uploaded_at": "2024-01-01T00:00:00Z"
}
```

### Get Document Status

```http
GET /api/v1/documents/{document_id}/status
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "status": "completed",
  "processing_started_at": "2024-01-01T00:01:00Z",
  "processing_completed_at": "2024-01-01T00:02:00Z",
  "error_message": null
}
```

### Delete Document

```http
DELETE /api/v1/documents/{document_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Document deleted successfully"
}
```

## Knowledge Base Endpoints

### Search Knowledge Base

```http
POST /api/v1/knowledge/search
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "invoice amount greater than 1000",
  "filters": {
    "document_type": "invoice",
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    }
  },
  "page": 1,
  "size": 20,
  "sort_by": "created_at",
  "sort_order": "desc"
}
```

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "entry_type": "invoice_data",
      "title": "Invoice #12345",
      "description": "Sample invoice data",
      "structured_data": {
        "invoice_number": "12345",
        "amount": 1500.00,
        "vendor": "ABC Company",
        "date": "2024-01-15"
      },
      "confidence_score": 0.95,
      "search_score": 0.85,
      "tags": ["invoice", "financial"],
      "categories": ["billing"],
      "created_at": "2024-01-01T00:00:00Z",
      "document_id": 1
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20,
  "pages": 1,
  "query": "invoice amount greater than 1000",
  "filters": {
    "document_type": "invoice",
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    }
  }
}
```

### List Knowledge Entries

```http
GET /api/v1/knowledge/entries
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 100)
- `entry_type` (string): Filter by entry type
- `is_validated` (boolean): Filter by validation status

**Response:**
```json
[
  {
    "id": 1,
    "entry_type": "invoice_data",
    "title": "Invoice #12345",
    "description": "Sample invoice data",
    "structured_data": {
      "invoice_number": "12345",
      "amount": 1500.00,
      "vendor": "ABC Company"
    },
    "confidence_score": 0.95,
    "searchable_text": "Invoice 12345 ABC Company 1500.00",
    "tags": ["invoice", "financial"],
    "categories": ["billing"],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "is_validated": true,
    "validated_by": 1,
    "validated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Get Knowledge Entry

```http
GET /api/v1/knowledge/entries/{entry_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "entry_type": "invoice_data",
  "title": "Invoice #12345",
  "description": "Sample invoice data",
  "structured_data": {
    "invoice_number": "12345",
    "amount": 1500.00,
    "vendor": "ABC Company"
  },
  "confidence_score": 0.95,
  "searchable_text": "Invoice 12345 ABC Company 1500.00",
  "tags": ["invoice", "financial"],
  "categories": ["billing"],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "is_validated": true,
  "validated_by": 1,
  "validated_at": "2024-01-01T00:00:00Z"
}
```

### Get Knowledge Base Statistics

```http
GET /api/v1/knowledge/stats
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_entries": 1000,
  "total_documents": 500,
  "entries_by_type": {
    "invoice_data": 300,
    "contract_terms": 200,
    "medical_record": 150,
    "financial_statement": 350
  },
  "validation_pending": 50,
  "average_confidence": 0.87,
  "recent_activity": [
    {
      "entry_id": 1,
      "action": "created",
      "timestamp": "2024-01-01T00:00:00Z",
      "user_id": 1
    }
  ]
}
```

## Processing Management Endpoints

### Get Processing Queue Status

```http
GET /api/v1/processing/queue/status
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_tasks": 100,
  "pending_tasks": 20,
  "running_tasks": 5,
  "completed_tasks": 70,
  "failed_tasks": 5,
  "average_processing_time": 120.5,
  "active_workers": 3,
  "queue_health": "healthy"
}
```

### List Processing Tasks

```http
GET /api/v1/processing/tasks
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 100)
- `status` (string): Filter by task status
- `task_type` (string): Filter by task type

**Response:**
```json
[
  {
    "id": 1,
    "document_id": 1,
    "task_type": "ocr",
    "priority": "normal",
    "status": "completed",
    "retry_count": 0,
    "max_retries": 3,
    "queued_at": "2024-01-01T00:00:00Z",
    "started_at": "2024-01-01T00:01:00Z",
    "completed_at": "2024-01-01T00:02:00Z",
    "error_message": null,
    "error_details": null,
    "assigned_worker": "worker-1",
    "worker_pid": 12345
  }
]
```

### Get Processing Task Details

```http
GET /api/v1/processing/tasks/{task_id}/details
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "queue_entry_id": 1,
    "task_name": "perform_ocr",
    "status": "completed",
    "input_data": {
      "document_path": "/uploads/document_123.pdf"
    },
    "output_data": {
      "ocr_text": "Sample extracted text...",
      "confidence": 0.95
    },
    "task_config": {
      "language": "en",
      "tesseract_config": "--psm 6"
    },
    "started_at": "2024-01-01T00:01:00Z",
    "completed_at": "2024-01-01T00:02:00Z",
    "execution_time": 60,
    "error_message": null,
    "error_traceback": null,
    "depends_on_task_id": null
  }
]
```

### Retry Processing Task

```http
POST /api/v1/processing/tasks/{task_id}/retry
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Task queued for retry",
  "task_id": 1
}
```

### Cancel Processing Task

```http
POST /api/v1/processing/tasks/{task_id}/cancel
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Task cancelled successfully",
  "task_id": 1
}
```

## Validation Endpoints

### Get Validation Queue

```http
GET /api/v1/validation/queue
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 100)
- `status` (string): Filter by validation status
- `validation_type` (string): Filter by validation type
- `assigned_to` (int): Filter by assigned user

**Response:**
```json
[
  {
    "id": 1,
    "document_id": 1,
    "knowledge_entry_id": 1,
    "validation_type": "data_extraction",
    "status": "pending",
    "priority": 1,
    "original_data": {
      "invoice_number": "12345",
      "amount": "1500.00"
    },
    "suggested_corrections": {
      "amount": "1500.00"
    },
    "validation_metadata": {
      "confidence": 0.85,
      "extraction_method": "ai"
    },
    "assigned_to": null,
    "assigned_at": null,
    "created_at": "2024-01-01T00:00:00Z",
    "started_at": null,
    "completed_at": null,
    "sla_deadline": "2024-01-02T00:00:00Z",
    "is_overdue": false
  }
]
```

### Get Validation Queue Status

```http
GET /api/v1/validation/queue/status
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_tasks": 50,
  "pending_tasks": 20,
  "in_progress_tasks": 10,
  "completed_tasks": 15,
  "overdue_tasks": 5,
  "average_validation_time": 180.5,
  "assigned_tasks": 30,
  "unassigned_tasks": 20
}
```

### Assign Validation Task

```http
POST /api/v1/validation/tasks/{task_id}/assign
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": 1
}
```

**Response:**
```json
{
  "message": "Task assigned successfully",
  "task_id": 1,
  "assigned_to": 1
}
```

### Submit Validation Result

```http
POST /api/v1/validation/tasks/{task_id}/validate
Authorization: Bearer <token>
Content-Type: application/json

{
  "is_approved": true,
  "corrections": {
    "amount": "1500.00"
  },
  "confidence_score": 95,
  "validation_notes": "Amount looks correct",
  "validation_metadata": {
    "validation_time": 120
  }
}
```

**Response:**
```json
{
  "message": "Validation submitted successfully",
  "task_id": 1,
  "result": {
    "is_approved": true,
    "corrections": {
      "amount": "1500.00"
    },
    "confidence_score": 95
  }
}
```

### Get My Validation Tasks

```http
GET /api/v1/validation/my-tasks
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 100)
- `status` (string): Filter by validation status

**Response:**
```json
[
  {
    "id": 1,
    "document_id": 1,
    "knowledge_entry_id": 1,
    "validation_type": "data_extraction",
    "status": "in_progress",
    "priority": 1,
    "original_data": {
      "invoice_number": "12345",
      "amount": "1500.00"
    },
    "suggested_corrections": {
      "amount": "1500.00"
    },
    "validation_metadata": {
      "confidence": 0.85
    },
    "assigned_to": 1,
    "assigned_at": "2024-01-01T00:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "started_at": "2024-01-01T00:01:00Z",
    "completed_at": null,
    "sla_deadline": "2024-01-02T00:00:00Z",
    "is_overdue": false
  }
]
```

### Get Validation Statistics

```http
GET /api/v1/validation/stats
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_validated": 100,
  "approved_count": 85,
  "rejected_count": 15,
  "average_validation_time": 180.5,
  "validation_accuracy": 0.95,
  "recent_validations": [
    {
      "task_id": 1,
      "validation_type": "data_extraction",
      "result": "approved",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## Health Check Endpoints

### Application Health

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "elasticsearch": "healthy"
  }
}
```

### API Documentation

The interactive API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- **Authentication endpoints**: 10 requests per minute
- **Document upload**: 5 requests per minute
- **Search endpoints**: 100 requests per minute
- **Other endpoints**: 1000 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Webhooks

The API supports webhooks for real-time notifications:

### Register Webhook

```http
POST /api/v1/webhooks
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://your-domain.com/webhook",
  "events": ["document.processed", "validation.completed"],
  "secret": "your-webhook-secret"
}
```

### Webhook Events

Available events:
- `document.uploaded` - Document uploaded
- `document.processing` - Document processing started
- `document.processed` - Document processing completed
- `document.failed` - Document processing failed
- `validation.created` - Validation task created
- `validation.assigned` - Validation task assigned
- `validation.completed` - Validation task completed

### Webhook Payload Example

```json
{
  "event": "document.processed",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "document_id": 1,
    "status": "completed",
    "processing_time": 120.5
  }
}
```

This API reference provides comprehensive documentation for all endpoints and features of the Intelligent Document Processing platform.

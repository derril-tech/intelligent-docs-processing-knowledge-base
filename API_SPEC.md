# 🔌 API Specification - Intelligent Document Processing & Knowledge Base

## 📋 Overview

This document specifies the complete API integration between the Next.js 14 frontend and FastAPI backend for the Intelligent Document Processing & Knowledge Base system. All endpoints follow RESTful principles with JSON request/response formats.

---

## 🏗️ API Architecture

### Base Configuration
- **Base URL**: `https://api.intelligent-docs.com/v1` (Production)
- **Development URL**: `http://localhost:8000/v1`
- **Authentication**: JWT Bearer Token
- **Content-Type**: `application/json`
- **Rate Limiting**: 1000 requests/hour per user

### Environment Variables
```env
# Frontend Environment Variables
NEXT_PUBLIC_API_URL=http://localhost:8000/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000
```

---

## 🔐 Authentication Endpoints

### POST `/auth/login`
**Purpose**: User authentication and token generation

**Request Body**:
```typescript
interface LoginRequest {
  email: string;
  password: string;
  remember_me?: boolean;
}
```

**Response**:
```typescript
interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
  expires_in: number;
  user: User;
}
```

**Frontend Integration**:
```typescript
// lib/api.ts
async login(credentials: LoginRequest): Promise<LoginResponse> {
  const response = await this.post('/auth/login', credentials);
  this.setAuthToken(response.access_token);
  return response;
}
```

### POST `/auth/register`
**Purpose**: New user registration

**Request Body**:
```typescript
interface RegisterRequest {
  name: string;
  email: string;
  password: string;
  confirm_password: string;
  terms_accepted: boolean;
}
```

**Response**:
```typescript
interface RegisterResponse {
  user: User;
  message: string;
  verification_required: boolean;
}
```

### POST `/auth/refresh`
**Purpose**: Refresh access token

**Request Body**:
```typescript
interface RefreshRequest {
  refresh_token: string;
}
```

**Response**:
```typescript
interface RefreshResponse {
  access_token: string;
  expires_in: number;
}
```

### POST `/auth/logout`
**Purpose**: User logout and token invalidation

**Headers**: `Authorization: Bearer <token>`

**Response**:
```typescript
interface LogoutResponse {
  message: string;
}
```

### GET `/auth/me`
**Purpose**: Get current user information

**Headers**: `Authorization: Bearer <token>`

**Response**:
```typescript
interface UserResponse {
  user: User;
  permissions: Permission[];
  preferences: UserPreferences;
}
```

---

## 📄 Document Management Endpoints

### GET `/documents`
**Purpose**: Retrieve paginated list of documents

**Query Parameters**:
```typescript
interface DocumentQueryParams {
  page?: number;
  limit?: number;
  status?: DocumentStatus;
  type?: DocumentType;
  search?: string;
  date_from?: string;
  date_to?: string;
  sort_by?: 'created_at' | 'updated_at' | 'name' | 'size';
  sort_order?: 'asc' | 'desc';
}
```

**Response**:
```typescript
interface DocumentsResponse {
  documents: Document[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    pages: number;
  };
  stats: {
    total_documents: number;
    processing: number;
    completed: number;
    failed: number;
  };
}
```

### GET `/documents/{document_id}`
**Purpose**: Get specific document details

**Response**:
```typescript
interface DocumentDetailResponse {
  document: Document;
  extracted_data: ExtractedData;
  processing_results: ProcessingResults;
  quality_metrics: QualityMetrics;
  ai_insights: AIInsights;
}
```

### POST `/documents/upload`
**Purpose**: Upload new document for processing

**Content-Type**: `multipart/form-data`

**Form Data**:
```typescript
interface UploadRequest {
  file: File;
  document_type?: DocumentType;
  priority?: 'low' | 'normal' | 'high';
  metadata?: Record<string, any>;
}
```

**Response**:
```typescript
interface UploadResponse {
  document: Document;
  upload_id: string;
  processing_status: ProcessingStatus;
  estimated_completion_time?: string;
}
```

### DELETE `/documents/{document_id}`
**Purpose**: Delete document and associated data

**Response**:
```typescript
interface DeleteResponse {
  message: string;
  deleted_at: string;
}
```

### GET `/documents/{document_id}/status`
**Purpose**: Get real-time processing status

**Response**:
```typescript
interface StatusResponse {
  document_id: string;
  status: ProcessingStatus;
  progress: number;
  current_step: string;
  estimated_completion?: string;
  errors?: string[];
}
```

---

## 🔍 Knowledge Base Endpoints

### GET `/knowledge/search`
**Purpose**: Search knowledge base with natural language

**Query Parameters**:
```typescript
interface SearchQueryParams {
  query: string;
  filters?: {
    document_types?: DocumentType[];
    date_range?: {
      from: string;
      to: string;
    };
    confidence_threshold?: number;
  };
  page?: number;
  limit?: number;
  sort_by?: 'relevance' | 'date' | 'confidence';
}
```

**Response**:
```typescript
interface SearchResponse {
  results: KnowledgeEntry[];
  total_results: number;
  search_time: number;
  suggestions: string[];
  facets: {
    document_types: Record<string, number>;
    date_ranges: Record<string, number>;
  };
}
```

### GET `/knowledge/entries`
**Purpose**: Get knowledge base entries

**Query Parameters**:
```typescript
interface EntriesQueryParams {
  page?: number;
  limit?: number;
  document_id?: string;
  entity_type?: string;
  confidence_min?: number;
}
```

**Response**:
```typescript
interface EntriesResponse {
  entries: KnowledgeEntry[];
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
}
```

### GET `/knowledge/entries/{entry_id}`
**Purpose**: Get specific knowledge entry

**Response**:
```typescript
interface EntryDetailResponse {
  entry: KnowledgeEntry;
  related_entries: KnowledgeEntry[];
  source_documents: Document[];
}
```

### GET `/knowledge/stats`
**Purpose**: Get knowledge base statistics

**Response**:
```typescript
interface KnowledgeStatsResponse {
  total_entries: number;
  total_documents: number;
  entities_extracted: number;
  average_confidence: number;
  processing_success_rate: number;
  recent_activity: {
    documents_processed: number;
    entries_created: number;
    search_queries: number;
  };
}
```

---

## ⚙️ Processing Queue Endpoints

### GET `/processing/queue`
**Purpose**: Get processing queue status

**Response**:
```typescript
interface QueueStatusResponse {
  queue_stats: {
    total_tasks: number;
    pending: number;
    processing: number;
    completed: number;
    failed: number;
    average_processing_time: number;
  };
  recent_tasks: ProcessingTask[];
  system_status: {
    cpu_usage: number;
    memory_usage: number;
    queue_health: 'healthy' | 'warning' | 'critical';
  };
}
```

### GET `/processing/tasks`
**Purpose**: Get processing tasks

**Query Parameters**:
```typescript
interface TasksQueryParams {
  status?: ProcessingStatus;
  page?: number;
  limit?: number;
  user_id?: string;
}
```

**Response**:
```typescript
interface TasksResponse {
  tasks: ProcessingTask[];
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
}
```

### POST `/processing/tasks/{task_id}/retry`
**Purpose**: Retry failed processing task

**Response**:
```typescript
interface RetryResponse {
  task_id: string;
  status: ProcessingStatus;
  retry_count: number;
  estimated_completion: string;
}
```

### DELETE `/processing/tasks/{task_id}`
**Purpose**: Cancel processing task

**Response**:
```typescript
interface CancelResponse {
  task_id: string;
  status: 'cancelled';
  cancelled_at: string;
}
```

---

## ✅ Validation Endpoints

### GET `/validation/queue`
**Purpose**: Get validation queue

**Query Parameters**:
```typescript
interface ValidationQueueParams {
  status?: ValidationStatus;
  assigned_to?: string;
  priority?: 'low' | 'normal' | 'high';
  page?: number;
  limit?: number;
}
```

**Response**:
```typescript
interface ValidationQueueResponse {
  tasks: ValidationTask[];
  stats: {
    total_tasks: number;
    pending: number;
    in_progress: number;
    completed: number;
    average_completion_time: number;
  };
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
}
```

### GET `/validation/tasks/my`
**Purpose**: Get current user's validation tasks

**Response**:
```typescript
interface MyValidationTasksResponse {
  tasks: ValidationTask[];
  stats: {
    assigned: number;
    completed: number;
    accuracy_rate: number;
  };
}
```

### POST `/validation/tasks/{task_id}/assign`
**Purpose**: Assign validation task to current user

**Response**:
```typescript
interface AssignmentResponse {
  task_id: string;
  assigned_to: string;
  assigned_at: string;
  status: ValidationStatus;
}
```

### POST `/validation/tasks/{task_id}/submit`
**Purpose**: Submit validation result

**Request Body**:
```typescript
interface ValidationSubmissionRequest {
  result: ValidationResult;
  confidence: number;
  comments?: string;
  corrections?: {
    field: string;
    original_value: string;
    corrected_value: string;
    reason: string;
  }[];
}
```

**Response**:
```typescript
interface ValidationSubmissionResponse {
  task_id: string;
  status: ValidationStatus;
  submitted_at: string;
  quality_score: number;
}
```

---

## 🔌 WebSocket Events

### Connection
**URL**: `ws://localhost:8000/ws`
**Authentication**: JWT token in query parameter

```typescript
// Connection with authentication
const socket = io('ws://localhost:8000/ws', {
  auth: {
    token: accessToken
  }
});
```

### Client Events (Frontend → Backend)

#### `join_room`
```typescript
interface JoinRoomEvent {
  room: string; // 'user_{user_id}' | 'processing' | 'validation'
}
```

#### `leave_room`
```typescript
interface LeaveRoomEvent {
  room: string;
}
```

### Server Events (Backend → Frontend)

#### `document_processed`
```typescript
interface DocumentProcessedEvent {
  document_id: string;
  status: ProcessingStatus;
  progress: number;
  extracted_data?: ExtractedData;
  errors?: string[];
}
```

#### `validation_task_updated`
```typescript
interface ValidationTaskUpdatedEvent {
  task_id: string;
  status: ValidationStatus;
  assigned_to?: string;
  updated_at: string;
}
```

#### `knowledge_base_updated`
```typescript
interface KnowledgeBaseUpdatedEvent {
  document_id: string;
  entries_added: number;
  entities_extracted: number;
  updated_at: string;
}
```

#### `processing_queue_update`
```typescript
interface ProcessingQueueUpdateEvent {
  queue_stats: {
    pending: number;
    processing: number;
    completed: number;
    failed: number;
  };
  system_status: {
    cpu_usage: number;
    memory_usage: number;
    queue_health: string;
  };
}
```

---

## 📊 Data Types

### User Types
```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  avatar_url?: string;
  created_at: string;
  updated_at: string;
  last_login?: string;
  preferences: UserPreferences;
}

interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  language: string;
  timezone: string;
  notifications: NotificationSettings;
  dashboard_layout: DashboardLayout;
}

interface UserRole {
  id: string;
  name: string;
  permissions: Permission[];
}
```

### Document Types
```typescript
interface Document {
  id: string;
  name: string;
  original_filename: string;
  file_size: number;
  file_type: string;
  document_type: DocumentType;
  status: DocumentStatus;
  processing_status: ProcessingStatus;
  uploaded_by: string;
  uploaded_at: string;
  processed_at?: string;
  metadata: DocumentMetadata;
  tags: string[];
}

interface DocumentMetadata {
  page_count?: number;
  language?: string;
  confidence_score?: number;
  extracted_text_length?: number;
  processing_duration?: number;
}

interface ExtractedData {
  entities: Entity[];
  tables: Table[];
  images: ExtractedImage[];
  signatures: Signature[];
  dates: DateEntity[];
  amounts: AmountEntity[];
  addresses: AddressEntity[];
}
```

### Processing Types
```typescript
interface ProcessingTask {
  id: string;
  document_id: string;
  status: ProcessingStatus;
  progress: number;
  current_step: string;
  started_at: string;
  completed_at?: string;
  error_message?: string;
  retry_count: number;
  priority: 'low' | 'normal' | 'high';
}

interface ProcessingResults {
  ocr_results: OCRResults;
  nlp_results: NLPResults;
  classification_results: ClassificationResults;
  extraction_results: ExtractionResults;
  quality_metrics: QualityMetrics;
  ai_insights: AIInsights;
}
```

### Validation Types
```typescript
interface ValidationTask {
  id: string;
  document_id: string;
  field_name: string;
  field_value: string;
  confidence_score: number;
  status: ValidationStatus;
  assigned_to?: string;
  assigned_at?: string;
  completed_at?: string;
  priority: 'low' | 'normal' | 'high';
  context: {
    surrounding_text: string;
    document_section: string;
    extracted_entities: Entity[];
  };
}

interface ValidationResult {
  is_correct: boolean;
  corrected_value?: string;
  confidence: number;
  comments?: string;
  corrections?: ValidationCorrection[];
}
```

---

## 🛡️ Error Handling

### Error Response Format
```typescript
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: any;
    timestamp: string;
    request_id: string;
  };
}
```

### Common Error Codes
- `AUTH_001`: Invalid credentials
- `AUTH_002`: Token expired
- `AUTH_003`: Insufficient permissions
- `DOC_001`: Document not found
- `DOC_002`: Invalid file format
- `DOC_003`: File too large
- `PROC_001`: Processing task not found
- `PROC_002`: Task already in progress
- `VAL_001`: Validation task not found
- `VAL_002`: Task already assigned
- `API_001`: Rate limit exceeded
- `API_002`: Invalid request format

### Frontend Error Handling
```typescript
// lib/api.ts
class ApiError extends Error {
  constructor(
    public code: string,
    public message: string,
    public status: number,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Error handling in API client
private handleError(error: any): never {
  if (error.response) {
    const { data, status } = error.response;
    throw new ApiError(
      data.error?.code || 'UNKNOWN_ERROR',
      data.error?.message || 'An unknown error occurred',
      status,
      data.error?.details
    );
  }
  throw new ApiError('NETWORK_ERROR', 'Network error occurred', 0);
}
```

---

## 🔄 Real-time Integration

### WebSocket Provider Setup
```typescript
// app/providers/websocket-provider.tsx
const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { accessToken } = useAuth();
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    if (accessToken) {
      const newSocket = io(process.env.NEXT_PUBLIC_WS_URL!, {
        auth: { token: accessToken },
        transports: ['websocket'],
        autoConnect: true,
      });

      newSocket.on('connect', () => {
        console.log('WebSocket connected');
        newSocket.emit('join_room', { room: 'user' });
      });

      newSocket.on('document_processed', (data) => {
        // Update document status in real-time
        queryClient.invalidateQueries(['documents']);
      });

      newSocket.on('validation_task_updated', (data) => {
        // Update validation tasks in real-time
        queryClient.invalidateQueries(['validation-tasks']);
      });

      setSocket(newSocket);
    }

    return () => {
      if (socket) {
        socket.disconnect();
      }
    };
  }, [accessToken]);

  return (
    <WebSocketContext.Provider value={{ socket }}>
      {children}
    </WebSocketContext.Provider>
  );
};
```

### React Query Integration
```typescript
// Custom hooks for API integration
export const useDocuments = (params: DocumentQueryParams) => {
  return useQuery({
    queryKey: ['documents', params],
    queryFn: () => apiClient.getDocuments(params),
    staleTime: 30000, // 30 seconds
    refetchOnWindowFocus: false,
  });
};

export const useDocument = (id: string) => {
  return useQuery({
    queryKey: ['document', id],
    queryFn: () => apiClient.getDocument(id),
    enabled: !!id,
  });
};

export const useProcessingQueue = () => {
  return useQuery({
    queryKey: ['processing-queue'],
    queryFn: () => apiClient.getProcessingQueueStatus(),
    refetchInterval: 5000, // Refetch every 5 seconds
  });
};
```

---

## 🧪 Testing Integration

### API Mocking for Tests
```typescript
// __mocks__/api.ts
export const mockApiClient = {
  login: jest.fn(),
  getDocuments: jest.fn(),
  uploadDocument: jest.fn(),
  searchKnowledgeBase: jest.fn(),
  getProcessingQueueStatus: jest.fn(),
  getValidationQueue: jest.fn(),
};

// Test setup
beforeEach(() => {
  jest.clearAllMocks();
});
```

### Component Testing
```typescript
// components/features/__tests__/document-upload.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { DocumentUpload } from '../document-upload';

describe('DocumentUpload', () => {
  it('should upload document successfully', async () => {
    const mockUpload = jest.fn().mockResolvedValue({
      document: { id: '1', name: 'test.pdf' },
      upload_id: 'upload-1',
    });

    render(<DocumentUpload onUpload={mockUpload} />);

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const dropzone = screen.getByTestId('dropzone');

    fireEvent.drop(dropzone, {
      dataTransfer: {
        files: [file],
      },
    });

    await waitFor(() => {
      expect(mockUpload).toHaveBeenCalledWith(file);
    });
  });
});
```

---

## 🚀 Deployment Configuration

### Environment Variables
```env
# Production Environment
NEXT_PUBLIC_API_URL=https://api.intelligent-docs.com/v1
NEXT_PUBLIC_WS_URL=wss://api.intelligent-docs.com/ws
NEXTAUTH_SECRET=your-production-secret
NEXTAUTH_URL=https://app.intelligent-docs.com

# Staging Environment
NEXT_PUBLIC_API_URL=https://staging-api.intelligent-docs.com/v1
NEXT_PUBLIC_WS_URL=wss://staging-api.intelligent-docs.com/ws
NEXTAUTH_SECRET=your-staging-secret
NEXTAUTH_URL=https://staging.intelligent-docs.com
```

### Vercel Configuration
```json
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url",
    "NEXT_PUBLIC_WS_URL": "@ws-url",
    "NEXTAUTH_SECRET": "@auth-secret",
    "NEXTAUTH_URL": "@auth-url"
  }
}
```

---

This API specification provides a complete integration guide for the frontend-backend communication in the Intelligent Document Processing & Knowledge Base system. All endpoints are designed to work seamlessly with the React components and provide real-time updates through WebSocket connections.

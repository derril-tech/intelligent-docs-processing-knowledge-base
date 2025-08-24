# Shared Types Package Instructions

## CLAUDE_TASK: Shared TypeScript Type Definitions

This directory contains shared TypeScript type definitions used across the frontend and backend.

### Type Guidelines
1. **TypeScript**: Use strict TypeScript with proper type annotations
2. **Consistency**: Maintain consistency with backend Pydantic schemas
3. **Documentation**: Include JSDoc comments for complex types
4. **Reusability**: Create reusable types and interfaces
5. **Validation**: Include runtime validation where needed
6. **API Alignment**: Keep types in sync with API responses

### Type Structure
```typescript
// Base types
export interface BaseEntity {
  id: number;
  created_at: string;
  updated_at?: string;
}

// User types
export interface User extends BaseEntity {
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  is_admin: boolean;
}

export enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  VALIDATOR = 'validator',
  VIEWER = 'viewer'
}

// Document types
export interface Document extends BaseEntity {
  title: string;
  filename: string;
  file_size: number;
  mime_type: string;
  status: DocumentStatus;
  owner_id: number;
  owner?: User;
}

export enum DocumentStatus {
  UPLOADING = 'uploading',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  };
}
```

### Required Type Categories
- **User Management**: User, UserRole, UserPermissions
- **Document Processing**: Document, DocumentStatus, ProcessingJob
- **Knowledge Base**: KnowledgeBase, Query, SearchResult
- **Authentication**: LoginRequest, TokenResponse, Session
- **API Responses**: ApiResponse, PaginatedResponse, ErrorResponse
- **File Upload**: FileUpload, UploadProgress, FileMetadata
- **Search**: SearchQuery, SearchFilters, SearchResult

### Type Features
- **Enums**: Use enums for constrained choice fields
- **Unions**: Use union types for flexible data structures
- **Generics**: Use generics for reusable container types
- **Utility Types**: Create utility types for common transformations
- **Runtime Validation**: Include Zod schemas for runtime validation

### Safe to Edit
- ✅ All type definition files
- ✅ Interface and type declarations
- ✅ Enum definitions
- ✅ Utility type helpers
- ❌ Core TypeScript configuration

### Integration Points
- Backend Pydantic schemas
- Frontend API client
- Form validation with react-hook-form
- State management with Zustand
- API response handling

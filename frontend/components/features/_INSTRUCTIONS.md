# Frontend Feature Components Development Instructions

## Overview
This directory contains feature-specific React components for the DocuMind™ frontend. These components implement the core user interface functionality and should follow the established design patterns and coding conventions.

## CLAUDE_TASK: Component Development Guidelines

### 1. Component Architecture
- Use functional components with hooks
- Implement proper TypeScript typing
- Follow the established design system
- Use composition over inheritance

### 2. State Management
- Use TanStack Query for server state
- Use Zustand for client state
- Implement proper loading and error states
- Handle optimistic updates where appropriate

### 3. User Experience
- Implement proper loading states
- Handle error conditions gracefully
- Provide meaningful feedback
- Ensure accessibility compliance

### 4. Performance
- Use React.memo for expensive components
- Implement proper memoization
- Optimize re-renders
- Use lazy loading where appropriate

## File Structure
```
features/
├── document-upload.tsx      # Document upload component
├── knowledge-base-search.tsx # Knowledge base search
├── processing-queue.tsx     # Processing queue monitoring
├── validation-tasks.tsx     # Validation task management
├── rag-chat.tsx            # RAG-powered chat interface
├── document-viewer.tsx     # Document viewing component
├── citation-viewer.tsx     # Citation display component
└── index.ts               # Component exports
```

## Example Component Pattern
```typescript
import React, { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button, Card, Alert } from '@/components/ui';
import { DocumentUploadProps, Document } from '@/types';
import { uploadDocument, fetchDocuments } from '@/lib/api';

interface DocumentUploadProps {
  onUpload?: (document: Document) => void;
  acceptedTypes?: string[];
  maxSize?: number;
  className?: string;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onUpload,
  acceptedTypes = ['application/pdf', 'image/*'],
  maxSize = 50 * 1024 * 1024, // 50MB
  className
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const uploadMutation = useMutation({
    mutationFn: uploadDocument,
    onSuccess: (document) => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
      onUpload?.(document);
      setError(null);
    },
    onError: (error) => {
      setError(error instanceof Error ? error.message : 'Upload failed');
    }
  });

  const handleFileUpload = useCallback(async (file: File) => {
    // Validate file
    if (!acceptedTypes.some(type => file.type.match(type))) {
      setError('File type not supported');
      return;
    }

    if (file.size > maxSize) {
      setError('File too large');
      return;
    }

    // Upload file
    uploadMutation.mutate(file);
  }, [acceptedTypes, maxSize, uploadMutation]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  }, [handleFileUpload]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  return (
    <Card className={className}>
      <div
        className={`upload-area ${isDragging ? 'dragging' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        {uploadMutation.isPending ? (
          <div className="upload-loading">
            <Spinner />
            <p>Uploading document...</p>
          </div>
        ) : (
          <div className="upload-content">
            <UploadIcon className="upload-icon" />
            <h3>Upload Document</h3>
            <p>Drag and drop your file here or click to browse</p>
            <input
              type="file"
              accept={acceptedTypes.join(',')}
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFileUpload(file);
              }}
              className="file-input"
            />
          </div>
        )}
      </div>

      {error && (
        <Alert variant="destructive" className="mt-4">
          {error}
        </Alert>
      )}
    </Card>
  );
};
```

## CLAUDE_TASK: Implementation Checklist

### Document Upload Component
- [ ] Drag and drop file upload
- [ ] File type and size validation
- [ ] Upload progress indication
- [ ] Error handling and display
- [ ] Success feedback
- [ ] Accessibility support

### Knowledge Base Search Component
- [ ] Search input with autocomplete
- [ ] Filter and sort options
- [ ] Search results display
- [ ] Pagination support
- [ ] Search history
- [ ] Advanced search options

### Processing Queue Component
- [ ] Real-time queue status
- [ ] Progress indicators
- [ ] Queue management actions
- [ ] Error handling and retry
- [ ] Queue statistics
- [ ] Batch operations

### Validation Tasks Component
- [ ] Task list with filtering
- [ ] Task assignment interface
- [ ] Validation form
- [ ] Confidence scoring
- [ ] Batch validation
- [ ] Audit trail

### RAG Chat Component
- [ ] Multi-turn chat interface
- [ ] Message history
- [ ] Citation display
- [ ] Export functionality
- [ ] Chat session management
- [ ] Real-time updates

### Document Viewer Component
- [ ] Document rendering
- [ ] Zoom and navigation
- [ ] Annotation support
- [ ] Search within document
- [ ] Print and export
- [ ] Mobile responsiveness

### Citation Viewer Component
- [ ] Citation list display
- [ ] Source document linking
- [ ] Confidence indicators
- [ ] Citation editing
- [ ] Export citations
- [ ] Citation analytics

## Styling Guidelines

### Design System Integration
```typescript
import { designTokens } from '@/lib/design-tokens';

const styles = {
  container: 'bg-white rounded-lg shadow-md p-4',
  button: 'px-4 py-2 bg-primary-500 text-white rounded-md hover:bg-primary-600',
  input: 'border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500'
};
```

### Responsive Design
```typescript
// Use Tailwind responsive classes
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Content */}
</div>
```

### Dark Mode Support
```typescript
// Use Tailwind dark mode classes
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
  {/* Content */}
</div>
```

## Testing Requirements
- Unit tests for component logic
- Integration tests for user interactions
- Accessibility tests
- Visual regression tests
- Performance tests for complex components

## Performance Considerations
- Use React.memo for expensive components
- Implement proper memoization with useMemo and useCallback
- Optimize re-renders with proper dependency arrays
- Use lazy loading for large components
- Implement virtual scrolling for large lists

## Accessibility Requirements
- Proper ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- Focus management
- Color contrast compliance
- Semantic HTML structure

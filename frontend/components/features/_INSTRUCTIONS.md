# Frontend Feature Components Instructions

## Purpose
This folder contains feature-specific React components that implement the core functionality of the application. These components are business logic focused and combine multiple UI components to create complete features.

## File Structure
- `document-upload.tsx` - Document upload and file management component
- `knowledge-base-search.tsx` - Knowledge base search interface component
- `processing-queue.tsx` - Processing queue status and management component
- `validation-tasks.tsx` - Validation task management component

## Implementation Guidelines

### Component Pattern
```typescript
import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { DocumentUploadProps, UploadResponse } from '@/types/document';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { useToast } from '@/hooks/use-toast';

interface DocumentUploadComponentProps {
  onUploadComplete?: (document: UploadResponse) => void;
  maxFileSize?: number;
  acceptedTypes?: string[];
}

export const DocumentUploadComponent: React.FC<DocumentUploadComponentProps> = ({
  onUploadComplete,
  maxFileSize = 50 * 1024 * 1024, // 50MB
  acceptedTypes = ['pdf', 'docx', 'jpg', 'jpeg', 'png', 'tiff']
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const { toast } = useToast();

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('/api/documents/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Upload failed');
      }
      
      return response.json();
    },
    onSuccess: (data) => {
      toast({
        title: 'Upload Successful',
        description: 'Document uploaded and processing started',
      });
      onUploadComplete?.(data);
    },
    onError: (error) => {
      toast({
        title: 'Upload Failed',
        description: error.message,
        variant: 'destructive',
      });
    },
  });

  const handleFileSelect = (file: File) => {
    // Validate file
    if (file.size > maxFileSize) {
      toast({
        title: 'File Too Large',
        description: `File size must be less than ${maxFileSize / 1024 / 1024}MB`,
        variant: 'destructive',
      });
      return;
    }

    const fileExtension = file.name.split('.').pop()?.toLowerCase();
    if (!acceptedTypes.includes(fileExtension || '')) {
      toast({
        title: 'Invalid File Type',
        description: `Accepted types: ${acceptedTypes.join(', ')}`,
        variant: 'destructive',
      });
      return;
    }

    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    
    uploadMutation.mutate(selectedFile);
  };

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4">Upload Document</h3>
      
      <div className="space-y-4">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
          <input
            type="file"
            accept={acceptedTypes.map(type => `.${type}`).join(',')}
            onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <div className="text-gray-600">
              <p>Click to select a file or drag and drop</p>
              <p className="text-sm text-gray-500 mt-2">
                Accepted types: {acceptedTypes.join(', ')}
              </p>
            </div>
          </label>
        </div>

        {selectedFile && (
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="font-medium">{selectedFile.name}</p>
            <p className="text-sm text-gray-600">
              {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
        )}

        {uploadMutation.isPending && (
          <div className="space-y-2">
            <Progress value={uploadProgress} className="w-full" />
            <p className="text-sm text-gray-600">Uploading...</p>
          </div>
        )}

        <Button
          onClick={handleUpload}
          disabled={!selectedFile || uploadMutation.isPending}
          className="w-full"
        >
          {uploadMutation.isPending ? 'Uploading...' : 'Upload Document'}
        </Button>
      </div>
    </div>
  );
};
```

### Component Responsibilities
- **Business Logic**: Implement feature-specific business logic
- **State Management**: Manage component state and side effects
- **API Integration**: Handle API calls and data fetching
- **User Interaction**: Process user inputs and actions
- **Error Handling**: Handle and display errors appropriately

### Component Guidelines
- Use TypeScript for type safety
- Implement proper error handling
- Use React Query for data fetching
- Follow accessibility guidelines
- Implement responsive design
- Use consistent styling with design system

### Feature Components

#### Document Upload Component
- File selection and validation
- Upload progress tracking
- Error handling and user feedback
- Integration with processing queue

#### Knowledge Base Search Component
- Search interface with filters
- Real-time search results
- Result pagination and sorting
- Search history and suggestions

#### Processing Queue Component
- Queue status display
- Progress tracking
- Error handling and retry
- Queue management actions

#### Validation Tasks Component
- Task list and filtering
- Task assignment and completion
- Validation interface
- Task history and analytics

## TODO Items
- [ ] Implement document upload component
- [ ] Create knowledge base search component
- [ ] Add processing queue component
- [ ] Implement validation tasks component
- [ ] Add document viewer component
- [ ] Create analytics dashboard component
- [ ] Implement user management component
- [ ] Add settings and preferences component
- [ ] Create notification center component
- [ ] Implement export and sharing components

## Notes
- Keep components focused on single features
- Use composition over inheritance
- Implement proper loading states
- Add comprehensive error handling
- Write unit tests for all components
- Follow accessibility best practices

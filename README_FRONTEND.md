# Frontend Documentation - DocuMind™

## Overview

The DocuMind™ frontend is built with Next.js 14+ using the App Router, TypeScript 5+, and Tailwind CSS 3+. It provides a modern, responsive interface for document processing, RAG-powered Q&A, and knowledge management.

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+ with custom design tokens
- **State Management**: TanStack Query (server state), Zustand (client state)
- **Forms**: React Hook Form with Zod validation
- **UI Components**: Radix UI primitives + shadcn/ui
- **Real-time**: Socket.IO client
- **Testing**: Jest, React Testing Library, Playwright

## Quick Start

### Prerequisites
- Node.js 18.17.0+
- pnpm (recommended) or npm

### Installation
```bash
# Install dependencies
pnpm install

# Copy environment variables
cp env.example .env.local

# Start development server
pnpm dev
```

### Environment Variables
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Feature Flags
NEXT_PUBLIC_ENABLE_RAG=true
NEXT_PUBLIC_ENABLE_VALIDATION=true
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication pages
│   ├── dashboard/         # Main application pages
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable components
│   ├── features/          # Feature-specific components
│   └── ui/               # Base UI components
├── hooks/                # Custom React hooks
├── lib/                  # Utility functions
├── types/                # TypeScript type definitions
└── design-tokens.ts      # Centralized design system
```

## Key Features

### 1. Authentication
- JWT-based authentication
- Role-based access control
- Multi-tenant support
- Session management

### 2. Dashboard
- Document upload and management
- Processing queue monitoring
- Real-time status updates
- Search and filtering

### 3. RAG Interface
- Multi-turn chat interface
- Citation display
- Source document linking
- Export capabilities

### 4. Validation Queue
- Human-in-the-loop validation
- Confidence scoring
- Batch operations
- Audit trail

## Development Guidelines

### Component Structure
```typescript
// Feature component example
interface DocumentUploadProps {
  onUpload: (file: File) => Promise<void>;
  acceptedTypes: string[];
  maxSize: number;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onUpload,
  acceptedTypes,
  maxSize
}) => {
  // Implementation
};
```

### State Management
```typescript
// Server state with TanStack Query
const { data: documents, isLoading } = useQuery({
  queryKey: ['documents', filters],
  queryFn: () => fetchDocuments(filters)
});

// Client state with Zustand
const useDocumentStore = create<DocumentStore>((set) => ({
  selectedDocuments: [],
  setSelectedDocuments: (docs) => set({ selectedDocuments: docs })
}));
```

### Styling
```typescript
// Use design tokens
import { designTokens } from '@/lib/design-tokens';

const styles = {
  container: 'bg-white rounded-lg shadow-md p-4',
  button: 'px-4 py-2 bg-primary-500 text-white rounded-md hover:bg-primary-600'
};
```

## Testing

### Unit Tests
```bash
# Run unit tests
pnpm test

# Run with coverage
pnpm test:coverage

# Watch mode
pnpm test:watch
```

### E2E Tests
```bash
# Run E2E tests
pnpm test:e2e

# Run with UI
pnpm test:e2e:ui
```

### Component Testing
```typescript
import { render, screen } from '@testing-library/react';
import { DocumentUpload } from './DocumentUpload';

describe('DocumentUpload', () => {
  it('renders upload area', () => {
    render(<DocumentUpload onUpload={jest.fn()} acceptedTypes={[]} maxSize={100} />);
    expect(screen.getByText(/drop files/i)).toBeInTheDocument();
  });
});
```

## Build & Deployment

### Development
```bash
pnpm dev          # Start development server
pnpm build        # Build for production
pnpm start        # Start production server
```

### Production
```bash
# Build the application
pnpm build

# Start production server
pnpm start
```

### Docker
```bash
# Build Docker image
docker build -t documind-frontend .

# Run container
docker run -p 3000:3000 documind-frontend
```

## Performance

### Bundle Analysis
```bash
# Analyze bundle size
pnpm build:analyze
```

### Performance Budgets
- Initial bundle: < 500KB
- First Contentful Paint: < 1.5s
- Largest Contentful Paint: < 2.5s
- Cumulative Layout Shift: < 0.1

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Clear `.next` directory: `rm -rf .next`
   - Reinstall dependencies: `pnpm install`

2. **TypeScript Errors**
   - Check type definitions in `types/`
   - Verify API response types match schemas

3. **Styling Issues**
   - Ensure Tailwind classes are correct
   - Check design tokens in `lib/design-tokens.ts`

4. **API Connection**
   - Verify `NEXT_PUBLIC_API_URL` is correct
   - Check CORS configuration on backend

## Contributing

1. Follow the coding conventions in `docs/CLAUDE.md`
2. Write tests for new features
3. Update documentation as needed
4. Use conventional commit messages
5. Ensure all CI checks pass

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TanStack Query](https://tanstack.com/query/latest)
- [Radix UI](https://www.radix-ui.com/)
- [shadcn/ui](https://ui.shadcn.com/)

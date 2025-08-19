# 🗺️ Intelligent Document Processing & Knowledge Base - Frontend Repository Map

## 📁 Project Structure Overview

This repository contains a complete Next.js 14 frontend application for an AI-powered document processing and knowledge base system. The architecture follows modern React patterns with TypeScript, Tailwind CSS, and comprehensive state management.

```
frontend/
├── 📁 app/                          # Next.js 14 App Router directory
├── 📁 components/                   # Reusable UI components
├── 📁 hooks/                        # Custom React hooks
├── 📁 lib/                          # Utility functions and API client
├── 📁 types/                        # TypeScript type definitions
├── 📄 Configuration files           # Build, linting, styling configs
└── 📄 Documentation                 # Project documentation
```

---

## 🏗️ Core Application Structure

### 📁 `app/` - Next.js App Router
**Purpose**: Contains all pages and layouts using Next.js 14 App Router architecture

#### 📄 `layout.tsx`
- **Purpose**: Root layout wrapper for the entire application
- **Key Features**: 
  - Global metadata configuration
  - Providers wrapper (Theme, Auth, Query, WebSocket)
  - Global CSS imports
- **Claude Code Note**: This is the entry point for all pages

#### 📄 `page.tsx`
- **Purpose**: Landing page with marketing content
- **Key Features**:
  - Hero section with call-to-action
  - Feature highlights
  - Statistics display
  - Responsive design
- **Claude Code Note**: Replace with your actual landing page content

#### 📄 `globals.css`
- **Purpose**: Global CSS styles and Tailwind directives
- **Key Features**:
  - Tailwind CSS imports
  - CSS variables for theming
  - Custom component styles
  - Utility classes
- **Claude Code Note**: Contains all global styling and theme variables

#### 📁 `providers/` - Context Providers
**Purpose**: Centralized state management and context providers

##### 📄 `index.tsx`
- **Purpose**: Main providers wrapper
- **Key Features**:
  - QueryClientProvider for React Query
  - ThemeProvider for dark/light mode
  - AuthProvider for authentication
  - WebSocketProvider for real-time updates
  - Toaster for notifications
- **Claude Code Note**: All providers are configured here for easy management

##### 📄 `auth-provider.tsx`
- **Purpose**: Authentication context and functions
- **Key Features**:
  - User state management
  - Login/register/logout functions
  - Token management
  - Session persistence
- **Claude Code Note**: Handles all authentication logic and user state

##### 📄 `websocket-provider.tsx`
- **Purpose**: Real-time WebSocket connections
- **Key Features**:
  - Socket.io client connection
  - Event listeners for document processing
  - Real-time updates
  - Connection management
- **Claude Code Note**: Manages all real-time communication with backend

#### 📁 `(auth)/` - Authentication Pages
**Purpose**: Login and registration pages

##### 📄 `login/page.tsx`
- **Purpose**: User login interface
- **Key Features**:
  - Form validation with Zod
  - Password visibility toggle
  - Error handling
  - Loading states
- **Claude Code Note**: Uses react-hook-form for form management

##### 📄 `register/page.tsx`
- **Purpose**: User registration interface
- **Key Features**:
  - Multi-step registration
  - Password strength validation
  - Email verification
  - Terms acceptance
- **Claude Code Note**: Includes comprehensive validation

#### 📁 `dashboard/` - Protected Dashboard Pages
**Purpose**: Main application interface (requires authentication)

##### 📄 `layout.tsx`
- **Purpose**: Dashboard layout with navigation
- **Key Features**:
  - Sidebar navigation
  - Top header with user menu
  - Theme toggle
  - Mobile responsive
- **Claude Code Note**: Protects all dashboard routes

##### 📄 `page.tsx`
- **Purpose**: Dashboard overview page
- **Key Features**:
  - Welcome message
  - Quick action cards
  - Statistics dashboard
  - Recent documents
- **Claude Code Note**: Main dashboard with key metrics

##### 📁 `documents/` - Document Management
##### 📄 `page.tsx`
- **Purpose**: Document upload and search interface
- **Key Features**:
  - Document upload component
  - Knowledge base search
  - Document filtering
  - Tabbed interface
- **Claude Code Note**: Integrates DocumentUpload and KnowledgeBaseSearch components

##### 📁 `processing/` - Processing Management
##### 📄 `page.tsx`
- **Purpose**: Processing queue and validation tasks
- **Key Features**:
  - Processing queue monitoring
  - Validation task management
  - Real-time updates
  - Task actions
- **Claude Code Note**: Integrates ProcessingQueue and ValidationTasks components

---

## 🧩 Components Architecture

### 📁 `components/` - Reusable Components
**Purpose**: Modular, reusable UI components following atomic design principles

#### 📁 `ui/` - Base UI Components
**Purpose**: Fundamental UI building blocks

##### 📄 `button.tsx`
- **Purpose**: Reusable button component
- **Variants**: default, destructive, outline, secondary, ghost, link
- **Sizes**: default, sm, lg, icon
- **Claude Code Note**: Uses class-variance-authority for variant management

##### 📄 `card.tsx`
- **Purpose**: Card layout components
- **Components**: Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter
- **Claude Code Note**: Provides structured content containers

##### 📄 `input.tsx`
- **Purpose**: Form input component
- **Features**: Standard styling, focus states, accessibility
- **Claude Code Note**: Base input for all form fields

##### 📄 `textarea.tsx`
- **Purpose**: Multi-line text input
- **Features**: Resizable, consistent styling
- **Claude Code Note**: For longer text inputs

##### 📄 `select.tsx`
- **Purpose**: Dropdown select component
- **Features**: Radix UI primitives, accessible
- **Claude Code Note**: For single-choice selections

##### 📄 `modal.tsx`
- **Purpose**: Dialog/modal components
- **Features**: Radix UI Dialog, accessible, backdrop
- **Claude Code Note**: For overlays and confirmations

##### 📄 `table.tsx`
- **Purpose**: Data table components
- **Features**: Sortable, paginated, responsive
- **Claude Code Note**: For displaying tabular data

##### 📄 `tabs.tsx`
- **Purpose**: Tabbed interface
- **Features**: Radix UI Tabs, accessible
- **Claude Code Note**: For organizing content sections

##### 📄 `progress.tsx`
- **Purpose**: Progress indicator
- **Features**: Animated, customizable
- **Claude Code Note**: For showing loading/processing states

##### 📄 `alert.tsx`
- **Purpose**: Alert/notification component
- **Variants**: default, destructive, warning, info
- **Claude Code Note**: For important messages

##### 📄 `tooltip.tsx`
- **Purpose**: Tooltip component
- **Features**: Radix UI Tooltip, accessible
- **Claude Code Note**: For additional information

##### 📄 `checkbox.tsx`
- **Purpose**: Checkbox input
- **Features**: Radix UI Checkbox, accessible
- **Claude Code Note**: For boolean selections

##### 📄 `switch.tsx`
- **Purpose**: Toggle switch
- **Features**: Radix UI Switch, accessible
- **Claude Code Note**: For on/off toggles

##### 📄 `radio-group.tsx`
- **Purpose**: Radio button group
- **Features**: Radix UI RadioGroup, accessible
- **Claude Code Note**: For single-choice from multiple options

##### 📄 `skeleton.tsx`
- **Purpose**: Loading skeleton
- **Features**: Animated, customizable
- **Claude Code Note**: For loading states

##### 📄 `separator.tsx`
- **Purpose**: Visual separator
- **Features**: Horizontal/vertical, customizable
- **Claude Code Note**: For visual organization

##### 📄 `avatar.tsx`
- **Purpose**: User avatar component
- **Features**: Image fallback, initials
- **Claude Code Note**: For user profile display

##### 📄 `badge.tsx`
- **Purpose**: Status/label component
- **Variants**: default, secondary, destructive, outline
- **Claude Code Note**: For small status indicators

##### 📄 `dropdown-menu.tsx`
- **Purpose**: Dropdown menu
- **Features**: Radix UI DropdownMenu, accessible
- **Claude Code Note**: For context menus

##### 📄 `index.ts`
- **Purpose**: Centralized exports
- **Features**: All UI components exported
- **Claude Code Note**: Single import point for all UI components

#### 📁 `features/` - Feature-Specific Components
**Purpose**: Complex components for specific application features

##### 📄 `document-upload.tsx`
- **Purpose**: Document upload interface
- **Key Features**:
  - Drag-and-drop file upload
  - Progress tracking
  - File validation
  - Error handling
  - Multiple file support
- **Claude Code Note**: Handles all document ingestion workflows

##### 📄 `knowledge-base-search.tsx`
- **Purpose**: Knowledge base search interface
- **Key Features**:
  - Debounced search
  - Advanced filtering
  - Multi-tab results
  - Real-time updates
  - Export functionality
- **Claude Code Note**: Main interface for querying processed documents

##### 📄 `processing-queue.tsx`
- **Purpose**: Document processing monitoring
- **Key Features**:
  - Real-time queue status
  - Processing statistics
  - Task management
  - Error handling
  - Retry functionality
- **Claude Code Note**: Monitors AI processing workflows

##### 📄 `validation-tasks.tsx`
- **Purpose**: Human-in-the-loop validation
- **Key Features**:
  - Validation queue
  - Task assignment
  - Review interface
  - Approval workflow
  - Quality metrics
- **Claude Code Note**: Manages human validation workflows

##### 📄 `index.ts`
- **Purpose**: Feature components exports
- **Features**: All feature components exported
- **Claude Code Note**: Single import point for feature components

---

## 🪝 Custom Hooks

### 📁 `hooks/` - Custom React Hooks
**Purpose**: Reusable logic and state management

#### 📄 `use-debounce.ts`
- **Purpose**: Debounce values for performance
- **Usage**: Search inputs, API calls
- **Claude Code Note**: Optimizes performance by delaying updates

---

## 🛠️ Utilities and Services

### 📁 `lib/` - Utility Functions and Services
**Purpose**: Shared utilities and API client

#### 📄 `utils.ts`
- **Purpose**: General utility functions
- **Key Functions**:
  - `cn()` - Class name merging
  - `formatBytes()` - File size formatting
  - `formatDate()` - Date formatting
  - `debounce()` - Debounce function
  - `throttle()` - Throttle function
  - File validation helpers
  - Text manipulation helpers
- **Claude Code Note**: Contains all shared utility functions

#### 📄 `api.ts`
- **Purpose**: API client for backend communication
- **Key Features**:
  - Authentication endpoints
  - Document management
  - Knowledge base operations
  - Processing queue management
  - Validation tasks
  - Error handling
  - Request/response interceptors
- **Claude Code Note**: Centralized API communication layer

---

## 📝 Type Definitions

### 📁 `types/` - TypeScript Interfaces
**Purpose**: Type safety and data structure definitions

#### 📄 `auth.ts`
- **Purpose**: Authentication-related types
- **Key Interfaces**:
  - User, UserRole, UserPreferences
  - LoginCredentials, RegisterCredentials
  - AuthResponse, Session
  - Permissions and roles
- **Claude Code Note**: All authentication data structures

#### 📄 `document.ts`
- **Purpose**: Document processing types
- **Key Interfaces**:
  - Document, DocumentStatus, DocumentType
  - ExtractedData, ProcessingResults
  - QualityMetrics, AIInsights
  - Upload/update requests
- **Claude Code Note**: Complete document processing data model

#### 📄 `validation.ts`
- **Purpose**: Validation workflow types
- **Key Interfaces**:
  - ValidationTask, ValidationStatus
  - ValidationResult, ValidationQueue
  - Assignment and submission requests
- **Claude Code Note**: Human-in-the-loop validation data model

---

## ⚙️ Configuration Files

### 📄 `package.json`
- **Purpose**: Project dependencies and scripts
- **Key Dependencies**:
  - Next.js 14, React 18, TypeScript
  - Tailwind CSS, Framer Motion
  - Zustand, React Query, SWR
  - Radix UI, Headless UI
  - React Hook Form, Zod
  - Socket.io Client, NextAuth.js
- **Scripts**: dev, build, start, lint, test, storybook
- **Claude Code Note**: All necessary dependencies for the application

### 📄 `tsconfig.json`
- **Purpose**: TypeScript configuration
- **Key Features**:
  - Path aliases (@/ for src)
  - Strict type checking
  - Modern JavaScript features
- **Claude Code Note**: TypeScript compiler settings

### 📄 `tailwind.config.js`
- **Purpose**: Tailwind CSS configuration
- **Key Features**:
  - Custom color palette
  - Custom fonts and animations
  - Plugin configurations
  - Dark mode support
- **Claude Code Note**: All styling configuration

### 📄 `next.config.js`
- **Purpose**: Next.js configuration
- **Key Features**:
  - App Router enabled
  - Image optimization
  - API routes configuration
  - Environment variables
- **Claude Code Note**: Next.js build and runtime settings

### 📄 `postcss.config.js`
- **Purpose**: PostCSS configuration
- **Features**: Tailwind CSS and Autoprefixer
- **Claude Code Note**: CSS processing pipeline

### 📄 `.eslintrc.json`
- **Purpose**: ESLint configuration
- **Features**: TypeScript rules, Next.js rules
- **Claude Code Note**: Code quality and consistency

### 📄 `.prettierrc`
- **Purpose**: Prettier configuration
- **Features**: Code formatting rules
- **Claude Code Note**: Consistent code style

### 📄 `.gitignore`
- **Purpose**: Git ignore patterns
- **Features**: Node modules, build files, environment files
- **Claude Code Note**: Version control exclusions

---

## 📚 Documentation

### 📄 `README.md`
- **Purpose**: Project documentation
- **Key Sections**:
  - Project overview
  - Installation instructions
  - Environment setup
  - Development workflow
  - Deployment guide
- **Claude Code Note**: Complete project documentation

### 📄 `FRONTEND_IMPLEMENTATION_SUMMARY.md`
- **Purpose**: Detailed implementation summary
- **Key Sections**:
  - Architecture overview
  - Component breakdown
  - Technical features
  - Claude Code readiness
- **Claude Code Note**: Comprehensive implementation guide

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Git

### Installation
```bash
cd frontend
npm install
```

### Environment Setup
Copy `.env.example` to `.env.local` and configure:
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_WS_URL` - WebSocket URL
- `NEXTAUTH_SECRET` - Authentication secret
- `NEXTAUTH_URL` - Application URL

### Development
```bash
npm run dev
```

### Build
```bash
npm run build
npm start
```

---

## 🎯 Claude Code Implementation Notes

### Key Implementation Points:
1. **Component Architecture**: All components follow atomic design principles
2. **Type Safety**: Comprehensive TypeScript interfaces for all data
3. **State Management**: Context providers for global state
4. **Real-time Features**: WebSocket integration for live updates
5. **Performance**: Debouncing, lazy loading, optimization
6. **Accessibility**: WCAG 2.1 AA compliance throughout
7. **Error Handling**: Comprehensive error boundaries and user feedback

### Development Workflow:
1. Start with UI components in `components/ui/`
2. Build feature components in `components/features/`
3. Create pages in `app/` directory
4. Add types in `types/` directory
5. Implement utilities in `lib/` directory
6. Test with Jest and React Testing Library

### Integration Points:
- **Backend API**: Use `lib/api.ts` for all API calls
- **Real-time**: Use `useWebSocket` hook for live updates
- **Authentication**: Use `useAuth` hook for user management
- **Theming**: Use `useTheme` hook for dark/light mode

---

## 🔧 Customization Guide

### Adding New Features:
1. Create types in `types/` directory
2. Add API methods in `lib/api.ts`
3. Create feature component in `components/features/`
4. Add page in `app/dashboard/`
5. Update navigation in `app/dashboard/layout.tsx`

### Styling:
- Use Tailwind CSS classes
- Follow design system in `tailwind.config.js`
- Use CSS variables for theming
- Maintain accessibility standards

### State Management:
- Use React Context for global state
- Use React Query for server state
- Use local state for component-specific data
- Follow React 18 patterns

---

This scaffold provides a complete, production-ready foundation for the Intelligent Document Processing & Knowledge Base frontend application. All components are designed to work together seamlessly and follow modern React and Next.js best practices.

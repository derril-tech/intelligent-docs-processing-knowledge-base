# Frontend - Intelligent Docs Processing Knowledge Base

## Overview
Next.js 14 frontend application with TypeScript, Tailwind CSS, and modern React patterns.

## Tech Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Custom component library
- **State Management**: React Context + Hooks
- **Authentication**: Custom auth provider
- **Real-time**: WebSocket provider

## Quick Start

### Prerequisites
- Node.js 18.17.0+ (see .nvmrc)
- npm or pnpm

### Installation
```bash
cd frontend
npm install
```

### Development
```bash
npm run dev
```
The application will be available at http://localhost:3000

### Build
```bash
npm run build
npm start
```

### Environment Variables
Copy `env.example` to `.env.local` and configure:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Authentication routes
│   ├── dashboard/         # Dashboard routes
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable components
│   ├── features/          # Feature-specific components
│   └── ui/               # Base UI components
├── hooks/                # Custom React hooks
├── lib/                  # Utility libraries
├── types/                # TypeScript type definitions
└── providers/            # Context providers
```

## Key Features

### Authentication
- Login/Register pages
- Protected routes
- Auth context provider

### Dashboard
- Document management
- Processing queue monitoring
- Knowledge base search
- Validation tasks

### Real-time Updates
- WebSocket integration for live updates
- Processing status notifications
- Queue monitoring

## Development Guidelines

### Component Structure
- Use TypeScript for all components
- Follow the component hierarchy: UI → Features → Pages
- Implement proper error boundaries
- Use loading states and skeletons

### Styling
- Use Tailwind CSS utility classes
- Follow design system tokens
- Ensure responsive design
- Maintain accessibility standards

### State Management
- Use React Context for global state
- Prefer local state for component-specific data
- Implement proper loading and error states

## Testing
```bash
npm run test
npm run test:watch
```

## Linting and Formatting
```bash
npm run lint
npm run format
```

## Deployment
The application is containerized and can be deployed using Docker:
```bash
docker build -t frontend .
docker run -p 3000:3000 frontend
```

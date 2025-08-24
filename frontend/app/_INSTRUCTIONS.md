# Frontend App Directory Instructions

## CLAUDE_TASK: Next.js App Router Development

This directory contains the Next.js 14+ app router structure. Follow these guidelines:

### Directory Structure
- `page.tsx` - Main landing page
- `layout.tsx` - Root layout with providers and global styles
- `globals.css` - Global CSS with Tailwind directives
- `dashboard/` - Protected dashboard routes
- `(auth)/` - Authentication-related pages (grouped route)
- `providers/` - React context providers

### Development Rules
1. **App Router**: Use Next.js 14+ app router patterns
2. **TypeScript**: All files must be TypeScript with strict typing
3. **Server Components**: Default to server components, use 'use client' only when needed
4. **Styling**: Use Tailwind CSS with design tokens from `packages/ui/tokens.ts`
5. **State Management**: Use Zustand for global state, TanStack Query for server state
6. **Error Handling**: Implement error boundaries and loading states

### TODO Markers
- Add authentication state management
- Implement analytics tracking
- Add loading states and error boundaries
- Replace mock data with actual API calls

### Safe to Edit
- ✅ All `.tsx` files in this directory
- ✅ `globals.css` (follow design tokens)
- ❌ `layout.tsx` (core structure - minimal changes only)

### Integration Points
- API calls to `/api/v1/*` endpoints
- Authentication via NextAuth.js
- Real-time updates via Socket.IO
- File uploads via FilePond

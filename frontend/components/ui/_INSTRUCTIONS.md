# UI Components Directory Instructions

## CLAUDE_TASK: Reusable UI Component Development

This directory contains reusable UI components built with Radix UI and shadcn/ui patterns.

### Component Guidelines
1. **Radix UI**: Use Radix UI primitives as base components
2. **shadcn/ui**: Follow shadcn/ui patterns and styling
3. **TypeScript**: All components must be fully typed
4. **Accessibility**: Implement ARIA labels and keyboard navigation
5. **Design Tokens**: Use tokens from `packages/ui/tokens.ts` (no hard-coded colors)
6. **Variants**: Use `class-variance-authority` for component variants

### Component Structure
```typescript
// Example component structure
import { cn } from "@/lib/utils"
import { cva, type VariantProps } from "class-variance-authority"

const componentVariants = cva(
  "base-classes",
  {
    variants: {
      variant: {
        default: "default-classes",
        secondary: "secondary-classes",
      },
      size: {
        default: "default-size",
        sm: "small-size",
        lg: "large-size",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

interface ComponentProps extends VariantProps<typeof componentVariants> {
  // Component props
}

export const Component = ({ className, variant, size, ...props }: ComponentProps) => {
  return (
    <div className={cn(componentVariants({ variant, size, className }))} {...props}>
      {/* Component content */}
    </div>
  )
}
```

### Required Components
- Button (with variants: default, secondary, outline, ghost, link)
- Input (text, email, password, textarea)
- Card (with header, content, footer)
- Dialog (modal, drawer)
- Dropdown Menu
- Form components (with react-hook-form integration)
- Loading states (spinner, skeleton)
- Toast notifications
- Data display (table, list, grid)

### Safe to Edit
- ✅ All component files in this directory
- ✅ Component variants and props
- ❌ Core Radix UI primitives (import only)

### Integration Points
- Design tokens from `packages/ui/tokens.ts`
- Utility functions from `lib/utils.ts`
- Form validation with react-hook-form + zod
- Theme integration for dark/light mode

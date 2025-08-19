# Intelligent Document Processing & Knowledge Base - Frontend

A modern, responsive React application built with Next.js 14 for intelligent document processing and knowledge management.

## 🚀 Features

- **Modern UI/UX**: Built with Tailwind CSS and Framer Motion
- **Real-time Updates**: WebSocket integration for live document processing
- **File Upload**: Drag-and-drop file upload with progress tracking
- **Document Viewer**: Advanced PDF and document viewing capabilities
- **Search & Filter**: Powerful search with autocomplete and filtering
- **Dark/Light Mode**: Theme switching with system preference detection
- **Responsive Design**: Mobile-first approach with touch-friendly interfaces
- **Accessibility**: WCAG 2.1 AA compliant components
- **Type Safety**: Full TypeScript implementation

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5.0+
- **Styling**: Tailwind CSS 3.3+
- **State Management**: Zustand + React Query
- **UI Components**: Radix UI + Headless UI
- **Animations**: Framer Motion
- **Forms**: React Hook Form + Zod
- **File Handling**: React Dropzone + FilePond
- **Real-time**: Socket.io Client
- **Authentication**: NextAuth.js

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the root directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Authentication
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key

# AI Services
NEXT_PUBLIC_OPENAI_API_KEY=your-openai-key
NEXT_PUBLIC_ANTHROPIC_API_KEY=your-anthropic-key

# File Storage
NEXT_PUBLIC_S3_BUCKET=your-bucket-name
NEXT_PUBLIC_S3_REGION=us-east-1
```

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Authentication pages
│   ├── dashboard/         # Main application pages
│   ├── api/              # API routes
│   └── providers/        # Context providers
├── components/           # Reusable components
│   ├── ui/              # Base UI components
│   ├── layout/          # Layout components
│   ├── documents/       # Document-specific components
│   └── forms/           # Form components
├── hooks/               # Custom React hooks
├── lib/                 # Utility functions
├── store/               # State management
├── types/               # TypeScript type definitions
└── styles/              # Global styles
```

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## 📚 Storybook

```bash
# Start Storybook
npm run storybook

# Build Storybook
npm run build-storybook
```

## 🚀 Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Configure environment variables in Vercel dashboard
4. Deploy automatically on push

### Manual Deployment

```bash
# Build the application
npm run build

# Start production server
npm start
```

## 🔍 Code Quality

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Type checking
npm run type-check
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the component library in Storybook

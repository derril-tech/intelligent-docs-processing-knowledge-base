#!/bin/bash

# Development Environment Startup Script
# This script starts both the backend and frontend development servers

set -e  # Exit on any error

echo "🚀 Starting Intelligent Document Processing Development Environment"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed"
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_warning "Docker is not installed. Using local services instead."
        USE_DOCKER=false
    else
        USE_DOCKER=true
    fi
    
    print_success "Dependencies check completed"
}

# Setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        if [ -f env.example ]; then
            print_status "Creating .env file from env.example..."
            cp env.example .env
            print_warning "Please update .env file with your configuration"
        else
            print_error "No .env or env.example file found"
            exit 1
        fi
    fi
    
    # Check if frontend .env exists
    if [ ! -f frontend/.env.local ]; then
        print_status "Creating frontend .env.local file..."
        cat > frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
EOF
    fi
    
    print_success "Environment setup completed"
}

# Start database and Redis
start_services() {
    print_status "Starting database and Redis services..."
    
    if [ "$USE_DOCKER" = true ]; then
        # Start services with Docker Compose
        if docker-compose up -d postgres redis; then
            print_success "Database and Redis started with Docker"
        else
            print_error "Failed to start services with Docker"
            exit 1
        fi
    else
        print_warning "Docker not available. Please ensure PostgreSQL and Redis are running locally."
        print_status "You can start them manually or install Docker for automatic service management."
    fi
}

# Install backend dependencies
setup_backend() {
    print_status "Setting up backend..."
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Run database migrations
    print_status "Running database migrations..."
    alembic upgrade head
    
    print_success "Backend setup completed"
}

# Install frontend dependencies
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    cd ..
    
    print_success "Frontend setup completed"
}

# Start backend server
start_backend() {
    print_status "Starting backend server..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Start FastAPI server
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    print_success "Backend server started (PID: $BACKEND_PID)"
}

# Start frontend server
start_frontend() {
    print_status "Starting frontend server..."
    
    cd frontend
    
    # Start Next.js development server
    npm run dev &
    FRONTEND_PID=$!
    
    cd ..
    
    print_success "Frontend server started (PID: $FRONTEND_PID)"
}

# Start Celery worker
start_celery() {
    print_status "Starting Celery worker..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Start Celery worker
    celery -A app.core.celery worker --loglevel=info &
    CELERY_PID=$!
    
    print_success "Celery worker started (PID: $CELERY_PID)"
}

# Cleanup function
cleanup() {
    print_status "Shutting down development environment..."
    
    # Kill background processes
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$CELERY_PID" ]; then
        kill $CELERY_PID 2>/dev/null || true
    fi
    
    print_success "Development environment stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo "=========================================="
    echo "Intelligent Document Processing"
    echo "Development Environment Startup"
    echo "=========================================="
    echo ""
    
    # Check dependencies
    check_dependencies
    
    # Setup environment
    setup_environment
    
    # Start services
    start_services
    
    # Setup applications
    setup_backend
    setup_frontend
    
    # Start servers
    start_backend
    start_celery
    start_frontend
    
    echo ""
    echo "=========================================="
    print_success "Development environment is ready!"
    echo "=========================================="
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo "📊 Admin Panel: http://localhost:8000/admin"
    echo ""
    echo "Press Ctrl+C to stop all services"
    echo ""
    
    # Wait for user to stop
    wait
}

# Run main function
main

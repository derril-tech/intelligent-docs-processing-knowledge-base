#!/bin/bash

# DocuMind™ Development Environment Startup Script
# This script starts the complete development environment

set -e

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is available
port_available() {
    ! nc -z localhost $1 2>/dev/null
}

# Function to wait for service to be ready
wait_for_service() {
    local service=$1
    local port=$2
    local max_attempts=30
    local attempt=1
    
    print_status "Waiting for $service to be ready on port $port..."
    
    while [ $attempt -le $max_attempts ]; do
        if nc -z localhost $port 2>/dev/null; then
            print_success "$service is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service failed to start within $((max_attempts * 2)) seconds"
    return 1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check for Docker
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check for Docker Compose
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check for Node.js
    if ! command_exists node; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    # Check for pnpm
    if ! command_exists pnpm; then
        print_warning "pnpm is not installed. Installing pnpm..."
        npm install -g pnpm
    fi
    
    # Check for Python
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    print_success "All prerequisites are satisfied!"
}

# Function to setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    # Copy environment files if they don't exist
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_warning "Created .env from .env.example. Please update with your configuration."
        else
            print_error ".env.example not found. Please create a .env file."
            exit 1
        fi
    fi
    
    if [ ! -f frontend/.env.local ]; then
        if [ -f frontend/env.example ]; then
            cp frontend/env.example frontend/.env.local
            print_warning "Created frontend/.env.local from env.example."
        fi
    fi
    
    print_success "Environment setup complete!"
}

# Function to start infrastructure services
start_infrastructure() {
    print_status "Starting infrastructure services..."
    
    # Start PostgreSQL, Redis, and Elasticsearch
    docker-compose up -d postgres redis elasticsearch
    
    # Wait for services to be ready
    wait_for_service "PostgreSQL" 5432
    wait_for_service "Redis" 6379
    wait_for_service "Elasticsearch" 9200
    
    print_success "Infrastructure services are running!"
}

# Function to setup database
setup_database() {
    print_status "Setting up database..."
    
    # Run database migrations
    cd app
    python -m alembic upgrade head
    cd ..
    
    # Seed sample data
    cd app
    python scripts/seed_tenant_data.py
    cd ..
    
    print_success "Database setup complete!"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Install backend dependencies
    cd app
    pip install -r requirements.txt
    cd ..
    
    # Install frontend dependencies
    cd frontend
    pnpm install
    cd ..
    
    # Install shared types
    cd packages/types
    pnpm install
    pnpm build
    cd ../..
    
    print_success "Dependencies installed!"
}

# Function to start backend
start_backend() {
    print_status "Starting backend server..."
    
    cd app
    
    # Start FastAPI server
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    cd ..
    
    # Wait for backend to be ready
    wait_for_service "Backend API" 8000
    
    print_success "Backend server is running on http://localhost:8000"
}

# Function to start frontend
start_frontend() {
    print_status "Starting frontend server..."
    
    cd frontend
    
    # Start Next.js development server
    pnpm dev &
    FRONTEND_PID=$!
    
    cd ..
    
    # Wait for frontend to be ready
    wait_for_service "Frontend" 3000
    
    print_success "Frontend server is running on http://localhost:3000"
}

# Function to start Celery workers
start_celery_workers() {
    print_status "Starting Celery workers..."
    
    cd app
    
    # Start Celery worker for document processing
    celery -A app.core.celery worker --loglevel=info --queues=document_processing &
    DOCUMENT_WORKER_PID=$!
    
    # Start Celery worker for AI processing
    celery -A app.core.celery worker --loglevel=info --queues=ai_processing &
    AI_WORKER_PID=$!
    
    # Start Celery worker for validation
    celery -A app.core.celery worker --loglevel=info --queues=validation &
    VALIDATION_WORKER_PID=$!
    
    # Start Celery worker for search
    celery -A app.core.celery worker --loglevel=info --queues=search &
    SEARCH_WORKER_PID=$!
    
    # Start Celery worker for maintenance
    celery -A app.core.celery worker --loglevel=info --queues=maintenance &
    MAINTENANCE_WORKER_PID=$!
    
    cd ..
    
    print_success "Celery workers are running!"
}

# Function to start Celery beat (scheduler)
start_celery_beat() {
    print_status "Starting Celery beat scheduler..."
    
    cd app
    
    # Start Celery beat for scheduled tasks
    celery -A app.core.celery beat --loglevel=info &
    CELERY_BEAT_PID=$!
    
    cd ..
    
    print_success "Celery beat scheduler is running!"
}

# Function to display status
show_status() {
    echo ""
    echo "=========================================="
    echo "DocuMind™ Development Environment Status"
    echo "=========================================="
    echo ""
    echo "🌐 Frontend:     http://localhost:3000"
    echo "🔧 Backend API:  http://localhost:8000"
    echo "📊 API Docs:     http://localhost:8000/docs"
    echo "🗄️  PostgreSQL:   localhost:5432"
    echo "🔴 Redis:        localhost:6379"
    echo "🔍 Elasticsearch: localhost:9200"
    echo ""
    echo "Process IDs:"
    echo "  Backend:       $BACKEND_PID"
    echo "  Frontend:      $FRONTEND_PID"
    echo "  Document Worker: $DOCUMENT_WORKER_PID"
    echo "  AI Worker:     $AI_WORKER_PID"
    echo "  Validation Worker: $VALIDATION_WORKER_PID"
    echo "  Search Worker: $SEARCH_WORKER_PID"
    echo "  Maintenance Worker: $MAINTENANCE_WORKER_PID"
    echo "  Celery Beat:   $CELERY_BEAT_PID"
    echo ""
    echo "To stop all services, run: ./scripts/stop-dev.sh"
    echo "=========================================="
}

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down development environment..."
    
    # Kill background processes
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$DOCUMENT_WORKER_PID" ]; then
        kill $DOCUMENT_WORKER_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$AI_WORKER_PID" ]; then
        kill $AI_WORKER_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$VALIDATION_WORKER_PID" ]; then
        kill $VALIDATION_WORKER_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$SEARCH_WORKER_PID" ]; then
        kill $SEARCH_WORKER_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$MAINTENANCE_WORKER_PID" ]; then
        kill $MAINTENANCE_WORKER_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$CELERY_BEAT_PID" ]; then
        kill $CELERY_BEAT_PID 2>/dev/null || true
    fi
    
    print_success "Development environment stopped!"
}

# Set up signal handlers
trap cleanup EXIT INT TERM

# Main execution
main() {
    echo "🚀 Starting DocuMind™ Development Environment"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Setup environment
    setup_environment
    
    # Install dependencies
    install_dependencies
    
    # Start infrastructure
    start_infrastructure
    
    # Setup database
    setup_database
    
    # Start services
    start_backend
    start_frontend
    start_celery_workers
    start_celery_beat
    
    # Show status
    show_status
    
    # Keep script running
    print_status "Development environment is ready! Press Ctrl+C to stop."
    wait
}

# Run main function
main "$@"

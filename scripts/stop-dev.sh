#!/bin/bash

# DocuMind™ Development Environment Stop Script
# This script stops all development services

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

# Function to stop Docker services
stop_docker_services() {
    print_status "Stopping Docker services..."
    
    if command -v docker-compose >/dev/null 2>&1; then
        docker-compose down
        print_success "Docker services stopped!"
    else
        print_warning "Docker Compose not found. Please stop services manually."
    fi
}

# Function to kill processes by port
kill_process_by_port() {
    local port=$1
    local process_name=$2
    
    if lsof -ti:$port >/dev/null 2>&1; then
        print_status "Stopping $process_name on port $port..."
        lsof -ti:$port | xargs kill -9
        print_success "$process_name stopped!"
    else
        print_status "$process_name not running on port $port"
    fi
}

# Function to kill Celery processes
kill_celery_processes() {
    print_status "Stopping Celery processes..."
    
    # Kill Celery workers
    pkill -f "celery.*worker" || true
    pkill -f "celery.*beat" || true
    
    print_success "Celery processes stopped!"
}

# Main execution
main() {
    echo "🛑 Stopping DocuMind™ Development Environment"
    echo ""
    
    # Stop processes by port
    kill_process_by_port 3000 "Frontend"
    kill_process_by_port 8000 "Backend"
    kill_process_by_port 5432 "PostgreSQL"
    kill_process_by_port 6379 "Redis"
    kill_process_by_port 9200 "Elasticsearch"
    
    # Stop Celery processes
    kill_celery_processes
    
    # Stop Docker services
    stop_docker_services
    
    echo ""
    print_success "Development environment stopped successfully!"
}

# Run main function
main "$@"

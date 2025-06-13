#!/bin/bash

# Resume Analyzer Platform Startup Script
# This script provides multiple ways to start the frontend and backend together

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

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to kill processes on specific ports
cleanup_ports() {
    print_status "Cleaning up processes on ports 3000 and 8000..."
    
    if port_in_use 3000; then
        print_warning "Killing process on port 3000"
        lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    fi
    
    if port_in_use 8000; then
        print_warning "Killing process on port 8000"
        lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    fi
    
    sleep 2
}

# Function to start with Docker
start_docker() {
    print_status "Starting Resume Analyzer Platform with Docker..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    cleanup_ports
    
    print_status "Building and starting containers..."
    docker-compose down --remove-orphans 2>/dev/null || true
    docker-compose up --build
}

# Function to start locally
start_local() {
    print_status "Starting Resume Analyzer Platform locally..."
    
    # Check prerequisites
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    if ! command_exists node; then
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
    
    if ! command_exists pnpm; then
        print_warning "pnpm is not installed. Installing pnpm..."
        npm install -g pnpm
    fi
    
    cleanup_ports
    
    # Setup backend
    print_status "Setting up backend..."
    cd job-search-be
    
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    print_status "Activating virtual environment and installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    print_status "Starting backend server..."
    uvicorn main:app --reload --port 8000 &
    BACKEND_PID=$!
    cd ..
    
    # Setup frontend
    print_status "Setting up frontend..."
    cd job-search-fe
    
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        pnpm install
    fi
    
    print_status "Starting frontend server..."
    pnpm dev &
    FRONTEND_PID=$!
    cd ..
    
    # Wait for services to start
    print_status "Waiting for services to start..."
    sleep 5
    
    # Check if services are running
    if port_in_use 8000 && port_in_use 3000; then
        print_success "✅ Both services are running!"
        print_success "📋 Backend API: http://localhost:8000"
        print_success "🌐 Frontend App: http://localhost:3000"
        print_status "Press Ctrl+C to stop both services"
        
        # Wait for user interrupt
        trap "cleanup_local" INT
        wait
    else
        print_error "Failed to start services. Please check the logs above."
        cleanup_local
        exit 1
    fi
}

# Function to cleanup local processes
cleanup_local() {
    print_status "Stopping services..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    cleanup_ports
    print_success "Services stopped successfully"
}

# Function to show help
show_help() {
    echo "Resume Analyzer Platform Startup Script"
    echo ""
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  docker    Start with Docker (recommended for production)"
    echo "  local     Start locally (recommended for development)"
    echo "  dev       Alias for local"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 docker    # Start with Docker"
    echo "  $0 local     # Start locally"
    echo "  $0           # Interactive mode (will ask for preference)"
    echo ""
    echo "Services:"
    echo "  Backend:  http://localhost:8000 (FastAPI)"
    echo "  Frontend: http://localhost:3000 (Nuxt.js)"
}

# Main script logic
main() {
    echo ""
    echo "🚀 Resume Analyzer Platform Startup Script"
    echo "==========================================="
    echo ""
    
    case "${1:-}" in
        "docker")
            start_docker
            ;;
        "local"|"dev")
            start_local
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        "")
            # Interactive mode
            echo "How would you like to start the platform?"
            echo ""
            echo "1) Docker (recommended for quick start)"
            echo "2) Local development (recommended for coding)"
            echo ""
            read -p "Enter your choice (1 or 2): " choice
            
            case $choice in
                1)
                    start_docker
                    ;;
                2)
                    start_local
                    ;;
                *)
                    print_error "Invalid choice. Please run '$0 help' for usage information."
                    exit 1
                    ;;
            esac
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 
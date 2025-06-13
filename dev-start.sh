#!/bin/bash

# Development Setup Script - Hybrid Mode
# Backend: Docker | Frontend: Local

set -e

echo "🚀 Starting Development Environment"
echo "=================================="

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo "❌ Docker is not running. Please start Docker Desktop."
        exit 1
    fi
}

# Function to check if pnpm is installed
check_pnpm() {
    if ! command -v pnpm &> /dev/null; then
        echo "❌ pnpm is not installed. Installing pnpm globally..."
        npm install -g pnpm
    fi
}

# Function to start backend in Docker
start_backend_docker() {
    echo "🐳 Starting backend in Docker..."
    check_docker
    docker-compose up -d backend
    echo "✅ Backend started at http://localhost:8000"
}

# Function to start frontend locally
start_frontend_local() {
    echo "💻 Starting frontend locally..."
    check_pnpm
    cd job-search-fe
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        pnpm install
    fi
    
    echo "🎯 Frontend starting at http://localhost:3000"
    echo "🔗 Connected to backend at http://localhost:8000"
    echo ""
    echo "Press Ctrl+C to stop the frontend"
    pnpm dev:local
}

# Function to stop backend Docker container
stop_backend_docker() {
    echo "🛑 Stopping backend Docker container..."
    docker-compose down
    echo "✅ Backend Docker container stopped"
}

# Function to show logs
show_logs() {
    echo "📋 Backend logs:"
    docker-compose logs -f backend
}

# Function to start hybrid mode (backend Docker, frontend local)
start_hybrid() {
    echo "🔄 Starting Hybrid Development Environment..."
    echo "Backend: Docker (port 8000)"
    echo "Frontend: Local (port 3000)"
    echo ""
    
    start_backend_docker
    start_frontend_local
}

# Function to start both services in Docker
start_docker() {
    echo "🐳 Starting both services in Docker..."
    check_docker
    docker-compose up -d
    echo "✅ Both services started in Docker"
    echo "   Backend: http://localhost:8000"
    echo "   Frontend: http://localhost:3000 (if configured in docker-compose)"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [hybrid|docker|backend|frontend|stop|logs|restart]"
    echo ""
    echo "🚀 Environment Commands:"
    echo "  hybrid    - Start backend in Docker, frontend locally [default]"
    echo "  docker    - Start both services in Docker"
    echo ""
    echo "🔧 Individual Service Commands:"
    echo "  backend   - Start only backend in Docker"
    echo "  frontend  - Start only frontend locally"
    echo ""
    echo "🛠️  Utility Commands:"
    echo "  stop      - Stop all Docker containers"
    echo "  logs      - Show backend Docker logs"
    echo "  restart   - Restart the backend Docker container"
    echo ""
    echo "💡 Examples:"
    echo "  $0          # Hybrid mode (default)"
    echo "  $0 hybrid   # Backend in Docker, frontend locally"
    echo "  $0 docker   # Both services in Docker"
}

# Main execution
case "${1:-hybrid}" in
    "hybrid"|"")
        start_hybrid
        ;;
    "docker")
        start_docker
        ;;
    "backend")
        start_backend_docker
        echo "✅ Backend only started. Run 'cd job-search-fe && pnpm dev:local' to start frontend."
        ;;
    "frontend")
        start_frontend_local
        ;;
    "stop")
        stop_backend_docker
        ;;
    "logs")
        show_logs
        ;;
    "restart")
        stop_backend_docker
        sleep 2
        start_backend_docker
        start_frontend_local
        ;;
    *)
        show_usage
        ;;
esac 
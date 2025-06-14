#!/bin/bash

# Job Search Platform - Microservices Startup Script
# Services: Model Service, Backend API, Frontend

set -e

echo "🚀 Job Search Platform - Microservices Architecture"
echo "=================================================="

# Function to run one-time setup
one_time_setup() {
    echo "🔧 Running one-time setup..."
    
    # Check if model file needs to be extracted
    MODEL_ZIP="services/model-service/custom_model/fine_tuned_mpnet.zip"
    MODEL_TARGET_DIR="services/model-service/model"
    
    if [ -f "$MODEL_ZIP" ] && [ ! -d "$MODEL_TARGET_DIR" ]; then
        echo "📦 Extracting 387MB model file..."
        echo "    Estimated time: 1-3 minutes depending on your system"
        echo "    Please wait, extraction in progress..."
        unzip -q "$MODEL_ZIP" -d "$MODEL_TARGET_DIR" &
        PID=$!
        while kill -0 $PID 2>/dev/null; do
            echo -n "."
            sleep 2
        done
        echo " Done!"
    elif [ -d "$MODEL_TARGET_DIR" ]; then
        echo "✅ Model already extracted, skipping..."
    else
        echo "⚠️  Model zip file not found at $MODEL_ZIP"
        echo "   Continuing without model extraction..."
    fi
    
    echo ""
}

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

# Function to start backend services in Docker
start_backend_services_only() {
    echo "🐳 Starting backend services in Docker..."
    check_docker
    one_time_setup
    
    docker-compose up -d --build
    echo "✅ Backend services started:"
    echo "   Model Service: http://localhost:8001"
    echo "   Backend API: http://localhost:8000"
    echo ""
    echo "💻 To start frontend locally:"
    echo "   cd services/frontend && pnpm install && pnpm dev:local"
}

# Function to start development mode
start_all() {
    echo "🔄 Starting development environment..."
    check_docker
    check_pnpm
    one_time_setup
    
    # Start backend services in Docker
    echo "🐳 Starting backend services with development settings..."
    docker-compose up -d --build
    
    echo "✅ Backend services started:"
    echo "   Model Service: http://localhost:8001"
    echo "   Backend API: http://localhost:8000 (with hot reload)"
    echo ""
    
    # Start frontend locally
    echo "💻 Starting frontend locally..."
    cd services/frontend
    
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        pnpm install
    fi
    
    echo "🎯 Frontend starting at http://localhost:3000"
    echo "🔗 Connected to backend at http://localhost:8000"
    echo "🤖 Model service at http://localhost:8001"
    echo ""
    echo "Press Ctrl+C to stop the frontend (backend will keep running)"
    pnpm dev:local
}

# Function to start only frontend
start_frontend() {
    echo "💻 Starting frontend locally..."
    check_pnpm
    cd services/frontend
    
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        pnpm install
    fi
    
    echo "🎯 Frontend starting at http://localhost:3000"
    echo "🔗 Make sure backend is running at http://localhost:8000"
    pnpm dev:local
}

# Function to stop all services
stop_services() {
    echo "🛑 Stopping all services..."
    docker-compose down
    docker-compose -f docker-compose.dev.yml down
    echo "✅ All services stopped"
}

# Function to show logs
show_logs() {
    echo "📋 Service logs:"
    docker-compose logs -f
}

# Function to show status
show_status() {
    echo "📊 Backend Service Status:"
    echo "========================="
    
    # Check Docker containers
    docker-compose ps
    
    echo ""
    echo "🌐 Access URLs:"
    echo "   Backend API: http://localhost:8000"
    echo "   Model Service: http://localhost:8001"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "💻 Frontend (runs locally):"
    echo "   URL: http://localhost:3000"
    echo "   Start: cd services/frontend && pnpm dev:local"
    
    # Check if frontend is running
    if lsof -i :3000 >/dev/null 2>&1; then
        echo "   Status: ✅ Running"
    else
        echo "   Status: ❌ Not running"
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "🚀 Main Commands:"
    echo "  all         - Start backend services + show frontend instructions [default]"
    echo "  dev         - Start backend services with dev settings + frontend locally"
    echo "  backend     - Start only backend services (Model + API)"
    echo "  frontend    - Start only frontend locally"
    echo ""
    echo "🛠️  Utility Commands:"
    echo "  setup       - Run one-time setup only"
    echo "  stop        - Stop all backend services"
    echo "  restart     - Restart all backend services"
    echo "  logs        - Show backend service logs"
    echo "  status      - Show backend service status"
    echo "  clean       - Clean up Docker resources"
    echo ""
    echo "💡 Examples:"
    echo "  $0          # Start backend services (frontend runs locally)"
    echo "  $0 dev      # Development mode with hot reload"
    echo "  $0 backend  # Backend services only"
    echo "  $0 frontend # Frontend only"
    echo ""
    echo "📝 Note: Frontend always runs locally for better development experience"
}

# Function to clean up Docker resources
clean_docker() {
    echo "🧹 Cleaning up Docker resources..."
    docker-compose down --remove-orphans
    docker system prune -f
    echo "✅ Docker cleanup completed"
}

# Main execution
case "${1:-all}" in
    "all")
        start_all
        ;;
    "frontend")
        start_frontend
        ;;
    "setup")
        one_time_setup
        echo "✅ One-time setup completed!"
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        stop_services
        sleep 2
        start_backend_services_only
        ;;
    "logs")
        show_logs
        ;;
    "status")
        show_status
        ;;
    "clean")
        clean_docker
        ;;
    "usage")
        show_usage
        ;;
    "*")
        start_all
        ;;
esac 
# Development Guide - Hybrid Setup

This setup runs the **backend in Docker** and the **frontend locally** for optimal development experience.

## Prerequisites

- **Docker Desktop** - For backend containerization
- **Node.js 18+** and **pnpm** - For frontend development
- **Google API Key** - For AI resume analysis

## Quick Start

### 1. Setup Environment

```bash
# Copy and configure backend environment
cp job-search-be/.env_template job-search-be/.env
# Edit job-search-be/.env and add your Google API key from:
# https://aistudio.google.com/app/apikey
```

### 2. Start Development Environment

```bash
# Option 1: Use the automated script (recommended)
./dev-start.sh

# Option 2: Manual setup
# Terminal 1 - Start backend in Docker
docker-compose up -d backend

# Terminal 2 - Start frontend locally
cd job-search-fe
pnpm install  # Only needed first time
pnpm dev:local
```

## Access Points

- **Frontend**: http://localhost:3000 (local)
- **Backend**: http://localhost:8000 (Docker)
- **API Docs**: http://localhost:8000/docs

## Development Commands

```bash
# Start everything
./dev-start.sh

# Start only backend (Docker)
./dev-start.sh backend

# Start only frontend (local)
./dev-start.sh frontend

# Stop backend
./dev-start.sh stop

# View backend logs
./dev-start.sh logs

# Restart backend
./dev-start.sh restart
```

## Benefits of Hybrid Setup

### ✅ Advantages
- **Fast frontend hot reload** - No Docker overhead
- **Native Node.js performance** - Direct file system access
- **Easy debugging** - Native browser dev tools
- **Quick dependency updates** - Direct npm/pnpm usage
- **Backend isolation** - Consistent environment in Docker

### 📁 File Structure
```
resume-analyzer-platform/
├── dev-start.sh              # Hybrid development script
├── docker-compose.yml        # Backend-only Docker config
├── job-search-be/           # Backend (Docker)
│   ├── Dockerfile
│   └── .env                 # Your API key here
└── job-search-fe/           # Frontend (Local)
    ├── package.json         # Updated with local dev scripts
    └── nuxt.config.ts       # Pre-configured for localhost:8000
```

## Troubleshooting

### Frontend can't connect to backend
- Ensure backend is running: `docker-compose ps`
- Check backend logs: `./dev-start.sh logs`
- Verify API URL in frontend: Should be `http://localhost:8000`

### Port conflicts
- Backend uses port 8000
- Frontend uses port 3000
- Make sure these ports are available

### Docker issues
- Restart Docker Desktop
- Clean up: `docker system prune -f`
- Rebuild: `docker-compose up --build -d backend`

## Environment Variables

### Backend (.env in job-search-be/)
```env
GOOGLE_API_KEY=your_actual_api_key_here
PYTHONPATH=.
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
```

### Frontend (Automatic)
The frontend automatically connects to `http://localhost:8000` when using `pnpm dev:local`. 
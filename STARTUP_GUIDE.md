# 🚀 Job Search Platform - Quick Start Guide

## Overview

The **Job Search Platform** is an AI-powered monorepo application for resume analysis and job searching:

- **Backend** (`job-search-be/`): FastAPI (Python) - AI analysis, resume parsing, API endpoints
- **Frontend** (`job-search-fe/`): Nuxt.js 3 (Vue.js) - Modern web interface, file upload, results display
- **Infrastructure**: Docker, unified scripts, monorepo management

## 📋 Prerequisites

Ensure you have these installed:
- **Node.js 18+** and **pnpm** (frontend)
- **Python 3.8+** and **pip** (backend)
- **Docker & Docker Compose** (containerized deployment)
- **Git** (version control)
- **Google API Key** for AI resume analysis (required)

## 🚀 Startup Methods

### ⚠️ IMPORTANT: Setup Google API Key First

**Before starting the application**, you must configure your Google API key for AI resume analysis:

```bash
# Step 1: Copy the environment template
cp job-search-be/.env_template job-search-be/.env

# Step 2: Get your Google API key
# Visit: https://aistudio.google.com/app/apikey
# Create a new API key and copy it

# Step 3: Edit the .env file
# Open job-search-be/.env and replace 'your_google_api_key_here' with your actual API key
```

**Quick Setup Example:**
```bash
# Edit the .env file (use your preferred editor)
nano job-search-be/.env
# or
code job-search-be/.env
# or
vim job-search-be/.env

# Make sure it looks like this:
# GOOGLE_API_KEY=your_actual_api_key_from_google
```

### 🌟 Method 1: Automated Scripts (Recommended)

**Linux/macOS:**
```bash
./start.sh                 # Interactive mode (asks Docker/local)
./start.sh docker          # Docker deployment
./start.sh local           # Local development with hot reload
./start.sh help            # Show all options
```

**Windows:**
```cmd
start.bat                  # Interactive mode
start.bat docker           # Docker deployment
start.bat local            # Local development
start.bat help             # Show options
```

**Features:**
- ✅ Automatic prerequisite checks
- ✅ Virtual environment setup
- ✅ Dependency installation
- ✅ Port conflict resolution
- ✅ Graceful shutdown (Ctrl+C)
- ✅ Error handling and logging

### Method 2: NPM Scripts (Workspace)

```bash
# One-time setup
npm install                 # Install root dependencies

# Start development
npm run dev                # Start both services together
npm start                  # Alternative start command

# Docker commands
npm run docker:up          # Deploy with Docker
npm run docker:down        # Stop Docker services
npm run docker:logs        # View Docker logs

# Maintenance
npm run install:all        # Install all dependencies
npm run clean             # Clean build artifacts
```

### Method 3: Docker Compose

```bash
# Start with Docker (production-like)
docker-compose up --build

# Background deployment
docker-compose up -d --build

# Stop all services
docker-compose down

# View logs
docker-compose logs -f
```

### Method 4: Manual Development

**Terminal 1 - Backend:**
```bash
cd job-search-be

# IMPORTANT: Setup .env file first (if not done already)
cp .env_template .env
# Edit .env file with your Google API key

python -m venv venv

# Activate virtual environment
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd job-search-fe
pnpm install
pnpm dev
```

## 🌐 Access URLs

Once running, access the platform at:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application interface |
| **Backend API** | http://localhost:8000 | API endpoints |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |

## 🛠 Development Workflow

### Quick Development
```bash
# Start everything with hot reload
./start.sh local

# Edit files in either directory:
# - job-search-fe/ (frontend changes reload automatically)
# - job-search-be/ (backend restarts on file changes)
```

### Production Testing
```bash
# Test with Docker containers
./start.sh docker

# Or use Docker Compose directly
docker-compose up --build
```

### Switching Between Modes
```bash
# Stop current services (Ctrl+C or)
./start.sh stop

# Start in different mode
./start.sh [docker|local]
```

## 🔧 Troubleshooting

### Common Issues & Solutions

**1. Google API Key Issues**
```bash
# Error: "GOOGLE_API_KEY not found"
# Solution: Ensure .env file exists and contains valid API key
ls job-search-be/.env              # Check if file exists
cat job-search-be/.env             # Verify API key is set

# If missing, copy template and edit:
cp job-search-be/.env_template job-search-be/.env
# Then edit with your actual API key from: https://aistudio.google.com/app/apikey
```

**2. Port Already in Use**
```bash
# Scripts auto-kill processes, but manual option:
lsof -ti:3000,8000 | xargs kill -9
```

**3. Python Virtual Environment Issues**
```bash
cd job-search-be
rm -rf venv                    # Delete existing
python -m venv venv           # Recreate
# Re-run startup script
```

**4. Node Dependencies Issues**
```bash
cd job-search-fe
rm -rf node_modules           # Delete modules
pnpm install                  # Reinstall
```

**5. Docker Problems**
```bash
# Clean up Docker
docker-compose down --remove-orphans
docker system prune -f

# Rebuild from scratch
docker-compose up --build --force-recreate
```

**6. Git Issues (Monorepo)**
```bash
# If submodule errors persist
git submodule deinit --all
rm -rf .git/modules
# Repository is now pure monorepo
```

### Debugging & Logs

**Local Development:**
- Check terminal outputs for errors
- Frontend: Browser dev tools + terminal
- Backend: FastAPI auto-reload logs

**Docker Mode:**
```bash
# View all logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f frontend
docker-compose logs -f backend

# Debug container
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 📁 Project Structure

```
job-search-platform/          # Monorepo root
├── .git/                    # Unified Git repository
├── .gitignore              # Monorepo ignore rules
├── package.json            # Root workspace scripts
├── docker-compose.yml      # Container orchestration
├── start.sh/.bat           # Cross-platform startup
├── README.md              # Complete documentation
├── STARTUP_GUIDE.md       # This quick start guide
│
├── job-search-be/         # Backend Service
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   ├── .env_template     # Environment variables template
│   ├── .env             # Environment variables (created from template)
│   ├── Dockerfile       # Backend container
│   ├── venv/           # Virtual environment (created)
│   └── README.md       # Backend-specific docs
│
└── job-search-fe/        # Frontend Service
    ├── pages/           # Nuxt.js pages
    ├── components/      # Vue components
    ├── package.json     # Frontend dependencies
    ├── nuxt.config.ts   # Nuxt configuration
    ├── Dockerfile      # Frontend container
    ├── node_modules/   # NPM packages (created)
    └── README.md       # Frontend-specific docs
```

## 🎯 Usage Flow

1. **Start Platform**: Choose any method above
2. **Open Browser**: Navigate to http://localhost:3000
3. **Upload Resume**: Drop PDF/DOC/DOCX file (max 10MB)
4. **Parse Content**: Extract resume sections automatically
5. **Analyze Resume**: Get AI-powered insights and recommendations
6. **Review Results**: Check completeness score and suggestions
7. **Export Data**: Download analysis as JSON if needed
8. **Iterate**: Upload different resumes or make improvements

## 🛡 Best Practices

### Development
- **Use `./start.sh local`** for active development (hot reload)
- **Use `./start.sh docker`** for production testing
- **Keep dependencies updated** in both package.json files
- **Test in both modes** before committing changes

### Production
- **Use Docker Compose** for consistent deployments
- **Set environment variables** appropriately
- **Monitor logs** for performance insights
- **Scale services** independently as needed

### Maintenance
```bash
# Regular cleanup
npm run clean               # Clean build artifacts
docker system prune        # Clean Docker cache
git log --oneline          # Check commit history

# Dependency updates
cd job-search-fe && pnpm update
cd job-search-be && pip list --outdated
```

## 📞 Getting Help

**If you encounter issues:**

1. **Check this guide first** - covers 90% of common problems
2. **Run diagnostics**: `./start.sh help` shows script options
3. **Check logs**: Use appropriate logging method for your setup
4. **Review main README**: See [README.md](./README.md) for comprehensive docs
5. **Verify setup**: Ensure all prerequisites are installed correctly

**Quick diagnostics:**
```bash
# Check versions
node --version && python --version && docker --version

# Check ports
lsof -i :3000,8000

# Check processes
ps aux | grep -E "(node|python|uvicorn)"
```

---

**Happy developing! 🎉 Need help? Check the logs and try different startup methods.** 
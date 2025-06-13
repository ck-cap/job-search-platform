# Resume Analysis Platform

A modern AI-powered resume analysis platform with intelligent parsing capabilities. Built as a monorepo with FastAPI backend and Nuxt.js frontend.

## 🌟 Features

- **Resume Analysis**: AI-powered resume parsing and improvement suggestions using Google Gemini
- **File Upload Support**: PDF, DOC, DOCX formats (max 10MB)
- **Intelligent Parsing**: Automatic section extraction and organization
- **Multimodal Processing**: Direct PDF analysis and DOCX-to-PDF conversion
- **Structured Output**: JSON-formatted resume data with summaries
- **Modern UI**: Responsive interface with real-time feedback
- **Hybrid Development**: Optimized development workflow with Docker backend and local frontend

## 🛠 Tech Stack

### Backend (`job-search-be/`)
- **FastAPI**: Modern Python web framework
- **Python 3.8+**: Core language
- **Google Generative AI**: Gemini-1.5-flash for multimodal parsing
- **LibreOffice**: DOCX-to-PDF conversion in Docker
- **Uvicorn**: ASGI server

### Frontend (`job-search-fe/`)
- **Nuxt.js 3**: Vue.js framework with SSR
- **Vue 3**: Progressive JavaScript framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Shadcn/ui**: Component library via reka-ui

### Infrastructure
- **Docker**: Containerized backend deployment
- **pnpm**: Package management
- **Git**: Version control (monorepo)

## 📋 Prerequisites

- **Node.js** v18+ and **pnpm**
- **Python** v3.8+ and **pip**
- **Docker** & **Docker Compose** (for backend)
- **Git** for version control
- **Google API Key** for AI resume analysis (required)

## 🚀 Quick Start

### ⚠️ Important: Setup Google API Key First

Before starting the application, you must configure your Google API key:

```bash
# 1. Copy the environment template
cp job-search-be/.env_template job-search-be/.env

# 2. Edit the .env file and add your Google API key
# Replace 'your_google_api_key_here' with your actual API key from:
# https://aistudio.google.com/app/apikey
```

### Recommended Development Setup (Hybrid Mode)

**All Platforms:**
```bash
./dev-start.sh           # Hybrid mode: backend in Docker, frontend local
./dev-start.sh docker    # Both services in Docker
./dev-start.sh backend   # Only backend in Docker
./dev-start.sh frontend  # Only frontend locally
```

**NPM Scripts:**
```bash
npm install          # Install root dependencies
npm run dev         # Start hybrid development environment
npm run start       # Alternative start command
npm run stop        # Stop Docker services
npm run logs        # View backend logs
npm run restart     # Restart backend container
```

### Docker Deployment

```bash
# Start backend service in Docker
docker-compose up --build

# Background mode
docker-compose up -d --build

# Stop backend service
docker-compose down

# Note: Frontend must be started separately with:
# cd job-search-fe && pnpm dev:local
```

### Manual Development Setup

**Backend (Docker - Recommended):**
```bash
# Ensure .env file is configured first
docker-compose up -d backend
```

**Backend (Local):**
```bash
cd job-search-be
python -m venv venv
source venv/bin/activate  # Linux/macOS: venv\Scripts\activate (Windows)
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend (Local):**
```bash
cd job-search-fe
pnpm install
pnpm dev:local
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📖 Usage Guide

1. **Upload Resume**: Drag & drop or click to upload (PDF/DOC/DOCX)
2. **Parse Content**: Extract and organize resume sections using AI
3. **Review Sections**: Verify parsed information accuracy
4. **Analyze Resume**: Get AI-powered insights and recommendations
5. **Export Results**: Download analysis report as JSON

### API Endpoints
- **POST `/parse_resume`**: Upload and parse resume files
- **POST `/analyze_resume`**: Analyze parsed resume data
- **GET `/`**: Health check endpoint
- **GET `/docs`**: Interactive API documentation

## 🐳 Development Workflow

### Hybrid Mode (Recommended)
- **Backend**: Runs in Docker for consistent environment and LibreOffice support
- **Frontend**: Runs locally for fast hot reload and debugging
- **Benefits**: Best of both worlds - consistency + performance

```bash
./dev-start.sh           # Start hybrid mode
./dev-start.sh stop      # Stop backend Docker container
./dev-start.sh logs      # View backend logs
./dev-start.sh restart   # Restart both services
```

### Docker Mode
- **Backend**: Runs in Docker container
- **Frontend**: Still runs locally (docker-compose only defines backend service)
- **Use case**: Consistent backend environment testing

```bash
./dev-start.sh docker    # Start backend in Docker (frontend still local)
docker-compose logs -f   # View backend logs
```

## 📁 Project Structure

```
resume-analyzer-platform/          # Monorepo root
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules
├── package.json                   # Root workspace config (resume-analyzer-platform)
├── pnpm-lock.yaml                # Root lockfile
├── docker-compose.yml             # Container orchestration
├── dev-start.sh                   # Development startup script
├── README.md                      # This file
├── DEVELOPMENT.md                 # Hybrid development guide
├── STARTUP_GUIDE.md              # Detailed startup guide
├── job-search-be/                # Backend application
│   ├── main.py                   # FastAPI app (v6.2.0)
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # Backend container
│   ├── .env_template            # Environment template
│   ├── .env                     # Your API key (create this)
│   └── venv/                    # Virtual environment
└── job-search-fe/               # Frontend application
    ├── pages/                   # Nuxt pages
    ├── components/              # Vue components
    ├── package.json            # Frontend dependencies
    ├── nuxt.config.ts          # Nuxt configuration
    ├── tailwind.config.js      # Tailwind configuration
    ├── components.json         # Shadcn component config
    └── node_modules/          # NPM packages
```

## 🔧 Development

### Environment Variables

#### Required Setup: Google API Key

**⚠️ IMPORTANT**: Before running the application, you must create a `.env` file in the backend directory with your Google API key.

**Backend** (`.env` in `job-search-be/`):
```env
# Required: Google Generative AI API Key
GOOGLE_API_KEY=your_actual_api_key_here

# Optional server configuration
PYTHONPATH=.
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
```

**How to get your Google API Key:**
1. Visit https://aistudio.google.com/app/apikey
2. Create a new API key
3. Copy the key and replace `your_actual_api_key_here` in your `.env` file

**Quick Setup:**
```bash
# Copy the template and edit it
cp job-search-be/.env_template job-search-be/.env
# Then edit job-search-be/.env with your actual API key
```

**Frontend** (Automatic via scripts):
```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Available Scripts

```bash
# Root level (coordination)
npm run dev              # Start hybrid development environment
npm run start            # Alternative start command
npm run stop             # Stop Docker services
npm run logs             # View backend Docker logs
npm run dev:backend      # Start only backend in Docker
npm run dev:frontend     # Start only frontend locally
npm run install:frontend # Install frontend dependencies
npm run clean           # Clean build artifacts

# Development script options
./dev-start.sh           # Hybrid mode (default)
./dev-start.sh docker    # Both services in Docker
./dev-start.sh backend   # Only backend
./dev-start.sh frontend  # Only frontend
./dev-start.sh stop      # Stop Docker containers
./dev-start.sh logs      # Show backend logs
./dev-start.sh restart   # Restart backend container

# Frontend specific
cd job-search-fe
pnpm dev:local          # Development with local API connection
pnpm build              # Production build
pnpm preview            # Preview build

# Backend specific
cd job-search-be
uvicorn main:app --reload  # Development server (if running locally)
```

## 🛠 Troubleshooting

### Common Issues

**Google API Key Issues:**
```bash
# Check if .env file exists and contains API key
ls job-search-be/.env
cat job-search-be/.env

# If missing, copy template and edit:
cp job-search-be/.env_template job-search-be/.env
# Then edit with your actual API key
```

**Port Conflicts:**
```bash
# Kill processes on ports 3000, 8000
lsof -ti:3000,8000 | xargs kill -9
```

**Dependency Issues:**
```bash
# Frontend
cd job-search-fe && rm -rf node_modules && pnpm install

# Backend
cd job-search-be && rm -rf venv && python -m venv venv
```

**Docker Issues:**
```bash
docker-compose down --remove-orphans
docker system prune -f
./dev-start.sh stop
```

### Logs and Debugging

- **Hybrid Development**: Frontend logs in terminal, backend via `./dev-start.sh logs`
- **Docker**: `docker-compose logs -f [service]`
- **Individual Services**: Check service-specific terminal output

## 🚀 Deployment

### Development Deployment Checklist
- [ ] Environment variables configured (.env file with GOOGLE_API_KEY)
- [ ] Docker service running
- [ ] LibreOffice available in backend container for DOCX conversion
- [ ] Frontend connecting to backend API successfully

### Docker Deployment
```bash
# Build and run backend
docker-compose up --build

# Run backend in background
docker-compose up -d --build

# Start frontend separately
cd job-search-fe && pnpm dev:local

# View backend logs
docker-compose logs -f
```

## 📄 License

MIT License - see LICENSE file for details.

## 📞 Support

- Check [DEVELOPMENT.md](./DEVELOPMENT.md) for hybrid development setup
- Review [STARTUP_GUIDE.md](./STARTUP_GUIDE.md) for detailed startup instructions
- Review logs for error details

---
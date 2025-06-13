# Job Search Platform

A modern AI-powered job search platform with resume analysis capabilities. Built as a monorepo with FastAPI backend and Nuxt.js frontend.

## 🌟 Features

- **Resume Analysis**: AI-powered resume parsing and improvement suggestions
- **File Upload Support**: PDF, DOC, DOCX formats (max 10MB)
- **Intelligent Parsing**: Automatic section extraction and organization
- **Action Verb Analysis**: Optimize resume language and impact
- **Missing Sections Detection**: Comprehensive resume completeness check
- **Export Reports**: Download analysis results as JSON
- **Modern UI**: Responsive interface with real-time feedback
- **Live Status Monitoring**: Backend connection status tracking

## 🛠 Tech Stack

### Backend (`job-search-be/`)
- **FastAPI**: Modern Python web framework
- **Python 3.8+**: Core language
- **pdfminer.six**: PDF text extraction
- **python-docx**: DOCX file processing
- **Uvicorn**: ASGI server

### Frontend (`job-search-fe/`)
- **Nuxt.js 3**: Vue.js framework with SSR
- **Vue 3**: Progressive JavaScript framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Shadcn/ui**: Component library

### Infrastructure
- **Docker**: Containerized deployment
- **pnpm**: Package management
- **Git**: Version control (monorepo)

## 📋 Prerequisites

- **Node.js** v18+ and **pnpm**
- **Python** v3.8+ and **pip**
- **Docker** & **Docker Compose** (optional)
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

### Automated Startup (Recommended)

**Linux/macOS:**
```bash
./start.sh           # Interactive mode
./start.sh docker    # Docker deployment
./start.sh local     # Local development
```

**Windows:**
```cmd
start.bat           # Interactive mode
start.bat docker    # Docker deployment
start.bat local     # Local development
```

**NPM Scripts:**
```bash
npm install          # Install root dependencies
npm run dev         # Start both services
npm run docker:up   # Docker deployment
```

### Docker Deployment

```bash
# Start all services
docker-compose up --build

# Background mode
docker-compose up -d --build

# Stop services
docker-compose down
```

### Manual Development Setup

**Backend:**
```bash
cd job-search-be
python -m venv venv
source venv/bin/activate  # Linux/macOS: venv\Scripts\activate (Windows)
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd job-search-fe
pnpm install
pnpm dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📖 Usage Guide

1. **Upload Resume**: Drag & drop or click to upload (PDF/DOC/DOCX)
2. **Parse Content**: Extract and organize resume sections
3. **Review Sections**: Verify parsed information accuracy
4. **Analyze Resume**: Get AI-powered insights and recommendations
5. **Export Results**: Download analysis report as JSON

### Analysis Features
- **Completeness Score**: 0-100% resume quality rating
- **Missing Sections**: Identification of gaps
- **Action Verb Analysis**: Language impact assessment
- **Personalized Recommendations**: Tailored improvement suggestions

## 🐳 Docker Configuration

The project includes optimized Docker configuration:

- **Multi-stage builds** for production efficiency
- **Development volumes** for hot reloading
- **Environment-specific** configurations
- **Network isolation** between services

See `docker-compose.yml` for complete configuration.

## 📁 Project Structure

```
job-search-platform/                # Monorepo root
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules
├── package.json                   # Root workspace config
├── docker-compose.yml             # Container orchestration
├── start.sh / start.bat           # Startup scripts
├── README.md                      # This file
├── STARTUP_GUIDE.md              # Quick start guide
├── job-search-be/                # Backend application
│   ├── main.py                   # FastAPI app
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # Backend container
│   └── venv/                    # Virtual environment
└── job-search-fe/               # Frontend application
    ├── pages/                   # Nuxt pages
    ├── components/              # Vue components
    ├── package.json            # Frontend dependencies
    ├── nuxt.config.ts          # Nuxt configuration
    ├── Dockerfile             # Frontend container
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

**Frontend** (`.env` in `job-search-fe/`):
```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Scripts Available

```bash
# Root level (coordination)
npm run dev              # Start both services
npm run install:all      # Install all dependencies
npm run clean           # Clean build artifacts
npm run docker:up       # Docker deployment
npm run docker:down     # Stop Docker services

# Frontend specific
cd job-search-fe
pnpm dev                # Development server
pnpm build              # Production build
pnpm preview            # Preview build

# Backend specific
cd job-search-be
uvicorn main:app --reload  # Development server
python -m pytest          # Run tests (if available)
```

## 🛠 Troubleshooting

### Common Issues

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
```

### Logs and Debugging

- **Local Development**: Check terminal output
- **Docker**: `docker-compose logs -f [service]`
- **Individual Services**: Check service-specific logs

## 🚀 Deployment

### Production Checklist
- [ ] Environment variables configured
- [ ] Docker images built and tested
- [ ] Backend API endpoints secured
- [ ] Frontend build optimized
- [ ] CORS settings configured
- [ ] File upload limits set

### Docker Production
```bash
# Build production images
docker-compose -f docker-compose.prod.yml up --build

# Scale services
docker-compose up --scale frontend=2 --scale backend=2
```

## 🤝 Contributing

1. Clone the repository
2. Create a feature branch
3. Make changes in appropriate service directory
4. Test locally with `./start.sh local`
5. Test with Docker using `./start.sh docker`
6. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

## 📞 Support

- Check [STARTUP_GUIDE.md](./STARTUP_GUIDE.md) for quick start
- Review logs for error details
- Use `./start.sh help` for script options

---
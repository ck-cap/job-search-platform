# Architecture

## System Overview

The Job Search Platform follows a microservices architecture with three main components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Frontend     │    │   Backend API   │    │  Model Service  │
│   (Nuxt.js)     │◄──►│   (FastAPI)     │◄──►│   (FastAPI)     │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 8001    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         │                       ▼                       ▼
         │              ┌─────────────────┐    ┌─────────────────┐
         │              │  Google Gemini  │    │  Fine-tuned ML  │
         │              │      API        │    │     Models      │
         │              └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│   User Browser  │
└─────────────────┘
```

## Component Details

### Frontend Service
- **Technology**: Nuxt.js 3 with Vue.js
- **UI**: Tailwind CSS + Shadcn/ui components
- **Purpose**: User interface for resume upload and job search
- **Deployment**: Runs locally during development

### Backend API Service
- **Technology**: FastAPI with Python
- **Purpose**: Resume parsing, AI analysis, service orchestration  
- **External APIs**: Google Gemini for resume analysis
- **Features**:
  - File upload handling (PDF/DOCX)
  - Document conversion (DOCX to PDF)
  - Resume parsing using AI
  - Job matching coordination

### Model Service
- **Technology**: FastAPI with PyTorch/Transformers
- **Purpose**: ML-powered job matching
- **Models**: Fine-tuned sentence transformers
- **Features**:
  - Semantic similarity matching
  - Job recommendation ranking
  - Model serving with health checks

## Data Flow

1. **Resume Upload**: User uploads resume via frontend
2. **File Processing**: Backend converts DOCX to PDF if needed
3. **AI Parsing**: Google Gemini extracts structured data
4. **Job Matching**: Model service finds similar jobs
5. **Results Display**: Frontend shows parsed data and matches

## Technology Stack

### Frontend
- Nuxt.js 3 (Vue.js framework)
- Tailwind CSS (styling)
- TypeScript (type safety)
- pnpm (package management)

### Backend
- FastAPI (Python web framework)
- Google Generative AI SDK
- LibreOffice (document conversion)
- Docker (containerization)

### Model Service
- PyTorch (ML framework)
- Sentence Transformers (embeddings)
- Pandas (data processing)
- Custom fine-tuned models

## Infrastructure

### Development
- Docker Compose for service orchestration
- Local frontend development server
- Containerized backend services
- Volume mounts for hot reloading

### Networking
- Internal Docker network for service communication
- Port mappings for external access
- CORS enabled for frontend-backend communication 
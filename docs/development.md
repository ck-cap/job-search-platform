# Development Guide

## Development Commands

The `start.sh` script provides several commands for development:

```bash
# Start all services (default)
./start.sh

# Development mode with hot reload
./start.sh dev

# Backend services only
./start.sh backend

# Frontend only
./start.sh frontend

# View service status
./start.sh status

# View logs
./start.sh logs

# Stop all services
./start.sh stop

# Clean Docker resources
./start.sh clean
```

## Development Workflow

### Frontend Development
```bash
cd services/frontend

# Install dependencies
pnpm install

# Start dev server (connects to local backend)
pnpm dev:local

# Build for production
pnpm build
```

### Backend Development
```bash
cd services/backend-api

# Install dependencies
pip install -r requirements.txt

# Run locally (requires environment setup)
uvicorn main:app --reload
```

### Model Service Development
```bash
cd services/model-service

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn model_service:app --port 8001 --reload
```

## File Structure

```
job-search-platform/
├── services/
│   ├── frontend/           # Nuxt.js application
│   │   ├── components/     # Vue components
│   │   ├── pages/          # Route pages
│   │   ├── assets/         # Static assets
│   │   └── nuxt.config.ts  # Nuxt configuration
│   ├── backend-api/        # FastAPI backend
│   │   ├── main.py         # Main API routes
│   │   ├── Dockerfile      # Container config
│   │   └── requirements.txt
│   └── model-service/      # ML service
│       ├── model_service.py # FastAPI service
│       ├── model.py        # ML model logic
│       └── model/          # Model files
├── docs/                   # Documentation
├── docker-compose.yml      # Service orchestration
└── start.sh               # Development script
```

## Environment Variables

Create `.env` file in project root:

```bash
# Required for backend
GOOGLE_API_KEY=your_google_api_key

# Model service paths (configured in Docker)
MODEL_PATH=/app/model/fine_tuned_mpnet_with_eval
DATASET_PATH=/app/dataset/mpnet_finetune_dataset_test.csv
```

## Hot Reloading

- **Frontend**: Automatic reload via Nuxt dev server
- **Backend**: Enabled via `--reload` flag in Docker
- **Model Service**: Container restart required for changes

## Debugging

### View Logs
```bash
# All services
./start.sh logs

# Specific service
docker-compose logs backend-api
docker-compose logs model-service
```

### Common Issues

1. **Port conflicts**: Change ports in `docker-compose.yml`
2. **Model not loading**: Check model files exist in `services/model-service/model/`
3. **API key errors**: Verify Google API key in `.env`
4. **Docker issues**: Restart Docker Desktop

### Testing APIs

Use the interactive API documentation:
- Backend: http://localhost:8000/docs
- Model Service: http://localhost:8001/docs

Or test with curl:
```bash
# Health check
curl http://localhost:8001/health

# Parse resume (replace with actual file)
curl -X POST "http://localhost:8000/parse_resume" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
``` 
# Setup Guide

## Prerequisites

- Docker Desktop
- pnpm (for frontend development)
- Google API Key (for Gemini AI)

## Environment Setup

1. **Copy environment template**:
   ```bash
   cp .env_template .env
   ```

2. **Configure environment variables**:
   ```bash
   # Edit .env file
   GOOGLE_API_KEY=your_google_api_key_here
   MODEL_PATH=/app/model/fine_tuned_mpnet_with_eval
   DATASET_PATH=/app/dataset/mpnet_finetune_dataset_test.csv
   ```

3. **Get Google API Key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

## Installation

### Option 1: Full Setup (Recommended)
```bash
# Run complete setup
./start.sh
```

### Option 2: Manual Setup
```bash
# 1. Extract model (if required)
# The script will automatically extract the 387MB model file

# 2. Start backend services
docker-compose up -d --build

# 3. Start frontend (in separate terminal)
cd services/frontend
pnpm install
pnpm dev:local
```

## Verification

1. Check backend services:
   ```bash
   ./start.sh status
   ```

2. Test API endpoints:
   - Backend API: http://localhost:8000/docs
   - Model Service: http://localhost:8001/health

3. Access frontend: http://localhost:3000

## Troubleshooting

- **Docker not running**: Start Docker Desktop
- **Model extraction fails**: Check available disk space (387MB required)
- **Google API errors**: Verify API key in `.env` file
- **Port conflicts**: Ensure ports 3000, 8000, 8001 are available 
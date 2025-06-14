# Job Search Platform

AI-powered job search platform with resume analysis and job matching capabilities.

## Overview

This is a microservices-based platform that helps users analyze their resumes and find matching job opportunities using AI and machine learning.

## Architecture

- **Frontend**: Nuxt.js web application with Tailwind CSS
- **Backend API**: FastAPI service for resume parsing and analysis
- **Model Service**: ML service for job matching using fine-tuned models
- **Docker**: Containerized deployment with Docker Compose

## Key Features

- Resume upload and parsing (PDF/DOCX)
- AI-powered resume analysis using Google Gemini
- Job matching using fine-tuned sentence transformers
- Modern web interface with responsive design
- RESTful API architecture

## Quick Start

```bash
# Start all services
./start.sh

# Backend only
./start.sh backend

# Frontend only
./start.sh frontend
```

## Access URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Model Service: http://localhost:8001
- API Documentation: http://localhost:8000/docs

## Documentation

- [Setup Guide](setup.md)
- [API Reference](api.md)
- [Architecture](architecture.md)
- [Development](development.md) 
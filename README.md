# Job Search Platform 🚀

AI-powered job search platform with resume analysis and intelligent job matching.

## ✨ Features

- **Resume Upload & Parsing** - Support for PDF and DOCX files
- **AI-Powered Analysis** - Google Gemini integration for smart resume parsing
- **Job Matching** - Fine-tuned ML models for accurate job recommendations
- **Modern UI** - Responsive Nuxt.js frontend with Tailwind CSS
- **Microservices Architecture** - Scalable Docker-based deployment

## 📋 Prerequisites

Refer **[Prerequisites](docs/prerequisites.md)** to set up the development environment.
- Docker Desktop
- pnpm (for frontend development)
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))

## 📖 Documentation

- **[Prerequisites](docs/prerequisites.md)** - Install Docker, Node.js, pnpm and other dependencies
- **[Setup Guide](docs/setup.md)** - Detailed installation and configuration
- **[API Reference](docs/api.md)** - Complete API documentation
- **[Architecture](docs/architecture.md)** - System design and components
- **[Development](docs/development.md)** - Development workflow and debugging


## 🏃‍♂️ Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd job-search-platform
   cp .env_template .env
   ```

2. **Add your Google API key** to `.env`:
   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Start the platform**:
   ```bash
   ./start.sh
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🏗️ Architecture

```
Frontend (Nuxt.js) ←→ Backend API (FastAPI) ←→ Model Service (ML)
     ↓                      ↓                       ↓
User Interface         Google Gemini AI        Job Matching Models
```
## 🛠️ Tech Stack

- **Frontend**: Nuxt.js, Vue.js, Tailwind CSS
- **Backend**: FastAPI, Python
- **AI/ML**: Google Gemini, PyTorch, Sentence Transformers
- **Infrastructure**: Docker, Docker Compose

## 🚦 Commands

```bash
./start.sh          # Start all services
./start.sh backend  # Backend services only
./start.sh frontend # Frontend only
./start.sh status   # Check service status
./start.sh logs     # View logs
./start.sh stop     # Stop all services
```

---

<img width="1629" alt="image" src="https://github.com/user-attachments/assets/c61ce7a9-1027-4f7d-8502-a98328a158f4" />

## Not Covered Scope
- Database, current using mock data to simulate
- Some data was hardcoded as this is still a POC
- Cron job not available as of now (model is ready)

*Built with ❤️ using modern web technologies and AI, VibeCoding hehe* 

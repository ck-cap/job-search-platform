# Use a stable base image optimized for ML workloads
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for ML libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements for model service
COPY requirements.txt .

# Install Python dependencies for model service
RUN pip install --no-cache-dir -r requirements.txt

# Copy model-related files
COPY model.py .
COPY model_service.py .
COPY model/ ./model/
COPY dataset/ ./dataset/

# Set environment variables for better memory management
ENV PYTHONUNBUFFERED=1
ENV TORCH_NUM_THREADS=2
ENV OMP_NUM_THREADS=2

# Expose the port for the model service
EXPOSE 8001

# Add health check
HEALTHCHECK --interval=30s --timeout=15s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

# Command to run the model service with memory optimizations
CMD ["uvicorn", "model_service:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "1"] 
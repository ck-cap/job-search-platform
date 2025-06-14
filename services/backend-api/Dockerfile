# Use a stable slim base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for document processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre \
    libreoffice-writer \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies for backend service
RUN pip install --no-cache-dir -r requirements.txt

# Copy only backend-related files
COPY main.py .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the backend application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
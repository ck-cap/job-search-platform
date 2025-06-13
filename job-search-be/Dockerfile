# Use a stable slim base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre \
    libreoffice-writer \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
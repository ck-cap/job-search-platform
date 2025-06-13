FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install system dependencies including wget for health check
RUN apk add --no-cache wget

# Install pnpm
RUN npm install -g pnpm

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install

# Copy the application code
COPY . .

# Expose port
EXPOSE 3000

# Health check - use curl instead of wget for better compatibility
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Start the application with explicit port and host
CMD ["pnpm", "dev", "--host", "0.0.0.0", "--port", "3000"] 
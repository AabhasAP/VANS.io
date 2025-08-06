FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    git golang-go gcc libffi-dev libssl-dev build-essential \
    curl wget unzip nmap dnsutils nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install gau (Go-based tool)
RUN go install github.com/lc/gau/v2/cmd/gau@latest
ENV PATH="/root/go/bin:$PATH"

# Copy backend code
COPY .env .env
COPY ./core /app/core
COPY ./modules /app/modules
COPY ./api /app/api

# Build React frontend
COPY ./frontend /app/frontend
WORKDIR /app/frontend

RUN npm install && npm run build

# Move frontend build output into FastAPI static serving dir
RUN mkdir -p /app/core/static && cp -r build/* /app/core/static/

# Return to root app directory
WORKDIR /app

# Run FastAPI (will serve static files from /core/static)
CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000"]

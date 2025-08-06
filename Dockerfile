FROM python:3.12-slim

WORKDIR /app


# Bad
RUN apt-get update
RUN apt-get install -y nodejs

# Better
RUN apt-get update && apt-get install -y nodejs







# --- OS & Core Dependencies ---
RUN apt-get update && apt-get install -y \
    git \
    golang-go \
    gcc \
    libffi-dev \
    libssl-dev \
    build-essential \
    curl \
    wget \
    unzip \
    nmap \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# --- Copy Files ---
COPY requirements.txt requirements.txt
COPY .env .env
COPY ./core /app/core

# --- Install gau ---
RUN go install github.com/lc/gau/v2/cmd/gau@latest
ENV PATH="/root/go/bin:$PATH"

# --- Install Python Packages ---
RUN pip install --no-cache-dir -r requirements.txt

# --- Expose & Start API ---
CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000"]

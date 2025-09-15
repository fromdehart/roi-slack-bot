# Dockerfile for safe graph generation
FROM python:3.9-slim

# Install system dependencies for matplotlib
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash graphuser
USER graphuser

# Create working directory for graph generation
WORKDIR /home/graphuser

# Copy the graph generator
COPY --chown=graphuser:graphuser graph_generator.py .

# Create a safe execution script
COPY --chown=graphuser:graphuser safe_executor.py .

# Set environment variables
ENV PYTHONPATH=/home/graphuser
ENV MATPLOTLIB_BACKEND=Agg

# Default command
CMD ["python3", "safe_executor.py"]

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml, README.md, and workspace directory
COPY pyproject.toml README.md ./
COPY workspace/ workspace/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy the rest of the application code (e.g., .env)
COPY .env .env

# Expose port 5000 for the Flask API
EXPOSE 5000

# Set the default command for the Flask API
CMD ["python", "-m", "flask", "--app", "workspace.src.api", "run", "--host=0.0.0.0"]
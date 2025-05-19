# Use the official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy backend source code
COPY backend/src/ ./src/
COPY backend/credentials.json ./credentials.json
COPY backend/.env ./

# Expose port for Cloud Run
EXPOSE 8080

# Start FastAPI app with uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]

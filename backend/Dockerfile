# Base image for the API container.
FROM python:3.11-slim

# Set working directory in container.
WORKDIR /app

# Python runtime settings.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code.
COPY ./app ./app

# Run FastAPI via Uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

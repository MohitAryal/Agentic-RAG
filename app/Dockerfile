FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY ../requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copy FastAPI app
COPY . /app/

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with gunicorn + uvicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
# Python FastAPI Dockerfile

# Pull base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

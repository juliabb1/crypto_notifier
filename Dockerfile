# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Default command
CMD ["python", "-m", "app.main"]

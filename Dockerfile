FROM python:3.11-alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole app, including tests
COPY . .

# Default command
CMD ["python", "app.py"]

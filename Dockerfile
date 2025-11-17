FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app and tests into the image
COPY app.py .
COPY tests/ tests/

CMD ["python", "app.py"]

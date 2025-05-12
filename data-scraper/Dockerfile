FROM python:3.12-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose FastAPI port
EXPOSE 7000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]


FROM python:3.12-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose FastAPI port
EXPOSE 7010

# Run the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7010"]


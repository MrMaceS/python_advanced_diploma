FROM python:3.11-slim

WORKDIR /home

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend backend/

COPY static static/

COPY init_db.py .

COPY seed_db.py .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.12-slim

WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app
COPY frontend /app/frontend_build

ENV DATA_PATH=/app/data
ENV PORT=8080
EXPOSE 8080
CMD ["/bin/sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]

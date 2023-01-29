FROM python:3.10-slim

ENV PORT 8081
EXPOSE $PORT
WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
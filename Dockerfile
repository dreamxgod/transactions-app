FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app2 /app

EXPOSE 8080

WORKDIR /app/app2

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
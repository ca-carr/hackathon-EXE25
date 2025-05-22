FROM python:3.9-slim

WORKDIR /app

COPY main.py .
COPY relays.json .

RUN pip install requests

EXPOSE 55665

CMD ["python", "main.py"] 
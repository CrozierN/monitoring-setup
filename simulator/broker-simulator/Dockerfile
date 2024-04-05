FROM python:3.10.13-slim

WORKDIR /usr/src/app

COPY . .

ENV OTLP_ENDPOINT="http://localhost:4318"
ENV CONSUMER_ENDPOINT="http://localhost:5001"

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./broker-simulator.py"]
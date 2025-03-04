FROM python:3.9.21-alpine3.21

WORKDIR /mqtt_client

COPY db.py .
COPY requirements.txt .
COPY sub_client.py .
COPY validator.py . 

RUN pip install --no-cache-dir -r requirements.txt

# Environment variables for the broker
ENV BROKER_HOST=mosquitto-broker

# Run the subscriber script
CMD ["python3", "subscriber.py"]

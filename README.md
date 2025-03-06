# IoT-Event-Processing-System

## Overview

This project implements an **IoT Event Processing System** for ingesting, validating, storing, and serving IoT sensor data using **MQTT**, **SQLite**, and **RESTful APIs** with Docker containerization.

The system is divided into three main services:

1. **MQTT Broker** - Manages communication between IoT devices and the system.
2. **MQTT Client** - Subscribes to sensor data topics, validates JSON payloads, and stores them in a database.
3. **REST API** - Provides device information and sensor data through HTTP endpoints.

## Directory Structure

```
IOT-EVENT-PROCESSING-SYSTEM/
├── data/                  # Database Storage
│   └── iot_database.db    # SQLite Database
├── mqtt_broker/           # MQTT Broker Configuration
│   └── config/
│       └── mosquitto.conf
├── mqtt_client/           # MQTT Subscriber and Validator
│   ├── logs/              # Logs for invalid messages
│   ├── db.py              # Database interaction module
│   ├── Dockerfile         # Docker container for MQTT client
│   ├── requirements.txt   # Dependencies
│   ├── sub_client.py      # MQTT Subscriber
│   └── validator.py       # JSON Validator
├── rest_api/              # REST API Service
│   ├── logs/              # API Logs
│   ├── app.py             # Flask API
│   ├── Dockerfile         # Docker container for REST API
│   └── requirements.txt   # Dependencies
├── .env                   # Environment Variables
├── docker-compose.yml      # Docker Compose for orchestrating services
├── README.md              # Project Documentation
└── .gitignore             # Git Ignore file
```

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

1. Clone the Repository:

```bash
$ git clone <repository-url>
$ cd IOT-EVENT-PROCESSING-SYSTEM
```

2. Configure Environment Variables: Create a `.env` file in the root directory with the following variables:

```
BROKER_HOST=mqtt_broker
BROKER_PORT=1883
TOPIC=iot/sensor/data
DB_PATH=/data/iot_database.db
API_PORT=5000
```

3. Build and Start Services:

```bash
$ docker-compose up --build
```

4. Verify Services:

- MQTT Broker: `tcp://localhost:1883`
- REST API: `http://localhost:5000/api/v1`

## API Documentation

### Base URL

```
http://<host>:5000/api/v1
```

### Endpoints

#### 1. List All Devices

**GET** `/devices`

- Response:

```json
[
  {"device_id": "1001", "last_seen": "2025-03-06T10:20:30Z"}
]
```

#### 2. Get Device Events

**GET** `/events?device_id=<device_id>`

- Query Params:
  - `device_id` (required): Device ID to fetch event logs.
- Response:

```json
[
  {"event_id": 1, "sensor_type": "temperature", "sensor_value": 23.4, "timestamp": "2025-03-06T10:20:30Z"}
]
```

#### Error Response

```json
{
  "error": "Missing required query parameter: ?device_id="
}
```

## Test Cases & Example Usage

1. Start the system with Docker:

```bash
$ docker-compose up
```

2. Publish MQTT Messages (Simulated via `pub_client.py`):

```bash
$ python pub_client.py
```

Example Payload:

```json
{
  "device_id": "1001",
  "sensor_type": "temperature",
  "sensor_value": 23.4,
  "timestamp": "2025-03-06T10:20:30Z"
}
```

3. Verify Device Information:

```bash
$ curl http://localhost:5000/api/v1/devices
```

4. Fetch Device Events:

```bash
$ curl http://localhost:5000/api/v1/events?device_id=1001
```

## System Architecture

The solution is designed with **modularity** and **scalability** in mind:

- Independent services for message ingestion, validation, and serving.
- Docker containerization enables platform-agnostic deployment.
- SQLite provides lightweight persistent storage.
- REST API versioning ensures backward compatibility.

## Logs

- MQTT Client logs are stored under `mqtt_client/logs`
- REST API logs are stored under `rest_api/logs`

## Conclusion

This project demonstrates an IoT event processing system capable of validating, storing, and serving sensor data with a scalable microservices architecture.

---

**Author:** Nimesh Nagar **Date:** March 2025


import asyncio
import json
from gmqtt import Client as MQTTClient
from datetime import datetime

MQTT_HOST = "localhost" 
PORT = 1883
PUB_TOPIC = "device/events"

STOP = asyncio.Event()


def on_connect(client, flags, rc, properties):
    print("Connected to MQTT broker")

def on_disconnect(client, packet, exc=None):
    print("Disconnected")

async def publish_message():
    client = MQTTClient("publisher_client")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    await client.connect(MQTT_HOST, PORT)

    message1 = {
        "device_id": "1001",
        "sensor_type": "humidity",
        "sensor_value": 70.6,
        "timestamp": datetime.now().isoformat()
        # "timestamp": "12:13:55"
    }

    message2 = {
        "device_id": "1002",
        "sensor_type": "temperature",
        "sensor_value": 28.5,
        "timestamp": datetime.now().isoformat()
        # "timestamp": "12:13:55"
    }

    json_payload = json.dumps(message2) #change message number accordingly

    client.publish(PUB_TOPIC, json_payload, qos=1)
    print(f"Published: {json_payload}")

    await asyncio.sleep(2)
    await client.disconnect()
    STOP.set()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(publish_message())
    finally:
        loop.close()
        print("[INFO] Publisher disconnected")

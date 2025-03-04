import asyncio
import os
import signal
import time

from gmqtt import Client as MQTTClient
from validator import validation_message
from db import log_invalid_message, store_valid_message


# MQTT_HOST ='localhost'
# SUB_TOPIC = 'device/events'

SUB_TOPIC = os.getenv("MQTT_TOPIC", "devices/events")
MQTT_HOST = os.getenv("MQTT_BROKER_HOST", "mqtt-broker")

QOS = 0
PORT = 1883

STOP = asyncio.Event()

def on_connect(client, flags, rc, properties):
    print('Connected to mqtt broker')
    client.subscribe(SUB_TOPIC, QOS)

def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_message(client, topic, payload, qos, properties):
    # print(type(payload))
    message = payload.decode('utf-8')
    print( f'Received Message: {message}' )

    if validation_message(message):
        print(f"Valid message received ! now store to db")
        store_valid_message(message)
    else:
        log_invalid_message(message, "Validation failed")
        
    
def on_subscribe(client, mid, qos, properties):
    print(f'SUBSCRIBED to Topic : {SUB_TOPIC}' )

def ask_exit(*args):
    STOP.set()

async def main(broker_host, port):
    client = MQTTClient("python-client")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    # client.set_auth_credentials(token, None)
    await client.connect(host=broker_host, port=port)

    client.publish('TEST/TIME', str(time.time()), qos=1)

    try:
        await STOP.wait()
    finally:
        await client.disconnect()
        print("[INFO] Client disconnected")


if __name__ == '__main__':
    # loop = asyncio.new_event_loop() # Ensuring a clean event loop
    # asyncio.set_event_loop(loop)

    # if os.name != "nt":  # Unix-based signal handling
    #     loop.add_signal_handler(signal.SIGINT, ask_exit)
    #     loop.add_signal_handler(signal.SIGTERM, ask_exit)

    # try:
    #     loop.run_until_complete(main(MQTT_HOST, PORT))
    # finally:
    #     loop.close()

    loop = asyncio.get_event_loop()  # Use the default event loop

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    asyncio.run(main(MQTT_HOST, PORT))  # Use asyncio.run instead of run_until_complete()

    


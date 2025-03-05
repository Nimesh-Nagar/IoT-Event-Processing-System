from flask import Flask, jsonify, request
import sqlite3
import os
import logging

from dotenv import load_dotenv

load_dotenv()

# Configure logging
LOG_DIR = os.path.join(os.path.dirname(__file__), './logs')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOG_DIR, 'api.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
# DB_PATH = os.path.join(os.path.dirname(__file__), '../data/iot_database.db')
DB_PATH = os.getenv("DB_PATH", "/data/test.db")

app = Flask(__name__)
API_VERSION = '/api/v1'

@app.route("/", methods=['GET'])
def home():
    logging.info("Home endpoint accessed")
    return "<h1> IoT Dash Board</h1>"

@app.route(f"{API_VERSION}/devices", methods=['GET'])
def get_devices():
    '''
    List all registered devices and their last seen details
    '''
    logging.info("Fetching all devices")
    try:
        conn = sqlite3.connect(DB_PATH)   # assign proper path
        c = conn.cursor()
        
        c.execute("SELECT * FROM Devices")
        devices = c.fetchall()
        conn.close()

        logging.info(f"{len(devices)} devices fetched successfully")
        return jsonify( [{'device_id' : device[0], 'last_seen' : device[1] } for device in devices] )
    except Exception as e:
        logging.error(f"Error fetching devices: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route(f"{API_VERSION}/events", methods=['GET'])
def get_events():
    device_id = request.args.get('device_id')

    if not device_id:
        logging.warning("Missing required device_id parameter")
        return jsonify({"error": "Missing required query parameter: ?device_id="}), 400  # HTTP 400 Bad Request

    try:
        logging.info(f"Fetching events for device_id: {device_id}")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()    
        c.execute("SELECT event_id, sensor_type, sensor_value, timestamp FROM Events WHERE device_id = ? ORDER BY timestamp DESC", (device_id,))
        events = c.fetchall()

        conn.close()

        logging.info(f"{len(events)} events fetched for device_id: {device_id}")
        return jsonify([{
            "event_id": event[0],
            "sensor_type": event[1],
            "sensor_value": event[2],
            "timestamp": event[3]
        } for event in events])
    
    # logic for without query api
    # conn = sqlite3.connect('iot_database.db')
    # c = conn.cursor()

    # if device_id:
    #     c.execute("SELECT event_id, sensor_type, sensor_value, timestamp FROM Events WHERE device_id = ? ORDER BY timestamp DESC", (device_id,))
    # else:
    #     c.execute("SELECT event_id, device_id, sensor_type, sensor_value, timestamp FROM Events ORDER BY timestamp DESC")
    # events = c.fetchall()

    # conn.close()

    # return jsonify([{ "event_id": event[0], "device_id": event[1] if len(event) == 5 else device_id, "sensor_type": event[-3], "sensor_value": event[-2], "timestamp": event[-1]} for event in events])

    except Exception as e:
        logging.error(f"Error fetching events for device_id {device_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    logging.info("Starting Flask API service")
    app.run(host='0.0.0.0', port=5000, debug=True)

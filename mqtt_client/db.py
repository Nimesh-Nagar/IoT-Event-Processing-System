# db.py
import logging
import sqlite3
import json
from datetime import datetime

# logging configurations
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

# Database setup
conn = sqlite3.connect('iot_database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Devices (
                device_id TEXT PRIMARY KEY,
                last_seen TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT,
                sensor_type TEXT,
                sensor_value REAL,
                timestamp TEXT,
                FOREIGN KEY (device_id) REFERENCES Devices(device_id))''')
conn.commit()



def log_invalid_message(message, error_reason):
    error_msg = f"Invalid message: {message} | Error: {error_reason}"
    logging.error(error_msg)
    print(error_msg)

def store_valid_message(message):
    try:
        data = json.loads(message)

        device_id = data['device_id']
        sensor_type = data['sensor_type']
        sensor_value = data['sensor_value']
        timestamp = data['timestamp']

        # Update device last seen time
        c.execute("INSERT OR REPLACE INTO Devices (device_id, last_seen) VALUES (?, ?)",
                  (device_id, timestamp))
        
        # Insert Events 
        c.execute("INSERT INTO Events (device_id, sensor_type, sensor_value, timestamp) VALUES (?, ?, ?, ?)",
                  (device_id, sensor_type, sensor_value, timestamp))
        
        conn.commit()

        print("-----------Stored Valid Message in DB -----------")
        

    except Exception as error_msg:
        log_invalid_message(message, error_msg)


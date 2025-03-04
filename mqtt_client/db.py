
import logging
import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "./data"
LOG_PATH = "./logs"


LOG_FILE = os.path.join(LOG_PATH, "messages.log")
DB_FILE = os.path.join(DB_PATH, "iot_database.db")


print(f"\n--------------> {LOG_FILE} \n")

# Ensure directories exists
os.makedirs(DB_PATH, exist_ok=True)

# Ensure log file exists
if not os.path.exists(DB_FILE):
    open(DB_FILE, "w").close()  # Create an empty file

# logging configurations
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# logging.basicConfig(filename='error.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Database setup
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
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
    error_msg = f" Error: {error_reason}"
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

        print("----------- Stored Valid Message in DB -----------")
        

    except Exception as error_msg:
        log_invalid_message(message, error_msg)
        print(f"[Error] : {error_msg}")


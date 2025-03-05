import json
import logging 
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

LOG_PATH = os.path.join(os.path.dirname(__file__), './logs')
# Ensure logs directory exists
os.makedirs(LOG_PATH, exist_ok=True)

LOG_FILE = os.path.join(LOG_PATH, "messages.log")

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()  # Create an empty file

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


# Payload Schema
PAYLOAD_SCHEMA = {
    "device_id": str,
    "sensor_type": str,
    "sensor_value": float,
    "timestamp": str
}

def valid_isoformat(timestamp):
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False

def validation_message(message):
    try:
        data = json.loads(message)
        for key , value_type in PAYLOAD_SCHEMA.items():
            
            if key not in data:
                logging.error(f"Invalid Message: {message} | Error Missing : {key} ")
                print(f"Invalid Message: {message} | Error Missing : {key} ")
                return False
            if not isinstance(data[key], value_type):
                logging.error(f"Invalid Message: {message} | Error : Invalid data type for key : {key} ")
                print(f"Invalid Message: {message} | Error : Invalid data type for key : {key} ")
                return False
            if key == "timestamp" and not valid_isoformat((data[key])):
                logging.error(f"Invalid Message: {message} | Error : Invalid ISO8601 Timestamp formate : {key} ")
                print(f"Invalid Message: {message} | Error : Invalid ISO8601 Timestamp formate : {key} ")
                return False

        return True
    
    except Exception as e:
        logging.error(f"Invalid message: {message} | Error: JSON Decode Error: {str(e)}")
        print(f"Invalid message: {message} | Error: JSON Decode Error: {str(e)}")
        return False

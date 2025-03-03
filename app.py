from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
API_VERSION = '/api/v1'


@app.route("/", methods=['GET'])
def home():
    return "<h1> IoT Dash Board</h1>"


@app.route(f"{API_VERSION}/devices", methods=['GET'])
def get_devices():
    '''
    List all registered devices and their last seen details
    '''

    conn = sqlite3.connect('iot_database.db')   # assign proper path
    c = conn.cursor()
    
    c.execute("SELECT * FROM Devices")
    devices = c.fetchall()
    conn.close()

    return jsonify( [{'device_id' : device[0], 'last_seen' : device[1] } for device in devices] )


@app.route(f"{API_VERSION}/events", methods=['GET'])
def get_events():
    device_id = request.args.get('device_id')

    if not device_id:
        return jsonify({"error": "Missing required query parameter: ?device_id="}), 400  # HTTP 400 Bad Request

    conn = sqlite3.connect('iot_database.db')
    c = conn.cursor()    
    c.execute("SELECT event_id, sensor_type, sensor_value, timestamp FROM Events WHERE device_id = ? ORDER BY timestamp DESC", (device_id,))
    events = c.fetchall()

    conn.close()

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



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


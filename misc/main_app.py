from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import threading
import time

app = Flask(__name__)
CORS(app)

# MySQL Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "smartpond_dbs"
}

# Insert function to save data to DB
def insert_sensor_data(sensor_id, data_value):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO sensor_logs (sensorID, tankID, data, datetime) VALUES (%s, 1, %s, NOW())"
        cursor.execute(query, (sensor_id, data_value))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print("Database error:", e)
        raise

# Store latest values in memory
latest_sensor_values = {
    "ph": None,
    "ppt": None
}

# Buffer to temporarily hold sensor values for averaging
buffered_sensor_data = {
    1: [],  # pH
    2: []   # ppt
}

# Lock for thread-safe operations
data_lock = threading.Lock()

# Background thread function to compute average every 1 minute
def average_and_insert():
    while True:
        time.sleep(60)  # Wait for 1 minute

        with data_lock:
            for sensor_id, values in buffered_sensor_data.items():
                if values:
                    avg = sum(values) / len(values)
                    try:
                        insert_sensor_data(sensor_id, avg)
                        print(f"Inserted average for sensor {sensor_id}: {avg}")
                    except Exception as e:
                        print(f"Failed to insert average for sensor {sensor_id}: {e}")
                    buffered_sensor_data[sensor_id].clear()  # Clear buffer after insert

@app.route("/esp32_flask", methods=["POST"])
def receive_data():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    ph_value = data.get("ph_value")
    ppt_value = data.get("ppt_value")
    rwl_value = data.get("rwl_value")
    ftl_value = data.get("ftl_value")
    phul_value = data.get("phul_value")
    phdl_value = data.get("phdl_value")
    ffl_value = data.get("ffl_value")

    # Ensure all values are present
    required_values = [ph_value, ppt_value, rwl_value, ftl_value, phul_value, phdl_value, ffl_value]
    if any(val is None for val in required_values):
        return jsonify({"error": "Missing one or more sensor data values"}), 400

    try:
        # Convert to float
        ph = float(ph_value)
        ppt = float(ppt_value)
        rwl = float(rwl_value)
        ftl = float(ftl_value)
        phul = float(phul_value)
        phdl = float(phdl_value)
        ffl = float(ffl_value)

        with data_lock:
            # Buffer data for averaging
            buffered_sensor_data[1].append(ph)
            buffered_sensor_data[2].append(ppt)

        # Save to latest memory store
        latest_sensor_values["ph"] = ph
        latest_sensor_values["ppt"] = ppt

        return jsonify({
            "message": "Data buffered successfully",
            "ph": ph,
            "ppt": ppt,
            "rwl": rwl,
            "ftl": ftl,
            "phul": phul,
            "phdl": phdl,
            "ffl": ffl
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid data format"}), 400
    except Error as db_error:
        return jsonify({"error": f"Database error: {db_error}"}), 500
    

    

# Return latest pH and ppt values (not from DB)
@app.route("/get_data_visualization", methods=["GET"])
def data_visualization():
    return jsonify({
        "labels": ["Latest"],
        "ph_values": [latest_sensor_values["ph"]],
        "ppt_values": [latest_sensor_values["ppt"]]
    })

if __name__ == "__main__":
    # Start the averaging thread
    threading.Thread(target=average_and_insert, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)

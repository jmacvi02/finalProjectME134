import csv
import os
from datetime import datetime
import paho.mqtt.client as mqtt

# MQTT Config
BROKER_IP = "10.247.137.123"
TOPIC = "data"
PORT = 1883

# Output CSV setup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"/Users/elihoulton/Desktop/5Spring/RoboticsME134/finalProjectME134/run_data/mqtt_data_{timestamp}.csv"
csv_file = open(filename, mode='w', newline='')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(["time", "left effort","right effort","x accel","y accel","z gyro",\
                     "rangefinder","encoder left","encoder right","vel left", "vel right"])

print(f"[INFO] Writing to {filename}")
# MQTT Callback: when message is received
def on_message(client, userdata, msg):
    try:
        decoded_msg = msg.payload.decode()
        print(f"[DATA] {decoded_msg}")
        row = decoded_msg.split(",")
        print(row)
        csv_writer.writerow(row)
    except Exception as e:
        print(f"[ERROR] Failed to write message: {e}")

# MQTT Callback: on connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected successfully")
        client.subscribe(TOPIC)
    else:
        print(f"[MQTT] Connection failed with code {rc}")

# MQTT Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"[INFO] Connecting to broker at {BROKER_IP}...")
client.connect(BROKER_IP, PORT, keepalive=1200)

# Loop forever
try:
    client.loop_forever()
except KeyboardInterrupt:
    csv_file.flush()  # Make sure data is written immediately
    print("\n[INFO] Interrupted by user, closing...")
    csv_file.close()
    client.disconnect()


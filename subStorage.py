import paho.mqtt.client as mqtt
import json
import csv
import sqlite3
from datetime import datetime
import os

# MQTT Settings
MQTT_BROKER = "35.175.188.98"  # Your broker IP
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/pub"

# Database settings
DB_NAME = "sensor_data.db"
CSV_FILE = "sensor_data.csv"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            temperature FLOAT,
            humidity FLOAT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_database(temperature, humidity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO sensor_readings (timestamp, temperature, humidity)
        VALUES (?, ?, ?)
    ''', (timestamp, temperature, humidity))
    conn.commit()
    conn.close()

def save_to_csv(temperature, humidity):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Temperature', 'Humidity'])
        writer.writerow([timestamp, temperature, humidity])

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        # Parse the JSON message
        data = json.loads(msg.payload.decode())
        temperature = data.get('temperature')
        humidity = data.get('humidity')

        print(f"Received - Temperature: {temperature}°C, Humidity: {humidity}%")

        # Save to database
        save_to_database(temperature, humidity)

        # Save to CSV
        save_to_csv(temperature, humidity)

        print("Data logged successfully")

    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    # Create database and table
    create_database()

    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to MQTT broker
    print(f"Connecting to MQTT broker at {MQTT_BROKER}")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start the loop
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Script terminated by user")
        client.disconnect()

if __name__ == "__main__":
    main()
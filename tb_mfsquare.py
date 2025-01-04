# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import json

class TBMFSquare:
    def __init__(self, broker_host, broker_port, access_token, keep_alive=60):
        self.client = mqtt.Client()
        self.client.username_pw_set(access_token)
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.keep_alive = keep_alive
        self.connected = False

        # Assign callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("Connected to MQTT broker.")
        else:
            print(f"Connection to MQTT broker failed with code {rc}.")
            self.connected = False

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        print("Disconnected from MQTT broker.")

    def on_publish(self, client, userdata, mid):
        print(f"Message with ID {mid} published.")

    def connect(self):
        try:
            print(f"Connecting to MQTT broker at {self.broker_host}:{self.broker_port}...")
            self.client.connect(self.broker_host, self.broker_port, self.keep_alive)
            self.client.loop_start()
            time.sleep(0.5)  # Short delay to ensure connection stability
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            self.connected = False

    def publish(self, topic, payload):
        if not self.connected:
            print("MQTT client is not connected. Aborting publish.")
            return

        try:
            result = self.client.publish(topic, json.dumps(payload), qos=1)
            # Warten, bis die Nachricht tatsächlich veröffentlicht wird
            while not result.is_published():
                time.sleep(0.1)
            print(f"MQTT message published successfully: {payload}")
        except Exception as e:
            print(f"Error publishing message: {e}")

    def disconnect(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
            print("Disconnected from MQTT broker.")
        except Exception as e:
            print(f"Error disconnecting from MQTT broker: {e}")

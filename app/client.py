# Paho MQTT Client implementation for SpineLine Desktop App
# Connects to 'test.mosquitto.org:8884'
# Subscribes to topic='IC.embedded/ΣϻβΔ_$¥$/#'

import time
# Import MQTT Client
import paho.mqtt.client as mqtt

class Client():
	def __init__(self):
		self.client = mqtt.Client()
		self.client.connected_flag = False

		# Link on_X methods
		self.client.on_connect=self.on_connect
		self.client.on_disconnect =self.on_disconnect

		self.topic = "IC.embedded/ΣϻβΔ_$¥$/#"

		# MQTT broker details
		self.broker_addr = "test.mosquitto.org" 
		self.broker_port = 8884


	def connect(self):
		# Encypt messages
		self.client.tls_set(ca_certs="cert/mosquitto.org.crt", certfile="cert/client.crt",keyfile="cert/client.key")
		# Connect to broker
		self.client.connect(self.broker_addr,port=self.broker_port)

	def on_connect(self, client, userdata, flags, rc):
		if rc==0:
			self.client.connected_flag = True
			print("connected OK Returned code=",rc)
		else:
			print("Bad connection Returned code=",rc)
			# try again
			self.connect()

	def disconnect(self):
		self.client.disconnect()

	def on_disconnect(self, client, userdata, rc):
		if rc==0:
			print("disconnected gracefully")
		else:
			# Unexpected disconnection
			print("disconnecting reason " +str(rc))
			# Main loop will attempt to reconnect later
		client.connected_flag=False

	def subscribe(self):
		rc=self.client.subscribe(self.topic, qos=2)
		# Check if subscription was successful
		if rc[0]==0:
			return
		else:
			print("Failed to subscribe, re-trying")
			self.subscribe()

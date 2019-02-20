# Paho MQTT Client implementation for SpineLine device
# Connects to 'test.mosquitto.org:8884'
# Subscribes to topic='IC.embedded/ΣϻβΔ_$¥$/_'+topic

import time
# Import MQTT Client
import paho.mqtt.client as mqtt

class Client():
	def __init__(self, topic):
		self.client = mqtt.Client()
		self.client.connected_flag = False

		# Link on_X methods
		self.client.on_connect=self.on_connect
		self.client.on_publish=self.on_publish

		self.topic = "IC.embedded/ΣϻβΔ_$¥$/_" + topic

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

	def on_disconnect(self, client, userdata, rc):
		print("disconnecting reason " +str(rc))
		client.connected_flag=False
		client.connect()

	# Publish payload to topic
	def publish(self, payload):
		MSG_INFO = self.client.publish(self.topic , payload)
		# if MSG_INFO.is_published() == False:
		# 	print("Message is not yet published.")
		# # Block until the message is published.
		# MSG_INFO.wait_for_publish()

	def on_publish(self, client, userdata, mid):
		print("mid: "+str(mid))

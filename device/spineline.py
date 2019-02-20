# SpineLine with 2 FlexSensors and 2 output LEDs

# Using an implementaiton of Paho MQTT Client
from client import Client

# Import standard libraries
import time
import json

# Import sensor I/O
from flexsensor import FlexSensor
import RPi.GPIO as GPIO

class SpineLine():
	def __init__(self, topic):
		# Instantiate and connect an MQTT client that will publish to topic
		self.client = Client(topic)
		self.client.connect()

		# FlexSensors
		# Top - ID=1
		# Threshold MinCurve = 0, Threshold MaxCurve = 35
		# ADC value to curve mapping: gradient, offset = -446.67,60200
		self.top_sensor 	= FlexSensor(1, 0, 35,-446.67,60200)
		# Bottom - ID=2
		# Threshold MinCurve = 0, Threshold MaxCurve = 20
		# ADC value to curve mapping: gradient, offset = -444.44,49000
		self.bottom_sensor 	= FlexSensor(2, 0, 20,-444.44,49000)
		# Sample period
		self.sample_period = 10 #seconds

		# LEDs
		# LED associated with top_sensor
		self.top_pin = 24
		# LED associated with bottom_sensor
		self.bottom_pin = 23
		self.init_LED()

		# Data logging and transfer
		self.top_log = []
		self.bottom_log = []
		self.top_avg = 0
		self.bottom_avg = 0
		self.payload = {}
		# Amount of sensor readings to send (per sensor)
		self.transfer_amount = 30

	# Main loop
	def run(self):
		# Count to transfer_amount
		count = 0
		while True:
			# Record a measurement of both top and bottom sensors
			self.record_curves()
			count += 1
			# Measurement Sample rate = 1/sample_period
			time.sleep(self.sample_period)

			# Data transfer after 30 measurements
			if count == self.transfer_amount:
				# Compress by taking average
				self.compress_logs()
				# Update LED outputs
				self.notify()
				# Create new message payload then publish
				self.package_logs()
				self.client.publish(self.payload)
				# Recount to transfer_amount
				count = 0


	# Take a measurement for both top and bottom FlexSensors, and add to log
	def record_curves(self):
		self.top_log.append( self.top_sensor.get_curve() )
		self.bottom_log.append( self.bottom_sensor.get_curve() )

	# Calculate average curves, then clear curve logs
	def compress_logs(self):
		# Calculate average 
		self.top_avg = sum(self.top_log) / len(self.top_log)
		self.bottom_avg = sum(self.bottom_log) / len(self.bottom_log)
		# Now clear to free up memory
		self.top_log.clear()
		self.bottom_log.clear()

	# Package data into a JSON dump to send via MQTT client
	# Adds a time-stamp as well
	def package_logs(self):
		# Time-stamp averages with current hour and minute
		time_stamp = time.strftime("%H:%M", time.localtime())
		top_stamp = (time_stamp, self.top_avg)
		bottom_stamp = (time_stamp, self.bottom_avg)

		# New payload in JSON format
		self.payload = json.dumps( [{'name':'top sensor', 'curverecord':top_stamp},
							{'name':'bottom sensor', 'curverecord':bottom_stamp}] )


	# LED methods
	def init_LED(self):
		# BCM naming convention
		GPIO.setmode(GPIO.BCM)
		# Diable ptinting of GPIO warnings
		GPIO.setwarnings(False)
		# Define as output
		GPIO.setup(self.top_pin, GPIO.OUT)
		GPIO.setup(self.bottom_pin, GPIO.OUT)
		# Initially LEDs are switched off
		GPIO.output(self.top_pin, GPIO.LOW)
		GPIO.output(self.bottom_pin, GPIO.LOW)

	# Switch on LED if average curve out of range
	def notify(self):
		# LED for top sensor
		# if average is in range - turn LED off
		if self.top_sensor.in_range(self.top_avg):
			GPIO.output(self.top_pin, GPIO.LOW)
		# else, turn LED on
		else:
			GPIO.output(self.top_pin, GPIO.HIGH)

		# LED for bottom sensor
		if self.bottom_sensor.in_range(self.bottom_avg):
			GPIO.output(self.bottom_pin, GPIO.LOW) #off
		else:
			GPIO.output(self.bottom_pin, GPIO.HIGH) #on

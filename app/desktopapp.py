# Desktop application to plot data from a SpineLine device
# Incorporates a tkinter Frame for the GUI
# and an MQTT Client to recieve messages form the device

import json

import tkinter
from window import Window
from client import Client

# Inherit Window - easy access to update screen on_message
class DesktopApp(Window):
	def __init__(self, master):
		super(DesktopApp, self).__init__(master)
		# Connection to Broker
		self.client = Client()
		self.client.connect()
		# Bind MQTT client on_message
		self.client.client.on_message=self.on_message
		self.client.subscribe()

		# Data history
		# fmt = [time_stamp],[avg_curve]
		self.top_history = [[],[]]
		self.bottom_history = [[],[]]
		# reference values (degrees)
		self.top_ref = 25
		self.bottom_ref = 10

		# Set MQTT Client loop to start as soon as Window opens
		self.master.after(0, self.client_loop)

	# Call MQTT client loop method every 5s
	# expecting to recieve a message every 300 seconds
	# keeps GUI responsive as loop() is blocking
	def client_loop(self):
		self.client.client.loop()
		self.master.after(5000, self.client_loop)

	# Call Window.plotter() to update graph
	def plot(self):
		# Plot top and bottom sesnor history
		self.plotter(self.top_history, self.bottom_history, self.top_ref, self.bottom_ref)

	# Callback method when the MQTT client recieves a message
	# Updates graph plot with new data
	def on_message(self, client, userdata, message):
		print("Recieved a log")
		# Load JSON into Python data types
		payload = json.loads(message.payload)
		top_record, bottom_record = payload[0]['curverecord'], payload[1]['curverecord']

		# Add to history
		self.top_history[0].append(top_record[0]) # time_stamp
		self.top_history[1].append(top_record[1]) # curve
		self.bottom_history[0].append(bottom_record[0]) # time_stamp
		self.bottom_history[1].append(bottom_record[1]) # curve

		# Re-plot
		self.plot()

	# Clear and reset graph
	# Overriden to also clear data stored
	def clear_graph(self):
		self.top_history = [[],[]]
		self.bottom_history = [[],[]]
		# reference line
		self.top_ref = []
		self.bottom_ref = []
		self.ax.cla()
		self.set_axis()
		self.graph.draw()

	# Disconnect then close the application
	def safe_exit(self):
		# Disconnect
		self.client.disconnect()
		# Close application
		exit()

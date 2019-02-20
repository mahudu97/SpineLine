# Class for a sensor to interface with ADS1115 ADC via I2C

# Import libraries
import smbus
import time

class ADC():
	def __init__(self):
		self.bus = smbus.SMBus(1)
		# Base address of ADS1115
		self.base_addr = 0x48
		# Configuration and Convertion register addresses
		self.con_reg   = 0x00
		self.cfg_reg   = 0x01

	# Read the value from Analog-INput-X (returned as an integer)
	# ain - 3 bit binary value
	#   refer to ADS1115 datasheet section on configuration register
	def read_AINX(self, ain):
		# Start an AD conversion
		self.start_conversion(ain)
		# Wait for conversion to finish (0.125 sampling period)
		time.sleep(0.15)

		# Read from 16-bit conversion register
		data = self.bus.read_i2c_block_data(self.base_addr,self.con_reg,2)

		# Convert byte data to Python Int
		value = int(data[0] + (data[1] << 8) )
		return value

	# Perform a single AD conversion
	# Result stored in ADS1115's conversion register
	def start_conversion(self, ain):
		# Build up 16-bit command to place in Config regiter
		# MSByte
		# Convert(bit-7) - start a conversion
		# AINX(bits-6:4) - select analog input
		# PGA=1(bit-3:1) - programmable gain = 1
		# Single-Shot(bit-1) - Stop after one conversion
		MSB = 0b10000011 | (ain << 4)

		# LSByte
		# #SPS(bits-7:5) - sampling rate = 8Hz
		# COMP_Default(bits-4:0), Disable Comparator
		LSB = 0b00000011

		# Write to config register
		# Send MSB first
		config = [MSB, LSB]
		self.bus.write_i2c_block_data(self.base_addr, self.cfg_reg, config)

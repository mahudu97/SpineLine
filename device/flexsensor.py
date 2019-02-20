# Class to interact with a FlexSensor
# Supports 2 instances

# Connected to an ADS1115
from adc import ADC

class FlexSensor():
	def __init__(self, id, minc, maxc, m , c):
		self.id = id
		# Connection to ADS1115
		self.adc = ADC()

		# Threshold curves
		self.min_curve = minc
		self.max_curve = maxc

		# Linear approximation of ADC conversion to curve in degrees
		# angle = (adc_value - offset)/gradient
		self.gradient = float(m)
		self.offset = float(c)

	# Map ID of FlexSensor instance to an analog input pin
	def map_id(self):
		# ID=1 -> AIN0
		if self.id == 1:
			return 0b100
		# ID=2 -> AIN2
		elif self.id == 2:
			return 0b110

	# Get the current approximation of how curved the FlexSensor is
	def get_curve(self):
		# Start a conversion on the ADS1115
		val = self.adc.read_AINX(self.map_id())

		# Convert into degrees
		curve = (val - self.offset)/self.gradient

		# Lower limit = 0, Upper Limit = 120 degrees
		curve = min(120,max(0,curve))
		return curve

	# Check if input 'curve' is within the min and max threshold curves
	def in_range(self, curve):
		return curve >= self.min_curve \
				and curve <= self.max_curve

# Import the IoT product class
from spineline import SpineLine

# Instantiate a SpineLine object,
# which publishes MQTT messages to
# topic = "IC.embedded/ΣϻβΔ_$¥$/SpineLine_001"
spineline_001 = SpineLine("001")

# Enter main loop, starts taking measurements
spineline_001.run()

'''
Reads and prints the ADC input in single conversion mode, 
every 1 second
'''

# Import the ADCRP2 class
from ADCRP2 import ADCRP2
import time

ADCRP2.gpio_init(26) # Initialize pin 26 for ADC input
ADCRP2.init() # Initialize the ADC
ADCRP2.select_input(0) # Select the channel 0 (GPIO 26) for ADC input

while(True):
  print(ADCRP2.read())
  time.sleep(1)

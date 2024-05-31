'''
This example shows configuring free-running ADC using 
DMA to transfer data to a sample buffer
'''

# Import the ADC and DMA modules
from ADCRP2 import ADCRP2
from rp2 import DMA


no_of_samples = 10_000 # Total number of samples
sample_buffer = bytearray(no_of_samples) # Buffer to store ADC results

ADCRP2.init_gpio(26) # Initialize pin 26 for ADC input
ADCRP2.init() # Initialize the ADC hardware
ADCRP2.select_input(0) # Select the channel 0 (pin 26) as the MUX input

'''
Setup the ADC FIFO
en = True => Enable the ADC FIFO, which is required for DMA transfer
dreq_en = True => Enable the data request to DMA
dreq_thresh = 1 => Call the DMA to transfer data after each conversion
error_in_fifo = False => 
byte_shift = True => Ignore the 4 LSBs and shift the 12-bit number to fit a byte for lesser memory
'''
ADCRP2.fifo_setup(en = True, dreq_en = True, dreq_thresh = 1, error_in_fifo = False, byte_shift = True)

ADCRP2.set_clkdiv(48000) # Set the clock divider to 48000, which corresponds to 1 kSps


d = rp2.DMA() # Start setting up the DMA channel

'''
Create DMA configuration
size = 0 => 1 byte transfer per request
inc_read = False => Do not increment the read address, as the address is of ADC FIFO
treq_sel = ADCRP2.TREQ => Transfer request from ADC
'''
c = d.pack_ctrl(size = 0, inc_read = False, treq_sel = ADCRP2.TREQ)
'''
Configure the DMA
read = ADCRP2.FIFO => Read from ADC FIFO
write = sample_buffer => Write to sample buffer
count = no_of_samples => Total no of transfers
ctrl = c => Use the previously created configuration
trigger = False => Do not trigger DMA immediately
'''
d.config(read = ADCRP2.FIFO, write = sample_buffer, count = no_of_samples, ctrl = c, trigger = False)


ADCRP2.run(True) # Put the ADC in continuous sampling mode

d.active(1) # Activate the DMA to start data transfer
# Wait for data transfer to finish. Should take about 10 seconds
while(d.active()):
    pass

# Close the DMA channel and put ADC in single shot mode
d.close()
ADCRP2.run(False)

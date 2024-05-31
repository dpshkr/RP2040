'''
This example shows configuring free-running ADC using 
DMA to transfer data to a sample buffer using all 12-bit 
resolution
'''

# Import the ADC and DMA modules
from ADCRP2 import ADCRP2
from rp2 import DMA

'''
Each sample is 12 bit, so we need to use 2 bytes for a sample.
'''
no_of_samples = 10_000 # Total number of samples
sample_buffer = bytearray(2*no_of_samples) # Buffer to store ADC results

ADCRP2.init_gpio(26) # Initialize pin 26 for ADC input
ADCRP2.init() # Initialize the ADC hardware
ADCRP2.select_input(0) # Select the channel 0 (pin 26) as the MUX input

'''
Setup the ADC FIFO
en = True => Enable the ADC FIFO, which is required for DMA transfer
dreq_en = True => Enable the data request to DMA
dreq_thresh = 1 => Call the DMA to transfer data after each conversion
error_in_fifo = False => Do not set the error bit 
byte_shift = False => Do not shift the 4 LSBs, as we want all 12 bits 
'''
ADCRP2.fifo_setup(en = True, dreq_en = True, dreq_thresh = 1, error_in_fifo = False, byte_shift = False)

ADCRP2.set_clkdiv(48000) # Set the clock divider to 48000, which corresponds to 1 kSps


d = rp2.DMA() # Start setting up the DMA channel

'''
Create DMA configuration
size = 1 => 2-byte transfer per request
inc_read = False => Do not increment the read address, as the address is of ADC FIFO
treq_sel = ADCRP2.TREQ => Transfer request from ADC
'''
c = d.pack_ctrl(size = 1, inc_read = False, treq_sel = ADCRP2.TREQ)
'''
Configure the DMA
read = ADCRP2.FIFO => Read from ADC FIFO
write = sample_buffer => Write to sample buffer
count = no_of_samples => Total no of transfers
ctrl = c => Use the previously created configuration
trigger = False => Do not trigger DMA immediately
'''
d.config(read = ADCRP2.FIFO, write = sample_buffer, count = no_of_samples, ctrl = c, trigger = False)


ADCRP2.run(True) # Put the ADC in continuous sampling mode.

d.active(1) # Activate the DMA to start data transfer
# Wait for the data transfer to finish. Should take about 10 seconds
while(d.active()):
    pass

# Close the DMA channel and put ADC in single shot mode
d.close()
ADCRP2.run(False)

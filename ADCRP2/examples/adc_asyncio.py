'''
Use asyncio to concurrently transfer ADC data usin DMA 
and do some other task
'''

import asyncio
import rp2
from ADCRP2 import ADCRP2
import machine

# Setup ADC and DMA channel 
ADCRP2.init()
ADCRP2.init_gpio(26)
ADCRP2.select_input(0)
ADCRP2.fifo_setup(True, True, 1, False, True)
ADCRP2.set_clkdiv(48000)
no_of_samples = 20_000
sample_buffer = bytearray(no_of_samples)
d = rp2.DMA()
c = d.pack_ctrl(size = 0, inc_read = False, treq_sel = ADCRP2.TREQ)
d.config(read = ADCRP2.FIFO, write = sample_buffer, count = no_of_samples, ctrl = c, trigger = False)
led = machine.Pin(25, machine.Pin.OUT)

async def adc_read():
    ADCRP2.run(True)
    d.active(True)
    while (d.active()):
        '''
        Yeild control to the scheduler.
        Based on sampling rate and buffer size, 
        a higher sleep time might improve the performance
        '''
        await asyncio.sleep(0)
    ADCRP2.run(False)
    ADCRP2.fifo_drain()
    
async def blink_led():
    for i in range(0,100):
        led.value(1)
        await asyncio.sleep(0.1)
        led.value(0)
        await asyncio.sleep(0.1)

async def main():
    # Start reading the ADC
    task1 = asyncio.create_task(adc_read())
    # Start blinking the LED
    task2 = asyncio.create_task(blink_led())
  
    # Wat for both tasks to finish
    await task1
    await task2

asyncio.run(main())

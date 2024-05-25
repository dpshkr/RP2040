import machine
import time
import rp2

def setup_adc(Fs):
    clkdiv = (48_000_000 / Fs) - 1
    # Clear the single shot conversion mode - OPTIONAL
    machine.mem32[0x4004C000] = machine.mem32[0x4004C000] & ~(1 << 2)
    # Setup continuous sampling mode
    machine.mem32[0x4004C000] = machine.mem32[0x4004C000] | (1 << 3)
    # Clock Divider set sampling rate to 1 kHz
    machine.mem32[0x4004C010] = int(clkdiv * (1 << 8))
    # SETUP FIFO
    # Set the DREQ threshold to 1, so that DMA is called as soon one conversion is done
    machine.mem32[0x4004C008] = machine.mem32[0x4004C008] | (1 << 24)
    # Enable shifting the 12 bits to a byte for easy DMA transfer
    machine.mem32[0x4004C008] = machine.mem32[0x4004C008] | (1 << 1)
    # Enable the DREQ
    machine.mem32[0x4004C008] = machine.mem32[0x4004C008] | (1 << 3)
    # Enable the FIFO
    machine.mem32[0x4004C008] = machine.mem32[0x4004C008] | (1 << 0)
    #


Fs = 1000

adc = machine.ADC(machine.Pin(26))
setup_adc(Fs)
sample_buffer = bytearray(25000)
d = rp2.DMA()
led = machine.Pin(25, machine.Pin.OUT)
print(d.channel)
# size = 0 => Byte transfer, no read increment, treq_sel=36 => ADC dreq
c = d.pack_ctrl(size=0, inc_read = False, treq_sel = 36)
d.config(read=0x4004C00C, write=sample_buffer, count = len(sample_buffer), ctrl=c, trigger=False)
#time.sleep(1)

for i in range(0,1):
    d.active(1)
    led.value(1)
    while d.active():
        pass
    #print(sample_buffer)
    d.config(read=0x4004C00C, write=sample_buffer, count = len(sample_buffer), ctrl=c, trigger=False)
    print("===================================")
    time.sleep(0.2)
d.close()
with open('samples1.bin', 'wb') as f:
    f.write(sample_buffer)

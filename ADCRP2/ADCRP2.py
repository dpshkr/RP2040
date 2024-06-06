import machine

class ADCRP2:
    
    TREQ = 36
    FIFO = 0x4004C00C
    
    @staticmethod
    def init():
        # Reset ADC
        machine.mem32[0x4000C000] = machine.mem32[0x4000C000] | (1 << 0)
        machine.mem32[0x4000C000] = machine.mem32[0x4000C000] & ~(1 << 0)
        while(~(machine.mem32[0x4000C008]) & (1 << 0 )):
            pass
        # Enable the ADC
        machine.mem32[0x4004C000] = machine.mem32[0x4004C000] | (1 << 0) 
        # wait for the ADC to be ready
        while (not (machine.mem32[0x4004C000] & (1 << 8))):
            pass
    
    @staticmethod
    def get_selected_input():
        return (machine.mem32[0x4004C000] & (7 << 12))
    
    @staticmethod
    def init_gpio(pin):
        io_bank_addr = 0x40014004 + pin*8
        # Select NULL function to make output driver hi-Z
        machine.mem32[io_bank_addr] = 0x1F
        pads_bank_addr = 0x4001C000 + (pin + 1)*4
        # Disable pull up and pull down respectively
        machine.mem32[pads_bank_addr] = machine.mem32[pads_bank_addr] & ~(1 << 3)
        machine.mem32[pads_bank_addr] = machine.mem32[pads_bank_addr] & ~(1 << 2)
        # Digital Digital Input
        machine.mem32[pads_bank_addr] = machine.mem32[pads_bank_addr] & ~(1 << 6)
    
    @staticmethod
    def select_input(input_):
        machine.mem32[0x4004C000] = machine.mem32[0x4004C000] | (input_ << 12)
    
    @staticmethod
    def read():
        # Assert the start once bit
        machine.mem32[0x4004C000] = machine.mem32[0x4004C000] | (1 << 2)
        # Wait till ADC is not ready (for another conversion)
        while (not (machine.mem32[0x4004C000] & (1 << 8))):
            pass
        # Return the result
        return machine.mem32[0x4004C004]
    
    @staticmethod
    def set_roundrobin(input_mask):
        machine.mem32[0x4004C000] = machine.mem32[0x4004C000] | (input_mask << 16)
    
    @staticmethod
    def fifo_setup(en, dreq_en, dreq_thresh, error_in_fifo, byte_shift):
        if (en):
            machine.mem32[0x4004C008] = machine.mem32[0x4004C008] | (1 << 0)
        else:
            machine.mem32[0x4004C008] = machine.mem32[0x4004C008] & ~(1 << 0)
        if (byte_shift):
            machine.mem32[0x4004C008] = machine.mem32[0x4004C008] | (1 << 1)
        else:
            machine.mem32[0x4004C008] = machine.mem32[0x4004C008] & ~(1 << 1)
        if (error_in_fifo):
            machine.mem32[0x4004C008] = machine.mem32[0x4004C008] | (1 << 2)
        else:
            machine.mem32[0x4004C008] = machine.mem32[0x4004C008] & ~(1 << 2)
        if (dreq_en):
            machine.mem32[0x4004C008] = machine.mem32[0x4004C008] | (1 << 3)
        else:
            machine.mem32[0x4004C008] = machine.mem32[0x4004C008] & ~(1 << 3)
        
        machine.mem32[0x4004C008] = machine.mem32[0x4004C008] | (dreq_thresh << 24)
    
    @staticmethod
    def run(run):
        if (run):
            # Set the start many bit
            machine.mem32[0x4004C000] = machine.mem32[0x4004C000] | (1 << 3)
        else:
            # Clear the start many bit
            machine.mem32[0x4004C000] = machine.mem32[0x4004C000] & ~(1 << 3)
            
    
    @staticmethod
    def set_clkdiv(clkdiv):
        machine.mem32[0x4004C010] = machine.mem32[0x4004C010] | (int(clkdiv) << 8)
    
    @staticmethod
    def get_selected_input():
        return (machine.mem32[0x4004C000] & (7 << 12)) >> 12
    
    @staticmethod
    def set_temp_sensor_enabled(enable):
        if (enable):
            machine.mem32[0x4004C000] = machine.mem32[0x4004C000] | (1 << 1)
        else:
            machine.mem32[0x4004C000] = machine.mem32[0x4004C000] & ~(1 << 1)
    
    @staticmethod
    def fifo_is_empty():
        return bool((machine.mem32[0x4004C008] & (1 << 8)) >> 8)
    
    @staticmethod
    def fifo_get_level():
        return ((machine.mem32[0x4004C008] & (15 << 16)) >> 16)
    
    @staticmethod
    def fifo_get():
        return (machine.mem32[0x4004C00C] & 4095)
    
    @staticmethod
    def fifo_get_blocking():
        while(ADCRP2.fifo_is_empty()):
            pass
        return ADCRP2.fifo_get()
    
    @staticmethod
    def fifo_drain():
        # Potentially there is still a conversion in progress -- wait for this to complete before draining
        while (not bool(machine.mem32[0x4004C000] & (1 << 8))):
            pass
        while (not ADCRP2.fifo_is_empty()):
            ADCRP2.fifo_get()

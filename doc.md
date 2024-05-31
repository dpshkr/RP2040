## `class ADCRP2`

12-bit analog to digital converter.
All the functions provided here correspond to the C SDK. 
For more details refer to the C SDK.

* `ADCRP2.init()` :  Initialise the ADC HW.
* `ADCRP2.gpio_init(gpio)`: Initialise the `gpio` for use as an ADC pin.
* `ADCRP2.get_selected_input()`: Get the currently selected ADC input channel.
* `ADCRP2.set_round_robin (input_mask)`:  Round Robin sampling selector.
* `ADCRP2.set_temp_sensor_enabled (enable)`:  Enable the onboard temperature sensor.
* `ADCRP2.read()`: Perform a single conversion.
* `ADCRP2.run(run)`:  Enable or disable free-running sampling mode.
* `ADCRP2.set_clkdiv(clkdiv)`: Set the ADC Clock divisor.
* `ADCRP2.fifo_setup (en, dreq_en, dreq_thresh, err_in_fifo, byte_shift)`:  Setup the ADC FIFO.
* `ADCRP2.fifo_is_empty()`: Check FIFO empty state.
* `ADCRP2.fifo_get_level()`: Get the number of entries in the ADC FIFO.
* `ADCRP2.fifo_get()`:  Get ADC result from FIFO.
* `ADCRP2.adc_fifo_get_blocking()`: Wait for the ADC FIFO to have data.
* `ADCRP2.fifo_drain ()`:  Drain the ADC FIFO.
* `ADCRP2.adc_irq_set_enabled(enabled)`: Enable/Disable ADC interrupts. 

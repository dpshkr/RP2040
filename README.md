# RP2040
Micropython classes for controlling RP2040 peripherals. 

The peripheral classes provided by the Micropython standard library (in the `machine` module) are limited 
and do not provide all the functionality offered by the real hardware.
Due to significant variations in functionalities provided by various hardware manufacturers (beyond the basics), ,
it might not be possible for the standard library to incorporate all the differences with a consistent API across various ports.

## Design of the library

This library mimics the RP2040 C SDK in both implementation and API.
Each peripheral class has a bunch of static methods having a one to one correspondence with the C SDK.
All that these methods do is to set or get the appropriate status and configuration registers/bits.


# Micropython / Circuitpython Builds for ADIY FLY Board

Many custom boards for RP2040 face the problem of delayed oscillator stabilization which results in the 
failure of any firmware to run after any kind of reset.
This can be solved by increasing the oscillator startup delay in the SDK.
Since the PICO micro/circuit python images are compiled without the delay, they may fail to work.
This folder contains firmware compiled with increased delay and has been tested to solve the problem/ 

## Compile instructions for C SDK

In the `pico-sdk` folder, go to `src/boards/include/boards` folder and add the following lines 
in the `pico.h` file (before the final `#endif` statement):

```
#ifndef PICO_XOSC_STARTUP_DELAY_MULTIPLIER
#define PICO_XOSC_STARTUP_DELAY_MULTIPLIER 128
#endif
```

Also change the `PICO_FLASH_SIZE_BYTES` in the `pico.h` folder 
to `(4 * 1024 * 1024)` for informing the SDK about the higher flash size.

## Compile instructions for Micropython

Download the latest stable `tar.xz` source code from Micropython website.
This archive has the SDK already included. 
Extract the archive and go to `lib/pico-sdk` folder and follow the instructions as above.

To change the board name at the prompt (optional), go to `ports/rp2/boards/RPI_PICO` folder and 
and edit the `mpconfigboard.h` to change the `#define MICROPY_HW_BOARD_NAME` definition to `ADIY FLY`.

Go to root micropython folder and run `make -C mpy-cross`.
Then go to `ports/rp2` folder and run `make` command. 

## Compile instructions for Circuitpython

Follow the instructions from the Circuitpython guide to download the circuitpython source code and included pico-sdk.
Inside the `ports/raspberrypi/boards/raspberry_pi_pico` folder, add the following line in the file `pico-sdk-configboard.h`

```
#define PICO_XOSC_STARTUP_DELAY_MULTIPLIER 128
```

Also make the changes mentioned for C/C++ SDK above to edit `pico.h` file 
in `ports/raspberrypi/sdk/src/boards/include/boards` folder.

To change the board name at the prompt (optional), go to `ports/raspberrypi/boards/raspberry_pi_pico` folder and 
and edit the `mpconfigboard.h` to change the `#define MICROPY_HW_BOARD_NAME` definition to `ADIY FLY`.

Finally compile with `make BOARD=raspberry_pi_pico`.

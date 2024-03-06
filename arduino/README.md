# Arduino Firmware

This part of the code is designed for installation on a typical Arduino UNO with an ATMEGA328P chip.

It utilises the AVR build tools and the [AVR Libc](https://www.nongnu.org/avr-libc/) library.

Approach and insight on some decisions is listed underneath. In-detail documentation for each function can be found inside the code as comments.

## Approach

In brief, the code performs the following tasks:

1. The code entry point is `src/main.c`, at `main()`.
2. Upon entry, the code initialises the UART serial port available via the USB-B connection on the Arduino UNO. It is alternatively possible to use pins 0 and 1.
3. After initialisation, it reads in bytes from the serial port until a `0` character is encountered, at which point it stops. On reading each byte, it immediately stores it in the EEPROM.
4. There is a short delay of 500ms for the PC end to prepare for receiving data.
5. The program goes through each byte in the EEPROM, and sends it back through the UART port, byte by byte, until a `0` character is encountered, at which point it stops.
6. Finally, the `main()` function exits.

## Insight on Design Decisions

### Utilisation of AVR libc for EEPROM

AVR Libc provides useful functions - somewhat of an API - for the EEPROM, which facilitates simple communication with it. It is alternatively possible to directly address the hardware (as is done on systems where there is no convenient Libc available), but it is ideal to use existing, bug-free and widely supported code for crucial tasks like these.

### Stopping at the `0` character

This is due to the common format used for ASCII strings. Considering the text also had multiple lines, typical separators like `\n`/`\r` were out of the picture, leaving only the terminating `0` character as a viable and compatible stopping character.

## Build instructions

These instructions are written for Ubuntu 20.04 LTS, however they may be adaptable to other versions/operating systems.

```bash
# Clone the Git repo
git clone https://github.com/ryuukumar/nymble-task
cd nymble-task

# Download requirements
sudo apt install gcc-avr avr-libc avrdude

# Build
make build
make install # Optional, this installs it into the Arduino
```

The port on which the Arduino is connected is set in the Makefile. In case you are running this, please set the port appropriately before building.

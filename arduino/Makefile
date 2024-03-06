
TARGET = main
MCU = atmega328p
F_CPU = 16000000UL
PROGRAMMER = arduino
PORT = /dev/ttyACM0

CC = avr-gcc
OBJCOPY = avr-objcopy
INCLUDE = include

CFLAGS = -DF_CPU=$(F_CPU) -mmcu=$(MCU) -Os -Iinclude
LDFLAGS = -DF_CPU=$(F_CPU) -mmcu=$(MCU) -Os -Iinclude
AVRDUDEFLAGS = -p $(MCU) -c $(PROGRAMMER) -P $(PORT)

SRC = $(wildcard src/*.c)
OBJ = $(SRC:src/%.c=build/%.o)

build/$(TARGET).hex: build/$(TARGET).elf
	$(OBJCOPY) -O ihex $< $@

build/$(TARGET).elf: $(OBJ)
	$(CC) $(LDFLAGS) $(OBJ) -o $@

build/%.o: src/%.c
	@mkdir -p build
	$(CC) $(CFLAGS) -c $< -o $@
	
build: build/$(TARGET).hex
	@echo "Build completed."

install: build
	avrdude $(AVRDUDEFLAGS) -U flash:w:build/$(TARGET).hex
	@echo "Install completed."

clean:
	rm -rf build

.PHONY: clean

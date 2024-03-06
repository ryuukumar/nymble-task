
//
//	MAIN.C
//	Entry point and main body of the firmware.
//


#include <avr/eeprom.h>
#include <util/delay.h>

#include <uart_driver.h>

#define EEPROM_SIZE 1024

// Read into EEPROM from UART
int read_into_eeprom(void) {
	uint16_t eepromptr = 0;
	
	while(1) {
		char c = uart_receive();
		eeprom_write_byte((const uint8_t*) eepromptr, (uint8_t)c);
		eepromptr++;
		if (eepromptr >= 1024) eepromptr = 1024;
		if (c == 0) break;
	}
	
	return eepromptr;
}

// Read out the EEPROM contents to UART
void return_eeprom_via_uart (uint16_t content_size) {
	for (uint16_t i=0; i<content_size; i++) {
		char c = eeprom_read_byte((const uint8_t*)i);
		uart_transmit(c);
	}
}

// Entry point
int main() {
	uart_init();
	
	uint16_t content_size = read_into_eeprom();
	_delay_ms(500);
	return_eeprom_via_uart(content_size);
	
	return 0;
}

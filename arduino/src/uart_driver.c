
//
//	UART_DRIVER.C
//	Driver for UART communication.
//


#include <avr/io.h>

#define BAUD 2400
#define BRC ((F_CPU/16/BAUD) - 1)

// Initialise UART
void uart_init() {
    UBRR0H = (BRC >> 8) & 0xF;
    UBRR0L = BRC & 0xFF;

    UCSR0A = 0;
    UCSR0B = (1 << TXEN0) | (1 << RXEN0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

// Transmit a byte via UART
void uart_transmit(char data) {
    while (!(UCSR0A & (1 << UDRE0)));
    UDR0 = (uint8_t)data;
}

// Receive a byte from UART
char uart_receive() {
    while (!(UCSR0A & (1 << RXC0)));
    return (char)UDR0;
}

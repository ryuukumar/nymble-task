
#ifndef UART_DRIVER_H
#define UART_DRIVER_H

extern void uart_init(void);
extern void uart_transmit(char);
extern char uart_receive(void);

#endif


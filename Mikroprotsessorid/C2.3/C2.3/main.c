/*
 * C2.3.c
 *
 * Created: 20.05.2021 13:44:36
 * Author : ralfs
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>

void kontrolli();
void saada(char num);
void viivis(uint16_t ms);


int main(void) {
	
	//UART init
	UBRR1 = 12;
	UCSR1B = (1 << TXEN1);
	UCSR1C = (1 << UCSZ11)|(1 << UCSZ10);
	//LED init
	DDRA = 0x02;
	//Timer init
	TCNT0 = 0x00;
	TIMSK0 = (1 << TOIE1); //Overflow interrupt
	TCCR0B = (1 << CS02)|(1 << CS00); //Prescaler 1024
	sei(); //Enable global interrupts by setting SREG
	
	while (1) {
		saada('R');
		saada('a');
		saada('l');
		saada('f');
		viivis(1000);
	}
}

ISR(TIMER0_OVF_vect) {
	PINA = 0xff;
}

void kontrolli() {
	while(!(UCSR1A & (1 << UDRE1)));
		 
}

void saada(char num) {
	kontrolli();
	UDR1 = num;
}

void viivis(uint16_t ms) {
	for(uint16_t j = 0; j < ms; j++) {
		for(uint8_t i = 0; i < 170; i++) {
			asm volatile("nop");
			asm volatile("nop");
			asm volatile("nop");
		}
	}
}


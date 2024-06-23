/*
 * C1.4.c
 *
 * Created: 06.05.2021 11:46:34
 * Author : ralfs
 */ 

#include <avr/io.h>
#include <inttypes.h>

void paus_05s(uint16_t);
void S(void);
void O(void);

int main(void)
{
	DDRA = 0xff;
	
	//S
	S();
	paus_05s(1000);

	
	//O
	O();
	paus_05s(2000);
	
	
	
	//S
	S();
	paus_05s(1000);
	
}

void paus_05s(uint16_t ms) {
	for(uint16_t j = 0; j < ms; j++)
	{for(uint16_t i = 0; i < 200; i++) {
			asm volatile("nop");
			asm volatile("nop");
		}
	}
}

void S(void) { //S
	PORTA = 0xff;
	paus_05s(500);
	PORTA = 0x00;
	paus_05s(500);
	
	PORTA = 0xff;
	paus_05s(500);
	PORTA = 0x00;
	paus_05s(500);
	
	PORTA = 0xff;
	paus_05s(500);
	PORTA = 0x00;
	paus_05s(500);
}

void O(void) { //o
	PORTA = 0xff;
	paus_05s(500);
	paus_05s(500);
	paus_05s(500);
	PORTA = 0x00;
	paus_05s(500);
	
	PORTA = 0xff;
	paus_05s(500);
	paus_05s(500);
	paus_05s(500);
	PORTA = 0x00;
	paus_05s(500);
	
	PORTA = 0xff;
	paus_05s(500);
	paus_05s(500);
	paus_05s(500);
	PORTA = 0x00;
	paus_05s(500);
}

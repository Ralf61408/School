/*
 * C1.2.c
 *
 * Created: 22.04.2021 13:31:49
 * Author : ralfs
 */ 

#include <avr/io.h>
#include <inttypes.h>

void paus_05s();
void S();
void O();
void paus();

int main(void)
{
	DDRA = 0xff;
	
	//S
	S();
	
	paus();
	
	//O
	O();
	
	paus();
	
	//S
	S();
	
	paus();
	
}

void paus_05s() {
	uint16_t i;
	uint16_t j;
	
	for(i = 15; i != 0; i--)
	{
		for(j = 30000; j!= 0; j--) {
			asm("nop");
		}
	}
}

void S() { //S
	PORTA = 0xff;
	paus_05s();
	PORTA = 0x00;
	paus_05s();
	
	PORTA = 0xff;
	paus_05s();
	PORTA = 0x00;
	paus_05s();
	
	PORTA = 0xff;
	paus_05s();
	PORTA = 0x00;
	paus_05s();
}

void O() { //o
	PORTA = 0xff;
	paus_05s();
	paus_05s();
	paus_05s();
	PORTA = 0x00;
	paus_05s();
	
	PORTA = 0xff;
	paus_05s();
	paus_05s();
	paus_05s();
	PORTA = 0x00;
	paus_05s();
	
	PORTA = 0xff;
	paus_05s();
	paus_05s();
	paus_05s();
	PORTA = 0x00;
	paus_05s();
}

void paus() {
	paus_05s();
}
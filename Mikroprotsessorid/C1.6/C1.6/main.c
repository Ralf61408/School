/*
 * C1.6.c
 *
 * Created: 06.05.2021 13:40:23
 * Author : ralfs
 */ 

#include <avr/io.h>
void viivitus(uint16_t);


int main(void){
	DDRA = 0xff;
	PORTF = 1 << PINF5;
	PORTF |= 1 << PINF3;
    /* Replace with your application code */
	
	MCUCR |= 1 << JTD;
	MCUCR |= 1 << JTD;
    while (1) 
	//vasakule
    {if (!(PINF & 1 <<PINF5)){
		PORTA = PORTA << 1;
		
		if (PORTA == 0x00){
			PORTA = 0x01;
		}
		
		viivitus(500);
		
		while (!(PINF & (1 << PINF5))){
			
		}
		 }
		//paremale
		
		if (!(PINF & 1 <<PINF3)){
			PORTA = PORTA >> 1;
			
			if (PORTA == 0x00){
				PORTA = 0x80;
			}
			
			viivitus(500);
			
			while (!(PINF & 1 << PINF3)){
		
			}
		}
	}
}

void viivitus(uint16_t ms){
	for(uint16_t j = 0; j < ms; j++) {
		for(uint16_t i = 0; i < 200; i++) {
			asm volatile("nop");
			asm volatile("nop");
		}
	}
}
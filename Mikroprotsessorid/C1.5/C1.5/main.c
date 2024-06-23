/*
 * C1.5.c
 *
 * Created: 06.05.2021 12:58:27
 * Author : ralfs
 */ 

#include <avr/io.h>


int main(void)
{	DDRA = 0xff;
	PORTF = 1 << PINF5;
    //JOISTICK
    MCUCR = 1 << JTD;
	MCUCR = 1 << JTD;
	
	
	
	while(1)
	{
		if(!(PINF & 1 << PINF5))
			PORTA = 0x01;
	
		else{
			PORTA = 0x00;
		}
	}
}
	




/*
 * C1.1.c
 *
 * Created: 22.04.2021 11:59:01
 * Author : ralfs
 */ 
#ifndef F_CPU
#define F_CPU 16000000UL // 16 MHz clock speed
#endif

#include <avr/io.h>
#include <util/delay.h>


int main(void){
    DDRA = 0xff; //output vaja korgeks saada
    while (1) 
    {
		PORTA = 0x01; //led kaima
		//int UINT_8_t(int i){
		//for (uint_8_t i = 0; i < 100000; i++) {
		//asm("nop");}}
		
		_delay_ms(1000); //1 sekund
		PORTA = 0x00; //paneb ledi kinni
		//for (uint_8_t i = 0; i < 100000; i++) {
		//asm("nop");}
		_delay_ms(1000);
		 
    }
}

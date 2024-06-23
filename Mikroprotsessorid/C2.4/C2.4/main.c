/*
 * C2.4.c
 *
 * Created: 20.05.2021 15:52:25
 * Author : ralfs
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>

void kontrolli();
void saada(char num);

int main(void) {
	
	//UART init
	UBRR1 = 12;
	UCSR1B = (1 << TXEN1)|(1 << RXEN1)|(1 << RXCIE1);
	UCSR1C = (1 << UCSZ11)|(1 << UCSZ10);
	//LED init
	DDRA = 0xff;
	//Timer init
	TCNT1 = 0x00;
	OCR1A = 2000;
	TIMSK1 = (1 << OCIE1A); //COMPARE MATCH INTERRUPT ENABLE
	TCCR1B = (1 << CS12)|(1 << CS10)|(1 << WGM12); //Prescaler 1024 CTC MODE
	sei(); //Enable global interrupts by setting SREG
	
	while (1) {
		saada('R');
		saada('a');
		saada('l');
		saada('f');
	}
}

ISR(TIMER1_COMPA_vect) {
	PORTA ^= 0xff;
}

void kontrolli() {
	while(!(UCSR1A & (1 << UDRE1)));
	
}
ISR(USART1_RX_vect){
	while(!(UCSR1A & (1 << RXC1)));{
		
	}
	char receivedData;
	//int x;
	receivedData = UDR1;
	if(receivedData == '0'){
		TIMSK1 = 0;
		PORTA = 0;
	}
	else if ((receivedData == '1')){
		TIMSK1 = (1<<OCIE1A);
		TCNT1 = 0;
		OCR1A = 2000/1;
		}
	else if ((receivedData == '2')){
		TIMSK1 = (1<<OCIE1A);
		TCNT1 = 0;
		OCR1A = 2000/2;
	}
	else if ((receivedData == '3')){
		TIMSK1 = (1<<OCIE1A);
		TCNT1 = 0;
		OCR1A = 2000/3;
	}
	else if ((receivedData == '4')){
		TIMSK1 = (1<<OCIE1A);
		TCNT1 = 0;
		OCR1A = 2000/4;
	}
	else if ((receivedData == '5')){
		TIMSK1 = (1<<OCIE1A);
		TCNT1 = 0;
		OCR1A = 2000/5;
	}	
	else if ((receivedData == '6')){
		TIMSK1 = (1<<OCIE1A);
		TCNT1 = 0;
		OCR1A = 2000/6;
	}
	else if ((receivedData == '7')){
		TIMSK1 = (1<<OCIE1A);
		TCNT1 = 0;
		OCR1A = 2000/7;
	}
	else if ((receivedData == '8')){
		TIMSK1 = (1<<OCIE1A);
		TCNT1 = 0;
		OCR1A = 2000/8;
	}
	else if ((receivedData == '9')){
		TIMSK1 = (1<<OCIE1A);
		TCNT1 = 0;
		OCR1A = 2000/9;
	}
		else if((receivedData == 'X')){
			TCCR0B = 0;
			PORTA = 0xff;
		}
	}

void saada(char num) {
	kontrolli();
	UDR1 = num;
}

/*
 * C2.1.c
 *
 * Created: 19.05.2021 12:53:10
 * Author : ralfs
 */ 

#include <avr/io.h>


int main(void){
	void init_usart(void);
	void init_adc(void);
	void send(char num);
	int mis_nr();
	
	
	init_usart();
	init_adc();
	//send('a');
	
	while (ADCSRA & (1<<ADSC)) {
		
		//send('b');
		/* Wait for empty transmit buffer */
		
			mis_nr();
		
	}
}

void init_usart(void){
	//baud to 9600
	UBRR1= 12;
	//enable saaks saata
	UCSR1B=(1<<TXEN1);
	//Frame format 8bit
	UCSR1C=(1 << UCSZ11)|(1 << UCSZ10);
}

void init_adc(void){
	//enable adc, adc Start Conversion, adc Auto Trigger Enable, Prescaler /16
	ADCSRA=(1 << ADEN)|(1 << ADSC)|(1 << ADATE)|(1 << ADPS2);
	// ADC2
	ADMUX=(1 << MUX1)|(1 << REFS0);
	//while(!(ADCSRA&(1<<ADIF))); 
}

void send(char num){
	while((UCSR1A&(1<<UDRE1))==0);
	UDR1= num;
}

int mis_nr(){
	uint16_t adc= ADC;
	if(adc<101){
		
		send('0');
	}
	else if (adc<201){
		send('1');
	}
	else if (adc<301){
		send('2');
	}
	else if (adc<401){
		send('3');
	}
	else if (adc<501){
		send('4');
	}
	else if (adc<601){
		send('5');
	}
	else if (adc<701){
		send('6');
	}
	else if (adc<801){
		send('7');
	}
	else if (adc<=899){
		send('8');
	}
	else {
		send('9');
	}
}
	


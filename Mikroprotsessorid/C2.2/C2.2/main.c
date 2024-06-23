/*
 * C2.2.c
 *
 * Created: 20.05.2021 13:31:49
 * Author : ralfs
 */ 

#include <avr/io.h>


int main(void){
	void init_adc(void);
	void init_pwm(void);
	void init_led(void);
	
	
	init_adc();
	init_pwm();
	init_led();
	while (1) {
		while (ADCSRA & (1<<ADSC))  {
			OCR1A=ADC;
		}
	}
}

void init_adc(){
	//enable ADC, ADC Start Conversion, ADC Auto Trigger Enable, Prescaler /16
	ADCSRA=(1 << ADEN)|(1 << ADSC)|(1 << ADATE)|(1 << ADPS2);
	// ADC2 pot tööle
	ADMUX=(1 << MUX1)|(1 << REFS0);
}
void init_pwm(){
	// set to 10 bit fast pmw
	TCCR1A= (1 << WGM11)|(1 << WGM10)|(1 << COM0A1);
	// timer prescaler
	TCCR1B= (1 << WGM12)|(1<<CS10);
}
void init_led(){
	//led väljundiks
	DDRB= (1<<DDB5);
}


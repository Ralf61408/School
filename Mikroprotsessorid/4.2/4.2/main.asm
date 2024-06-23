;
; 4.2.asm
;
; Created: 28.04.2021 22:31:17
; Author : ralfs
;


; Replace with your application code
LDI R16, LOW(RAMEND)
OUT SPL, R16
LDI R16, HIGH(RAMEND)
OUT SPH, R16

; enable ADC, ADC Start Conversion, ADC Auto Trigger Enable, Prescaler votsin suvalise div factor 2
ldi r17, (1 << ADEN)|(1 << ADSC)|(1 << ADATE)//|(1 << ADPS0) 
sts ADCSRA, r17

;ADC2
ldi r17, (1 << MUX1)|(1 << REFS0) //potentsiomeetri tööle
sts ADMUX, r17

;set to 10 bit fast PWM
ldi r17, (1 << WGM11)|(1 << WGM10)|(1 << COM0A1)
sts TCCR1A, r17
; timer prescaler
ldi r17, (1 << WGM12)|(1<<CS10)
sts TCCR1B, r17

//LED väljundiks  OC1A
ldi r16, (1<<DDB5)
out DDRB, r16

main:
call get_adc
rjmp main

get_adc:
	push r17
	push r18
	lds r17, ADCL
	lds r18, ADCH
	sts OCR1AH, r18
	sts OCR1AL, r17
	pop r18
	pop r17
ret
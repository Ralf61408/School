LDI R16, LOW(RAMEND)
OUT SPL, R16
LDI R16, HIGH(RAMEND)
OUT SPH, R16


LDI R16, LOW(12)
LDI R17, HIGH(12)

; Set baud rate
sts UBRR1H, R17
sts UBRR1L, R16

; Enable transmitter
LDI R16, (1<<TXEN1)
sts UCSR1B, R16

; Set frame format: 8data
ldi r16, (1 << UCSZ11)|(1 << UCSZ10)

sts UCSR1C, R16

; enable ADC, ADC Start Conversion, ADC Auto Trigger Enable, Prescaler /16
ldi r17, (1 << ADEN)|(1 << ADSC)|(1 << ADATE)|(1 << ADPS2) 
sts ADCSRA, r17

;ADC2
ldi r17, (1 << MUX1)|(1 << REFS0) //potentsiomeetri tööle
sts ADMUX, r17	


main:
	call get_adc
	
rjmp main


get_adc:
	push r17
	push r18
	lds r17, ADCL
	lds r18, ADCH
	call compare
	pop r18
	pop r17
ret

compare:
	push r20
	push r21

	xbit:
		cpi r18,0
		brne kolm 
	null:
		rjmp yks
		send_null:
			ldi r24, '0'
			call saada
			pop r21
			pop r20
		ret

	yks:
		ldi r20, 101
		cp r17, r20

		BRSH kaks
		rjmp send_null

		send_yks:

			ldi r24, '1'
			call saada
			pop r21
			pop r20
		ret

	kaks:
		ldi r20, 201
		cp r17, r20

		BRSH kolm
		rjmp send_yks

		send_kaks:
			
			ldi r24, '2'
			call saada
			pop r21
			pop r20
		ret

	kolm:
		ldi r20, LOW(301)
		ldi r21, HIGH(301)
	
		cp r17, r20
		cpc r18, r21 

		BRSH neli
		rjmp send_kaks

		send_kolm:
			ldi r24, '3'
			call saada
			pop r21
			pop r20
		ret

	neli:
		ldi r20, LOW(401)
		ldi r21, HIGH(401)
	
		cp r17, r20
		cpc r18, r21 

		BRSH viis
		rjmp send_kolm

		send_neli:
			ldi r24, '4'
			call saada
			pop r21
			pop r20
		ret

	viis:
		ldi r20, LOW(501)
		ldi r21, HIGH(501)
	
		cp r17, r20
		cpc r18, r21 

		BRSH kuus
		rjmp send_neli

		send_viis:
			ldi r24, '5'
			call saada
			pop r21
			pop r20
		ret
	
	kuus:
		ldi r20, LOW(601)
		ldi r21, HIGH(601)
	
		cp r17, r20
		cpc r18, r21 

		BRSH seitse
		rjmp send_viis

		send_kuus:
			ldi r24, '6'
			call saada
			pop r21
			pop r20
		ret

	seitse:
		ldi r20, LOW(701)
		ldi r21, HIGH(701)
	
		cp r17, r20
		cpc r18, r21 

		BRSH kaheksa
		rjmp send_kuus

		send_seitse:
			ldi r24, '7'
			call saada
			pop r21
			pop r20
		ret

	kaheksa:
		ldi r20, LOW(801)
		ldi r21, HIGH(801)
	
		cp r17, r20
		cpc r18, r21 

		BRSH yheksa
		rjmp send_seitse

		send_kaheksa:
			ldi r24, '8'
			call saada
			pop r21
			pop r20
		ret

	yheksa:
		ldi r20, LOW(900)
		ldi r21, HIGH(900)
	
		cp r17, r20
		cpc r18, r21 

		BRSH send_yheksa
		rjmp send_kaheksa

		send_yheksa:
			ldi r24, '9'
			call saada
			pop r21
			pop r20
		ret

saada:
	push R17
	check:
		lds R17, UCSR1A

		sbrs R17, UDRE1
	rjmp check

	sts UDR1, R24
	pop R17
ret
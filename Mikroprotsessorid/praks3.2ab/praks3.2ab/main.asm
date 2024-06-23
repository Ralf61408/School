;
; praks3.2ab.asm
;
; Created: 26.05.2020 10:45:17
; Author : ralfs
;


; Replace with your application code
//LDI R21, 0x01
//LDI R22, 0x01 
//OUT DDRA, R21 
;STACK POINTER
LDI R16, low(RAMEND) ;(0x10FF)
OUT SPL, R16
LDI R16, high(RAMEND) ;viimase rami baidi aadress(0x10FF)
OUT SPH, R16

start:
	LDI R17,high(1000) ;korgema osa vaartus
	LDI R16,low(1000);madalama osa vaartus
	CALL delay
	//CALL LED
	JMP start

delay:
	PUSH R16 ;salvestab andmed sinna kuhu stackp viitab
	PUSH R17 ;salvestab andmed sinna kuhu stackp viitab

	ADD R16, R16 ;alumised baidid add kasuga liidame/ OCR reg. v22rtus mis on 2x suurem
	ADC R17, R17 ;sama aga jarmgised adc-ga

	STS OCR1AH,R17 ;Output Compare Register A High Byte
	STS OCR1AL,R16 ;Output Compare Register A Low Byte

	LDI  R16, 1 << OCF1A ;RESET FLAG (TIFR1) OCFnA can be cleared by writing a logic one to its bit location.
	OUT  TIFR1,R16

	LDI R16, 0 ;resetib
	STS TCNT1L, R16 ;vaartuse hoidmine tcnt registris
	STS TCNT1H, R16 ;Timer/Counter1

	LDI R16, (1 << CS10) | (1 << CS12) | (1 << WGM12)
	STS TCCR1B, R16 ;Määran /1024 ja WGM12 HIGH CTC mode jaoks, muidu ei reseti. maarame timeri kaitumist, mida ta tegema peab

	PAUSE:
		IN   R16,TIFR1      ;Timer sisse           
		ANDI R16, 1 << OCF1A ;(KONTROLLIB OCF1A) bit1 zero flag lipp pusti
		BREQ PAUSE

	POP R17     
	POP R16
	RET

//led:
	//EOR R21, R22 ;logical eor
	//OUT PORTA, R21
	//RET


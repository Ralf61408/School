;
; praks3.3.asm
;
; Created: 25.05.2022 11:56:47
; Author : ralfs
;


; Replace with your application code
Init:
	LDI R16, LOW(RAMEND)
	OUT SPL, R16
	LDI R16, HIGH(RAMEND)
	OUT SPH, R16

	LDI R16, LOW(12)
	LDI R17, HIGH(12)
	STS UBRR1H, R17
	STS UBRR1L, R16

	LDI R16, (1 << TXEN1)
	STS UCSR1B, R16

	LDI R16, (1 << UCSZ11)|(1 << UCSZ10)
	STS UCSR1C, R16

Main:
	ldi R24,'n'
	call USARTtransmit
	ldi R24,'i'
	call USARTtransmit
	ldi R24,'m'
	call USARTtransmit
	ldi R24,'i'
	call USARTtransmit
	rjmp Main

USARTtransmit:
	PUSH R17
	Kontroll:
		LDS R17, UCSR1A
		SBRS R17, UDRE1
		RJMP Kontroll
	STS	UDR1, R24
	POP R17
	RET

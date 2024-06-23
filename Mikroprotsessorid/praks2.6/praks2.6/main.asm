;
; praks2.6.asm
;
; Created: 28.04.2020 18:17:02
; Author : ralfs
;


; Replace with your application code

LDI r18, HIGH(RAMEND)
OUT SPH, r18
LDI r18, LOW(RAMEND)
OUT SPL, r18

LDI R19, 1
OUT 0x01, R19

Main_loop:
	LDI r16, 0x00
	LDI r17, 0x02

	CALL s
	CALL o
	CALL s
	CALL sonavahe

Delay_1ms:
	PUSH r19
	LDI r19, 0x00
	
	DelayLoop:
		NOP
		NOP
		NOP
		NOP
		INC r19
		CPI r19, 250
	BRNE DelayLoop
	POP r19
	RET

Awesome_Delay:
	PUSH r16
	PUSH r17
	AwesomeLoop:
		CALL Delay_1ms
		SUBI r16, 1
		SBCI r17, 0
		BRNE AwesomeLoop

	POP r17
	POP r16
	RET

RJMP Main_Loop

tahevahe:
	LDI R20, low(1000)
	LDI R21, high(1000)
	CALL Awesome_Delay

RET

s:
	CALL punkt
	CALL punkt
	CALL punkt
	CALL tahevahe

RET

o:
	CALL kriips
	CALL kriips
	CALL kriips
	CALL tahevahe

RET

sonavahe:
	LDI R20, low(2000)
	LDI R21, high(2000)
	CALL Awesome_Delay

RET

punkt:
	OUT 0x02, R19
	LDI R16, low(500)
	LDI R17, high(500)
	CALL Awesome_Delay
	COM R19
	OUT 0x02, R19
	LDI R16, low(500)
	LDI R17, high(500)
	CALL Awesome_Delay
	COM R19

RET

kriips:
	LDI R19, 1
	OUT 0x02, R19
	LDI R20, low(1500)
    LDI R21, high(1500)
    CALL Awesome_Delay
	COM R19
	OUT 0x02, R19
	LDI R20, low(500)
    LDI R21, high(500)
    CALL Awesome_Delay
    POP R19
	

RET
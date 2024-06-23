;
; praks22.5.asm
;
; Created: 28.04.2020 14:44:23
; Author : ralfs
;


; Replace with your application code
LDI r20, low(ramend)
OUT SPL, r20
LDI r20, high(ramend)
OUT SPH, r20

LDI R19, 1
OUT 0x01, R19

Main_loop:
	CALL s
	CALL o
	CALL s
	CALL sonavahe
	

RJMP Main_loop

tahevahe:
	CALL delay
	CALL delay
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
	CALL delay
	CALL delay
	CALL delay
	CALL delay
RET

delay:

	PUSH R16
	PUSH R17
	PUSH R18

	LDI R16, 0
	delay_loop_0:
		
		LDI R17, 0

		delay_loop_1:
			LDI R18, 0

			delay_loop_2:
				INC R18
				CPI R18, 50
			BRNE delay_loop_2

			INC R17
			CPI R17, 49
		BRNE delay_loop_1

		INC R16
		CPI R16, 100
	BRNE delay_loop_0

	POP R18
	POP R17
	POP R16

RET

punkt:	
	OUT 0x02, R19
	CALL delay
	COM R19
	OUT 0x02, R19
	CALL delay
	COM R19
RET

kriips:
	PUSH R19
	LDI R19, 1
	OUT 0x02, R19
	CALL delay
	CALL delay
	CALL delay
	COM R19
	OUT 0x02, R19
	CALL delay
	POP R19
RET

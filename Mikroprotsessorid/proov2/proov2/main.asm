;
; proov2.asm
;
; Created: 28.04.2020 16:56:29
; Author : ralfs
;


; Replace with your application code
LDI R20,low(ramend)
OUT SPL, r20
LDI r20,high(ramend)
OUT SPH,R20

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

		
		ldi r16, 0
		xxx1:
			ldi r17, 0
			xxx:
				LDI R18, 0x00
				delay_loop:
					NOP
					NOP
					NOP
					NOP
					NOP
					NOP
					INC R18
					CPI R18,236
				BRNE delay_loop
				INC R17
				CPI R17,141
			BRNE xxx
			INC R16
			CPI R16,3
		BRNE xxx1

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

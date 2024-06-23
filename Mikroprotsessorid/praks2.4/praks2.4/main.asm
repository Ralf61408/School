;
; praks2.4.asm
;
; Created: 23.04.2020 10:34:25
; Author : ralfs
;


; Replace with your application code
LDI R16, Low(RAMEND) //1
OUT SPL, r16 //2
LDI r16, HIGH(RAMEND) //3
OUT SPH, r16 //4
Tsykkel:
	CALL SimpleProcedure //5 SALVESTAS 4
	CALL SmarterProcedure //6..
	NOP
	NOP
RJMP Tsykkel 
SimpleProcedure:
NOP
RET // 9

SmarterProcedure:
	CALL SimpleProcedure // A
	CALL SimpleProcedure // C
	RET


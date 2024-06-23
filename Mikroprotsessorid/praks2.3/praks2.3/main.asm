;
; praks2.3.asm
;
; Created: 18.04.2020 14:03:38
; Author : ralfs
;


;Initsialiseerime Sp, et see viitaks RAMi lõpu 0x10FFga
LDI R16, Low(RAMEND)
OUT SPL, r16
LDI r16, HIGH(RAMEND)
OUT SPH, r16
Tsykkel:
	CALL SimpleProcedure
	CALL SimpleProcedure
	CALL SimpleProcedure
RJMP Tsykkel
SimpleProcedure:
	Nop
RET


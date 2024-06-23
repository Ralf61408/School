;
; praks3.1.asm
;
; Created: 05.05.2020 14:44:39
; Author : ralfs
;


LDI R20, (1 << CS00)
OUT TCCR0B, R20  
Delay:
	RJMP Delay






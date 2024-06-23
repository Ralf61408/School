;
; AssemblerApplication1.asm
;
; Created: 27.02.2020 14:59:16
; Author : ralfs
;


; Replace with your application code
LDI R16,0x00

Main_loop:
	INC R16

	LDI R17,0x00
	delay_loop:
		NOP
		NOP
		INC R17
		CPI R17,0x09
	BRNE delay_loop


RJMP Main_loop

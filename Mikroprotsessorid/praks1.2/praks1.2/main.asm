;
; praks1.2.asm
;
; Created: 18.02.2021 10:13:27
; Author : ralfs
;


; Replace with your application code

LDI R16,0x08
OUT 0x01,R16
OUT 0x02,R16

	
	
loop:
	NOP
	JMP loop

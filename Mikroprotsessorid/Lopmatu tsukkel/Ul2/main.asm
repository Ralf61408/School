;
; Ul2.asm
;
; Created: 27.02.2020 13:58:43
; Author : ralfs
;



    LDI R16,0x08
	OUT 0x01,R16
	OUT 0x02,R16
	
	
	loop:
		NOP
		JMP loop

;
; Lõpmatu tsükkel.asm
;
; Created: 27.02.2020 12:50:13
; Author : ralfs
;


LDI R16,0xFF	
OUT 0x04, R16 	
OUT 0x05, R16 
JMP 0x0003

	
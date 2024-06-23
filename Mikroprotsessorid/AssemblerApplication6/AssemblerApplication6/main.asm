;
; AssemblerApplication6.asm
;
; Created: 12.03.2020 15:05:35
; Author : ralfs
;


; Replace with your application code
;initsialiseerime SP, et see viitaks RAMi lõpu 0x10FFga
LDI r16, 0xff
OUT SPL, r16
LDI r16, 0x10
OUT SPH, r16 

tsykkel:
LDI r16, 10
PUSH r16
PUSH r16
POP r16
POP r16
pop r16

RJMP tsykkel 

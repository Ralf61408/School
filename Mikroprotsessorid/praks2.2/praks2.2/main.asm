;
; praks2.2.asm
;
; Created: 18.04.2020 10:41:09
; Author : ralfs
;


; Replace with your application code
LDI R17, 0xFF
OUT SPL, R17
LDI r17, 0x10
OUT SPH, r17

LDI r18, 0x20
start:
PUSH r17
PUSH r18
POP r17
POP r18
NOP
rjmp start
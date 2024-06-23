;
; AssemblerApplication4.asm
;
; Created: 12.03.2020 14:14:50
; Author : ralfs
;


; Replace with your application code
start:
    ldi r16, 100
	ldi r17, 200

	add r16, r17
	sub r16, r17
	mul r16, r17
    rjmp start

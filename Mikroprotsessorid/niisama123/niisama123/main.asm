;
; niisama123.asm
;
; Created: 07.04.2021 01:40:19
; Author : ralfs
;


ldi r16, 10
ldi r17, 20

call delay

add r16, 17

delay:
	push r16
	ldi r16, 0xff
	delay_loop:
		dec r16
	brne delay_loop
	pop r16
ret

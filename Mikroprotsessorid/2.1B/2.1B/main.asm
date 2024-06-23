;
; 2.1B.asm
;
; Created: 25.02.2021 10:07:13
; Author : ralfs
;


;Initsialiseerime Sp, et see viitaks RAMi lõpu 0x10FFga
LDI R16, 0xff
OUT SPL, r16
LDI r16, HIGH(RAMEND)
OUT SPH, r16
ldi r17,55
call Tsykkel
Tsykkel:
	push r16
	ldi r16, 0xff
	delay_loop:
		dec r16
		brne delay_loop
		pop r16
	ret


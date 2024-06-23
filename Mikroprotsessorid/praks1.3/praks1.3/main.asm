;
; praks1.3.asm
;
; Created: 18.02.2021 12:45:49
; Author : ralfs
;


; Replace with your application code
LDI R16, 0xFF
OUT 0x01, R16		; DDRA

Main_loop:		; andsime programmikohale nime “Main_loop”
	OUT 0x02, R16 		; PORTB
	INC R16

	LDI R17, 0x00		; viivis algas
	delay_loop:
		NOP		; no operation – aja raiskamine :)
		NOP
		INC R17
	CPI R17, 255
	BRNE delay_loop	; kui tulemus polnud null, siis hüppame, kui oli 0 – siis läheme edasi
				; viivis lõppes siin
RJMP Main_loop		


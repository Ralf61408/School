;
; AssemblerApplication2.asm
;
; Created: 05.03.2020 12:56:03
; Author : ralfs
;


; Replace with your application code
LDI R16,0x08
LDI R21,0x08
OUT 0x01,R16
	
Main_loop:
LDI R20,0x08
EOR R21,R20
OUT 0x02,R21
	INC R16
	ldi r19, 0
	xxx1:
		ldi r18, 0
		xxx:
			LDI R17, 0x00
			delay_loop:
				NOP
				NOP
				NOP
				NOP
				NOP
				NOP
				INC R17
				CPI R17,236
			BRNE delay_loop
			INC R18
			CPI R18,141
		BRNE xxx
		INC R19
		CPI R19,3
	BRNE xxx1
	
rjmp Main_loop


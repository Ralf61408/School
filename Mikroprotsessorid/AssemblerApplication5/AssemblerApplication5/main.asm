;
; AssemblerApplication5.asm
;
; Created: 12.03.2020 14:40:52
; Author : ralfs
;


; Replace with your application code
LDI R19, 128
OUT 0x04, R19

Main_loop:
	OUT 0x05, R19

	LDI R16, 0

	delay_loop_0:
		LDI R17, 0

		delay_loop_1:
			LDI R18, 0

			delay_loop_2:
				INC R18
				CPI R18, 57
			BRNE delay_loop_2

			INC R17
			CPI R17, 5
		BRNE delay_loop_1

		INC R16
		CPI R16, 4
	BRNE delay_loop_0

	COM R19
	
RJMP Main_loop


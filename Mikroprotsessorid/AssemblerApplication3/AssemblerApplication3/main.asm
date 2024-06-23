;
; AssemblerApplication3.asm
;
; Created: 05.03.2020 14:42:36
; Author : ralfs
;


; Replace with your application code
Delay_1sec:                 ; For CLK(CPU) = 1 MHz
    LDI     dly1,   8       ; One clock cycle;
Delay1:
    LDI     dly2,   125     ; One clock cycle
Delay2:
    LDI     dly3,   250     ; One clock cycle
Delay3:
    DEC     dly3            ; One clock cycle
    NOP                     ; One clock cycle
    BRNE    Delay3          ; Two clock cycles when jumping to Delay3, 1 clock when continuing to DEC

    DEC     dly2            ; One clock cycle
    BRNE    Delay2          ; Two clock cycles when jumping to Delay2, 1 clock when continuing to DEC

    DEC     dly1            ; One clock Cycle
    BRNE    Delay1          ; Two clock cycles when jumping to Delay1, 1 clock when continuing to RET
RET

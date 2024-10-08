; Supports interrupt-driven keyboard input
; CSC 225, Assignment 5
; Given code, Winter '24

        .ORIG x500

; Reads one character, executing a second program while waiting for input:
;  0. Save state of Program 1
;  1. Saves the keyboard entry in the IVT.
;  2. Sets the keyboard entry in the IVT to ISR180.
;  3. Enables keyboard interrupts.
;  4. Returns to the second program.
;  5. Load state of Program 2
TRAP26  LDR R0, R6, #0          ; Load PC from R6 (pointer)
        ST R0, P1PC             ; Store PC into P1PC
        LDR R0, R6, #1          ; Load PSR from R6 (pointer add 1 offset)
        ST R0, P1PSR            ; Store PSR
        
        ; save registers
        ST R1, P1R1
        ST R2, P1R2
        ST R3, P1R3
        ST R4, P1R4
        ST R5, P1R5
        ST R7, P1R7
        
        ; save the keyboard entry in the IVT
        LDI R0, KBIV   ; load the old keyboard entry 
        ST R0, SAVEIV   ; Save that value (entry) into SAVEIV
        
        ; enables interrupts
        LD R0, KBIMASK  ; load bit 14 as 1 into R0
        STI R0, KBSR     ; load bit 14 (1) into KBSR
        
        ; set the keyboard entry in the IVT to ISR180
        LEA R0, ISR180
        STI R0, KBIV
        
        ; set up Program 2
        ADD R3, R6, #0
        LD R2, P2PC
        STR R2, R3, #0      ; change thing at R6 to R2's PC
        
        LD R2, P2PSR
        STR R2, R3, #1   
        
        LD R0, P2R0
        LD R1, P2R1
        LD R2, P2R2
        LD R3, P2R3
        LD R4, P2R4
        LD R5, P2R5
        LD R7, P2R7
        
        RTI    
        
        

; Responds to a keyboard interrupt:
;  0. Save state of Program 2
;  1. Disables keyboard interrupts.
;  2. Restores the original keyboard entry in the IVT.
;  3. Places the typed character in R0.
;  4. Returns to the caller of TRAP26.
;  5. Load state of Program 1
ISR180  LDR R0, R6, #0          ; Load PC from R6 (pointer)
        ST R0, P2PC             ; Store PC into P2PC
        LDR R0, R6, #1          ; Load PSR from R6 (pointer add 1 offset)
        ST R0, P2PSR            ; Store PSR
        
        ; save registers
        ST R0, P2R0
        ST R1, P2R1
        ST R2, P2R2
        ST R3, P2R3
        ST R4, P2R4
        ST R5, P2R5
        ST R7, P2R7   
        
        ; disables keyboard interrupts
        AND R1, R1, #0      ; clear R0
        STI R1, KBSR     ; store x0000 into KBSR
        
        
        
        ; restores the orignial keyboard entry in the IVT
        LD R0, SAVEIV   ; typed character in R0
        STI R0, KBIV
        
        LDI R0, KBDR     ; store typed character in R0
        

        ; set up Program 1
        LD R2, P1PC
        STR R2, R6, #0      ; change thing at R6 to R2's PC
        
        LD R2, P1PSR
        STR R2, R6, #1   
        
        LD R1, P1R1
        LD R2, P1R2
        LD R3, P1R3
        LD R4, P1R4
        LD R5, P1R5
        LD R7, P1R7
        
        RTI

; Program 1's data:
P1R1    .FILL x0000     ; TODO: Use these memory locations to save and restore
P1R2    .FILL x0000     ;       the first program's state.
P1R3    .FILL x0000
P1R4    .FILL x0000
P1R5    .FILL x0000
P1R7    .FILL x0000
P1PC    .FILL x0000
P1PSR   .FILL x0000

; Program 2's data:
P2R0    .FILL x0000     ; TODO: Use these memory locations to save and restore
P2R1    .FILL x0000     ;       the second program's state.
P2R2    .FILL x0000
P2R3    .FILL x0000
P2R4    .FILL x0000
P2R5    .FILL x0000
P2R7    .FILL x0000
P2PC    .FILL x4000     ; Initially, Program 2's PC is 0x4000.
P2PSR   .FILL x8002     ; Initially, Program 2 is unprivileged.

; Shared data:
SAVEIV  .FILL x0000     ; TODO: Use this memory location to save and restore
                        ;       the keyboard's IVT entry.

; Shared constants:
KBIV    .FILL x0180     ; The keyboard's interrupt vector
KBSR    .FILL xFE00     ; The Keyboard Status Register
KBDR    .FILL xFE02     ; The Keyboard Data Register
KBIMASK .FILL x4000     ; The keyboard interrupt bit's mask


        .END

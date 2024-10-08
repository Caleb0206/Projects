; Recursively computes Fibonacci numbers.
; CSC 225, Assignment 6
; Given code, Winter '24

        .ORIG x3000

; int main(void)
; NOTE: Do not alter this function.
MAINFN  LD  R6, INITSP  ; Init. the stack pointer.
        ADD R5, R6, #-1 ; Init. the frame pointer.
        ADD R6, R6, #-1 ; Push space for "n".

        LEA R0, PROMPT  ; Print the prompt.
        PUTS
        GETC            ; Read an integer.
        OUT
        LD  R1, INTNEG
        ADD R0, R0, R1
        STR R0, R5, #0  ; Assign the integer to "n".
        GETC            ; Consume the newline.
        OUT

        LDR R0, R5, #0  ; Push "n".
        ADD R6, R6, #-1
        STR R0, R6, #0
        LD  R4, FIBFN
        JSRR R4         ; Call "fib".
        LDR R1, R6, #0  ; Pop the return value.
        ADD R6, R6, #1
        ADD R6, R6, #1  ; Pop "n".

        LEA R0, RES1    ; Print the result.
        PUTS
        LD  R2, INTPOS
        LDR R0, R5, #0
        ADD R0, R0, R2
        OUT
        LEA R0, RES2
        PUTS
        ADD R0, R1, R2
        OUT
        LD  R0, NEWLINE
        OUT

        ADD R6, R6, #1  ; Pop "n".
        HALT

INITSP  .FILL xFE00
PROMPT  .STRINGZ "Enter an integer: "
RES1    .STRINGZ "f("
RES2    .STRINGZ ") = "
INTPOS  .FILL x30
INTNEG  .FILL x-30
NEWLINE .FILL x0A
FIBFN   .FILL x4000

        .END

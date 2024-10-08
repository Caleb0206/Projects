; Recursively computes Fibonacci numbers.
; CSC 225, Assignment 6
; Given code, Winter '24

        .ORIG x4000

; int fib(int)
; TODO: Implement this function.
FIBFN   LDR R0, R6, #0
        ST R2, SAVE_R2      ; save past n into SAVE_R2
        ST R0, INT_N        ; store n into INT_N
        
        AND R3, R3, #0
        
       ; space for the return value
        ADD R6, R6, #-1     ; decrement R6 pointer
        ADD R6, R6, #-1     ; decrement R6 pointer
        STR R7, R6, #0      ; store return address
        
        ADD R6, R6, #-1     ; decrement R6 pointer
        STR R5, R6, #0      ; store dynamic link (old R5) in address of R6
        
        ADD R5, R6, #-1     ; R5 = one abov R6 pointer (a)
        
        ADD R6, R6, #-2      ; R6 -= 2, now points at b
        
        ; actual code
        ADD R0, R0, #0
        BRnz IF_ZERO        ; if n <= 0
        
        ; check if n == 1
        ADD R1, R0, #-1     ; R1 = R0 - 1
        BRz IF_ONE      
        
        ; else
        ; caller setup for A
        
        ; put n-1 into a variable
        
    A   ADD R1, R0, #-1     ; R1 = n - 1
        
        ADD R6, R6, #-1 ; R6 points to n of fib(a)
        STR R1, R6, #0  ; load n-1 into the new R6 ( the new n )
        JSR FIBFN
        
        ; caller teardown for A
        LDR R3, R6, #0  ; get return value
        STR R3, R5, #0  ; store in a
        
        
        ; Caller setup for B
               
    B   LDR R1, R5, #4  ; R1 = n
        ADD R1, R1, #-2 ; n - 2
        
        ADD R6, R6, #1  ; R6 currently points to return value of A, so now points to n of fib(b)
        STR R1, R6, #0  ; load n-1 into the new R6 ( the new n )
        JSR FIBFN
        
        ; caller teardown for B
        LDR R3, R6, #0  ; get return value
        STR R3, R5, #-1  ; store in b
        
        LDR R4, R5, #0  ; A
        ADD R3, R3, R4  ; A + B
        STR R3, R5, #3
        BRnzp TEAR_CALLEE
        
IF_ZERO AND R0, R0, #0      ; R0 = 0
        STR R0, R5, #3      ; store 0 into the Return value
        BRnzp TEAR_CALLEE
        
IF_ONE  AND R0, R0, #0      ; R0 = 0
        ADD R0, R0, #1      ; R0 = 1
        STR R0, R5, #3      ; store 1 into the Return value
        BRnzp TEAR_CALLEE
          
TEAR_CALLEE
        LDR R4, R5, #3      ; load the return value
        
        ADD R6, R5, #1      ; R5 = Dynamic LInk
        
        LDR R5, R6, #0      ; R5 = dynamic link value
        
        ADD R6, R6, #1      ; R6 pointer + 1 (now points to return address)
        LDR R7, R6, #0      ; R7 = the return address
        ADD R6, R6, #1      ; R6 points to the RET value
        
        STR R4, R6, #0      ; store the return value
        
        LD R2, SAVE_R2      ; restore R2 ( the old n)
        RET 
        

INT_N   .BLKW #1            ; 1 memory space for parameter n
SAVE_R2 .BLKW #1            ; save R2 space
        .END


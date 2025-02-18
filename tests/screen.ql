; Example for ScreenModule for Q-Emulator specifically
; In real CPU you can write screen drivers yourself for your own implementation


; initialize the screen
; [MODULE INDEX] - port 0
load 1      ; load 1 into ACC
portw 0     ; write 1 to port 0 (ScreenModule)

; [WIDTH | HEIGHT] - port 1
load 32     ; load 32
store $0    ; store to 0
lsl 8       ; left shift by 8
or $0       ; bitwise OR with 0 addr
portw 1     ; write to port 1

; [MODE] - port 2
load 16     ; load 16
portw 2     ; write to port 2

; interrupt call
int 0x80


halt


; Example for ScreenModule for Q-Emulator specifically
; In real CPU you can write screen drivers yourself for your own implementation


#define WIN_WIDTH 32
#define WIN_HEIGHT 32


; update subroutine
subr update_call
    ; pick ScreenModule
    load 1
    portw 0         ; module index

    ; pick starting index (at 32768 or 0x8000)
    load 0x8000
    portw 1         ; starting cache index

    ; syscall
    int 0x80


; render frame
subr render_call
    ; reset X and Y counters
    load 0
    store $x
    store $y

    @render_y_loop
    @render_x_loop

    ; do per pixel stuff here

    ; increment x
    load $x
    inc
    store $x

    comp WIN_WIDTH          ; compare with window width
    loadpr @render_x_loop   ; load pointer
    jumpc 0b00_1000         ; if x < width -> loop back

    ; increment y
    load $y
    inc
    store $y

    comp WIN_HEIGTH         ; compare with window height
    loadpr @render_y_loop   ; load pointer
    jumpc 0b00_1000         ; if y < height -> loop back

    return


; initialize the screen
; [MODULE INDEX] - port 0
load 1      ; load 1 into ACC
portw 0     ; write 1 to port 0 (ScreenModule)

; [WIDTH | HEIGHT] - port 1
load WIN_WIDTH  ; load window width
lsl 8           ; shift 8 bits
or WIN_HEIGHT   ; bitwise OR with window height
portw 1         ; write to port 1

; [MODE] - port 2
load 16     ; load 16
portw 2     ; write to port 2

; syscall
int 0x80


; main update loop
@main_loop

; update screen
call update_call

; loop back
jump @main_loop


@exit
halt

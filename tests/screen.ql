; Example for ScreenModule for Q-Emulator specifically
; In real CPU you can write screen drivers yourself for your own implementation


#define WIN_WIDTH 32
#define WIN_HEIGHT 32
#define ARR_START 0x8000


macro make_array_ptr uses ptr index
    load ptr    ; load array pointer
    add index   ; add index

macro write_array uses ptr index value
    make_array_ptr uses ptr index  ; make pointer (output in ACC)
    tapr        ; transfer ACC to pointer register (PR)
    load value  ; load value into ACC
    storep      ; store value at address defined by PR

macro read_array uses ptr index
    make_array_ptr uses ptr index  ; make pointer (output in ACC)
    loadp


; update subroutine
subr update_call
    ; pick ScreenModule
    load 1
    portw 0         ; module index

    ; pick starting index (at 32768 or 0x8000)
    load ARR_START
    portw 1         ; starting cache index

    ; syscall
    int 0x80


; render frame
subr render_call
    ; reset X and Y counters
    load 0
    store $x
    store $y

    @render_loop

    ; per pixel stuff here

    ; calculate pixel index in array
    load $y
    mul WIN_WIDTH
    add $x
    store $index

    write_array uses ARR_START $index $index


    ; increment x
    load $x
    inc
    store $x

    comp WIN_WIDTH          ; compare with window width
    loadpr @render_loop     ; load pointer
    jumpc 0b00_1000         ; if x < width -> loop back

    ; reset x
    load 0
    store $x

    ; increment y
    load $y
    inc
    store $y

    comp WIN_HEIGHT         ; compare with window height
    loadpr @render_loop     ; load pointer
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

; render frame
call render_call

; update screen
call update_call

; loop back
jump @main_loop


@exit
halt

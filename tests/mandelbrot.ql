; Attempt at mandelbrot set renderer

#define WIN_WIDTH   32
#define WIN_HEIGHT  32
#define WIN_MODE   16       ; TODO: fix buggy \t detection in lexer
#define ITERATIONS  16

#define ARRAY_POINTER 0x8000

#define ACC_BIT 8
#define ACCURACY 1 << ACC_BIT


macro plot uses pos_x pos_y value
    load pos_y          ; load position y
    mul WIN_WIDTH       ; select row
    add pos_x           ; add position x, select column
    add ARRAY_POINTER   ; offset by array pointer
    tapr                ; transfer pointer to PR
    load value          ; load value
    storep              ; store value at address PR


macro init_screen uses width height mode
    ; [MODULE INDEX] - port 0
    load 1      ; load 1 into ACC
    portw 0     ; write 1 to port 0 (ScreenModule)

    ; [WIDTH | HEIGHT] - port 1
    load width  ; load window width
    lsl 8       ; shift 8 bits
    or height   ; bitwise OR with window height
    portw 1     ; write to port 1

    ; [MODE] - port 2
    load mode   ; load 16
    portw 2     ; write to port 2

    ; syscall
    int 0x80


macro iterate_point uses pos_x pos_y
    load ACCURACY
    div pos_x
    store $u
    store $za

    load ACCURACY
    div pos_y
    store $v
    store $zb

    store $temp_a
    store $temp_b

    load 0
    store $iteration

    @loop

    ; square U
    load $za
    mul $za
    lsr ACC_BIT
    store $temp_a

    ; square V
    load $zb
    mul $zb
    lsr ACC_BIT
    store $temp_b

    add $temp_a

    ; if za*za + zb*zb < 4 -> continue, else -> exit loop
    comp 4
    loadpr @continue_loop
    jumpc 0b00_1000
    jump @exit_loop

    @continue_loop
    ; calculate za to temp_a
    load $temp_a
    sub $temp_b
    add $u
    store $temp_a

    ; calculate zb
    load $za
    mul $zb
    lsr ACC_BIT
    lsl 1
    add $v
    store $zb

    ; move temp_a to za
    load $temp_a
    store $za

    ; increment iteration
    load $iteration
    inc
    store $iteration

    comp ITERATIONS         ; compare with ITERATIONS
    loadpr @loop            ; load pointer
    jumpc 0b00_1000         ; if iteration < ITERATIONS -> loop back

    @exit_loop
    load $iteration


subr update_call
    ; pick ScreenModule
    load 1
    portw 0         ; module index

    ; pick starting index (at 32768 or 0x8000)
    load ARRAY_POINTER
    portw 1         ; starting cache index

    ; syscall
    int 0x80


subr render_call
    ; reset X and Y counters
    load 0
    store $x
    store $y

    @render_loop

    ; do mandelbrot stuff here
    iterate_point uses $x $y
    store $iter

    load $x
    sub 16
    store $ox

    load $y
    sub 16
    store $oy

    plot uses $ox $oy $iter

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


; initialize screen module
init_screen uses WIN_WIDTH WIN_HEIGHT WIN_MODE


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

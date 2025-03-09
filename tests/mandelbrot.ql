; Attempt at mandelbrot set renderer

#define WIN_WIDTH   32
#define WIN_HEIGHT  32
#define WIN_MODE    16
#define ITERATIONS  16

#define ARRAY_POINTER 0x8000


macro plot uses pos_x pos_y value
    load pos_y          ; load position y
    mul WIN_WIDTH       ; select row
    add pos_x           ; add position x, select column
    add ARRAY_POINTER   ; offset by array pointer
    tapr                ; transfer pointer to PR
    load value          ; load value
    storep              ; store value at address PR


subr update_call
    ; pick ScreenModule
    load 1
    portw 0         ; module index

    ; pick starting index (at 32768 or 0x8000)
    load ARR_START
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

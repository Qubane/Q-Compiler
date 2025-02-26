; Attempt at Game Of Life

#define GRID_SIZE 64
#define GRID_WIDTH GRID_SIZE // 16
#define ARR_PTR 0x8000
#define ARR_SIZE ( GRID_SIZE * GRID_SIZE ) // 16
#define RNG_SEED 0x1543


load RNG_SEED
store $rand


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


subr random
    load $rand
    mul 20077
    add 12345
    store $rand
    return

subr fill_board
    ; define counter
    load 0
    store $counter

    @loop_start

    write_array uses ARR_PTR $counter $rand     ; write random to array
    call random                                 ; update random number

    ; increment counter
    load $counter
    inc
    store $counter

    ; compare against array size
    comp ARR_SIZE
    loadpr @loop_start
    jumpc 0b00_1000

    ; return if counter exceeds array size
    return

subr process_board
    ; define counter
    load 0
    store $counter

    @loop_start
    ; convert count to X Y cell position
    load $counter
    mod GRID_WIDTH
    store $X

    load $counter
    div GRID_WIDTH
    store $Y

    ; increment counter
    load $counter
    inc
    store $counter

    ; compare against array size
    comp ARR_SIZE
    loadpr @loop_start
    jumpc 0b00_1000

    ; return if counter exceeds array size
    return


subr init_screen_module uses WIN_WIDTH WIN_HEIGHT
    ; [MODULE INDEX] - port 0
    load 1      ; load 1 into ACC
    portw 0     ; write 1 to port 0 (ScreenModule)

    ; [WIDTH | HEIGHT] - port 1
    load $WIN_WIDTH     ; load window width
    lsl 8               ; shift 8 bits
    or $WIN_HEIGHT      ; bitwise OR with window height
    portw 1             ; write to port 1

    ; [MODE] - port 2
    load 1      ; load 1 (BW mode)
    portw 2     ; write to port 2

    ; syscall
    int 0x80
    return

subr update_screen
    ; pick ScreenModule
    load 1
    portw 0         ; module index

    ; pick starting index (at 32768 or 0x8000)
    load ARR_PTR
    portw 1         ; starting cache index

    ; syscall
    int 0x80
    return


; initialize screen module
; [WIN_WIDTH, WIN_HEIGHT]
call init_screen_module uses GRID_SIZE GRID_SIZE

; fill the board
call fill_board

; main update loop
@main_loop
call update_screen
call process_board
jump @main_loop


halt

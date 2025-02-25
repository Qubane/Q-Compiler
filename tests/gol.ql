; Attempt at Game Of Life

#define GRID_SIZE 32
#define ARR_PTR 0x8000
#define ARR_SIZE ( GRID_SIZE * GRID_SIZE ) // 16
#define RNG_SEED 0x1234


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


halt

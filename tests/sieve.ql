; sieve of Eratosthenes


; constants
load 256
store $SIEVE_SIZE
store $offset

load 128
store $ARRAY_START


; subroutines
subr append_to_list
    load $idx           ; load index
    add $ARRAY_START    ; add array_start
    tapr                ; make pointer
    pop                 ; pop from stack
    storep              ; store value at index

    load $idx   ; load index
    inc         ; increment
    store $idx  ; store index

    return              ; else return


; fill the array with numbers
load 0      ; load 0
store $idx  ; store index

@make_array_loop
load $idx               ; load index
add 2                   ; add 2
push                    ; push to stack
call append_to_list     ; append value to stack
load $idx               ; load index
comp $SIEVE_SIZE        ; compare with size

loadpr @make_array_loop
jumpc 0b00_1000         ; if index < SIEVE_SIZE then loop back


; sieve numbers
load 2          ; load 2
store $idx      ; store idx
store $offset   ; store offset

@sieve_loop
load $ARRAY_START   ; load array start
add $offset         ; add offset
tapr                ; make pointer
load 0              ; load 0
storep              ; store 0 at pointer

load $offset        ; load offset
add $idx            ; add index
store $offset       ; store offset

comp $SIEVE_SIZE    ; compare offset and sieve_size
loadpr @sieve_loop
jumpc 0b00_1000     ; if offset < sieve_size then continue the loop

load $idx           ; load index
inc                 ; increment
store $idx          ; store index
lsl 1               ; double it
sub 2               ; shift by 2
store $offset       ; store offset

comp $SIEVE_SIZE    ; compare offset and sieve_size
loadpr @sieve_loop
jumpc 0b00_1000     ; if offset < sieve_size then continue the loop


; "compress" the array
load 0
store $idx
store $offset

@compress_loop
load $offset        ; load offset
add $ARRAY_START    ; add array_start
loadp               ; load value at offset
store $value        ; store value

loadpr @compress_loop_skipped
jumpc 0b00_0100 ; if value is zero then skip call

load $value         ; load value
push                ; push to stack
call append_to_list ; call append to list

@compress_loop_skipped
load $offset    ; load offset
inc             ; increment
store $offset   ; store offset

comp $SIEVE_SIZE    ; compare offset with sieve_size
loadpr @compress_loop
jumpc 0b00_1000     ; if offset < sieve_size then loop back


halt

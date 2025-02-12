; simple case
load 10     ; load 10 to accumulator
store $A    ; store accumulator to variable A
add $A      ; add variable A to accumulator (basically A+A = 10+10)

load 128            ; load 128
store $array_ptr    ; store as array_ptr
load 32             ; load 32
store $array_size   ; store as array_size


; different number bases
load 31421      ; base 10
load 0b1001     ; base 2
load 0xF00F     ; base 16


; simple macro
macro make_array_ptr uses ptr index
    load ptr    ; load array pointer
    add index   ; add index

; complex macro
macro write_array uses ptr index value
    make_array_ptr uses ptr index  ; make pointer (output in ACC)
    tapr        ; transfer ACC to pointer register (PR)
    load value  ; load value into ACC
    storep      ; store value at address defined by PR

; complex macro
macro read_array uses ptr index
    make_array_ptr uses ptr index  ; make pointer (output in ACC)
    loadp


; test address pointers (labels)
load 0
store $counter


@basic_loop_start   ; the '@' defines a label
; use macro to write count to the array
;                ptr        index    value
write_array uses $array_ptr $counter $counter

load $counter
inc
store $counter

comp $array_size            ; compare counter+1 with array_size
loadpr @basic_loop_start    ; load address for '@basic_loop_start' label into PR
jumpc 0b00_1000             ; if counter+1 < array_size then loop back (jump to address in PR)
                            ; check available flags in QT instruction set google spreadsheet
                            ; https://docs.google.com/spreadsheets/d/1Sl82E1pRsVYuFbP9roWOJOsSJ4JLtFiOXaD3Rq9oaJI

; halt the CPU
; NOTE: if not present, the CPU will continue executing instructions,
; even after it overflows the program counter, it will just re-execute the whole program
halt

; NOTE: compiler puts subroutine calls after the end of the program, so beware of that
; every subroutine that is intended to be called / jumped to, must have some kind of 'return'
; to avoid unintended behaviour

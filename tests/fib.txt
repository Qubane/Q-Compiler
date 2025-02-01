; good old fibonacci sequence test
; except now it's 16 bit

load 0
store A

load 1
store B

loadpr @halt

@fib-loop
load A
add B
jumpc 0b0000_0000_0000_0001
store A
sub B
store B
jump @fib-loop

@halt
halt

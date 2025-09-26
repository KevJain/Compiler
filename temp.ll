declare i32 @_print_int(i32)

@LAST = global i32 0
@n = global i32 0
define i32 @fib(i32 %.arg_n) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %B0
B0:
    %.0 = load i32, i32* %n
    %.1 = icmp slt i32 %.0, 2
    br i1 %.1, label %L0, label%L1
L0:
    ret i32 1
    br label %L2
L1:
    %.2 = load i32, i32* %n
    %.3 = sub i32 %.2, 1
    %.4 = call i32 (i32) @fib(i32 %.3)
    %.5 = load i32, i32* %n
    %.6 = sub i32 %.5, 2
    %.7 = call i32 (i32) @fib(i32 %.6)
    %.8 = add i32 %.4, %.7
    ret i32 %.8
    br label %L2
L2:
    ret i32 0
}

define i32 @main() {
entry:
    br label %L3
L3:
    store i32 30, i32* @LAST
    store i32 0, i32* @n
    br label %B1
B1:
    %.9 = load i32, i32* @n
    %.10 = load i32, i32* @LAST
    %.11 = icmp slt i32 %.9, %.10
    br i1 %.11, label %L4, label%L5
L4:
    %.12 = load i32, i32* @n
    %.13 = call i32 (i32) @fib(i32 %.12)
    call i32 (i32) @_print_int(i32 %.13)
    %.14 = load i32, i32* @n
    %.15 = add i32 %.14, 1
    store i32 %.15, i32* @n
    br label %B1
L5:
    ret i32 0
}

# LLVMgen.py
from instructionsmodel import *
_n = 0
def new_register():
    global _n
    ret = f'%.{_n}'
    _n += 1
    return ret

def llvm_make(program : Program) -> Program:
    global _n
    _n = 0
    new_statements = []
    for s in program.statements:
        match s:
            case FunctionDefinition(name, parameters, body):
                new_statements.append(FunctionDefinition(name, parameters, llvm_statements(body)))
            case GlobalVarDec():
                new_statements.append(s)
            case _:
                raise RuntimeError(f'Invalid statement type {s} found during llvm generation')
    return Program(new_statements)

def llvm_statements(statements : list[Statement]) -> list[Statement]:
    out = []
    for s in statements:
        out.append(create_llvm(s))
    return out


# lLvm is a virtual register machine simulator. our code is currently represented in a stack based
# format, so we must simulate the stack processes to create corresponding register code output
# operations can only be done using registers.
# values on the stack are either numbers or register names
"""
; Math operations

left + right          %result = add i32 %left, %right
left - right          %result = sub i32 %left, %right
left * right          %result = mul i32 %left, %right
left / right          %result = sdiv i32 %left, %right
left < right          %result = icmp slt i32 %left, %right
left <= right         %result = icmp sle i32 %left, %right
left > right          %result = icmp sgt i32 %left, %right
left >= right         %result = icmp sge i32 %left, %right
left == right         %result = icmp eq i32 %left, %right
left != right         %result = icmp ne i32 %left, %right

; Memory operations
%{name} = alloca i32                       ; local name;
{result} = load i32, i32* %{name}          ; result = local[name]
store i32 {value}, i32* %{name}            ; local[name] = value
{result} = load i32, i32* @{name}          ; result = global[name]
store i32 {value}, i32* @{name}            ; global[name] = value

; Control flow operations
br label %{name}                           ; GOTO(name)
br i1 {test}, label %{Lc}, label %{La}     ; CBRANCH(Lc, La)
{result} = call i32 (i32) @name(i32 {arg}) ; result = name(arg)
ret i32 {value}                            ; return value

; Printing
call i32 (i32) @_print_int(i32 {value})    ; print value
"""
def create_llvm(block : BLOCK) -> BLOCK:
    ops = [] # everything is converted to a string, all LLVM ops must be strings
    stack = [] # vm simulation, which we use to generate appropriate LLVM instructions
    for instr in block.instructions:
        match instr:
            case PUSH(value):
                stack.append(str(instr.value))
            case POP():
                stack.pop()
            case ARITHMETIC() | RELATION():
                right = stack.pop()
                left = stack.pop()
                result = new_register()
                stack.append(result)
                op_str = ""
                if isinstance(instr, ARITHMETIC):
                    match instr:
                        case ADD():
                            op_str = 'add'
                        case MINUS():
                            op_str = 'sub'
                        case MULT():
                            op_str = 'mul'
                        case DIVIDE():
                            op_str = 'sdiv'
                    ops.append(LLVM(f'{result} = {op_str} i32 {left}, {right}'))
                elif isinstance(instr, RELATION):
                    match instr:
                        case LT():
                            op_str = 'slt'
                        case LE():
                            op_str = 'sle'
                        case GT():
                            op_str = 'sgt'
                        case GE():
                            op_str = 'sge'
                        case EQ():
                            op_str = 'eq'
                        case NE():
                            op_str = 'ne'
                    ops.append(LLVM(f'{result} = icmp {op_str} i32 {left}, {right}'))
            case LOAD_GLOBAL(name):
                register = new_register()
                ops.append(LLVM(f'{register} = load i32, i32* @{name}'))
                stack.append(register)
            case LOAD_LOCAL(name):
                register = new_register()
                ops.append(LLVM(f'{register} = load i32, i32* %{name}'))
                stack.append(register)
            case STORE_GLOBAL(name):
                value = stack.pop()
                ops.append(LLVM(f'store i32 {value}, i32* @{name}'))
            case STORE_LOCAL(name):
                value = stack.pop()
                ops.append(LLVM(f'store i32 {value}, i32* %{name}'))
            case PRINT():
                value = stack.pop()
                ops.append(LLVM(f'call i32 (i32) @_print_int(i32 {value})'))
            case LOCAL(name):
                ops.append(LLVM(f'%{name} = alloca i32'))
            case RETURN():
                value = stack.pop()
                ops.append(LLVM(f'ret i32 {value}'))
            case GOTO(destination):
                ops.append(LLVM(f'br label %{destination.label}'))
            case CBRANCH(true_block, false_block):
                test = stack.pop()
                ops.append(LLVM(f'br i1 {test}, label %{true_block.label}, label%{false_block.label}'))
            case CALL(name, return_type, arg_wtypes):
                register = new_register()
                arg_types = []
                for t in arg_wtypes:
                    if t == 'int':
                        arg_types.append('i32')
                    elif t == 'float':
                        arg_types.append('f32')
                    else:
                        raise RuntimeError(f'Unknown type in {arg_wtypes}')
                # TODO: CALL has been changed
                # Update the LLVM generation with thew new attributes of CALL
                llvm_return = "" # TODO: update
                ins = f'{register} = call i32 ({",".join(arg_types)}) @{name}('
                args = []
                for _ in range(num_args):
                    args.append(f'i32 {stack.pop()}')
                args.reverse()
                ins += ", ".join(args) + ")"
                ops.append(LLVM(ins))
                stack.append(register)
            case _:
                raise RuntimeError(f'Unknown instruction type {instr} found during LLVM generation')
    return BLOCK(block.label, ops)

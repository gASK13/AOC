import re


def do_op(_ops, _stack, _buffer):
    op = _ops.pop()
    if op is None:
        _stack.pop()
        _stack.append(int(_buffer))
    elif op == '*':
        _stack.append(_stack.pop() * int(_buffer))
    elif op == '+':
        _stack.append(_stack.pop() + int(_buffer))


def eval(_expr):
    stack = [None]
    ops = [None]
    buffer = ''
    for ch in _expr:
        if re.match('[0-9]', ch):
            buffer += ch
        elif ch == '(':
            stack.append(None)
            ops.append(None)
        elif ch == ')':
            do_op(ops, stack, buffer)
            buffer = str(stack.pop())
        elif re.match('[*+]', ch):
            ops.append(ch)
        else:
            # end of number
            if len(buffer) > 0:
                do_op(ops, stack, buffer)
                buffer = ''
    if len(buffer) > 0:
        do_op(ops, stack, buffer)
    return stack.pop()


def eval_new(_expr):
    if len(re.findall('\+', _expr)) == 0:
        return eval(_expr)
    elif len(re.findall('\*', _expr)) == 0:
        return eval(_expr)

    # redo parentheses
    buffer = ''
    inner_buffer = ''
    parent = ['', 0]
    for chr in _expr:
        if chr == ')':
            parent[1] -= 1
            if parent[1] == 0:
                ret = eval_new(parent[0])
                inner_buffer += str(ret)
                parent[0] = ''
            else:
                parent[0] += chr
        elif chr == '(':
            if parent[1] > 0:
                parent[0] += chr
            parent[1] += 1
        elif parent[1] > 0:
            parent[0] += chr
        elif chr == '+':
            inner_buffer += chr
        elif chr == '*':
            buffer += ' {} * '.format(str(eval(inner_buffer)))
            inner_buffer = ''
        else:
            inner_buffer += chr

    buffer += ' {}'.format(str(eval(inner_buffer)))
    return eval(buffer)


assert(eval('1 + 2 * 3 + 4 * 5 + 6') == 71)
assert(eval('1 + (2 * 3) + (4 * (5 + 6))') == 51)
assert(eval('2 * 3 + (4 * 5)') == 26)
assert(eval('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437)
assert(eval('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240)
assert(eval('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632)

sum = 0
for line in open('18.txt', 'r').readlines():
    sum += eval(line.strip())

print('Old way: {}'.format(sum))

assert(eval_new('1 + 2 * 3 + 4 * 5 + 6') == 231)
assert(eval_new('1 + (2 * 3) + (4 * (5 + 6))') == 51)
assert(eval_new('2 * 3 + (4 * 5)') == 46)
assert(eval_new('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445)
assert(eval_new('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060)
assert(eval_new('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340)

sum = 0
for line in open('18.txt', 'r').readlines():
    sum += eval_new(line.strip())

print('New way: {}'.format(sum))
import common

test_result = {'d': 72, 'e': 507, 'f': 492, 'g': 114, 'h': 65412, 'i': 65079, 'x': 123, 'y': 456}


# 123 -> x means that the signal 123 is provided to wire x.
# x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.
# p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then provided to wire q.
# NOT e -> f means that the bitwise complement of the value from wire e is provided to wire f.

class BitwiseLogic:
    def __init__(self, overrides=None):
        if overrides is not None:
            self.buffers = overrides
        else:
            self.buffers = {}

    def get_value(self, part):
        try:
            return int(part)
        except ValueError:
            if part in self.buffers:
                return self.buffers[part]
            else:
                return None

    def direct_command(self, parts):
        value = self.get_value(parts[0])
        if value is not None:
            self.buffers[parts[1]] = value
            return True
        return False

    def evaluate_command(self, command):
        # try to evaluate command
        parts = command.split(' -> ')
        if parts[1] in self.buffers:
            # overrides
            return True
        if ' ' not in parts[0]:
            return self.direct_command(parts)
        else:
            # composite command
            if parts[0].startswith('NOT'):
                # this is NOT in 65535 context (2 bytes)
                value = self.get_value(parts[0][4:])
                if value is not None:
                    self.buffers[parts[1]] = value ^ 65535
                    return True
            if 'AND' in parts[0]:
                operands = parts[0].split(' AND ')
                if all([self.get_value(x) is not None for x in operands]):
                    self.buffers[parts[1]] = self.get_value(operands[0]) & self.get_value(operands[1])
                    return True
            if 'OR' in parts[0]:
                operands = parts[0].split(' OR ')
                if all([self.get_value(x) is not None for x in operands]):
                    self.buffers[parts[1]] = self.get_value(operands[0]) | self.get_value(operands[1])
                    return True
            if 'LSHIFT' in parts[0]:
                operands = parts[0].split(' LSHIFT ')
                if all([self.get_value(x) is not None for x in operands]):
                    self.buffers[parts[1]] = self.get_value(operands[0]) << int(operands[1])
                    return True
            if 'RSHIFT' in parts[0]:
                operands = parts[0].split(' RSHIFT ')
                if all([self.get_value(x) is not None for x in operands]):
                    self.buffers[parts[1]] = self.get_value(operands[0]) >> int(operands[1])
                    return True
        return False

    def evaluate_commands(self, cmd_list):
        hit = True
        new_cmd = cmd_list
        while hit:
            hit = False
            cmd_list = new_cmd
            new_cmd = []
            for cmd in cmd_list:
                if self.evaluate_command(cmd):
                    hit = True
                else:
                    new_cmd.append(cmd)

        if len(new_cmd) > 0:
            print(self.buffers)
            raise RuntimeError(f'Could not evaluate commands {new_cmd}')
        return self.buffers


# test
bl = BitwiseLogic()
assert not bl.evaluate_command('u -> v')
assert not bl.evaluate_command('x AND y -> d')
assert bl.evaluate_command('123 -> x')
assert bl.get_value('x') == 123
assert bl.evaluate_command('x -> y')
assert bl.get_value('y') == 123
assert bl.evaluate_command('NOT y -> z')
assert bl.get_value('z') == 65412
assert bl.evaluate_command('x AND y -> d')
assert bl.get_value('d') == 123
assert bl.evaluate_command('x AND 257 -> e')
assert bl.get_value('e') == 1

bl = BitwiseLogic(overrides={'x': 123})
assert bl.evaluate_command('x AND 257 -> e')
assert bl.get_value('e') == 1
assert bl.evaluate_command('456 -> x')
assert bl.get_value('x') == 123

assert BitwiseLogic().evaluate_commands(common.Loader.load_lines('test')) == test_result

# real part
wire_a = BitwiseLogic().evaluate_commands(common.Loader.load_lines())["a"]
print(f'Value of wire a is {wire_a}')
print(
    f'Value of wire a with override is {BitwiseLogic(overrides={"b": wire_a}).evaluate_commands(common.Loader.load_lines())["a"]}')

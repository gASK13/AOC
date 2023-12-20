import common
from colorama import Fore, Back, Style
import sys

class Module:
    def __init__(self, module_id):
        self.id = module_id
        self.outputs = []

    def add_input(self, input_id):
        pass

    def add_output(self, output):
        self.outputs.append(output)

    def handle_input(self, signal):
        return []


class Broadcast(Module):
    def __init__(self, module_id):
        super().__init__(module_id)

    def handle_input(self, signal):
        return [(self.id, output, signal[2]) for output in self.outputs]


class FlipFlop(Module):
    def __init__(self, module_id):
        super().__init__(module_id)
        self.state = False

    def handle_input(self, signal):
        if not signal[2]:
            self.state = not self.state
            return [(self.id, output, self.state) for output in self.outputs]
        return []


class Conjunction(Module):
    def __init__(self, module_id):
        super().__init__(module_id)
        self.inputs = {}

    def add_input(self, input_id):
        self.inputs[input_id] = False

    def handle_input(self, signal):
        self.inputs[signal[0]] = signal[2]
        return [(self.id, output, not all(self.inputs.values())) for output in self.outputs]


class Network:
    def __init__(self, lines):
        self.modules = {}
        for line in lines:
            id = line.split(' -> ')[0]
            if '%' in id:
                self.modules[id[1:]] = FlipFlop(id[1:])
            elif '&' in id:
                self.modules[id[1:]] = Conjunction(id[1:])
            else:
                self.modules[id] = Broadcast(id)
        for line in lines:
            id, connections = line.split(' -> ')
            id = id.strip('%').strip('&')
            for connection in connections.split(', '):
                self.modules[id].add_output(connection)
                if connection not in self.modules:
                    self.modules[connection] = Module(connection)
                self.modules[connection].add_input(id)

    def push_button(self, pushes=None, stop_component=False):
        counter = {False: 0, True: 0}
        if pushes is None:
            pushes = sys.maxsize
        if stop_component:
            # this is "hard coded" -> I know that the component is & linked to NS component
            # so I can check what I need to align NS and compute cycles for alignment
            # and then find LCM of those cycles
            cycles = {}
            for _ in self.modules['ns'].inputs:
                cycles[_] = None
        for i in range(pushes):
            signals = [(None, 'broadcaster', False)]
            while len(signals) > 0:
                signal = signals.pop(0)
                if stop_component:
                    if signal[2] and signal[0] in cycles and signal[1] == 'ns':
                        print(f'Found "{signal[0]}" > "ns" at {i + 1}')
                        cycles[signal[0]] = i + 1
                        if all(cycles.values()):
                            lcm = 1
                            for value in cycles.values():
                                lcm = common.utils.lcm(lcm, value)
                            return lcm
                counter[signal[2]] += 1
                signals += self.modules[signal[1]].handle_input(signal)

        return counter[False] * counter[True]


assert Network(common.Loader.load_lines('test_0')).push_button(1000) == 8000*4000
assert Network(common.Loader.load_lines('test')).push_button(1000) == 4250*2750

print(f'Part 1: {Back.GREEN}{Fore.BLACK}{Network(common.Loader.load_lines()).push_button(1000)}')

print(f'Part 2: {Back.GREEN}{Fore.BLACK}{Network(common.Loader.load_lines()).push_button(stop_component=True)}')

# test > 0, 1, 1, 1 (4 cycle)
# test_0 > 8000 x 4000
# test > 4250 x 2750


# RX will receive LOW when all NS are HIGH
# So this means one of each of these needs to send LOW
# &cq
# &dc
# &rv
# &vp
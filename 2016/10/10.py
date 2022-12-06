import common


class ChipHandler:
    def __init__(self):
        pass

    def store(self, chip):
        raise NotImplementedError('OOPS')


class Output(ChipHandler):
    def __init__(self):
        super().__init__()
        self._bin = None

    def store(self, chip):
        if self._bin is not None:
            raise Exception('ALREADY HAVE ONE')
        self._bin = chip

    def value(self):
        return self._bin if self._bin is not None else 0

    def __repr__(self):
        return str(self._bin)

    def __str__(self):
        return str(self._bin)


class Bot(ChipHandler):
    def __init__(self, targets, id):
        super().__init__()
        self._chips = []
        self._lower = None
        self._higher = None
        self._targets = targets
        self._id = id

    def store(self, value):
        self._chips.append(value)
        if len(self._chips) == 2:
            self._chips.sort()
            if self._chips == self._targets:
                print(f'BOT {self._id} COMPARED {self._chips} !')
            self._lower.store(self._chips.pop(0))
            self._higher.store(self._chips.pop(0))

    def set_process(self, lower, higher):
        self._lower = lower
        self._higher = higher


def run_program(lines, targets):
    # global - output and bots (yeah, not ideal)
    output = {}
    bots = {}
    for line in lines:
        items = line.split(' ')
        if items[0] == 'bot':
            bot_id = int(items[1])
            if bot_id not in bots:
                bots[bot_id] = Bot(targets, bot_id)
            low = int(items[6])
            if items[5] == 'output':
                if low not in output:
                    output[low] = Output()
                low = output[low]
            else:
                if low not in bots:
                    bots[low] = Bot(targets, low)
                low = bots[low]
            high = int(items[11])
            if items[10] == 'output':
                if high not in output:
                    output[high] = Output()
                high = output[high]
            else:
                if high not in bots:
                    bots[high] = Bot(targets, high)
                high = bots[high]
            bots[bot_id].set_process(low, high)
    for line in lines:
        items = line.split(' ')
        if items[0] == 'value':
            bot_id = int(items[5])
            if bot_id not in bots:
                bots[bot_id] = Bot(targets, bot_id)
            bots[bot_id].store(int(items[1]))
    return output[0].value() * output[1].value() * output[2].value()

assert run_program(common.Loader.load_lines(filename='test'), [2, 5]) == 30
print(f'Result of part 2: {run_program(common.Loader.load_lines(), [17, 61])}')
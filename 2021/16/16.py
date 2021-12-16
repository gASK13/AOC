import common


class Packet:
    @staticmethod
    def from_string(data):
        return Packet(int(data, 16), len(data) * 4)

    def __init__(self, number, bits):
        self.num = number
        self.bits = bits
        self.version = self.__extract_bits(3)
        self.type = self.__extract_bits(3)
        self.sub_packets = []

        if self.type == 4:
            self.value = self.__get_value()
        else:
            if self.__extract_bits(1) == 1:
                # the next 11 bits are number of subpackets (?)
                subpacket_count = self.__extract_bits(11)
                for i in range(subpacket_count):
                    self.sub_packets.append(Packet(self.num, self.bits))
                    self.bits = self.sub_packets[-1].bits
                    self.num = self.sub_packets[-1].num
            else:
                # get next 15 bits as length and then parse that many bits into packets
                bitlen = self.__extract_bits(15)
                subbits = self.__extract_bits(bitlen)
                while bitlen > 0:
                    self.sub_packets.append(Packet(subbits, bitlen))
                    bitlen = self.sub_packets[-1].bits
                    subbits = self.sub_packets[-1].num

    def get_version(self):
        return self.version + sum([sp.get_version() for sp in self.sub_packets])

    def calculate(self):
        match self.type:
            case 0:
                return sum([sp.calculate() for sp in self.sub_packets])
            case 1:
                rv = 1
                for sp in self.sub_packets:
                    rv *= sp.calculate()
                return rv
            case 2:
                return min([sp.calculate() for sp in self.sub_packets])
            case 3:
                return max([sp.calculate() for sp in self.sub_packets])
            case 4:
                return self.value
            case 5:
                return 1 if self.sub_packets[0].calculate()  > self.sub_packets[1].calculate() else 0
            case 6:
                return 1 if self.sub_packets[0].calculate() < self.sub_packets[1].calculate() else 0
            case 7:
                return 1 if self.sub_packets[0].calculate() == self.sub_packets[1].calculate() else 0

    def __extract_bits(self, count):
        self.bits -= count
        part = self.num >> self.bits
        self.num ^= part << self.bits
        return part

    def __get_value(self):
        res = 0
        while self.bits >= 5:
            part = self.__extract_bits(5)
            res = (res << 4) | (part % 16)
            if part < 16:
                return res


# test of parsing
print(f'Test {Packet.from_string("D2FE28").value}, expected 2021.')
print(f'Test {len(Packet.from_string("38006F45291200").sub_packets)}, expected 2')
print(f'Test {len(Packet.from_string("EE00D40C823060").sub_packets)}, expected 3')

# test data
test_data = {
    '8A004A801A8002F478': 16,
    '620080001611562C8802118E34': 12,
    'C0015000016115A2E0802F182340': 23,
    'A0016C880162017C3686B18A3D4780': 31
}
for td in test_data:
    print(f'Test {Packet.from_string(td).get_version()}, expected {test_data[td]}.')

print(f'Real {Packet.from_string(common.Loader.load_lines()[0]).get_version()}.')

test_data_two = {
    'C200B40A82': 3,
    '04005AC33890': 54,
    '880086C3E88112': 7,
    'CE00C43D881120': 9,
    'D8005AC2A8F0': 1,
    'F600BC2D8F': 0,
    '9C005AC2F8F0': 0,
    '9C0141080250320F1802104A08': 1
}
for td in test_data_two:
    print(f'Test {Packet.from_string(td).calculate()}, expected {test_data_two[td]}.')

print(f'Real {Packet.from_string(common.Loader.load_lines()[0]).calculate()}.')

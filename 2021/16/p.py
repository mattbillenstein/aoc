#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

SUM = 0
PRODUCT = 1
MIN = 2
MAX = 3
LITERAL = 4
GT = 5
LT = 6
EQ = 7

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

class Packet:
    def __init__(self, version, type):
        self.version = version
        self.type = type
        if type == LITERAL:
            self.value = None
        else:
            # operator - subpackets
            self.packets = []

    def calc(self):
        '''
        Packets with type ID 0 are sum packets - their value is the sum of the
        values of their sub-packets. If they only have a single sub-packet,
        their value is the value of the sub-packet.

        Packets with type ID 1 are product packets - their value is the result of
        multiplying together the values of their sub-packets. If they only have a
        single sub-packet, their value is the value of the sub-packet.

        Packets with type ID 2 are minimum packets - their value is the minimum of
        the values of their sub-packets.

        Packets with type ID 3 are maximum packets - their value is the maximum of
        the values of their sub-packets.

        Packets with type ID 5 are greater than packets - their value is 1 if the
        value of the first sub-packet is greater than the value of the second
        sub-packet; otherwise, their value is 0. These packets always have exactly
        two sub-packets.

        Packets with type ID 6 are less than packets - their value is 1 if the
        value of the first sub-packet is less than the value of the second
        sub-packet; otherwise, their value is 0. These packets always have exactly
        two sub-packets.

        Packets with type ID 7 are equal to packets - their value is 1 if the value
        of the first sub-packet is equal to the value of the second sub-packet;
        otherwise, their value is 0. These packets always have exactly two
        sub-packets.
        '''
        if self.type == LITERAL:
            return self.value

        values = [_.calc() for _ in self.packets]
        if self.type == SUM:
            return sum(values)
        elif self.type == PRODUCT:
            p = 1
            for v in values:
                p *= v
            return p
        elif self.type == MIN:
            return min(values)
        elif self.type == MAX:
            return max(values)
        elif self.type == GT:
            return int(values[0] > values[1])
        elif self.type == LT:
            return int(values[0] < values[1])
        elif self.type == EQ:
            return int(values[0] == values[1])
        else:
            assert 0

    def __repr__(self):
        v = self.value if self.type == LITERAL else self.packets
        return f'Packet({self.version}, {self.type}, {v})'

def hex_to_bin(s):
    out = ''
    for i in range(0, len(s), 16):
        x = s[i:i+16]
        y = bin(int(x, 16))[2:].zfill(len(x)*4)
        out += y
    return out

def decode_literal(bits, idx):
    v = 0
    while 1:
        s = bits[idx:idx+5]
        idx += 5
        v <<= 4
        v |= int(s[1:], 2)
        if s[0] == '0':
            break

    return v, idx

def decode_version(bits, idx):
    version = int(bits[idx:idx+3], 2)
    return version, idx+3

def decode_type(bits, idx):
    type = int(bits[idx:idx+3], 2)
    return type, idx+3

def decode_operator(bits, idx):
#    print('decode_operator', idx)
    end_idx = 1000000
    num_pkts = 1000000

    if bits[idx] == '0':
        # 15 bits - total bits of sub-packets
        idx += 1
        num_bits = int(bits[idx:idx+15], 2)
        idx += 15
        end_idx = idx + num_bits
    else:
        # 11 bits - number of sub-packets in this packet
        idx += 1
        num_pkts = int(bits[idx:idx+11], 2)
        idx += 11

    packets = []
    while len(packets) < num_pkts and idx < end_idx:
        pkt, idx = decode_packet(bits, idx)
        assert pkt
        packets.append(pkt)

    return packets, idx

def decode_packet(bits, idx):
#    print('decode_packet', idx)
    version, idx = decode_version(bits, idx)
    type, idx = decode_type(bits, idx)
    pkt = Packet(version, type)

    if type == LITERAL:
        pkt.value, idx = decode_literal(bits, idx)
    else:
        # operator
        pkt.packets, idx = decode_operator(bits, idx)

    return pkt, idx

def version_sum(pkt):
    tot = pkt.version
    if pkt.type != LITERAL:
        tot += sum(version_sum(_) for _ in pkt.packets)
    return tot

def run(data):
    for line in data:
        bits = hex_to_bin(line)
        print(line, bits)

        idx = 0
        while idx < len(bits):
            try:
                pkt, idx = decode_packet(bits, idx)
                print(pkt)
                print('Version sum:', version_sum(pkt))
                print('Calc:', pkt.calc())
            except (ValueError, IndexError):
                break

def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()

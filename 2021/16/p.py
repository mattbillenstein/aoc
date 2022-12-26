#!/usr/bin/env pypy3

import math
import sys

SUM = 0
PRODUCT = 1
MIN = 2
MAX = 3
LITERAL = 4
GT = 5
LT = 6
EQ = 7

MIN_PACKET = 11 # version (3), type (3), loop (1), 4-bit literal?

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

    def versions_sum(self):
        if self.type == LITERAL:
            return self.version
        return self.version + sum(_.versions_sum() for _ in self.packets)

    def calc(self):
        if self.type == LITERAL:
            return self.value

        values = [_.calc() for _ in self.packets]
        if self.type == SUM:
            return sum(values)
        elif self.type == PRODUCT:
            return math.prod(values)
        elif self.type == MIN:
            return min(values)
        elif self.type == MAX:
            return max(values)
        elif self.type == GT:
            return 1 if values[0] > values[1] else 0
        elif self.type == LT:
            return 1 if values[0] < values[1] else 0
        elif self.type == EQ:
            return 1 if values[0] == values[1] else 0
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

def consume(bits, idx, cnt):
    v = int(bits[idx:idx+cnt], 2)
    return v, idx+cnt

def decode_literal(bits, idx):
    v = 0
    while 1:
        loop, idx = consume(bits, idx, 1)
        x, idx = consume(bits, idx, 4)
        v <<= 4
        v |= x
        if not loop:
            break

    return v, idx

def decode_operator(bits, idx):
    end_idx = sys.maxsize
    num_pkts = sys.maxsize

    length_type, idx = consume(bits, idx, 1)
    if length_type == 0:
        # 15 bits - total bits of sub-packets
        num_bits, idx = consume(bits, idx, 15)
        end_idx = idx + num_bits
    else:
        # 11 bits - number of sub-packets in this packet
        num_pkts, idx = consume(bits, idx, 11)

    packets = []
    while len(packets) < num_pkts and idx < end_idx:
        pkt, idx = decode_packet(bits, idx)
        packets.append(pkt)

    return packets, idx

def decode_version(bits, idx):
    return consume(bits, idx, 3)

def decode_type(bits, idx):
    return consume(bits, idx, 3)

def decode_packet(bits, idx):
    version, idx = decode_version(bits, idx)
    type, idx = decode_type(bits, idx)
    pkt = Packet(version, type)

    if type == LITERAL:
        pkt.value, idx = decode_literal(bits, idx)
    else:
        # operator
        pkt.packets, idx = decode_operator(bits, idx)

    return pkt, idx

def run(data):
    for line in data:
        bits = hex_to_bin(line)
        print(line, bits)

        idx = 0
        while len(bits) - idx >= MIN_PACKET:
            pkt, idx = decode_packet(bits, idx)
            print(pkt, idx)
            print('Sum versions:', pkt.versions_sum())
            print('Calc:', pkt.calc())

def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import copy
import math
import sys
from collections import deque

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

class Button:
    def __init__(self, name, modules):
        self.name = name
        self.dests = ['broadcaster']
        self.modules = modules
        self.pulses = [0, 0]
        self.inbox = None

    def press(self):
        for n in self.dests:
            self.send(n, 0)

    def send(self, name, signal):
        self.pulses[signal] += 1
        self.modules[name].receive(self.name, signal)

    def process(self):
        return False

    def __repr__(self):
        return 'Button()'

class Module:
    def __init__(self, name, dests, modules):
        self.name = name
        self.dests = dests
        self.modules = modules
        self.pulses = [0, 0]
        self.inbox = deque()
        self.srcs = []

    def send(self, name, signal):
        self.pulses[signal] += 1
        if name in self.modules:
            self.modules[name].receive(self.name, signal)

    def receive(self, name, signal):
        self.inbox.append((name, signal))

class Broadcaster(Module):
    def process(self):
        if not self.inbox:
            return False

        for i in range(len(self.inbox)):
            name, signal = self.inbox.popleft()
            for n in self.dests:
                self.send(n, signal)

        return True

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.dests})'

class FlipFlop(Module):
    def __init__(self, name, dests, modules):
        super().__init__(name, dests, modules)
        self.state = 0

    def process(self):
        if not self.inbox:
            return False

        for i in range(len(self.inbox)):
            name, signal = self.inbox.popleft()
            if signal == 0:
                self.state = 0 if self.state else 1
                for n in self.dests:
                    self.send(n, self.state)

        return True

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.srcs}, {self.dests}, {self.state})'

class Conjunction(Module):
    def __init__(self, name, dests, modules):
        super().__init__(name, dests, modules)
        self.mem = {}

    def process(self):
        if not self.inbox:
            return False

        for i in range(len(self.inbox)):
            name, signal = self.inbox.popleft()
            self.mem[name] = signal
            signal = 1
            if all(self.mem.values()):
                signal = 0

            for n in self.dests:
                self.send(n, signal)

        return True

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.srcs}, {self.dests}, {self.mem})'

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    modules = {}
    modules['button'] = Button('button', modules)

    for line in lines:
        line = line.replace(',', '')
        tup = line.split()
        if tup[0] == 'broadcaster':
            type = 'b'
            name = tup[0]
        else:
            type = tup[0][0]
            name = tup[0][1:]
        dests = sorted(tup[2:])

        if type == 'b':
            mod = Broadcaster(name, dests, modules)
        elif type == '%':
            mod = FlipFlop(name, dests, modules)
        elif type == '&':
            mod = Conjunction(name, dests, modules)
        else:
            assert 0, type

        modules[name] = mod

    # set sources
    d = {}
    for n, m in modules.items():
        d[n] = set()

    for n, m in modules.items():
        if n == 'button':
            continue
        for dest in m.dests:
            if dest in d:
                d[dest].add(n)
        
    for n, srcs in d.items():
        srcs = sorted(srcs)
        modules[n].srcs = srcs
        if isinstance(modules[n], Conjunction):
            modules[n].mem = {_: 0 for _ in srcs}

    return modules

def part1(modules):
    button = modules['button']
    for i in range(1000):
        button.press()
        while any(_.process() for _ in modules.values()):
            pass

    pulses = [0, 0]
    for mod in modules.values():
        debug(mod.name, mod.__class__.__name__, mod.pulses)
        for i, v in enumerate(mod.pulses):
            pulses[i] += v

    print(pulses[0] * pulses[1])

def part2(modules):
    button = modules['button']

    # find the module with 'rx' as a dest, peek the output of modules that are
    # sources of this module and compute period - then math.lcm
    mod = None
    for m in modules.values():
        if 'rx' in m.dests:
            mod = m
            break

    debug(mod)

    srcs = []
    for n in mod.srcs:
        m = modules[n]
        srcs.append(m)

    periods = {_.name: {'last': 0, 'period': 0, 'cnt': 0} for _ in srcs}

    i = 0
    while 1:
        i += 1

        button.press()

        while any(_.inbox for _ in modules.values()):
            for m in srcs:
                if i > 1 and all(_ == 0 for _ in m.mem.values()):
                    p = periods[m.name]
                    if p['period'] == i - p['last']:
                        p['cnt'] += 1
                    p['period'] = i - p['last']
                    p['last'] = i
                    debug(i, m, m.mem, p)

            for n, m in modules.items():
                m.process()

        if all(_['cnt'] > 0 for _ in periods.values()):
            break

    debug(i, periods)
    print(math.lcm(*[_['period'] for _ in periods.values()]))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()

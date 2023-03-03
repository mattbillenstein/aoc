#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    passports = []
    pp = {}
    for line in lines:
        if not line:
            passports.append(pp)
            pp = {}
        pp.update(dict(_.split(':') for _ in line.split()))
    passports.append(pp)
    return passports

def is_valid(passport):
    fields = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid') #'cid'
    return all(_ in passport for _ in fields)

def is_valid_2(passport):
    if not is_valid(passport):
        return False

    for k, v in passport.items():
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        # hgt (Height) - a number followed by either cm or in:
        #   If cm, the number must be at least 150 and at most 193.
        #   If in, the number must be at least 59 and at most 76.
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        # cid (Country ID) - ignored, missing or not.

        if k == 'byr':
            if not 1920 <= int(v) <= 2002:
                return False
        elif k == 'iyr':
            if not 2010 <= int(v) <= 2020:
                return False
        elif k == 'eyr':
            if not 2020 <= int(v) <= 2030:
                return False
        elif k == 'hgt':
            unit = v[-2:]
            if unit not in ('cm', 'in'):
                return False
            v = int(v[:-2])
            if unit == 'cm' and not 150 <= v <= 193:
                return False
            elif unit == 'in' and not 59 <= v <= 76:
                return False
        elif k == 'hcl':
            if v[0] != '#' or len(v) != 7 or any(_ not in '0123456789abcdef' for _ in v[1:]):
                return False
        elif k == 'ecl':
            if not v in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
                return False
        elif k == 'pid':
            if len(v) != 9 or any(_ not in '0123456789' for _ in v):
                return False
        elif k == 'cid':
            pass
        else:
            assert 0, k

    return True

def part1(passports):
    cnt = 0
    for pp in passports:
        if is_valid(pp):
            cnt += 1
    print(cnt)

def part2(passports):
    cnt = 0
    for pp in passports:
        if is_valid_2(pp):
            cnt += 1
    print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()

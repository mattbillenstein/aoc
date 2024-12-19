#!/usr/bin/env python3

import datetime
import json
import os
import os.path
import re
import sys
import urllib.request

with open(os.path.expanduser('~/src/mattb/dotfiles/aoc')) as f:
    cookie = f.read().strip()

headers = {
    'User-Agent': 'github.com/mattbillenstein/aoc/leaderboard.py v0 by matt@vazor.com',
    'Cookie': cookie,
}

year = datetime.datetime.today().year
if len(sys.argv) > 1:
    year = int(sys.argv[1])

board = '2731085'
if len(sys.argv) > 2:
    board = sys.argv[2]
    if board == 'other':
        board = '1808026'

url = f'https://adventofcode.com/{year}/leaderboard/private/view/{board}.json'
req = urllib.request.Request(url, headers=headers)
res = urllib.request.urlopen(req)
assert res.status == 200, res.status
data = json.loads(res.read().decode(res.headers.get_content_charset('utf-8')))


for id, d in sorted(data['members'].items(), key=lambda x: x[1]['local_score'], reverse=True):
    print(f"{d['name']:20s} stars:{d['stars']:2d} score:{d['local_score']:d}")

print()

for id, d in sorted(data['members'].items(), key=lambda x: x[1]['local_score'], reverse=True):
    print()
    print(f"{d['name']:20s} stars:{d['stars']:2d} score:{d['local_score']:d}")
    x = d['completion_day_level']
    for day in range(1, 26):
        start = int(datetime.datetime(year, 12, day, 0, 0, 0).timestamp()) - 3*3600
        k = str(day)
        if k not in x:
            continue
        ts = {}
        for star in (1, 2):
            ts[star] = x[k].get(str(star), {}).get('get_star_ts', '')
            if ts[star]:
                elapsed = ts[star] - start
                h = elapsed // 3600
                m = (elapsed - h*3600) // 60
                s = elapsed % 60
                ts[star] = f"{h:02d}h{m:02d}m{s:02d}s"
        print(f"{day:2d} {ts[1]} {ts[2]}")

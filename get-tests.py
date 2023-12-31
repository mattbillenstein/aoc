#!/usr/bin/env python3

import html
import os
import os.path
import re
import urllib.request

with open(os.path.expanduser('~/src/mattb/dotfiles/aoc')) as f:
    cookie = f.read().strip()

headers = {
    'User-Agent': 'github.com/mattbillenstein/aoc/get-test.py v0 by matt@vazor.com',
    'Cookie': cookie,
}

year = os.path.basename(os.path.dirname(os.getcwd()))
day = os.path.basename(os.getcwd())
day = day[1] if day[0] == '0' else day

url = f'https://adventofcode.com/{year}/day/{day}'
req = urllib.request.Request(url, headers=headers)
res = urllib.request.urlopen(req)
assert res.status == 200, res.status
data = res.read().decode(res.headers.get_content_charset('utf-8'))

tests = []

idx = 0
while 1:
    idx = data.find('<pre><code>', idx)
    if idx == -1:
        break

    idx += len('<pre>')

    eidx = data.find('</code>', idx)

    test = data[idx+len('<code>'):eidx]
    test = re.sub('<[/a-z]+>', '', test)
    test = html.unescape(test)
    if test not in tests:
        tests.append(test)

    idx = eidx

if not tests:
    print(data)
    print('Not found')
elif len(tests) == 1:
    with open('test.txt', 'w') as f:
        f.write(tests[0])
else:
    for i, test in enumerate(tests):
        with open(f'test{i+1}.txt', 'w') as f:
            f.write(test)

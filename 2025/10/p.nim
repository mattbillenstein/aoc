import os
import std/re
import std/strformat
import std/strutils
import std/tables

import itertools

var DEBUG = 0

type
  Machine = tuple
    lights: seq[int]
    buttons: seq[seq[int]]
    joltages: seq[int]
  
proc parse_input(): seq[Machine] =
  while true:
    var line: string
    try:
      line = readLine(stdin)
    except EOFError:
      break

    line = line.replace(re"[\[\]{}()]", "")

    var parts = line.split()

    var m: Machine = (@[], @[], @[])

    for c in parts[0]:
      if c == '#':
        m.lights.add(1)
      else:
        m.lights.add(0)

    for b in parts[1..parts.high-1]:
      var button = newSeq[int]()
      for idx in b.split(','):
        button.add(parseInt(idx))
      m.buttons.add(button)

    for j in parts[parts.high].split(','):
      m.joltages.add(parseInt(j))

    if DEBUG > 0:
      echo line
      echo m

    result.add(m)

proc part1(machines: seq[Machine]) =
  var tot = 0

  for m in machines:

    var lights: int = 0
    for i, v in m.lights:
      if v != 0:
        lights = lights or (1 shl i)

    var buttons: seq[int] = @[]
    for button in m.buttons:
      var b = 0
      for idx in button:
        b = b or (1 shl idx)
      buttons.add(b)

    if DEBUG > 0:
      echo m
      echo &"{lights} {buttons}"

    var found = -1
    for p in 1..100:
      for pressed in product(buttons, p):
        var L = 0
        for b in pressed:
          L = L xor b
        if L == lights:
          found = p
          break
      if found > -1:
        break

    assert found > -1
    tot += found

  echo tot

proc part2(prog: seq[Machine]) =
  echo "p2"

proc main() =
  let args = commandLineParams()
  for arg in args:
    if arg == "-v":
      DEBUG += 1

  let machines = parse_input()

  if "1" in args:
    part1(machines)
  if "2" in args:
    part2(machines)

main()

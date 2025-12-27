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
  echo machines[0].buttons
  for x in combinations(machines[0].buttons, 2):
    echo x

proc part2(prog: seq[Machine]) =
  echo "p2"

proc main() =
  let args = commandLineParams()
  for arg in args:
    if arg == "-v":
      DEBUG += 1

  let machines = parse_input()

  echo "main ", machines

  if "1" in args:
    part1(machines)
  if "2" in args:
    part2(machines)

main()

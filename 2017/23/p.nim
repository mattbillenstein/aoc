import os
import std/strformat
import std/strutils
import std/tables

var DEBUG = 0

type
  Op = enum
    Set, Sub, Jnz, Mod, Mul, Add

var op_table = {
  "set": Op.Set,
  "sub": Op.Sub,
  "jnz": Op.Jnz,
  "mod": Op.Mod,
  "mul": Op.Mul,
  "add": Op.Add,
}.toTable

type
  Instruction = tuple
    op: Op
    ar: int # ar/br register, a=0, b=1, etc
    ai: int # ai/bi immediate
    br: int
    bi: int

proc parse_input(): seq[Instruction] =
  var prog: seq[Instruction]
  while true:
    var line: string
    try:
      line = readLine(stdin)
    except EOFError:
      break

    let regs = "abcdefgh"
    var idx, ar, ai, br, bi: int = -1

    let L = split(line)

    idx = regs.find(L[1])
    if (idx > -1):
      ar = idx
    else:
      ai = parseInt(L[1])

    idx = regs.find(L[2])
    if (idx > -1):
      br = idx
    else:
      bi = parseInt(L[2])

    let instr: Instruction = (op_table[L[0]], ar, ai, br, bi)
    prog.add(instr)

  return prog

proc part1(prog: seq[Instruction]) =
  var pc = 0
  var regs: array[8, int]

  var muls = 0

  while 0 <= pc and pc < len(prog):
    if DEBUG > 0:
      echo &"{pc:>2} {prog[pc]:<45} {regs}"

    let (op, ar, ai, br, bi) = prog[pc]
    pc += 1

    var a = ai
    if ar > -1:
      a = ar

    var b = bi
    if br > -1:
      b = regs[br]

    case op:
      of Op.Set:
        regs[a] = b
      of Op.Sub:
        regs[a] -= b
      of Op.Jnz:
        if (ar > -1 and regs[ar] != 0) or (ai > -1 and ai != 0):
          pc += b - 1
      of Op.Mod:
        regs[a] = regs[a] mod b
      of Op.Mul:
        regs[a] *= b
        muls += 1
      of Op.Add:
        regs[a] += b

  echo muls

proc part2(prog: seq[Instruction]) =
  var pc = 0
  var regs: array[8, int]
  regs[0] = 1

  var muls = 0

  while 0 <= pc and pc < len(prog):
    if DEBUG > 0:
      echo &"{pc:>2} {prog[pc]:<45} {regs}"

    let (op, ar, ai, br, bi) = prog[pc]
    pc += 1

    var a = ai
    if ar > -1:
      a = ar

    var b = bi
    if br > -1:
      b = regs[br]

    case op:
      of Op.Set:
        regs[a] = b
      of Op.Sub:
        regs[a] -= b
      of Op.Jnz:
        if (ar > -1 and regs[ar] != 0) or (ai > -1 and ai != 0):
          pc += b - 1
      of Op.Mod:
        regs[a] = regs[a] mod b
      of Op.Mul:
        regs[a] *= b
        muls += 1
      of Op.Add:
        regs[a] += b

  echo regs[7]

proc main() =
  let args = commandLineParams()
  for arg in args:
    if arg == "-v":
      DEBUG += 1

  let prog = parse_input()

  if "1" in args:
    part1(prog)
  if "2" in args:
    part2(prog)

main()

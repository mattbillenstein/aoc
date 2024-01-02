import os
import std/bitops
import std/intsets
import std/strformat
import std/strutils
import std/tables

var DEBUG = 0

type
  Op = enum
    addi, addr, bani, banr, borr, bori, seti, setr, muli, mulr, gtrr, gtir, gtri, eqrr, eqir, eqri

var op_table = {
          "addi": Op.addi,
          "addr": Op.addr,
          "bani": Op.bani,
          "banr": Op.banr,
          "borr": Op.borr,
          "bori": Op.bori,
          "seti": Op.seti,
          "setr": Op.setr,
          "muli": Op.muli,
          "mulr": Op.mulr,
          "gtrr": Op.gtrr,
          "gtir": Op.gtir,
          "gtri": Op.gtri,
          "eqrr": Op.eqrr,
          "eqir": Op.eqir,
          "eqri": Op.eqri,
}.toTable

type 
    Instruction = tuple
        op: Op
        a: int
        b: int
        c: int

proc parse_input(): (int, seq[Instruction]) =
    var ipreg: int = -1
    var prog: seq[Instruction]
    while true:
        try:
            let line = readLine(stdin)
            if line[0] == '#':
                ipreg = parseInt(split(line)[1])
            else:
                let L = split(line)
                let instr: Instruction = (op_table[L[0]], parseInt(L[1]), parseInt(L[2]), parseInt(L[3]))
                prog.add(instr)
        except EOFError:
            break

    return (ipreg, prog)

proc part(ipreg: int, prog: seq[Instruction]) =
    var ip = 0
    var regs: array[6, int]
    var last = -1
    var seen = initIntSet()
    while 0 <= ip and ip < len(prog):
        regs[ipreg] = ip

        if DEBUG > 0:
            echo &"{ip:>2} {prog[ip]:<45} {regs}"

        if ip == 28:
            if regs[4] in seen:
                echo last
                return

            if last == -1:
                echo regs[4]
            last = regs[4]
            seen.incl(regs[4])

        let (op, a, b, c) = prog[ip]

        case op:
          of Op.addi:
            regs[c] = regs[a] + b
          of Op.addr:
            regs[c] = regs[a] + regs[b]
          of Op.bani:
            regs[c] = bitand(regs[a], b)
          of Op.banr:
            regs[c] = bitand(regs[a], regs[b])
          of Op.borr:
            regs[c] = bitor(regs[a], regs[b])
          of Op.bori:
            regs[c] = bitor(regs[a], b)
          of Op.seti:
            regs[c] = a
          of Op.setr:
            regs[c] = regs[a]
          of Op.muli:
            regs[c] = regs[a] * b
          of Op.mulr:
            regs[c] = regs[a] * regs[b]
          of Op.gtrr:
            regs[c] = int(regs[a] > regs[b])
          of Op.gtir:
            regs[c] = int(a > regs[b])
          of Op.gtri:
            regs[c] = int(regs[a] > b)
          of Op.eqrr:
            regs[c] = int(regs[a] == regs[b])
          of Op.eqir:
            regs[c] = int(a == regs[b])
          of Op.eqri:
            regs[c] = int(regs[a] == b)

        ip = regs[ipreg]
        ip += 1

proc main() =
    let args = commandLineParams()
    for arg in args:
        if arg == "-v":
            DEBUG += 1
    let (ipreg, prog) = parse_input()
    part(ipreg, prog)

main()

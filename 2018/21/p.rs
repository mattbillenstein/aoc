use std::io;
use std::collections::HashSet;

#[derive(Debug)]
enum Instruction {
    Addi(usize, usize, usize),
    Addr(usize, usize, usize),
    Bani(usize, usize, usize),
    Banr(usize, usize, usize),
    Borr(usize, usize, usize),
    Bori(usize, usize, usize),
    Seti(usize, usize, usize),
    Setr(usize, usize, usize),
    Muli(usize, usize, usize),
    Mulr(usize, usize, usize),
    Gtrr(usize, usize, usize),
    Gtir(usize, usize, usize),
    Gtri(usize, usize, usize),
    Eqrr(usize, usize, usize),
    Eqir(usize, usize, usize),
    Eqri(usize, usize, usize),
}

fn parse_input() -> (usize, Vec<Instruction>) {
    let mut ipreg = 0;
    let mut prog: Vec<Instruction> = Vec::new();
    for res in io::stdin().lines() {
        let line = res.unwrap();
        let parts: Vec<&str> = line.split(' ').collect();
        if line.starts_with("#ip") {
            ipreg = parts[1].parse().unwrap();
        } else {
            let ints: Vec<usize> = parts[1..].iter().map(|x| x.parse().unwrap()).collect();
            let instr = match parts[0] {
                "addi" => Instruction::Addi,
                "addr" => Instruction::Addr,
                "bani" => Instruction::Bani,
                "banr" => Instruction::Banr,
                "borr" => Instruction::Borr,
                "bori" => Instruction::Bori,
                "seti" => Instruction::Seti,
                "setr" => Instruction::Setr,
                "muli" => Instruction::Muli,
                "mulr" => Instruction::Mulr,
                "gtrr" => Instruction::Gtrr,
                "gtir" => Instruction::Gtir,
                "gtri" => Instruction::Gtri,
                "eqrr" => Instruction::Eqrr,
                "eqir" => Instruction::Eqir,
                "eqri" => Instruction::Eqri,
                _ => panic!("Unmatched"),
            };
            prog.push(instr(ints[0], ints[1], ints[2]));
        }
    }
    (ipreg, prog)
}

fn part(ipreg: usize, prog: Vec<Instruction>) {
    let mut ip: usize = 0;
    let mut regs: [usize; 6] = [0; 6];
    let mut last: Option<usize> = None;
    let mut seen = HashSet::new();
    while ip < prog.len() {
        regs[ipreg] = ip;

        if ip == 28 {
            if seen.contains(&regs[4]) {
                if let Some(x) = last {
                    println!("{}", x);
                }
                break;
            }

            if let None = last {
                println!("{}", regs[4]);
            }

            last = Some(regs[4]);
            seen.insert(regs[4]);
        }

        match prog[ip] {
            Instruction::Addi(a, b, c) => {regs[c] = regs[a] + b},
            Instruction::Addr(a, b, c) => {regs[c] = regs[a] + regs[b]},
            Instruction::Bani(a, b, c) => {regs[c] = regs[a] & b},
            Instruction::Banr(a, b, c) => {regs[c] = regs[a] & regs[b]},
            Instruction::Bori(a, b, c) => {regs[c] = regs[a] | b},
            Instruction::Borr(a, b, c) => {regs[c] = regs[a] | regs[b]},
            Instruction::Seti(a, _, c) => {regs[c] = a},
            Instruction::Setr(a, _, c) => {regs[c] = regs[a]},
            Instruction::Muli(a, b, c) => {regs[c] = regs[a] * b},
            Instruction::Mulr(a, b, c) => {regs[c] = regs[a] * regs[b]},
            Instruction::Gtir(a, b, c) => {regs[c] = if a > regs[b] { 1 } else { 0 }},
            Instruction::Gtri(a, b, c) => {regs[c] = if regs[a] > b { 1 } else { 0 }},
            Instruction::Gtrr(a, b, c) => {regs[c] = if regs[a] > regs[b] { 1 } else { 0 }},
            Instruction::Eqir(a, b, c) => {regs[c] = if a == regs[b] { 1 } else { 0 }},
            Instruction::Eqri(a, b, c) => {regs[c] = if regs[a] == b { 1 } else { 0 }},
            Instruction::Eqrr(a, b, c) => {regs[c] = if regs[a] == regs[b] { 1 } else { 0 }},
        }

        ip = regs[ipreg];
        ip += 1;
    }
}

fn main() {
    let (ipreg, prog) = parse_input();
    part(ipreg, prog);
}

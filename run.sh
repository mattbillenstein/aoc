#!/bin/bash

set -eo pipefail

export PATH="$(pwd)/bin:$PATH"

START=$(date +'%s')

cd $1 > /dev/null

EXE="$AOCPY ./p.py"
if [ -e p.rs ] && [ "$(which rustc)" != "" ]; then
  rustc -O p.rs
  EXE="./p"
elif [ -e p.nim ] && [ "$(which nim)" != "" ]; then
  nim compile -d:release -o:p.exe p.nim 2> /dev/null
  EXE="./p.exe"
fi

if [[ "$AOCPY ./p.py" =~ .*pypy3\ ./p\.py$ ]] || grep -q pypy3 ./p.py; then
  source ../../.venv-pypy3/bin/activate
else
  source ../../.venv-python3/bin/activate
fi

if [ -e input-mod.txt ]; then
  $EXE 1 < input.txt > output.txt
  $EXE 2 < input-mod.txt >> output.txt
else
  $EXE 1 2 < input.txt > output.txt
fi

END=$(date +'%s')
echo "$1 $(($END - $START))"

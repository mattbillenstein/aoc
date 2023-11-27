#!/bin/bash

set -eo pipefail

export PATH="$(pwd)/bin:$PATH"

START=$(date +'%s')

cd $1 > /dev/null

if [ -e input-mod.txt ]; then
  $AOCPY ./p.py 1 < input.txt > output.txt
  $AOCPY ./p.py 2 < input-mod.txt >> output.txt
else
  $AOCPY ./p.py 1 2 < input.txt > output.txt
fi

END=$(date +'%s')
echo "$1 $(($END - $START))"

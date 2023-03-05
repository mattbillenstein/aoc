#!/bin/bash

set -eo pipefail

START=$(date +'%s')

cd $1 > /dev/null

if [ -e input-mod.txt ]; then
  ./p.py 1 < input.txt > output.txt
  ./p.py 2 < input-mod.txt >> output.txt
else
  ./p.py 1 2 < input.txt > output.txt
fi

END=$(date +'%s')
echo "$1 $(($END - $START))"

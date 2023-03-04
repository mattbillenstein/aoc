#!/bin/bash

set -eo pipefail

for d in */[0-9][0-9]; do
  echo $d
  pushd $d
  if [ -e input-mod.txt ]; then
    ./p.py 1 < input.txt > output.txt
    ./p.py 2 < input-mod.txt >> output.txt
  else
    ./p.py 1 2 < input.txt > output.txt
  fi
  popd
done

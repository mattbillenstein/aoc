#!/bin/bash

set -eo pipefail

for d in */[0-9][0-9]; do
  if [ "$(cat $d/output.txt)" != "$(cat $d/answers.txt)" ]; then
    echo $d
    echo '----'
    cat $d/output.txt
    echo '----'
    cat $d/answers.txt
    echo '----'
    read x
  fi
done

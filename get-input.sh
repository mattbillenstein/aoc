#!/bin/bash

set -eo pipefail

COOKIE="$(cat ~/src/mattb/dotfiles/aoc)"

YEAR="$(basename $(dirname $PWD))"
DAY="$(basename $PWD)"

mkdir -p ../../../aoc-input/$YEAR/$DAY

UA="github.com/mattbillenstein/aoc/get-input.sh v0 by matt@vazor.com"
curl -s --header "Cookie: $COOKIE" --header "User-Agent: $UA" https://adventofcode.com/$YEAR/day/$(echo $DAY | sed -e 's/^0//')/input > ../../../aoc-input/$YEAR/$DAY/input.txt

ln -s ../../../aoc-input/$YEAR/$DAY/input.txt .

if [ ! -e p.py ]; then
  cp ../../p.py .
fi

#!/bin/bash

set -eo pipefail

COOKIE="$(cat ~/src/mattb/dotfiles/aoc)"

YEAR="$(date --utc +'%Y')"
DAY="$(date --utc +'%_d' | tr -d ' ')"
if [ "$1" != "" ]; then
  YEAR="$1"
  DAY="$2"
fi

UA="github.com/mattbillenstein/aoc/get-data.sh v0 by matt@vazor.com"
curl -s --header "Cookie: $COOKIE" --header "User-Agent: $UA" https://adventofcode.com/$YEAR/day/$DAY/input > input.txt

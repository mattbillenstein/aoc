#!/bin/bash

set -eo pipefail

COOKIE="$(cat ~/src/mattb/dotfiles/aoc)"

YEAR="$(basename $(dirname $PWD))"
DAY="$(basename $PWD | sed -e 's/^0//')"

UA="github.com/mattbillenstein/aoc/get-answers.sh v0 by matt@vazor.com"
curl -s --header "Cookie: $COOKIE" --header "User-Agent: $UA" https://adventofcode.com/$YEAR/day/$DAY | grep 'Your puzzle answer' | sed -e 's:^.*<p>Your puzzle answer was <code>\([^<]*\)</code>\.</p>.*$:\1:'

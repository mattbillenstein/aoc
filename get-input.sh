#!/bin/bash

set -eo pipefail

COOKIE="$(cat ~/src/mattb/dotfiles/aoc)"

YEAR="$(basename $(dirname $PWD))"
DAY="$(basename $PWD)"

pushd ../../../aoc-input
mkdir -p $YEAR/$DAY

UA="github.com/mattbillenstein/aoc/get-input.sh v0 by matt@vazor.com"
curl -s --header "Cookie: $COOKIE" --header "User-Agent: $UA" https://adventofcode.com/$YEAR/day/$(echo $DAY | sed -e 's/^0//')/input > $YEAR/$DAY/input.txt

if grep -q 'Please log in' $YEAR/$DAY/input.txt; then
  echo 'Error, please login and update your aoc session token'
  exit 1
fi

git add $YEAR/$DAY
git commit -am "$YEAR Day $DAY"
git pushme
popd

ln -s ../../../aoc-input/$YEAR/$DAY/input.txt .
if [ ! -e p.py ]; then
  cp ../../p.py .
fi

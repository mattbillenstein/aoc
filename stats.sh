#!/bin/bash

set -eo pipefail

YEAR="$1"
if [ "$YEAR" == "" ]; then
  YEAR="$(date +'%Y')"
fi

COOKIE="$(cat ~/src/mattb/dotfiles/aoc)"
UA="github.com/mattbillenstein/aoc/get-input.sh v0 by matt@vazor.com"
curl -s --header "Cookie: $COOKIE" --header "User-Agent: $UA" https://adventofcode.com/$YEAR/stats \
  | sed -e 's/^.*<a /<a /' \
  | grep "href=\"/$YEAR/day/" | sed -e 's/<[^<]*>//g' \
  | awk '{printf "%2d %7d (%4.1f%%) %7d (%4.1f%%) %7d\n", $1, $2, $2 * 100 / ($2 + $3), $3, $3 * 100 / ($2 + $3), $2 + $3}'

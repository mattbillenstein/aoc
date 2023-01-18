#!/usr/bin/env -S gnuplot -p -c

reset session

set xyplane relative 0
set view equal xyz
set view 60,30,1.0
set xtics auto
set ytics auto
set ztics auto
set key noautotitle

splot for [i=0:3] ARG1 u 1:i/2+3:i%2+5:($2-$1):(0):(0):0 w vec lc var nohead, \
      for [i=0:3]   '' u i/2+1:3:i%2+5:(0):($4-$3):(0):0 w vec lc var nohead, \
      for [i=0:3]   '' u i/2+1:i%2+3:5:(0):(0):($6-$5):0 w vec lc var nohead

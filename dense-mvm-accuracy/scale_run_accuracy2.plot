set terminal png size 1150,280 enhanced
set output 'scale_run_accuracy2.png'
#set title "Event accuracy comparison for DP dense quadratic matrix-vector-multiplication with 4 threads (pinned)\nIntel Broadwell E5-2697 v4 @ 2.30GHz, NO Prefetchers"  font ",14"

set yrange [0:]
set xrange [100:30000]
set key at 800,15
set ylabel 'Bytes per y[] update' font ",13"
#set label 1 "Event used by LIKWID to derive the \nL3 load data volume metric" at 10000,40 center
set arrow 1 from 100,8 to 30000,8 nohead lc 'grey'
set arrow 2 from 100,16 to 30000,16 nohead lc 'grey'
set logscale x
set xtics auto font ",13"
set ytics auto  font ",13"
set xlabel 'Number of rows in quadratic matrix' font ",13"

set output 'scale_run_accuracy_nopf.png'

plot 'broadep2_LIKWID_L2_PAPI_L1_LDM_nopf.dat' u 1:(($3*1E9)/($1*$1*$2)) w lines title 'L2\_TRANS.DEMAND\_DATA\_RD' lw 2 lc 'red', \
     'broadep2_LIKWID_L2_PAPI_L1_LDM_nopf.dat' u 1:(($4*1E9)/($1*$1*$2)) w lines title 'L1D.REPLACEMENT' lw 2 lc 'green', \
     'broadep2_LIKWID_L3_PAPI_L2_LDM_nopf.dat' u 1:(($3*1E9)/($1*$1*$2)) w lines title 'L2\_RQSTS.DEMAND\_DATA\_RD\_MISS' lw 2 lc 'blue', \
     'broadep2_LIKWID_L3_PAPI_L2_LDM_nopf.dat' u 1:(($4*1E9)/($1*$1*$2)) w lines title 'L2\_LINES\_IN.ALL' lw 2 lc 'magenta'

#set title "Event accuracy comparison for DP dense quadratic matrix-vector-multiplication with 4 threads (pinned)\nIntel Broadwell E5-2697 v4 @ 2.30GHz, WITH Prefetchers"  font ",14"
set output 'scale_run_accuracy_pf.png'

plot 'broadep2_LIKWID_L2_PAPI_L1_LDM_pf.dat' u 1:(($3*1E9)/($1*$1*$2)) w lines title 'L2\_TRANS.DEMAND\_DATA\_RD' lw 2 lc 'red', \
     'broadep2_LIKWID_L2_PAPI_L1_LDM_pf.dat' u 1:(($4*1E9)/($1*$1*$2)) w lines title 'L1D.REPLACEMENT' lw 2 lc 'green', \
     'broadep2_LIKWID_L3_PAPI_L2_LDM_pf.dat' u 1:(($3*1E9)/($1*$1*$2)) w lines title 'L2\_RQSTS.DEMAND\_DATA\_RD\_MISS' lw 2 lc 'blue', \
     'broadep2_LIKWID_L3_PAPI_L2_LDM_pf.dat' u 1:(($4*1E9)/($1*$1*$2)) w lines title 'L2\_LINES\_IN.ALL' lw 2 lc 'magenta'


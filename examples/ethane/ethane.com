mem=60GB
%nprocshared=28
# opt=(calcfc,verytight,maxcyc=400) freq cbs-qb3 nosymm geom=connectivity
ccsd=maxcyc=1000

Title Card Required

0 1
 C                 -0.81811172    0.30578512   -0.01070967
 H                 -0.46145729   -0.70302488   -0.01070967
 H                 -0.46143888    0.81018331   -0.88436117
 H                 -1.88811172    0.30579830   -0.01070967
 C                 -0.30476950    1.03174139    1.24669530
 H                  0.76523050    1.03171130    1.24670472
 H                 -0.66140832    2.04055691    1.24668575
 H                 -0.66145800    0.52735392    2.12034659

 1 2 1.0 3 1.0 4 1.0 5 1.0
 2
 3
 4
 5 6 1.0 7 1.0 8 1.0
 6
 7
 8


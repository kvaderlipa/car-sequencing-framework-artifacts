- seems every file is demand for shift, 

- car classes ase same for all instances
- option restrictions are also same for all instances
- just demand for shift is changed,, for my purposes, I will put incrementaly all three shifts together to emulate day shift, then try to solve

#cars 6 12
1 3 1 1 1 2
3 4 2 6 4 3
0 #carsPerClass 1 1 0 0 0 0
1 #carsPerClass 0 1 1 0 0 0
2 #carsPerClass 1 0 0 0 0 0
3 #carsPerClass 0 1 1 1 0 0
4 #carsPerClass 0 0 0 0 0 1
5 #carsPerClass 0 1 1 0 0 1
6 #carsPerClass 0 1 1 0 1 1
7 #carsPerClass 0 1 1 1 0 1
8 #carsPerClass 1 0 0 0 0 1
9 #carsPerClass 0 0 0 0 0 0
10 #carsPerClass 0 1 1 0 0 0
11 #carsPerClass 0 1 1 1 0 0


- for testing reason I aggregate sequence to desired sequence size 1200 by sctipt 
- aggregated.py 1200

Aggregates consecutive production-shift instances into larger sequencing instances with a user-defined target number of vehicles (e.g., 1200 vehicles per aggregated instance).

Preserves the original CSP structure and option-capacity constraints while replacing individual shift demands with the aggregated demand obtained from multiple consecutive shifts.

Automatically validates that all source instances use identical class definitions, option signatures, and H:NH:NH:N constraints before aggregation.

Generates aggregated benchmark instances together with a reproducibility log identifying the source shifts used to construct each aggregated sequence.

Produces longer sequence horizons that more closely resemble full daily production sequencing scenarios while retaining the characteristics of the original industrial demand data.
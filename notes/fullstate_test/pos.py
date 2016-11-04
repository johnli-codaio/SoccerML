from collections import defaultdict
from heapq import nlargest

d = defaultdict(int)
with open('fullstate_1_pos.txt', 'r') as f:
  for line in f:
    d[line.strip()] += 1

for k in sorted(d, key=lambda k:d[k]):
  print k, d[k]

# (5,-25,10) 394
# (6,-25,0) 397
# (7,-15,-5) 411
# (4,-25,-10) 420
# (8,-15,5) 438
# (3,-25,5) 449
# (9,-15,-10) 452
# (10,-15,10) 460
# (2,-25,-5) 479
# (1,-49,0) 486
# (11,-15,0) 492
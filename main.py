from methods import *
from rounding import *
from sorting import by_value
from math import floor

out = base_prop(2018, b=5, round=standard, parliament_size=705)
# out = dhondt(2013)
# out = spline(2019)
# out = real(2013)
out = by_value(out, lambda x: x[1].population)

s=0
for k in out:
    print(k, out[k])
    s += out[k].seats

print(s)

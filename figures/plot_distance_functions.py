import numpy as np

from math import *
from decimal import Decimal

# Function distance between two points
# and calculate distance value to given
# root value(p is root value)
def p_root(value, root):
    root_value = 1 / float(root)
    return round(Decimal(value) **
                 Decimal(root_value), 3)


def minkowski_distance(x, y, p_value):
    # pass the p_root function to calculate
    # all the value of vector parallely
    return (p_root(sum(pow(abs(a - b), p_value)
                       for a, b in zip(x, y)), p_value))


t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

plt.figure()
plt.subplot(211)
plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

plt.subplot(212)
plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
plt.show()
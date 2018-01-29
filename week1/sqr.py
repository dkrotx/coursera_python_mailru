import math
import sys

a, b, c = map(int, sys.argv[1:])
D = b*b - 4*a*c
assert(D > 0)

x1 = (-b + math.sqrt(b*b - 4*a*c)) / 2*a
x2 = (-b - math.sqrt(b*b - 4*a*c)) / 2*a

print(int(x1))
print(int(x2))

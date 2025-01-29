from math import sin, cos
from math import pi
g = 9.81
v = input('Hitrost?')
o = input('Kot?')
x = (pi * int(o)) / 180
s = (int(v) ** 2 * (2 * sin(x) * cos(x))) / g
print('Pot je', s, 'm.')

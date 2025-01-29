import math

najm = float(math.inf)
najv = - float(math.inf)

for vrstica in open('vremenske-postaje.txt', encoding='UTF-8'):
    kraj, datum, temp1, temp2 = vrstica.split(',')
    temp1 = float(temp1)
    temp2 = float(temp2)
    if temp1 > najv:
        najv = temp1
    if temp2 < najm:
        najm = temp2
print(najm, najv)
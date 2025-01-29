
a = []
seznam = []
for vrstica in open('zapisnik1.txt', encoding='UTF-8'):
    predmet, _, cena = vrstica.split(',')
    seznam.append([predmet, cena])



print(seznam)

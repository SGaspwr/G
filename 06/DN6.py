
def unikati(s):
    novi_seznam = []
    for oseba in s:
        if oseba not in novi_seznam:
            novi_seznam.append(oseba)
    return novi_seznam
def skupnih(s, t):
    stevilo = 0
    a = []
    b = []
    for oseba2 in t:
        if oseba2 not in a:
            a.append(oseba2)
    for oseba1 in s:
        if oseba1 not in b:
            b.append(oseba1)
    for oseba3 in a:
        if oseba3 in b:
            stevilo += 1
    return stevilo
def vseh(s, t):
    stevilo = 0
    a = []
    for oseba2 in t:
        if oseba2 not in a:
            a.append(oseba2)
            stevilo +=1
    for oseba1 in s:
        if oseba1 not in a:
            a.append(oseba1)
            stevilo += 1
    return stevilo
def preberi_datoteko(ime_dat, locilo):
    seznam = []
    for vrstica in open(ime_dat, encoding = 'UTF-8'):
        use = vrstica.split(locilo)
        seznam.append(use)
    return seznam

def filtriran(s, stolpec, vrednost):
    n = []
    for all in s:
        if all[stolpec] == vrednost:
            n.append(all)
    return n

def izlusci(s, stolpec):
    n = []
    for a, b, c, d in s:
        if stolpec == 0:
            n.append(a)
        elif stolpec == 1:
            n.append(b)
        elif stolpec == 2:
            n.append(c)
        else:
            n.append(d)
    return n

def predmeti(ime_dat, oseba):
    a = preberi_datoteko(ime_dat, ',')
    n = []
    s = filtriran(a, 1, oseba)
    for predmet, _, _ in s:
        if predmet not in n:
            n.append(predmet)

    return n

def osebe(ime_dat, predmet):
    seznam = preberi_datoteko(ime_dat, ',')
    n = []
    s = filtriran(seznam, 0, predmet)
    for _, oseba, _ in s:
        if oseba not in n:
            n.append(oseba)
    return n

def podobnost_oseb(ime_dat, oseba1, oseba2):
    o1 = predmeti(ime_dat, oseba1)
    o2 = predmeti(ime_dat, oseba2)
    vsi = vseh(o2, o1)
    skupni = skupnih(o2, o1)
    razultat = skupni/vsi
    return razultat

def podobnost_predmetov(ime_dat, predmet1, predmet2):
    p1 = osebe(ime_dat, predmet1)
    p2 = osebe(ime_dat, predmet2)
    vsi = vseh(p1, p2)
    skupni = skupnih(p1, p2)
    razultat = skupni/vsi
    return razultat

def argmax(s):
    max_k = max_v = None

    for k, v in s:
        if max_v is None or v > max_v:
            max_v = v
            max_k = k
    return max_k

def priporoci_predmet(ime_dat, predmet):
    n= []
    m = []
    seznam = preberi_datoteko(ime_dat, ',')
    for a, _, _ in seznam:
        if a not in n and a != predmet:
            n.append(a)
    for predmeti in n:
        s = podobnost_predmetov(ime_dat, predmeti, predmet)
        if s not in m:
            m.append([predmeti, s])
    return argmax(m)

def priporoci_prijatelja(ime_dat, oseba):
    n = []
    m = []
    seznam = preberi_datoteko(ime_dat, ',')
    for _, a, _ in seznam:
        if a not in n and a != oseba:
            n.append(a)
    for osebe in n:
        s = podobnost_oseb(ime_dat, osebe, oseba)
        if s not in m:
            m.append([osebe, s])
    return argmax(m)





import unittest
import os
import warnings

class NoWarning(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


class TestSeznami(NoWarning):
    def test_01_unikati(self):
        s = ["Ana", "Ana", "Berta", "Cilka", "Ana", "Berta", "Berta", "Berta", "Ema", "Dani", "Cilka"]
        t = s.copy()
        self.assertEqual(["Ana", "Berta", "Cilka", "Ema", "Dani"], unikati(s))
        self.assertEqual(t, s, "Pusti seznam, ki ga funkcija dobi kot argument, pri miru!")
        self.assertEqual([], unikati([]))
        self.assertEqual(["Ana"], unikati(["Ana"]))
        self.assertEqual([5, 8, 3], unikati([5, 8, 3]))
        self.assertEqual([5, 8, 3], unikati([5, 5, 5, 5, 8, 5, 8, 8, 8, 3, 3, 3, 5]))

    def test_02_skupnih(self):
        s = ["Ana", "Ana", "Berta", "Cilka", "Ana", "Berta", "Berta", "Berta", "Ema", "Dani", "Cilka"]
        sc = s.copy()
        t = ["Cilka", "Fanči", "Ana", "Ana", "Fanči", "Ana", "Cilka"]
        tc = t.copy()
        self.assertEqual(2, skupnih(s, t))
        self.assertEqual(2, skupnih(t, s))
        self.assertEqual(sc, s, "Pusti seznam, ki ga funkcija dobi kot argument, pri miru!")
        self.assertEqual(tc, t, "Pusti seznam, ki ga funkcija dobi kot argument, pri miru!")
        self.assertEqual(0, skupnih(s, ["Fanči", "Greta"]))
        self.assertEqual(1, skupnih(t, ["Fanči", "Greta"]))
        self.assertEqual(0, skupnih(s, []))
        self.assertEqual(0, skupnih([], []))

    def test_03_vseh(self):
        s = ["Ana", "Ana", "Berta", "Cilka", "Ana", "Berta", "Berta", "Berta", "Ema", "Dani", "Cilka"]
        sc = s.copy()
        t = ["Cilka", "Fanči", "Ana", "Ana", "Fanči", "Ana", "Cilka"]
        tc = t.copy()
        self.assertEqual(6, vseh(s, t))
        self.assertEqual(6, vseh(t, s))
        self.assertEqual(sc, s, "Pusti seznam, ki ga funkcija dobi kot argument, pri miru!")
        self.assertEqual(tc, t, "Pusti seznam, ki ga funkcija dobi kot argument, pri miru!")
        self.assertEqual(7, vseh(s, ["Fanči", "Greta"]))
        self.assertEqual(4, vseh(t, ["Fanči", "Greta"]))
        self.assertEqual(5, vseh(s, []))
        self.assertEqual(0, vseh([], []))


class TestProcesiranjeSeznamov(NoWarning):
    def test_01_preberi_datoteko(self):
        self.assertEqual([['Cube', '5031', '159', 'Janez', '2017\n'],
                          ['Stevens', '3819', '1284', 'Ana', '2012\n'],
                          ['Focus', '3823', '1921', 'Benjamin', '2019\n']],
                         preberi_datoteko("kolesa.txt", "-"))
        self.assertEqual([['slika', 'Berta', '31\n'],
                          ['slika', 'Ana', '33\n'],
                          ['slika', 'Berta', '35\n'],
                          ['slika', 'Fanči', '37\n'],
                          ['slika', 'Ana', '40\n']],
                         preberi_datoteko("zapisnik.txt", ",")[:5])

    def test_02_filter(self):
        s = [["Ana", 5, 9, "Berta"],
             ["Cilka", 5, 12, "Berta"],
             ["Ana", 5, 9, "Cilka"],
             ["Berta", 5, 1, "Ana"]]
        self.assertEqual(
            [["Ana", 5, 9, "Berta"],
             ["Ana", 5, 9, "Cilka"]], filtriran(s, 0, "Ana")
        )
        self.assertEqual(
            [["Ana", 5, 9, "Cilka"],
             ["Ana", 5, 9, "Berta"]], filtriran(s[::-1], 0, "Ana")
        )
        self.assertEqual(s, filtriran(s, 1, 5))
        self.assertEqual([], filtriran(s, 0, "Dani"))
        self.assertEqual([["Ana", 5, 9, "Cilka"]], filtriran(s, 3, "Cilka"))

    def test_03_izlusci(self):
        s = [["Ana", 5, 9, "Berta"],
             ["Cilka", 5, 12, "Berta"],
             ["Ana", 5, 9, "Cilka"],
             ["Berta", 5, 1, "Ana"]]
        self.assertEqual(["Ana", "Cilka", "Ana", "Berta"], izlusci(s, 0))
        self.assertEqual([5, 5, 5, 5], izlusci(s, 1))
        self.assertEqual([9, 12, 9, 1], izlusci(s, 2))


class TestDrazba(NoWarning):
    def test_01_predmeti(self):
        self.assertEqual(['slika', 'Meldrumove vaze'], predmeti("zapisnik.txt", "Ana"))
        self.assertEqual(['slika', 'skodelice', 'kip', 'čajnik'], predmeti("zapisnik.txt", "Berta"))
        self.assertEqual(['Meldrumove vaze', 'kip', 'srebrn jedilni servis'], predmeti("zapisnik.txt", "Cilka"))
        self.assertEqual([], predmeti("zapisnik.txt", "Benjamin"))

        try:
            os.rename("zapisnik.txt", "zapisnik-2.txt")
            self.assertEqual(['slika', 'Meldrumove vaze'], predmeti("zapisnik-2.txt", "Ana"))
        finally:
            os.rename("zapisnik-2.txt", "zapisnik.txt")

    def test_02_osebe(self):
        self.assertEqual(['Cilka', 'Ema', 'Berta', 'Dani', 'Greta'], osebe("zapisnik.txt", "kip"))
        self.assertEqual(['Fanči', 'Helga'], osebe("zapisnik.txt", "perzijska preproga"))
        self.assertEqual([], osebe("zapisnik.txt", "stol brez noge"))

    def test_03_podobnost_oseb(self):
        self.assertAlmostEqual(0.2, podobnost_oseb("zapisnik.txt", "Ana", "Berta"))
        self.assertAlmostEqual(0.5, podobnost_oseb("zapisnik.txt", "Cilka", "Ema"))
        self.assertAlmostEqual(0.25, podobnost_oseb("zapisnik.txt", "Ana", "Cilka"))
        self.assertAlmostEqual(1 / 6, podobnost_oseb("zapisnik.txt", "Berta", "Cilka"))
        self.assertAlmostEqual(1, podobnost_oseb("zapisnik.txt", "Berta", "Berta"))

    def test_04_podobnost_predmetov(self):
        self.assertAlmostEqual(0.4, podobnost_predmetov("zapisnik.txt", "kip", "skodelice"))
        self.assertAlmostEqual(1 / 7, podobnost_predmetov("zapisnik.txt", "kip", "slika"))
        self.assertAlmostEqual(0, podobnost_predmetov("zapisnik.txt", "kip", "perzijska preproga"))
        self.assertAlmostEqual(1, podobnost_predmetov("zapisnik.txt", "kip", "kip"))


class TestPriporocila(NoWarning):
    def test_01_priporoci_predmet(self):
        self.assertEqual("srebrn jedilni servis", priporoci_predmet("zapisnik.txt", "kip"))
        self.assertEqual("Meldrumove vaze", priporoci_predmet("zapisnik.txt", "slika"))

    def test_02_priporoci_prijatelja(self):
        self.assertEqual("Fanči", priporoci_prijatelja("zapisnik.txt", "Ana"))
        self.assertEqual("Dani", priporoci_prijatelja("zapisnik.txt", "Berta"))


if __name__ == "__main__":
    unittest.main()
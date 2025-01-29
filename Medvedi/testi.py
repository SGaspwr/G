import csv
from datetime import datetime
import numpy as np

def preberi_podatke():
    branje = open('Brown bear Slovenia 1993-1999.csv', encoding='UTF-8')
    st = (len(branje.readlines())) - 1
    imena = np.empty(st, dtype='U50')
    datumi = np.empty((st, 3), dtype=int)
    xy = np.empty((st, 2), dtype=float)
    dnevi = np.empty(st, dtype=int)
    najstarejsi_datum = None
    s = 0
    x = 0
    for vrstica in csv.DictReader(open('Brown bear Slovenia 1993-1999.csv', encoding='UTF-8')):
        imena[s] = vrstica['individual-local-identifier']
        a = vrstica['timestamp'].split(' ')
        b = a[0].split('-')
        m = [int(x) for x in b]
        datumi[s] = m
        lat_diff = (float(vrstica['location-lat']) - 45.9709794) * (40007 / 360)
        lon_diff = (float(vrstica['location-long']) - 14.1118016) * (40075 * np.cos(np.radians(45.9709794)) / 360)
        xy[s] = [lat_diff, lon_diff]
        if najstarejsi_datum is None or m < najstarejsi_datum:
            najstarejsi_datum = m
        s += 1
    while x < st:
        dnevi[x] = (datetime(*datumi[x]) - datetime(*najstarejsi_datum)).days
        x += 1
    return imena, datumi, dnevi, xy

imena, datumi, dnevi, xy = preberi_podatke()

def medvedi():
    return sorted(np.unique(imena))

def n_meritev():
    ime, st = (np.unique(imena, return_counts=True))
    return dict(zip(ime, st))

def razponi():
    d = {}
    for x in medvedi():
        podatki = dnevi[imena == x]
        a = np.ptp(podatki)
        d[x] = a
    return d

def n_zaporednih_meritev(medved):
    podatki = dnevi[imena == medved]
    s = np.sum(np.diff(podatki) == 1)
    return s

def zaporedne_meritve():
    a = []
    for x in medvedi():
        a.append(n_zaporednih_meritev(x))
    return dict(zip(medvedi(), a))

def dnevna_razdalja(medved):
    indeksi = np.where(imena == medved)[0]
    razdalje = []
    for i in range(len(indeksi) - 1):
        trenutni = indeksi[i]
        naslednji = indeksi[i + 1]

        if dnevi[naslednji] - dnevi[trenutni] == 1:
            razdalje.append(np.linalg.norm(xy[naslednji] - xy[trenutni]))
    if not razdalje:
        return np.nan
    povprecna_razdalja = np.mean(razdalje)

    return povprecna_razdalja


def dnevne_razdalje():
    a = []
    for x in medvedi():
        a.append(dnevna_razdalja(x))
    return dict(zip(medvedi(), a))


def popotnik():
    a = []
    for x, y in dnevne_razdalje().items():
        a.append(y)
    max_index = np.nanargmax(a)
    return medvedi()[max_index]

def izlet():
    naj_dolzina = 0
    medvd = None
    podatki = None

    for x in medvedi():
        indeks = np.where(imena == x)[0]
        for y in indeks[:-1]:
            trenutna = datumi[y]
            naseldnja = datumi[y + 1]
            if naseldnja[2] - trenutna[2] == 1:
                dolzina = np.linalg.norm(xy[y + 1] - xy[y])
                if dolzina > naj_dolzina:
                    naj_dolzina = dolzina
                    medvd = x
                    podatki = naseldnja

    return medvd, podatki, naj_dolzina






import unittest
from unittest.mock import patch
import warnings
import contextlib
import os

import numpy as np


class TestBase(unittest.TestCase):
    fake_tables = None
    saved_tables = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not os.path.exists("fake-data.csv") \
                or not os.path.exists("Brown bear Slovenia 1993-1999.csv") \
                or os.stat("Brown bear Slovenia 1993-1999.csv").st_size < 100_000:
            print("Nekaj je narobe s podatki. Morda so se pokvarili med testiranjem.")
            print("Pred nadaljevanjem jih ponovno skopiraj.")
            exit()

    def setUp(self):
        super().setUp()
        warnings.simplefilter("ignore", ResourceWarning)

    def preberi_fake_data(self):
        try:
            os.rename("Brown bear Slovenia 1993-1999.csv", "Brown bear Slovenia 1993-1999-copy.csv")
            os.rename("fake-data.csv", "Brown bear Slovenia 1993-1999.csv")

            imena, datumi, dnevi, xy = preberi_podatke()
            np.testing.assert_equal(
                ['berta', 'berta', 'berta', 'ana', 'ana', 'cilka', 'cilka', 'cilka'],
                imena)
            np.testing.assert_equal(
                [[2002, 3, 1],
                 [2002, 3, 15],
                 [2002, 3, 16],
                 [2001, 1, 1],
                 [2001, 1, 3],
                 [2001, 1, 4],
                 [2001, 1, 5],
                 [2001, 1, 6]], datumi)
            np.testing.assert_equal(
                [424, 438, 439, 0, 2, 3, 4, 5],
                dnevi)
            np.testing.assert_almost_equal(
                [[-9.094650340890247, 16.75602643953276],
                 [-11.142102371192092, 20.11171775997127],
                 [-11.601063397540615, 22.183052641201567],
                 [-9.338323398435938, 23.237680298285497],
                 [-10.692978721638882, 23.272541717833736],
                 [-9.047621112214934, 22.66232226047802],
                 [-9.393685296183817, 23.18824417630305],
                 [-14.964763931027381, 31.12211440749531]], xy)
            type(self).fake_tables = (imena, datumi, dnevi, xy)
        finally:
            os.rename("Brown bear Slovenia 1993-1999.csv", "fake-data.csv")
            os.rename("Brown bear Slovenia 1993-1999-copy.csv", "Brown bear Slovenia 1993-1999.csv")

    @contextlib.contextmanager
    def fake_data(self):
        global imena, datumi, dnevi, xy

        if not self.fake_tables:
            try:
                self.preberi_fake_data()
            except:
                self.skipTest("Ta test se ne požene, dokler preberi_datoteko ne deluje pravilno")
                return
        try:
            self.saved_tables = (imena, datumi, dnevi, xy)
            imena, datumi, dnevi, xy = self.fake_tables
            yield
        finally:
            imena, datumi, dnevi, xy = self.saved_tables


class Test06(TestBase):
    def test_01_preberi_podatke(self):
        imena, datumi, dnevi, xy = preberi_podatke()
        self.assertEqual((1898, ), imena.shape)
        self.assertEqual("ancka", imena[0])
        self.assertEqual("jana", imena[432])
        self.assertEqual("jana", imena[450])
        self.assertEqual("maja", imena[1000])
        self.assertEqual("vinko", imena[-1])

        self.assertEqual((1898, 3), datumi.shape)
        np.testing.assert_equal([1994, 4, 23], datumi[0])
        np.testing.assert_equal([1993, 5, 4], datumi[432])
        np.testing.assert_equal([1993, 5, 28], datumi[450])
        np.testing.assert_equal([1997, 5, 10], datumi[1000])
        np.testing.assert_equal([1997, 5, 19], datumi[-1])

        self.assertEqual((1898, ), dnevi.shape)
        np.testing.assert_equal(354, dnevi[0])
        np.testing.assert_equal(0, dnevi[432])
        np.testing.assert_equal(1, dnevi[433])
        np.testing.assert_equal(24, dnevi[450])
        np.testing.assert_equal(1467, dnevi[1000])
        np.testing.assert_equal(1476, dnevi[-1])

        self.assertEqual((1898, 2), xy.shape)
        np.testing.assert_almost_equal([-9.09465034, 16.75602644], xy[0])
        np.testing.assert_almost_equal([-9.09486079, 16.73110564], xy[432])
        np.testing.assert_almost_equal([-4.86981867, 16.77041817], xy[1000])
        np.testing.assert_almost_equal([-20.98983042,  14.34320278], xy[-1])

        self.preberi_fake_data()

    def test_02_globalne_spremenljivke(self):
        im, da, dn, x = preberi_podatke()
        np.testing.assert_equal(imena, im)
        np.testing.assert_equal(datumi, da)
        np.testing.assert_equal(dnevi, dn)
        np.testing.assert_equal(xy, x)

    def test_03_medvedi(self):
        self.assertEqual(
            ['ancka', 'clio', 'dinko', 'dusan', 'ivan', 'jana', 'janko', 'joze', 'jure', 'klemen', 'lucia', 'maja',
             'metka', 'milan', 'mishko', 'nejc', 'polona', 'srecko', 'urosh', 'vanja', 'vera', 'vinko'],
            medvedi())
        with self.fake_data():
            self.assertEqual(["ana", "berta", "cilka"], medvedi())

    def test_04_n_meritev(self):
        self.assertEqual(
            {'ancka': 351, 'clio': 20, 'dinko': 11, 'dusan': 43, 'ivan': 7, 'jana': 111, 'janko': 7, 'joze': 24,
             'jure': 17, 'klemen': 19, 'lucia': 169, 'maja': 247, 'metka': 66, 'milan': 3, 'mishko': 129, 'nejc': 117,
             'polona': 208, 'srecko': 138, 'urosh': 21, 'vanja': 65, 'vera': 92, 'vinko': 33},
            n_meritev())
        with self.fake_data():
            self.assertEqual({'ana': 2, 'berta': 3, 'cilka': 3}, n_meritev())

    def test_05_razpon(self):
        self.assertEqual(
            {'ancka': 1979, 'clio': 64, 'dinko': 69, 'dusan': 66, 'ivan': 12, 'jana': 551, 'janko': 81, 'joze': 45,
             'jure': 79, 'klemen': 185, 'lucia': 354, 'maja': 787, 'metka': 183, 'milan': 9, 'mishko': 578,
             'nejc': 346, 'polona': 520, 'srecko': 218, 'urosh': 48, 'vanja': 113, 'vera': 249, 'vinko': 200},
            razponi())
        with self.fake_data():
            self.assertEqual({'ana': 2, 'berta': 15, 'cilka': 2}, razponi())


class Test07(TestBase):
    def test_01_n_zaporednih_meritev(self):
        self.assertEqual(164, n_zaporednih_meritev("ancka"))
        self.assertEqual(109, n_zaporednih_meritev("maja"))
        self.assertEqual(61, n_zaporednih_meritev("jana"))

        with self.fake_data():
            self.assertEqual(0, n_zaporednih_meritev("ana"))
            self.assertEqual(1, n_zaporednih_meritev("berta"))
            self.assertEqual(2, n_zaporednih_meritev("cilka"))

    def test_02_zaporedne_meritve(self):
        self.assertEqual(
            {'ancka': 164, 'clio': 9, 'dinko': 2, 'dusan': 24, 'ivan': 3, 'jana': 61, 'janko': 1, 'joze': 13,
             'jure': 8, 'klemen': 1, 'lucia': 115, 'maja': 109, 'metka': 21, 'milan': 0, 'mishko': 45, 'nejc': 52,
             'polona': 102, 'srecko': 96, 'urosh': 11, 'vanja': 32, 'vera': 67, 'vinko': 15},
            zaporedne_meritve())

        with self.fake_data():
            self.assertEqual({"ana": 0, "berta": 1, "cilka": 2}, zaporedne_meritve())

    def test_02_dnevna_razdalja(self):
        self.assertAlmostEqual(1.8759694102519862, dnevna_razdalja("jana"))
        self.assertAlmostEqual(2.3820652450335333, dnevna_razdalja("vinko"))
        self.assertTrue(np.isnan(dnevna_razdalja("milan")))

        with self.fake_data():
            self.assertTrue(np.isnan(dnevna_razdalja("ana")))
            self.assertAlmostEqual(np.sqrt(np.sum((xy[1] - xy[2]) ** 2)), dnevna_razdalja("berta"))
            self.assertAlmostEqual((np.sqrt(np.sum((xy[-1] - xy[-2]) ** 2))
                                    + np.sqrt(np.sum((xy[-2] - xy[-3]) ** 2))
                                    ) / 2, dnevna_razdalja("cilka"))

    def test_03_dnevne_razdalje(self):
        exp = {'ancka': 1.6286982832719568, 'clio': 1.739582953462859, 'dinko': 2.2873958565635926,
               'dusan': 1.8872584567158508, 'ivan': 0.5242693676243966, 'jana': 1.4490237605496012,
               'janko': 7.377825605075058, 'joze': 1.0724000204905733, 'jure': 2.048201865060818,
               'klemen': 7.036581726745521, 'lucia': 2.0730121928571172, 'maja': 2.3249171859808855,
               'metka': 2.1200309015488608, 'milan': np.nan, 'mishko': 2.752594639663309, 'nejc': 1.7643782515630508,
               'polona': 1.5906733467685534, 'srecko': 2.3359326919713603, 'urosh': 2.759859825843726,
               'vanja': 1.404713256901303, 'vera': 2.3548863311959125, 'vinko': 1.7586571535972377}
        act = dnevne_razdalje()
        self.assertEqual(set(exp), set(act))
        for k, v in act.items():
            if np.isnan(v):
                self.assertTrue(np.isnan(act[k]), msg=f"Napaka pri medvedu {k}")
            else:
                self.assertAlmostEqual(v, act[k], msg=f"Napaka pri medvedu {k}")

        with self.fake_data():
            act = dnevne_razdalje()
            self.assertEqual({"ana", "berta", "cilka"}, set(act))
            self.assertTrue(np.isnan(act["ana"]))
            self.assertAlmostEqual(np.sqrt(np.sum((xy[1] - xy[2]) ** 2)), act["berta"])
            self.assertAlmostEqual(5.162030372531544, act["cilka"])

    def test_04_popotnik(self):
        self.assertEqual("janko", popotnik())
        with self.fake_data():
            self.assertEqual("cilka", popotnik())

    def test_05_izlet(self):
        ime, datum, razdalja = izlet()
        self.assertEqual("jana", ime)
        np.testing.assert_equal([1994, 8, 14], datum)
        self.assertEqual(16.971524437756226, razdalja)

        with self.fake_data():
            ime, datum, razdalja = izlet()
            self.assertEqual("cilka", ime)
            np.testing.assert_equal([2001, 1, 6], datum)
            self.assertEqual(9.694494004382546, razdalja)


class Test08(TestBase):
    def test_01_mesecna_razdalja(self):
        np.testing.assert_almost_equal(
            [0.1011831, 0., 2.9312846, 1.9335919, 2.2192923, 2.7600592,
             2.8303944, 2.6086782, 2.0960126, 2.116222, 2.2377832, 0.8756167],
            mesecna_razdalja())
        with self.fake_data():
            np.testing.assert_almost_equal(
                [5.1620304, np.nan, 2.1215733] + [np.nan] * 9, mesecna_razdalja())

    def test_02_leni_meseci(self):
        self.assertEqual(12, leni_meseci(mesecna_razdalja()))
        self.assertEqual(4, leni_meseci([5, 3, 5, 1, 2, 0, 3, 4, 1, 6, 1, 5]))

    def test_03_lenoba(self):
        self.assertAlmostEqual(0.17204663041569274, lenoba(mesecna_razdalja()))
        self.assertAlmostEqual(((1 + 2 + 0) / 3) / ((5 + 3 + 5 + 1 + 2 + 0 + 3 + 4 + 1 + 6 + 1 + 5) / 12),
                               lenoba([5, 3, 5, 1, 2, 0, 3, 4, 1, 6, 1, 5]))


class Test09(TestBase):
    def test_01_povprecna_razdalja(self):
        self.assertAlmostEqual(14.272051319824765, povprecna_razdalja("jana", "maja"))
        self.assertAlmostEqual(14.272051319824763, povprecna_razdalja("maja", "jana"))
        self.assertAlmostEqual(4.044968190696584, povprecna_razdalja("vera", "lucia"))
        self.assertAlmostEqual(2.8779738438620894, povprecna_razdalja("vanja", "dusan"))

        with self.fake_data():
            self.assertAlmostEqual(3.9853797524769377, povprecna_razdalja("ana", "berta"))
            self.assertAlmostEqual(3.7330897346434058, povprecna_razdalja("ana", "cilka"))
            self.assertAlmostEqual(6.7703739925187145, povprecna_razdalja("cilka", "berta"))

    def test_02_povprecne_razdalje(self):
        with self.fake_data():
            exp = {('ana', 'berta'): 3.9853797524769377,
                   ('ana', 'cilka'): 3.7330897346434058,
                   ('berta', 'cilka'): 6.7703739925187145}
            act = povprecne_razdalje()
            self.assertEqual(set(exp), set(act))
            for k, v in exp.items():
                self.assertAlmostEqual(v, act[k])

    def test_03_prijatelji(self):
        s = []
        with patch("builtins.print", new=s.append):
            prijatelji()
            self.assertEqual("""               dusan :  2.88 : vanja
               vanja :  2.96 : vera
                maja :  3.22 : vanja
               dusan :  3.39 : vera
               dusan :  3.63 : maja
               lucia :  3.73 : vanja
                maja :  3.76 : vera
                clio :  3.89 : lucia
                clio :  3.94 : vanja
               lucia :  4.04 : vera""", "\n".join(s))

            s.clear()
            with self.fake_data():
                prijatelji()
                self.assertEqual("""                 ana :  3.73 : cilka
                 ana :  3.99 : berta
               berta :  6.77 : cilka""", "\n".join(s))

    def test_04_bffl(self):
        self.assertEqual({"vanja", "dusan"}, set(bffl()))
        with self.fake_data():
            self.assertEqual({"ana", "cilka"}, set(bffl()))


class Test10(unittest.TestCase):
    def test_01_druzabnost(self):
        #         Vrhnika,               Logatec                 Postojna                Cerknica
        kraji = [[45.962375, 14.293736], [45.916703, 14.229728], [45.775864, 14.213661], [45.796389, 14.358056]]
        self.assertEqual(68, druzabnost("polona", kraji, 5))
        self.assertEqual(90, druzabnost("ancka", kraji, 5))
        self.assertEqual(33, druzabnost("vinko", kraji, 8))

        self.assertEqual(68, druzabnost("polona", kraji[1:], 5))
        self.assertEqual(63, druzabnost("ancka", kraji[1:], 5))
        self.assertEqual(33, druzabnost("vinko", kraji[1:], 8))

        self.assertEqual(68, druzabnost("polona", kraji[2:], 5))
        self.assertEqual(0, druzabnost("ancka", kraji[2:], 3))
        self.assertEqual(31, druzabnost("vinko", kraji[2:], 8))

        self.assertEqual(68, druzabnost("polona", kraji[2:], 5))
        self.assertEqual(35, druzabnost("polona", kraji[2:], 4))
        self.assertEqual(2, druzabnost("polona", kraji[2:], 3))
        self.assertEqual(0, druzabnost("polona", kraji[2:], 2))

    def test_02_center(self):
        #         Vrhnika,               Logatec                 Postojna                Cerknica
        kraji = [[45.962375, 14.293736], [45.916703, 14.229728], [45.775864, 14.213661], [45.796389, 14.358056]]
        np.testing.assert_almost_equal([0.3675214, 0.2849003, 0, 0.3475783], tezisce_delovanja("ancka", kraji))
        np.testing.assert_almost_equal([0.5870445, 0.3157895, 0, 0.097166 ], tezisce_delovanja("maja", kraji))
        np.testing.assert_almost_equal([0, 0.03418803, 0.00854701, 0.95726496], tezisce_delovanja("nejc", kraji))
        np.testing.assert_almost_equal([0.0630631, 0.8378378, 0.       , 0.0990991], tezisce_delovanja("jana", kraji))
        np.testing.assert_almost_equal([0, 0, 0, 1], tezisce_delovanja("polona", kraji))
        np.testing.assert_almost_equal([0.0724638, 0.5942029, 0.2753623, 0.057971 ], tezisce_delovanja("srecko", kraji))

    def test_03_obiskovalci(self):
        #         Vrhnika,               Logatec                 Postojna                Cerknica
        kraji = [[45.962375, 14.293736], [45.916703, 14.229728], [45.775864, 14.213661], [45.796389, 14.358056]]
        self.assertEqual(
            [{'maja', 'ancka', 'dusan', 'vera'},
             {'jana', 'urosh', 'vanja', 'clio', 'metka', 'jure', 'srecko', 'lucia'},
             {'janko'},
             {'dinko', 'ivan', 'joze', 'klemen', 'milan', 'mishko', 'nejc', 'polona', 'vinko'}], obiskovalci(kraji))
        self.assertEqual(
            [{'ivan', 'dusan', 'mishko', 'urosh', 'ancka', 'maja'},
             {'metka', 'vanja', 'lucia', 'clio', 'srecko', 'vera', 'jure', 'jana', 'joze'},
             {'nejc', 'polona', 'janko', 'milan', 'dinko', 'klemen', 'vinko'}], obiskovalci(kraji[:-1]))


if __name__ == "__main__":
    unittest.main()

import numpy as np

def preberi_podatke():
    s = np.genfromtxt("polona-in-ancka.csv", delimiter=',', dtype=str)
    datumi = s[:, 0]
    polona = s[:, 1:3].astype(float)
    ancka = s[:, 3:5].astype(float)
    return datumi, polona, ancka

def meritev(xy):
    return np.count_nonzero(np.isnan(xy[:, 0]) == False)

def vzhod_zahod(xy):
    return np.array([np.nanmax(xy[:, 1]), np.nanmin(xy[:, 1])])

def najvzhodnejša(xy):
    return xy[np.nanargmax(xy[:, 1]), :]

def minrazdalja(xy, tocka):
    return np.nanmin(np.sqrt(np.sum((xy - tocka) ** 2, axis=1)))

def najblizja(xy, tocka):
    return xy[np.nanargmin(np.sqrt(np.sum((xy - tocka) ** 2, axis=1))), :]

def minmedrazdalja(xy1, xy2):
    return np.nanmin(np.sqrt(np.sum((xy1 - xy2) ** 2, axis=1)))

def dan_srecanja(datumi, xy1, xy2):
    return datumi[np.nanargmin(np.sqrt(np.sum((xy1 - xy2) ** 2, axis=1)))]



import unittest

class Test(unittest.TestCase):
    def test_01_preberi(self):
        datumi, polona, ancka = preberi_podatke()
        self.assertEqual((2604, ), datumi.shape)
        self.assertEqual((2604, 2), polona.shape)
        self.assertEqual((2604, 2), ancka.shape)

        self.assertEqual(float, polona.dtype)
        self.assertEqual(float, ancka.dtype)

        self.assertAlmostEqual(12530.0036645154, np.nansum(polona))
        self.assertAlmostEqual(21081.948339962, np.nansum(ancka))
        self.assertEqual('1993-01-01', datumi[0])
        self.assertEqual('1999-12-31', datumi[-1])

    def test_02_meritev(self):
        datumi, polona, ancka = preberi_podatke()

        self.assertEqual(350, meritev(ancka))
        self.assertEqual(208, meritev(polona))

    def test_03_vzhod_zahod(self):
        datumi, polona, ancka = preberi_podatke()

        np.testing.assert_almost_equal(vzhod_zahod(ancka), (14.5140544398, 14.2663288151),)
        np.testing.assert_almost_equal(vzhod_zahod(polona), (14.4868167466, 14.3361857993))

    def test_04_najvzhodnejša(self):
        datumi, polona, ancka = preberi_podatke()

        np.testing.assert_almost_equal(najvzhodnejša(ancka), (45.83632009, 14.5140544398))
        np.testing.assert_almost_equal(najvzhodnejša(polona), (45.8236039136, 14.4868167466))

    def test_05_minrazdalja(self):
        datumi, polona, ancka = preberi_podatke()
        preseren = np.array([46.0513539,14.502127])
        np.testing.assert_almost_equal(minrazdalja(polona, preseren), 0.1877726)
        np.testing.assert_almost_equal(minrazdalja(ancka, preseren), 0.1494795)

    def test_06_najblizja(self):
        datumi, polona, ancka = preberi_podatke()

        preseren = np.array([46.0513539,14.502127])
        np.testing.assert_almost_equal(najblizja(polona, preseren), [45.8675868, 14.4635502])
        np.testing.assert_almost_equal(najblizja(ancka, preseren), [45.9034319, 14.4806042])

        pgd_borovnica = np.array([45.9178048,14.3596468])
        np.testing.assert_almost_equal(najblizja(polona, pgd_borovnica), [45.8602007, 14.3415998])
        np.testing.assert_almost_equal(najblizja(ancka, pgd_borovnica), [45.910938 , 14.3635576])

    def test_07_minmedrazdalja(self):
        datumi, polona, ancka = preberi_podatke()
        np.testing.assert_almost_equal(minmedrazdalja(polona, ancka), 0.07254133219635045)

    def test_08_dan_srecanja(self):
        self.assertEqual("1998-06-23", dan_srecanja(*preberi_podatke()))


if __name__ == "__main__":
    unittest.main()

from urllib.request import urlopen
import string
from bs4 import BeautifulSoup
import re
import os

def prenesi_podatke():
    for crka in string.ascii_lowercase:
        pot = f'authors/{crka}.html'
        if not os.path.exists(pot):
            url = f'https://ucilnica.fri.uni-lj.si/pluginfile.php/217381/mod_folder/content/0/{crka}.html'
            html = urlopen(url).read().decode('utf-8')
            with open(pot, 'w', encoding='utf-8') as s:
                s.write(html)

prenesi_podatke()
def avtorji(priimek):
    s = []
    crka = priimek[0].lower()
    html = open(f'authors/{crka}.html', encoding='UTF-8').read()
    soup = BeautifulSoup(html, features="html.parser")
    for div in soup.find_all("div", class_="pgdbbyauthor"):
        a = div.find_all("h2")
    for el in a:
        if el.string != None:
            print(el.string)
            s.append(el.string)
    for link in soup.find_all("a", id=True):
        if link.parent.name == 'h2':
            s.append(link.nextSibling)
    osebe = [avtor for avtor in s if avtor.startswith(priimek + ',') or avtor == priimek]
    return sorted(osebe)



import unittest
import warnings
import os
import json


class NoWarnings(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


class Test06(NoWarnings):
    def test_01_poberi_podatke(self):
        prenesi_podatke()
        self.assertEqual("""<!DOCTYPE html>
<html class="client-nojs" lang="en" dir="ltr">
<head>
 <meta charset="UTF-8"/>

<tit""", open("../../../Desktop/programiranje1/Gutenberg/authors/r.html", encoding="utf-8").read()[:100])

        os.remove("../../../Desktop/programiranje1/Gutenberg/authors/r.html")
        try:
            os.rename("../../../Desktop/programiranje1/Gutenberg/authors/c.html", "authors/c.html.bak")
            open("../../../Desktop/programiranje1/Gutenberg/authors/c.html", "w", encoding="utf-8").write("test")
            prenesi_podatke()
            self.assertEqual("""<!DOCTYPE html>
<html class="client-nojs" lang="en" dir="ltr">
<head>
 <meta charset="UTF-8"/>

<tit""", open("../../../Desktop/programiranje1/Gutenberg/authors/r.html", encoding="utf-8").read()[:100])

            if open("../../../Desktop/programiranje1/Gutenberg/authors/c.html", encoding="utf-8").read() != "test":
                self.fail("preberi_podatke naj ne nalaga ponovno datotek, ki že obstajajo!")
        finally:
            os.remove("../../../Desktop/programiranje1/Gutenberg/authors/c.html")
            os.rename("authors/c.html.bak", "../../../Desktop/programiranje1/Gutenberg/authors/c.html")

    def test_02_avtorji(self):
        self.assertEqual(['Fairfax, Cecil', 'Fairfax, Edward, -1635'], avtorji("Fairfax"))
        self.assertEqual(["Tal, Fulano de"], avtorji("Tal"))
        self.assertEqual(['Macaulay, Fannie Caldwell',
                          'Macaulay, G. C. (George Campbell), 1852-1915',
                          'Macaulay, James, 1817-1902',
                          'Macaulay, Rose, 1881-1958',
                          'Macaulay, Thomas Babington',
                          'Macaulay, Thomas Babington Macaulay, Baron, 1800-1859',
                          'Macaulay, W. Hastings',
                          'Macaulay, Zachary, 1768-1838'], avtorji("Macaulay"))
        self.assertEqual(['Babbage, Charles, 1791-1871'], avtorji("Babbage"))


class Test07(NoWarnings):
    def test_01_razberi_avtorja(self):
        self.assertEqual(("Macaulay", ["James"], 1817, 1902), razberi_avtorja('Macaulay, James, 1817-1902'))
        self.assertEqual(("Macaulay", ["James", "Peter"], 1817, 1902), razberi_avtorja('Macaulay, James, Peter, 1817-1902'))
        self.assertEqual(("Macaulay", ["James", "Peter"], 1817, 1902), razberi_avtorja('Macaulay, James, Peter, 1817?-1902'))
        self.assertEqual(("Macaulay", ["James", "Peter"], 1817, 1902), razberi_avtorja('Macaulay, James, Peter, 1817-1902?'))
        self.assertEqual(("Macaulay", ["James", "Peter"], None, 1902), razberi_avtorja('Macaulay, James, Peter, -1902'))
        self.assertEqual(("Cicero", ["Marcus Tullius"], -106, -43), razberi_avtorja("Cicero, Marcus Tullius, 106 BC-43 BC"))
        self.assertEqual(("Bach", ["P. D. Q."], 33, -12), razberi_avtorja("Bach, P. D. Q., 33-12? BC"))
        self.assertEqual(("Macaulay", ["James", "Peter"], 1817, None), razberi_avtorja('Macaulay, James, Peter, 1817-'))
        self.assertEqual(("Macaulay", ["James", "Peter", "Joe-Ann"], 1817, None), razberi_avtorja('Macaulay, James, Peter, Joe-Ann, 1817-'))
        self.assertEqual(("Macaulay", ["James", "Peter", "Joe-Ann"], 1817, 1902), razberi_avtorja('Macaulay, James, Peter, Joe-Ann, 1817-1902'))
        self.assertIsNone(razberi_avtorja('Macaulay, James, Peter'))
        self.assertIsNone(razberi_avtorja('Macaulay, James, Peter, Joe-Ann'))
        self.assertIsNone(razberi_avtorja('King, George, 3'))
        self.assertIsNone(razberi_avtorja('King, George, 1941'))
        self.assertIsNone(razberi_avtorja('King, George, 1941, 1945'))

    def test_02_zberi_podatke(self):
        avtorji = zberi_podatke("g")
        self.assertTrue(all(a[0] == "G" for a in avtorji))
        self.assertEqual(749, len(avtorji))
        self.assertEqual([('Gallagher', ['Sears'], 1869, 1955)], avtorji["Gallagher"])
        self.assertEqual([('Gannett', ['Ezra S. (Ezra Stiles)'], 1801, 1871),
                          ('Gannett', ['Frank E. (Frank Ernest)'], 1876, 1957),
                          ('Gannett', ['Henry'], 1846, 1914)], avtorji["Gannett"])

        avtorji = zberi_podatke("gtm")
        self.assertTrue(all(a[0] in "GTM" for a in avtorji))
        self.assertEqual(2428, len(avtorji))

        self.assertEqual([('Gallagher', ['Sears'], 1869, 1955)], avtorji["Gallagher"])
        self.assertEqual([('Talbot', ['Ethel'], 1880, 1944),
                          ('Talbot', ['Eugène'], 1814, 1894),
                          ('Talbot', ['Eugene S. (Eugene Solomon)'], 1847, 1924),
                          ('Talbot', ['Frederick Arthur Ambrose'], 1880, 1924),
                          ('Talbot', ['Henry Paul'], 1864, 1927),
                          ('Talbot', ['N. S. (Neville Stuart)'], 1879, 1943),
                          ('Talbot', ['William Henry Fox'], 1800, 1877),
                          ('Talbot', ['William', 'Sir'], None, 1691)], avtorji["Talbot"])

        if not os.path.exists("../../../Desktop/programiranje1/Gutenberg/authors"):
            avtorji = zberi_podatke("")
            self.assertEqual(13990, len(avtorji))

    def test_03_authors_json(self):
        avtorji = json.load(open("authors.json", encoding="utf-8"))
        self.assertEqual(13990, len(avtorji))
        self.assertEqual([['Gannett', ['Ezra S. (Ezra Stiles)'], 1801, 1871],
                          ['Gannett', ['Frank E. (Frank Ernest)'], 1876, 1957],
                          ['Gannett', ['Henry'], 1846, 1914]],
                         avtorji["Gannett"])


class Test08(NoWarnings):
    def test_01_v_obdobju(self):
        self.assertTrue(v_obdobju(1780, 1840, 1800, 1900))  # rojen pred, umrl v
        self.assertTrue(v_obdobju(1780, 1800, 1800, 1900))  # rojen pred, umrl v
        self.assertTrue(v_obdobju(1880, 1910, 1800, 1900))  # rojen v, umrl po
        self.assertTrue(v_obdobju(1900, 1910, 1800, 1900))  # rojen v, umrl po
        self.assertTrue(v_obdobju(1500, 1550, 1480, 1560))  # živel znotraj obdobja
        self.assertTrue(v_obdobju(1500, 1550, 1510, 1520))  # obdobje znotraj življenja
        self.assertTrue(v_obdobju(1500, 1550, 1510, 1510))  # obdobje znotraj življenja

        self.assertTrue(v_obdobju(1500, None, 1410, 1510))  # rojen znotraj obdobja
        self.assertTrue(v_obdobju(None, 1500, 1410, 1510))  # umrl znotraj obdobja

        self.assertFalse(v_obdobju(1780, 1840, 1841, 1900))  # rojen po, umrl pred
        self.assertFalse(v_obdobju(1780, 1840, 1641, 1779))  # rojen po, umrl pred
        self.assertFalse(v_obdobju(1780, None, 1641, 1779))  # rojen po, umrl pred
        self.assertFalse(v_obdobju(None, 1780, 1641, 1779))  # rojen po, umrl pred
        self.assertFalse(v_obdobju(1640, None, 1641, 1779))  # rojen po, umrl pred
        self.assertFalse(v_obdobju(None, 1580, 1641, 1779))  # rojen po, umrl pred

        self.assertFalse(v_obdobju(0, 10**22, 2.3 * 10**22, 2 * 10**40))

    def test_02_avtorji_v_obdobju(self):
        self.assertEqual([['Amir Khusraw Dihlavi', [], 1253, 1325],
                          ['Bury', ['Richard de'], 1287, 1345],
                          ['Dante Alighieri', [], 1265, 1321],
                          ['Gao', ['Ming'], 1306, 1359],
                          ['Joinville', ['Jean', 'sire de'], 1224, 1317],
                          ['Juan Manuel', ['Infante of Castile'], 1282, 1347],
                          ['Liu', ['Ji'], 1311, 1375],
                          ['Llull', ['Ramon'], 1232, 1316],
                          ['Ma', ['Zhiyuan'], 1250, 1324],
                          ['Petrarca', ['Francesco'], 1304, 1374],
                          ['Polo', ['Marco'], 1254, 1324],
                          ['Rolle', ['Richard', 'of Hampole'], 1290, 1349],
                          ['Ruiz', ['Juan'], 1283, 1350],
                          ['Ruusbroec', ['Jan van'], 1293, 1381],
                          ['Shi', ["Nai'an"], 1290, 1365],
                          ['Wang', ['Mian'], 1287, 1359],
                          ['Wang', ['Shifu'], 1260, 1316],
                          ['Zhu', ['Mingshi'], 1260, 1340]],
                          avtorji_v_obdobju(1310, 1311))

    def test_03_razpon(self):
        self.assertEqual((-1810, 2023), razpon())

    def test_04_pokritost(self):
        self.assertEqual([78, 78, 80, 82, 83, 85, 86, 86, 86, 88, 94, 96, 99, 99, 100, 105, 107, 109, 109, 111, 112],
                         pokritost(1500, 1520))

        self.assertEqual([1913, 1945, 1999, 2058, 2114, 2195, 2270, 2331, 2388, 2491, 2591, 2677, 2790, 2888, 2966,
                          3051, 3139, 3235, 3348, 3464, 3582, 3694, 3805, 3914, 4023, 4127, 4228, 4312, 4432, 4538,
                          4676, 4811, 4940, 5057, 5163, 5293, 5456, 5587, 5755, 5899, 6098, 6257, 6458, 6624, 6790,
                          6957, 7135, 7320, 7523],
                         pokritost(1800, 1848))

        self.assertEqual([0, 0, 0, 0], pokritost(-5003, -5000))


class Test09(NoWarnings):
    def test_01_razberi_delo(self):
        self.assertEqual(("Lightships and Lighthouses", "English"), razberi_delo("Lightships and Lighthouses (English) (as Author)"))
        self.assertEqual(('Histoire de la Litterature Anglaise (Volume 1 de 5)', 'French'), razberi_delo("Histoire de la Litterature Anglaise (Volume 1 de 5) (French) (as Author)"))
        self.assertIsNone(razberi_delo("My Reminiscences (English) (as Translator)"))

    def test_02_dela(self):
        if os.path.exists("works.json"):
            return

        vsa_dela = dela()
        self.assertIn(('Rambles Beyond Railways; or, Notes in Cornwall taken A-foot', 'English', 'Collins', ['Wilkie'], 1824, 1889), vsa_dela)
        self.assertIn(('Points of friction', 'English', 'Repplier', ['Agnes'], 1855, 1950), vsa_dela)
        self.assertIn(('Marianne-rouva: Romaani', 'Finnish', 'Benedictsson', ['Victoria'], 1850, 1888), vsa_dela)

    def test_03_dela_json(self):
        vsa_dela = json.load(open("works.json", encoding="utf-8"))
        self.assertIn(['Rambles Beyond Railways; or, Notes in Cornwall taken A-foot', 'English', 'Collins', ['Wilkie'], 1824, 1889], vsa_dela)
        self.assertIn(['Points of friction', 'English', 'Repplier', ['Agnes'], 1855, 1950], vsa_dela)
        self.assertIn(['Marianne-rouva: Romaani', 'Finnish', 'Benedictsson', ['Victoria'], 1850, 1888], vsa_dela)

    def test_04_dela_po_jezikih(self):
        self.assertEqual({ 'Afrikaans': 13, 'Bodo': 2, 'Bulgarian': 5, 'Catalan': 29, 'Cebuano': 2, 'Chinese': 247,
                           'Czech': 13, 'Danish': 69, 'Dutch': 826, 'English': 41374, 'Esperanto': 94, 'Estonian': 1,
                           'Farsi': 1, 'Finnish': 2629, 'French': 3010, 'Frisian': 6, 'Friulian': 6, 'Galician': 3,
                           'German': 1918, 'Greek': 201, 'Hebrew': 3, 'Hungarian': 489, 'Icelandic': 6,
                           'Interlingua': 1, 'Irish': 1, 'Italian': 851, 'Japanese': 21, 'Kashubian': 1, 'Khasi': 1,
                           'Latin': 102, 'Mayan Languages': 1, 'Middle English': 2, 'Nahuatl': 1,
                           'Napoletano-Calabrese': 1, 'Navajo': 1, 'North American Indian': 2, 'Norwegian': 20,
                           'Occitan': 1, 'Old English': 1, 'Polish': 28, 'Portuguese': 477, 'Romanian': 4,
                           'Russian': 4, 'Serbian': 4, 'Slovenian': 1, 'Spanish': 712, 'Swedish': 189, 'Tagalog': 37,
                           'Telugu': 6, 'Welsh': 12}, dela_po_jezikih())


class Test10(NoWarnings):
    def test_01_preveri_delo(self):
        delo = ["The Bears of Blue River", "English", "Major", ["Charles", "Peter"], 1856, 1913]
        self.assertTrue(preveri_delo(delo, naslov="Bears"))
        self.assertTrue(preveri_delo(delo, naslov="Bears", jezik="English"))
        self.assertTrue(preveri_delo(delo, naslov="Bears", jezik="English", avtor="Major"))
        self.assertTrue(preveri_delo(delo, naslov="ears", jezik="English", avtor="Major"))
        self.assertTrue(preveri_delo(delo, naslov="Bears", jezik="English", avtor="Peter Major"))
        self.assertTrue(preveri_delo(delo, naslov="Bears", jezik="English", avtor="Peter Major"))
        self.assertTrue(preveri_delo(delo, naslov="Bears", jezik="English", avtor="er Maj"))
        self.assertTrue(preveri_delo(delo, jezik="English", avtor="er Maj", leto=1890))
        self.assertTrue(preveri_delo(delo, avtor="er Maj", leto=1890))
        self.assertTrue(preveri_delo(delo, leto=1890))
        self.assertTrue(preveri_delo(delo))

        self.assertFalse(preveri_delo(delo, naslov="Red"))
        self.assertFalse(preveri_delo(delo, naslov="Bears", jezik="Finnish"))
        self.assertFalse(preveri_delo(delo, naslov="Bears", jezik="English", avtor="Minor"))
        self.assertFalse(preveri_delo(delo, naslov="Bears", jezik="English", avtor="Minor Major"))
        self.assertFalse(preveri_delo(delo, jezik="English", avtor="er Maj", leto=1850))

        self.assertFalse(preveri_delo(["The Bears of Blue River", "English", "Major", ["Charles", "Peter"], None, 1913], leto=1920))
        self.assertFalse(preveri_delo(["The Bears of Blue River", "English", "Major", ["Charles", "Peter"], None, 1913], leto=1913))
        self.assertFalse(preveri_delo(["The Bears of Blue River", "English", "Major", ["Charles", "Peter"], None, 1913], leto=1900))
        self.assertFalse(preveri_delo(["The Bears of Blue River", "English", "Major", ["Charles", "Peter"], 1913, None], leto=1920))
        self.assertFalse(preveri_delo(["The Bears of Blue River", "English", "Major", ["Charles", "Peter"], 1913, None], leto=1913))
        self.assertFalse(preveri_delo(["The Bears of Blue River", "English", "Major", ["Charles", "Peter"], 1913, None], leto=1900))

    def test_02_poisci(self):
        babbage = [['On the Economy of Machinery and Manufactures',  'English',  'Babbage',  ['Charles'],  1791,  1871],
                   ['Passages from the Life of a Philosopher',  'English',  'Babbage',  ['Charles'],  1791,  1871],
                   ['Reflections on the Decline of Science in England, and on Some of Its Causes', 'English', 'Babbage', ['Charles'], 1791, 1871],
                   ['The calculating engine', 'English', 'Babbage', ['Charles'], 1791, 1871]]
        self.assertEqual(babbage, sorted(poisci(avtor="Babbage")))
        self.assertEqual(babbage, sorted(poisci(avtor="Babbage", leto=1800)))
        self.assertEqual(babbage, sorted(poisci(avtor="Babbage", leto=1800, jezik="English")))


if __name__ == "__main__":
    unittest.main()

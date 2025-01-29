from collections import defaultdict
import os
import math

def sopomenke_besede(s):
    vsi = set()
    predmeti = s.split(' ')
    for x in predmeti:
        if x[0] == '*':
            osnovni = x.strip('*').strip()
            vsi.add(osnovni)
        else:
            y = x.strip()
            vsi.add(y)
    terka = (osnovni, vsi)
    return terka

def preberi_sopomenke():
    seznam = defaultdict(str)
    for vrstica in open('podatki/sopomenke.txt', encoding='UTF-8'):
        vsi = sopomenke_besede(vrstica)
        for predmeti in vsi[1]:
            seznam[predmeti] = vsi[0]

    return seznam
sopomenke = preberi_sopomenke()

def prevod_besede(beseda):
    if beseda in sopomenke.keys():
        s = sopomenke[beseda]
    else:
        s = None
    return s

def poenostavi_besedilo(s):
    d = ""
    uredu = set("AaBbCcČčDdEeFfGgHhIiJjKkLlMmNnOoPpRrSsŠšTtUuVvZzŽž \n")
    for crke in s:
        if crke in uredu:
            d += f"{crke.lower()}"

    return d

def izlusci_avtorja(ime_dat):
    oseba = []
    for vrstica in open(ime_dat, encoding='UTF-8'):
        s = vrstica.split()
        for x in s:
            oseba.append(x)
    return oseba[-1]

def izlusci_darila(ime_dat):
    darila = set()
    for vrstica in open(ime_dat, encoding='UTF-8'):
        a = poenostavi_besedilo(vrstica)
        beseda = a.split()
        for x in beseda:
            if x in sopomenke.keys():
                darila.add(sopomenke[x])

    return darila

def darila_po_otrocih():
    d = {}
    for x in os.listdir('podatki/pisma'):
        s = f'podatki/pisma/{x}'
        d[izlusci_avtorja(s)] = izlusci_darila(s)
    return d

def zbirnik_daril():
    d = defaultdict(int)
    for x, darila in darila_po_otrocih().items():
        for a in darila:
            d[a] += 1
    return d

def preberi_cenik(ime_ponudnika):
    d = {}
    for vrstica in open(f'podatki/dobavitelji/{ime_ponudnika}.txt', encoding='UTF-8'):
        predmet, cena = vrstica.strip().split(': ')
        d[predmet] = float(cena)
    return d

def ceniki():
    d = {}
    for x in os.listdir('podatki/dobavitelji'):
        ime, koncnica  = os.path.splitext(x)
        d[ime] = preberi_cenik(ime)
    return d

def najcenejsi_ponudnik(ceniki, darilo):
    najmn = math.inf
    oseba = None
    for prodajalec, cenik in ceniki.items():
        if darilo in cenik.keys():
            cena = cenik[darilo]
            if cena < najmn or (cena == najmn and prodajalec > oseba):
                najmn = cena
                oseba = prodajalec
    return (oseba, najmn)

def ponudniki_in_cene(ceniki, darila):
    d = defaultdict()
    for a in darila:
        if a not in d:
            d[a] = najcenejsi_ponudnik(ceniki, a)
    return d

def vrednost_daril(otrok):
    skupna = 0
    darila = izlusci_darila(f"podatki/pisma/{otrok}.txt")
    ponudbe = ponudniki_in_cene(ceniki(), darila)
    for x, y in ponudbe.items():
        skupna += int(y[1])
    return skupna

def preberi_tockovalnik():
    i = []
    t = []
    tockovalnik = defaultdict() #kljuci so otroci, vrednosti skupno stevilo
    for vrstica in open('podatki/tockovalnik.txt', encoding='UTF-8'):
        vrstica = vrstica.strip().split(':')
        i.append(vrstica[0])
        t.append(vrstica[1].strip().split(' '))
        for ime, tocke in zip(i, t):
            tockovalnik[ime] = 0
            for x in tocke:
                tockovalnik[ime] += int(x)
    return tockovalnik

def dolocitev_daril(proracun, darila, ponudniki_cene):
    d = sorted(darila, key=lambda x: (ponudniki_cene[x][1], x), reverse=True)
    usa = set()
    for x in d:
        cena = ponudniki_cene[x][1]
        if cena <= proracun:
            usa.add(x)
            proracun -= cena

    return usa

def darila_za_otroka(otrok, tockovalnik, otroci_darila, ponudniki_cene):
    return dolocitev_daril(tockovalnik[otrok] / 10, otroci_darila[otrok], ponudniki_cene)








import unittest
import warnings


class Test(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


class Test06(Test):
    def test_01_sopomenke(self):
        self.assertEqual(('žoga', {'žoga', 'žogi', 'žogo', 'žoge'}), sopomenke_besede("*žoga žogo žoge žogi"))
        self.assertEqual(('sanke', {'sani', 'sank', 'sanke'}), sopomenke_besede("sani *sanke sank"))
        self.assertEqual(('pero', {'pero'}), sopomenke_besede("*pero"))

    def test_02_preberi_sopomenke(self):
        sop = preberi_sopomenke()
        exp = {'avtomobilček': 'avtomobilček',
               'avtomobilčka': 'avtomobilček',
               'avtomobilčke': 'avtomobilček',
               'barvic': 'barvice',
               'barvice': 'barvice',
               'blazin': 'blazina',
               'blazina': 'blazina',
               'blazine': 'blazina',
               'blazino': 'blazina',
               'bombon': 'bomboni',
               'bombone': 'bomboni',
               'bomboni': 'bomboni',
               'bombonov': 'bomboni',
               'bombonček': 'bomboni',
               'bombončke': 'bomboni',
               'bombončki': 'bomboni',
               'bonbon': 'bomboni',
               'bonbone': 'bomboni',
               'bonboni': 'bomboni',
               'bonbonček': 'bomboni',
               'bonbončke': 'bomboni',
               'bonbončki': 'bomboni',
               'flomastre': 'barvice',
               'flomastri': 'barvice',
               'flomastrov': 'barvice',
               'glina': 'glina',
               'glino': 'glina',
               'knjig': 'knjiga',
               'knjiga': 'knjiga',
               'knjige': 'knjiga',
               'knjigi': 'knjiga',
               'knjigo': 'knjiga',
               'kock': 'kocke',
               'kocke': 'kocke',
               'kolo': 'kolo',
               'lego': 'kocke',
               'medvedek': 'medvedek',
               'medvedka': 'medvedek',
               'medvedke': 'medvedek',
               'medvedkov': 'medvedek',
               'peres': 'pero',
               'pero': 'pero',
               'pisala': 'pisalo',
               'pisalo': 'pisalo',
               'piškot': 'piškoti',
               'piškote': 'piškoti',
               'piškoti': 'piškoti',
               'piškotov': 'piškoti',
               'poušter': 'blazina',
               'pouštre': 'blazina',
               'pouštrov': 'blazina',
               'sani': 'sanke',
               'sank': 'sanke',
               'sanke': 'sanke',
               'sladkarij': 'bomboni',
               'sladkarije': 'bomboni',
               'slikanic': 'knjiga',
               'slikanica': 'knjiga',
               'slikanice': 'knjiga',
               'slikanico': 'knjiga',
               'vlak': 'vlak',
               'vlakec': 'vlak',
               'zemljevid': 'zemljevid',
               'zvezek': 'zvezek',
               'zvezke': 'zvezek',
               'zvezki': 'zvezek',
               'zvezkov': 'zvezek',
               'čelada': 'čelada',
               'čelade': 'čelada',
               'čelado': 'čelada',
               'čokolada': 'čokolada',
               'čokolade': 'čokolada',
               'čokoladk': 'čokolada',
               'čokoladko': 'čokolada',
               'čokolado': 'čokolada',
               'čokolatko': 'čokolada',
               'žirafa': 'žirafa',
               'žirafica': 'žirafa',
               'žirafico': 'žirafa',
               'žirafo': 'žirafa',
               'žoga': 'žoga',
               'žoge': 'žoga',
               'žogi': 'žoga',
               'žogic': 'žoga',
               'žogica': 'žoga',
               'žogico': 'žoga',
               'žogo': 'žoga'}
        self.assertEqual(exp, sop)
        if globals().get("sopomenke") != exp:
            self.fail("""
Preden nadaljuješ, dodaj pod funkcijo slovar_sopomenke vrstico
'sopomenke = preberi_sopomenke() (na začetek vrstice).
"To spremenljivko lahko potem uporabljaš v vseh naslednjih funkcijah
(kjer jo boš potreboval, seveda).""")

    def test_03_prevod_besede(self):
        self.assertEqual("žoga", prevod_besede("žoga"))
        self.assertEqual("žoga", prevod_besede("žogico"))
        self.assertEqual("pero", prevod_besede("pero"))
        self.assertIsNone(prevod_besede("Miklavž"))


class Test07(Test):
    def test_01_poenostavi_besedilo(self):
        self.assertEqual("dragi miklavž\n\npišem ti kot vsako leto lep božič",
                         poenostavi_besedilo("Dragi Miklavž,\n\npišem ti (kot vsako leto):: lep božič!"))

    def test_02_izlusci_avtorja(self):
        self.assertEqual("Zala", izlusci_avtorja("podatki/pisma/zala.txt"))
        self.assertEqual("Janez", izlusci_avtorja("podatki/pisma/janez.txt"))

    def test_03_izlusci_darila(self):
        self.assertEqual({'glina', 'bomboni', 'piškoti'},
                         izlusci_darila("podatki/pisma/Klara.txt"))

        self.assertEqual({'čokolada', 'bomboni', 'zvezek', 'pero', 'vlak', 'žoga', 'kolo', 'knjiga'},
                         izlusci_darila("podatki/pisma/Dudley.txt"))

        self.assertEqual({'bomboni', 'glina', 'knjiga', 'kolo', 'medvedek', 'piškoti', 'vlak',
                          'zemljevid', 'čelada', 'čokolada'},
                         izlusci_darila("podatki/pisma/Janez.txt"))

    def test_04_darila_po_otrocih(self):
        self.assertEqual({'Albert': {'žoga'},
                          'Ana': {'knjiga', 'pisalo', 'zvezek'},
                          'Benjamin': {'čelada', 'kolo'},
                          'Berta': {'čokolada', 'piškoti'},
                          'Cilka': {'barvice', 'bomboni'},
                          'Dani': {'kocke', 'bomboni'},
                          'Daniela': {'knjiga', 'blazina', 'medvedek'},
                          'Dudley': {'vlak', 'zvezek', 'pero', 'čokolada', 'bomboni', 'žoga', 'knjiga', 'kolo'},
                          'Ema': {'knjiga', 'medvedek'},
                          'Ernest': {'žoga', 'knjiga'},
                          'Fanči': {'barvice', 'bomboni'},
                          'Franci': {'čokolada', 'avtomobilček'},
                          'Gorazd': {'knjiga'},
                          'Greta': {'žoga', 'barvice', 'bomboni'},
                          'Helga': {'knjiga', 'piškoti', 'žirafa'},
                          'Ivan': {'žoga', 'čokolada'},
                          'Janez': {'glina', 'vlak', 'zemljevid', 'piškoti', 'medvedek', 'čokolada', 'bomboni',
                                    'knjiga', 'čelada', 'kolo'},
                          'Klara': {'glina', 'piškoti', 'bomboni'},
                          'Krištof': {'zemljevid', 'pisalo', 'zvezek'},
                          'Lojze': {'knjiga', 'čokolada'},
                          'Miran': {'barvice', 'piškoti', 'medvedek'},
                          'Nina': {'barvice', 'medvedek', 'čokolada', 'žoga', 'blazina'},
                          'Olga': {'knjiga', 'zvezek'},
                          'Peter': {'vlak'},
                          'Robi': {'čokolada', 'medvedek'},
                          'Saša': {'piškoti', 'vlak'},
                          'Tina': {'barvice', 'vlak', 'medvedek', 'bomboni', 'žoga'},
                          'Urban': {'bomboni', 'knjiga', 'čelada', 'kolo', 'žirafa'},
                          'Veronika': {'blazina', 'piškoti', 'medvedek', 'žirafa'},
                          'Zala': {'barvice', 'pisalo', 'zvezek', 'pero', 'čokolada', 'bomboni', 'žoga',
                                   'avtomobilček'},
                          'Štefan': {'čokolada', 'kocke'},
                          'Žan': {'žoga', 'bomboni', 'vlak'}
                          }, darila_po_otrocih())

    def test_05_zbirnik(self):
        self.assertEqual({'avtomobilček': 2,
                          'barvice': 7,
                          'blazina': 3,
                          'bomboni': 11,
                          'glina': 2,
                          'knjiga': 11,
                          'kocke': 2,
                          'kolo': 4,
                          'medvedek': 8,
                          'pero': 2,
                          'pisalo': 3,
                          'piškoti': 7,
                          'vlak': 6,
                          'zemljevid': 2,
                          'zvezek': 5,
                          'čelada': 3,
                          'čokolada': 10,
                          'žirafa': 3,
                          'žoga': 9},
                         zbirnik_daril())


class Test08(Test):
    def test_01_preberi_cenik(self):
        self.assertEqual({'avtomobilček': 15.0,
                          'barvice': 9.0,
                          'bomboni': 3.0,
                          'knjiga': 12.0,
                          'medvedek': 15.0,
                          'pero': 4.0,
                          'pisalo': 3.0,
                          'piškoti': 4.5,
                          'vlak': 15.0,
                          'zemljevid': 9.0,
                          'zvezek': 5.0,
                          'čokolada': 3.5,
                          'žoga': 22.0},
                         preberi_cenik("Lampic"))

    def test_02_ceniki(self):
        self.assertEqual({'Dezman': {'avtomobilček': 15.0,
                                     'barvice': 7.0,
                                     'bomboni': 3.0,
                                     'knjiga': 15.0,
                                     'medvedek': 15.0,
                                     'pisalo': 3.0,
                                     'piškoti': 3.0,
                                     'zvezek': 4.0,
                                     'čelada': 22.0,
                                     'čokolada': 3.0,
                                     'žirafa': 13.0,
                                     'žoga': 20.0},
                          'Godler': {'barvice': 9.0,
                                     'bomboni': 3.0,
                                     'glina': 3.0,
                                     'knjiga': 15.0,
                                     'kocke': 28.0,
                                     'kolo': 230.0,
                                     'medvedek': 15.0,
                                     'pero': 5.0,
                                     'pisalo': 3.0,
                                     'piškoti': 5.0,
                                     'čelada': 25.0,
                                     'čokolada': 4.5,
                                     'žoga': 22.0},
                          'Klemencic': {'avtomobilček': 22.0,
                                        'barvice': 6.5,
                                        'blazina': 5.0,
                                        'bomboni': 3.0,
                                        'knjiga': 17.0,
                                        'kocke': 20.0,
                                        'kolo': 220.0,
                                        'medvedek': 15.0,
                                        'pero': 8.0,
                                        'pisalo': 3.0,
                                        'piškoti': 3.5,
                                        'čokolada': 5.0,
                                        'žirafa': 19.0,
                                        'žoga': 24.0},
                          'Lampic': {'avtomobilček': 15.0,
                                     'barvice': 9.0,
                                     'bomboni': 3.0,
                                     'knjiga': 12.0,
                                     'medvedek': 15.0,
                                     'pero': 4.0,
                                     'pisalo': 3.0,
                                     'piškoti': 4.5,
                                     'vlak': 15.0,
                                     'zemljevid': 9.0,
                                     'zvezek': 5.0,
                                     'čokolada': 3.5,
                                     'žoga': 22.0},
                          'Pavlic': {'barvice': 9.0,
                                     'bomboni': 3.0,
                                     'knjiga': 13.0,
                                     'kocke': 22.0,
                                     'kolo': 210.0,
                                     'medvedek': 15.0,
                                     'pero': 4.0,
                                     'pisalo': 3.0,
                                     'piškoti': 4.0,
                                     'zemljevid': 4.0,
                                     'zvezek': 4.5,
                                     'čokolada': 2.0,
                                     'žirafa': 16.0,
                                     'žoga': 21.0}}, ceniki())

    def test_03_najcenejsi_ponudnik(self):
        ponudbe = ceniki()
        ponudbe = {k: ponudbe[k] for k in ("Lampic", "Pavlic", "Dezman", "Klemencic", "Godler")}
        self.assertEqual(("Pavlic", 210), najcenejsi_ponudnik(ponudbe, "kolo"))
        self.assertEqual(("Pavlic", 15), najcenejsi_ponudnik(ponudbe, "medvedek"))
        self.assertEqual(("Godler", 3), najcenejsi_ponudnik(ponudbe, "glina"))
        self.assertEqual(("Dezman", 20), najcenejsi_ponudnik(ponudbe, "žoga"))

    def test_04_ponudniki_in_cene(self):
        ponudbe = ceniki()
        self.assertEqual({'glina': ('Godler', 3.0),
                          'kolo': ('Pavlic', 210.0),
                          'medvedek': ('Pavlic', 15.0),
                          'žoga': ('Dezman', 20.0)}, ponudniki_in_cene(ponudbe, {"medvedek", "kolo", "glina", "žoga"}))

        darila = set(zbirnik_daril())
        self.assertEqual({'avtomobilček': ('Lampic', 15.0),
                          'barvice': ('Klemencic', 6.5),
                          'blazina': ('Klemencic', 5.0),
                          'bomboni': ('Pavlic', 3.0),
                          'glina': ('Godler', 3.0),
                          'knjiga': ('Lampic', 12.0),
                          'kocke': ('Klemencic', 20.0),
                          'kolo': ('Pavlic', 210.0),
                          'medvedek': ('Pavlic', 15.0),
                          'pero': ('Pavlic', 4.0),
                          'pisalo': ('Pavlic', 3.0),
                          'piškoti': ('Dezman', 3.0),
                          'vlak': ('Lampic', 15.0),
                          'zemljevid': ('Pavlic', 4.0),
                          'zvezek': ('Dezman', 4.0),
                          'čelada': ('Dezman', 22.0),
                          'čokolada': ('Pavlic', 2.0),
                          'žirafa': ('Dezman', 13.0),
                          'žoga': ('Dezman', 20.0)},
                         ponudniki_in_cene(ponudbe, darila))


class Test09(Test):
    def test_01_vrednost_daril(self):
        self.assertEqual(270, vrednost_daril("Dudley"))
        self.assertEqual(9, vrednost_daril("Klara"))
        self.assertEqual(19, vrednost_daril("Ana"))
        self.assertEqual(289, vrednost_daril("Janez"))
        self.assertEqual(15, vrednost_daril("Peter"))

    def test_02_preberi_tockovalnik(self):
        self.assertEqual({'Albert': 290,
                          'Ana': 202,
                          'Benjamin': 419,
                          'Berta': 221,
                          'Cilka': 502,
                          'Dani': 214,
                          'Daniela': 407,
                          'Dudley': -393,
                          'Ema': 393,
                          'Ernest': 299,
                          'Fanči': 290,
                          'Franci': 296,
                          'Gorazd': 385,
                          'Greta': 433,
                          'Helga': 353,
                          'Ivan': 252,
                          'Janez': 397,
                          'Klara': 432,
                          'Krištof': 487,
                          'Lojze': 308,
                          'Miran': 309,
                          'Nina': 295,
                          'Olga': 368,
                          'Peter': 465,
                          'Robi': 321,
                          'Saša': 391,
                          'Tina': 448,
                          'Urban': 246,
                          'Veronika': 272,
                          'Zala': 253,
                          'Štefan': 429,
                          'Žan': 390},
                         preberi_tockovalnik())

    def test_03_dolocitev_daril(self):
        ponudniki_cene = {'avtomobilček': ('Lampic', 15.0),
                          'barvice': ('Klemencic', 6.5),
                          'blazina': ('Klemencic', 5.0),
                          'bomboni': ('Pavlic', 3.0),
                          'glina': ('Godler', 3.0),
                          'knjiga': ('Lampic', 12.0),
                          'kocke': ('Klemencic', 20.0),
                          'kolo': ('Pavlic', 210.0),
                          'medvedek': ('Pavlic', 15.0),
                          'pero': ('Pavlic', 4.0),
                          'pisalo': ('Pavlic', 3.0),
                          'piškoti': ('Dezman', 3.0),
                          'vlak': ('Lampic', 15.0),
                          'zemljevid': ('Pavlic', 4.0),
                          'zvezek': ('Dezman', 4.0),
                          'čelada': ('Dezman', 22.0),
                          'čokolada': ('Pavlic', 2.0),
                          'žirafa': ('Dezman', 13.0),
                          'žoga': ('Dezman', 20.0)}

        self.assertEqual({"čelada", "čokolada", "glina", "pisalo"},
                         dolocitev_daril(30, {"čelada", "žoga", "knjiga", "glina", "bomboni", "pisalo", "čokolada"},
                                         ponudniki_cene))

        self.assertEqual({"čelada"},
                         dolocitev_daril(22, {"čelada", "žoga", "knjiga", "glina", "bomboni", "pisalo", "čokolada"},
                                         ponudniki_cene))

        self.assertEqual({"žoga"},
                         dolocitev_daril(21, {"čelada", "žoga", "knjiga", "glina", "bomboni", "pisalo", "čokolada"},
                                         ponudniki_cene))

        self.assertEqual({"glina", "knjiga", "pisalo"},
                         dolocitev_daril(18, {"čelada", "žoga", "knjiga", "glina", "bomboni", "pisalo", "čokolada"},
                                         ponudniki_cene))

        self.assertEqual({"knjiga"},
                         dolocitev_daril(12, {"čelada", "žoga", "knjiga", "glina", "bomboni", "pisalo", "čokolada"},
                                         ponudniki_cene))

        self.assertEqual({"bomboni", "pisalo", "čokolada", "glina"},
                         dolocitev_daril(11, {"čelada", "žoga", "knjiga", "glina", "bomboni", "pisalo", "čokolada"},
                                         ponudniki_cene))

        self.assertEqual(set(),
                         dolocitev_daril(11, {"kolo"}, ponudniki_cene))

    def test_04_darila_za_otroka(self):
        otroci_darila = darila_po_otrocih()

        vsa_darila = set(zbirnik_daril())

        ponudbe = ceniki()
        ponudniki_cene = ponudniki_in_cene(ponudbe, vsa_darila)

        tockovalnik = preberi_tockovalnik()

        self.assertEqual({'žoga'}, darila_za_otroka('Albert', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'knjiga', 'pisalo', 'zvezek'},
                         darila_za_otroka('Ana', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'čelada'}, darila_za_otroka('Benjamin', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'piškoti', 'čokolada'}, darila_za_otroka('Berta', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'barvice', 'bomboni'}, darila_za_otroka('Cilka', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'kocke'}, darila_za_otroka('Dani', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'knjiga', 'medvedek', 'blazina'},
                         darila_za_otroka('Daniela', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual(set(), darila_za_otroka('Dudley', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'knjiga', 'medvedek'}, darila_za_otroka('Ema', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'žoga'}, darila_za_otroka('Ernest', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'barvice', 'bomboni'}, darila_za_otroka('Fanči', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'avtomobilček', 'čokolada'},
                         darila_za_otroka('Franci', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'knjiga'}, darila_za_otroka('Gorazd', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'barvice', 'bomboni', 'žoga'},
                         darila_za_otroka('Greta', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'knjiga', 'žirafa', 'piškoti'},
                         darila_za_otroka('Helga', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'čokolada', 'žoga'}, darila_za_otroka('Ivan', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'čokolada', 'čelada', 'vlak'},
                         darila_za_otroka('Janez', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'piškoti', 'glina', 'bomboni'},
                         darila_za_otroka('Klara', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'pisalo', 'zvezek', 'zemljevid'},
                         darila_za_otroka('Krištof', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'knjiga', 'čokolada'}, darila_za_otroka('Lojze', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'barvice', 'medvedek', 'piškoti'},
                         darila_za_otroka('Miran', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'barvice', 'čokolada', 'žoga'},
                         darila_za_otroka('Nina', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'knjiga', 'zvezek'}, darila_za_otroka('Olga', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'vlak'}, darila_za_otroka('Peter', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'medvedek', 'čokolada'}, darila_za_otroka('Robi', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'piškoti', 'vlak'}, darila_za_otroka('Saša', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'barvice', 'bomboni', 'vlak', 'žoga'},
                         darila_za_otroka('Tina', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'čelada'}, darila_za_otroka('Urban', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'piškoti', 'medvedek', 'blazina'},
                         darila_za_otroka('Veronika', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'zvezek', 'žoga'}, darila_za_otroka('Zala', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'kocke', 'čokolada'}, darila_za_otroka('Štefan', tockovalnik, otroci_darila, ponudniki_cene))
        self.assertEqual({'bomboni', 'vlak', 'žoga'},
                         darila_za_otroka('Žan', tockovalnik, otroci_darila, ponudniki_cene))


class Test10(Test):
    def test_01_narocila(self):
        narocila()
        exp = """Spoštovani dobavitelj,

pri vas bi rad naročil naslednja darila:

                     kosov
barvice..................6
blazina..................2
kocke....................2

Lep pozdrav,
Sveti Miklavž"""
        act = open("Klemencic.txt", encoding="utf-8").read()
        if not [x.rstrip() for x in exp.splitlines()] == \
               [x.rstrip() for x in act.splitlines()]:
            self.assertEqual(exp, act)


if __name__ == "__main__":
    unittest.main()

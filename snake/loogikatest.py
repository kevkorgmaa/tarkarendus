# =============================================================================
#  TESTID  –  game_logic.py mooduli testimine
#  Käivitamine:
#    pytest  test_game_logic.py -v
#    python -m unittest test_game_logic.py -v
# =============================================================================

import unittest
from manguloogika import (
    RUUDUSTIKU_LAIUS,
    RUUDUSTIKU_KÕRGUS,
    arvuta_uus_pea,
    on_vastassuund,
    on_kokkupõrge_iseendaga,
    on_kokkupõrge_kiviga,
    uuenda_uss,
    lühenda_uss,
    arvuta_kiirus,
    sorteeri_ja_piirita_tulemused,
    on_uus_rekord,
)


# =============================================================================
#  1. LIIKUMINE JA WRAP-AROUND
# =============================================================================

class TestArvutaUusPea(unittest.TestCase):
    """Testib ussi liikumist ja läbivaid seinu."""

    def test_liikumine_paremale(self):
        uss = [(5, 5)]
        self.assertEqual(arvuta_uus_pea(uss, (1, 0)), (6, 5))

    def test_liikumine_vasakule(self):
        uss = [(5, 5)]
        self.assertEqual(arvuta_uus_pea(uss, (-1, 0)), (4, 5))

    def test_liikumine_üles(self):
        uss = [(5, 5)]
        self.assertEqual(arvuta_uus_pea(uss, (0, -1)), (5, 4))

    def test_liikumine_alla(self):
        uss = [(5, 5)]
        self.assertEqual(arvuta_uus_pea(uss, (0, 1)), (5, 6))

    def test_wrap_parem_serv(self):
        # Paremast servast välja → tuleb vasakult
        uss = [(RUUDUSTIKU_LAIUS - 1, 5)]
        uus_pea = arvuta_uus_pea(uss, (1, 0))
        self.assertEqual(uus_pea, (0, 5))

    def test_wrap_vasak_serv(self):
        # Vasakust servast välja → tuleb paremalt
        uss = [(0, 5)]
        uus_pea = arvuta_uus_pea(uss, (-1, 0))
        self.assertEqual(uus_pea, (RUUDUSTIKU_LAIUS - 1, 5))

    def test_wrap_ülemine_serv(self):
        # Ülemisest servast välja → tuleb alt
        uss = [(5, 0)]
        uus_pea = arvuta_uus_pea(uss, (0, -1))
        self.assertEqual(uus_pea, (5, RUUDUSTIKU_KÕRGUS - 1))

    def test_wrap_alumine_serv(self):
        # Alumisest servast välja → tuleb ülevalt
        uss = [(5, RUUDUSTIKU_KÕRGUS - 1)]
        uus_pea = arvuta_uus_pea(uss, (0, 1))
        self.assertEqual(uus_pea, (5, 0))

    def test_pikk_uss_kasutab_pead(self):
        # Ainult viimane ruut (pea) loeb, mitte esimene
        uss = [(1, 1), (2, 1), (3, 1)]
        self.assertEqual(arvuta_uus_pea(uss, (1, 0)), (4, 1))


class TestOnVastassuund(unittest.TestCase):
    """Testib vastassuuna kontrolli."""

    def test_parem_ja_vasak_on_vastakud(self):
        self.assertTrue(on_vastassuund((1, 0), (-1, 0)))

    def test_üles_ja_alla_on_vastakud(self):
        self.assertTrue(on_vastassuund((0, -1), (0, 1)))

    def test_parem_ja_alla_ei_ole_vastakud(self):
        self.assertFalse(on_vastassuund((1, 0), (0, 1)))

    def test_sama_suund_ei_ole_vastak(self):
        self.assertFalse(on_vastassuund((1, 0), (1, 0)))

    def test_üles_ja_vasak_ei_ole_vastakud(self):
        self.assertFalse(on_vastassuund((0, -1), (-1, 0)))


# =============================================================================
#  2. KOKKUPÕRKED
# =============================================================================

class TestKokkupõrgeIseendaga(unittest.TestCase):
    """Testib ussi kokkupõrget iseendaga."""

    def test_pea_tabab_keha(self):
        uss = [(3, 5), (4, 5), (5, 5)]
        self.assertTrue(on_kokkupõrge_iseendaga(uss, (3, 5)))

    def test_vaba_ruut_pole_kokkupõrge(self):
        uss = [(3, 5), (4, 5), (5, 5)]
        self.assertFalse(on_kokkupõrge_iseendaga(uss, (6, 5)))

    def test_üheruuduline_uss_ei_põrka(self):
        uss = [(5, 5)]
        self.assertFalse(on_kokkupõrge_iseendaga(uss, (6, 5)))

    def test_pea_tabab_saba(self):
        uss = [(1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (1, 2)]
        self.assertTrue(on_kokkupõrge_iseendaga(uss, (1, 1)))


class TestKokkupõrgeKiviga(unittest.TestCase):
    """Testib ussi kokkupõrget kividega (MOD-4)."""

    def test_pea_tabab_kivi(self):
        kivid = {(5, 5), (10, 10)}
        self.assertTrue(on_kokkupõrge_kiviga((5, 5), kivid))

    def test_vaba_ruut_pole_kivi(self):
        kivid = {(5, 5)}
        self.assertFalse(on_kokkupõrge_kiviga((6, 5), kivid))

    def test_tühi_kivide_hulk(self):
        self.assertFalse(on_kokkupõrge_kiviga((5, 5), set()))


# =============================================================================
#  3. USSI KASV JA LÜHENEMINE
# =============================================================================

class TestUuendaUss(unittest.TestCase):
    """Testib ussi liikumist, kasvu ja saba eemaldamist."""

    def test_uss_liigub_ilma_kasvuta(self):
        # kasv=0: saba eemaldatakse, pea lisatakse
        uss, kasv = uuenda_uss([(3, 5), (4, 5)], (5, 5), kasv=0)
        self.assertEqual(uss, [(4, 5), (5, 5)])
        self.assertEqual(kasv, 0)

    def test_uss_kasvab(self):
        # kasv=1: saba ei eemaldata, uss pikeneb
        uss, kasv = uuenda_uss([(3, 5), (4, 5)], (5, 5), kasv=1)
        self.assertEqual(uss, [(3, 5), (4, 5), (5, 5)])
        self.assertEqual(kasv, 0)

    def test_kasvuloendur_väheneb(self):
        _, kasv = uuenda_uss([(5, 5)], (6, 5), kasv=3)
        self.assertEqual(kasv, 2)

    def test_originaal_uss_ei_muutu(self):
        # Funktsioon ei tohi muuta algset listi
        originaal = [(3, 5), (4, 5)]
        uuenda_uss(originaal, (5, 5), kasv=0)
        self.assertEqual(originaal, [(3, 5), (4, 5)])


class TestLühendaUss(unittest.TestCase):
    """Testib mürgitatud õuna efekti (MOD-2): ussi lühenemine."""

    def test_pikk_uss_lüheneb(self):
        uss = [(1, 1), (2, 1), (3, 1), (4, 1)]
        tulemus = lühenda_uss(uss)
        self.assertEqual(len(tulemus), 3)
        self.assertEqual(tulemus[0], (2, 1))  # saba eemaldati

    def test_kaheruuduline_uss_ei_lühene(self):
        uss = [(1, 1), (2, 1)]
        tulemus = lühenda_uss(uss)
        self.assertEqual(len(tulemus), 2)

    def test_üheruuduline_uss_ei_lühene(self):
        uss = [(1, 1)]
        tulemus = lühenda_uss(uss)
        self.assertEqual(len(tulemus), 1)

    def test_originaal_ei_muutu(self):
        originaal = [(1, 1), (2, 1), (3, 1)]
        lühenda_uss(originaal)
        self.assertEqual(len(originaal), 3)


# =============================================================================
#  4. KIIRUS JA SKOOR
# =============================================================================

class TestArvutaKiirus(unittest.TestCase):
    """Testib kiiruse suurenemist iga 5 õuna järel."""

    def test_kiirus_suureneb_5_juures(self):
        self.assertEqual(arvuta_kiirus(12, 5), 13)

    def test_kiirus_suureneb_10_juures(self):
        self.assertEqual(arvuta_kiirus(13, 10), 14)

    def test_kiirus_ei_suurene_muul_skooril(self):
        self.assertEqual(arvuta_kiirus(12, 3), 12)
        self.assertEqual(arvuta_kiirus(12, 7), 12)

    def test_maksimaalne_kiirus_on_30(self):
        self.assertEqual(arvuta_kiirus(30, 5), 30)

    def test_kiirus_ei_ületa_30(self):
        self.assertEqual(arvuta_kiirus(29, 5), 30)

    def test_skoor_null_ei_muuda_kiirust(self):
        self.assertEqual(arvuta_kiirus(12, 0), 12)


# =============================================================================
#  5. TULEMUSTE TABEL
# =============================================================================

class TestSorteerijaPiirita(unittest.TestCase):
    """Testib tulemuste sorteerimist ja top-5 piiramist (MOD-3)."""

    def test_lisab_uue_tulemuse(self):
        tulemused = [(10, "KERGE"), (8, "KERGE")]
        uued = sorteeri_ja_piirita_tulemused(tulemused, 12, "RASKE")
        self.assertEqual(uued[0], (12, "RASKE"))

    def test_sorteerib_kahanevalt(self):
        tulemused = [(5, "KERGE"), (15, "RASKE"), (10, "KESKMINE")]
        uued = sorteeri_ja_piirita_tulemused(tulemused, 8, "KERGE")
        skoorid = [s for s, _ in uued]
        self.assertEqual(skoorid, sorted(skoorid, reverse=True))

    def test_hoidab_maksimaalselt_5(self):
        tulemused = [(10, "K"), (9, "K"), (8, "K"), (7, "K"), (6, "K")]
        uued = sorteeri_ja_piirita_tulemused(tulemused, 5, "K")
        self.assertEqual(len(uued), 5)

    def test_nõrk_tulemus_ei_mahu_sisse(self):
        tulemused = [(10, "K"), (9, "K"), (8, "K"), (7, "K"), (6, "K")]
        uued = sorteeri_ja_piirita_tulemused(tulemused, 1, "K")
        skoorid = [s for s, _ in uued]
        self.assertNotIn(1, skoorid)

    def test_tühi_nimekiri(self):
        uued = sorteeri_ja_piirita_tulemused([], 10, "KERGE")
        self.assertEqual(uued, [(10, "KERGE")])


class TestOnUusRekord(unittest.TestCase):
    """Testib rekordikontrolli."""

    def test_tühi_nimekiri_on_rekord(self):
        self.assertTrue(on_uus_rekord([], 5))

    def test_alla_5_tulemuse_on_rekord(self):
        tulemused = [(10, "K"), (8, "K")]
        self.assertTrue(on_uus_rekord(tulemused, 1))

    def test_ületab_viimase_top5(self):
        tulemused = [(10, "K"), (9, "K"), (8, "K"), (7, "K"), (6, "K")]
        self.assertTrue(on_uus_rekord(tulemused, 7))

    def test_ei_ületa_viimast_top5(self):
        tulemused = [(10, "K"), (9, "K"), (8, "K"), (7, "K"), (6, "K")]
        self.assertFalse(on_uus_rekord(tulemused, 5))

    def test_võrdne_viimase_top5ga_pole_rekord(self):
        tulemused = [(10, "K"), (9, "K"), (8, "K"), (7, "K"), (6, "K")]
        self.assertFalse(on_uus_rekord(tulemused, 6))


# =============================================================================
#  KÄIVITAMINE
# =============================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
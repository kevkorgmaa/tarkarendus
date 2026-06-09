"""
=============================================================
 USSI-MOOD - PyGame Ussimäng
 Autor: [Sinu Nimi]
 Kuupäev: 2026
 Versioon: 1.0

 TÄIENDUSED (5 modifikatsiooni):
   1. TASEMED (Levels)       - mäng kiireneb iga 5 punktiga
   2. TAKISTUSED (Obstacles) - kasvav seinte/takistuste arv
   3. ERILINE TOIT (Power-up) - kuldne õun annab +3 punkti ja aeglustab
   4. MITU ELU (Lives)       - mängijal on 3 elu
   5. ANIMEERITUD TAUST       - liikuv täheline taust vastavalt tasemele
=============================================================
"""

import pygame          # peamine mängumootor
import random          # juhuslike arvude generaator
import sys             # süsteemi funktsioonid (väljumine)
import math            # matemaatilised funktsioonid (animatsiooniks)

# ── Pygame initsialiseerimine ──────────────────────────────
pygame.init()
pygame.mixer.init()    # helikaart (mõjud)

# ── Akna seaded ───────────────────────────────────────────
LAIUS = 800            # akna laius pikslites
KÕRGUS = 650           # akna kõrgus pikslites
PANEEL_KÕRGUS = 50     # ülaosa infopaneeli kõrgus

# ── Ruudustiku seaded ─────────────────────────────────────
PLOKI_SUURUS = 20      # ühe mänguruudu suurus pikslites
VEERGUDE_ARV = LAIUS // PLOKI_SUURUS          # ruudustiku veergude arv
RIDADE_ARV = (KÕRGUS - PANEEL_KÕRGUS) // PLOKI_SUURUS  # ruudustiku ridade arv

# ── Värvipalett ───────────────────────────────────────────
MUST           = (0, 0, 0)
VALGE          = (255, 255, 255)
ROHELINE       = (0, 200, 50)       # ussi keha põhivärv
TUMEROHELINE   = (0, 140, 30)       # ussi keha teine värv (ruudustik)
PEAVÄRV        = (0, 255, 100)      # ussi pea värv
PUNANE         = (220, 30, 30)      # tavaline toit (õun)
KULLANE        = (255, 215, 0)      # eriline toit (kuldõun)
HALL           = (80, 80, 80)       # takistuste värv
TUME_HALL      = (50, 50, 50)       # taust
SININE_TAUST   = (5, 10, 30)        # animeeritud tausta põhivärv
PUNANE_TAUST   = (30, 5, 5)         # kõrge taseme tausta värv
ELU_PUNANE     = (255, 60, 60)      # elude kuvamine
TEKST_KOLLANE  = (255, 230, 0)      # tähtsate tekstide värv

# ── Liikumissuunad ────────────────────────────────────────
ÜLES    = (0, -1)
ALLA    = (0, 1)
VASAKULE = (-1, 0)
PAREMALE = (1, 0)

# ── Mängu põhiklassis kasutatavad konstandid ──────────────
ALGKIIRUS         = 8     # algne kaadrisagedus (liikumised sekundis)
KIIRUSE_KASV      = 2     # kiiruse juurdekasv taseme kohta
MAKS_KIIRUS       = 25    # maksimaalne kiirus
PUNKTID_TASEMEKS  = 5     # mitu punkti on vaja järgmisele tasemele
ERILINE_TÕENÄOSUS = 15    # tõenäosus (%) et toit on kuldne
ERILINE_KESTUS    = 150   # kuldõuna eluiga kaadrites (150 / FPS = ~sekundit)
AEGLUSTUS_KESTUS  = 100   # kuldõuna aeglustusefekti kestus kaadrites


class Ussimaang:
    """
    Peamine mänguklass - haldab kogu mängu loogikat ja joonistamist.
    Sisaldab kõiki 5 modifikatsiooni:
      - tasemed, takistused, eriline toit, mitu elu, animeeritud taust
    """

    def __init__(self):
        """Mängu initsialiseerimine - seab kõik algväärtused."""
        # Loo mänguaken
        self.ekraan = pygame.display.set_mode((LAIUS, KÕRGUS))
        pygame.display.set_caption("🐍 USSI-MOOD - Sinu Mood Mäng!")

        # Kellaobj - FPS kontrollimiseks
        self.kell = pygame.time.Clock()

        # Laadi fondid
        self.font_suur   = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_kesk   = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_väike  = pygame.font.SysFont("Arial", 18)
        self.font_tiitel = pygame.font.SysFont("Arial", 64, bold=True)

        # Loo heli (lühike beep programmiliselt)
        self.heli_sõö   = self._loo_heli(440, 80)    # söömine - kõrgem toon
        self.heli_kuldne = self._loo_heli(880, 150)  # kuldõun - kõrgem pikk toon
        self.heli_surm  = self._loo_heli(150, 400)   # surm - madal pikk toon

        # Initsialiseeri mänguolek
        self._alusta_uus_mäng()

        # Animatsiooni loendur (tähtede liikumiseks taustal)
        self.animatsioon_loendur = 0

        # Tähed taustal (MODIFIKATSIOON 5: animeeritud taust)
        self.tähed = self._genereeri_tähed(100)

    # ── Abimeetodid ───────────────────────────────────────

    def _loo_heli(self, sagedus, kestus_ms):
        """
        Loo programmiline heli antud sageduse ja kestusega.
        Kasutab numpy-laadset lähendust läbi pygame.sndarray.
        Tagastab pygame.Sound objekti või None.
        """
        try:
            import numpy as np
            näidissagedus = 44100                          # standardne helinäidissagedus
            näidiste_arv  = int(näidissagedus * kestus_ms / 1000)
            t = np.linspace(0, kestus_ms / 1000, näidiste_arv, False)
            laine = np.sin(sagedus * t * 2 * math.pi)     # sinuslaine genereerimine
            heli_andmed = (laine * 32767).astype(np.int16)
            stereo = np.column_stack([heli_andmed, heli_andmed])  # stereo
            heli = pygame.sndarray.make_sound(stereo)
            heli.set_volume(0.3)                           # vaikne volüüm
            return heli
        except Exception:
            return None   # kui numpy puudub, siis helita

    def _mängi_heli(self, heli):
        """Mängi heli ohutult (kontrollib, kas heli on olemas)."""
        if heli is not None:
            try:
                heli.play()
            except Exception:
                pass

    def _genereeri_tähed(self, arv):
        """
        MODIFIKATSIOON 5: Genereeri juhuslikud tähed animeeritud taustaks.
        Iga täht on sõnastik: positsioon, suurus, kiirus, heledus.
        """
        tähed = []
        mänguala_y = PANEEL_KÕRGUS   # tähed ainult mänguala kohal
        for _ in range(arv):
            täht = {
                "x":       random.randint(0, LAIUS),
                "y":       random.randint(mänguala_y, KÕRGUS),
                "suurus":  random.uniform(0.5, 2.5),    # tähe suurus
                "kiirus":  random.uniform(0.1, 0.5),    # vilkumise kiirus
                "faas":    random.uniform(0, 2 * math.pi),  # algfaas
            }
            tähed.append(täht)
        return tähed

    def _alusta_uus_mäng(self):
        """
        Lähtesta kõik mängu muutujad - kasutatakse nii alustamisel
        kui ka pärast mängu lõppu uuesti alustamisel.
        """
        # ── Uss ───────────────────────────────────────────
        # Uss algab ekraani keskel, 3 plokki pikk
        kesk_x = VEERGUDE_ARV // 2
        kesk_y = RIDADE_ARV // 2
        self.uss = [
            (kesk_x,     kesk_y),    # pea
            (kesk_x - 1, kesk_y),    # keha
            (kesk_x - 2, kesk_y),    # saba
        ]
        self.suund         = PAREMALE   # algne liikumissuund
        self.järgmine_suund = PAREMALE  # järgmise sammu suund (puhver)

        # ── Punktid ja tasemed ────────────────────────────
        self.punktid        = 0         # praegune punktisumma
        self.tase           = 1         # praegune tase (alates 1)
        self.kiirus         = ALGKIIRUS # praegune mängukiirus (FPS)

        # ── Elude süsteem (MODIFIKATSIOON 4) ─────────────
        self.elud           = 3         # algne elukogus
        self.surnud         = False     # kas uss on hetkel surnud (vilgub)
        self.surma_loendur  = 0         # surma-animatsiooni loendur

        # ── Toit ──────────────────────────────────────────
        self.toit           = None      # tavatoidu positsioon
        self.eriline_toit   = None      # kuldõuna positsioon
        self.eriline_loendur = 0        # kuldõuna eluea loendur

        # ── Aeglustusefekt (MODIFIKATSIOON 3) ────────────
        self.aeglustus_loendur = 0      # kuldõunast saadud aeglustuse loendur

        # ── Takistused (MODIFIKATSIOON 2) ─────────────────
        # NB! Takistused peavad olema enne _paiguta_toit() kutsumist!
        self.takistused     = []        # takistuste loend [(x, y), ...]
        self._uuenda_takistused()       # lisa tasemele vastavad takistused

        # ── Toit paigutatakse PÄRAST takistusi ────────────
        self._paiguta_toit()            # pane esimene toit mängulauale

        # ── Parimad tulemused ─────────────────────────────
        self.parim_tulemus  = getattr(self, "parim_tulemus", 0)  # säilita parimat

        # ── Mängu olek ────────────────────────────────────
        self.mäng_käib      = True      # kas mäng on aktiivne
        self.paus           = False     # kas mäng on peatatud

    def _paiguta_toit(self):
        """
        Pane toit juhuslikule vabale positsioonile mängulaual.
        Kontrollib, et toit ei kattuks ussi ega takistustega.
        MODIFIKATSIOON 3: juhuslikult võib ilmuda kuldõun.
        """
        hõivatud = set(self.uss) | set(self.takistused)  # kõik hõivatud ruudud

        # Leia vaba ruut tavalisele toidule
        vabad = [
            (x, y)
            for x in range(VEERGUDE_ARV)
            for y in range(RIDADE_ARV)
            if (x, y) not in hõivatud
        ]
        if vabad:
            self.toit = random.choice(vabad)   # vali juhuslik vaba ruut

        # MODIFIKATSIOON 3: kas genereerida kuldõun?
        # Kuldõun ilmub ainult siis kui eelmist pole ja tõenäosus täitub
        if self.eriline_toit is None:
            if random.randint(1, 100) <= ERILINE_TÕENÄOSUS:
                vabad2 = [r for r in vabad if r != self.toit]
                if vabad2:
                    self.eriline_toit    = random.choice(vabad2)
                    self.eriline_loendur = ERILINE_KESTUS  # sea eluiga

    def _uuenda_takistused(self):
        """
        MODIFIKATSIOON 2: Loo takistused vastavalt praegusele tasemele.
        Kõrgem tase = rohkem takistusi.
        Takistused on juhuslikult paigutatud ruudud (ei kattu ussi/toiduga).
        """
        self.takistused = []
        takistuste_arv = (self.tase - 1) * 3   # taseme 1 = 0, tase 2 = 3, jne

        hõivatud = set(self.uss)
        # Lisame ohutsusvööndi ussi ümber (et mäng poleks kohe võimatu)
        pea_x, pea_y = self.uss[0]
        ohutu_tsoon = {
            (pea_x + dx, pea_y + dy)
            for dx in range(-3, 4)
            for dy in range(-3, 4)
        }

        for _ in range(takistuste_arv):
            katseid = 0
            while katseid < 100:   # max 100 katset et mitte lõputult otsida
                x = random.randint(0, VEERGUDE_ARV - 1)
                y = random.randint(0, RIDADE_ARV - 1)
                pos = (x, y)
                if pos not in hõivatud and pos not in ohutu_tsoon:
                    self.takistused.append(pos)
                    hõivatud.add(pos)
                    break
                katseid += 1

    # ── Mängu loogika ─────────────────────────────────────

    def _liigu(self):
        """
        Liiguta ussi ühe sammu edasi.
        Kontrollib kõiki kokkupõrkeid: seinad, iseenda keha, takistused.
        Käsitleb toidu söömist ja punktide/tasemete uuendamist.
        """
        if self.surnud:
            # Uss vilgub surma-animatsiooni ajal, ei liigu
            self.surma_loendur += 1
            if self.surma_loendur >= 30:   # 30 kaadrit vilkumist (~0.5s)
                self.surnud        = False
                self.surma_loendur = 0
                # Lähtesta uss aga säilita punktid ja tase
                self._lähtesta_uss_pärast_surma()
            return

        # Uuenda suund (puhvrist)
        self.suund = self.järgmine_suund

        # Arvuta uue pea positsioon
        pea_x, pea_y = self.uss[0]
        dx, dy       = self.suund
        uus_pea      = (pea_x + dx, pea_y + dy)

        # ── Kontroll 1: Seina põrkamine ───────────────────
        if not (0 <= uus_pea[0] < VEERGUDE_ARV and 0 <= uus_pea[1] < RIDADE_ARV):
            self._käsitle_surm()
            return

        # ── Kontroll 2: Iseenda põrkamine ─────────────────
        if uus_pea in self.uss[:-1]:   # [:-1] kuna saba liigub samal ajal
            self._käsitle_surm()
            return

        # ── Kontroll 3: Takistusega põrkamine (MOD 2) ─────
        if uus_pea in self.takistused:
            self._käsitle_surm()
            return

        # ── Liiguta ussi ──────────────────────────────────
        self.uss.insert(0, uus_pea)    # lisa uus pea

        # ── Kontroll: Kas sõime tavalist toitu? ───────────
        if uus_pea == self.toit:
            self.punktid += 1
            self._mängi_heli(self.heli_sõö)
            self._uuenda_tase()        # kontrolli kas tase muutus
            self._paiguta_toit()       # pane uus toit
        # ── Kontroll: Kas sõime kuldõuna? (MOD 3) ─────────
        elif uus_pea == self.eriline_toit:
            self.punktid          += 3              # +3 punkti kuldõunast
            self.aeglustus_loendur = AEGLUSTUS_KESTUS  # aktiveeri aeglustus
            self.eriline_toit      = None            # eemalda kuldõun
            self._mängi_heli(self.heli_kuldne)
            self._uuenda_tase()
            self._paiguta_toit()       # võib tekkida uus kuldõun
        else:
            self.uss.pop()             # eemalda saba (uss ei kasva)

        # ── Kuldõuna eluea vähendamine ────────────────────
        if self.eriline_toit is not None:
            self.eriline_loendur -= 1
            if self.eriline_loendur <= 0:
                self.eriline_toit = None   # kuldõun kadus

        # ── Aeglustuse loenduri vähendamine (MOD 3) ───────
        if self.aeglustus_loendur > 0:
            self.aeglustus_loendur -= 1

    def _käsitle_surm(self):
        """
        MODIFIKATSIOON 4: Käsitle ussi surma.
        Vähendab elusid, käivitab surma-animatsiooni.
        Kui elud otsas → mäng läbi.
        """
        self._mängi_heli(self.heli_surm)
        self.elud -= 1                   # vähenda elusid
        if self.elud <= 0:
            # Mäng läbi - uuenda parimat tulemust
            if self.punktid > self.parim_tulemus:
                self.parim_tulemus = self.punktid
            self.mäng_käib = False       # lõpeta mäng
        else:
            # Veel elusid järel - käivita surma-animatsioon
            self.surnud        = True
            self.surma_loendur = 0

    def _lähtesta_uss_pärast_surma(self):
        """
        Pärast elukaotust - lähtesta ussi positsioon ja takistused.
        Punktid ja tase jäävad samaks (MODIFIKATSIOON 4).
        """
        kesk_x = VEERGUDE_ARV // 2
        kesk_y = RIDADE_ARV // 2
        self.uss = [
            (kesk_x,     kesk_y),
            (kesk_x - 1, kesk_y),
            (kesk_x - 2, kesk_y),
        ]
        self.suund          = PAREMALE
        self.järgmine_suund = PAREMALE
        self.eriline_toit   = None      # eemalda kuldõun
        self._paiguta_toit()            # pane uus toit
        self._uuenda_takistused()       # pane takistused uuesti

    def _uuenda_tase(self):
        """
        MODIFIKATSIOON 1: Kontrolli kas mängija on jõudnud uuele tasemele.
        Iga PUNKTID_TASEMEKS punkti = 1 tase rohkem.
        Kõrgem tase = suurem kiirus + rohkem takistusi.
        """
        uus_tase = self.punktid // PUNKTID_TASEMEKS + 1
        if uus_tase > self.tase:
            self.tase  = uus_tase
            # Uuenda kiirus - kuid ärge ületa maksimumi
            self.kiirus = min(ALGKIIRUS + (self.tase - 1) * KIIRUSE_KASV, MAKS_KIIRUS)
            self._uuenda_takistused()   # lisa uued takistused (MOD 2)

    # ── Joonistamine ──────────────────────────────────────

    def _joonista_animeeritud_taust(self):
        """
        MODIFIKATSIOON 5: Joonista animeeritud tähtedega kosmose taust.
        Tausta värv muutub tasemega (sinine → punane kõrgetel tasemetel).
        Tähed vilguvad sinusfunktsiooni abil.
        """
        self.animatsioon_loendur += 1   # suurenda animatsiooniloendur

        # Sega tausta värvi vastavalt tasemele (sinine → punane)
        t = min((self.tase - 1) / 10.0, 1.0)   # 0.0 kuni 1.0 vastavalt tasemele
        r = int(SININE_TAUST[0] * (1 - t) + PUNANE_TAUST[0] * t)
        g = int(SININE_TAUST[1] * (1 - t) + PUNANE_TAUST[1] * t)
        b = int(SININE_TAUST[2] * (1 - t) + PUNANE_TAUST[2] * t)
        self.ekraan.fill((r, g, b))     # täida ekraan taustavärviga

        # Joonista vilkuvad tähed
        for täht in self.tähed:
            # Arvuta heledus sinusfunktsiooni abil (vilkumine)
            heledus = 0.5 + 0.5 * math.sin(
                self.animatsioon_loendur * täht["kiirus"] + täht["faas"]
            )
            värv = int(heledus * 200) + 55   # heledus vahemikus 55-255
            pygame.draw.circle(
                self.ekraan,
                (värv, värv, min(värv + 40, 255)),   # pisut sinakam
                (int(täht["x"]), int(täht["y"])),
                max(1, int(täht["suurus"])),
            )

    def _joonista_infopaneel(self):
        """
        Joonista ülaosas infopaneel:
        punktid, tase, elud (südamed), parim tulemus.
        """
        # Taustariba paneelile
        pygame.draw.rect(self.ekraan, (15, 15, 40), (0, 0, LAIUS, PANEEL_KÕRGUS))
        pygame.draw.line(self.ekraan, ROHELINE, (0, PANEEL_KÕRGUS), (LAIUS, PANEEL_KÕRGUS), 2)

        # Punktid
        punkti_tekst = self.font_kesk.render(f"Punktid: {self.punktid}", True, VALGE)
        self.ekraan.blit(punkti_tekst, (10, 12))

        # Tase (MODIFIKATSIOON 1)
        tase_tekst = self.font_kesk.render(f"Tase: {self.tase}", True, TEKST_KOLLANE)
        self.ekraan.blit(tase_tekst, (200, 12))

        # Elud südametena (MODIFIKATSIOON 4)
        elu_x = 380
        for i in range(3):
            värv = ELU_PUNANE if i < self.elud else (60, 60, 60)
            # Joonista süda kahe ringi ja kolmnurgaga
            pygame.draw.circle(self.ekraan, värv, (elu_x + i * 35 + 6, 20), 7)
            pygame.draw.circle(self.ekraan, värv, (elu_x + i * 35 + 18, 20), 7)
            pygame.draw.polygon(self.ekraan, värv, [
                (elu_x + i * 35, 22),
                (elu_x + i * 35 + 24, 22),
                (elu_x + i * 35 + 12, 36),
            ])

        # Aeglustusefekti indikaator (MODIFIKATSIOON 3)
        if self.aeglustus_loendur > 0:
            prot = self.aeglustus_loendur / AEGLUSTUS_KESTUS
            aegl_tekst = self.font_väike.render("⚡ AEGLUSTUS", True, KULLANE)
            self.ekraan.blit(aegl_tekst, (490, 5))
            # Edenemisriba
            pygame.draw.rect(self.ekraan, (80, 80, 0), (490, 28, 120, 8))
            pygame.draw.rect(self.ekraan, KULLANE, (490, 28, int(120 * prot), 8))

        # Parim tulemus
        parim_tekst = self.font_väike.render(f"Rekord: {self.parim_tulemus}", True, (180, 180, 180))
        self.ekraan.blit(parim_tekst, (LAIUS - 140, 15))

    def _joonista_uss(self):
        """
        Joonista uss.
        Pea on erinevat värvi ja erineva suurusega kui keha.
        Surma ajal vilgub (MODIFIKATSIOON 4).
        """
        if self.surnud:
            # Vilgub surma-animatsiooni ajal
            if (self.surma_loendur // 5) % 2 == 0:
                return   # iga 5. kaadri tagant peidab ussi

        for i, (x, y) in enumerate(self.uss):
            ekraani_x = x * PLOKI_SUURUS
            ekraani_y = y * PLOKI_SUURUS + PANEEL_KÕRGUS

            if i == 0:
                # Pea - suurem ja heledam
                pygame.draw.rect(
                    self.ekraan, PEAVÄRV,
                    (ekraani_x + 1, ekraani_y + 1, PLOKI_SUURUS - 2, PLOKI_SUURUS - 2),
                    border_radius=5,
                )
                # Silmad
                dx, dy = self.suund
                s1 = (ekraani_x + 5 + dx * 5, ekraani_y + 5 + dy * 5)
                s2 = (ekraani_x + PLOKI_SUURUS - 5 + dx * 5, ekraani_y + 5 + dy * 5)
                pygame.draw.circle(self.ekraan, MUST, s1, 2)
                pygame.draw.circle(self.ekraan, MUST, s2, 2)
            else:
                # Keha - vahelduvad toonid (ruudustik-efekt)
                värv = ROHELINE if i % 2 == 0 else TUMEROHELINE
                pygame.draw.rect(
                    self.ekraan, värv,
                    (ekraani_x + 2, ekraani_y + 2, PLOKI_SUURUS - 4, PLOKI_SUURUS - 4),
                    border_radius=3,
                )

    def _joonista_toit(self):
        """Joonista tavaline (punane) ja eriline (kuldne) toit."""
        # Tavaline toit - punane õun
        if self.toit:
            x, y = self.toit
            cx = x * PLOKI_SUURUS + PLOKI_SUURUS // 2
            cy = y * PLOKI_SUURUS + PLOKI_SUURUS // 2 + PANEEL_KÕRGUS
            pygame.draw.circle(self.ekraan, PUNANE, (cx, cy), PLOKI_SUURUS // 2 - 2)
            # Vars
            pygame.draw.line(
                self.ekraan, (0, 120, 0),
                (cx, cy - PLOKI_SUURUS // 2 + 2),
                (cx + 3, cy - PLOKI_SUURUS // 2 - 3), 2,
            )

        # Eriline toit - MODIFIKATSIOON 3 - kuldõun vilgub
        if self.eriline_toit:
            x, y = self.eriline_toit
            cx = x * PLOKI_SUURUS + PLOKI_SUURUS // 2
            cy = y * PLOKI_SUURUS + PLOKI_SUURUS // 2 + PANEEL_KÕRGUS
            # Vilkumisefekt - heledus muutub
            heledus = 0.7 + 0.3 * math.sin(self.animatsioon_loendur * 0.2)
            r = int(255 * heledus)
            g = int(215 * heledus)
            pygame.draw.circle(self.ekraan, (r, g, 0), (cx, cy), PLOKI_SUURUS // 2 - 1)
            # Sära efekt
            pygame.draw.circle(self.ekraan, VALGE, (cx - 3, cy - 3), 3)
            # Vars
            pygame.draw.line(
                self.ekraan, (0, 150, 0),
                (cx, cy - PLOKI_SUURUS // 2 + 1),
                (cx + 3, cy - PLOKI_SUURUS // 2 - 4), 2,
            )

    def _joonista_takistused(self):
        """
        MODIFIKATSIOON 2: Joonista takistused (hallid ruudud).
        Kõrgem tase = rohkem takistusi ekraanil.
        """
        for x, y in self.takistused:
            ekraani_x = x * PLOKI_SUURUS
            ekraani_y = y * PLOKI_SUURUS + PANEEL_KÕRGUS
            # Välisraam
            pygame.draw.rect(
                self.ekraan, HALL,
                (ekraani_x, ekraani_y, PLOKI_SUURUS, PLOKI_SUURUS),
            )
            # Sisemine tumem osa (3D efekt)
            pygame.draw.rect(
                self.ekraan, TUME_HALL,
                (ekraani_x + 3, ekraani_y + 3, PLOKI_SUURUS - 6, PLOKI_SUURUS - 6),
            )
            # Rist sümbol takistuse peal
            pygame.draw.line(
                self.ekraan, (120, 120, 120),
                (ekraani_x + 4, ekraani_y + 4),
                (ekraani_x + PLOKI_SUURUS - 4, ekraani_y + PLOKI_SUURUS - 4), 2,
            )
            pygame.draw.line(
                self.ekraan, (120, 120, 120),
                (ekraani_x + PLOKI_SUURUS - 4, ekraani_y + 4),
                (ekraani_x + 4, ekraani_y + PLOKI_SUURUS - 4), 2,
            )

    def _joonista_mäng_läbi(self):
        """Joonista 'Mäng läbi' ekraan koos statistikaga."""
        # Poolläbipaistev kate
        kate = pygame.Surface((LAIUS, KÕRGUS), pygame.SRCALPHA)
        kate.fill((0, 0, 0, 160))
        self.ekraan.blit(kate, (0, 0))

        # Pealkiri
        t1 = self.font_tiitel.render("MÄNG LÄBI!", True, PUNANE)
        self.ekraan.blit(t1, (LAIUS // 2 - t1.get_width() // 2, 150))

        # Statistika
        read = [
            f"Lõpptulemus: {self.punktid} punkti",
            f"Jõudsid tasemeni: {self.tase}",
            f"Rekord: {self.parim_tulemus} punkti",
            "",
            "Vajuta  R  - mängida uuesti",
            "Vajuta  Q  - väljuda",
        ]
        värvid = [VALGE, TEKST_KOLLANE, KULLANE, VALGE, ROHELINE, (200, 100, 100)]
        for i, (rida, värv) in enumerate(zip(read, värvid)):
            t = self.font_kesk.render(rida, True, värv)
            self.ekraan.blit(t, (LAIUS // 2 - t.get_width() // 2, 270 + i * 45))

    def _joonista_paus(self):
        """Joonista peatamise ekraan."""
        kate = pygame.Surface((LAIUS, KÕRGUS), pygame.SRCALPHA)
        kate.fill((0, 0, 0, 120))
        self.ekraan.blit(kate, (0, 0))
        t = self.font_tiitel.render("PAUS", True, TEKST_KOLLANE)
        self.ekraan.blit(t, (LAIUS // 2 - t.get_width() // 2, KÕRGUS // 2 - 60))
        t2 = self.font_kesk.render("Vajuta P - jätkata", True, VALGE)
        self.ekraan.blit(t2, (LAIUS // 2 - t2.get_width() // 2, KÕRGUS // 2 + 20))

    def _joonista_alguseekraan(self):
        """Joonista avaekraan mängu alustamisel."""
        self.ekraan.fill(SININE_TAUST)

        # Tähed taustal
        for täht in self.tähed:
            pygame.draw.circle(
                self.ekraan, (150, 150, 200),
                (int(täht["x"]), int(täht["y"])),
                max(1, int(täht["suurus"] * 0.7)),
            )

        # Pealkiri - ainult "Ussi Mäng", ilma emojita ja subtiitlita
        t1 = self.font_tiitel.render("Ussi Mang", True, ROHELINE)
        self.ekraan.blit(t1, (LAIUS // 2 - t1.get_width() // 2, 90))

        # Eraldajoon pealkirja all
        pygame.draw.line(self.ekraan, ROHELINE,
                         (LAIUS // 2 - 200, 175), (LAIUS // 2 + 200, 175), 2)

        # Klahvide juhised - joondatud tabelina
        # Vasak veerg (klahv) ja parem veerg (kirjeldus) fikseeritud x-positsiooniga
        t_juhe = self.font_kesk.render("Klahvid:", True, TEKST_KOLLANE)
        self.ekraan.blit(t_juhe, (LAIUS // 2 - t_juhe.get_width() // 2, 195))

        juhised = [
            ("Nooled / WASD", "liikumine"),
            ("P",                   "paus / jatkata"),
            ("ESC / Q",             "valjuda"),
        ]
        klahv_x   = 180   # klahvi teksti algus
        kir_x     = 430   # kirjelduse teksti algus
        y         = 235
        for klahv, kirjeldus in juhised:
            tk = self.font_kesk.render(klahv, True, TEKST_KOLLANE)
            kk = self.font_kesk.render("- " + kirjeldus, True, VALGE)
            self.ekraan.blit(tk, (klahv_x, y))
            self.ekraan.blit(kk, (kir_x, y))
            y += 38

        # Eraldajoon
        pygame.draw.line(self.ekraan, (40, 80, 40),
                         (LAIUS // 2 - 250, y + 5), (LAIUS // 2 + 250, y + 5), 1)

        # Modifikatsioonide nimekiri - ilma emojita (fondid ei toeta neid)
        t3 = self.font_kesk.render("Mangu eriparad:", True, KULLANE)
        self.ekraan.blit(t3, (LAIUS // 2 - t3.get_width() // 2, y + 18))
        eripärad = [
            "Tasemed  - mäng kiireneb iga 5 punktiga",
            "Takistused - rohkem seinu kõrgematel tasemetel",
            "Kuldõun  - +3 punkti, aeglustab mängu",
            "3 elu    - ole ettevaatlik!",
            "Animeeritud taust - tähistaevas muutub tasemega",
        ]
        for i, rida in enumerate(eripärad):
            t = self.font_väike.render(rida, True, (180, 220, 255))
            self.ekraan.blit(t, (LAIUS // 2 - t.get_width() // 2, y + 55 + i * 26))

        # Vilkuv "alusta" nupp allosas
        t4 = self.font_suur.render("Vajuta TUHIK - alustada!", True, ROHELINE)
        t4_x = LAIUS // 2 - t4.get_width() // 2
        t4_r = pygame.Rect(t4_x - 10, 597, t4.get_width() + 20, t4.get_height() + 10)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            pygame.draw.rect(self.ekraan, (0, 80, 0), t4_r, border_radius=8)
            self.ekraan.blit(t4, (t4_x, 602))

        pygame.display.flip()

    # ── Peamine mängutsükkel ──────────────────────────────

    def käivita(self):
        """
        Peamine mängutsükkel.
        Haldab: sündmused, loogika uuendamine, joonistamine, FPS.
        """
        # ── Avaekraan ─────────────────────────────────────
        ootab = True
        while ootab:
            self._joonista_alguseekraan()
            for sündmus in pygame.event.get():
                if sündmus.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if sündmus.type == pygame.KEYDOWN:
                    if sündmus.key in (pygame.K_SPACE, pygame.K_RETURN):
                        ootab = False   # alusta mäng
                    if sündmus.key in (pygame.K_q, pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
            self.kell.tick(30)

        # ── Põhimängu tsükkel ─────────────────────────────
        while True:
            # Sündmuste töötlemine
            for sündmus in pygame.event.get():
                if sündmus.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if sündmus.type == pygame.KEYDOWN:
                    # Välju (Q või ESC klahviga)
                    if sündmus.key in (pygame.K_q, pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()

                    # Paus (MODIFIKATSIOON 4 - paus säilitab eluolek)
                    if sündmus.key == pygame.K_p:
                        self.paus = not self.paus

                    # Mäng läbi - uuesti alustamine
                    if not self.mäng_käib and sündmus.key == pygame.K_r:
                        self._alusta_uus_mäng()

                    # Liikumisklahvid (nooleklahvid ja WASD)
                    if self.mäng_käib and not self.paus and not self.surnud:
                        if sündmus.key in (pygame.K_UP, pygame.K_w):
                            if self.suund != ALLA:     # ei saa otse tagasi pöörduda
                                self.järgmine_suund = ÜLES
                        elif sündmus.key in (pygame.K_DOWN, pygame.K_s):
                            if self.suund != ÜLES:
                                self.järgmine_suund = ALLA
                        elif sündmus.key in (pygame.K_LEFT, pygame.K_a):
                            if self.suund != PAREMALE:
                                self.järgmine_suund = VASAKULE
                        elif sündmus.key in (pygame.K_RIGHT, pygame.K_d):
                            if self.suund != VASAKULE:
                                self.järgmine_suund = PAREMALE

            # ── Loogika uuendamine ────────────────────────
            if self.mäng_käib and not self.paus:
                self._liigu()

            # ── Joonistamine ──────────────────────────────
            # MODIFIKATSIOON 5: Animeeritud taust
            self._joonista_animeeritud_taust()

            # Mänguala raam
            pygame.draw.rect(
                self.ekraan, (0, 100, 30),
                (0, PANEEL_KÕRGUS, LAIUS, KÕRGUS - PANEEL_KÕRGUS), 2,
            )

            # Mängu elemendid
            self._joonista_takistused()   # MODIFIKATSIOON 2
            self._joonista_toit()         # MODIFIKATSIOON 3
            self._joonista_uss()          # MODIFIKATSIOON 4 (vilkumine surma korral)
            self._joonista_infopaneel()   # MODIFIKATSIOON 1 (tase) + 4 (elud)

            # Ekraani katted
            if not self.mäng_käib:
                self._joonista_mäng_läbi()
            elif self.paus:
                self._joonista_paus()

            pygame.display.flip()   # uuenda ekraan

            # ── FPS kontroll ──────────────────────────────
            # MODIFIKATSIOON 3: aeglustus vähendab kiirust pooleks
            tegelik_kiirus = self.kiirus
            if self.aeglustus_loendur > 0:
                tegelik_kiirus = max(ALGKIIRUS // 2, self.kiirus // 2)
            self.kell.tick(tegelik_kiirus)


# ── Programmi sisendpunkt ─────────────────────────────────
if __name__ == "__main__":
    mäng = Ussimaang()
    mäng.käivita()
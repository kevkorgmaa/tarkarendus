import pygame   # mängumootor
import random   # juhuslike positsioonide genereerimiseks
import sys      # programmi lõpetamiseks
import os       # failitee kontrollimiseks (tulemuste salvestus)
from collections import deque  # sisendijärjekord kiireks reageerimiseks (MOD-1)

# -----------------------------------------------------------------------------
#  KONSTANDID
# -----------------------------------------------------------------------------
RUUDUSTIKU_LAIUS  = 30          # ruutude arv horisontaalselt
RUUDUSTIKU_KÕRGUS = 30          # ruutude arv vertikaalselt
RUUDU_SUURUS      = 20          # ühe ruudu pikslite arv
EKRAANI_LAIUS     = RUUDUSTIKU_LAIUS  * RUUDU_SUURUS   # 600 px
EKRAANI_KÕRGUS    = RUUDUSTIKU_KÕRGUS * RUUDU_SUURUS   # 600 px

# Värvid (RGB)
MUST        = (0,   0,   0)
VALGE       = (255, 255, 255)
TAUST       = (15,  20,  30)    # tume sinine taust
RUUDUSTIK   = (25,  30,  45)    # ruudustiku joonte värv
PUNANE      = (220,  40,  40)   # tavaõuna värv
KOLLANE     = (240, 200,  30)   # mürgitatud õuna värv (MOD-2)
PRUUN       = (100,  60,  10)   # õuna varre värv
HALL        = (120, 120, 130)   # kivi värv (MOD-4)
HALL_TUME   = (70,   70,  80)   # kivi varju värv

# Tulemuste faili asukoht (salvestatakse skriptiga samasse kausta)
TULEMUSTE_FAIL = os.path.join(os.path.dirname(__file__), "tulemused.txt")

# Raskusastme kiirused (kaadrit sekundis)
KIIRUSED = {
    pygame.K_1: 8,    # kerge
    pygame.K_2: 12,   # keskmine
    pygame.K_3: 16,   # raske
    pygame.K_4: 20,   # äärmuslik
}

# Raskusastme nimed kuvamiseks
RASKUS_NIMED = {
    pygame.K_1: "KERGE",
    pygame.K_2: "KESKMINE",
    pygame.K_3: "RASKE",
    pygame.K_4: "ÄÄRMUSLIK",
}


# =============================================================================
#  KLASS: Õun  (alusversioon: pythonspot OOP-stiil, MOD-2 mürgiga laiendatud)
# =============================================================================
class Õun:
    """Esindab ühte õuna mänguväljal. Kaks tüüpi: tavaline ja mürgitatud."""

    def __init__(self, uss: list, takistused: set, mürgitatud: bool = False):
        self.mürgitatud = mürgitatud   # kas tegu on mürgitatud õunaga?
        self.pos = self._aseta(uss, takistused)  # vali juhuslik vaba positsioon
        self.pulsi_nurk = 0.0          # animatsiooni nurk (MOD-5)

    def _aseta(self, uss: list, takistused: set) -> pygame.Vector2:
        """Leia juhuslik positsioon, mis ei kattu ussiga ega takistustega."""
        while True:
            p = pygame.Vector2(
                random.randrange(RUUDUSTIKU_LAIUS),
                random.randrange(RUUDUSTIKU_KÕRGUS)
            )
            # Kontrolli, et uus positsioon on vaba
            if p not in uss and (int(p.x), int(p.y)) not in takistused:
                return p

    def taasilmu(self, uss: list, takistused: set):
        """Tekita uus positsioon pärast söömist."""
        self.pos = self._aseta(uss, takistused)

    def uuenda(self):
        """Uuenda pulsi-animatsiooni nurka iga kaadriga (MOD-5)."""
        self.pulsi_nurk = (self.pulsi_nurk + 0.15) % (2 * 3.14159)

    def joonista(self, pind: pygame.Surface):
        """Joonista õun ekraanile. Mürgitatud õun on kollane, tavaline punane."""
        import math
        # Pulsi-efekt: raadius muutub ±2 px sinusfunktsiooni järgi (MOD-5)
        pulsi = math.sin(self.pulsi_nurk) * 2
        x = int(self.pos.x) * RUUDU_SUURUS
        y = int(self.pos.y) * RUUDU_SUURUS
        cx = x + RUUDU_SUURUS // 2
        cy = y + RUUDU_SUURUS // 2
        r  = int(RUUDU_SUURUS // 2 - 1 + pulsi)  # pulseeriv raadius

        # Põhivärv sõltub tüübist
        põhivärv  = KOLLANE if self.mürgitatud else PUNANE
        sära_värv = (255, 255, 150) if self.mürgitatud else (255, 140, 140)

        pygame.draw.circle(pind, põhivärv,  (cx, cy), max(r, 3))
        pygame.draw.rect(  pind, PRUUN,     (cx - 1, y + 1, 3, r // 2))       # vars
        pygame.draw.circle(pind, sära_värv, (cx - 2, cy - 3), max(r // 4, 1)) # sära


# =============================================================================
#  TULEMUSTE TABEL  (MOD-3)
# =============================================================================

def loe_tulemused() -> list:
    """Loe kõrgeimad tulemused failist. Tagastab [(skoor, raskus), ...] järjestikku."""
    if not os.path.exists(TULEMUSTE_FAIL):
        return []
    tulemused = []
    try:
        with open(TULEMUSTE_FAIL, "r", encoding="utf-8") as f:
            for rida in f:
                osad = rida.strip().split("|")
                if len(osad) == 2:
                    tulemused.append((int(osad[0]), osad[1]))
    except (ValueError, IOError):
        pass  # vigane fail – ignoreeri
    return tulemused


def salvesta_tulemus(skoor: int, raskus: str):
    """Lisa uus tulemus faili, hoia top-5 järjestatuna."""
    tulemused = loe_tulemused()
    tulemused.append((skoor, raskus))
    tulemused.sort(key=lambda x: x[0], reverse=True)  # sorteeri kahaneva skoori järgi
    tulemused = tulemused[:5]                           # hoia ainult top-5
    try:
        with open(TULEMUSTE_FAIL, "w", encoding="utf-8") as f:
            for skoor_rida, raskus_rida in tulemused:
                f.write(f"{skoor_rida}|{raskus_rida}\n")
    except IOError:
        pass  # failikirjutuse viga – ignoreeri vaikselt


# =============================================================================
#  TAKISTUSTE GENEREERIMINE  (MOD-4)
# =============================================================================

def genereeri_takistused(raskus_klahv: int, uss: list) -> set:
    """
    Genereeri kivide koordinaatide hulk vastavalt raskusastmele.
    Kerge/keskmine = 0 kivi, raske = 8 kivi, äärmuslik = 16 kivi.
    """
    arv = {pygame.K_1: 0, pygame.K_2: 0, pygame.K_3: 8, pygame.K_4: 16}.get(raskus_klahv, 0)
    kivid: set = set()
    # Ussi algpositsioon on (W//2, H//2) – jäta selle ümber turvaruum
    keelatud = {(int(s.x), int(s.y)) for s in uss}
    keelatud |= {(int(s.x) + dx, int(s.y) + dy)
                 for s in uss
                 for dx in range(-3, 4)
                 for dy in range(-3, 4)}  # 7×7 turvaala ussi ümber

    while len(kivid) < arv:
        x = random.randrange(RUUDUSTIKU_LAIUS)
        y = random.randrange(RUUDUSTIKU_KÕRGUS)
        if (x, y) not in keelatud:
            kivid.add((x, y))
    return kivid


# =============================================================================
#  JOONISTUSFUNKTSIOONID
# =============================================================================

def joonista_ruudustik(pind: pygame.Surface):
    """Joonista taustruudustik (õhukesed jooned)."""
    for x in range(0, EKRAANI_LAIUS, RUUDU_SUURUS):
        pygame.draw.line(pind, RUUDUSTIK, (x, 0), (x, EKRAANI_KÕRGUS))
    for y in range(0, EKRAANI_KÕRGUS, RUUDU_SUURUS):
        pygame.draw.line(pind, RUUDUSTIK, (0, y), (EKRAANI_LAIUS, y))


def joonista_uss(pind: pygame.Surface, uss: list, vel: pygame.Vector2, font: pygame.font.Font):
    """
    Joonista uss – saba tumerohelisest pärani heledamaks (gradijent).
    Pea peal on silmad, mis vaatavad liikumissuunas (allikas: kood 2).
    """
    pikkus = len(uss)
    for i, ruut in enumerate(uss):
        # i=0 on saba (vanim), i=pikkus-1 on pea (uusim)
        x = int(ruut.x) * RUUDU_SUURUS
        y = int(ruut.y) * RUUDU_SUURUS
        on_pea = (i == pikkus - 1)

        if on_pea:
            # Pea: heleroheline täisruut
            pygame.draw.rect(pind, (60, 220, 80), (x, y, RUUDU_SUURUS, RUUDU_SUURUS))
            # Silmad liikumissuunas
            e = RUUDU_SUURUS // 5
            if   vel.y == -1:  # üles
                silmad = [(x + e, y + e), (x + RUUDU_SUURUS - 2*e, y + e)]
            elif vel.y ==  1:  # alla
                silmad = [(x + e, y + RUUDU_SUURUS - 2*e), (x + RUUDU_SUURUS - 2*e, y + RUUDU_SUURUS - 2*e)]
            elif vel.x == -1:  # vasakule
                silmad = [(x + e, y + e), (x + e, y + RUUDU_SUURUS - 2*e)]
            else:              # paremale (vaikimisi)
                silmad = [(x + RUUDU_SUURUS - 2*e, y + e), (x + RUUDU_SUURUS - 2*e, y + RUUDU_SUURUS - 2*e)]
            for sx, sy in silmad:
                pygame.draw.circle(pind, MUST, (sx, sy), e)
        else:
            # Keha: gradijent sabast (tume) pea poole (hele)
            heledus = max(70, 170 - (pikkus - 1 - i) * 3)
            värv = (0, heledus, 0)
            pygame.draw.rect(pind, värv, (x + 1, y + 1, RUUDU_SUURUS - 2, RUUDU_SUURUS - 2), border_radius=3)


def joonista_takistused(pind: pygame.Surface, kivid: set):
    """Joonista kivid (takistused) hallidena varjuga (MOD-4)."""
    for (x, y) in kivid:
        px = x * RUUDU_SUURUS
        py = y * RUUDU_SUURUS
        # Vari (tume)
        pygame.draw.rect(pind, HALL_TUME, (px + 2, py + 2, RUUDU_SUURUS, RUUDU_SUURUS))
        # Kivi keha
        pygame.draw.rect(pind, HALL,      (px,     py,     RUUDU_SUURUS, RUUDU_SUURUS))
        # Kivi tekstuur (heledamad joonejupid)
        pygame.draw.line(pind, (160, 160, 170), (px + 3, py + 3), (px + 10, py + 3), 1)
        pygame.draw.line(pind, (160, 160, 170), (px + 3, py + 3), (px + 3,  py + 10), 1)


def joonista_skoor(pind: pygame.Surface, skoor: int, font: pygame.font.Font):
    """Kuva skoor ekraani ülemises vasakus nurgas."""
    tekst = font.render(f"Pisteid: {skoor}", True, VALGE)
    pind.blit(tekst, (10, 8))


def joonista_flash(pind: pygame.Surface, flash_alpha: int):
    """
    Joonista ekraanile valge läbipaistev kiire (flash-efekt) õuna söömisel (MOD-5).
    flash_alpha väheneb iga kaadriga, kuni efekt kaob.
    """
    if flash_alpha > 0:
        overlay = pygame.Surface((EKRAANI_LAIUS, EKRAANI_KÕRGUS), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, flash_alpha))
        pind.blit(overlay, (0, 0))


def joonista_algusekraan(pind: pygame.Surface, big_font, small_font, tulemused: list):
    """Kuva peamenüü raskusastme valikuga ja kõrgeimate tulemustega (MOD-3)."""
    pind.fill(TAUST)

    # Pealkiri
    pealkiri = big_font.render("Snake", True, (60, 220, 80))
    pind.blit(pealkiri, (EKRAANI_LAIUS // 2 - pealkiri.get_width() // 2, 60))

    # Raskusastme valik
    read = [
        "Vali raskusaste:",
        "  1 – Kerge      (aeglane, ilma kivideta)",
        "  2 – Keskmine   (keskmise kiirus)",
        "  3 – Raske      (kiire + 8 kivi)",
        "  4 – Äärmuslik  (väga kiire + 16 kivi)",
        "",
        "TÜHIK – paus  |  ESC – välju",
    ]
    for i, rida in enumerate(read):
        värv = (200, 200, 200) if i == 0 else VALGE
        tekst = small_font.render(rida, True, värv)
        pind.blit(tekst, (EKRAANI_LAIUS // 2 - 160, 160 + i * 28))

    # Kõrgeimate tulemuste tabel (MOD-3)
    if tulemused:
        tiitel = small_font.render("TOP-5 TULEMUSED:", True, (255, 220, 60))
        pind.blit(tiitel, (EKRAANI_LAIUS // 2 - 80, 380))
        for j, (sk, rk) in enumerate(tulemused[:5]):
            rida_tekst = small_font.render(f"  {j+1}. {sk} pt  [{rk}]", True, VALGE)
            pind.blit(rida_tekst, (EKRAANI_LAIUS // 2 - 80, 405 + j * 24))


def joonista_mang_labi(pind: pygame.Surface, skoor: int, on_rekord: bool, big_font, small_font):
    """Kuva 'mäng läbi' ülekate koos tulemuse ja juhisega (MOD-3 rekord)."""
    overlay = pygame.Surface((EKRAANI_LAIUS, EKRAANI_KÕRGUS), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    pind.blit(overlay, (0, 0))

    tekst1 = big_font.render("MÄNG LÄBI", True, (220, 60, 60))
    tekst2 = small_font.render(f"Tulemus: {skoor} punkti", True, VALGE)
    tekst3 = small_font.render("Vajuta  R  – uuesti  |  ESC – välju", True, VALGE)
    pind.blit(tekst1, (EKRAANI_LAIUS // 2 - tekst1.get_width() // 2, EKRAANI_KÕRGUS // 2 - 60))
    pind.blit(tekst2, (EKRAANI_LAIUS // 2 - tekst2.get_width() // 2, EKRAANI_KÕRGUS // 2))
    pind.blit(tekst3, (EKRAANI_LAIUS // 2 - tekst3.get_width() // 2, EKRAANI_KÕRGUS // 2 + 34))

    # Rekorditeade
    if on_rekord:
        rek = small_font.render("🏆 UUS REKORD!", True, (255, 220, 60))
        pind.blit(rek, (EKRAANI_LAIUS // 2 - rek.get_width() // 2, EKRAANI_KÕRGUS // 2 + 68))


def joonista_paus(pind: pygame.Surface, font: pygame.font.Font):
    """Kuva pausiteade ekraani keskel."""
    tekst = font.render("PAUS  –  vajuta TÜHIK jätkamiseks", True, (255, 220, 60))
    pind.blit(tekst, (EKRAANI_LAIUS // 2 - tekst.get_width() // 2, EKRAANI_KÕRGUS // 2))


# =============================================================================
#  MÄNGU LÄHTESTAMINE
# =============================================================================

def lähtesta_mäng(raskus_klahv: int):
    """
    Loo uus mänguolek: uss keskel, õun juhuslikul kohal, takistused raskuse järgi.
    Tagastab: (uss, vel, õun, mürgitatud_õun, takistused, skoor, kasv)
    """
    uss  = [pygame.Vector2(RUUDUSTIKU_LAIUS // 2, RUUDUSTIKU_KÕRGUS // 2)]
    vel  = pygame.Vector2(1, 0)          # algsuund: paremale
    kivid = genereeri_takistused(raskus_klahv, uss)   # MOD-4
    õun  = Õun(uss, kivid, mürgitatud=False)
    # Mürgitatud õun tekib ainult raskusastmel 2+ (MOD-2)
    mürgitatud_õun = Õun(uss, kivid, mürgitatud=True) if raskus_klahv in (pygame.K_2, pygame.K_3, pygame.K_4) else None
    skoor = 0
    kasv  = 3   # algul kasvab uss 3 ruutu
    return uss, vel, õun, mürgitatud_õun, kivid, skoor, kasv


# =============================================================================
#  PEAFUNKTSIOON
# =============================================================================

def main():
    pygame.init()
    ekraan   = pygame.display.set_mode((EKRAANI_LAIUS, EKRAANI_KÕRGUS))
    pygame.display.set_caption("Snake 🐍")
    kell     = pygame.time.Clock()

    # Fondid
    tavaFont = pygame.font.SysFont("Arial", 22)
    suurFont = pygame.font.SysFont("Arial", 42, bold=True)
    väikeFont = pygame.font.SysFont("Arial", 18)

    # Mänguseis
    mäng_alustatud = False   # kas mängija on raskusastme valinud?
    mäng_läbi      = False   # kas uss on surnud?
    paus            = False   # kas mäng on pausis?
    kiirus          = 12      # vaikimisi kiirus (kaadrit/sek)
    raskus_klahv    = pygame.K_2  # vaikimisi raskusaste

    # Algne mänguolek
    uss, vel, õun, mürgitatud_õun, kivid, skoor, kasv = lähtesta_mäng(raskus_klahv)

    # MOD-1: sisendijärjekord – kogub klahvivajutused, et uss reageeriks koheselt
    sisend_järjekord: deque = deque(maxlen=2)
    ootel_vel = vel.copy()   # järgmine suund, rakendatakse järgmisel sammul

    # MOD-5: flash-efekti läbipaistvus (0 = nähtamatu)
    flash_alpha = 0

    on_rekord    = False   # kas saadi uus rekord? (näidatakse mäng-läbi ekraanil)
    tulemused    = loe_tulemused()  # lae olemasolevad tulemused failist

    # Suunajuhtimine: klahv → Vector2
    SUUNAD = {
        pygame.K_RIGHT: pygame.Vector2( 1,  0),
        pygame.K_LEFT:  pygame.Vector2(-1,  0),
        pygame.K_UP:    pygame.Vector2( 0, -1),
        pygame.K_DOWN:  pygame.Vector2( 0,  1),
    }

    # ─── Peaahel ─────────────────────────────────────────────────────────────
    while True:

        # ── Sündmuste töötlus ─────────────────────────────────────────────────
        for sündmus in pygame.event.get():
            if sündmus.type == pygame.QUIT:
                # Kasutaja sulges akna
                pygame.quit()
                sys.exit()

            elif sündmus.type == pygame.KEYDOWN:

                # MOD-1: ESC lõpetab mängu igal hetkel
                if sündmus.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif not mäng_alustatud:
                    # Algusekraanil: vali raskusaste numbriklahviga
                    if sündmus.key in KIIRUSED:
                        kiirus        = KIIRUSED[sündmus.key]
                        raskus_klahv  = sündmus.key
                        uss, vel, õun, mürgitatud_õun, kivid, skoor, kasv = lähtesta_mäng(raskus_klahv)
                        sisend_järjekord.clear()
                        ootel_vel      = vel.copy()
                        flash_alpha    = 0
                        on_rekord      = False
                        mäng_alustatud = True
                        mäng_läbi      = False
                        paus           = False

                elif mäng_läbi:
                    # Mäng läbi ekraanil: R alustab uuesti
                    if sündmus.key == pygame.K_r:
                        uss, vel, õun, mürgitatud_õun, kivid, skoor, kasv = lähtesta_mäng(raskus_klahv)
                        sisend_järjekord.clear()
                        ootel_vel      = vel.copy()
                        flash_alpha    = 0
                        on_rekord      = False
                        mäng_alustatud = False  # mine tagasi menüüsse raskuse valimiseks
                        mäng_läbi      = False

                else:
                    # Mängu ajal: suund ja paus
                    if sündmus.key == pygame.K_SPACE:
                        paus = not paus   # lülita paus sisse/välja

                    elif sündmus.key in SUUNAD:
                        # MOD-1: lisa sisendijärjekorda, ära blokeeri kohe
                        uus_vel = SUUNAD[sündmus.key]
                        # Väldi pöördumist vastassuunda
                        viimane = sisend_järjekord[-1] if sisend_järjekord else ootel_vel
                        if uus_vel + viimane != pygame.Vector2(0, 0):
                            sisend_järjekord.append(uus_vel)

        # ── Joonistamine ──────────────────────────────────────────────────────
        if not mäng_alustatud:
            # Kuva algusekraan
            tulemused = loe_tulemused()   # värskenda tulemuste tabelit
            joonista_algusekraan(ekraan, suurFont, väikeFont, tulemused)
            pygame.display.flip()
            kell.tick(30)
            continue   # hüppa ülejäänud tsükli koodist mööda

        # Joonista mängupind
        ekraan.fill(TAUST)
        joonista_ruudustik(ekraan)
        joonista_takistused(ekraan, kivid)   # MOD-4: joonista kivid
        õun.uuenda()                          # MOD-5: uuenda pulsi-animatsiooni
        õun.joonista(ekraan)
        if mürgitatud_õun:
            mürgitatud_õun.uuenda()           # MOD-5: uuenda mürgitatud õuna animatsiooni
            mürgitatud_õun.joonista(ekraan)
        joonista_uss(ekraan, uss, vel, tavaFont)
        joonista_skoor(ekraan, skoor, tavaFont)
        joonista_flash(ekraan, flash_alpha)   # MOD-5: flash-efekt

        # Vähenda flash-alpha iga kaadriga
        if flash_alpha > 0:
            flash_alpha = max(0, flash_alpha - 15)

        if mäng_läbi:
            joonista_mang_labi(ekraan, skoor, on_rekord, suurFont, väikeFont)
            pygame.display.flip()
            kell.tick(30)
            continue

        if paus:
            joonista_paus(ekraan, tavaFont)
            pygame.display.flip()
            kell.tick(10)
            continue

        # ── Mängu loogika uuendamine ──────────────────────────────────────────

        # MOD-1: rakenda järgmine suund järjekorrast (optimiseeritud sisend)
        if sisend_järjekord:
            ootel_vel = sisend_järjekord.popleft()
        vel = ootel_vel

        # Arvuta uue pea positsioon
        # Allikas: kood 3 – Vector2 + läbivad seinad (wrap-around)
        uus_pea = uss[-1] + vel
        uus_pea.x %= RUUDUSTIKU_LAIUS   # läbi parema seina → vasakule
        uus_pea.y %= RUUDUSTIKU_KÕRGUS  # läbi alumise seina → üles

        # Kontrolli kokkupõrkeid
        # 1) Ussiga iseendaga
        if uus_pea in uss:
            mäng_läbi = True
            on_rekord = _salvesta_ja_kontroll(skoor, RASKUS_NIMED.get(raskus_klahv, "?"))
            continue

        # 2) Kividega (MOD-4)
        if (int(uus_pea.x), int(uus_pea.y)) in kivid:
            mäng_läbi = True
            on_rekord = _salvesta_ja_kontroll(skoor, RASKUS_NIMED.get(raskus_klahv, "?"))
            continue

        # Liigu edasi: lisa uus pea
        uss.append(uus_pea)

        # Kontrolli, kas sõid tavalist õuna
        if uus_pea == õun.pos:
            skoor += 1
            kasv  += 1
            flash_alpha = 80                        # käivita flash-efekt (MOD-5)
            õun.taasilmu(uss, kivid)
            # Suurenda kiirust iga 5 õuna järel
            if skoor % 5 == 0:
                kiirus = min(kiirus + 1, 30)

        # Kontrolli, kas sõid mürgitatud õuna (MOD-2)
        elif mürgitatud_õun and uus_pea == mürgitatud_õun.pos:
            mürgitatud_õun.taasilmu(uss, kivid)
            # Lühenda usse – eemalda saba, kui uss pole liiga lühike
            if len(uss) > 2:
                uss.pop(0)   # eemalda saba (ekstra, lisaks tavalisele eemaldusele)
            flash_alpha = 60  # väiksem flash kollaka tooniga

        # Eemalda saba, kui pole vaja kasvada
        if kasv > 0:
            kasv -= 1
        else:
            uss.pop(0)

        pygame.display.flip()
        kell.tick(kiirus)


def _salvesta_ja_kontroll(skoor: int, raskus: str) -> bool:
    """
    Salvesta tulemus ja kontrolli, kas see on uus top-5 rekord.
    Tagastab True, kui tulemus mahtus top-5 hulka.
    """
    vanad = loe_tulemused()
    min_vana = vanad[-1][0] if len(vanad) >= 5 else -1
    salvesta_tulemus(skoor, raskus)
    return skoor > min_vana or len(vanad) < 5


# =============================================================================
#  KÄIVITAMINE
# =============================================================================
if __name__ == "__main__":
    main()
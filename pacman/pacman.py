# =============================================================================
#  PACMAN MÄNG – Kolmest koodist ühendatud versioon
#
#  Allikad:
#    Kood 1: sprite-põhine mäng (Menu, draw_environment, Slime AI, Player)
#    Kood 2: OOP mäng (Entity/Pacman/Ghost/Blinky/Pinky/Inky/Clyde, GRID, pildid)
#    Kood 3: lihtne mäng (lives süsteem, positsiooni reset)
#
#  Kasutatud elemendid:
#    Kood 1 → Menu klass + draw_environment (sinijooned) + Slime AI
#    Kood 2 → Entity/Pacman/Ghost klassid, GRID kaart, pildifailid, sihtimisloogika
#    Kood 3 → lives süsteem (mitu elu, positsiooni reset kaotamisel)
# =============================================================================

import pygame
import sys
import math
import random

# -----------------------------------------------------------------------------
#  PYGAME INITSIALISEERIMINE
# -----------------------------------------------------------------------------
pygame.init()

# -----------------------------------------------------------------------------
#  KONSTANDID
# -----------------------------------------------------------------------------
SCREEN_WIDTH  = 900    # ekraani laius pikslites
SCREEN_HEIGHT = 900    # ekraani kõrgus pikslites
EXTRA_HEIGHT  = 50     # lisaruum UI elementide jaoks (skoor, elud)
FPS           = 60     # kaadrid sekundis

# Värvid
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
BLUE   = (0,   0,   255)
GREEN  = (0,   255, 0)
RED    = (255, 0,   0)
YELLOW = (255, 255, 0)

# Tähtede (punktide) värv
STAR_COLOR = (205, 205, 205)

# Pildifailide asukohad (kood 2 lähenemine)
PACMAN_IMG_PATH = "images/pacman.png"
RED_GHOST_PATH  = "images/red_ghost.png"
BLUE_GHOST_PATH = "images/blue_ghost.png"
ORANGE_GHOST_PATH = "images/orange_ghost.png"
PINK_GHOST_PATH = "images/pink_ghost.png"
MAP_IMG_PATH    = "images/pacman_map.jpeg"

# -----------------------------------------------------------------------------
#  PILTIDE LAADIMINE  (kood 2)
# -----------------------------------------------------------------------------
def laadi_pilt(path, suurus=(30, 30)):
    """Lae pilt failist ja skaleeri soovitud suurusele."""
    pilt = pygame.image.load(path)
    return pygame.transform.scale(pilt, suurus)

PACMAN_PILT  = laadi_pilt(PACMAN_IMG_PATH)
RED_PILT     = laadi_pilt(RED_GHOST_PATH)
BLUE_PILT    = laadi_pilt(BLUE_GHOST_PATH)
ORANGE_PILT  = laadi_pilt(ORANGE_GHOST_PATH)
PINK_PILT    = laadi_pilt(PINK_GHOST_PATH)
TAUST_PILT   = pygame.transform.scale(
    pygame.image.load(MAP_IMG_PATH), (SCREEN_WIDTH, SCREEN_HEIGHT)
)

# Fondid
VÄIKE_FONT = pygame.font.SysFont("monospace", 18)
SUUR_FONT  = pygame.font.SysFont("monospace", 30)

# -----------------------------------------------------------------------------
#  KAART  (kood 2 – GRID struktuur)
#  0 = sein, 1 = tavaline käik (täht), 2 = eriruut (käik ilma tähteta)
# -----------------------------------------------------------------------------
GRID = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0],
    [0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,2,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,2,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,2,2,2,2,2,2,2,2,2,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
    [2,2,2,2,2,2,1,2,2,2,0,0,0,0,0,0,0,0,2,2,2,1,2,2,2,2,2,2,2,2,2],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,2,2,2,2,2,2,2,2,2,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
    [0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0],
    [0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0],
    [0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

# -----------------------------------------------------------------------------
#  KOORDINAATIDE TEISENDUS  (kood 2)
# -----------------------------------------------------------------------------
def x_koord(ruudustiku_x: int) -> int:
    """Teisenda ruudustiku x-positsioon ekraani piksliteks."""
    return 32 * ruudustiku_x + 20

def y_koord(ruudustiku_y: int) -> int:
    """Teisenda ruudustiku y-positsioon ekraani piksliteks."""
    return int(28.9 * ruudustiku_y + 20)

def kaugus(a: tuple, b: tuple) -> float:
    """Arvuta Eukleidese kaugus kahe punkti vahel."""
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# -----------------------------------------------------------------------------
#  MENU KLASS  (kood 1 – Menu klass)
# -----------------------------------------------------------------------------
class Menu:
    """Menüü klass: kuvab valikud, käsitleb üles/alla navigeerimist."""
    olek = 0  # hetkel valitud menüükirje indeks

    def __init__(self, kirjed, font_värv=WHITE, valitu_värv=RED, font_suurus=60):
        self.font_värv   = font_värv
        self.valitu_värv = valitu_värv
        self.kirjed      = kirjed
        self.font        = pygame.font.Font(None, font_suurus)

    def kuva(self, ekraan):
        """Joonista menüükirjed ekraanile, valitud kirje on punane."""
        for i, kirje in enumerate(self.kirjed):
            värv = self.valitu_värv if self.olek == i else self.font_värv
            tekst = self.font.render(kirje, True, värv)
            laius  = tekst.get_width()
            kõrgus = tekst.get_height()
            posX = SCREEN_WIDTH  // 2 - laius // 2
            kokku_kõrgus = len(self.kirjed) * kõrgus
            posY = SCREEN_HEIGHT // 2 - kokku_kõrgus // 2 + i * kõrgus
            ekraan.blit(tekst, (posX, posY))

    def käsitle_sündmus(self, sündmus):
        """Uuenda valitud menüükirjet nooleklahvidega."""
        if sündmus.type == pygame.KEYDOWN:
            if sündmus.key == pygame.K_UP and self.olek > 0:
                self.olek -= 1
            elif sündmus.key == pygame.K_DOWN and self.olek < len(self.kirjed) - 1:
                self.olek += 1

# -----------------------------------------------------------------------------
#  KESKKONNA JOONISTAMINE  (kood 1 – draw_environment sinijooned)
# -----------------------------------------------------------------------------
def joonista_keskkond(ekraan):
    """
    Joonista käigud siniste joontena GRID põhjal (kood 1 lähenemine).
    Väärtus 1 = horisontaalne käik, väärtus 2 = vertikaalne käik.
    """
    for i, rida in enumerate(GRID):
        for j, ruut in enumerate(rida):
            if ruut == 1:
                # Horisontaalne käik – joonista ülemine ja alumine joon
                pygame.draw.line(ekraan, BLUE, [j*32, i*32],     [j*32+32, i*32],    2)
                pygame.draw.line(ekraan, BLUE, [j*32, i*32+29],  [j*32+32, i*32+29], 2)
            elif ruut == 2:
                # Vertikaalne käik – joonista vasak ja parem joon
                pygame.draw.line(ekraan, BLUE, [j*32,    i*32], [j*32,    i*32+29], 2)
                pygame.draw.line(ekraan, BLUE, [j*32+29, i*32], [j*32+29, i*32+29], 2)

# -----------------------------------------------------------------------------
#  ENTITEEDI BAASKLASS  (kood 2 – Entity klass)
# -----------------------------------------------------------------------------
class Entiteet:
    """
    Baasklass mängijale ja kummitustele.
    Haldab liikumist, suunda ja ekraanil kuvamist.
    """
    def __init__(self, x, y, pilt, kiirus=8):
        self.x      = x
        self.y      = y
        self.pilt   = pilt
        self.kiirus = kiirus
        self.liigub = False
        # järgmine suund: {praegune, järjekorras} – võimaldab suunda sujuvalt muuta
        self.järgmine_suund = {'praegune': (0, 0), 'järjekorras': (0, 0)}
        self.liigutuste_arv = 0

    def kuva(self, ekraan):
        """Joonista entiteet ekraanile."""
        ekraan.blit(self.pilt, (x_koord(self.x) - 15, y_koord(self.y) - 15))

    def liiguta(self, grid):
        """Uuenda entiteedi positsiooni vastavalt suunale ja gridile."""
        # Läbiv sein: vasakust servast välja → tuleb paremalt
        if self.x < -1:
            self.x = 28
        if self.x > 29:
            self.x = -1

        if not self.liigub:
            # Kontrolli järjekorras olevat suunda
            järjekorras = self.järgmine_suund['järjekorras']
            if grid[int(self.y) + järjekorras[1]][int(self.x) + järjekorras[0]] != 0:
                self.järgmine_suund['praegune'] = järjekorras

            # Alusta liikumist kui suund on vaba
            praegune = self.järgmine_suund['praegune']
            if grid[int(self.y) + praegune[1]][int(self.x) + praegune[0]] != 0:
                self.liigub = True
                self.liigutuste_arv = 0

        if self.liigub:
            dx, dy = self.järgmine_suund['praegune']
            self.x += dx / self.kiirus
            self.y += dy / self.kiirus
            self.x = round(self.x, 2)
            self.y = round(self.y, 2)
            self.liigutuste_arv += 1

            if self.liigutuste_arv == self.kiirus:
                # Liikumine lõpetatud – ümarda täisarvuks
                self.x = round(self.x)
                self.y = round(self.y)
                self.liigub = False

# -----------------------------------------------------------------------------
#  PACMAN KLASS  (kood 2 – Pacman klass + kood 3 – lives süsteem)
# -----------------------------------------------------------------------------
class Pacman(Entiteet):
    """
    Mängija klass.
    Kood 2: liikumine ja punktide kogumine.
    Kood 3: lives süsteem – kaotamisel reset, mitte kohene mäng läbi.
    """
    ALG_X = 13   # alguspositsioon x
    ALG_Y = 17   # alguspositsioon y
    MAX_ELUD = 3 # maksimaalne elude arv (kood 3)

    def __init__(self):
        super().__init__(self.ALG_X, self.ALG_Y, PACMAN_PILT, kiirus=8)
        self.punktid = 0
        self.elud    = self.MAX_ELUD  # kood 3: mitu elu

    def söö(self, tähted: list, võit_callback):
        """
        Kontrolli, kas Pacman on tähel — kui jah, eemalda täht ja lisa punkt.
        Kood 2 lähenemine tähtede haldusele.
        """
        if (self.x, self.y) in tähted:
            tähted.remove((self.x, self.y))
            self.punktid += 10
        if not tähted:
            võit_callback()

    def kaota_elu(self) -> bool:
        """
        Kood 3: kaota üks elu ja lähtesta positsioon.
        Tagastab True kui elud on otsas (mäng läbi).
        """
        self.elud -= 1
        if self.elud <= 0:
            return True   # mäng läbi
        # Lähtesta positsioon (kood 3)
        self.x = self.ALG_X
        self.y = self.ALG_Y
        self.liigub = False
        self.järgmine_suund = {'praegune': (0, 0), 'järjekorras': (0, 0)}
        return False

# -----------------------------------------------------------------------------
#  KUMMITUSE BAASKLASS  (kood 2 – Ghost klass)
# -----------------------------------------------------------------------------
class Kummitus(Entiteet):
    """Kummituse baasklass. Haldab sihtimist ja rünnaku kontrollimist."""

    def __init__(self, x, y, pilt, kiirus=10):
        super().__init__(x, y, pilt, kiirus)
        self.sihtmärk = (0, 0)

    def sihtimine(self, grid, pacman, mäng_läbi_callback):
        """
        Leia parim suund sihtmärgi poole liikumiseks (kood 2).
        Väldib kohest tagasipöördumist.
        """
        parim_suund = (0, 0)
        min_kaugus  = float("inf")
        self.järgmine_suund['järjekorras'] = (0, 0)

        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            uus_x = int(self.x) + dx
            uus_y = int(self.y) + dy
            # Kontrolli, et ruut pole sein ja pole vastassuund
            if grid[uus_y][uus_x] != 0:
                if (dx, dy) == tuple(-v for v in self.järgmine_suund['praegune']):
                    continue
                d = kaugus((uus_y, uus_x), self.sihtmärk)
                if d < min_kaugus:
                    min_kaugus  = d
                    parim_suund = (dx, dy)

        self.järgmine_suund['järjekorras'] = parim_suund
        self.liiguta(grid)
        self.kontrolli_rünnak(pacman, mäng_läbi_callback)

    def kontrolli_rünnak(self, pacman, mäng_läbi_callback):
        """Kui kummitus on Pacmanile piisavalt lähedal, käivita kaotus."""
        if kaugus((self.x, self.y), (pacman.x, pacman.y)) < 0.6:
            mäng_läbi_callback()

# -----------------------------------------------------------------------------
#  KONKREETSED KUMMITUSED  (kood 2 – Blinky/Pinky/Inky/Clyde)
# -----------------------------------------------------------------------------
class Blinky(Kummitus):
    """Punane kummitus – jälitab Pacmani otse."""
    def __init__(self):
        super().__init__(1, 28, RED_PILT)

    def uuenda_sihtmärk(self, pacman):
        self.sihtmärk = (pacman.y, pacman.x)

class Pinky(Kummitus):
    """Roosa kummitus – sihtib 4 sammu Pacmani ette."""
    def __init__(self):
        super().__init__(1, 1, PINK_PILT)

    def uuenda_sihtmärk(self, pacman):
        dx, dy = pacman.järgmine_suund['praegune']
        self.sihtmärk = (pacman.y + dy * 4, pacman.x + dx * 4)
        if pacman.järgmine_suund['praegune'][1] == -1:
            self.sihtmärk = (pacman.y - 4, pacman.x - 4)

class Inky(Kummitus):
    """Sinine kummitus – sihtib Blinkyt ja Pacmani kasutades vektori."""
    def __init__(self, blinky):
        super().__init__(26, 26, BLUE_PILT)
        self.blinky = blinky

    def uuenda_sihtmärk(self, pacman):
        dx, dy = pacman.järgmine_suund['praegune']
        kaks_ette = (pacman.y + dy * 2, pacman.x + dx * 2)
        vektor = (kaks_ette[0] - self.blinky.y, kaks_ette[1] - self.blinky.x)
        self.sihtmärk = (pacman.y + vektor[0], pacman.x + vektor[1])

class Clyde(Kummitus):
    """Oranž kummitus – jälitab Pacmani, aga põgeneb kui on liiga lähedal."""
    def __init__(self):
        super().__init__(26, 1, ORANGE_PILT)

    def uuenda_sihtmärk(self, pacman):
        self.sihtmärk = (pacman.y, pacman.x)
        if kaugus((self.x, self.y), (pacman.x, pacman.y)) < 8:
            self.sihtmärk = (29, 1)  # põgene nurka

# -----------------------------------------------------------------------------
#  SLIME AI  (kood 1 – Slime klass loogika, ilma pildita)
#  Kasutatakse lisavaenlasena, liigub juhuslikult ristmikul
# -----------------------------------------------------------------------------
class Slime:
    """
    Kood 1 Slime'i liikumisloogika: liigub juhuslikult,
    pöördub uude suunda ristmikel.
    """
    KIIRUS = 2  # liikumiskiirus ruutudes

    def __init__(self, x, y, dx, dy):
        self.x  = x    # positsioon ruudustikus
        self.y  = y
        self.dx = dx   # liikumissuund x
        self.dy = dy   # liikumissuund y

    def uuenda(self, grid):
        """Liigu edasi ja vali ristmikul juhuslik uus suund (kood 1 loogika)."""
        self.x += self.dx
        self.y += self.dy

        # Läbivad seinad
        if self.x < 0:   self.x = len(grid[0]) - 1
        if self.x >= len(grid[0]): self.x = 0
        if self.y < 0:   self.y = len(grid) - 1
        if self.y >= len(grid):    self.y = 0

        # Ristmikul: vali juhuslik suund (kood 1 loogika)
        if self._on_ristmik(grid):
            suund = random.choice(["vasak", "parem", "üles", "alla"])
            if suund == "vasak"  and self.dx == 0: self.dx, self.dy = -self.KIIRUS, 0
            elif suund == "parem" and self.dx == 0: self.dx, self.dy =  self.KIIRUS, 0
            elif suund == "üles"  and self.dy == 0: self.dx, self.dy = 0, -self.KIIRUS
            elif suund == "alla"  and self.dy == 0: self.dx, self.dy = 0,  self.KIIRUS

    def _on_ristmik(self, grid) -> bool:
        """Kontrolli, kas Slime asub ristmikul (kood 1 get_intersection_position loogika)."""
        x_ruut = int(self.x / 32)
        y_ruut = int(self.y / 29)
        if 0 <= y_ruut < len(grid) and 0 <= x_ruut < len(grid[0]):
            return grid[y_ruut][x_ruut] == 2
        return False

    def kuva(self, ekraan):
        """Joonista Slime rohelise ringina ekraanile."""
        pygame.draw.circle(ekraan, GREEN, (self.x, self.y), 8)

    def kontrolli_rünnak(self, pacman, mäng_läbi_callback):
        """Kui Slime puutub Pacmani, käivita kaotus."""
        px = x_koord(int(pacman.x))
        py = y_koord(int(pacman.y))
        if kaugus((self.x, self.y), (px, py)) < 20:
            mäng_läbi_callback()

# -----------------------------------------------------------------------------
#  TÄHTEDE INITSIALISEERIMINE  (kood 2)
# -----------------------------------------------------------------------------
def initsialiseeri_tähted() -> list:
    """Loo tähtede nimekiri GRID põhjal (väärtus 1 = täht)."""
    tähted = []
    for y, rida in enumerate(GRID):
        for x, väärtus in enumerate(rida):
            if väärtus == 1:
                tähted.append((x, y))
    return tähted

# -----------------------------------------------------------------------------
#  EKRAANI UUENDAMINE
# -----------------------------------------------------------------------------
def uuenda_ekraan(ekraan, tähted, pacman, kummitused, slimed):
    """Tühjenda ekraan ja joonista kõik mänguelemendid."""
    ekraan.fill(BLACK)
    ekraan.blit(TAUST_PILT, (0, 0))

    # Joonista käigud siniste joontena (kood 1)
    joonista_keskkond(ekraan)

    # Joonista tähted (punktid)
    for täht in tähted:
        pygame.draw.circle(ekraan, STAR_COLOR,
                           (x_koord(täht[0]), y_koord(täht[1])), 5)

    # Joonista kummitused ja pacman
    for k in kummitused:
        k.kuva(ekraan)
    for s in slimed:
        s.kuva(ekraan)
    pacman.kuva(ekraan)

    # Skoor ja elud (kood 3 – elud ekraanil)
    skoor_tekst = VÄIKE_FONT.render(f"Points: {pacman.punktid}", True, WHITE)
    elud_tekst  = VÄIKE_FONT.render(f"Lives: {pacman.elud}",    True, WHITE)
    ekraan.blit(skoor_tekst, (40,  SCREEN_HEIGHT + 15))
    ekraan.blit(elud_tekst,  (700, SCREEN_HEIGHT + 15))

    pygame.display.update()

# -----------------------------------------------------------------------------
#  TEADETE KUVAMINE
# -----------------------------------------------------------------------------
def kuva_teade(ekraan, sõnum: str):
    """Kuva teade (võit/kaotus) ekraani keskel."""
    pygame.draw.rect(ekraan, (100, 100, 200), (300, 315, 300, 200))
    tekst1 = SUUR_FONT.render(f"You {sõnum}!", True, WHITE)
    tekst2 = VÄIKE_FONT.render("Press SPACE to restart", True, WHITE)
    ekraan.blit(tekst1, (385, 370))
    ekraan.blit(tekst2, (330, 420))
    pygame.display.update()

def kuva_elu_kaotus(ekraan, elud: int):
    """Kuva teade elu kaotamisel (kood 3)."""
    overlay = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    ekraan.blit(overlay, (0, SCREEN_HEIGHT // 2 - 50))
    tekst = SUUR_FONT.render(f"Lost a life! Lives left: {elud}", True, RED)
    ekraan.blit(tekst, (SCREEN_WIDTH // 2 - tekst.get_width() // 2,
                        SCREEN_HEIGHT // 2 - tekst.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(1000)

# -----------------------------------------------------------------------------
#  MÄNGU LÕPP – oota SPACE klahvi
# -----------------------------------------------------------------------------
def mäng_läbi_ekraan(ekraan):
    """Oota SPACE klahvi, seejärel alusta uuesti."""
    while True:
        for sündmus in pygame.event.get():
            if sündmus.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif sündmus.type == pygame.KEYDOWN and sündmus.key == pygame.K_SPACE:
                mäng(ekraan)
                return

# -----------------------------------------------------------------------------
#  PEAMÄNGU FUNKTSIOON
# -----------------------------------------------------------------------------
def mäng(ekraan):
    """Käivita mängutsükkel: loo objektid, käivita peaahel."""
    tähted   = initsialiseeri_tähted()
    pacman   = Pacman()
    blinky   = Blinky()
    pinky    = Pinky()
    inky     = Inky(blinky)
    clyde    = Clyde()
    kummitused = [blinky, pinky, inky, clyde]

    # Kood 1: Slime'id lisavaenlastena, liiguvad juhuslikult
    slimed = [
        Slime(288, 96,  0,  2),
        Slime(544, 128, 0,  2),
        Slime(160, 64,  2,  0),
    ]

    mäng_lõppes = False   # kas mäng on lõppenud (võit/kaotus)?

    def kaotus():
        """Kood 3: kaota elu, lähtesta positsioon või lõpeta mäng."""
        nonlocal mäng_lõppes
        mäng_lõppes_täielikult = pacman.kaota_elu()
        if mäng_lõppes_täielikult:
            kuva_teade(ekraan, "Lost")
            mäng_lõppes = True
        else:
            kuva_elu_kaotus(ekraan, pacman.elud)

    def võit():
        """Kuva võidu teade."""
        nonlocal mäng_lõppes
        kuva_teade(ekraan, "Won")
        mäng_lõppes = True

    kell = pygame.time.Clock()

    while True:
        # Sündmuste töötlus
        for sündmus in pygame.event.get():
            if sündmus.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif sündmus.type == pygame.KEYDOWN:
                if sündmus.key == pygame.K_ESCAPE:
                    return   # tagasi menüüsse
                if not mäng_lõppes:
                    if sündmus.key == pygame.K_a:
                        pacman.järgmine_suund['järjekorras'] = (-1, 0)
                    elif sündmus.key == pygame.K_d:
                        pacman.järgmine_suund['järjekorras'] = (1, 0)
                    elif sündmus.key == pygame.K_w:
                        pacman.järgmine_suund['järjekorras'] = (0, -1)
                    elif sündmus.key == pygame.K_s:
                        pacman.järgmine_suund['järjekorras'] = (0, 1)
                elif sündmus.key == pygame.K_SPACE:
                    mäng(ekraan)
                    return

        if not mäng_lõppes:
            # Uuenda Pacmani ja kummituste liikumist
            pacman.liiguta(GRID)

            for k in kummitused:
                if isinstance(k, Blinky):   k.uuenda_sihtmärk(pacman)
                elif isinstance(k, Pinky):  k.uuenda_sihtmärk(pacman)
                elif isinstance(k, Inky):   k.uuenda_sihtmärk(pacman)
                elif isinstance(k, Clyde):  k.uuenda_sihtmärk(pacman)
                k.sihtimine(GRID, pacman, kaotus)

            # Slime'ide uuendamine (kood 1)
            for s in slimed:
                s.uuenda(GRID)
                s.kontrolli_rünnak(pacman, kaotus)

            # Söö täht ja kontrolli võitu
            pacman.söö(tähted, võit)

        uuenda_ekraan(ekraan, tähted, pacman, kummitused, slimed)
        kell.tick(FPS)

# -----------------------------------------------------------------------------
#  PEAFUNKTSIOON – MENU EKRAAN  (kood 1 – Menu klass)
# -----------------------------------------------------------------------------
def main():
    """Programmi sisenemispunkt. Kuvab menüü ja käivitab mängu."""
    ekraan = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + EXTRA_HEIGHT))
    pygame.display.set_caption("Pacman")

    # Menüü loomine (kood 1 – Menu klass)
    menüü = Menu(("Start", "Exit"), font_värv=WHITE, valitu_värv=RED, font_suurus=60)
    menüü_aktiivne = True

    kell = pygame.time.Clock()

    while menüü_aktiivne:
        ekraan.fill(BLACK)
        menüü.kuva(ekraan)
        pygame.display.flip()

        for sündmus in pygame.event.get():
            if sündmus.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            menüü.käsitle_sündmus(sündmus)

            if sündmus.type == pygame.KEYDOWN and sündmus.key == pygame.K_RETURN:
                if menüü.olek == 0:
                    # Start – käivita mäng
                    menüü_aktiivne = False
                    mäng(ekraan)
                    menüü_aktiivne = True   # pärast mängu naase menüüsse
                    menüü.olek = 0
                elif menüü.olek == 1:
                    # Exit
                    pygame.quit()
                    sys.exit()

        kell.tick(30)

# -----------------------------------------------------------------------------
#  KÄIVITAMINE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
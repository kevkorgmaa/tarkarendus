import pygame
import sys
import math
import random

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
EXTRA_HEIGHT = 50
FPS = 60
GRID_COLS = 28
GRID_ROWS = 30
MAP_OFFSET_X = 15
MAP_OFFSET_Y = 15
MAP_W = 770
MAP_H = 755
CELL_W = MAP_W / GRID_COLS
CELL_H = MAP_H / GRID_ROWS
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
YELLOW = (255, 255, 0)
STAR_COLOR       = (205, 205, 205)
FRIGHTENED_COLOR = (0, 100, 255)

PACMAN_IMG_PATH   = "images/pacman.png"
RED_GHOST_PATH    = "images/red_ghost.png"
BLUE_GHOST_PATH   = "images/blue_ghost.png"
ORANGE_GHOST_PATH = "images/orange_ghost.png"
PINK_GHOST_PATH   = "images/pink_ghost.png"
MAP_IMG_PATH      = "images/pacman_map.jpeg"

def laadi_pilt(path, suurus=(28, 28)):
    pilt = pygame.image.load(path)
    return pygame.transform.scale(pilt, suurus)

_pacman_base = laadi_pilt(PACMAN_IMG_PATH)
PACMAN_PILDID = {
    (1, 0):  _pacman_base,
    (-1, 0): pygame.transform.flip(_pacman_base, True, False),
    (0, -1): pygame.transform.rotate(_pacman_base, 90),
    (0, 1):  pygame.transform.rotate(_pacman_base, 270),
    (0, 0):  _pacman_base,
}
PACMAN_PILT   = _pacman_base
RED_PILT      = laadi_pilt(RED_GHOST_PATH)
BLUE_PILT     = laadi_pilt(BLUE_GHOST_PATH)
ORANGE_PILT   = laadi_pilt(ORANGE_GHOST_PATH)
PINK_PILT     = laadi_pilt(PINK_GHOST_PATH)
TAUST_PILT    = pygame.transform.scale(pygame.image.load(MAP_IMG_PATH), (SCREEN_WIDTH, SCREEN_HEIGHT))
VAIKE_FONT    = pygame.font.SysFont("monospace", 18)
SUUR_FONT     = pygame.font.SysFont("monospace", 30)

GRID = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0],
    [0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,2,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,2,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,2,2,2,2,2,2,2,2,2,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0],
    [2,2,2,2,2,2,1,2,2,2,0,0,0,0,0,0,0,0,2,2,2,1,2,2,2,2,2,2],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,2,2,2,2,2,2,2,2,2,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0],
    [0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0],
    [0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0],
    [0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0],
    [0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
]

def x_koord(gx): return int(MAP_OFFSET_X + gx * CELL_W + CELL_W / 2)
def y_koord(gy): return int(MAP_OFFSET_Y + gy * CELL_H + CELL_H / 2)

def on_labi(gx, gy):
    """Kas tile (gx,gy) on läbipääsetav (!=0)?"""
    ix, iy = int(round(gx)), int(round(gy))
    if 0 <= iy < GRID_ROWS and 0 <= ix < GRID_COLS:
        return GRID[iy][ix] != 0
    return False

def kaugus(ax, ay, bx, by):
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

# =============================================================================
# MENU
# =============================================================================
class Menu:
    def __init__(self, kirjed, font_varv=WHITE, valitu_varv=RED, font_suurus=60):
        self.olek = 0
        self.font_varv = font_varv
        self.valitu_varv = valitu_varv
        self.kirjed = kirjed
        self.font = pygame.font.Font(None, font_suurus)

    def kuva(self, ekraan):
        for i, kirje in enumerate(self.kirjed):
            varv = self.valitu_varv if self.olek == i else self.font_varv
            tekst = self.font.render(kirje, True, varv)
            posX = SCREEN_WIDTH // 2 - tekst.get_width() // 2
            posY = SCREEN_HEIGHT // 2 - (len(self.kirjed) * tekst.get_height()) // 2 + i * tekst.get_height()
            ekraan.blit(tekst, (posX, posY))

    def kasitle_sundmus(self, sundmus):
        if sundmus.type == pygame.KEYDOWN:
            if sundmus.key == pygame.K_UP and self.olek > 0:
                self.olek -= 1
            elif sundmus.key == pygame.K_DOWN and self.olek < len(self.kirjed) - 1:
                self.olek += 1

# =============================================================================
# TILE-PÕHINE LIIKUMINE — kasutatakse nii Pacmani kui kummituste poolt
# x, y on tile-koordinaadid (täisarvud ruudu keskel, vahepeal float)
# kiirus = sammude arv ühe tile läbimiseks (suurem = aeglasem)
# =============================================================================
class TileEntity:
    def __init__(self, x, y, kiirus=8):
        self.x = float(x)
        self.y = float(y)
        self.kiirus = kiirus
        self.dx = 0       # praegune liikumissuund
        self.dy = 0
        self.ndx = 0      # soovitud järgmine suund
        self.ndy = 0
        self.sammud = 0   # mitu sub-sammu on praeguse tile-liigutuse jooksul jäänud

    def liiguta(self):
        """Liiguta ühe raami võrra. Kutsutakse iga frame."""
        # Torud vasakul/paremal
        if self.x < -0.5:
            self.x = GRID_COLS - 1.5
            self.sammud = 0
            return
        if self.x > GRID_COLS - 0.5:
            self.x = 0.5
            self.sammud = 0
            return

        if self.sammud == 0:
            # Tile-piir saavutatud — otsusta järgmine suund
            cx = int(round(self.x))
            cy = int(round(self.y))

            # Proovi soovitud suunda
            if (self.ndx, self.ndy) != (0, 0) and on_labi(cx + self.ndx, cy + self.ndy):
                self.dx = self.ndx
                self.dy = self.ndy

            # Proovi praegust suunda
            if on_labi(cx + self.dx, cy + self.dy):
                self.sammud = self.kiirus
            else:
                self.dx = 0
                self.dy = 0
                return

        # Liigu sub-sammu võrra
        self.x += self.dx / self.kiirus
        self.y += self.dy / self.kiirus
        self.sammud -= 1
        if self.sammud == 0:
            self.x = round(self.x)
            self.y = round(self.y)

# =============================================================================
# PACMAN
# =============================================================================
class Pacman(TileEntity):
    ALG_X    = 13
    ALG_Y    = 23
    MAX_ELUD = 3

    def __init__(self):
        super().__init__(self.ALG_X, self.ALG_Y, kiirus=8)
        self.pilt = PACMAN_PILT
        self.punktid = 0
        self.elud = self.MAX_ELUD

    def kuva(self, ekraan):
        pilt = PACMAN_PILDID.get((self.dx, self.dy), PACMAN_PILDID[(0, 0)])
        ekraan.blit(pilt, (x_koord(self.x) - 14, y_koord(self.y) - 14))

    def soo(self, tahted, power_ups, voit_cb, frightened_cb):
        pos = (int(round(self.x)), int(round(self.y)))
        if pos in tahted:
            tahted.remove(pos)
            self.punktid += 10
            if not tahted:
                voit_cb()
        if pos in power_ups:
            power_ups.remove(pos)
            frightened_cb()

    def kaota_elu(self):
        self.elud -= 1
        if self.elud <= 0:
            return True
        self.x = float(self.ALG_X)
        self.y = float(self.ALG_Y)
        self.dx = self.dy = self.ndx = self.ndy = 0
        self.sammud = 0
        return False

# =============================================================================
# KUMMITUS — tile-põhine, juhuslik liikumine
# =============================================================================
RESPAWN_DELAY = 5000

# Neli erinevat spawni — laiali üle kaardi
GHOST_SPAWNS = [(1, 1), (26, 1), (1, 29), (26, 29)]
GHOST_DIRS   = [(1, 0), (-1, 0), (1, 0), (-1, 0)]

class Kummitus(TileEntity):
    def __init__(self, pilt, spawn_idx):
        sx, sy = GHOST_SPAWNS[spawn_idx]
        super().__init__(sx, sy, kiirus=10)
        self.pilt = pilt
        self.spawn_idx = spawn_idx
        ddx, ddy = GHOST_DIRS[spawn_idx]
        self.dx = ddx
        self.dy = ddy
        self.syodud = False
        self.respawn_aeg = 0
        self.frightened = False

    def reset_pos(self):
        sx, sy = GHOST_SPAWNS[self.spawn_idx]
        self.x = float(sx)
        self.y = float(sy)
        ddx, ddy = GHOST_DIRS[self.spawn_idx]
        self.dx = ddx
        self.dy = ddy
        self.ndx = self.ndy = 0
        self.sammud = 0
        self.syodud = False
        self.frightened = False

    def kuva(self, ekraan):
        if self.syodud:
            return
        if self.frightened:
            pygame.draw.circle(ekraan, FRIGHTENED_COLOR,
                               (x_koord(self.x), y_koord(self.y)), 12)
        else:
            ekraan.blit(self.pilt, (x_koord(self.x) - 14, y_koord(self.y) - 14))

    def uuenda_respawn(self):
        if self.syodud and pygame.time.get_ticks() >= self.respawn_aeg:
            self.reset_pos()

    def syhta_soodud(self):
        self.syodud = True
        self.respawn_aeg = pygame.time.get_ticks() + RESPAWN_DELAY

    def vali_juhuslik_suund(self):
        """
        Ristmikul: vali juhuslik vaba suund.
        Ei luba tagasipööret (180 kraadi) v.a kui muud pole.
        Kutsutakse ainult tile-piiril (sammud==0).
        """
        cx = int(round(self.x))
        cy = int(round(self.y))

        # Kõik vabad suunad (v.a tagasi)
        tagasi = (-self.dx, -self.dy)
        voimalused = []
        for ddx, ddy in [(1,0),(-1,0),(0,1),(0,-1)]:
            if (ddx, ddy) == tagasi:
                continue
            if on_labi(cx + ddx, cy + ddy):
                voimalused.append((ddx, ddy))

        if voimalused:
            ddx, ddy = random.choice(voimalused)
            self.ndx = ddx
            self.ndy = ddy
        elif on_labi(cx + tagasi[0], cy + tagasi[1]):
            # Ummiktee — pööra tagasi
            self.ndx = tagasi[0]
            self.ndy = tagasi[1]

    def uuenda(self):
        if self.syodud:
            return
        # Tile-piiril vali uus suund
        if self.sammud == 0:
            self.vali_juhuslik_suund()
        self.liiguta()

    def kontrolli_kollisioon(self, pacman, frightened, syya_cb, kaotus_cb):
        if self.syodud:
            return
        if kaugus(self.x, self.y, pacman.x, pacman.y) < 0.75:
            if frightened:
                syya_cb(self)
            else:
                kaotus_cb()

class Blinky(Kummitus):
    def __init__(self): super().__init__(RED_PILT,    0)

class Pinky(Kummitus):
    def __init__(self): super().__init__(PINK_PILT,   1)

class Inky(Kummitus):
    def __init__(self): super().__init__(BLUE_PILT,   2)

class Clyde(Kummitus):
    def __init__(self): super().__init__(ORANGE_PILT, 3)

# =============================================================================
# TAHTED JA POWER-UP'ID
# =============================================================================
def initsialiseeri_tahted():
    return {(x, y) for y, rida in enumerate(GRID) for x, v in enumerate(rida) if v == 1}

def initsialiseeri_power_ups():
    return [(1, 1), (26, 1), (1, 28), (26, 28)]

# =============================================================================
# EKRAAN
# =============================================================================
def uuenda_ekraan(ekraan, tahted, power_ups, pacman, kummitused, frightened, grace_aeg):
    ekraan.fill(BLACK)
    ekraan.blit(TAUST_PILT, (0, 0))
    for tx, ty in tahted:
        pygame.draw.circle(ekraan, STAR_COLOR, (x_koord(tx), y_koord(ty)), 4)
    for px, py in power_ups:
        pygame.draw.circle(ekraan, YELLOW, (x_koord(px), y_koord(py)), 8)
    for k in kummitused:
        k.kuva(ekraan)
    praegu = pygame.time.get_ticks()
    if grace_aeg > 0:
        jaanud = max(0, (grace_aeg - praegu) // 1000)
        if (praegu // 200) % 2 == 0:
            pacman.kuva(ekraan)
        tekst = VAIKE_FONT.render(f"Invincible: {jaanud}s", True, YELLOW)
        ekraan.blit(tekst, (SCREEN_WIDTH // 2 - tekst.get_width() // 2, SCREEN_HEIGHT - 30))
    else:
        pacman.kuva(ekraan)
    if frightened:
        tekst = VAIKE_FONT.render("FRIGHTENED!", True, FRIGHTENED_COLOR)
        ekraan.blit(tekst, (SCREEN_WIDTH // 2 - tekst.get_width() // 2, 10))
    ekraan.blit(VAIKE_FONT.render(f"Points: {pacman.punktid}", True, WHITE), (40, SCREEN_HEIGHT + 15))
    ekraan.blit(VAIKE_FONT.render(f"Lives: {pacman.elud}", True, WHITE), (620, SCREEN_HEIGHT + 15))
    pygame.display.update()

def kuva_teade(ekraan, sonum):
    pygame.draw.rect(ekraan, (100, 100, 200), (250, 300, 300, 150))
    ekraan.blit(SUUR_FONT.render(f"You {sonum}!", True, WHITE), (300, 330))
    ekraan.blit(VAIKE_FONT.render("SPACE – uuesti", True, WHITE), (300, 390))
    pygame.display.update()

def kuva_elu_kaotus(ekraan, elud):
    tekst = SUUR_FONT.render(f"Lost a life! Lives: {elud}", True, RED)
    ekraan.blit(tekst, (SCREEN_WIDTH // 2 - tekst.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(900)

# =============================================================================
# PEAMÄNG
# =============================================================================
def mang(ekraan):
    tahted    = initsialiseeri_tahted()
    power_ups = initsialiseeri_power_ups()
    pacman    = Pacman()
    kummitused = [Blinky(), Pinky(), Inky(), Clyde()]

    mang_loppes     = False
    frightened      = False
    frightened_lopp = 0
    grace_lopp      = 0
    GRACE_KESTUS      = 5000
    FRIGHTENED_KESTUS = 8000

    def lylita_frightened():
        nonlocal frightened, frightened_lopp
        frightened = True
        frightened_lopp = pygame.time.get_ticks() + FRIGHTENED_KESTUS
        for k in kummitused:
            k.frightened = True

    def syya_kummitus(k):
        k.syhta_soodud()
        k.frightened = False
        pacman.punktid += 200

    def kaotus():
        nonlocal mang_loppes, grace_lopp, frightened
        if pygame.time.get_ticks() < grace_lopp:
            return
        frightened = False
        for k in kummitused:
            k.frightened = False
        if pacman.kaota_elu():
            kuva_teade(ekraan, "Lost")
            mang_loppes = True
        else:
            kuva_elu_kaotus(ekraan, pacman.elud)
            grace_lopp = pygame.time.get_ticks() + GRACE_KESTUS

    def voit():
        nonlocal mang_loppes
        kuva_teade(ekraan, "Won")
        mang_loppes = True

    kell = pygame.time.Clock()
    while True:
        praegu = pygame.time.get_ticks()
        if frightened and praegu >= frightened_lopp:
            frightened = False
            for k in kummitused:
                k.frightened = False

        for sundmus in pygame.event.get():
            if sundmus.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif sundmus.type == pygame.KEYDOWN:
                if sundmus.key == pygame.K_ESCAPE:
                    return
                if not mang_loppes:
                    if sundmus.key in (pygame.K_a, pygame.K_LEFT):
                        pacman.ndx, pacman.ndy = -1, 0
                    elif sundmus.key in (pygame.K_d, pygame.K_RIGHT):
                        pacman.ndx, pacman.ndy =  1, 0
                    elif sundmus.key in (pygame.K_w, pygame.K_UP):
                        pacman.ndx, pacman.ndy =  0, -1
                    elif sundmus.key in (pygame.K_s, pygame.K_DOWN):
                        pacman.ndx, pacman.ndy =  0,  1
                elif sundmus.key == pygame.K_SPACE:
                    mang(ekraan); return

        if not mang_loppes:
            pacman.liiguta()
            for k in kummitused:
                k.uuenda_respawn()
                k.uuenda()
                k.kontrolli_kollisioon(pacman, frightened,
                                       lambda k=k: syya_kummitus(k), kaotus)
            pacman.soo(tahted, power_ups, voit, lylita_frightened)

        grace_aeg = grace_lopp if praegu < grace_lopp else 0
        uuenda_ekraan(ekraan, tahted, power_ups, pacman, kummitused, frightened, grace_aeg)
        kell.tick(FPS)

# =============================================================================
# MENUU
# =============================================================================
def main():
    ekraan = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + EXTRA_HEIGHT))
    pygame.display.set_caption("Pacman")
    menuu = Menu(("Start", "Exit"), font_varv=WHITE, valitu_varv=RED, font_suurus=60)
    kell = pygame.time.Clock()
    while True:
        ekraan.fill(BLACK)
        menuu.kuva(ekraan)
        pygame.display.flip()
        for sundmus in pygame.event.get():
            if sundmus.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            menuu.kasitle_sundmus(sundmus)
            if sundmus.type == pygame.KEYDOWN and sundmus.key == pygame.K_RETURN:
                if menuu.olek == 0:
                    mang(ekraan); menuu.olek = 0
                elif menuu.olek == 1:
                    pygame.quit(); sys.exit()
        kell.tick(30)

if __name__ == "__main__":
    main()
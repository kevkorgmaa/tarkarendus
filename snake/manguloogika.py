# =============================================================================
#  MÄNGU LOOGIKA  –  pygame-vaba moodul testide jaoks
#  Kõik funktsioonid töötavad ilma pygame'i initsialiseerimata.
# =============================================================================

# Ruudustiku mõõtmed (peavad kattuma snake.py konstantidega)
RUUDUSTIKU_LAIUS  = 30
RUUDUSTIKU_KÕRGUS = 30


# ─── Liikumine ────────────────────────────────────────────────────────────────

def arvuta_uus_pea(uss: list, vel: tuple) -> tuple:
    """
    Arvuta ussi uue pea koordinaadid.
    Kasutab läbivaid seinu (wrap-around): serva tagant tullakse teisest otsast.

    Args:
        uss: ruutude list, iga ruut on (x, y) tuple
        vel: liikumissuund (dx, dy) tuplena

    Returns:
        Uue pea (x, y) tuple
    """
    vana_pea_x, vana_pea_y = uss[-1]
    dx, dy = vel
    uus_x = (vana_pea_x + dx) % RUUDUSTIKU_LAIUS
    uus_y = (vana_pea_y + dy) % RUUDUSTIKU_KÕRGUS
    return (uus_x, uus_y)


def on_vastassuund(vel: tuple, uus_vel: tuple) -> bool:
    """
    Kontrolli, kas uus suund on praeguse suuna vastand.
    Vastassuunda pöördumine ei ole lubatud.

    Args:
        vel:     praegune suund (dx, dy)
        uus_vel: soovitud uus suund (dx, dy)

    Returns:
        True kui suunad on vastakud (summa on (0,0))
    """
    return vel[0] + uus_vel[0] == 0 and vel[1] + uus_vel[1] == 0


# ─── Kokkupõrked ──────────────────────────────────────────────────────────────

def on_kokkupõrge_iseendaga(uss: list, uus_pea: tuple) -> bool:
    """
    Kontrolli, kas uus pea positsioon kattub ussi kehaga.

    Args:
        uss:     ruutude list (x, y) tupleid
        uus_pea: uue pea (x, y)

    Returns:
        True kui pea tabab oma keha
    """
    return uus_pea in uss


def on_kokkupõrge_kiviga(uus_pea: tuple, kivid: set) -> bool:
    """
    Kontrolli, kas uus pea positsioon kattub kiviga.

    Args:
        uus_pea: uue pea (x, y)
        kivid:   kivide koordinaatide hulk {(x, y), ...}

    Returns:
        True kui pea tabab kivi
    """
    return uus_pea in kivid


# ─── Ussi kasv ja lühenemine ──────────────────────────────────────────────────

def uuenda_uss(uss: list, uus_pea: tuple, kasv: int) -> tuple:
    """
    Lisa uus pea ja eemalda saba kui vaja.

    Args:
        uss:     praegune ussi ruutude list
        uus_pea: lisatav uus pea (x, y)
        kasv:    kasvuloendur (>0 = uss kasvab, saba ei eemaldata)

    Returns:
        (uus_uss, uus_kasv) – uuendatud uss ja kasvuloendur
    """
    uus_uss = list(uss)  # koopia, et mitte muuta originaali
    uus_uss.append(uus_pea)
    if kasv > 0:
        uus_kasv = kasv - 1
    else:
        uus_uss.pop(0)   # eemalda saba
        uus_kasv = 0
    return uus_uss, uus_kasv


def lühenda_uss(uss: list) -> list:
    """
    Lühenda usse ühe ruutu võrra (mürgitatud õun, MOD-2).
    Ei lühenda kui uss on juba minimaalne (2 ruutu).

    Args:
        uss: praegune ussi ruutude list

    Returns:
        Lühendatud (või muutmata) uss
    """
    if len(uss) > 2:
        return uss[1:]  # eemalda saba
    return list(uss)


# ─── Skoor ja kiirus ──────────────────────────────────────────────────────────

def arvuta_kiirus(praegune_kiirus: int, skoor: int) -> int:
    """
    Suurenda kiirust iga 5 õuna järel, maksimaalselt 30 kaadrit/sek.

    Args:
        praegune_kiirus: hetke FPS
        skoor:           praegune pistete arv

    Returns:
        Uus kiirus
    """
    if skoor > 0 and skoor % 5 == 0:
        return min(praegune_kiirus + 1, 30)
    return praegune_kiirus


# ─── Tulemuste tabel ──────────────────────────────────────────────────────────

def sorteeri_ja_piirita_tulemused(tulemused: list, uus_skoor: int, uus_raskus: str) -> list:
    """
    Lisa uus tulemus, sorteeri kahanevalt ja hoia top-5.

    Args:
        tulemused:  olemasolev list [(skoor, raskus), ...]
        uus_skoor:  lisatav skoor
        uus_raskus: raskusastme nimi (string)

    Returns:
        Uus top-5 list
    """
    uued = list(tulemused) + [(uus_skoor, uus_raskus)]
    uued.sort(key=lambda x: x[0], reverse=True)
    return uued[:5]


def on_uus_rekord(tulemused: list, skoor: int) -> bool:
    """
    Kontrolli, kas skoor mahub top-5 hulka.

    Args:
        tulemused: olemasolev [(skoor, raskus), ...] list
        skoor:     kontrollitav skoor

    Returns:
        True kui skoor on rekord (list on lühem kui 5 või skoor ületab viimase)
    """
    if len(tulemused) < 5:
        return True
    return skoor > tulemused[-1][0]
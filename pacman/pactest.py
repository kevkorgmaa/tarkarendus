import pytest
from pacman import (
    on_labi,
    kaugus,
    initsialiseeri_tahted,
    initsialiseeri_power_ups,
    Pacman,
    TileEntity
)


# ---------------------------
# Funktsioonide testid
# ---------------------------

def test_on_labi_tagastab_true_labipaasetava_ruudu_jaoks():
    assert on_labi(1, 1) is True


def test_on_labi_tagastab_false_seina_jaoks():
    assert on_labi(0, 0) is False


def test_on_labi_valjaspool_kaarti():
    assert on_labi(-1, -1) is False
    assert on_labi(100, 100) is False


def test_kaugus_arvutab_oigesti():
    assert kaugus(0, 0, 3, 4) == 5.0


def test_initsialiseeri_tahted_tagastab_hulga():
    tahted = initsialiseeri_tahted()
    assert isinstance(tahted, set)
    assert (1, 1) in tahted


def test_initsialiseeri_power_ups():
    powerups = initsialiseeri_power_ups()
    assert len(powerups) == 4
    assert (1, 1) in powerups
    assert (26, 28) in powerups


# ---------------------------
# Pacmani testid
# ---------------------------

def test_pacman_algvaartused():
    pacman = Pacman()
    assert pacman.punktid == 0
    assert pacman.elud == pacman.MAX_ELUD
    assert pacman.x == pacman.ALG_X
    assert pacman.y == pacman.ALG_Y


def test_pacman_kaotab_elu():
    pacman = Pacman()
    tulemus = pacman.kaota_elu()

    assert tulemus is False
    assert pacman.elud == pacman.MAX_ELUD - 1
    assert pacman.x == pacman.ALG_X
    assert pacman.y == pacman.ALG_Y


def test_pacman_kaotab_viimase_elu():
    pacman = Pacman()
    pacman.elud = 1

    tulemus = pacman.kaota_elu()

    assert tulemus is True
    assert pacman.elud == 0


def test_pacman_soob_tahe():
    pacman = Pacman()
    pacman.x = 1
    pacman.y = 1

    tahted = {(1, 1)}
    powerups = []

    voit_kutsutud = False
    frightened_kutsutud = False

    def voit():
        nonlocal voit_kutsutud
        voit_kutsutud = True

    def frightened():
        nonlocal frightened_kutsutud
        frightened_kutsutud = True

    pacman.soo(tahted, powerups, voit, frightened)

    assert pacman.punktid == 10
    assert len(tahted) == 0
    assert voit_kutsutud is True
    assert frightened_kutsutud is False


def test_pacman_soob_powerupi():
    pacman = Pacman()
    pacman.x = 1
    pacman.y = 1

    tahted = set()
    powerups = [(1, 1)]

    frightened_kutsutud = False

    def voit():
        pass

    def frightened():
        nonlocal frightened_kutsutud
        frightened_kutsutud = True

    pacman.soo(tahted, powerups, voit, frightened)

    assert powerups == []
    assert frightened_kutsutud is True


# ---------------------------
# TileEntity testid
# ---------------------------

def test_tileentity_liigub_edasi():
    entity = TileEntity(1, 1, kiirus=4)

    entity.dx = 1
    entity.dy = 0
    entity.ndx = 1
    entity.ndy = 0
    entity.sammud = 4

    vana_x = entity.x
    entity.liiguta()

    assert entity.x > vana_x


def test_tileentity_torust_vasakul():
    entity = TileEntity(-1, 5)
    entity.liiguta()

    assert entity.sammud == 0


def test_tileentity_torust_paremal():
    entity = TileEntity(28, 5)
    entity.liiguta()

    assert entity.sammud == 0
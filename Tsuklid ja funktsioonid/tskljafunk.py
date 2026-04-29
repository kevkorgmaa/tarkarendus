import pygame
import sys

# Estonian color → RGB mapping
color_map = {
    "punane": (255, 0, 0),
    "roheline": (0, 255, 0),
    "sinine": (0, 0, 255),
    "kollane": (255, 255, 0),
    "oranž": (255, 165, 0),
    "lilla": (128, 0, 128),
    "must": (0, 0, 0),
    "valge": (255, 255, 255),
    "hall": (128, 128, 128),
    "pruun": (139, 69, 19)
}


def run_input_form():
    """Show the input form and return (a, b, c, rgb) or None if quit."""
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Input Form")
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 28)

    fields = [
        ["Ruudu suurus (int)", ""],
        ["Ridade arv(int)", ""],
        ["Veergude arv(int)", ""],
        ["Värv (eesti keeles)", ""]
    ]
    active_field = 0
    error_msg = ""

    while True:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(len(fields)):
                    rect = pygame.Rect(270, 80 + i * 80, 280, 40)
                    if rect.collidepoint(x, y):
                        active_field = i

            if event.type == pygame.KEYDOWN:
                error_msg = ""
                if event.key == pygame.K_TAB:
                    active_field = (active_field + 1) % len(fields)
                elif event.key == pygame.K_BACKSPACE:
                    fields[active_field][1] = fields[active_field][1][:-1]
                elif event.key == pygame.K_RETURN:
                    try:
                        a = int(fields[0][1])
                        b = int(fields[1][1])
                        c = int(fields[2][1])
                        color_name = fields[3][1].lower().strip()
                        rgb = color_map.get(color_name)
                        if rgb is None:
                            error_msg = f"Tundmatu värv: '{color_name}'"
                        else:
                            pygame.display.quit()
                            return a, b, c, rgb
                    except ValueError:
                        error_msg = "Väärtused 1-3 peavad olema täisarvud!"
                else:
                    fields[active_field][1] += event.unicode

        # Draw fields
        for i, (label, value) in enumerate(fields):
            y = 80 + i * 80
            label_surf = font.render(label, True, (200, 200, 200))
            screen.blit(label_surf, (20, y))
            rect = pygame.Rect(270, y, 280, 40)
            border_color = (255, 200, 0) if i == active_field else (100, 100, 100)
            pygame.draw.rect(screen, border_color, rect, 2)
            text_surf = font.render(value, True, (255, 255, 255))
            screen.blit(text_surf, (rect.x + 5, rect.y + 5))

        # Hint
        hint = small_font.render("Vajuta ENTER kinnitamiseks, TAB järgmisele väljale", True, (150, 150, 150))
        screen.blit(hint, (20, 460))

        # Error
        if error_msg:
            err_surf = small_font.render(error_msg, True, (255, 80, 80))
            screen.blit(err_surf, (20, 430))

        pygame.display.flip()


def joonista_ruudustik(ekraan, ruudu_suurus=20, read=24, veerud=32, joone_varv=(255, 0, 0), taustavärv=(144, 238, 144)):
    ekraan.fill(taustavärv)

    for rida in range(read + 1):
        y = rida * ruudu_suurus
        pygame.draw.line(ekraan, joone_varv, (0, y), (veerud * ruudu_suurus, y))

    for veerg in range(veerud + 1):
        x = veerg * ruudu_suurus
        pygame.draw.line(ekraan, joone_varv, (x, 0), (x, read * ruudu_suurus))


def main():
    # Phase 1: collect input
    a, b, c, joone_varv = run_input_form()

    print(f"Values: {a}, {b}, {c}")
    print(f"Line color: {joone_varv}")

    # Phase 2: launch grid using the collected values
    pygame.init()
    ekraan = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Harjutamine")
    kell = pygame.time.Clock()

    # a, b, c are available here — used as ruudu_suurus, read, veerud
    # Clamp to safe values to avoid zero/negative sizes
    ruudu_suurus = max(5, a)
    read = max(1, b)
    veerud = max(1, c)

    while True:
        for sündmus in pygame.event.get():
            if sündmus.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if sündmus.type == pygame.KEYDOWN:
                if sündmus.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        joonista_ruudustik(
            ekraan,
            ruudu_suurus=ruudu_suurus,
            read=read,
            veerud=veerud,
            joone_varv=joone_varv
        )

        pygame.display.flip()
        kell.tick(60)


if __name__ == "__main__":
    main()
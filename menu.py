# menu.py — Schermata principale di BLACK NIGHT
import arcade
import math
import random
from impostazioni import LARGHEZZA, ALTEZZA, SCALA

# ── Colori tema ──────────────────────────────────────────────
NERO          = (0,   0,   0,   255)
ROSSO_SANGUE  = (140,  0,   0,   255)
ROSSO_VIVO    = (200,  20,  20,  255)
BIANCO_SPORCO = (220, 210, 200,  255)
GRIGIO_SCURO  = (30,   30,  30,  255)
GRIGIO_MEDIO  = (60,   60,  60,  255)
AMBRA         = (180, 120,  20,  255)


# ── Particella fumo/polvere ───────────────────────────────────
class Particella:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x        = random.uniform(0, LARGHEZZA)
        self.y        = random.uniform(-20, -5)
        self.vel_x    = random.uniform(-0.3, 0.3) * SCALA
        self.vel_y    = random.uniform(0.2, 0.6)  * SCALA
        self.alpha    = 0
        self.raggio   = random.uniform(1, 3) * SCALA
        self.vita     = 0
        self.vita_max = random.randint(180, 360)

    def aggiorna(self):
        self.x    += self.vel_x
        self.y    += self.vel_y
        self.vita += 1
        t = self.vita / self.vita_max
        if t < 0.2:
            self.alpha = int(80 * (t / 0.2))
        elif t > 0.8:
            self.alpha = int(80 * ((1 - t) / 0.2))
        else:
            self.alpha = 80
        if self.vita >= self.vita_max or self.y > ALTEZZA + 20:
            self.reset()

    def disegna(self):
        arcade.draw_circle_filled(
            self.x, self.y, self.raggio,
            (GRIGIO_MEDIO[0], GRIGIO_MEDIO[1], GRIGIO_MEDIO[2], self.alpha)
        )


# ── Stella tremolante ─────────────────────────────────────────
class Stella:
    def __init__(self):
        self.x          = random.uniform(0, LARGHEZZA)
        self.y          = random.uniform(ALTEZZA * 0.4, ALTEZZA)
        self.base_alpha = random.randint(40, 160)
        self.alpha      = self.base_alpha
        self.fase       = random.uniform(0, math.pi * 2)
        self.velocita   = random.uniform(0.02, 0.06)
        self.raggio     = random.uniform(0.5, 1.5) * SCALA

    def aggiorna(self, dt):
        self.fase  += self.velocita
        self.alpha  = int(self.base_alpha * (0.5 + 0.5 * math.sin(self.fase)))

    def disegna(self):
        arcade.draw_circle_filled(
            self.x, self.y, self.raggio,
            (AMBRA[0], AMBRA[1], AMBRA[2], self.alpha)
        )


# ── Bottone ───────────────────────────────────────────────────
class Bottone:
    LARGH = int(320 * SCALA)
    ALT   = int(52  * SCALA)

    def __init__(self, testo: str, x: float, y: float, callback):
        self.testo    = testo
        self.cx       = x
        self.cy       = y
        self.callback = callback
        self.hover    = False
        self.pulse    = 0.0

    def _rect_x(self): return self.cx - self.LARGH / 2
    def _rect_y(self): return self.cy - self.ALT  / 2

    def contiene(self, mx, my) -> bool:
        return (self._rect_x() <= mx <= self._rect_x() + self.LARGH and
                self._rect_y() <= my <= self._rect_y() + self.ALT)

    def aggiorna(self, dt, mx, my):
        self.hover = self.contiene(mx, my)
        if self.hover:
            self.pulse = (self.pulse + dt * 4) % (math.pi * 2)

    def disegna(self):
        if self.hover:
            alpha_bg     = 180
            colore_bordo = ROSSO_VIVO
            glow         = int(8 * SCALA)
            colore_testo = BIANCO_SPORCO
        else:
            alpha_bg     = 80
            colore_bordo = ROSSO_SANGUE
            glow         = 0
            colore_testo = (180, 160, 140, 220)

        if glow:
            gw = self.LARGH + glow * 2
            gh = self.ALT   + glow * 2
            arcade.draw_lrbt_rectangle_filled(
                self.cx - gw/2, self.cx + gw/2,
                self.cy - gh/2, self.cy + gh/2,
                (ROSSO_SANGUE[0], ROSSO_SANGUE[1], ROSSO_SANGUE[2], 40)
            )

        arcade.draw_lrbt_rectangle_filled(
            self.cx - self.LARGH/2, self.cx + self.LARGH/2,
            self.cy - self.ALT/2,   self.cy + self.ALT/2,
            (10, 0, 0, alpha_bg)
        )
        arcade.draw_lrbt_rectangle_outline(
            self.cx - self.LARGH/2, self.cx + self.LARGH/2,
            self.cy - self.ALT/2,   self.cy + self.ALT/2,
            colore_bordo, border_width=int(2 * SCALA)
        )
        arcade.draw_text(
            self.testo,
            self.cx, self.cy,
            colore_testo,
            font_size=int(18 * SCALA),
            font_name="Arial",
            bold=self.hover,
            anchor_x="center",
            anchor_y="center",
        )

    def click(self):
        if self.hover:
            self.callback()


# ── Menu principale ───────────────────────────────────────────
class Menu:
    """
    Schermata menu di Black Night.

    In game.py:
        from menu import Menu
        self.menu = Menu(on_inizia=self.avvia_gioco, on_esci=self.chiudi)

    Ogni frame:
        self.menu.on_update(delta_time)
        self.menu.on_draw()
        self.menu.on_mouse_press(x, y, button, modifiers)
        self.menu.on_mouse_motion(x, y, dx, dy)
    """

    def __init__(self, on_inizia=None, on_esci=None):
        self.on_inizia_cb = on_inizia
        self.on_esci_cb   = on_esci

        self.tempo        = 0.0
        self.mouse_x      = 0
        self.mouse_y      = 0
        self.titolo_alpha = 255
        self.flicker_cd   = random.uniform(4, 9)

        # Particelle fumo
        self.particelle = [Particella() for _ in range(60)]
        for p in self.particelle:
            p.y = random.uniform(0, ALTEZZA)   # pre-sparge

        # Stelle
        self.stelle = [Stella() for _ in range(80)]

        # Occhi nell'oscurità
        self.occhi = self._genera_occhi(5)

        # Bottoni
        cx = LARGHEZZA / 2
        self.bottoni = [
            Bottone("INIZIA NOTTE",  cx, ALTEZZA * 0.42,                    self._cb_inizia),
            Bottone("CONTINUA",      cx, ALTEZZA * 0.42 - int(70  * SCALA), lambda: None),
            Bottone("OPZIONI",       cx, ALTEZZA * 0.42 - int(140 * SCALA), lambda: None),
            Bottone("ESCI",          cx, ALTEZZA * 0.42 - int(210 * SCALA), self._cb_esci),
        ]

    # ── callbacks ─────────────────────────────────────────────
    def _cb_inizia(self):
        if self.on_inizia_cb:
            self.on_inizia_cb()

    def _cb_esci(self):
        if self.on_esci_cb:
            self.on_esci_cb()
        else:
            arcade.close_window()

    # ── occhi ─────────────────────────────────────────────────
    def _genera_occhi(self, n):
        occhi = []
        zone = [
            (0,               LARGHEZZA * 0.18),
            (LARGHEZZA * 0.82, LARGHEZZA),
            (0,               LARGHEZZA * 0.12),
            (LARGHEZZA * 0.88, LARGHEZZA),
            (LARGHEZZA * 0.08, LARGHEZZA * 0.22),
        ]
        for i in range(n):
            x1, x2 = zone[i % len(zone)]
            occhi.append({
                "x":      random.uniform(x1, x2),
                "y":      random.uniform(ALTEZZA * 0.05, ALTEZZA * 0.32),
                "fase":   random.uniform(0, math.pi * 2),
                "vel":    random.uniform(0.3, 0.9),
                "sep":    random.uniform(8, 18) * SCALA,
                "raggio": random.uniform(3, 6)  * SCALA,
            })
        return occhi

    # ── aggiornamento ─────────────────────────────────────────
    def on_update(self, delta_time):
        self.tempo    += delta_time
        self.flicker_cd -= delta_time

        for p in self.particelle:
            p.aggiorna()
        for s in self.stelle:
            s.aggiorna(delta_time)
        for b in self.bottoni:
            b.aggiorna(delta_time, self.mouse_x, self.mouse_y)

        # flickering titolo
        if self.flicker_cd <= 0:
            self.titolo_alpha = random.randint(50, 140)
            self.flicker_cd   = random.uniform(4, 9)

        # recupero alpha titolo
        if self.titolo_alpha < 255:
            self.titolo_alpha = min(255, self.titolo_alpha + 12)

    # ── disegno ───────────────────────────────────────────────
    def on_draw(self):
        # Sfondo nero
        arcade.draw_lrbt_rectangle_filled(0, LARGHEZZA, 0, ALTEZZA, arcade.color.BLACK)

        # Gradiente rosso-scuro in basso
        fasce = 10
        for i in range(fasce):
            y0    = ALTEZZA * i / fasce
            y1    = ALTEZZA * (i + 1) / fasce
            alpha = int(25 * (i / fasce))
            arcade.draw_lrbt_rectangle_filled(0, LARGHEZZA, y0, y1, (25, 3, 3, alpha))

        for s in self.stelle:
            s.disegna()

        self._disegna_occhi()

        for p in self.particelle:
            p.disegna()

        self._disegna_linea_decorativa()
        self._disegna_titolo()

        for b in self.bottoni:
            b.disegna()

        # Footer
        arcade.draw_text(
            "v0.1  —  BLACK NIGHT",
            LARGHEZZA / 2, int(14 * SCALA),
            (80, 70, 60, 140),
            font_size=int(10 * SCALA),
            font_name="Arial",
            anchor_x="center",
            anchor_y="center",
        )

    def _disegna_occhi(self):
        for o in self.occhi:
            a = int(180 * (0.4 + 0.6 * abs(math.sin(self.tempo * o["vel"] + o["fase"]))))
            for segno in (-1, 1):
                ex = o["x"] + segno * o["sep"] / 2
                # iride
                arcade.draw_ellipse_filled(ex, o["y"],
                    o["raggio"] * 1.6, o["raggio"],
                    (AMBRA[0], AMBRA[1], AMBRA[2], a))
                # pupilla
                arcade.draw_ellipse_filled(ex, o["y"],
                    o["raggio"] * 0.5, o["raggio"] * 0.8,
                    (0, 0, 0, a))

    def _disegna_linea_decorativa(self):
        y = ALTEZZA * 0.72
        arcade.draw_line(
            LARGHEZZA * 0.12, y, LARGHEZZA * 0.88, y,
            (ROSSO_SANGUE[0], ROSSO_SANGUE[1], ROSSO_SANGUE[2], 120),
            int(1 * SCALA)
        )
        # rombo (quadrato ruotato 45°) — disegnato come poligono
        d = int(7 * SCALA)
        cx2 = LARGHEZZA / 2
        arcade.draw_polygon_filled(
            [(cx2, y + d), (cx2 + d, y), (cx2, y - d), (cx2 - d, y)],
            ROSSO_SANGUE
        )

    def _disegna_titolo(self):
        a   = self.titolo_alpha
        cy  = ALTEZZA * 0.82

        # Ombra rossa a layer
        for off, oa in [(6, 30), (4, 50), (2, 70)]:
            arcade.draw_text("BLACK",
                LARGHEZZA / 2 + off, cy + off,
                (ROSSO_SANGUE[0], ROSSO_SANGUE[1], ROSSO_SANGUE[2], oa),
                font_size=int(72 * SCALA), font_name="Arial",
                bold=True, anchor_x="center", anchor_y="center")

        # Testo principale
        arcade.draw_text("BLACK",
            LARGHEZZA / 2, cy,
            (a, int(a * 0.85), int(a * 0.78)),
            font_size=int(72 * SCALA), font_name="Arial",
            bold=True, anchor_x="center", anchor_y="center")

        # Sottotitolo NIGHT
        arcade.draw_text("N  I  G  H  T",
            LARGHEZZA / 2, cy - int(60 * SCALA),
            (ROSSO_VIVO[0], ROSSO_VIVO[1], ROSSO_VIVO[2], a),
            font_size=int(36 * SCALA), font_name="Arial",
            bold=False, anchor_x="center", anchor_y="center")

        # Linea sotto NIGHT
        half = int(160 * SCALA)
        arcade.draw_line(
            LARGHEZZA / 2 - half, cy - int(82 * SCALA),
            LARGHEZZA / 2 + half, cy - int(82 * SCALA),
            (ROSSO_SANGUE[0], ROSSO_SANGUE[1], ROSSO_SANGUE[2], 180),
            int(1 * SCALA)
        )

    # ── input ─────────────────────────────────────────────────
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for b in self.bottoni:
                b.click()
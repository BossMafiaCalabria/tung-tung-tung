# game.py — Punto di ingresso di BLACK NIGHT
import arcade
from impostazioni import LARGHEZZA, ALTEZZA, FPS, TITOLO, MODALITA, POS_X, POS_Y


class Game(arcade.Window):
    def __init__(self):
        fullscreen = (MODALITA == "fullscreen")
        super().__init__(LARGHEZZA, ALTEZZA, TITOLO, fullscreen=fullscreen)
        if not fullscreen:
            self.set_location(POS_X, POS_Y)   # centra sul monitor
        arcade.set_background_color(arcade.color.BLACK)

        self.stato = "MENU"

        # Importa qui dentro, solo quando il file esiste
        from menu import Menu
        self.menu = Menu(
            on_inizia=self.avvia_gioco,
            on_esci=self.chiudi
        )

        # Aggiungi gli altri moduli man mano che li crei:
        # from schermata_notte import SchermataNote
        # self.schermata_notte = SchermataNote()

    # ── cambio stato ──────────────────────────────────────────
    def avvia_gioco(self):
        print("→ Avvio notte...")   # sostituisci con cambio stato reale
        self.stato = "GIOCO"

    def chiudi(self):
        arcade.close_window()

    # ── loop principale ───────────────────────────────────────
    def on_update(self, delta_time):
        if self.stato == "MENU":
            self.menu.on_update(delta_time)
        elif self.stato == "GIOCO":
            pass  # self.schermata_notte.on_update(delta_time)

    def on_draw(self):
        self.clear()
        if self.stato == "MENU":
            self.menu.on_draw()
        elif self.stato == "GIOCO":
            pass  # self.schermata_notte.on_draw()

    # ── input ─────────────────────────────────────────────────
    def on_mouse_motion(self, x, y, dx, dy):
        if self.stato == "MENU":
            self.menu.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.stato == "MENU":
            self.menu.on_mouse_press(x, y, button, modifiers)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()


def main():
    window = Game()
    arcade.set_window(window)
    arcade.run()


if __name__ == "__main__":
    main()
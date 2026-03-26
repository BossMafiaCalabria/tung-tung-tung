import arcade
from impostazioni import LARGHEZZA, ALTEZZA, FPS, TITOLO

class Game(arcade.Window):
    def __init__(self):
        super().__init__(LARGHEZZA, ALTEZZA, TITOLO)
        arcade.set_background_color(arcade.color.BLACK)
        self.stato = "MENU"

        # Importi i moduli QUI DENTRO, solo quando esistono
        # from menu import Menu
        # self.menu = Menu()

    def on_draw(self):
        self.clear()
        # Per ora solo un testo placeholder
        arcade.draw_text(
            "Game OK",
            LARGHEZZA / 2,
            ALTEZZA / 2,
            arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
            anchor_y="center",
        )

    def on_update(self, delta_time):
        # Logica aggiornamento in base allo stato
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

def main():
    window = Game()
    arcade.run()

if __name__ == "__main__":
    main()
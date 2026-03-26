import arcade
import animatronico
import gestore_audio
import gestore_gioco
import gestore_minigiochi
import impostazioni
import interfaccia
import menu
import minigioco_base
import minigioco_fuga
import minigioco_memoria
import minigioco_nascondiglio
import minigioco_riparazione
import schermata_storia
import schermata_notte
import sistema_telecamere

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Hello Arcade"


class HelloWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Hello!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=72,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )


def main():
    window = HelloWindow()
    arcade.run()


if __name__ == "__main__":
    main()
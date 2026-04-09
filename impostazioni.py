# impostazioni.py — BLACK NIGHT
import arcade

# ── Rileva monitor ────────────────────────────────────────────
monitor_w, monitor_h = arcade.get_display_size()

# ── Modalità: "finestra", "adattiva", "fullscreen" ────────────
MODALITA = "adattiva"

if MODALITA == "fullscreen":
    LARGHEZZA = monitor_w
    ALTEZZA   = monitor_h

elif MODALITA == "adattiva":
    LARGHEZZA = max(800,  int(monitor_w * 0.50))
    ALTEZZA   = max(600,  int(monitor_h * 0.50))

else:  # finestra fissa
    LARGHEZZA = 1280
    ALTEZZA   = 720

# ── Posizione centrata sul monitor ────────────────────────────
POS_X = (LARGHEZZA) // 2
POS_Y = (ALTEZZA)   // 2

# ── Scala UI ─────────────────────────────────────────────────
SCALA = LARGHEZZA / 1280

# ── Altro ─────────────────────────────────────────────────────
FPS    = 60
TITOLO = "Black Night"
# impostazioni.py
import arcade

# --- Rileva la dimensione del monitor ---
schermo_info = arcade.get_display_size()
MONITOR_LARGHEZZA = schermo_info[0]
MONITOR_ALTEZZA   = schermo_info[1]

# --- Modalità finestra ---
# Cambia qui: "finestra", "fullscreen", "adattiva"
MODALITA = "adattiva"

if MODALITA == "fullscreen":
    LARGHEZZA = MONITOR_LARGHEZZA
    ALTEZZA   = MONITOR_ALTEZZA

elif MODALITA == "adattiva":
    # 80% dello schermo, mai sotto 800x600
    LARGHEZZA = max(800, int(MONITOR_LARGHEZZA * 0.80))
    ALTEZZA   = max(600, int(MONITOR_ALTEZZA   * 0.80))

else:  # "finestra" — dimensione fissa
    LARGHEZZA = 1280
    ALTEZZA   = 720

# --- Scala UI ---
# Tutti gli elementi grafici si moltiplicano per questo valore
# Su uno schermo 1920x1080 → SCALA = 1.0 (riferimento)
SCALA = LARGHEZZA / 1280

# --- Altre costanti ---
FPS    = 60
TITOLO = "FNAF Clone"
define config.name = _("Zwischen Front und Heimat")

define gui.show_name = True

define config.version = "0.4.0-kapitel"

define gui.about = _p("""
Ein entscheidungsbasiertes Serious Game zum Ersten Weltkrieg aus der Perspektive des Alltags.

Prototyp im Rahmen eines geschichtsdidaktischen Entwicklungsvorhabens.
""")

define build.name = "ZwischenFrontUndHeimat"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.enter_transition = Dissolve(0.4)
define config.exit_transition = Dissolve(0.4)
define config.intra_transition = Dissolve(0.2)
define config.after_load_transition = None
define config.end_game_transition = None

define config.window = "auto"
define config.window_show_transition = Dissolve(0.2)
define config.window_hide_transition = Dissolve(0.2)

define config.rollback_enabled = False
define config.hard_rollback_limit = 0
define config.allow_skipping = False
define config.fast_skipping = False
define config.has_autosave = False
define config.autosave_on_choice = False

## Ohne Speichersystem darf das Spielmenü nicht mehr auf "save" zeigen.
## Es wird sicher auf die Einstellungen umgeleitet.
define _game_menu_screen = "preferences"

default preferences.text_cps = 45
default preferences.afm_time = 15

default persistent.analysemodus = False

define config.save_directory = "ZwischenFrontUndHeimat-Kern"

define config.window_icon = "gui/window_icon.png"

init python:
    ## Rollback und Überspringen bleiben abgeschaltet.
    config.keymap['rollback'] = [ ]
    config.keymap['skip'] = [ ]
    config.keymap['toggle_skip'] = [ ]
    config.keymap['fast_skip'] = [ ]

    ## Die rechte Maustaste (mouseup_3) wird aus dem Spielmenü genommen.
    ## Escape bleibt erhalten und führt in die Einstellungen.
    config.keymap['game_menu'] = ['K_ESCAPE', 'K_MENU', 'K_AC_BACK']

    ## Tastatursteuerung im Spiel vorerst abgeschaltet: Der Fokus lässt sich
    ## nicht mehr mit den Pfeiltasten verschieben, und Leertaste/Eingabetaste
    ## lösen kein Weiterblättern mehr aus. Bedient wird ausschließlich mit
    ## der Maus. (Die linke Maustaste bleibt in allen Zuordnungen erhalten.)
    config.keymap['focus_left'] = [ ]
    config.keymap['focus_right'] = [ ]
    config.keymap['focus_up'] = [ ]
    config.keymap['focus_down'] = [ ]
    config.keymap['button_alternate'] = [ ]
    config.keymap['dismiss'] = ['mouseup_1']

init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.documentation('*.html')
    build.documentation('*.txt')

# -*- coding: utf-8 -*-
"""kontrast.py - die Farbwelt am Beamer nachgerechnet.

    python kontrast.py

Schreibt KONTRAST.md neben die .rpy-Dateien: fuer jede Kombination aus
Textfarbe und Untergrund, die im Spiel vorkommt, das Kontrastverhaeltnis
nach WCAG 2.1, und wo es nicht reicht, einen Vorschlag.

WARUM 7:1 UND NICHT 4,5:1
Im Klassenzimmer ist das Licht an. Der uebliche Mindestwert 4,5:1 (WCAG
AA) gilt fuer einen Bildschirm auf dem Schreibtisch; ein Beamer verliert
durch Streulicht einen guten Teil des Kontrasts, bevor das Bild an der
Wand ankommt. Deshalb der strengere Wert 7:1 (WCAG AAA). Grosse Schrift
(ab 24 px fett oder 30 px normal) darf nach AAA auf 4,5:1 - das ist unten
eigens ausgewiesen, weil viele Ueberschriften darunter fallen.

ES AENDERT NICHTS
Dieses Skript rechnet und schreibt. Es fasst keine Farbe an. Die Farbwelt
ist das Gesicht des Spiels, und darueber entscheidet der Projektleiter -
der Auftrag sagt das ausdruecklich.

DIE FARBEN WERDEN GEFRAGT, NICHT ABGESCHRIEBEN
Sie kommen aus dem geladenen Namensraum ueber probe_alles. Eine zweite
Liste von Hexwerten neben gui.rpy waere in einer Woche veraltet, und dann
rechnete dieses Skript eine Farbwelt nach, die es nicht mehr gibt.
"""

import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import probe_alles


ZIEL_KLEIN = 7.0        ## WCAG AAA, normale Schrift
ZIEL_GROSS = 4.5        ## WCAG AAA, grosse Schrift (>= 24 px fett / 30 px)


################################################################################
## 1. Rechnen
################################################################################


def zerlegen(farbe):
    """#rrggbb oder #rrggbbaa -> (r, g, b) als 0..255."""
    text = str(farbe).lstrip("#")
    if len(text) == 3:
        text = "".join(z * 2 for z in text)
    return (int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16))


def zusammensetzen(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(w))))
                                   for w in rgb)


def leuchtdichte(farbe):
    """Relative Leuchtdichte nach WCAG 2.1."""
    teile = []
    for wert in zerlegen(farbe):
        anteil = wert / 255.0
        if anteil <= 0.03928:
            teile.append(anteil / 12.92)
        else:
            teile.append(((anteil + 0.055) / 1.055) ** 2.4)
    return 0.2126 * teile[0] + 0.7152 * teile[1] + 0.0722 * teile[2]


def verhaeltnis(vorne, hinten):
    a = leuchtdichte(vorne)
    b = leuchtdichte(hinten)
    hell, dunkel = max(a, b), min(a, b)
    return (hell + 0.05) / (dunkel + 0.05)


def vorschlag(vorne, hinten, ziel=ZIEL_KLEIN):
    """Die naechstliegende Farbe, die das Ziel erreicht.

    Der Farbton bleibt, nur die Helligkeit wandert - und zwar in die
    Richtung, die vom Untergrund wegfuehrt. So bleibt aus einem gedeckten
    Rot ein gedecktes Rot und wird kein Signalrot.
    """
    if verhaeltnis(vorne, hinten) >= ziel:
        return None
    r, g, b = zerlegen(vorne)
    dunkler = leuchtdichte(vorne) < leuchtdichte(hinten)
    beste = None
    for schritt in range(1, 101):
        anteil = schritt / 100.0
        if dunkler:
            kandidat = (r * (1 - anteil), g * (1 - anteil), b * (1 - anteil))
        else:
            kandidat = (r + (255 - r) * anteil,
                        g + (255 - g) * anteil,
                        b + (255 - b) * anteil)
        hex_kandidat = zusammensetzen(kandidat)
        if verhaeltnis(hex_kandidat, hinten) >= ziel:
            beste = hex_kandidat
            break
    return beste


################################################################################
## 2. Was im Spiel wirklich zusammentrifft
################################################################################
##
## Jedes Paar ist belegt. Die Fundstelle steht dabei, damit niemand raten
## muss, ob eine Kombination wirklich vorkommt - eine Kreuztabelle aus
## allen Farben mal allen Untergruenden waere laenger und wertloser.

UNTERGRUENDE = [
    ("FARBE_PAPIER", "Bildschirmgrund",
     "add Solid(FARBE_PAPIER) - 31 Fundstellen, u.a. karten_entscheidung"),
    ("FARBE_PAPIER_HELL", "Karten und Rahmen",
     "kartenpapier() in gui.rpy, rahmen_doppelt(...) in screens.rpy"),
    ("FARBE_PAPIER_DUNKEL", "Zeitungskarte, Motivflaeche, Platzhalter",
     "kartenpapier(\"zeitung\"), bild_platzhalter() in gui.rpy"),
    ("FARBE_DUNKEL_HELL", "dunkle Flaechen im Endbildschirm",
     "background rahmen(FARBE_DUNKEL_HELL, FARBE_LINIE, 2) - 6 Fundstellen"),
    ("FARBE_DUNKEL", "der Endbildschirm und die Uebergaenge",
     "UEBERGANG_KAPITEL() und UEBERGANG_ENDE() in bewegung.rpy"),
    ("FARBE_TINTE", "die Balkenueberschrift der Zeitungskarte",
     "kartenblatt_zeitung in screens.rpy, seit Paket 8 Schritt 1"),
    ("FARBE_AKZENT", "Schaltflaechen unter der Maus",
     "hover_background rahmen(FARBE_AKZENT, FARBE_AKZENT, 2) - 5 Fundstellen"),
]

## Textfarbe -> auf welchen Untergruenden sie vorkommt, und wie gross.
## "gross" heisst: ab 24 px fett oder 30 px normal; dann gilt 4,5:1.
TEXTFARBEN = [
    ("FARBE_TINTE", "Fliesstext, Kartentitel, Ereignistext", 44,
     ["FARBE_PAPIER", "FARBE_PAPIER_HELL", "FARBE_PAPIER_DUNKEL"], False),
    ("FARBE_TINTE_MATT", "Kartentext, Nebenangaben", 42,
     ["FARBE_PAPIER", "FARBE_PAPIER_HELL", "FARBE_PAPIER_DUNKEL"], False),
    ("FARBE_LINIE", "Hinweise, Rubriken, ruhige Zweitzeilen", 31,
     ["FARBE_PAPIER", "FARBE_PAPIER_HELL", "FARBE_PAPIER_DUNKEL"], False),
    ("FARBE_LINIE_FEIN", "Rubriken auf hellem Grund", 2,
     ["FARBE_PAPIER_HELL"], False),
    ("FARBE_AKZENT", "Optionstitel, Stempel, Zustandsmarken", 26,
     ["FARBE_PAPIER", "FARBE_PAPIER_HELL", "FARBE_PAPIER_DUNKEL"], True),
    ("FARBE_AKZENT_MATT", "gedaempfte Akzente", 4,
     ["FARBE_PAPIER", "FARBE_PAPIER_HELL"], False),
    ("FARBE_TEXT_HELL", "Text auf dunklem Grund", 8,
     ["FARBE_DUNKEL", "FARBE_DUNKEL_HELL", "FARBE_TINTE"], False),
    ("FARBE_PAPIER", "Text auf der Akzentflaeche unter der Maus", 2,
     ["FARBE_AKZENT"], False),
    ("FARBE_FEHLEND", "der Pfad im Bildplatzhalter", 1,
     ["FARBE_PAPIER_DUNKEL"], False),
]

## Die Stufenfarben stehen als Text UND als Balkensegment. Als Text sind
## sie der Zustandsname ueber dem Balken - klein und fett.
STUFENFARBEN = ("FARBEN_STUFE", ["FARBE_PAPIER", "FARBE_PAPIER_HELL"])
STUFENFARBEN_HELL = ("FARBEN_STUFE_HELL", ["FARBE_DUNKEL", "FARBE_DUNKEL_HELL"])


################################################################################
## 3. Das Dokument
################################################################################


def marke(wert, ziel):
    return "ja" if wert >= ziel else "**NEIN**"


def bauen():
    ordner = probe_alles.spielordner_finden()
    aufbau = probe_alles.Aufbau(ordner)
    aufbau.lesen()
    aufbau.ausfuehren()
    NS = aufbau.NS

    z = []
    durchgefallen = []

    z.append("# KONTRAST AM BEAMER")
    z.append("")
    z.append("Jede Kombination aus Textfarbe und Untergrund, die im Spiel")
    z.append("vorkommt, nach WCAG 2.1 nachgerechnet.")
    z.append("")
    z.append("**Erzeugt von `kontrast.py`. Es ändert keine Farbe** — die")
    z.append("Farbwelt ist das Gesicht des Spiels, und darüber entscheidet")
    z.append("Dominik.")
    z.append("")
    z.append("## Der Maßstab")
    z.append("")
    z.append("Verlangt sind **%.0f:1**, nicht die üblichen 4,5:1. Der Grund ist"
             % ZIEL_KLEIN)
    z.append("das Klassenzimmer: Bei Tageslicht verliert ein Beamer einen")
    z.append("guten Teil seines Kontrasts, bevor das Bild an der Wand")
    z.append("ankommt. Große Schrift — ab 24 px fett oder 30 px normal —")
    z.append("darf nach demselben Maßstab auf **%.1f:1**; das steht in einer"
             % ZIEL_GROSS)
    z.append("eigenen Spalte, weil viele Überschriften darunter fallen.")
    z.append("")

    ## ------------------------------------------------------------ Untergründe
    z.append("## Die Untergründe")
    z.append("")
    z.append("| Farbe | Wert | Wo | Beleg |")
    z.append("|---|---|---|---|")
    for name, wo, beleg in UNTERGRUENDE:
        if name not in NS:
            continue
        z.append("| `%s` | `%s` | %s | %s |" % (name, NS[name], wo, beleg))
    z.append("")

    ## ------------------------------------------------------------ Haupttabelle
    z.append("## Die Paare")
    z.append("")
    z.append("| Textfarbe | auf Untergrund | Verhältnis | ≥ %.0f:1 | groß: ≥ %.1f:1 |"
             % (ZIEL_KLEIN, ZIEL_GROSS))
    z.append("|---|---|---|---|---|")

    for name, zweck, anzahl, gruende, ist_gross in TEXTFARBEN:
        if name not in NS:
            continue
        for grund in gruende:
            if grund not in NS:
                continue
            wert = verhaeltnis(NS[name], NS[grund])
            z.append("| `%s` <br><small>%s</small> | `%s` | **%.2f:1** | %s | %s |"
                     % (name, zweck, grund, wert,
                        marke(wert, ZIEL_KLEIN), marke(wert, ZIEL_GROSS)))
            if wert < ZIEL_KLEIN:
                durchgefallen.append((name, zweck, grund, wert, ist_gross,
                                      NS[name], NS[grund]))

    for tafelname, gruende in [STUFENFARBEN, STUFENFARBEN_HELL]:
        if tafelname not in NS:
            continue
        for stelle, farbe in enumerate(NS[tafelname]):
            for grund in gruende:
                if grund not in NS:
                    continue
                wert = verhaeltnis(farbe, NS[grund])
                z.append("| `%s[%d]` <br><small>Zustandsname über dem Balken"
                         "</small> | `%s` | **%.2f:1** | %s | %s |"
                         % (tafelname, stelle, grund, wert,
                            marke(wert, ZIEL_KLEIN), marke(wert, ZIEL_GROSS)))
                if wert < ZIEL_KLEIN:
                    durchgefallen.append(
                        ("%s[%d]" % (tafelname, stelle),
                         "Zustandsname über dem Balken",
                         grund, wert, True, farbe, NS[grund]))
    z.append("")

    ## ------------------------------------------------------------ Vorschläge
    z.append("## Wo es nicht reicht")
    z.append("")
    if not durchgefallen:
        z.append("Nirgends. Jede Kombination erreicht %.0f:1." % ZIEL_KLEIN)
    else:
        z.append("%d Kombinationen bleiben unter %.0f:1. Der Vorschlag hält den"
                 % (len(durchgefallen), ZIEL_KLEIN))
        z.append("Farbton fest und verschiebt nur die Helligkeit — aus einem")
        z.append("gedeckten Rot wird so kein Signalrot.")
        z.append("")
        z.append("| Farbe | auf | ist | Vorschlag | wäre | betrifft |")
        z.append("|---|---|---|---|---|---|")
        for name, zweck, grund, wert, ist_gross, vorne, hinten in durchgefallen:
            neu = vorschlag(vorne, hinten, ZIEL_KLEIN)
            if neu:
                neu_wert = verhaeltnis(neu, hinten)
                z.append("| `%s` | `%s` | %.2f:1 | `%s` | %.2f:1 | %s |"
                         % (name, grund, wert, neu, neu_wert, zweck))
            else:
                z.append("| `%s` | `%s` | %.2f:1 | *nicht erreichbar* | – | %s |"
                         % (name, grund, wert, zweck))
        z.append("")
        z.append("Für die Zeilen, die nur die Marke für **große** Schrift")
        z.append("reißen, gilt: Sie sind in Ordnung, solange der Text")
        z.append("tatsächlich groß gesetzt ist. Welche das sind, sagt die")
        z.append("letzte Spalte der Haupttabelle.")
    z.append("")

    ## ------------------------------------------------------------ Nachwort
    z.append("## Was das für den Unterricht heißt")
    z.append("")
    z.append("Eine gerissene Marke ist kein Fehler im Spiel — sie ist eine")
    z.append("Aussage über den schlechtesten Fall: helles Klassenzimmer,")
    z.append("schwacher Beamer, letzte Reihe. Wer den Raum verdunkeln kann,")
    z.append("hat das Problem nicht. Deshalb steht hier eine Tabelle und")
    z.append("keine Reparatur.")
    z.append("")

    ziel = os.path.join(ordner, "KONTRAST.md")
    io.open(ziel, "w", encoding="utf-8").write("\n".join(z) + "\n")
    return ziel, len(durchgefallen)


def main():
    ziel, schlecht = bauen()
    print("KONTRAST.md geschrieben: %s" % ziel)
    print("  %d Kombinationen unter %.0f:1." % (schlecht, ZIEL_KLEIN))
    return 0


if __name__ == "__main__":
    sys.exit(main())

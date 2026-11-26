# STAND

**6. September 2026. Paket 8, Schritt 2.6 (Tongerüst) ist gebaut und
gemessen. Schritt 2 ist damit abgeschlossen — aber das Gegenlesen hat
offene Funde hinterlassen.**

## Wo anfangen

**Offener Punkt 121, vor allem anderen.** Neun Tonfunde aus dem
Gegenlesen: **einer belegt, acht ungeprüft, keiner behoben.** Der
schwerste: `musik_setzen()` startet Musik, aber **nichts beendet sie je**
— derselbe Fehler wie AUFGEFALLEN 116, nur auf dem Musikkanal, und ich
habe ihn beim Beheben übersehen. Alle Belege in AUFGEFALLEN 121.

**Jeden Fund erst gegenprüfen, dann beheben.** Acht sind Behauptungen
ohne Gegenprobe — ihre Prüfer sind am Sitzungslimit gescheitert.

Danach: die **Vorziehregel** (Punkt 104, von Dominik entschieden), dann
die Messung über den kurzen Verlauf und `RHYTHMUS_NACHZIEHEN`. Erst
danach Paket 8, Schritt 3.

## Was 2.6 gebracht hat

- **`game/ton.rpy` neu**, ein Block `init −45`. Zehn Klangräume,
  `ORTSKLANG`, `ORT_KLANGRAUM` (54 Ortsangaben), `STELLENMUSIK` (7),
  `ton_spielen()` mit der harten Sperre, eigener Kanal `umgebung` am
  vorhandenen Regler „Geräusche". 22 Aufrufstellen in 7 Dateien.
- **Probe 11 Tonprobe**, 225 Fälle, sechs Abschnitte. Medienprobe zählt
  Töne mit: 333 → **367** Pfade.
- **Die Sperre war zuerst keine** (AUFGEFALLEN 116): Sie verhinderte nur
  das Anwerfen. Jetzt drei Beine, im laufenden Spiel gemessen — sogar
  `renpy.music.play()` unter Umgehung aller Tonfunktionen wird abgeräumt.

## Probenstand (voller Lauf, `--vergleich bericht_vor_26.txt`)

Alle zehn alten Proben **unverändert**: 126, 563947, 57823, 24211, 105,
367, 31335, 4001, 62, 3488. Nur **Probe 4 mit 1 Beanstandung** wie im
Ausgangsbild. **Probe 11 neu, 225 Fälle, 0 Beanstandungen.** Aufbau
10 Dateien / 74 Blöcke. Lint 0, kein `errors.txt`.

**Diese Null ist mit Vorsicht zu lesen:** Probe 11 hat einen belegten
blinden Fleck (AUFGEFALLEN 121d).

## Was ein Nachfolger wissen muss

- **Es klingt nichts.** Keine Tondatei im Projekt; alle 17 Tafelzeilen
  sind Bedarfsplan. `audio/stummer_morgen.mp3` ist eine **Probedatei**
  (Dominik) und bekommt keine Zeile — AUFGEFALLEN 111.
- **`renpy.py … test` verträgt kein `renpy.pause()`** (Punkt 118):
  `RecursionError`, Ursache nicht im `traceback.txt`. Gemessen wird über
  ein temporäres `label splashscreen` (Punkt 62).
- **Ein leeres Workflow-Ergebnis ist kein Freispruch.** Zweimal sind die
  meisten Leser am Sitzungslimit gescheitert; beide Male sah das Ergebnis
  wie „nichts gefunden" aus. Immer ins `journal.jsonl` sehen.
- **Zwei Schalter liegen bei Dominik:** `RHYTHMUS_NACHZIEHEN` (102) und
  `MUSIK_EINGESCHALTET` (116, offener Punkt 116).
- Neue AUFGEFALLEN-Punkte: 111 bis 121.

# Startprompt für die nächste Sitzung

*Geschrieben am 6. September 2026, nach Paket 8, Schritt 2.6. Zum
Kopieren.*

---

```
Geh die Tonfunde an, offener Punkt 121.

Das Tongerüst aus Schritt 2.6 steht, aber das Gegenlesen hat neun Funde
hinterlassen: einer belegt, acht ungeprüft, keiner behoben. Sie stehen in
AUFGEFALLEN 121 mit Datei, Zeile und Ausfallszenario.

Arbeite sie in dieser Reihenfolge ab, und prüfe jeden einzeln nach,
bevor du ihn behebst — acht davon sind Behauptungen ohne Gegenprobe,
ihre Prüfer sind am Sitzungslimit gescheitert:

1. musik_setzen() startet Musik, aber nichts beendet sie je. Derselbe
   Fehler wie AUFGEFALLEN 116, nur auf dem Musikkanal.
2. TON_AUSBLENDEN wird beim normalen Wechsel nie benutzt.
   config.fadeout_audio ist 0,016 s, der Kommentar sagt 1,5 s zu.
3. Die Sperre fragt für art="umgebung" den Pfad gar nicht, und beide
   Sperrbeine räumen nur den Kanal "music" ab.
4. Der belegte: In Probe 11 ist die Meldung "musik_sperre_durchsetzen()
   gibt es nicht" unerreichbar — die Attrappe springt vorher ein, und die
   Probe meldet dann die falsche Ursache am falschen Pfad.
5. Die drei Werkbankfunde: zwei Tafelzeilen mit derselben Dateikennung,
   leeres TON_ENDUNGEN, Abschnitt 1 zählt nur Freigaben.

Zwei Dinge aus gestern, die du wissen musst:

- renpy.py … test verträgt kein renpy.pause() — RecursionError, und die
  Ursache steht nicht im traceback.txt. Miss über ein temporäres
  label splashscreen (offener Punkt 62). So ist die ganze Tonmessung
  entstanden.
- Ein leeres Workflow-Ergebnis ist kein Freispruch. Zweimal in Folge
  sahen Ausfälle am Sitzungslimit wie "nichts gefunden" aus; beide Male
  standen die Funde nur im journal.jsonl.

Wenn Punkt 121 durch ist, meldest du dich, bevor du weitermachst. Danach
kommt die Vorziehregel (Punkt 104, von mir entschieden), und erst dann
die Messung über den kurzen Verlauf und RHYTHMUS_NACHZIEHEN.

Abnahme misst gegen game/bericht_vor_26.txt: alle zehn alten Proben
müssen bei +0 bleiben, Probe 4 bei 1 Beanstandung, Probe 11 bei 0.
```

---

## Wenn du stattdessen etwas anderes willst

Zwei Schalter warten auf eine Entscheidung von dir, beide sind ein Wort:

- **`RHYTHMUS_NACHZIEHEN`** (offener Punkt 102) — die Nachziehregel aus
  Schritt 2.5. Gebaut, gemessen, aus.
- **`MUSIK_EINGESCHALTET`** (offener Punkt 116) — die Freigabe für Musik
  an den sieben Stellen aus Entscheidung 24. **Erst nach Punkt 121
  umlegen:** Fund 1 wacht genau dann auf.

Und: Es liegt weiterhin keine Tondatei im Projekt. Alle 17 Tafelzeilen
sind Bedarfsplan; der vollständige Bedarf mit 34 Pfaden steht in
`game/MEDIEN.md` unter `## audio`. Es genügt **eine** Endung je Zeile,
`.ogg` oder `.mp3` (AUFGEFALLEN 115).

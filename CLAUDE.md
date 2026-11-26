# Zwischen Front und Heimat

Ein Ren'Py-Lernspiel über den Alltag 1914–1919. Zielgruppe ist die
**8. Klasse an der Oberschule**, 13 bis 14 Jahre, gespielt in einer
Doppelstunde. Drei Pfade (Front, Etappe, Heimat), sechs Kapitel, vier
Werte, kein Speicherstand, keine Punkte.

Projektleiter ist Dominik, Lehrer für Geografie und Geschichte. **Er
entscheidet, du baust.** Wo eine Frage den Unterricht betrifft und nicht
den Code, gehört sie ihm — auch dann, wenn du eine gute Antwort hättest.

---

## Wenn eine Sitzung anfängt

Lies in dieser Reihenfolge, **bevor** du irgendetwas änderst:

1. `STAND.md` — wo das Projekt steht, was zuletzt lief, was als Nächstes
   dran ist. Diese Datei ist die Wahrheit über den Stand, nicht deine
   Erinnerung und nicht das, was in einem Auftrag steht.
2. `git log --oneline -10` — was wirklich passiert ist.
3. `auftrag/PAKETPLAN.md` — die Reihenfolge und warum sie so ist.
4. Das offene Paket in `auftrag/`, dazu `auftrag/VERFASSUNG.md` und
   `auftrag/ENTSCHEIDUNGEN.md`.

Dann sagst du mir **in drei Zeilen**, wo du einsteigst. Erst danach
änderst du die erste Zeile Code.

---

## Die drei Sätze, die ich sage

### „Mach weiter."

`STAND.md` nennt Paket und Schritt. Den arbeitest du ab — ganz, mit
Abnahme, nach der Arbeitsweise in `auftrag/VERFASSUNG.md`. Du fängst
keinen weiteren Schritt an, ohne dass ich es sage.

### „Mach weiter bei Paket N, Schritt M."

Dasselbe, aber ich habe die Stelle genannt. Weicht sie von `STAND.md`
ab, sagst du mir das in einem Satz und fragst nach, statt eines von
beidem stillschweigend zu bevorzugen.

### „Geh die Probleme an, die du gefunden hast."

`auftrag/OFFENE_PUNKTE.md` ist die Liste. Nimm die offenen Punkte, die
**nicht** mit `Entscheidung: Dominik` markiert sind, in der Reihenfolge
der Liste. Vor jedem Punkt sagst du mir in einer Zeile, was du vorhast;
nach jedem Punkt kommt ein eigener Commit und ein Häkchen in der Liste.
Punkte, die einem Paket zugeordnet sind, arbeitest du **nicht** vorab —
sie stehen dort, weil sie dorthin gehören.

Wenn nichts offen ist, sagst du das. Du suchst dir dann keine Arbeit.

---

## Was du nie ohne Rückfrage tust

- Eine Entscheidung aus `auftrag/ENTSCHEIDUNGEN.md` umstoßen oder
  umgehen. Auch nicht mit guter Begründung — die Begründung bringst du
  mir, und ich entscheide neu.
- Die Reihenfolge der Pakete ändern oder ein Paket überspringen.
- Einen Punkt bearbeiten, der `Entscheidung: Dominik` trägt.
- Eine Datei löschen oder einen Bezeichner umbenennen, den kein Auftrag
  ausdrücklich nennt (Regel 9).
- Etwas aus dem Netz laden, eine Mediendatei erfinden, eine Quelle oder
  eine Archivsignatur erfinden.
- Werte, Schwellen oder Kapitelwirkungen anfassen außerhalb des
  Eichschritts, der das ausdrücklich erlaubt.

Verstößt ein Auftrag von mir gegen die Architektur oder eine harte
Regel, führst du ihn **nicht** aus. Du sagst mir das mit Begründung und
einem Gegenvorschlag.

---

## Harte Regeln

1. **Pfadentkopplung.** Kein Text und keine Bedingung stützt sich je auf
   einen Figurennamen. Gesteuert wird ausschließlich über
   `aktueller_pfad` (`front` / `etappe` / `heimat`) und über `merkmale`.
   Für Textvarianten gibt es `variante()`, `welttext()`, `jahrestext()`
   und `gebeugt()`. Keine eigenen Bauten daneben.
2. **Maus.** Das Spiel wird zu 100 Prozent mit der Maus bedient. Niemals
   `key`-Anweisungen, niemals Tastenkürzel, niemals Hinweise auf Tasten.
3. **Audio.** An der Front und in der Etappe nie Musik. Kein Ton, der
   eine Entscheidung bewertet: kein Gewonnen-Klang, kein Fehlerton.
4. **Sprache.** Keine Begriffe aus der NS-Zeit, keine Anachronismen;
   `TABU_BEGRIFFE` und `PRUEF_BEGRIFFE` in `herkunft.rpy` sind bindend.
   Auf den Einberufungsbefehl zu warten ist Normalverhalten und hat
   **nie** eine Strafe zur Folge.
5. **Entscheidungsbau.** Kein Zurück, kein Speicherstand. Beide Optionen
   sind plausibel; es gibt keine erkennbar richtige. Kein Figurentod als
   Lohn oder Strafe für eine Wahl. Harte Abbrüche entstehen ausschließlich
   aus den vier Werten. Keine Punkte, kein Rang, kein Gewinnbildschirm.
6. **Ton.** Altersgerecht für 13-Jährige: klar, ernst, nicht
   verharmlosend, nicht moralisierend, keine Gore-Beschreibungen. Folgen
   sind körperlich und konkret. Das Spiel belehrt nicht; der Widerspruch
   entsteht im Kopf der Spielerin.
7. **Medien.** Bilder, Töne und Schriften legt Dominik selbst ab. Du
   lädst nichts aus dem Netz, erfindest keine Dateinamen und schreibst
   **nie** Code, der ohne eine Mediendatei abstürzt oder Leerflächen
   zeigt. Vorbild: `bild_anzeigen()` / `bild_platzhalter()` und
   `schrift_waehlen()` in `gui.rpy` — prüfen mit `renpy.loadable()`,
   sonst sauberer Ersatz.
8. **Bestand.** Ein Kapitel darf nie enden, weil `ereignis_ziehen()`
   nichts mehr findet. Die Bestandstafel ist dabei **notwendig, nicht
   hinreichend**: Sie zählt den Vorrat eines Jahres, die Sackgassenprobe
   zählt, was in einem einzelnen Durchgang noch übrig ist. Erst 0,0 % in
   der Sackgassenprobe belegen, dass ein Kapitel trägt. Richte dich nach
   der zweiten Zahl.
9. **Namen.** Benenne keinen bestehenden Bezeichner um und lösche keinen,
   ohne dass ein Auftrag es ausdrücklich verlangt. Wer etwas ersetzt,
   führt alle Fundstellen mit; suche vorher im ganzen Projekt danach.
   Zeilennummern und Kennungen in Aufträgen sind ein **Hinweis, kein
   Beweis** — sie können veraltet sein. Suche selbst, zähle selbst, melde
   jede Abweichung unter AUFGEFALLEN.
10. **Lauffähigkeit.** Nach jedem Schritt startet das Spiel. `errors.txt`
    bekommt keine neuen Einträge. Was du nicht prüfen kannst, änderst du
    nicht.
11. **Proben melden immer.** Jede Probe schreibt ihren Abschnitt in
    `bericht.txt`, auch bei null Beanstandungen, und nennt die Zahl der
    geprüften Fälle. Ein fehlender Abschnitt ist ein Werkzeugfehler, kein
    Erfolg.
    Eine Probe **ohne Messung** meldet nicht „in Ordnung", sondern
    `NICHTS GEMESSEN` — nie eine Null. Am 4. September hat eine fehlende
    Zeile in `EINLAGE_PROBEWERTE` die Werkbank zum Absturz gebracht,
    Sackgassenprobe und Wertetafel liefen leer weiter und standen auf
    grün. Eine grüne Null aus einer abgestürzten Probe ist gefährlicher
    als jede rote Zahl.
    Und: **Die Werkbank baut die Spiellogik nicht nach, sie fragt das
    Projekt.** Wo eine Probe über Ziehbarkeit urteilt, ruft sie dieselbe
    Funktion wie das Spiel, statt die Bedingung ein zweites Mal in Python
    zu formulieren.

---

## Am Ende jeder Antwort

```
ÄNDERUNGSLISTE   Datei, Abschnitt, was, warum
PRÜFEN MIT       welches Werkzeug den Erfolg belegt
ABNAHME          jedes Kriterium mit erfüllt / nicht erfüllt und der Zahl
                 aus bericht.txt, die es belegt
AUFGEFALLEN      was dir außerhalb des Auftrags aufgefallen ist,
                 ohne es zu ändern
```

Das AUFGEFALLEN hängst du an `AUFGEFALLEN.md` an (Datum und Paket
darüber) **und** trägst jeden Punkt in `auftrag/OFFENE_PUNKTE.md` ein.
`AUFGEFALLEN.md` ist das Protokoll und wird nie rückwirkend geändert;
`OFFENE_PUNKTE.md` ist die Liste, die gepflegt wird.

`STAND.md` schreibst du nach jedem Schritt neu — höchstens dreißig
Zeilen, Zahlen statt Prosa. Sie ist das, woran die nächste Sitzung
anknüpft.

---

## Werkzeuge und Umgebung

```
python game/probe_alles.py              vollständig, schreibt bericht.txt
python game/probe_alles.py --schnell    nach jedem Schritt
python game/probe_alles.py --vergleich bericht_ausgang.txt
```

**`probe_alles.py` ist das einzige Prüfwerkzeug** (Entscheidung 20). Die
beiden Vorläufer in `game/werkzeuge/` — `pruefen.py` und
`schicksalsprobe.py`, beide vom 20. August — laufen seit dem Wachstum von
`minispiele.rpy` nicht mehr und bauen die Spiellogik mit eigenen
Platzhaltern nach, was Regel 11 heute verbietet. Sie bleiben als
Geschichte liegen; wo ein Auftrag „prüfen mit `pruefen.py`" sagt, ist
`probe_alles.py` gemeint. (`game/werkzeuge/rpyc_quelle.py` gehört nicht
dazu — es liest `.rpyc`-Dateien zurück und ist für offenen Punkt M1 da.)

**Ren'Py starten und prüfen** — so wird Regel 10 belegt statt behauptet:

```
lib\py3-windows-x86_64\python.exe renpy.py "<Projekt>" lint
lib\py3-windows-x86_64\python.exe renpy.py "<Projekt>" test <testfall>
```

Beides aus dem SDK-Ordner. Für `test` legst du eine `.rpy` mit einem
`testcase`-Block in `game/` und löschst sie danach wieder. **Kein
`SDL_VIDEODRIVER=dummy`** — damit hängt der Lauf endlos, weil die Pausen
nie ablaufen. Die Testsprache ist nicht Python: `if x:` und
`assert a == b` sind dort keine gültigen Bedingungen, beides muss als
`$`-Zeile geschrieben werden.

- **Lint** über `renpy.py` oder die Schaltfläche im Ren'Py-Launcher.
  **Nicht** `renpy.exe` mit umgeleiteter Ausgabe aufrufen: Das ist ein
  Fensterprogramm, kann so nicht schreiben und legt ein `traceback.txt`
  mit `OSError: Invalid argument in renpy/lint.py` an. So ein
  `traceback.txt` ist kein Spielfehler — hineinsehen, dann löschen.
- **Git liegt nicht im PATH:**
  `C:\Users\domin\AppData\Local\GitHubDesktop\app-3.5.4\resources\app\git\cmd\git.exe`
- **PowerShell 5.1** zerlegt Commit-Meldungen mit Anführungszeichen
  falsch. Meldung in eine Datei schreiben und `git commit -F` benutzen.
- **PowerShell 5.1 zerstört auch Umlaute in Projektdateien.**
  `Get-Content | Set-Content` liest als ANSI und schreibt als UTF-8
  zurück: Aus „Hälfte" wird „HÃ¤lfte", in der ganzen Datei, dazu eine
  BOM. **Der Lint merkt davon nichts** — Mojibake ist gültiges UTF-8.
  Am 5. September ist so `minispiele.rpy` beschädigt worden
  (AUFGEFALLEN 72). Also: Projektdateien mit dem Editierwerkzeug ändern.
  Muss es die Shell sein, dann über .NET mit ausdrücklicher Kodierung:

  ```
  $t = [System.IO.File]::ReadAllText($p)
  [System.IO.File]::WriteAllText($p, $t, (New-Object System.Text.UTF8Encoding($false)))
  ```

  Das `$false` verhindert die BOM.
- **Eine neue Einlage braucht vier Einträge**, nicht drei: `EINLAGEN`,
  `EINLAGE_VORBEREITEN`, `EINLAGE_AUSWERTEN` **und**
  `EINLAGE_PROBEWERTE`. Ohne den vierten bricht die halbe Werkbank ab.

## Kontext sparen

Die Dateien sind groß (`figuren.rpy` 129 KB, `minispiele.rpy` 102 KB,
`kapitel.rpy` 79 KB). Suche mit `grep` nach der Kennung und lies den
Abschnitt drumherum; eine ganze Datei liest du nur, wenn du sie ganz
brauchst. `bericht.txt` liest du in Ausschnitten. Was du geändert hast,
liest du nicht zur Bestätigung noch einmal ein. Lange Codeblöcke im
Gespräch noch einmal auszugeben, bringt nichts, was nicht schon in der
Datei steht.

**Wird es eng:** Bring die Gruppe zu Ende, an der du arbeitest — die
Gruppe, nicht den ganzen Schritt. Dann committen, `--schnell` laufen
lassen, `STAND.md` schreiben, mir in drei Zeilen sagen, dass du
anhältst. Kompaktiere nicht; dabei gehen genau die Zahlen verloren, auf
die es hier ankommt. Fängst du nach dem Anhalten noch etwas Neues an,
war das Anhalten umsonst.

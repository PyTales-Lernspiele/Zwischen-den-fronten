<!-- Erzeugt aus bau/. Nicht von Hand ändern - die Änderung
     wäre beim nächsten Bauen weg. Melde stattdessen unter AUFGEFALLEN. -->

# Paket 8 - MEDIEN, RÜCKMELDUNG, GLOSSAR

> **Vor diesem Paket gelesen:** `STAND.md`, `git log --oneline -10`,
> `auftrag/VERFASSUNG.md`, `auftrag/ENTSCHEIDUNGEN.md`.
> **Nach jedem Schritt:** Commit, `probe_alles.py --schnell`, Kurzmeldung,
> `STAND.md` und `auftrag/OFFENE_PUNKTE.md` nachziehen.

## Überblick

```text
Drei Schritte Politur an der Oberfläche, die das Spiel im Klassenzimmer
brauchbar machen: das Medienverzeichnis mit Kartentypen und Schriften,
die Rückmeldung der Werte samt Onboarding und Tongerüst, und das
Glossar mit den Quellenkarten.
Sie gehören zusammen, weil alle drei dieselben Bildschirme anfassen -
entscheidungskarte, karten_ausgang, das Hauptmenü. Getrennt bearbeitet
würden sie sich gegenseitig überschreiben.
```

## Die Schritte

1. MEDIENVERZEICHNIS, KARTENTYPEN, SCHRIFTEN
2. WERTEFEEDBACK, ONBOARDING, RHYTHMUS, TON
3. GLOSSAR UND QUELLENKARTEN

Jeder Schritt hat seine eigene Abnahme. Die Gesamtabnahme steht unten.

---

## Schritt 1 von 3 - MEDIENVERZEICHNIS, KARTENTYPEN, SCHRIFTEN

```text
BEFUND
Probe 6: 214 erwartete Dateipfade, 7 vorhanden, 207 fehlen. Alle sechs
Schriftdateien fehlen; es greift überall DejaVuSans.ttf. Außerdem
meldet der Bericht:
  vorhanden, aber von keiner Stelle erwartet:
      audio/stummer_morgen.mp3
      images/karten/front_beginn_1.png
      images/karten/front_beginn_2.png
  in BILD_MASSE angelegt, aber nie abgerufen:
      personen (600x1200), orte (1920x1080), dokumente (900x600)
Das Spiel stürzt deswegen nirgends ab - überall greift ein Ersatz. Es
fehlt aber eine Liste, mit der sich das Material sammeln lässt.

AUFGABE
1. SKRIPT medienbedarf.py
   Erzeugt MEDIEN.md neben den .rpy-Dateien. Aufbau:
   - Nach Kategorie gruppiert (fonts, images/karten, images/portraits,
     images/figuren, audio).
   - Je Eintrag: erwarteter Pfad, wo im Code er erwartet wird, Status
     (vorhanden / fehlt), Anzeigemaß aus BILD_ANZEIGE.
   - Je Eintrag zwei bis drei Suchbegriffe für die Recherche in Archiven,
     deutsch und englisch, dazu die Rechtelage, soweit bekannt.
     Bevorzugte Häuser: Deutsches Historisches Museum / LeMO,
     Bundesarchiv, Europeana 1914-1918, Landesarchive.
   - Ein Abschnitt "Vorhanden, aber unbenutzt" mit den drei Dateien oben
     und dem Vorschlag, wo sie hingehören könnten.
   - Eine Kopfzeile mit Gesamtzahlen.
   Erfinde keine Signaturen und keine Bildnachweise.
2. KLÄRUNG DER DREI BILDMASSE
   Entscheide je Kategorie: wird sie noch gebraucht oder fällt sie weg?
   Was bleibt, bekommt mindestens eine aufrufende Stelle. Was fällt,
   wird mit Begründung entfernt.
3. KARTENTYPEN
   Führe Ereignis.kartentyp ein mit den Werten "karte", "feldpost",
   "lebensmittel", "zeitung", "amtlich". Vorgabe ist "karte". Baue die
   fünf Layouts in entscheidungskarte ausschließlich mit Ren'Py-
   Bordmitteln:
     karte         wie bisher
     feldpost      schmaler Bogen, SCHRIFT_DOKUMENT, Faltlinie als
                   dünne Linie, Feldpostnummer statt Ort
     lebensmittel  Kartenraster mit abgetrennten Abschnitten, gestrichelt
     zeitung       zwei Spalten, Balkenüberschrift, engerer Zeilenabstand
     amtlich       Kopf mit Behördenzeile, Aktenzeichen rechts oben,
                   Stempelfeld unten
   KEINE externen Bilddateien erzwingen. Wo ein Motiv fehlt, greift
   bild_platzhalter() wie bisher.
   Vergib den Typ für alle bestehenden Ereignisse, die erkennbar ein
   Dokument sind.
4. VIERTE SCHRIFT
   SCHRIFT_SCHMAL für Stempel und Aktenzeichen, nach dem Muster von
   schrift_waehlen() mit Ersatz auf SCHRIFT_DOKUMENT. Kandidaten:
   fonts/schmal.ttf, fonts/schmal.otf.
5. KONTRAST FÜR DEN BEAMER
   Rechne für jede Kombination aus Textfarbe und Untergrund, die im Spiel
   vorkommt, das Kontrastverhältnis nach WCAG aus. Verlangt sind
   mindestens 7:1, weil im Klassenzimmer das Licht an ist. Gib eine
   Tabelle aus: Farbpaar, Verhältnis, bestanden ja/nein. Wo es nicht
   reicht, schlage eine angepasste Farbe vor - ändere sie erst nach
   meiner Zustimmung, weil die Farbwelt das Gesicht des Spiels ist.

ABNAHME DIESES SCHRITTS
  - MEDIEN.md liegt vor und nennt alle 214 Pfade plus die drei unbenutzten
    Dateien.
  - Probe 6 zählt nach der Einführung von SCHRIFT_SCHMAL entsprechend
    mehr erwartete Pfade; die Zahl stimmt mit MEDIEN.md überein.
  - Alle fünf Kartentypen sind ohne eine einzige Bilddatei sichtbar
    verschieden. Zeige je einen Bildschirmabzug.
  - Die Kontrasttabelle liegt vor.

PRÜFEN MIT: medienbedarf.py und probe_alles.py.
```

---

## Schritt 2 von 3 - WERTEFEEDBACK, ONBOARDING, RHYTHMUS, TON

```text
TEIL A - WERTEFEEDBACK
1. Auf karten_ausgang schweben die geänderten Werte kurz nach oben:
   wert_schwebt() aus Paket 7, Schritt 1, mit Plus- oder Minuszeichen und der Zahl.
2. Die Farbe richtet sich nach WERT_HOCH_IST_GUT, nicht nach dem Vorzeichen:
   versorgung -1 ist schlecht, belastung -1 ist gut. Nutze
   wirkung_zeilen() (kapitel.rpy) als Grundlage, damit die Logik nur an
   einer Stelle steht.
3. Kein Ton dazu. Keine Wertung im Text, nur der Wert und sein Name.
4. Ändert sich nichts, erscheint auch nichts. Kein "0".

TEIL A2 - EINE RICHTUNG FÜR ALLE VIER WERTE
Heute sind zwei Werte gut, wenn sie hoch sind (versorgung, rueckhalt), und
zwei schlecht (belastung, aufmerksamkeit). Wer in 45 Sekunden entscheidet,
muss die Richtung im Kopf umdrehen. Was das kostet, steht im Bericht:
zwischen zufälliger und aufmerksamer Wahl liegen 19,2 Prozentpunkte an der
Front und 29,2 in der Heimat.
Ab jetzt gilt in der ANZEIGE: ein voller Balken heißt überall "hier
stehst du gut da".
5. Nur die Anzeige dreht sich, nicht die Rechnung. WERT_HOCH_IST_GUT,
   ENDE_SCHWELLEN, stufe_von_wert() und sämtliche aenderungen bleiben
   unverändert. probe_alles.py muss danach exakt dieselben Zahlen liefern
   wie davor - das ist die Abnahme dieses Teils.
6. Für belastung und aufmerksamkeit zeichnet der Balken WERT_MAXIMUM
   minus Wert. Nur an der zeichnenden Stelle, nicht im Zustand.
7. Namen und Zustandssätze bleiben, wie sie sind: über dem Balken steht
   weiter "Erschöpfung", darunter "Am Ende". Die Wörter tragen die
   Sache, der Balken die Richtung.
8. Die Stufenfarbe hängt weiter an der Stufe, nicht am Rohwert - Stufe 0
   ist immer die gute Lage.
9. Geh ALLE Stellen durch, die einen Wertbalken zeichnen: zustandsblock,
   zustandskopf, werthinweis, der Lebenslauf, der Jahresabschluss und das
   Wertefeedback aus Teil A. Eine vergessene Stelle ist schlimmer als gar
   keine Änderung.
10. Der Hover-Text erklärt es in einem Satz: "Der Balken zeigt, wie viel
   dir noch bleibt."

TEIL A3 - LESBARKEIT UND BEDIENUNG
11. SCHRIFTGRÖSSE. Eine Einstellung im Spielmenü mit drei Stufen:
   normal, groß, sehr groß. Sie zieht gui.text_size und die
   Kartenschriften mit. In der letzten Reihe sitzt jemand sechs Meter vom
   Beamer entfernt. Nur mit der Maus bedienbar.
   Prüfe bei "sehr groß", dass keine Karte überläuft: Text, der nicht
   mehr passt, scrollt in seinem eigenen Bereich - er wird nicht
   abgeschnitten, und die Karte wächst nicht über den Bildschirm hinaus.
12. VORLESEN. Ren'Py bringt eine Vorlesefunktion mit (self-voicing). An
   einer Oberschule sitzen in jeder Klasse Schüler, denen Lesen schwer
   fällt; für sie entscheidet das darüber, ob sie mitkommen.
   Mach sie über eine Schaltfläche im Spielmenü erreichbar, mit einem
   erklärenden Satz. KEIN Tastenhinweis (Regel 2), auch wenn Ren'Py
   selbst einen nennt. Prüfe, dass die Kartentexte, die Optionen und die
   Ausgangstexte tatsächlich vorgelesen werden, und sag mir, was nicht
   geht.

TEIL B - ONBOARDING
5. hinweis_unumkehrbar wird auf drei prägnante Sätze gekürzt. Inhalt:
   es gibt kein Zurück, es gibt keinen Speicherstand, es gibt keine
   richtige Antwort.
6. Die drei Sätze bekommen je ein Element, das beim Überfahren mit der
   Maus einen Satz mehr zeigt - für die, die es genauer wissen wollen.
   Keine Tastenhinweise.
7. Prüfe, ob eine Schülerin ohne Anleitung erkennt, dass die vier Werte
   in der Kopfleiste anklickbar sind. Wenn nicht, mach es sichtbar - ein
   ruhiger Hinweis beim ersten Kapitel genügt.
   DAS IST KEIN ZIERRAT, UND ES IST GEMESSEN: Zwischen zufälliger und
   aufmerksamer Wahl liegen im kurzen Verlauf 19,2 Prozentpunkte an der
   Front und 29,2 in der Heimat. Wer die Kopfleiste liest, kommt spürbar
   weiter. Wer sie übersieht, verliert - ohne je zu erfahren, warum.

TEIL C - RHYTHMUS
8. Im langen Verlauf ist in jedem Kapitel mindestens eine Einlage und
   mindestens ein Brief garantiert. Heute regelt das der Zufall
   (EINLAGE_CHANCE 45, POST_CHANCE je Jahr 20 bis 35), und Probe 2 zeigt
   die Folge: im langen Frontverlauf kommen 2,82 Einlagen und 2,27 Briefe
   auf sechs Kapitel - rechnerisch bleiben also mehr als drei Kapitel ohne.
   Baue eine Nachziehregel: Ist ein Kapitel ohne Einlage oder ohne Brief zu
   Ende gegangen, wird im nächsten mit Sicherheit gezogen.
9. Im kurzen Verlauf gilt dasselbe für mindestens die Hälfte der Kapitel.
10. Miss die Verteilung in probe_alles.py nach der Änderung und gib sie
    je Pfad und Verlauf aus.

TEIL D - TONGERÜST
11. Funktion ton_spielen(kennung) mit Prüfung über renpy.loadable().
    Fehlt die Datei, geschieht nichts - kein Fehler, keine Meldung im
    Spiel, aber ein Eintrag in der Medienprobe.
12. Tabelle ORTSKLANG: je Ort ein Umgebungsklang, mit Dateiname,
    Lautstärke und der Angabe, ob er sich wiederholt.
13. HARTE CODESPERRE: Auf den Pfaden front und etappe wird niemals Musik
    abgespielt. Nicht als Vereinbarung, sondern als Abfrage in
    ton_spielen(), die den Aufruf verwirft und in der Probe zählt.
    Umgebungsklänge sind erlaubt, Musik ist es nicht - definiere den
    Unterschied im Kommentar.
14. Kein Ton bewertet eine Entscheidung. Keine Erfolgs- und keine
    Fehlerklänge, nirgends.
15. audio/stummer_morgen.mp3 liegt bereits im Projekt und wird von keiner
    Stelle aufgerufen. Entscheide, wohin er gehört, oder vermerke ihn in
    MEDIEN.md als unbenutzt.

ABNAHME DIESES SCHRITTS
  - Alle vier Balken füllen sich in dieselbe Richtung, und probe_alles.py
    liefert dabei exakt dieselben Zahlen wie vorher.
  - Bei "sehr groß" läuft keine Karte über.
  - Die Vorlesefunktion ist über eine Schaltfläche erreichbar und liest
    Karten, Optionen und Ausgangstexte.
  - Wertefeedback erscheint farbrichtig; belege es für alle vier Werte in
    beide Richtungen.
  - Probe 2 nach der Änderung: kein Kapitel im langen Verlauf ohne
    Einlage und ohne Brief.
  - Probe: ton_spielen() gibt auf front und etappe null Musikaufrufe frei.
  - probe_alles.py sonst unverändert.

PRÜFEN MIT: probe_alles.py, ein langer Durchgang je Pfad von Hand.
```

---

## Schritt 3 von 3 - GLOSSAR UND QUELLENKARTEN

```text
VORAUSSETZUNG
Paket 3, Schritt 1 hat allen Ereignissen und Einlagen ein quelle-Dict gegeben. Dieses
Paket macht es sichtbar. Neue Bestände gehören nach didaktik.rpy, die
Bildschirme nach screens.rpy.

TEIL A - GLOSSAR
1. Neue Datei didaktik.rpy mit dem Bestand GLOSSAR. Je Begriff:
     "kurz"      ein Satz, für die Anzeige beim Überfahren mit der Maus
     "lang"      drei bis fünf Sätze für die Detailansicht
     "zeitwort"  wahlweise: der zeitgenössische Begriff, falls das
                 Stichwort ein heutiger ist
     "siehe"     wahlweise: verwandte Stichwörter
2. DIE VERTIEFUNGEN AUS PAKET 12 AUFNEHMEN. Beim Kürzen der Einlagen-
   Einordnungen ist Fachinformation in Felder namens "vertiefung"
   ausgelagert worden. Sie gehört hierher: in den langen Text des
   passenden Stichworts und in die Quellenkarte der jeweiligen Einlage.
   Geh die sechs Einordnungen durch und weise für jede nach, wo ihre
   Vertiefung jetzt steht. Erst danach darf das Feld verschwinden.
3. Aufzunehmen sind alle historischen Fachbegriffe, die im Spiel
   vorkommen. Geh dafür den gesamten Textbestand durch - nicht aus dem
   Gedächtnis. Mindestens: Musterung, garnisonsverwendungsfähig,
   unabkömmlich, Landsturm, Landwehr, Etappe, Feldpost,
   Hilfsdienstgesetz, Brotkarte, Steckrübenwinter, Kriegsanleihe,
   Belagerungszustandsgesetz, Schutzhaft, Kriegsgericht,
   Majestätsbeleidigung, Ablieferungspflicht, Akkord, Liebesgaben,
   Arbeiter- und Soldatenrat, Waffenstillstand.
3a. HEIKLE BEGRIFFE MIT BESONDERER SORGFALT. Einige Stichwörter tragen
   eine Vorgeschichte, die über 1918 hinausreicht. Das wichtigste ist die
   Zählung vom Oktober 1916, an die front_1916_zaehlung anknüpft. Sie
   gehört ins Glossar, und zwar mit dem zeitgenössischen Namen, einer
   nüchternen Beschreibung dessen, was angeordnet wurde, und dem
   Hinweis, dass das Ergebnis nie veröffentlicht wurde. Kein Ausblick auf
   die Zeit nach 1918 - der gehört in den Unterricht, nicht ins Spiel.
   Geh den Bestand nach weiteren solchen Begriffen durch und behandle sie
   gleich sorgfältig. Nenne mir die Liste, bevor du sie schreibst.
4. SPRACHE: 13 bis 14 Jahre. Keine Spoiler auf den Spielverlauf, keine
   Wertung, keine Bezüge auf spätere Jahrzehnte. Das Sprachmaß aus der
   Verfassung gilt und wird von Probe 8 geprüft.
5. Anzeige: Beim Überfahren eines markierten Begriffs erscheint "kurz".
   Ein Klick öffnet "lang". Ausschließlich Maus. Der Spielfluss wird
   nicht angehalten - die Karte bleibt sichtbar.
6. Ein Sammelbildschirm listet alle bisher begegneten Begriffe, alphabetisch.

TEIL B - QUELLENKARTEN
6. Schaltfläche "Woher wissen wir das?" auf dem Ausgangsbildschirm jeder
   Karte. Sie zeigt das quelle-Dict: kurz, art, Zitat (falls vorhanden),
   Einordnung in zwei Sätzen, Vollbeleg klein darunter.
7. Steht dort "BELEG FEHLT - zu recherchieren", zeigt die Karte das
   ehrlich an: "Für diese Karte fehlt noch ein Beleg." Nichts
   beschönigen.
8. Sammelbildschirm für Quellen, erreichbar aus dem Hauptmenü - auch
   ohne einen einzigen Spieldurchgang. Sortierbar nach art. Das ist die
   Ansicht, mit der eine Lehrkraft die Stunde vorbereitet.
9. Bewegung: Die Quellenkarte kommt mit karte_kommt() und geht mit
   karte_geht(). Kein neuer Bildschirmwechsel, sie legt sich über die
   Karte.

TEIL C - VERBINDUNG
10. Begriffe im Quellentext werden ebenfalls markiert. Glossar und
    Quellenkarte greifen ineinander, ohne sich gegenseitig zu öffnen -
    höchstens eine Ebene tief.

ABNAHME DIESES SCHRITTS
  - Jeder in den Texten vorkommende Fachbegriff steht im Glossar; belege
    das mit einer Suche über den Textbestand, nicht mit einer Behauptung.
  - Jede Karte hat die Schaltfläche; wo der Beleg fehlt, steht es da.
  - Der Quellensammelbildschirm ist aus dem Hauptmenü erreichbar.
  - Probe 8: alle Glossartexte innerhalb des Sprachmaßes.
  - Sprachprobe ohne Beanstandung.

PRÜFEN MIT: probe_alles.py, ein Durchgang von Hand mit geöffnetem
Glossar, Aufruf des Quellenbildschirms aus dem Hauptmenü.
```

---

## Gesamtabnahme

```text
- Alle 3 Schritte haben ihre eigene Abnahme bestanden; nenne je
  Schritt das entscheidende Kriterium und die Zahl dazu.
- python probe_alles.py (vollständig, ohne --schnell) läuft durch.
- python probe_alles.py --vergleich bericht_ausgang.txt zeigt für
  jede Probe: früher, heute, Differenz. Keine Probe ist schlechter
  geworden. Wo eine schlechter wurde, begründest du sie einzeln.
- Das Spiel startet, errors.txt und traceback.txt sind leer.
- STAND.md, auftrag/OFFENE_PUNKTE.md und auftrag/PAKETPLAN.md sind
  auf dem Stand nach diesem Paket.
```

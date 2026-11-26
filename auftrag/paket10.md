<!-- Erzeugt aus bau/. Nicht von Hand ändern - die Änderung
     wäre beim nächsten Bauen weg. Melde stattdessen unter AUFGEFALLEN. -->

# Paket 10 - SCHULFASSUNG - EXPORT, LEHRKRAFTMATERIAL, ABNAHME

> **Vor diesem Paket gelesen:** `STAND.md`, `git log --oneline -10`,
> `auftrag/VERFASSUNG.md`, `auftrag/ENTSCHEIDUNGEN.md`.
> **Nach jedem Schritt:** Commit, `probe_alles.py --schnell`, Kurzmeldung,
> `STAND.md` und `auftrag/OFFENE_PUNKTE.md` nachziehen.

## Überblick

```text
Das letzte Paket. Schritt 1 baut den Protokoll-Export und das
Lehrkraftmaterial, Schritt 2 nimmt das ganze Spiel ab und packt die
Schulfassung.
Sie gehören zusammen, weil die Abnahme prüft, was Schritt 1 gerade
erst erzeugt hat, und weil beide dieselben zwölf Durchgänge von Hand
brauchen - die spielt man einmal, nicht zweimal.
```

## Die Schritte

1. PROTOKOLL-EXPORT UND LEHRKRAFTMATERIAL
2. ABNAHME UND SCHULFASSUNG

Jeder Schritt hat seine eigene Abnahme. Die Gesamtabnahme steht unten.

---

## Schritt 1 von 2 - PROTOKOLL-EXPORT UND LEHRKRAFTMATERIAL

```text
TEIL A - PROTOKOLL FÜR DEN UNTERRICHT
1. Am Ende des Lebenslaufs eine Schaltfläche, die ein druckfertiges
   .txt-Protokoll schreibt. Zeilenbreite genau 72 Zeichen, damit es ohne
   Nacharbeit auf eine Seite passt.
2. Dateiname mit Zeitstempel, Ablage in einem Ordner, den eine Schülerin
   auf einem Schulrechner beschreiben darf. Prüfe das ausdrücklich für
   Windows und weiche im Zweifel auf das Verzeichnis aus, das Ren'Py für
   Spielstände benutzt. Schlägt das Schreiben fehl, sagt das Spiel das
   ruhig und bietet die Anzeige am Bildschirm an.
3. Inhalt in dieser Reihenfolge:
     - Kopf: Datum, Lebenslage (Herkunft, Alter, Geschlecht, Erwerb),
       Pfad, Verlauf
     - Entscheidungsverlauf: je Jahr die gezogenen Ereignisse und die
       gewählte Option, ein Zeile je Entscheidung
     - Einlagen und Briefe, knapp
     - Endwerte mit Stufennamen, der Ausgang, die Nachklänge
     - Die Wahl in der Wirtshausszene
     - Fünf offene Reflexionsfragen, die sich auf DIESEN Durchgang
       beziehen und aus den gesammelten Merkmalen gebildet werden - keine
       feste Liste. Offene Fragen, keine Wissensfragen, keine Fragen mit
       einer richtigen Antwort.
4. Keine personenbezogenen Daten. Kein Name, keine Kennung des Rechners,
   keine Uhrzeit außer dem Datum.

TEIL B - LEHRKRAFT.md
Erstelle die Datei im Projektstamm. Abschnitte:
  1. Was das Spiel ist und was es nicht ist (eine halbe Seite).
  2. Zeitbedarf: Einzelstunde mit kurzem Verlauf, Doppelstunde mit langem
     Verlauf. Nimm die in Paket 2, Schritt 3 gemessenen Zeiten, nicht geschätzte.
     Dazu je ein Vorschlag für den Stundenverlauf mit Minutenangaben.
  3. Lehrplanbezug für Klasse 8 der Oberschule. Nutze die
     lehrplan-Felder, die in kapitel.rpy bereits an den Ausgängen stehen
     (ENDE_AUSGAENGE), und führe sie zusammen. Nenne den Lehrplan, auf
     den du dich stützt, und wenn du ihn nicht sicher kennst, schreib das
     hin, statt ihn zu erfinden.
  4. Die vier Werte und was sie abbilden - eine Seite für die Auswertung
     an der Tafel. Nimm die gemessene Zahl mit auf: Zwischen zufälliger
     und aufmerksamer Wahl liegen im kurzen Verlauf 19 bis 29
     Prozentpunkte. Das ist das Argument dafür, die Kopfleiste im
     Unterricht einmal gemeinsam zu lesen, bevor gespielt wird.
  5. Umgang mit sensiblen Inhalten: Tod, Hunger, Denunziation, Verhaftung.
     Was im Spiel vorkommt, was nicht, und was zu tun ist, wenn eine
     Schülerin betroffen reagiert.
  6. Auswertung im Plenum: fünf Fragen, die auf jeden Durchgang passen,
     und ein Vorschlag, wie die unterschiedlichen Protokolle verglichen
     werden.
  7. Die Wirtshausszene als Kern der Auswertung: was sie zeigt, warum sie
     nicht belehrt, wie man darüber spricht.
  8. Technisches: Systemvoraussetzungen, Start, Bewegung abschalten,
     Protokoll finden, keine Internetverbindung nötig, keine
     Datenerhebung.
  9. Bekannte Lücken, ehrlich benannt, mit Verweis auf MEDIEN.md.

ABNAHME DIESES SCHRITTS
  - Der Export läuft unter Windows und erzeugt eine Datei, die sich ohne
    Nacharbeit ausdrucken lässt. Lege ein Beispiel bei.
  - Alle Zeilen des Protokolls sind höchstens 72 Zeichen lang; prüfe das
    programmatisch.
  - Die fünf Reflexionsfragen unterscheiden sich zwischen zwei
    verschiedenen Durchgängen; lege beide Beispiele bei.
  - LEHRKRAFT.md ist vollständig, ohne erfundene Lehrplanstellen.

PRÜFEN MIT: zwei vollständige Durchgänge von Hand mit Export, dazu eine
Prüfung der Zeilenbreite.
```

---

## Schritt 2 von 2 - ABNAHME UND SCHULFASSUNG

```text
ZWECK
Das letzte Paket macht aus dem Projekt ein Spiel, das eine Kollegin ohne
Rücksprache im Unterricht einsetzen kann. Es fügt keinen Inhalt hinzu.
Es prüft, packt und dokumentiert.

TEIL A - GESAMTABNAHME
1. Führe probe_alles.py ohne Schalter aus und stelle es
   bericht_ausgang.txt gegenüber. Gib die Tafel aus:
   je Probe die Zahl der Beanstandungen damals, heute, Differenz.
   Ziel ist überall null. Wo nicht: begründe jede verbleibende
   Beanstandung einzeln und sage, ob sie bleiben darf.
2. Spiele 12 vollständige Durchgänge von Hand: drei Pfade mal zwei
   Verläufe mal zwei Jahrgänge. Protokolliere je Durchgang: Dauer,
   Ausgang, aufgefallene Fehler, ob die Wirtshausszene kam, ob der Export
   lief.
3. Lint ausführen, errors.txt und traceback.txt prüfen. Beide müssen
   leer bleiben. Achtung: Ein traceback.txt mit "OSError: Invalid
   argument in renpy/lint.py" stammt vom Lint-Aufruf über renpy.exe mit
   umgeleiteter Ausgabe und ist kein Spielfehler. Sieh hinein, bevor du
   es als Fehler meldest.
4. Prüfe alle sieben Regeln der Verfassung einzeln nach und belege jede
   mit einer Messung oder einer Fundstelle:
     Pfadentkopplung   - kein Figurenname in Bedingungen oder Texten
     Maus              - keine key-Anweisung im ganzen Projekt
     Audio             - null Musikaufrufe auf front und etappe
     Sprache           - Sprachprobe ohne Beanstandung
     Entscheidungsbau  - kein Speicherstand, kein Zurück, keine Punkte
     Ton               - Probe 8 innerhalb des Sprachmaßes
     Medien            - kein Absturz bei fehlender Datei; teste, indem du
                         den Ordner images vorübergehend umbenennst

TEIL B - SCHULFASSUNG
5. Baue die Distribution für Windows über den Ren'Py-Launcher. Prüfe:
   - Der Ordner läuft von einem USB-Stick und aus einem Netzlaufwerk.
   - Das Spiel startet ohne Adminrechte und ohne Internetverbindung.
   - Es schreibt nur dorthin, wo ein Schulkonto schreiben darf.
   - Auf einem Rechner ohne die fehlenden Mediendateien sieht man
     Platzhalter, keine Fehler.
6. Setze eine Versionsnummer und ein Datum in options.rpy und auf den
   Startbildschirm.
7. Lege in den Distributionsordner: LEHRKRAFT.md, MEDIEN.md und eine
   kurze LIESMICH.txt mit drei Absätzen - Start, Bewegung abschalten,
   Protokoll finden.

TEIL C - WAS OFFEN BLEIBT
8. DREI OFFENE PUNKTE AUS PAKET 1, hier abschließend entscheiden:
   a) merkbuch.rpy ist eine Rekonstruktion. Die Kommentare stammen nicht
      aus dem Original. Ist die alte Fassung inzwischen aufgetaucht
      (anderer Rechner, Papierkorb oder Versionsverlauf der Cloud), dann
      tausche die Kommentare zurück und lass den Code stehen, der
      inzwischen geprüft ist. Ist sie nicht aufgetaucht, vermerke das in
      der Restliste.
   b) Zwei tote Namen in merkbuch.rpy: MERKBUCH_SORGE_AB (init -7) und die
      Vorgabe merkbuch_gewaehlt werden nirgends gelesen. Entscheide je
      Name: gehört er zu einer Absicht, die noch kommt, oder fällt er
      weg? Begründe und handle danach.
   c) Prüfe, ob der Projektordner inzwischen ein Git-Repository ist. Wenn
      nicht, richte es hier ein - die Schulfassung soll nicht der letzte
      Stand ohne Versionsgeschichte sein.
   d) heimat_1914_post heißt nach 1914, läuft aber auch 1915 und
      verlangt seit Paket 2, Schritt 3 ein Familienmerkmal. Die Kennung passt nicht
      mehr zu den Jahren. Sieh nach, ob es weitere Kennungen mit
      Jahreszahl gibt, deren jahre-Feld darüber hinausgeht, und gib die
      Liste aus. Umbenennen NUR, wenn du alle Fundstellen mitführst -
      im Zweifel gehört das in die Restliste, nicht in die
      Schulfassung.

9. Schreibe RESTLISTE.md: alles, was bewusst offen geblieben ist, nach
   Dringlichkeit sortiert, mit je einem Satz, was zu tun wäre und wie
   lange es dauern dürfte. Dazu die Zahl der noch fehlenden Medien aus
   MEDIEN.md.
10. Nenne mir die drei Stellen, an denen du das Spiel als nächstes
   verbessern würdest, wenn Zeit wäre - mit Begründung, ohne sie zu
   ändern.

ABNAHME DIESES SCHRITTS
  - Die Gegenüberstellung zu bericht_ausgang.txt liegt vor.
  - 12 Durchgänge protokolliert, kein Abbruch aus einem Fehler.
  - Distribution läuft vom Stick auf einem zweiten Rechner.
  - LEHRKRAFT.md, MEDIEN.md, LIESMICH.txt und RESTLISTE.md liegen im
    Distributionsordner.
  - errors.txt und traceback.txt leer.

PRÜFEN MIT: probe_alles.py --vergleich bericht_ausgang.txt, Lint, 12
Durchgänge von Hand, ein zweiter Rechner.
```

---

## Gesamtabnahme

```text
- Alle 2 Schritte haben ihre eigene Abnahme bestanden; nenne je
  Schritt das entscheidende Kriterium und die Zahl dazu.
- python probe_alles.py (vollständig, ohne --schnell) läuft durch.
- python probe_alles.py --vergleich bericht_ausgang.txt zeigt für
  jede Probe: früher, heute, Differenz. Keine Probe ist schlechter
  geworden. Wo eine schlechter wurde, begründest du sie einzeln.
- Das Spiel startet, errors.txt und traceback.txt sind leer.
- STAND.md, auftrag/OFFENE_PUNKTE.md und auftrag/PAKETPLAN.md sind
  auf dem Stand nach diesem Paket.
```

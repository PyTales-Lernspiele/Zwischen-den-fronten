<!-- Erzeugt aus bau/. Nicht von Hand ändern - die Änderung
     wäre beim nächsten Bauen weg. Melde stattdessen unter AUFGEFALLEN. -->

# Paket 7 - BEWEGUNG UND HANDGRIFFE

> **Vor diesem Paket gelesen:** `STAND.md`, `git log --oneline -10`,
> `auftrag/VERFASSUNG.md`, `auftrag/ENTSCHEIDUNGEN.md`.
> **Nach jedem Schritt:** Commit, `probe_alles.py --schnell`, Kurzmeldung,
> `STAND.md` und `auftrag/OFFENE_PUNKTE.md` nachziehen.

## Überblick

```text
Schritt 1 legt das Bewegungsvokabular in einer eigenen Datei an. Die
Schritte 2 und 3 bauen die vier Einlagen aus und benutzen es sofort.
Deshalb gehören sie in ein Paket: Die Transforms würden sonst
ungenutzt herumliegen, oder die Einlagen bekämen jede ihre eigene
Bastellösung.
Alles nur mit Ren'Py-Bordmitteln, keine einzige Bilddatei.
```

## Die Schritte

1. BEWEGUNG - EINE EIGENE DATEI FÜR ALLE ANIMATIONEN
2. HANDGRIFFE I - ROTSTIFT UND ACHT STRICHE
3. HANDGRIFFE II - TORNISTER UND FAHRT AUFS LAND

Jeder Schritt hat seine eigene Abnahme. Die Gesamtabnahme steht unten.

---

## Schritt 1 von 3 - BEWEGUNG - EINE EIGENE DATEI FÜR ALLE ANIMATIONEN

```text
BEFUND
Im ganzen Projekt gibt es heute vier Bewegungen: notify_erscheinen
(screens.rpy:1211), figur_spricht, figur_still und blase_blinken
(dialoge.rpy:943 ff.), dazu drei Dissolve-Aufrufe. Alles andere erscheint
hart. Ein Spiel, das aus Papier, Karten, Stempeln und Briefen besteht,
kann viel mehr - ohne eine einzige Bilddatei.

Dieses Paket legt das Bewegungsvokabular an, BEVOR die die Schritte 2 und 3 und die Pakete 8 und 9 es
benutzen. Es ändert keinen Text und keinen Wert.

NEUE DATEI: bewegung.rpy
Konstanten in einem "init -45 python:"-Block (nach gui.rpy bei -50, damit
die Farben stehen), die transform-Blöcke auf Dateiebene.

TEIL A - SCHALTER
1. persistent.bewegung mit drei Stufen: "voll" (Vorgabe), "sparsam",
   "aus".
2. Funktion bewegungszeit(sekunden): gibt bei "voll" den Wert zurück, bei
   "sparsam" 60 Prozent davon, bei "aus" 0.0. JEDE Bewegung im Projekt
   holt ihre Dauer hier. Keine fest eingetragene Sekundenzahl in einem
   Screen.
3. Eintrag im Spielmenü (screen preferences): drei Schaltflächen,
   ausschließlich mit der Maus bedienbar, mit einem erklärenden Satz.
   Überschrift "Bewegung".
4. Bei "aus" sieht man überall sofort den Endzustand. Nichts verschwindet,
   nichts wird übersprungen.

TEIL B - DAS VOKABULAR
Baue diese transforms mit Parameter für die Dauer, damit der Aufruf
"at karte_kommt(bewegungszeit(0.32))" lauten kann:

  karte_kommt(dauer=0.32)
      Die Entscheidungskarte legt sich auf den Tisch: aus yoffset 34,
      alpha 0.0 und rotate 1.2 mit easeout auf 0/1.0/0.0.
  karte_geht(dauer=0.22)
      Die gewählte Karte wird weggenommen: yoffset -18, alpha 0.0.
  stempel_setzt(dauer=0.22)
      Zoom 1.6 auf 0.97, dann in 0.06 auf 1.0; alpha 0 auf 1. Der
      Drehwinkel gehört NICHT in den transform, sondern wird beim
      Erzeugen fest gewürfelt und mitgegeben (siehe Schritt 2 dieses Pakets).
  wert_schwebt(dauer=1.1)
      Ein Plus- oder Minuszeichen steigt um 46 Pixel und wird
      durchsichtig. Farbe kommt von außen, nicht aus dem transform.
  strich_waechst(dauer=0.22)
      Wächst von links nach rechts auf: xzoom 0.0 auf 1.0, xanchor 0.0.
  kalenderblatt(dauer=0.5)
      Das Jahresblatt kommt von oben: yoffset -60 auf 0, alpha 0 auf 1,
      ease.
  umschlag_oeffnet(dauer=0.4)
      Zweiteilig: die Lasche klappt (rotate), der Bogen fährt heraus
      (yoffset). Beide Teile in einem Aufruf nutzbar.
  zeile_taucht_auf(nummer, dauer=0.18)
      Für Listen: wartet nummer * 0.05 Sekunden und blendet dann auf.
      Höchstens acht Zeilen gestaffelt, danach alle zugleich.
  knopf_hebt(dauer=0.12)
      Beim Überfahren mit der Maus: yoffset -2. Mehr nicht.

TEIL C - ÜBERGÄNGE
Lege drei benannte Übergänge an und benutze überall nur diese:
  UEBERGANG_KARTE    Dissolve, kurz, zwischen zwei Entscheidungskarten
  UEBERGANG_KAPITEL  Fade über FARBE_DUNKEL, beim Jahreswechsel
  UEBERGANG_ENDE     langsamer Fade, vor dem Lebenslauf
Alle drei ziehen ihre Dauer aus bewegungszeit().

TEIL D - EINBAU
Setze das Vokabular an diesen Stellen ein, mehr nicht:
  screens.rpy  entscheidungskarte, karten_entscheidung  -> karte_kommt
               karten_ausgang                            -> karte_kommt
               kapitelkarte                              -> kalenderblatt
               alle textbutton der Kartenflächen        -> knopf_hebt
  kapitel.rpy  jahreskarte, jahresabschluss              -> kalenderblatt
  figuren.rpy  brief_bildschirm                          -> umschlag_oeffnet
Die Bildschirme der Einlagen kommen in Schritt 2 dieses Pakets und 15 dran.

TEIL E - GRENZEN EINHALTEN
5. Kein Bildschirm bewegt mehr als drei Elemente gleichzeitig.
6. Interaktion wird nie durch eine Bewegung aufgehalten: Jede Karte ist ab
   dem ersten Bild anklickbar, auch während sie noch einläuft.
7. Prüfe blase_blinken (dialoge.rpy:955). Es pulsiert dauerhaft zwischen
   alpha 0.45 und 0.20. Als Weiter-Zeichen ist das in Ordnung, als
   Dauerbewegung nicht. Entscheide begründet: beibehalten, verlangsamen
   oder durch ein ruhendes Zeichen ersetzen.
8. Beamertauglichkeit: Miss die Bildrate während eines Kapitelwechsels und
   während einer Einlage auf dem Zielrechner. Fällt sie unter 50 Bilder
   je Sekunde, vereinfache. Nenne die gemessenen Werte.

ABNAHME DIESES SCHRITTS
  - bewegung.rpy existiert, alle neun transforms sind vorhanden und
    parametrisiert.
  - Keine Sekundenzahl steht mehr fest in einem Screen; alles läuft über
    bewegungszeit().
  - Mit persistent.bewegung = "aus" ist das Spiel vollständig spielbar
    und sieht keinen Frame lang anders aus als am Ende der Bewegung.
  - probe_alles.py unverändert: kein Wert, kein Text, kein Bestand
    bewegt sich.
  - errors.txt leer, Lint ohne neue Meldungen.

PRÜFEN MIT: probe_alles.py --vergleich, ein Durchgang von Hand in jeder
der drei Bewegungsstufen, Lint.
```

---

## Schritt 2 von 3 - HANDGRIFFE I - ROTSTIFT UND ACHT STRICHE

```text
GRUNDSATZ
Nur Ren'Py-Bordmittel, keine externen Bilddateien. Bewegungen kommen
ausschließlich aus dem Vokabular von Schritt 1 dieses Pakets.
EINLAGE_HOECHSTWIRKUNG = 3 bleibt unverändert.

TEIL A - ROTSTIFT (Briefzensur)
1. STREICHBALKEN. Ein deckender Balken in FARBE_AKZENT liegt über der
   gestrichenen Zeile, leicht gedreht. Der Winkel liegt zwischen 0,4 und
   1,2 Grad und wird EINMAL fest in einlage_lage gewürfelt, nicht im
   Screen - sonst zittert der Balken bei jedem Neuzeichnen. Der Text
   darunter bleibt sichtbar, aber unlesbar.
2. BEWEGUNG. Der Balken wächst mit strich_waechst() von links nach
   rechts auf.
3. STEMPEL. Erscheint oben rechts mit stempel_setzt(): Rahmen in
   FARBE_AKZENT, Versalien "GEPRÜFT", 6 bis 8 Grad gedreht (Winkel
   ebenfalls einmal fest gewürfelt), halbdurchsichtig. NICHT "Zensiert" -
   das Wort stand nicht auf den Stempeln der Feldpostprüfstellen.
4. ZÄHLER. "X von Y Zeilen gestrichen." Ruhig gesetzt, keine Wertung.
5. RÜCKNAHME. Ein zweiter Klick hebt den Strich wieder auf. Die
   Schaltfläche heißt "Abschicken", nicht "Fertig" oder "Weiter".
6. Die Etappenfassung der Texte (einlage_text, minispiele.rpy:542) ist seit
   Paket 5, Schritt 1 vorhanden. Prüfe, dass sie hier greift.

TEIL B - ACHT STRICHE (Verteilung von Lebensmitteln)
1. GESICHTER STATT FELDER. Jeder Empfänger zeigt je nach Zuteilung einen
   Zustandssatz: nichts / zu wenig / genug. Drei Sätze je Empfänger, aus
   der Sicht der Person, nicht aus der Sicht der Verwaltung.
2. DER EIGENE ANTEIL. "selbst" ist ein Empfänger wie die anderen, kostet
   sichtbar und zeigt eine Konsequenz. Wer sich nichts nimmt, sieht das
   ebenso.
3. KEIN UNIVERSELLES OPTIMUM. Belege rechnerisch, dass keine Verteilung in
   allen vier Werten überlegen ist. Gib die Rechnung aus: alle
   Verteilungen durchgehen und zeigen, dass jede in mindestens einem Wert
   schlechter abschneidet als eine andere. Das ist das inhaltliche Herz
   der Einlage.
4. SCHALTFLÄCHE. Erst aktiv, wenn alle acht Teile verteilt sind. Solange
   sie inaktiv ist, steht darunter, was noch fehlt - nicht "Fehler",
   sondern "Drei Striche liegen noch auf dem Tisch."
5. BEWEGUNG. Ein zugeteilter Strich wandert sichtbar zum Empfänger
   (karte_geht / karte_kommt in kurzer Form). Die Zustandssätze wechseln
   ohne Blinken.

BEIDE EINLAGEN
  - einordnung bleibt bei genau zwei Sätzen.
  - Kein Ton, der die Verteilung bewertet.
  - Der Ausgangsbildschirm nennt keine Punktzahl.

ABNAHME DIESES SCHRITTS
  - Die Rechnung zu Punkt B3 liegt vor und zeigt kein Optimum.
  - Der Drehwinkel von Balken und Stempel bleibt über mehrere
    Neuzeichnungen konstant; weise es nach.
  - probe_alles.py: Einlagenbestand und Wertetafel unverändert oder
    innerhalb der Grenzen aus Paket 2, Schritt 3.
  - Sprachprobe und Zwei-Sätze-Regel ohne Beanstandung.

PRÜFEN MIT: pruefen.py und probe_alles.py; beide Einlagen je dreimal von
Hand.
```

---

## Schritt 3 von 3 - HANDGRIFFE II - TORNISTER UND FAHRT AUFS LAND

```text
TEIL A - TORNISTER (was man auf dem Marsch zurücklässt)
1. MERKMALE. Zurückgelassene Stücke setzen Merkmale: ohne_mantel,
   ohne_zeltbahn, ohne_stiefel, ohne_kochgeschirr, ohne_portion,
   ohne_briefe, ohne_putzzeug. Alle sieben werden in MERKMAL_REGISTER
   eingetragen (gruppe "lage"), mit Rang und Nachklang.
2. NACHWIRKUNG. ohne_mantel erhöht über gewicht_bonus in
   RUECKBEZUG_NACHTRAG die Ziehchance für front_1914_schanzen und die
   Winterereignisse. Zwei bis drei Frontereignisse greifen das Fehlen über
   variante() auf, in einem Satz und ohne Vorwurf:
   "Der Mann neben dir schlägt den Mantelkragen hoch. Du hast keinen."
   WEISE NACH, dass dadurch kein Ende unausweichlich wird: Simuliere
   Durchgänge mit allen sieben Merkmalen gesetzt und zeige, dass die
   Abbruchquote innerhalb der Grenzen aus Paket 2, Schritt 3 bleibt.
3. ABLAGE. Beim Abwerfen wandert das Stück sichtbar (karte_geht) in eine
   Fläche "Im Straßengraben" am unteren Rand. Von dort kann es vor dem
   Weitermarsch zurückgeholt werden. Die Entscheidung fällt erst mit dem
   Weitermarsch.
4. Die Traglast bleibt sichtbar: TRAGLAST_GRENZE und tornister_grundlast()
   sind vorhanden, der Balken zeigt Ist und Grenze.

TEIL B - FAHRT AUFS LAND (Hamsterfahrt)
1. ANTWORT DES HOFES. Der Hof antwortet mit einem erzählerischen Satz,
   gestaffelt nach der Höhe des Gebots. Bei Überzahlung nimmt er alles -
   und sagt dazu einen Satz, der zeigt, dass er weiß, was er tut.
2. FOLGE SOFORT SICHTBAR. Der folge-Satz erscheint schon beim Anbieten,
   nicht erst nach der Annahme.
3. WEGANZEIGE. Drei Höfe auf einer schlichten Linie am oberen Rand, dazu
   die Uhrzeit bis zum letzten Zug. Die Uhrzeit läuft nicht in Echtzeit,
   sie springt mit jedem Hof.
4. RUCKSACK. Ab HAMSTER_AUFFAELLIG (12 Pfund) bekommt der Balken einen
   Rahmen in FARBE_AKZENT und darunter steht: "Der Rucksack steht ab."
   Kein Warnton, kein Ausrufezeichen.
5. BEWEGUNG. Der Wechsel von Hof zu Hof nutzt UEBERGANG_KARTE, der
   Rucksackbalken wächst mit strich_waechst().

BEIDE EINLAGEN
  - quelle-Dict im Format aus Paket 3, Schritt 1 prüfen und ergänzen.
  - Etappenfassungen aus Paket 5, Schritt 1 prüfen.
  - Keine Wertung im Ausgangstext.

ABNAHME DIESES SCHRITTS
  - Die sieben ohne_-Merkmale stehen im Register und erscheinen im
    Lebenslauf.
  - Der Nachweis aus A2 liegt vor: kein Ende wird unausweichlich.
  - probe_alles.py innerhalb der Grenzen aus Paket 2, Schritt 3.
  - Beide Einlagen ohne neue Beanstandung in der Sprachprobe.

PRÜFEN MIT: pruefen.py und probe_alles.py; beide Einlagen je dreimal von
Hand, einmal mit vollem und einmal mit leerem Tornister.
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

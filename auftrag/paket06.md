<!-- Erzeugt aus bau/. Nicht von Hand ändern - die Änderung
     wäre beim nächsten Bauen weg. Melde stattdessen unter AUFGEFALLEN. -->

# Paket 6 - TEXTÜBERARBEITUNG FRONT UND HEIMAT

> **Vor diesem Paket gelesen:** `STAND.md`, `git log --oneline -10`,
> `auftrag/VERFASSUNG.md`, `auftrag/ENTSCHEIDUNGEN.md`.
> **Nach jedem Schritt:** Commit, `probe_alles.py --schnell`, Kurzmeldung,
> `STAND.md` und `auftrag/OFFENE_PUNKTE.md` nachziehen.

## Überblick

```text
Reine Textarbeit an dem, was schon da ist: 18 Frontereignisse, 20
Heimatereignisse, vier Einstiegsereignisse. Kein Wert, keine Bedingung,
keine Kennung wird angefasst.
Das ist der Schritt, der aus einer Sammlung von Karten ein Spiel macht,
das eine Achtklässlerin ernst nimmt. Er kommt bewusst spät: Es hat
keinen Sinn, 38 Ereignisse zu polieren und danach 40 neue zu schreiben.
Der Erfolg ist hart messbar - alle Zahlen müssen exakt gleich bleiben,
nur Probe 8 darf besser werden.
```

## Vorweg

```text
VORWEG - NACHTRAG ZUR EICHUNG (vor Schritt 1 erledigen, eigene Commits)

Paket 5, Schritt 3 hat alles erreicht außer seinem Hauptkriterium - und
hat bewiesen, dass es mit den erlaubten Größen nicht zu erreichen war.
Die Obergrenzenmessung: leerer Kalender, keine Einlagen, keine Post,
beste Startwerte (Versorgung 12, Belastung 0, Verdacht 0, Rückhalt 12).
Der lange Etappenverlauf kommt so auf 2,0 Prozent zufällig und 8,7
Prozent klug. Eine gezogene Karte kostet unter kluger Wahl 0,57 bis 0,93
Punkte, ein langer Durchgang hat 31 davon: 18 bis 29 Punkte gegen eine
Skala, die 12 hergibt. Nicht die Eichung war schlecht - die Rechnung ging
nicht auf.

Darauf sind zwei Entscheidungen gefallen, 11 und 12 in
auftrag/ENTSCHEIDUNGEN.md. Dieser Vorweg setzt sie um. Er steht hier und
nicht später, weil ab Schritt 1 keine Zahl mehr angefasst wird - die
Zahlen müssen vorher stimmen.

A) ZWEI GRENZEN STATT EINER
   Entscheidung 1 galt für beide Verläufe gleich. Ab jetzt nicht mehr:
     kurzer Verlauf   40 bis 60 Prozent zufällig, mindestens 80 klug
     langer Verlauf   20 bis 35 Prozent zufällig, mindestens 60 klug
   Der kurze Verlauf ist die Unterrichtsstunde, der lange ist der
   längere Krieg. Dass die Mehrheit ihn nicht übersteht, ist historisch
   wahr. Dass niemand ihn übersteht, ist ein Fehler.
   1. Trage beide Grenzen als benannte Größen ein, nicht als Zahlen im
      Prüfcode: ZIEL_KURZ und ZIEL_LANG, mit Kommentar und Datum.
   2. Probe 4 prüft ab jetzt je Verlauf gegen seine eigene Grenze und
      schreibt beide Grenzen in den Bericht, damit man sieht, wogegen
      gemessen wurde.
   3. WAS NICHT VERHANDELBAR IST: In JEDER der sechs Lagen erreicht ein
      messbarer Anteil das Jahr 1919. 0,0 Prozent ist kein Ergebnis,
      sondern ein toter Pfad. Wo eine Lage auf null steht, hältst du an
      und meldest es, statt die Grenze weiter zu senken.

B) WENIGER ZIEHUNGEN - DER EIGENTLICHE HEBEL
   Nicht die Karten sind zu teuer, der Durchgang ist zu lang. Bei acht
   Ziehungen misst der kurze Verlauf bereits 42 bis 51 Prozent.
   Das hilft zweimal: Dreizehn Entscheidungen in 45 Minuten sind für
   Dreizehnjährige ohnehin knapp gerechnet - mit Lesen, Nachdenken und
   Zwischenfragen sind neun realistisch.
   1. Setze MODUS_ZIELZAHL und KAPITEL_ZIEHUNGEN so, dass der kurze
      Verlauf bei rund NEUN Ziehungen liegt und der lange bei ACHTZEHN
      BIS ZWANZIG. Nimm die Ziehungen dort weg, wo ein Jahr heute mehr
      als seinen Anteil hat, nicht gleichmässig überall.
   2. Miss nach jeder Änderung, gib die Tafel aus, geh erst dann weiter.
      Eine Stellschraube je Messung.
   3. DER BESTAND BLEIBT VOLLSTÄNDIG. Es wird nichts gelöscht und
      nichts stillgelegt - es wird nur weniger je Durchgang gezogen. Die
      Bestandstafel muss danach unverändert auf null stehen, und die
      Sackgassenprobe ebenfalls. Weniger Ziehungen können keine
      Sackgasse erzeugen; melde es, wenn doch.
   4. Rechne mir vor, was ein kurzer Durchgang danach enthält:
      Ereignisse, Einlagen, Briefe, zusammen. Nenne die Zahl.

C) WENN DIE ETAPPE ZURÜCKBLEIBT
   Nach Schritt 3 liegt der kurze Etappenverlauf bei 14,2 Prozent gegen
   29,6 und 26,9 auf den anderen Pfaden. Der Abstand zwischen zufälliger
   und kluger Wahl stimmt dort inzwischen (+19,2), die Höhe nicht.
   AUFGEFALLEN 42 nennt den Grund: Der Etappe fehlen Karten gegen die
   Erschöpfung - 13 Prozent ihrer Optionen senken belastung, gegen 24
   an der Front und 21 in der Heimat.
   1. Miss zuerst. Reicht B, um die Etappe in ihre Grenze zu heben, ist
      hier nichts zu tun - sag es mit der Zahl und geh weiter.
   2. Reicht es nicht, schreibst du DREI neue Etappenereignisse, deren
      eine Option belastung wirklich senkt. Sachlich tragfähig, nicht
      bequem: eine Woche Innendienst nach einem Transport, ein Quartier
      mit Ofen, eine Ablösung, die tatsächlich kommt. Kein Freikaufen,
      keine Belohnung für gutes Benehmen.
   3. Diese drei Ereignisse sind die einzige Inhaltsarbeit, die dieser
      Vorweg erlaubt. Sie gehen durch alles, was für neue Ereignisse
      gilt: quelle-Dict, Handwerksregeln a bis h, Einbahnstraßen- und
      Dominanzprüfung.

D) VIER ZU LANGE EINORDNUNGEN IN DEN EREIGNISSEN
   AUFGEFALLEN 41: Probe 8 hat bisher nur die Einordnungen der EINLAGEN
   gemessen, nicht die der Ereignisse. Vier davon sind zu lang.
   Sie fallen unter dieselbe Regel wie die anderen - Entscheidung 9,
   genau zwei Sätze, jeder unter 20 Wörtern, zusammen höchstens 35 -
   und werden in Schritt 2 zusammen mit den zwölf Einlagen-Einordnungen
   gekürzt. Hier nur: nenne die vier Kennungen, damit Schritt 2 sie
   nicht sucht.

E) ZWEI BESTÄNDE IN EINER PRÜFUNG
   AUFGEFALLEN 43: Die Einbahnstraßenprüfung und die Dominanzprüfung
   zählen verschiedene Bestände - eine nimmt nur_kette-Ereignisse mit,
   die andere nicht. Damit meldet die eine Fälle, die die andere nie
   sieht, und die Fallzahlen im Selbsttest gehen auseinander.
   Entscheide, welcher Bestand richtig ist (Vorschlag: beide prüfen
   alles, was gezogen werden kann, nur_kette eingeschlossen), stelle
   beide darauf um und weise nach, dass die Fallzahlen danach gleich
   sind.

ABNAHME DES VORWEG-TEILS
  - ZIEL_KURZ und ZIEL_LANG stehen als benannte Größen mit Datum;
    Probe 4 misst je Verlauf dagegen und schreibt beide in den Bericht.
  - Alle sechs Lagen liegen in ihrer Grenze. KEINE Lage steht auf 0,0.
  - Der kurze Verlauf hat rund neun Ziehungen, der lange achtzehn bis
    zwanzig; die Zahl der Inhalte je kurzem Durchgang ist genannt.
  - Bestandstafel und Sackgassenprobe stehen weiter auf null.
  - Die Etappe liegt in ihrer Grenze - mit oder ohne die drei neuen
    Karten; welches von beidem, steht mit der Zahl dabei.
  - Die vier zu langen Ereignis-Einordnungen sind namentlich genannt.
  - Einbahnstraßen- und Dominanzprüfung zählen denselben Bestand;
    die Fallzahlen im Selbsttest stimmen überein.
```

## Die Schritte

1. TEXT-REFACTORING FRONT
2. TEXT-REFACTORING HEIMAT UND EINSTIEG

Jeder Schritt hat seine eigene Abnahme. Die Gesamtabnahme steht unten.

---

## Schritt 1 von 2 - TEXT-REFACTORING FRONT

```text
AUFGABE
Überarbeite ausschließlich die Ereignisse in script.rpy, deren Kennung
mit "front_" beginnt. Nach dem heutigen Stand sind das 18; prüfe die Zahl
selbst und nenne sie. Die Ereignisse aus den Paketen 7 bis 9 sind bereits
nach diesen Regeln geschrieben und werden nur gegengelesen.

PRINZIP
Ein Moment, keine Zusammenfassung. Zeigen statt berichten.

HANDWERKSREGELN
Es gelten die Regeln a bis f aus der Verfassung, dazu:
  - Der erste Satz verortet den Körper: wo er ist, was er trägt, wie
    kalt oder warm es ist.
  - Der letzte Satz schärft die Lage, statt sie zu bewerten.
  - jahrestext: 1914, 1915 und 1916 unterscheiden sich substanziell.
    1914 ist Bewegung und Neugier, 1915 Einrichtung im Graben, 1916
    Material und Erschöpfung. Ein ausgetauschtes Wort genügt nicht.
  - Fremdwörter und militärische Fachbegriffe: beim ersten Vorkommen im
    selben Satz erklärt. "Der Zugführer, also der Mann, der die dreißig
    Leute befehligt, ..." und nicht eine Fußnote.

SPRACHMASS
Probe 8 aus Paket 3, Schritt 2 gilt. Nimm die dortige Liste der Sätze über 20
Wörter und arbeite die front_-Einträge daraus ab. Nach diesem Paket
darf kein front_-Text mehr darin stehen.

UNVERÄNDERT BLEIBEN
Kennungen, aenderungen, bedingungen (braucht, braucht_eines, verbietet),
gewichte, ketten, quelle, jahre, pfad, kern-Kennzeichnung, Reihenfolge der
Optionen.

AUSGABE
Gib die vollständigen Codeblöcke aus. Führe probe_alles.py aus und zeige
mit dem Vergleichsschalter, dass Bestandstafel, Wertetafel und
Sackgassenprobe exakt gleich geblieben sind - ein reines Textpaket darf
keine Zahl bewegen.

ABNAHME DIESES SCHRITTS
  - Bestandstafel, Probe 3 und Probe 4 identisch zum Bericht davor.
  - Probe 8: kein front_-Satz über 20 Wörter, Durchschnitt unter 13.
  - Sprachprobe ohne Beanstandung.
  - Probe 5 unverändert: keine Quelle verloren gegangen.

PRÜFEN MIT: probe_alles.py --vergleich, Probe 8.
```

---

## Schritt 2 von 2 - TEXT-REFACTORING HEIMAT UND EINSTIEG

```text
AUFGABE
Überarbeite die Ereignisse in script.rpy, deren Kennung mit "heimat_"
beginnt - nach dem heutigen Stand 20 - sowie die vier Einstiegsereignisse
einstieg_meldung, einstieg_offizier, einstieg_etappe, einstieg_abschied.
ACHTUNG, ANDERE DATEI: Die vier Einstiegsereignisse stehen NICHT in
script.rpy, sondern in herkunft.rpy, Abschnitt 6, im Bestand
EREIGNISSE_PAKET2 (herkunft.rpy:1220). Wer nur script.rpy durchsucht, findet 38 statt 42
Ereignisse. Das ist beim Nachrüsten der Belege schon einmal aufgefallen.
Es gelten dieselben Handwerksregeln wie in Schritt 1 dieses Pakets.

ZUSÄTZLICH - DIE FAMILIENMERKMALE NUTZEN
Setze ehemann_im_feld, vater_im_feld und bruder_im_feld (aus Paket 2, Schritt 2) über
variante() ein, mindestens in:
  heimat_todesnachricht      wer trauert, welche behördliche Formel
  heimat_1914_post           wer schreibt
  heimat_unterstuetzung      Begründung am Schalter
  heimat_1916_ernaehrungsamt wer als Haushaltsvorstand gilt
Die Formel der Behörde ist zeitgenössisch und wird im selben Satz
übersetzt.

ZWEI BAHNSTEIGE IM EINSTIEG
Beim Umbau in Paket 2, Schritt 3 ist aufgefallen: Die neue Szene einstieg_bahnsteig
und die Karte einstieg_abschied spielen beide auf einem Bahnsteig,
getrennt nur durch die Erwerbswahl. Zweimal derselbe Ort in den ersten
fünf Minuten lässt den Anfang eng wirken.
Entscheide begründet und setze es um: Entweder bekommt eines der beiden
einen anderen Ort (die Wohnung, der Hof, das Werkstor, die Amtsstube),
oder die beiden werden so verschieden geschrieben, dass der Bahnsteig
zweimal etwas anderes bedeutet - einmal Aufbruch, einmal Zurückbleiben.
Kennungen bleiben unverändert.

VORSICHT BEI heimat_todesnachricht
Kein Verschulden der Spielerin andeuten. Der Tod kommt ausschließlich aus
dem Schicksalssystem beim Jahreswechsel, nicht aus einer Entscheidung.
Der Text darf nicht nahelegen, man hätte etwas tun können.

DIE HEIMAT IST KEIN NEBENSCHAUPLATZ
Die Heimatereignisse sollen in Genauigkeit und körperlicher Nähe den
Frontereignissen gleichkommen: Kälte in der Wohnung, das Gewicht des
Kohleeimers, der Geruch von Rüben, das Stehen in der Reihe, die Stimme am
Schalter. Wo ein Text heute zusammenfasst, wird er zu einem Moment.

SPRACHMASS
Wie Schritt 1 dieses Pakets: Nach diesem Paket steht kein heimat_- oder einstieg_-Satz
mehr in der Liste der Sätze über 20 Wörter.

AUCH ZU KÜRZEN: DIE EINORDNUNGEN DER EINLAGEN
Probe 8 hat 18 zu lange Sätze gefunden, zwölf davon stehen in den
historischen Einordnungen der Einlagen. Die sind bewusst dicht - sie
tragen den Fachertrag. Trotzdem stehen sie im Spiel auf dem Bildschirm
und werden von Dreizehnjährigen gelesen.
So wird es gelöst, und nur so:
1. Die Einordnung im Spiel wird auf zwei lesbare Sätze gebracht, jeder
   unter 20 Wörtern. Die Zwei-Sätze-Regel bleibt.
2. Was dabei wegfällt, wird NICHT gelöscht. Lege es als Feld
   "vertiefung" neben der Einordnung ab, mit derselben Kennung.
   Paket 8, Schritt 3 nimmt diese Texte in das Glossar und in die Quellenkarte auf,
   wo ohnehin ein langer Text für die Detailansicht steht.
3. Nichts geht verloren, es steht nur einen Klick weiter. Weise für jede
   der sechs Einordnungen nach, wohin welcher Satz gewandert ist.
4. Probe 8 weist Einordnungen ab jetzt als eigene Textart aus, damit man
   sieht, ob die Kürzung gehalten hat.

UNVERÄNDERT BLEIBEN
Kennungen, Werte, Bedingungen, Quellen, Reihenfolge der Optionen.

ABNAHME DIESES SCHRITTS
  - Bestandstafel, Probe 3 und Probe 4 identisch zum Bericht davor.
  - Probe 8: kein heimat_- oder einstieg_-Satz über 20 Wörter.
  - Die vier genannten Ereignisse zeigen für alle drei Familienmerkmale
    eine eigene Fassung; spiele je einen Durchgang und belege es.
  - Sprachprobe ohne Beanstandung.

PRÜFEN MIT: probe_alles.py --vergleich, Probe 8, drei Durchgänge von
Hand.
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

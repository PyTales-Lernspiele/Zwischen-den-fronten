<!-- Erzeugt aus bau/. Nicht von Hand ändern - die Änderung
     wäre beim nächsten Bauen weg. Melde stattdessen unter AUFGEFALLEN. -->

# Paket 9 - DIE SCHULSTUNDE

> **Vor diesem Paket gelesen:** `STAND.md`, `git log --oneline -10`,
> `auftrag/VERFASSUNG.md`, `auftrag/ENTSCHEIDUNGEN.md`.
> **Nach jedem Schritt:** Commit, `probe_alles.py --schnell`, Kurzmeldung,
> `STAND.md` und `auftrag/OFFENE_PUNKTE.md` nachziehen.

## Überblick

```text
Bis hierher ist das Spiel richtig geworden - jetzt wird es
unterrichtstauglich. Die beiden Schritte beantworten dieselbe Frage aus
zwei Richtungen: Was passiert in 45 Minuten mit 28 Dreizehnjährigen?
Schritt 1 räumt die Hürden weg, die Zeit kosten oder jemanden
zurücklassen: der lange Weg bis zur ersten Karte, die fehlende
Orientierung im Kriegsjahr, der Durchgang, der in Minute acht endet.
Schritt 2 baut das, wovon der Unterricht am Ende lebt: den Vergleich
zweier Lebensläufe, die Einordnung des eigenen Falls, und eine Datei, mit
der du die Stunde vorgibst - samt gemeinsamer Zufallssaat, damit alle
dieselben Karten ziehen und sich wirklich die Entscheidungen
unterscheiden.
Dazu kommt der Heeresbericht: was die Öffentlichkeit las, neben dem, was
die Figur erlebt hat. Das ist Quellenkritik, die sich von selbst ergibt.
```

## Die Schritte

1. SCHNELLSTART, ZEITLEISTE, HEERESBERICHT UND AUFFANGNETZ
2. VERGLEICHEN, EINORDNEN, STEUERN

Jeder Schritt hat seine eigene Abnahme. Die Gesamtabnahme steht unten.

---

## Schritt 1 von 2 - SCHNELLSTART, ZEITLEISTE, HEERESBERICHT UND AUFFANGNETZ

```text
WARUM DIESER SCHRITT
Bis hierher ist das Spiel richtig geworden. Jetzt wird es
unterrichtstauglich. Die vier Arbeiten hier haben alle dieselbe Frage im
Rücken: Was passiert in einer Schulstunde mit 28 Dreizehnjährigen und
45 Minuten?

TEIL A - SCHNELLSTART
Die Lebenslage wird heute in fünf Schritten zusammengestellt: Herkunft,
Geschlecht, Alter, Erwerb, Musterung. Das ist gut für die, die es wollen,
kostet aber drei bis vier Minuten von 45 - bevor die erste Karte liegt.
1. Ein Startbildschirm mit vier Feldern: drei fertige Lebenslagen und
   "Selbst zusammenstellen".
2. Die drei fertigen decken die drei Pfade ab und sind bewusst verschieden.
   Jede bekommt einen Vornamen, ein Alter, einen Ort und EINEN Satz - nicht
   mehr:
     18 Jahre, Arbeiterschaft, kriegsfreiwillig      -> front
     35 Jahre, Frau, Kinder, Mann im Feld, Rüstung  -> heimat
     35 Jahre, Mann, g.v. gemustert, Lazarettdienst  -> etappe
   Die Vornamen darfst du erfinden; es sind keine wirklichen Personen.
   Die Lebenslagen selbst werden aus den vorhandenen Bausteinen
   zusammengesetzt - keine Sonderfälle, keine neuen Erwerbslagen.
3. "Selbst zusammenstellen" führt in den bisherigen Ablauf, unverändert.
   Er wird nicht gekürzt und nicht versteckt.
4. Der Schnellstart ist nicht die einfachere Fassung: er trifft dieselben
   Entscheidungen, nur schneller. Sag das in einem Satz auf dem Bildschirm.
5. Miss, wie lange der Weg bis zur ersten Karte jetzt dauert, mit und ohne
   Schnellstart. Nenne beide Zeiten.

TEIL B - ZEITLEISTE UND ORT
Für eine achte Klasse ist die zeitliche Orientierung im Krieg selbst ein
Lernziel. Heute steht das Jahr auf der Kapitelkarte und danach nirgends
mehr. Wer im dritten Kapitel sitzt, weiß oft nicht mehr, welches Jahr
gerade läuft.
6. Eine schlichte Leiste, die während des ganzen Spiels sichtbar bleibt:
   die sechs Jahre 1914 bis 1919 als Band, das laufende Jahr markiert.
   Nur Ren'Py-Bordmittel. Keine Landkarte, kein Bild, keine Flaggen.
7. Daneben der Ort in zwei Wörtern, aus Ereignis.ort und PFAD_ORT:
   "Front - Flandern", "Heimat - Chemnitz". Wo kein Ort gesetzt ist, steht
   nur der Pfad.
8. Beim Jahreswechsel wandert die Markierung sichtbar - nimm kalenderblatt
   aus Paket 7, Schritt 1.
9. Die Leiste ist dünn und ruhig. Sie konkurriert nicht mit der
   Kopfleiste der Werte und nimmt ihr keinen Platz weg.

TEIL C - DER HEERESBERICHT
Das ist der stärkste didaktische Griff, den dieses Spiel noch tun kann,
und er kostet fast nichts. Was die Öffentlichkeit las, und was die Figur
erlebte, waren zwei verschiedene Dinge. Wenn beides nebeneinander steht,
entsteht Quellenkritik von selbst - ohne dass jemand das Wort sagen muss.
10. Neue Tabelle KAPITEL_MELDUNG: je Jahr eine kurze amtliche Meldung im
    Ton der Zeit. Ein bis zwei Sätze, im Wortlaut zurückhaltend, nie
    erfunden zugespitzt. Wo du keinen Beleg hast, schreibst du "BELEG
    FEHLT" ins quelle-Dict, wie überall.
11. Sie erscheint auf der Jahreskarte, gesetzt im Kartentyp "zeitung" aus
    Paket 8, Schritt 1 - anderer Satzspiegel, andere Schrift, sichtbar
    ein anderes Papier als die Erlebniskarten.
12. KEIN KOMMENTAR. Kein Erzähler, der die Meldung richtigstellt, kein
    Hinweis, dass sie beschönigt. Der Widerspruch entsteht im Kopf der
    Spielerin, weil sie das Jahr gerade selbst gespielt hat. Genau wie in
    der Wirtshausszene.
13. Im Lebenslauf stehen am Ende alle sechs Meldungen noch einmal
    untereinander, neben den eigenen Entscheidungen desselben Jahres. Das
    ist die Seite, die im Unterricht auf den Beamer kommt.

TEIL D - DAS AUFFANGNETZ
Der Fall, der im Klassenzimmer wehtut: In Minute acht endet ein Durchgang,
und die Schülerin sitzt siebzehn Minuten daneben. Speichern gibt es nicht
und soll es nicht geben - also muss der Abbruch selbst weiterführen.
14. Ein harter Abbruch führt NICHT ins Hauptmenü, sondern in den
    Lebenslauf. Verkürzt, aber vollständig genug: was gewesen ist,
    welche Merkmale gesammelt wurden, welche Nachklänge dazugehören.
    Wer 1916 verhaftet wird, erfährt trotzdem, wie es weiterging.
15. Danach ein Angebot, kein Bildschirm mit "Verloren": "Noch einmal, mit
    einer anderen Lebenslage." Ein Klick, und der Schnellstart steht
    wieder da - mit dem Vermerk, welche Lage gerade gespielt wurde, damit
    nicht dieselbe noch einmal vorgeschlagen wird.
16. Kein Wort, das die Schuld bei der Spielerin sucht. Ein Abbruch ist
    eine Biografie, kein Fehler. Geh alle vier Endtexte daraufhin durch
    und nenne mir jede Stelle, die du geändert hast.
17. Miss in probe_alles.py, nach wie vielen Ereignissen ein Abbruch im
    Mittel eintritt, je Lage. Liegt der Mittelwert unter der Hälfte der
    vorgesehenen Ziehungen, sag es deutlich - dann reicht das Auffangnetz
    nicht und der Wertehaushalt muss noch einmal ran.

ABNAHME DIESES SCHRITTS
  - Der Weg bis zur ersten Karte dauert mit Schnellstart höchstens ein
    Drittel der bisherigen Zeit; beide Zeiten sind genannt.
  - Zeitleiste und Ort sind in jedem Kapitel sichtbar, auf allen drei
    Pfaden.
  - KAPITEL_MELDUNG ist für alle sechs Jahre gefüllt, jede mit
    quelle-Dict, keine mit Kommentar.
  - Ein erzwungener Abbruch führt in den Lebenslauf und von dort in einen
    neuen Durchgang; spiele das dreimal durch, je einmal für verhungert,
    zusammenbruch und verhaftet.
  - probe_alles.py: keine neue Beanstandung, Wertetafel unverändert.

PRÜFEN MIT: probe_alles.py, drei erzwungene Abbrüche von Hand, eine
Zeitmessung bis zur ersten Karte.
```

---

## Schritt 2 von 2 - VERGLEICHEN, EINORDNEN, STEUERN

```text
WARUM DIESER SCHRITT
Ein Durchgang allein lehrt wenig. Der Ertrag entsteht, wenn zwei
Lebensläufe nebeneinanderliegen und jemand fragt, warum sie sich
unterscheiden. Dafür gibt es bisher nichts im Spiel.

TEIL A - DREI LEBEN NEBENEINANDER
1. persistent speichert die letzten drei Durchgänge, aber nur wenige
   Angaben: Lebenslage in einem Satz, Pfad, Verlauf, Endwerte, Ausgang,
   die zwei Merkmale mit dem höchsten Rang, das Datum.
   KEIN Spielstand, keine Möglichkeit fortzusetzen, kein Zurück. Regel 5
   bleibt unangetastet - gespeichert wird, was gewesen ist, nicht, wo man
   steht.
2. Der Lebenslauf-Bildschirm bekommt eine zweite Spalte: "Beim letzten
   Mal". Wer zum ersten Mal spielt, sieht sie nicht.
3. Im Hauptmenü ein Bildschirm "Drei Leben", der die drei nebeneinander
   stellt. Das ist die Ansicht, an der im Unterricht verglichen wird, und
   sie muss ohne Erklärung lesbar sein.
4. Keine Wertung, keine Punkte, kein "besser", keine Reihenfolge nach
   Erfolg. Nur nebeneinander, in der Reihenfolge des Spielens.
5. Eine Schaltfläche "Alles löschen" für den Schulrechner, an dem die
   nächste Klasse sitzt.

TEIL B - WAS DU NICHT GESEHEN HAST
6. Am Ende des Lebenslaufs eine ruhige Zeile: wie viele Ereignisse es im
   Spiel gibt und wie viele dieser Durchgang gezeigt hat. Darunter die
   TITEL - nicht die Inhalte - von fünf Karten, die diesmal nicht kamen.
7. Das ist keine Sammelaufgabe und kein Fortschrittsbalken. Es sagt einer
   Schülerin, dass ihre Geschichte eine von vielen möglichen war, und
   das ist genau der Gedanke, um den es geht.
8. Keine Prozentanzeige, kein "du hast erst 13 Prozent gesehen".

TEIL C - WAR DAS TYPISCH?
Historisches Denken auf Klasse-8-Niveau heißt auch: einordnen können, ob
das eigene Beispiel häufig oder selten war. Die Zahlen dafür liegen
längst vor - probe_alles.py rechnet sie ohnehin.
9. Erweitere probe_alles.py um einen Schalter, der die Häufigkeiten in
   eine Datei "häufigkeiten.py" neben den .rpy-Dateien schreibt: je
   Ausgang und je Merkmal der Anteil über alle simulierten Durchgänge,
   gerundet auf ganze Prozent.
10. Das Spiel liest die Datei beim Start, wenn sie da ist - mit
    renpy.loadable(), nach dem Muster aus Regel 7. Fehlt sie, erscheint
    die Angabe einfach nicht, und nichts stürzt ab.
11. Im Lebenslauf steht neben jedem Nachklang eine schlichte Angabe. Fünf
    Stufen genügen: fast allen / vielen / etwa jedem Dritten / wenigen /
    kaum jemandem. Keine Kommazahlen, keine Prozente auf dem Bildschirm.
12. WICHTIG UND EHRLICH: Das sind Häufigkeiten IM SPIEL, nicht in der
    Geschichte. Ein Satz auf demselben Bildschirm sagt das, und zwar in
    der Sprache der Zielgruppe. Ein Spiel, das seine eigene Statistik für
    historische Wirklichkeit ausgibt, wäre schlechter als eines ganz ohne
    Zahlen. Die längere Erklärung steht im Lehrkraftmaterial.

TEIL D - DIE HAND DER LEHRKRAFT
13. Eine Datei "unterricht.txt" im Spielordner, die beim Start gelesen
    wird, wenn sie da ist. Fünf Zeilen genügen:
      verlauf     kurz oder lang
      schnellstart ja oder nein
      bewegung    voll, sparsam oder aus
      schrift     normal, groß oder sehr groß
      saat        eine Zahl oder leer
14. DIE SAAT IST DER WICHTIGSTE EINTRAG. Steht dort eine Zahl, ziehen alle
    Rechner im Raum dieselbe Kartenfolge. Dann unterscheiden sich die
    Lebensläufe am Ende nur noch durch die Entscheidungen - und der
    Vergleich im Plenum wird sauber, statt Glück gegen Glück zu stellen.
    Bleibt die Zeile leer, würfelt jeder Rechner für sich, wie bisher.
15. Format: schlicht, kommentiert, von Hand zu bearbeiten. Kein Menü,
    keine Oberfläche, kein Passwort. Wer die Datei findet, darf sie
    ändern; sie ist eine Vorgabe, kein Schutz.
16. Fehlt die Datei, gilt alles wie bisher. Eine unverständliche Zeile
    wird übergangen und im Analysemodus gemeldet, nie im Spiel.
17. Lege eine Beispieldatei mit allen fünf Zeilen und Erklärungen bei.

ABNAHME DIESES SCHRITTS
  - Nach drei Durchgängen zeigt "Drei Leben" drei Spalten; "Alles
    löschen" leert sie.
  - Der Lebenslauf nennt die Zahl der ungesehenen Ereignisse und fünf
    Titel davon.
  - Mit häufigkeiten.py stehen die Einordnungen da, ohne sie nicht - und
    das Spiel läuft in beiden Fällen.
  - Zwei Durchgänge mit derselben Saat ziehen dieselben Karten in
    derselben Reihenfolge; weise es nach.
  - Eine kaputte Zeile in unterricht.txt bricht nichts.

PRÜFEN MIT: probe_alles.py, drei Durchgänge von Hand, zwei Durchgänge
mit gleicher Saat, eine absichtlich fehlerhafte unterricht.txt.
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

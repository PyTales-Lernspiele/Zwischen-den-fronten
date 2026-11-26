# KONTRAST AM BEAMER

Jede Kombination aus Textfarbe und Untergrund, die im Spiel
vorkommt, nach WCAG 2.1 nachgerechnet.

**Erzeugt von `kontrast.py`. Es ändert keine Farbe** — die
Farbwelt ist das Gesicht des Spiels, und darüber entscheidet
Dominik.

## Der Maßstab

Verlangt sind **7:1**, nicht die üblichen 4,5:1. Der Grund ist
das Klassenzimmer: Bei Tageslicht verliert ein Beamer einen
guten Teil seines Kontrasts, bevor das Bild an der Wand
ankommt. Große Schrift — ab 24 px fett oder 30 px normal —
darf nach demselben Maßstab auf **4.5:1**; das steht in einer
eigenen Spalte, weil viele Überschriften darunter fallen.

## Die Untergründe

| Farbe | Wert | Wo | Beleg |
|---|---|---|---|
| `FARBE_PAPIER` | `#efe9dc` | Bildschirmgrund | add Solid(FARBE_PAPIER) - 31 Fundstellen, u.a. karten_entscheidung |
| `FARBE_PAPIER_HELL` | `#f7f3ea` | Karten und Rahmen | kartenpapier() in gui.rpy, rahmen_doppelt(...) in screens.rpy |
| `FARBE_PAPIER_DUNKEL` | `#e2dbca` | Zeitungskarte, Motivflaeche, Platzhalter | kartenpapier("zeitung"), bild_platzhalter() in gui.rpy |
| `FARBE_DUNKEL_HELL` | `#241f19` | dunkle Flaechen im Endbildschirm | background rahmen(FARBE_DUNKEL_HELL, FARBE_LINIE, 2) - 6 Fundstellen |
| `FARBE_DUNKEL` | `#15130f` | der Endbildschirm und die Uebergaenge | UEBERGANG_KAPITEL() und UEBERGANG_ENDE() in bewegung.rpy |
| `FARBE_TINTE` | `#1f1c18` | die Balkenueberschrift der Zeitungskarte | kartenblatt_zeitung in screens.rpy, seit Paket 8 Schritt 1 |
| `FARBE_AKZENT` | `#8a3324` | Schaltflaechen unter der Maus | hover_background rahmen(FARBE_AKZENT, FARBE_AKZENT, 2) - 5 Fundstellen |

## Die Paare

| Textfarbe | auf Untergrund | Verhältnis | ≥ 7:1 | groß: ≥ 4.5:1 |
|---|---|---|---|---|
| `FARBE_TINTE` <br><small>Fliesstext, Kartentitel, Ereignistext</small> | `FARBE_PAPIER` | **14.03:1** | ja | ja |
| `FARBE_TINTE` <br><small>Fliesstext, Kartentitel, Ereignistext</small> | `FARBE_PAPIER_HELL` | **15.32:1** | ja | ja |
| `FARBE_TINTE` <br><small>Fliesstext, Kartentitel, Ereignistext</small> | `FARBE_PAPIER_DUNKEL` | **12.30:1** | ja | ja |
| `FARBE_TINTE_MATT` <br><small>Kartentext, Nebenangaben</small> | `FARBE_PAPIER` | **6.47:1** | **NEIN** | ja |
| `FARBE_TINTE_MATT` <br><small>Kartentext, Nebenangaben</small> | `FARBE_PAPIER_HELL` | **7.07:1** | ja | ja |
| `FARBE_TINTE_MATT` <br><small>Kartentext, Nebenangaben</small> | `FARBE_PAPIER_DUNKEL` | **5.68:1** | **NEIN** | ja |
| `FARBE_LINIE` <br><small>Hinweise, Rubriken, ruhige Zweitzeilen</small> | `FARBE_PAPIER` | **3.01:1** | **NEIN** | **NEIN** |
| `FARBE_LINIE` <br><small>Hinweise, Rubriken, ruhige Zweitzeilen</small> | `FARBE_PAPIER_HELL` | **3.29:1** | **NEIN** | **NEIN** |
| `FARBE_LINIE` <br><small>Hinweise, Rubriken, ruhige Zweitzeilen</small> | `FARBE_PAPIER_DUNKEL` | **2.64:1** | **NEIN** | **NEIN** |
| `FARBE_LINIE_FEIN` <br><small>Rubriken auf hellem Grund</small> | `FARBE_PAPIER_HELL` | **1.99:1** | **NEIN** | **NEIN** |
| `FARBE_AKZENT` <br><small>Optionstitel, Stempel, Zustandsmarken</small> | `FARBE_PAPIER` | **6.73:1** | **NEIN** | ja |
| `FARBE_AKZENT` <br><small>Optionstitel, Stempel, Zustandsmarken</small> | `FARBE_PAPIER_HELL` | **7.35:1** | ja | ja |
| `FARBE_AKZENT` <br><small>Optionstitel, Stempel, Zustandsmarken</small> | `FARBE_PAPIER_DUNKEL` | **5.90:1** | **NEIN** | ja |
| `FARBE_AKZENT_MATT` <br><small>gedaempfte Akzente</small> | `FARBE_PAPIER` | **4.04:1** | **NEIN** | **NEIN** |
| `FARBE_AKZENT_MATT` <br><small>gedaempfte Akzente</small> | `FARBE_PAPIER_HELL` | **4.42:1** | **NEIN** | **NEIN** |
| `FARBE_TEXT_HELL` <br><small>Text auf dunklem Grund</small> | `FARBE_DUNKEL` | **12.96:1** | ja | ja |
| `FARBE_TEXT_HELL` <br><small>Text auf dunklem Grund</small> | `FARBE_DUNKEL_HELL` | **11.42:1** | ja | ja |
| `FARBE_TEXT_HELL` <br><small>Text auf dunklem Grund</small> | `FARBE_TINTE` | **11.85:1** | ja | ja |
| `FARBE_PAPIER` <br><small>Text auf der Akzentflaeche unter der Maus</small> | `FARBE_AKZENT` | **6.73:1** | **NEIN** | ja |
| `FARBE_FEHLEND` <br><small>der Pfad im Bildplatzhalter</small> | `FARBE_PAPIER_DUNKEL` | **4.29:1** | **NEIN** | **NEIN** |
| `FARBEN_STUFE[0]` <br><small>Zustandsname über dem Balken</small> | `FARBE_PAPIER` | **6.27:1** | **NEIN** | ja |
| `FARBEN_STUFE[0]` <br><small>Zustandsname über dem Balken</small> | `FARBE_PAPIER_HELL` | **6.85:1** | **NEIN** | ja |
| `FARBEN_STUFE[1]` <br><small>Zustandsname über dem Balken</small> | `FARBE_PAPIER` | **4.60:1** | **NEIN** | ja |
| `FARBEN_STUFE[1]` <br><small>Zustandsname über dem Balken</small> | `FARBE_PAPIER_HELL` | **5.03:1** | **NEIN** | ja |
| `FARBEN_STUFE[2]` <br><small>Zustandsname über dem Balken</small> | `FARBE_PAPIER` | **4.15:1** | **NEIN** | **NEIN** |
| `FARBEN_STUFE[2]` <br><small>Zustandsname über dem Balken</small> | `FARBE_PAPIER_HELL` | **4.54:1** | **NEIN** | ja |
| `FARBEN_STUFE[3]` <br><small>Zustandsname über dem Balken</small> | `FARBE_PAPIER` | **5.48:1** | **NEIN** | ja |
| `FARBEN_STUFE[3]` <br><small>Zustandsname über dem Balken</small> | `FARBE_PAPIER_HELL` | **5.99:1** | **NEIN** | ja |
| `FARBEN_STUFE[4]` <br><small>Zustandsname über dem Balken</small> | `FARBE_PAPIER` | **8.50:1** | ja | ja |
| `FARBEN_STUFE[4]` <br><small>Zustandsname über dem Balken</small> | `FARBE_PAPIER_HELL` | **9.28:1** | ja | ja |
| `FARBEN_STUFE_HELL[0]` <br><small>Zustandsname über dem Balken</small> | `FARBE_DUNKEL` | **7.61:1** | ja | ja |
| `FARBEN_STUFE_HELL[0]` <br><small>Zustandsname über dem Balken</small> | `FARBE_DUNKEL_HELL` | **6.70:1** | **NEIN** | ja |
| `FARBEN_STUFE_HELL[1]` <br><small>Zustandsname über dem Balken</small> | `FARBE_DUNKEL` | **9.13:1** | ja | ja |
| `FARBEN_STUFE_HELL[1]` <br><small>Zustandsname über dem Balken</small> | `FARBE_DUNKEL_HELL` | **8.04:1** | ja | ja |
| `FARBEN_STUFE_HELL[2]` <br><small>Zustandsname über dem Balken</small> | `FARBE_DUNKEL` | **8.35:1** | ja | ja |
| `FARBEN_STUFE_HELL[2]` <br><small>Zustandsname über dem Balken</small> | `FARBE_DUNKEL_HELL` | **7.36:1** | ja | ja |
| `FARBEN_STUFE_HELL[3]` <br><small>Zustandsname über dem Balken</small> | `FARBE_DUNKEL` | **6.98:1** | **NEIN** | ja |
| `FARBEN_STUFE_HELL[3]` <br><small>Zustandsname über dem Balken</small> | `FARBE_DUNKEL_HELL` | **6.15:1** | **NEIN** | ja |
| `FARBEN_STUFE_HELL[4]` <br><small>Zustandsname über dem Balken</small> | `FARBE_DUNKEL` | **5.40:1** | **NEIN** | ja |
| `FARBEN_STUFE_HELL[4]` <br><small>Zustandsname über dem Balken</small> | `FARBE_DUNKEL_HELL` | **4.76:1** | **NEIN** | ja |

## Wo es nicht reicht

25 Kombinationen bleiben unter 7:1. Der Vorschlag hält den
Farbton fest und verschiebt nur die Helligkeit — aus einem
gedeckten Rot wird so kein Signalrot.

| Farbe | auf | ist | Vorschlag | wäre | betrifft |
|---|---|---|---|---|---|
| `FARBE_TINTE_MATT` | `FARBE_PAPIER` | 6.47:1 | `#514b45` | 7.11:1 | Kartentext, Nebenangaben |
| `FARBE_TINTE_MATT` | `FARBE_PAPIER_DUNKEL` | 5.68:1 | `#48433d` | 7.09:1 | Kartentext, Nebenangaben |
| `FARBE_LINIE` | `FARBE_PAPIER` | 3.01:1 | `#504c44` | 7.06:1 | Hinweise, Rubriken, ruhige Zweitzeilen |
| `FARBE_LINIE` | `FARBE_PAPIER_HELL` | 3.29:1 | `#565149` | 7.11:1 | Hinweise, Rubriken, ruhige Zweitzeilen |
| `FARBE_LINIE` | `FARBE_PAPIER_DUNKEL` | 2.64:1 | `#48443d` | 7.01:1 | Hinweise, Rubriken, ruhige Zweitzeilen |
| `FARBE_LINIE_FEIN` | `FARBE_PAPIER_HELL` | 1.99:1 | `#56524a` | 7.02:1 | Rubriken auf hellem Grund |
| `FARBE_AKZENT` | `FARBE_PAPIER` | 6.73:1 | `#863123` | 7.01:1 | Optionstitel, Stempel, Zustandsmarken |
| `FARBE_AKZENT` | `FARBE_PAPIER_DUNKEL` | 5.90:1 | `#772c1f` | 7.03:1 | Optionstitel, Stempel, Zustandsmarken |
| `FARBE_AKZENT_MATT` | `FARBE_PAPIER` | 4.04:1 | `#723f32` | 7.02:1 | gedaempfte Akzente |
| `FARBE_AKZENT_MATT` | `FARBE_PAPIER_HELL` | 4.42:1 | `#7b4336` | 7.03:1 | gedaempfte Akzente |
| `FARBE_PAPIER` | `FARBE_AKZENT` | 6.73:1 | `#f2eee3` | 7.02:1 | Text auf der Akzentflaeche unter der Maus |
| `FARBE_FEHLEND` | `FARBE_PAPIER_DUNKEL` | 4.29:1 | `#841b11` | 7.09:1 | der Pfad im Bildplatzhalter |
| `FARBEN_STUFE[0]` | `FARBE_PAPIER` | 6.27:1 | `#395335` | 7.05:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE[0]` | `FARBE_PAPIER_HELL` | 6.85:1 | `#3e5939` | 7.04:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE[1]` | `FARBE_PAPIER` | 4.60:1 | `#514e2b` | 7.02:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE[1]` | `FARBE_PAPIER_HELL` | 5.03:1 | `#56542e` | 7.01:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE[2]` | `FARBE_PAPIER` | 4.15:1 | `#5f491e` | 7.06:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE[2]` | `FARBE_PAPIER_HELL` | 4.54:1 | `#664e21` | 7.08:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE[3]` | `FARBE_PAPIER` | 5.48:1 | `#773d1b` | 7.03:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE[3]` | `FARBE_PAPIER_HELL` | 5.99:1 | `#7f421c` | 7.03:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE_HELL[0]` | `FARBE_DUNKEL_HELL` | 6.70:1 | `#91b485` | 7.06:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE_HELL[3]` | `FARBE_DUNKEL` | 6.98:1 | `#dc8c61` | 7.04:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE_HELL[3]` | `FARBE_DUNKEL_HELL` | 6.15:1 | `#e19a74` | 7.06:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE_HELL[4]` | `FARBE_DUNKEL` | 5.40:1 | `#df887e` | 7.03:1 | Zustandsname über dem Balken |
| `FARBEN_STUFE_HELL[4]` | `FARBE_DUNKEL_HELL` | 4.76:1 | `#e3978e` | 7.07:1 | Zustandsname über dem Balken |

Für die Zeilen, die nur die Marke für **große** Schrift
reißen, gilt: Sie sind in Ordnung, solange der Text
tatsächlich groß gesetzt ist. Welche das sind, sagt die
letzte Spalte der Haupttabelle.

## Was das für den Unterricht heißt

Eine gerissene Marke ist kein Fehler im Spiel — sie ist eine
Aussage über den schlechtesten Fall: helles Klassenzimmer,
schwacher Beamer, letzte Reihe. Wer den Raum verdunkeln kann,
hat das Problem nicht. Deshalb steht hier eine Tabelle und
keine Reparatur.


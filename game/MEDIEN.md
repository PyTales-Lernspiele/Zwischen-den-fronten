# MEDIEN

Der Bedarfsplan. Jede Datei, die das Spiel erwartet, mit ihrer Herkunft im
Code, ihrem Status und Suchbegriffen für die Recherche.

**Erzeugt von `medienbedarf.py`. Von Hand geänderte Stellen sind beim
nächsten Lauf weg** — was hier fehlt oder falsch steht, gehört im Skript
oder im Spiel geändert.

Das Spiel läuft ohne jede dieser Dateien: Überall greift
`bild_platzhalter()` oder eine Ersatzschrift (Regel 7). Eine fehlende Datei
ist kein Fehler, sondern eine offene Aufgabe.


## Die Zahlen

| | Dateien |
|---|---|
| Erwartet | **367** |
| Davon vorhanden | **7** |
| Noch abzulegen | **360** |

| Ordner | erwartet | vorhanden | fehlt |
|---|---|---|---|
| `fonts` | 8 | 0 | 8 |
| `images/karten` | 151 | 6 | 145 |
| `images/dokumente` | 50 | 0 | 50 |
| `images/portraits` | 48 | 0 | 48 |
| `images/figuren` | 75 | 0 | 75 |
| `images` | 1 | 1 | 0 |
| `audio` | 34 | 0 | 34 |

Berücksichtigte Stimmungen: angst, einsam, erschoepft, hungrig, neutral.

Kartentypen im Bestand: 75 x karte, 4 x feldpost, 2 x lebensmittel, 2 x zeitung, 17 x amtlich.

## Zur Rechtelage

**Dieses Dokument sagt für kein einzelnes Stück, ob es frei verwendbar
ist.** Es nennt nur, wo zu suchen sich lohnt. Ob ein bestimmtes Blatt
benutzt werden darf, sagt das Haus, das es verwahrt — und niemand sonst.
Für den Unterrichtsgebrauch gelten außerdem eigene Regeln, die nicht
dieselben sind wie für eine Veröffentlichung.

Was allgemein gilt und beim Suchen hilft:

| Haus | Was dort liegt | Worauf zu achten ist |
|---|---|---|
| Deutsches Historisches Museum / LeMO | Objekte und Dokumente zur Alltagsgeschichte, gut erschlossen | Nutzungsbedingungen je Objekt; oft Anfrage nötig |
| Bundesarchiv | Amtliche Überlieferung, Bild-Bestand | Bildnachweis in vorgeschriebener Form; Lizenz je Bild verschieden |
| Europeana 1914-1918 | Privatbestände, von Familien beigetragen: Briefe, Fotos, Karten | Lizenz steht je Beitrag dabei und ist oft freier als bei Archiven |
| Landes- und Stadtarchive | Vordrucke, Bekanntmachungen, Lebensmittelkarten der eigenen Stadt | Der kürzeste Weg für regionale Bezüge; oft unkompliziert für Schulen |
| Zeitungsdigitalisate der Staatsbibliotheken | Zeitungsseiten und Extrablätter | Erschließung nach Datum; Seiten sind meist als Scan verfügbar |

**Schriften sind ein anderer Fall.** Sie kommen nicht aus einem Archiv,
sondern von einem Schriftanbieter, und sie brauchen eine Lizenz, die das
Einbetten in ein Programm erlaubt. Freie Lizenzen wie die SIL Open Font
License tun das. Eine historisch aussehende Schrift ist nicht dasselbe wie
eine historische Schrift — gesucht wird der Eindruck, nicht das Original.


## Wie diese Liste zu lesen ist

Jeder Eintrag nennt den erwarteten Pfad, wo im Code er erwartet wird, ob
die Datei schon liegt, und in welchem Maß sie angezeigt wird.

**Die Suchbegriffe stehen je Motiv, nicht je Datei.** Ein Porträt in fünf
Stimmungen ist fünf Dateien, aber eine einzige Recherche; dasselbe gilt für
die Nebenfiguren auf drei Pfaden. Wo mehrere Dateien dasselbe Motiv
brauchen, stehen die Begriffe einmal darüber.

Zwei Maße gehören zusammen und bedeuten Verschiedenes:

- **Ablagemaß** (`BILD_MASSE`) — in dieser Größe wird die Datei abgelegt.
- **Anzeigemaß** (`BILD_ANZEIGE`) — in dieser Größe erscheint sie auf dem
  Bildschirm. Kleiner als das Ablagemaß, damit auf einem großen Beamer
  nichts ausfranst.


---

## fonts — die vier Schriften

Jede Schrift wird in zwei Fassungen gesucht, `.ttf` zuerst.
Liegt keine, greift der Ersatz, und man sieht davon nichts —
außer dass alles gleich aussieht.

### SCHRIFT_DOKUMENT

*Briefe und Vordrucke; wirkt geschrieben*

Greift heute: `DejaVuSans.ttf`

- `fonts/dokument.ttf` — **fehlt**
- `fonts/dokument.otf` — **fehlt**

Suche: freie Antiqua mit vollem deutschen Zeichensatz; *free serif typeface SIL OFL*. Bezug: Schriftanbieter mit freier Lizenz (SIL OFL), nicht Archive.

### SCHRIFT_FLIESS

*Fließtext und Bedienung; die Grundschrift*

Greift heute: `DejaVuSans.ttf`

- `fonts/fliesstext.ttf` — **fehlt**
- `fonts/fliesstext.otf` — **fehlt**

Suche: freie Antiqua mit vollem deutschen Zeichensatz; *free serif typeface SIL OFL*. Bezug: Schriftanbieter mit freier Lizenz (SIL OFL), nicht Archive.

### SCHRIFT_SCHMAL

*Aufdrucke: Stempel, Aktenzeichen, Rubriken*

Greift heute: `DejaVuSans.ttf`

- `fonts/schmal.ttf` — **fehlt**
- `fonts/schmal.otf` — **fehlt**

Suche: freie Antiqua mit vollem deutschen Zeichensatz; *free serif typeface SIL OFL*. Bezug: Schriftanbieter mit freier Lizenz (SIL OFL), nicht Archive.

### SCHRIFT_TITEL

*Überschriften, Ereignistext, Kartentitel*

Greift heute: `DejaVuSans.ttf`

- `fonts/titel.ttf` — **fehlt**
- `fonts/titel.otf` — **fehlt**

Suche: freie Antiqua mit vollem deutschen Zeichensatz; *free serif typeface SIL OFL*. Bezug: Schriftanbieter mit freier Lizenz (SIL OFL), nicht Archive.

---

## images/karten — Szenenbilder

Ein Bild je Option. Es zeigt die Lage, nicht die Entscheidung: kein Bild, auf dem schon jemand tut, was die Spielerin erst wählen soll.

Ablagemaß (800, 450), Anzeigemaß (468, 264). 151 Dateien, davon 6 vorhanden.

### front_1914_marsch

1914 · front · Belgien

- `images/karten/front_1914_marsch_1.png` — Option 1, vorhanden
- `images/karten/front_1914_marsch_2.png` — Option 2, vorhanden

Suche: *Marsch 1914*, *Fotografie Belgien 1914*; englisch *photograph Western Front, trench 1914*.

Der Beleg des Ereignisses nennt: Marschleistungen im Aufmarsch August 1914

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1914_dorf

1914 · front · Nordfrankreich

- `images/karten/front_1914_dorf_1.png` — Option 1, vorhanden
- `images/karten/front_1914_dorf_2.png` — Option 2, vorhanden

Suche: *Dorf 1914*, *Fotografie Nordfrankreich 1914*; englisch *photograph Western Front, trench 1914*.

Der Beleg des Ereignisses nennt: Requisition und Plünderungsverbot im Feldheer

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1914_erster_toter

1914 · front · Nordfrankreich

- `images/karten/front_1914_erster_toter_1.png` — Option 1, vorhanden
- `images/karten/front_1914_erster_toter_2.png` — Option 2, vorhanden

Suche: *Gefallener am Wegrand 1914*, *Fotografie Nordfrankreich 1914*; englisch *photograph Western Front, trench 1914*.

Der Beleg des Ereignisses nennt: Erkennungsmarke und Verlustmeldung im Feldheer

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1914_schanzen

1914 · front · Flandern

- `images/karten/front_1914_schanzen_1.png` — Option 1, **fehlt**
- `images/karten/front_1914_schanzen_2.png` — Option 2, **fehlt**

Suche: *Schanzen 1914*, *Fotografie Flandern 1914*; englisch *photograph Western Front, trench 1914*.

Der Beleg des Ereignisses nennt: Übergang zum Stellungskrieg, Herbst 1914

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1914_weihnachten

1914 · front · Flandern

- `images/karten/front_1914_weihnachten_1.png` — Option 1, **fehlt**
- `images/karten/front_1914_weihnachten_2.png` — Option 2, **fehlt**

Suche: *Weihnachten 1914*, *Fotografie Flandern 1914*; englisch *photograph Western Front, trench 1914*.

Der Beleg des Ereignisses nennt: Weihnachtsfrieden 1914 und die Verbote danach

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_trommelfeuer

1914-1918 · front · Grabenstellung

- `images/karten/front_trommelfeuer_1.png` — Option 1, **fehlt**
- `images/karten/front_trommelfeuer_2.png` — Option 2, **fehlt**

Suche: *Trommelfeuer 1914-1918*, *Fotografie Grabenstellung 1914-1918*; englisch *photograph Western Front, trench 1914-1918*.

Der Beleg des Ereignisses nennt: Trommelfeuer als neue Erfahrung des Materialkriegs

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_kamerad

1915-1917 · front · Grabenstellung

- `images/karten/front_kamerad_1.png` — Option 1, **fehlt**
- `images/karten/front_kamerad_2.png` — Option 2, **fehlt**

Suche: *Kamerad 1915-1917*, *Fotografie Grabenstellung 1915-1917*; englisch *photograph Western Front, trench 1915-1917*.

Der Beleg des Ereignisses nennt: Unerlaubte Entfernung vor dem Kriegsgericht

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_nachfrage

1915-1918 · front, etappe · Etappe

- `images/karten/front_nachfrage_1.png` — Option 1, **fehlt**
- `images/karten/front_nachfrage_2.png` — Option 2, **fehlt**

Suche: *Nachfrage 1915-1918*, *Fotografie Etappe 1915-1918*; englisch *photograph Western Front, trench 1915-1918*.

Der Beleg des Ereignisses nennt: Der Gerichtsherr und das militärische Ermittlungsverfahren

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_gas

1915-1916 · front · Grabenstellung

- `images/karten/front_gas_1.png` — Option 1, **fehlt**
- `images/karten/front_gas_2.png` — Option 2, **fehlt**

Suche: *Gas 1915-1916*, *Fotografie Grabenstellung 1915-1916*; englisch *photograph Western Front, trench 1915-1916*.

Der Beleg des Ereignisses nennt: Erster Chlorgaseinsatz bei Ypern, 22. April 1915

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_laeuse

1915-1918 · front · Grabenstellung

- `images/karten/front_laeuse_1.png` — Option 1, **fehlt**
- `images/karten/front_laeuse_2.png` — Option 2, **fehlt**

Suche: *Laeuse 1915-1918*, *Fotografie Grabenstellung 1915-1918*; englisch *photograph Western Front, trench 1915-1918*.

Der Beleg des Ereignisses nennt: Wolhynisches Fieber, übertragen durch Kleiderläuse

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_beute

1915-1918 · front · Niemandsland

- `images/karten/front_beute_1.png` — Option 1, **fehlt**
- `images/karten/front_beute_2.png` — Option 2, **fehlt**

Suche: *Beute 1915-1918*, *Fotografie Niemandsland 1915-1918*; englisch *photograph Western Front, trench 1915-1918*.

Der Beleg des Ereignisses nennt: Verbot der Leichenfledderei im Feldheer

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_stosstrupp

1915-1916 · front · Grabenstellung

- `images/karten/front_stosstrupp_1.png` — Option 1, **fehlt**
- `images/karten/front_stosstrupp_2.png` — Option 2, **fehlt**

Suche: *Stoßtrupp 1915-1916*, *Fotografie Grabenstellung 1915-1916*; englisch *photograph Western Front, trench 1915-1916*.

Der Beleg des Ereignisses nennt: Stoßtruppunternehmen und Urlaub als Anreiz

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_urlaub

1915-1918 · front, etappe · Heimatstadt

- `images/karten/front_urlaub_1.png` — Option 1, **fehlt**
- `images/karten/front_urlaub_2.png` — Option 2, **fehlt**

Suche: *Urlaub 1915-1918*, *Fotografie Heimatstadt 1915-1918*; englisch *photograph Western Front, trench 1915-1918*.

Der Beleg des Ereignisses nennt: Heimaturlaub und das Schweigen darüber

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1916_verdun

1916 · front · Verdun

- `images/karten/front_1916_verdun_1.png` — Option 1, **fehlt**
- `images/karten/front_1916_verdun_2.png` — Option 2, **fehlt**

Suche: *Verdun 1916*, *Fotografie Verdun 1916*; englisch *photograph Western Front, trench 1916*.

Der Beleg des Ereignisses nennt: Schlacht um Verdun, 21. Februar bis Dezember 1916

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1916_hunger

1916 · front · Grabenstellung

- `images/karten/front_1916_hunger_1.png` — Option 1, **fehlt**
- `images/karten/front_1916_hunger_2.png` — Option 2, **fehlt**

Suche: *Hunger 1916*, *Fotografie Grabenstellung 1916*; englisch *photograph Western Front, trench 1916*.

Der Beleg des Ereignisses nennt: Verpflegungslage der Feldtruppe 1916

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1916_gefangener

1916 · front · Somme

- `images/karten/front_1916_gefangener_1.png` — Option 1, **fehlt**
- `images/karten/front_1916_gefangener_2.png` — Option 2, **fehlt**

Suche: *Gefangener 1916*, *Fotografie Somme 1916*; englisch *photograph Western Front, trench 1916*.

Der Beleg des Ereignisses nennt: Haager Landkriegsordnung: Schutz der Kriegsgefangenen

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_brotschlange

1914-1918 · heimat · Wohnviertel

- `images/karten/heimat_brotschlange_1.png` — Option 1, **fehlt**
- `images/karten/heimat_brotschlange_2.png` — Option 2, **fehlt**

Suche: *Brotschlange 1914-1918*, *Fotografie Wohnviertel 1914-1918*; englisch *photograph German home front 1914-1918*.

Der Beleg des Ereignisses nennt: Höchstpreise und Kettenhandel als Straftatbestand

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1914_post

1914-1915 · heimat · Wohnviertel

- `images/karten/heimat_1914_post_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1914_post_2.png` — Option 2, **fehlt**

Suche: *Post 1914-1915*, *Fotografie Wohnviertel 1914-1915*; englisch *photograph German home front 1914-1915*.

Der Beleg des Ereignisses nennt: Vermisstensuche und Wahrsagerei im Krieg

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1914_liebesgaben

1914 · heimat · Gemeindesaal

- `images/karten/heimat_1914_liebesgaben_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1914_liebesgaben_2.png` — Option 2, **fehlt**

Suche: *Liebesgaben 1914*, *Fotografie Gemeindesaal 1914*; englisch *photograph German home front 1914*.

Der Beleg des Ereignisses nennt: Liebesgabensammlungen des Vaterländischen Frauenvereins

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_denunziation

1915-1918 · heimat · Wohnviertel

- `images/karten/heimat_denunziation_1.png` — Option 1, **fehlt**
- `images/karten/heimat_denunziation_2.png` — Option 2, **fehlt**

Suche: *Denunziation 1915-1918*, *Fotografie Wohnviertel 1915-1918*; englisch *photograph German home front 1915-1918*.

Der Beleg des Ereignisses nennt: Anzeigen wegen Hortens bei der Polizei

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_hamsterfahrt

1915-1918 · heimat · Bahnhof

- `images/karten/heimat_hamsterfahrt_1.png` — Option 1, **fehlt**
- `images/karten/heimat_hamsterfahrt_2.png` — Option 2, **fehlt**

Suche: *Hamsterfahrt 1915-1918*, *Fotografie Bahnhof 1915-1918*; englisch *photograph German home front 1915-1918*.

Der Beleg des Ereignisses nennt: Hamsterfahrten und Bahnsteigkontrollen

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_fabrik

1915-1918 · heimat · Rüstungsbetrieb

- `images/karten/heimat_fabrik_1.png` — Option 1, **fehlt**
- `images/karten/heimat_fabrik_2.png` — Option 2, **fehlt**

Suche: *Fabrik 1915-1918*, *Fotografie Rüstungsbetrieb 1915-1918*; englisch *photograph German home front 1915-1918*.

Der Beleg des Ereignisses nennt: Akkord und Schwerarbeiterzulage in der Rüstung

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_lazarettzug

1914-1918 · heimat, etappe · Güterbahnhof

- `images/karten/heimat_lazarettzug_1.png` — Option 1, **fehlt**
- `images/karten/heimat_lazarettzug_2.png` — Option 2, **fehlt**

Suche: *Lazarettzug 1914-1918*, *Fotografie Güterbahnhof 1914-1918*; englisch *photograph German home front 1914-1918*.

Der Beleg des Ereignisses nennt: Lazarettzüge und freiwillige Helferinnen am Bahnhof

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1916_rueben

1916 · heimat · Stadtrand

- `images/karten/heimat_1916_rueben_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1916_rueben_2.png` — Option 2, **fehlt**

Suche: *Rüben 1916*, *Fotografie Stadtrand 1916*; englisch *photograph German home front 1916*.

Der Beleg des Ereignisses nennt: Steckrübenwinter 1916/17 nach der Kartoffelmissernte

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1916_kohle

1916 · heimat · Wohnviertel

- `images/karten/heimat_1916_kohle_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1916_kohle_2.png` — Option 2, **fehlt**

Suche: *Kohle 1916*, *Fotografie Wohnviertel 1916*; englisch *photograph German home front 1916*.

Der Beleg des Ereignisses nennt: Kohlenmangel: Waggons an der Front statt in der Stadt

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1916_arbeitsniederlegung

1916 · heimat · Rüstungsbetrieb

- `images/karten/heimat_1916_arbeitsniederlegung_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1916_arbeitsniederlegung_2.png` — Option 2, **fehlt**

Suche: *Arbeitsniederlegung 1916*, *Fotografie Rüstungsbetrieb 1916*; englisch *photograph German home front 1916*.

Der Beleg des Ereignisses nennt: Belagerungszustandsgesetz vom 4. Juni 1851

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1916_kinderarbeit

1916 · heimat · Wohnviertel

- `images/karten/heimat_1916_kinderarbeit_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1916_kinderarbeit_2.png` — Option 2, **fehlt**

Suche: *Kinderarbeit 1916*, *Fotografie Wohnviertel 1916*; englisch *photograph German home front 1916*.

Der Beleg des Ereignisses nennt: Jugendliche in der Rüstung und die Schulpflicht

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_ruhequartier

1915-1918 · front · Ruhequartier

- `images/karten/front_ruhequartier_1.png` — Option 1, **fehlt**
- `images/karten/front_ruhequartier_2.png` — Option 2, **fehlt**

Suche: *Ruhequartier 1915-1918*, *Fotografie Ruhequartier 1915-1918*; englisch *photograph Western Front, trench 1915-1918*.

Der Beleg des Ereignisses nennt: Ablösung und Ruhequartier im Stellungskrieg

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_sonntag

1914-1918 · heimat · Wohnviertel

- `images/karten/heimat_sonntag_1.png` — Option 1, **fehlt**
- `images/karten/heimat_sonntag_2.png` — Option 2, **fehlt**

Suche: *Sonntag 1914-1918*, *Fotografie Wohnviertel 1914-1918*; englisch *photograph German home front 1914-1918*.

Der Beleg des Ereignisses nennt: Sonntag als freier Tag im Kriegsalltag

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### einstieg_meldung

1914-1918 · front, etappe, heimat · Kreisstadt

- `images/karten/einstieg_meldung_1.png` — Option 1, **fehlt**
- `images/karten/einstieg_meldung_2.png` — Option 2, **fehlt**

Suche: *Meldung 1914-1918*, *Fotografie Kreisstadt 1914-1918*; englisch *photograph Western Front, trench 1914-1918*.

Der Beleg des Ereignisses nennt: Kriegsfreiwillige und der Weg über den Jahrgang

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### einstieg_offizier

1914-1918 · front, etappe, heimat · Ersatztruppenteil

- `images/karten/einstieg_offizier_1.png` — Option 1, **fehlt**
- `images/karten/einstieg_offizier_2.png` — Option 2, **fehlt**

Suche: *Offizier 1914-1918*, *Fotografie Ersatztruppenteil 1914-1918*; englisch *photograph Western Front, trench 1914-1918*.

Der Beleg des Ereignisses nennt: Der Einjährig-Freiwillige und die Offizierslaufbahn

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### einstieg_abschied

1914-1918 · front, etappe, heimat · Bahnhofshalle

- `images/karten/einstieg_abschied_1.png` — Option 1, **fehlt**
- `images/karten/einstieg_abschied_2.png` — Option 2, **fehlt**

Suche: *Abschied 1914-1918*, *Fotografie Bahnhofshalle 1914-1918*; englisch *photograph Western Front, trench 1914-1918*.

Der Beleg des Ereignisses nennt: Abschied am Bahnhof, August 1914

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1917_verbruederung_nachhall

1917 · front · Grabenstellung

- `images/karten/front_1917_verbruederung_nachhall_1.png` — Option 1, **fehlt**
- `images/karten/front_1917_verbruederung_nachhall_2.png` — Option 2, **fehlt**

Suche: *Verbruederung nachhall 1917*, *Fotografie Grabenstellung 1917*; englisch *photograph Western Front, trench 1917*.

Der Beleg des Ereignisses nennt: Divisionsbefehle gegen Verbrüderung nach 1914

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1917_aprilstreik

1917 · heimat · Rüstungsbetrieb

- `images/karten/heimat_1917_aprilstreik_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1917_aprilstreik_2.png` — Option 2, **fehlt**

Suche: *Aprilstreik 1917*, *Fotografie Rüstungsbetrieb 1917*; englisch *photograph German home front 1917*.

Der Beleg des Ereignisses nennt: Aprilstreiks 1917 nach der Kürzung der Brotration

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1917_ablieferung

1917 · heimat · Bauernhof

- `images/karten/heimat_1917_ablieferung_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1917_ablieferung_2.png` — Option 2, **fehlt**

Suche: *Ablieferung 1917*, *Fotografie Bauernhof 1917*; englisch *photograph German home front 1917*.

Der Beleg des Ereignisses nennt: Ablieferungspflicht und Erntekommissionen

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1917_akkord

1917 · heimat · Rüstungsbetrieb

- `images/karten/heimat_1917_akkord_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1917_akkord_2.png` — Option 2, **fehlt**

Suche: *Akkord 1917*, *Fotografie Rüstungsbetrieb 1917*; englisch *photograph German home front 1917*.

Der Beleg des Ereignisses nennt: Akkordarbeit in der Munitionsfertigung

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1917_steckruebe

1917-1918 · front · Grabenstellung

- `images/karten/front_1917_steckruebe_1.png` — Option 1, **fehlt**
- `images/karten/front_1917_steckruebe_2.png` — Option 2, **fehlt**

Suche: *Steckruebe 1917-1918*, *Fotografie Grabenstellung 1917-1918*; englisch *photograph Western Front, trench 1917-1918*.

Der Beleg des Ereignisses nennt: Verpflegung im Feldheer 1917 und 1918

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1917_geruecht_osten

1917 · front · Grabenstellung

- `images/karten/front_1917_geruecht_osten_1.png` — Option 1, **fehlt**
- `images/karten/front_1917_geruecht_osten_2.png` — Option 2, **fehlt**

Suche: *Geruecht osten 1917*, *Fotografie Grabenstellung 1917*; englisch *photograph Western Front, trench 1917*.

Der Beleg des Ereignisses nennt: Feldpost 1917 über Gerüchte aus dem Osten

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1917_winterstellung

1917-1918 · front · Grabenstellung

- `images/karten/front_1917_winterstellung_1.png` — Option 1, **fehlt**
- `images/karten/front_1917_winterstellung_2.png` — Option 2, **fehlt**

Suche: *Winterstellung 1917-1918*, *Fotografie Grabenstellung 1917-1918*; englisch *photograph Western Front, trench 1917-1918*.

Der Beleg des Ereignisses nennt: Soldatenbrief über Kälte und Brennholz im Winter

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1917_ablosung

1917 · front · Grabenstellung

- `images/karten/front_1917_ablosung_1.png` — Option 1, **fehlt**
- `images/karten/front_1917_ablosung_2.png` — Option 2, **fehlt**

Suche: *Ablosung 1917*, *Fotografie Grabenstellung 1917*; englisch *photograph Western Front, trench 1917*.

Der Beleg des Ereignisses nennt: Ersatztransporte und Landsturm an der Front 1917

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1917_kohlennot

1917-1918 · heimat · Wohnviertel

- `images/karten/heimat_1917_kohlennot_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1917_kohlennot_2.png` — Option 2, **fehlt**

Suche: *Kohlennot 1917-1918*, *Fotografie Wohnviertel 1917-1918*; englisch *photograph German home front 1917-1918*.

Der Beleg des Ereignisses nennt: Kohlennot in den Kriegswintern 1917 und 1918

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1917_metallsammlung

1917-1918 · heimat · Wohnviertel

- `images/karten/heimat_1917_metallsammlung_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1917_metallsammlung_2.png` — Option 2, **fehlt**

Suche: *Metallsammlung 1917-1918*, *Fotografie Wohnviertel 1917-1918*; englisch *photograph German home front 1917-1918*.

Der Beleg des Ereignisses nennt: Metallsammlungen und Glockenabgabe ab 1917

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1918_abrechnung

1918 · front · Straße

- `images/karten/front_1918_abrechnung_1.png` — Option 1, **fehlt**
- `images/karten/front_1918_abrechnung_2.png` — Option 2, **fehlt**

Suche: *Abrechnung 1918*, *Fotografie Straße 1918*; englisch *photograph Western Front, trench 1918*.

Der Beleg des Ereignisses nennt: Feldstrafgefangenenabteilungen im Feldheer

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1918_liste

1918 · front, etappe · Etappe

- `images/karten/front_1918_liste_1.png` — Option 1, **fehlt**
- `images/karten/front_1918_liste_2.png` — Option 2, **fehlt**

Suche: *Liste 1918*, *Fotografie Etappe 1918*; englisch *photograph Western Front, trench 1918*.

Der Beleg des Ereignisses nennt: Rückkehr aus russischer Gefangenschaft 1918

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1918_freiwillig_von_1914

1918 · front · Ruhequartier

- `images/karten/front_1918_freiwillig_von_1914_1.png` — Option 1, **fehlt**
- `images/karten/front_1918_freiwillig_von_1914_2.png` — Option 2, **fehlt**

Suche: *Freiwillig von 1914 1918*, *Fotografie Ruhequartier 1918*; englisch *photograph Western Front, trench 1918*.

Der Beleg des Ereignisses nennt: Kriegsfreiwillige von 1914 und ihre Verluste

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1918_rat

1918 · heimat · Rüstungsbetrieb

- `images/karten/heimat_1918_rat_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1918_rat_2.png` — Option 2, **fehlt**

Suche: *Rat 1918*, *Fotografie Rüstungsbetrieb 1918*; englisch *photograph German home front 1918*.

Der Beleg des Ereignisses nennt: Arbeiter- und Soldatenräte im November 1918

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### lazarett_1918_grippestation

1918 · front, etappe, heimat · Lazarett

- `images/karten/lazarett_1918_grippestation_1.png` — Option 1, **fehlt**
- `images/karten/lazarett_1918_grippestation_2.png` — Option 2, **fehlt**

Suche: *Lazarett 1918 grippestation 1918*, *Fotografie Lazarett 1918*; englisch *photograph Western Front, trench 1918*.

Der Beleg des Ereignisses nennt: Grippestationen in Lazaretten im Herbst 1918

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1918_offensive

1918 · front · Niemandsland

- `images/karten/front_1918_offensive_1.png` — Option 1, **fehlt**
- `images/karten/front_1918_offensive_2.png` — Option 2, **fehlt**

Suche: *Offensive 1918*, *Fotografie Niemandsland 1918*; englisch *photograph Western Front, trench 1918*.

Der Beleg des Ereignisses nennt: Deutsche Frühjahrsoffensive ab 21. März 1918

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1918_kokarde

1918 · front · Etappe

- `images/karten/front_1918_kokarde_1.png` — Option 1, **fehlt**
- `images/karten/front_1918_kokarde_2.png` — Option 2, **fehlt**

Suche: *Kokarde 1918*, *Fotografie Etappe 1918*; englisch *photograph Western Front, trench 1918*.

Der Beleg des Ereignisses nennt: Matrosen und Novembertage 1918

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### front_1918_waffenstillstand

1918 · front · Grabenstellung

- `images/karten/front_1918_waffenstillstand_1.png` — Option 1, **fehlt**
- `images/karten/front_1918_waffenstillstand_2.png` — Option 2, **fehlt**

Suche: *Waffenstillstand 1918*, *Fotografie Grabenstellung 1918*; englisch *photograph Western Front, trench 1918*.

Der Beleg des Ereignisses nennt: Waffenstillstand vom 11. November 1918

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1918_januarstreik

1918 · heimat · Rüstungsbetrieb

- `images/karten/heimat_1918_januarstreik_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1918_januarstreik_2.png` — Option 2, **fehlt**

Suche: *Januarstreik 1918*, *Fotografie Rüstungsbetrieb 1918*; englisch *photograph German home front 1918*.

Der Beleg des Ereignisses nennt: Januarstreik 1918 in Berlin und anderen Städten

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### heimat_1918_matrosen

1918 · heimat · Bahnhof

- `images/karten/heimat_1918_matrosen_1.png` — Option 1, **fehlt**
- `images/karten/heimat_1918_matrosen_2.png` — Option 2, **fehlt**

Suche: *Matrosen 1918*, *Fotografie Bahnhof 1918*; englisch *photograph German home front 1918*.

Der Beleg des Ereignisses nennt: Matrosenaufstand und Rätebildung im November

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_1914_ankunft

1914 · etappe · Etappenort

- `images/karten/etappe_1914_ankunft_1.png` — Option 1, **fehlt**
- `images/karten/etappe_1914_ankunft_2.png` — Option 2, **fehlt**

Suche: *Ankunft 1914*, *Fotografie Etappenort 1914*; englisch *photograph rear area, lines of communication 1914*.

Der Beleg des Ereignisses nennt: Etappenordnung: Kommandanturen und Magazine

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_bahnhofsdienst

1914-1918 · etappe · Bahnhof

- `images/karten/etappe_bahnhofsdienst_1.png` — Option 1, **fehlt**
- `images/karten/etappe_bahnhofsdienst_2.png` — Option 2, **fehlt**

Suche: *Bahnhofsdienst 1914-1918*, *Fotografie Bahnhof 1914-1918*; englisch *photograph rear area, lines of communication 1914-1918*.

Der Beleg des Ereignisses nennt: Bahnhofskommandanturen und Militärfahrplan

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_verpflegungsausgabe

1914-1918 · etappe · Magazin

- `images/karten/etappe_verpflegungsausgabe_1.png` — Option 1, **fehlt**
- `images/karten/etappe_verpflegungsausgabe_2.png` — Option 2, **fehlt**

Suche: *Verpflegungsausgabe 1914-1918*, *Fotografie Magazin 1914-1918*; englisch *photograph rear area, lines of communication 1914-1918*.

Der Beleg des Ereignisses nennt: Verpflegungsstärke und Ausgabelisten der Etappe

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_verwundetenzug

1914-1918 · etappe · Verwundetensammelstelle

- `images/karten/etappe_verwundetenzug_1.png` — Option 1, **fehlt**
- `images/karten/etappe_verwundetenzug_2.png` — Option 2, **fehlt**

Suche: *Verwundetenzug 1914-1918*, *Fotografie Verwundetensammelstelle 1914-1918*; englisch *photograph rear area, lines of communication 1914-1918*.

Der Beleg des Ereignisses nennt: Verwundetentransport und Sichtung in der Etappe

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_listen

1915-1918 · etappe · Schreibstube

- `images/karten/etappe_listen_1.png` — Option 1, **fehlt**
- `images/karten/etappe_listen_2.png` — Option 2, **fehlt**

Suche: *Listen 1915-1918*, *Fotografie Schreibstube 1915-1918*; englisch *photograph rear area, lines of communication 1915-1918*.

Der Beleg des Ereignisses nennt: Stärkemeldungen und Verpflegungslisten

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_fronturlauber

1915-1918 · etappe · Bahnsteig

- `images/karten/etappe_fronturlauber_1.png` — Option 1, **fehlt**
- `images/karten/etappe_fronturlauber_2.png` — Option 2, **fehlt**

Suche: *Fronturlauber 1915-1918*, *Fotografie Bahnsteig 1915-1918*; englisch *photograph rear area, lines of communication 1915-1918*.

Der Beleg des Ereignisses nennt: Frontsprache über die Etappe: das Etappenschwein

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_feldbaeckerei

1914-1918 · etappe · Feldbäckerei

- `images/karten/etappe_feldbaeckerei_1.png` — Option 1, **fehlt**
- `images/karten/etappe_feldbaeckerei_2.png` — Option 2, **fehlt**

Suche: *Feldbaeckerei 1914-1918*, *Fotografie Feldbäckerei 1914-1918*; englisch *photograph rear area, lines of communication 1914-1918*.

Der Beleg des Ereignisses nennt: Feldbäckereikolonnen und die Streckung des Brotes

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_munitionslager

1915-1918 · etappe · Munitionslager

- `images/karten/etappe_munitionslager_1.png` — Option 1, **fehlt**
- `images/karten/etappe_munitionslager_2.png` — Option 2, **fehlt**

Suche: *Munitionslager 1915-1918*, *Fotografie Munitionslager 1915-1918*; englisch *photograph rear area, lines of communication 1915-1918*.

Der Beleg des Ereignisses nennt: Munitionsausgabe und Nachschub der Etappe

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_fuhrpark

1914-1916 · etappe · Pferdedepot

- `images/karten/etappe_fuhrpark_1.png` — Option 1, **fehlt**
- `images/karten/etappe_fuhrpark_2.png` — Option 2, **fehlt**

Suche: *Fuhrpark 1914-1916*, *Fotografie Pferdedepot 1914-1916*; englisch *photograph rear area, lines of communication 1914-1916*.

Der Beleg des Ereignisses nennt: Pferde im Heer: Ersatz, Futter und Verluste

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_1917_nachschubstockung

1917 · etappe · Etappenort

- `images/karten/etappe_1917_nachschubstockung_1.png` — Option 1, **fehlt**
- `images/karten/etappe_1917_nachschubstockung_2.png` — Option 2, **fehlt**

Suche: *Nachschubstockung 1917*, *Fotografie Etappenort 1917*; englisch *photograph rear area, lines of communication 1917*.

Der Beleg des Ereignisses nennt: Nachschubstockungen und Bestandsaufnahmen 1917

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_1914_gefangenenlager

1914 · etappe · Gefangenenlager

- `images/karten/etappe_1914_gefangenenlager_1.png` — Option 1, **fehlt**
- `images/karten/etappe_1914_gefangenenlager_2.png` — Option 2, **fehlt**

Suche: *Gefangenenlager 1914*, *Fotografie Gefangenenlager 1914*; englisch *photograph rear area, lines of communication 1914*.

Der Beleg des Ereignisses nennt: Kriegsgefangenenlager im ersten Kriegsherbst

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_gefangenenarbeit

1915-1918 · etappe · Arbeitsstelle

- `images/karten/etappe_gefangenenarbeit_1.png` — Option 1, **fehlt**
- `images/karten/etappe_gefangenenarbeit_2.png` — Option 2, **fehlt**

Suche: *Gefangenenarbeit 1915-1918*, *Fotografie Arbeitsstelle 1915-1918*; englisch *photograph rear area, lines of communication 1915-1918*.

Der Beleg des Ereignisses nennt: Haager Landkriegsordnung, Artikel 6: Gefangenenarbeit

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_1918_grippe

1918 · etappe · Etappenlazarett

- `images/karten/etappe_1918_grippe_1.png` — Option 1, **fehlt**
- `images/karten/etappe_1918_grippe_2.png` — Option 2, **fehlt**

Suche: *Grippe 1918*, *Fotografie Etappenlazarett 1918*; englisch *photograph rear area, lines of communication 1918*.

Der Beleg des Ereignisses nennt: Die Grippe von 1918 in Lazaretten und Etappe

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_1918_raeumung

1918 · etappe · Etappenort

- `images/karten/etappe_1918_raeumung_1.png` — Option 1, **fehlt**
- `images/karten/etappe_1918_raeumung_2.png` — Option 2, **fehlt**

Suche: *Räumung 1918*, *Fotografie Etappenort 1918*; englisch *photograph rear area, lines of communication 1918*.

Der Beleg des Ereignisses nennt: Räumung der Etappe in den letzten Kriegswochen

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_innendienst

1915-1918 · etappe · Bahnhofslazarett

- `images/karten/etappe_innendienst_1.png` — Option 1, **fehlt**
- `images/karten/etappe_innendienst_2.png` — Option 2, **fehlt**

Suche: *Innendienst 1915-1918*, *Fotografie Bahnhofslazarett 1915-1918*; englisch *photograph rear area, lines of communication 1915-1918*.

Der Beleg des Ereignisses nennt: Innendienst und Schonung im Etappensanitätsdienst

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_quartier

1914-1918 · etappe · Quartier

- `images/karten/etappe_quartier_1.png` — Option 1, **fehlt**
- `images/karten/etappe_quartier_2.png` — Option 2, **fehlt**

Suche: *Quartier 1914-1918*, *Fotografie Quartier 1914-1918*; englisch *photograph rear area, lines of communication 1914-1918*.

Der Beleg des Ereignisses nennt: Einquartierung im besetzten Gebiet

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### etappe_abloesung

1916-1918 · etappe · Etappenkommandantur

- `images/karten/etappe_abloesung_1.png` — Option 1, **fehlt**
- `images/karten/etappe_abloesung_2.png` — Option 2, **fehlt**

Suche: *Abloesung 1916-1918*, *Fotografie Etappenkommandantur 1916-1918*; englisch *photograph rear area, lines of communication 1916-1918*.

Der Beleg des Ereignisses nennt: Ablösung und Ruhestellung in der Etappe

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### epilog_1919_heimkehr

1919 · front, etappe · Bahnhof

- `images/karten/epilog_1919_heimkehr_1.png` — Option 1, **fehlt**
- `images/karten/epilog_1919_heimkehr_2.png` — Option 2, **fehlt**

Suche: *Heimkehr 1919*, *Fotografie Bahnhof 1919*; englisch *photograph Western Front, trench 1919*.

Der Beleg des Ereignisses nennt: Heimkehr und Demobilmachung nach dem Waffenstillstand

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### epilog_1919_rueckkehrer

1919 · heimat · Wohnviertel

- `images/karten/epilog_1919_rueckkehrer_1.png` — Option 1, **fehlt**
- `images/karten/epilog_1919_rueckkehrer_2.png` — Option 2, **fehlt**

Suche: *Rueckkehrer 1919*, *Fotografie Wohnviertel 1919*; englisch *photograph German home front 1919*.

Der Beleg des Ereignisses nennt: Rückkehr der Männer und die Arbeit der Frauen

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### epilog_1919_werktor

1919 · front, etappe, heimat · Werktor

- `images/karten/epilog_1919_werktor_1.png` — Option 1, **fehlt**
- `images/karten/epilog_1919_werktor_2.png` — Option 2, **fehlt**

Suche: *Werktor 1919*, *Fotografie Werktor 1919*; englisch *photograph Western Front, trench 1919*.

Der Beleg des Ereignisses nennt: Demobilmachung und Entlassung der Frauen

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### epilog_1919_wahl

1919 · front, etappe, heimat · Wahllokal

- `images/karten/epilog_1919_wahl_1.png` — Option 1, **fehlt**
- `images/karten/epilog_1919_wahl_2.png` — Option 2, **fehlt**

Suche: *Wahl 1919*, *Fotografie Wahllokal 1919*; englisch *photograph Western Front, trench 1919*.

Der Beleg des Ereignisses nennt: Wahl zur Nationalversammlung am 19. Januar 1919

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### epilog_1919_blockade

1919 · front, etappe, heimat · Wohnviertel

- `images/karten/epilog_1919_blockade_1.png` — Option 1, **fehlt**
- `images/karten/epilog_1919_blockade_2.png` — Option 2, **fehlt**

Suche: *Blockade 1919*, *Fotografie Wohnviertel 1919*; englisch *photograph Western Front, trench 1919*.

Der Beleg des Ereignisses nennt: Seeblockade bis zum Sommer 1919 und der Hunger danach

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

### wirtshaus_wahl

1919 · front, etappe, heimat · Wirtshaus

- `images/karten/wirtshaus_wahl_1.png` — Option 1, **fehlt**
- `images/karten/wirtshaus_wahl_2.png` — Option 2, **fehlt**
- `images/karten/wirtshaus_wahl_3.png` — Option 3, **fehlt**

Suche: *Wirtshaus wahl 1919*, *Fotografie Wirtshaus 1919*; englisch *photograph Western Front, trench 1919*.

Der Beleg des Ereignisses nennt: Die Behauptung vom unbesiegten Heer, ab November 1918

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)

---

## images/dokumente — Dokumentmotive

Dieselbe Stelle im Bildschirm, aber ein anderer Bestand: ein abfotografiertes Blatt, nah und fast quadratisch. Welche Karte hierher gehört, entscheidet ihr Kartentyp.

Ablagemaß (900, 600), Anzeigemaß (720, 480). 50 Dateien, davon 0 vorhanden.

### front_feldpost

1914-1918 · front, etappe · Grabenstellung

- `images/dokumente/front_feldpost_1.png` — Option 1, **fehlt**
- `images/dokumente/front_feldpost_2.png` — Option 2, **fehlt**

Suche: *Feldpost 1914-1918*, *Feldpostbrief Grabenstellung 1914-1918*; englisch *field post letter Western Front, trench 1914-1918*.

Der Beleg des Ereignisses nennt: Feldpost: rund 28,7 Milliarden Sendungen 1914-1918

Wo suchen: Museum für Kommunikation / Europeana 1914-1918 (Privatbestände)

### front_1916_zaehlung

1916 · front, etappe · Etappe

- `images/dokumente/front_1916_zaehlung_1.png` — Option 1, **fehlt**
- `images/dokumente/front_1916_zaehlung_2.png` — Option 2, **fehlt**

Suche: *Zählung 1916*, *Vordruck Etappe 1916*; englisch *official form Western Front, trench 1916*.

Der Beleg des Ereignisses nennt: Judenzählung im Heer, Oktober 1916

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_kriegsanleihe

1914-1918 · heimat · Wohnviertel

- `images/dokumente/heimat_kriegsanleihe_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_kriegsanleihe_2.png` — Option 2, **fehlt**

Suche: *Kriegsanleihe 1914-1918*, *Vordruck Wohnviertel 1914-1918*; englisch *official form German home front 1914-1918*.

Der Beleg des Ereignisses nennt: Neun Kriegsanleihen zwischen 1914 und 1918

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_todesnachricht

1914-1918 · heimat · Wohnviertel

- `images/dokumente/heimat_todesnachricht_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_todesnachricht_2.png` — Option 2, **fehlt**

Suche: *Todesnachricht 1914-1918*, *Vordruck Wohnviertel 1914-1918*; englisch *official form German home front 1914-1918*.

Der Beleg des Ereignisses nennt: Gefallenenmeldung: Vordruck mit eingetragenem Namen

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_1915_brotkarte

1915 · heimat · Wohnviertel

- `images/dokumente/heimat_1915_brotkarte_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_1915_brotkarte_2.png` — Option 2, **fehlt**

Suche: *Brotkarte 1915*, *Lebensmittelkarte Wohnviertel 1915*; englisch *ration card German home front 1915*.

Der Beleg des Ereignisses nennt: Brotkarte in Berlin ab 22. Februar 1915

Wo suchen: Deutsches Historisches Museum (LeMO), Stadt- und Landesarchive

### heimat_unterstuetzung

1915-1916 · heimat · Gemeindeamt

- `images/dokumente/heimat_unterstuetzung_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_unterstuetzung_2.png` — Option 2, **fehlt**

Suche: *Unterstützung 1915-1916*, *Vordruck Gemeindeamt 1915-1916*; englisch *official form German home front 1915-1916*.

Der Beleg des Ereignisses nennt: Familienunterstützung für Angehörige Eingezogener

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_verfahren

1915-1919 · heimat · Amtsgericht

- `images/dokumente/heimat_verfahren_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_verfahren_2.png` — Option 2, **fehlt**

Suche: *Verfahren 1915-1919*, *Vordruck Amtsgericht 1915-1919*; englisch *official form German home front 1915-1919*.

Der Beleg des Ereignisses nennt: Verfahren wegen Verstoßes gegen die Höchstpreise

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_1916_ernaehrungsamt

1916 · heimat · Bezirksamt

- `images/dokumente/heimat_1916_ernaehrungsamt_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_1916_ernaehrungsamt_2.png` — Option 2, **fehlt**

Suche: *Ernährungsamt 1916*, *Vordruck Bezirksamt 1916*; englisch *official form German home front 1916*.

Der Beleg des Ereignisses nennt: Kriegsernährungsamt, errichtet im Mai 1916

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_1916_zensur

1916 · heimat · Wohnviertel

- `images/dokumente/heimat_1916_zensur_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_1916_zensur_2.png` — Option 2, **fehlt**

Suche: *Zensur 1916*, *Feldpostbrief Wohnviertel 1916*; englisch *field post letter German home front 1916*.

Der Beleg des Ereignisses nennt: Briefzensur und Stimmungsberichte der Überwachungsstellen

Wo suchen: Museum für Kommunikation / Europeana 1914-1918 (Privatbestände)

### einstieg_etappe

1914-1918 · front, etappe, heimat · Reservelazarett

- `images/dokumente/einstieg_etappe_1.png` — Option 1, **fehlt**
- `images/dokumente/einstieg_etappe_2.png` — Option 2, **fehlt**

Suche: *einstieg etappe 1914-1918*, *Vordruck Reservelazarett 1914-1918*; englisch *official form Western Front, trench 1914-1918*.

Der Beleg des Ereignisses nennt: Schwestern in Etappenlazaretten hinter der Front

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### front_1917_gerichtsherr

1917 · front · Etappe

- `images/dokumente/front_1917_gerichtsherr_1.png` — Option 1, **fehlt**
- `images/dokumente/front_1917_gerichtsherr_2.png` — Option 2, **fehlt**

Suche: *Gerichtsherr 1917*, *Vordruck Etappe 1917*; englisch *official form Western Front, trench 1917*.

Der Beleg des Ereignisses nennt: Kriegsgerichtsverfahren wegen Entfernung

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_1917_hilfsdienst

1917 · heimat · Rüstungsbetrieb

- `images/dokumente/heimat_1917_hilfsdienst_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_1917_hilfsdienst_2.png` — Option 2, **fehlt**

Suche: *Hilfsdienst 1917*, *Vordruck Rüstungsbetrieb 1917*; englisch *official form German home front 1917*.

Der Beleg des Ereignisses nennt: Hilfsdienstgesetz vom 5. Dezember 1916

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_1917_schulspeisung

1917 · heimat · Wohnviertel

- `images/dokumente/heimat_1917_schulspeisung_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_1917_schulspeisung_2.png` — Option 2, **fehlt**

Suche: *Schulspeisung 1917*, *Vordruck Wohnviertel 1917*; englisch *official form German home front 1917*.

Der Beleg des Ereignisses nennt: Schulspeisung und Kriegsküchen in den Städten

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_1917_unterseeboot

1917 · heimat · Wohnviertel

- `images/dokumente/heimat_1917_unterseeboot_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_1917_unterseeboot_2.png` — Option 2, **fehlt**

Suche: *Unterseeboot 1917*, *Zeitungsseite Wohnviertel 1917*; englisch *newspaper page German home front 1917*.

Der Beleg des Ereignisses nennt: Unbeschränkter U-Boot-Krieg ab 1. Februar 1917

Wo suchen: Zeitungsdigitalisate der Staatsbibliotheken, ZEFYS

### front_1918_befehl

1918 · front · Grabenstellung

- `images/dokumente/front_1918_befehl_1.png` — Option 1, **fehlt**
- `images/dokumente/front_1918_befehl_2.png` — Option 2, **fehlt**

Suche: *Befehl 1918*, *Vordruck Grabenstellung 1918*; englisch *official form Western Front, trench 1918*.

Der Beleg des Ereignisses nennt: Räumung von Stellungen im Herbst 1918

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_1918_grippe

1918 · heimat · Wohnviertel

- `images/dokumente/heimat_1918_grippe_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_1918_grippe_2.png` — Option 2, **fehlt**

Suche: *Grippe 1918*, *Lebensmittelkarte Wohnviertel 1918*; englisch *ration card German home front 1918*.

Der Beleg des Ereignisses nennt: Grippewelle im Herbst 1918

Wo suchen: Deutsches Historisches Museum (LeMO), Stadt- und Landesarchive

### heimat_1918_grippewelle

1918 · heimat · Wohnviertel

- `images/dokumente/heimat_1918_grippewelle_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_1918_grippewelle_2.png` — Option 2, **fehlt**

Suche: *Grippewelle 1918*, *Vordruck Wohnviertel 1918*; englisch *official form German home front 1918*.

Der Beleg des Ereignisses nennt: Behördliche Maßnahmen gegen die Grippe 1918

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### heimat_1918_bekanntmachung

1918 · heimat · Wohnviertel

- `images/dokumente/heimat_1918_bekanntmachung_1.png` — Option 1, **fehlt**
- `images/dokumente/heimat_1918_bekanntmachung_2.png` — Option 2, **fehlt**

Suche: *Bekanntmachung 1918*, *Vordruck Wohnviertel 1918*; englisch *official form German home front 1918*.

Der Beleg des Ereignisses nennt: Bekanntmachungen der Novembertage 1918

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### etappe_zensurstelle

1915-1918 · etappe · Zensurstelle

- `images/dokumente/etappe_zensurstelle_1.png` — Option 1, **fehlt**
- `images/dokumente/etappe_zensurstelle_2.png` — Option 2, **fehlt**

Suche: *Zensurstelle 1915-1918*, *Feldpostbrief Zensurstelle 1915-1918*; englisch *field post letter rear area, lines of communication 1915-1918*.

Der Beleg des Ereignisses nennt: Briefprüfstellen und die Überwachung der Feldpost

Wo suchen: Museum für Kommunikation / Europeana 1914-1918 (Privatbestände)

### etappe_brief_von_daheim

1915-1918 · etappe · Quartier

- `images/dokumente/etappe_brief_von_daheim_1.png` — Option 1, **fehlt**
- `images/dokumente/etappe_brief_von_daheim_2.png` — Option 2, **fehlt**

Suche: *Feldpostbrief 1915-1918*, *Feldpostbrief Quartier 1915-1918*; englisch *field post letter rear area, lines of communication 1915-1918*.

Der Beleg des Ereignisses nennt: Feldpost aus der Heimat an Etappenangehörige

Wo suchen: Museum für Kommunikation / Europeana 1914-1918 (Privatbestände)

### etappe_1916_verschleppt

1916-1917 · etappe · Sammelstelle

- `images/dokumente/etappe_1916_verschleppt_1.png` — Option 1, **fehlt**
- `images/dokumente/etappe_1916_verschleppt_2.png` — Option 2, **fehlt**

Suche: *Zwangsarbeit Deportation 1916-1917*, *Vordruck Sammelstelle 1916-1917*; englisch *official form rear area, lines of communication 1916-1917*.

Der Beleg des Ereignisses nennt: Zwangsarbeit im besetzten Belgien, Winter 1916/17

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### etappe_requisition

1914-1917 · etappe · Besetztes Dorf

- `images/dokumente/etappe_requisition_1.png` — Option 1, **fehlt**
- `images/dokumente/etappe_requisition_2.png` — Option 2, **fehlt**

Suche: *Requisition 1914-1917*, *Vordruck Besetztes Dorf 1914-1917*; englisch *official form rear area, lines of communication 1914-1917*.

Der Beleg des Ereignisses nennt: Requisitionen und Scheine im besetzten Gebiet

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### epilog_1919_versorgungsamt

1919 · front, etappe, heimat · Versorgungsamt

- `images/dokumente/epilog_1919_versorgungsamt_1.png` — Option 1, **fehlt**
- `images/dokumente/epilog_1919_versorgungsamt_2.png` — Option 2, **fehlt**

Suche: *Versorgungsamt 1919*, *Vordruck Versorgungsamt 1919*; englisch *official form Western Front, trench 1919*.

Der Beleg des Ereignisses nennt: Versorgungsamt und Rente der Kriegsbeschädigten

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

### epilog_1919_vertrag

1919 · front, etappe, heimat · Wohnviertel

- `images/dokumente/epilog_1919_vertrag_1.png` — Option 1, **fehlt**
- `images/dokumente/epilog_1919_vertrag_2.png` — Option 2, **fehlt**

Suche: *Vertrag 1919*, *Zeitungsseite Wohnviertel 1919*; englisch *newspaper page Western Front, trench 1919*.

Der Beleg des Ereignisses nennt: Die Bedingungen des Vertrags im Frühjahr 1919

Wo suchen: Zeitungsdigitalisate der Staatsbibliotheken, ZEFYS

### epilog_1919_papiere

1919 · front, etappe · Meldebehörde

- `images/dokumente/epilog_1919_papiere_1.png` — Option 1, **fehlt**
- `images/dokumente/epilog_1919_papiere_2.png` — Option 2, **fehlt**

Suche: *Papiere 1919*, *Vordruck Meldebehörde 1919*; englisch *official form Western Front, trench 1919*.

Der Beleg des Ereignisses nennt: Entlassungsschein, Meldepflicht und Nachweise

Wo suchen: Bundesarchiv, Landes- und Stadtarchive

---

## images/portraits — die Spielfigur

Das Bild in der Kopfleiste. Es wechselt mit der Stimmung; fehlt die Stimmungsfassung, greift `_neutral`, und fehlt auch die, das Bild ohne Zusatz. **Es genügt also, je Herkunft und Geschlecht ein einziges Bild abzulegen** — die Stimmungen sind eine Steigerung, keine Bedingung.

Ablagemaß (500, 500), Anzeigemaß (240, 240). 48 Dateien, davon 0 vorhanden.

### arbeiterschaft_m

- `images/portraits/arbeiterschaft_m.png` — **das Grundbild.** Ohne Stimmung, springt immer ein.
- `images/portraits/arbeiterschaft_m_angst.png` — Stimmung angst
- `images/portraits/arbeiterschaft_m_einsam.png` — Stimmung einsam
- `images/portraits/arbeiterschaft_m_erschoepft.png` — Stimmung erschoepft
- `images/portraits/arbeiterschaft_m_hungrig.png` — Stimmung hungrig
- `images/portraits/arbeiterschaft_m_neutral.png` — Stimmung neutral

Suche: *Porträt Mann arbeiterschaft 1914-1918*, *Atelierfotografie Mann*; englisch *portrait German man arbeiterschaft 1915*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### arbeiterschaft_w

- `images/portraits/arbeiterschaft_w.png` — **das Grundbild.** Ohne Stimmung, springt immer ein.
- `images/portraits/arbeiterschaft_w_angst.png` — Stimmung angst
- `images/portraits/arbeiterschaft_w_einsam.png` — Stimmung einsam
- `images/portraits/arbeiterschaft_w_erschoepft.png` — Stimmung erschoepft
- `images/portraits/arbeiterschaft_w_hungrig.png` — Stimmung hungrig
- `images/portraits/arbeiterschaft_w_neutral.png` — Stimmung neutral

Suche: *Porträt Frau arbeiterschaft 1914-1918*, *Atelierfotografie Frau*; englisch *portrait German woman arbeiterschaft 1915*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### buergertum_m

- `images/portraits/buergertum_m.png` — **das Grundbild.** Ohne Stimmung, springt immer ein.
- `images/portraits/buergertum_m_angst.png` — Stimmung angst
- `images/portraits/buergertum_m_einsam.png` — Stimmung einsam
- `images/portraits/buergertum_m_erschoepft.png` — Stimmung erschoepft
- `images/portraits/buergertum_m_hungrig.png` — Stimmung hungrig
- `images/portraits/buergertum_m_neutral.png` — Stimmung neutral

Suche: *Porträt Mann buergertum 1914-1918*, *Atelierfotografie Mann*; englisch *portrait German man buergertum 1915*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### buergertum_w

- `images/portraits/buergertum_w.png` — **das Grundbild.** Ohne Stimmung, springt immer ein.
- `images/portraits/buergertum_w_angst.png` — Stimmung angst
- `images/portraits/buergertum_w_einsam.png` — Stimmung einsam
- `images/portraits/buergertum_w_erschoepft.png` — Stimmung erschoepft
- `images/portraits/buergertum_w_hungrig.png` — Stimmung hungrig
- `images/portraits/buergertum_w_neutral.png` — Stimmung neutral

Suche: *Porträt Frau buergertum 1914-1918*, *Atelierfotografie Frau*; englisch *portrait German woman buergertum 1915*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### landbevoelkerung_m

- `images/portraits/landbevoelkerung_m.png` — **das Grundbild.** Ohne Stimmung, springt immer ein.
- `images/portraits/landbevoelkerung_m_angst.png` — Stimmung angst
- `images/portraits/landbevoelkerung_m_einsam.png` — Stimmung einsam
- `images/portraits/landbevoelkerung_m_erschoepft.png` — Stimmung erschoepft
- `images/portraits/landbevoelkerung_m_hungrig.png` — Stimmung hungrig
- `images/portraits/landbevoelkerung_m_neutral.png` — Stimmung neutral

Suche: *Porträt Mann landbevoelkerung 1914-1918*, *Atelierfotografie Mann*; englisch *portrait German man landbevoelkerung 1915*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### landbevoelkerung_w

- `images/portraits/landbevoelkerung_w.png` — **das Grundbild.** Ohne Stimmung, springt immer ein.
- `images/portraits/landbevoelkerung_w_angst.png` — Stimmung angst
- `images/portraits/landbevoelkerung_w_einsam.png` — Stimmung einsam
- `images/portraits/landbevoelkerung_w_erschoepft.png` — Stimmung erschoepft
- `images/portraits/landbevoelkerung_w_hungrig.png` — Stimmung hungrig
- `images/portraits/landbevoelkerung_w_neutral.png` — Stimmung neutral

Suche: *Porträt Frau landbevoelkerung 1914-1918*, *Atelierfotografie Frau*; englisch *portrait German woman landbevoelkerung 1915*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### adel_m

- `images/portraits/adel_m.png` — **das Grundbild.** Ohne Stimmung, springt immer ein.
- `images/portraits/adel_m_angst.png` — Stimmung angst
- `images/portraits/adel_m_einsam.png` — Stimmung einsam
- `images/portraits/adel_m_erschoepft.png` — Stimmung erschoepft
- `images/portraits/adel_m_hungrig.png` — Stimmung hungrig
- `images/portraits/adel_m_neutral.png` — Stimmung neutral

Suche: *Porträt Mann adel 1914-1918*, *Atelierfotografie Mann*; englisch *portrait German man adel 1915*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### adel_w

- `images/portraits/adel_w.png` — **das Grundbild.** Ohne Stimmung, springt immer ein.
- `images/portraits/adel_w_angst.png` — Stimmung angst
- `images/portraits/adel_w_einsam.png` — Stimmung einsam
- `images/portraits/adel_w_erschoepft.png` — Stimmung erschoepft
- `images/portraits/adel_w_hungrig.png` — Stimmung hungrig
- `images/portraits/adel_w_neutral.png` — Stimmung neutral

Suche: *Porträt Frau adel 1914-1918*, *Atelierfotografie Frau*; englisch *portrait German woman adel 1915*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

---

## images/figuren — die fünf Nebenfiguren

**Diese Bilder sucht das Spiel heute gar nicht ab.** `FIGUREN_ECHTE_BILDER` steht auf `False`; solange das so ist, greift überall `FIGUREN_PLATZHALTER`. Die Liste steht hier, damit sie vollständig ist, und ist von allen Abschnitten der am wenigsten dringliche.

75 Dateien: fünf Figuren mal drei Pfade mal 5 Stimmungen.

### naechste

- Pfad front: `images/figuren/naechste_front_angst.png` … (5 Stimmungen)
- Pfad etappe: `images/figuren/naechste_etappe_angst.png` … (5 Stimmungen)
- Pfad heimat: `images/figuren/naechste_heimat_angst.png` … (5 Stimmungen)

Suche: *Porträt naechste 1914-1918*, *Gruppenfoto Westfront, Schützengraben*; englisch *portrait Western Front, trench Germany 1916*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### kind

- Pfad front: `images/figuren/kind_front_angst.png` … (5 Stimmungen)
- Pfad etappe: `images/figuren/kind_etappe_angst.png` … (5 Stimmungen)
- Pfad heimat: `images/figuren/kind_heimat_angst.png` … (5 Stimmungen)

Suche: *Porträt kind 1914-1918*, *Gruppenfoto Westfront, Schützengraben*; englisch *portrait Western Front, trench Germany 1916*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### kundige

- Pfad front: `images/figuren/kundige_front_angst.png` … (5 Stimmungen)
- Pfad etappe: `images/figuren/kundige_etappe_angst.png` … (5 Stimmungen)
- Pfad heimat: `images/figuren/kundige_heimat_angst.png` … (5 Stimmungen)

Suche: *Porträt kundige 1914-1918*, *Gruppenfoto Westfront, Schützengraben*; englisch *portrait Western Front, trench Germany 1916*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### amtsperson

- Pfad front: `images/figuren/amtsperson_front_angst.png` … (5 Stimmungen)
- Pfad etappe: `images/figuren/amtsperson_etappe_angst.png` … (5 Stimmungen)
- Pfad heimat: `images/figuren/amtsperson_heimat_angst.png` … (5 Stimmungen)

Suche: *Porträt amtsperson 1914-1918*, *Gruppenfoto Westfront, Schützengraben*; englisch *portrait Western Front, trench Germany 1916*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

### gegenseite

- Pfad front: `images/figuren/gegenseite_front_angst.png` … (5 Stimmungen)
- Pfad etappe: `images/figuren/gegenseite_etappe_angst.png` … (5 Stimmungen)
- Pfad heimat: `images/figuren/gegenseite_heimat_angst.png` … (5 Stimmungen)

Suche: *Porträt gegenseite 1914-1918*, *Gruppenfoto Westfront, Schützengraben*; englisch *portrait Western Front, trench Germany 1916*.

Wo suchen: Europeana 1914-1918, Stadtarchive, Fotosammlungen

---

## images

- `images/platzhalter.png` — vorhanden
  - Ersatzbild fuer jede Nebenfigur - FIGUREN_PLATZHALTER, figur_bild() in dialoge.rpy

---

## audio

- `audio/musik_epilog.mp3` — **fehlt**
  - Musik epilog - Lautstaerke 0.30, wiederholt sich, zweite Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_epilog.ogg` — **fehlt**
  - Musik epilog - Lautstaerke 0.30, wiederholt sich, erste Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_hauptmenue.mp3` — **fehlt**
  - Musik hauptmenue - Lautstaerke 0.30, wiederholt sich, zweite Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_hauptmenue.ogg` — **fehlt**
  - Musik hauptmenue - Lautstaerke 0.30, wiederholt sich, erste Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_heimat.mp3` — **fehlt**
  - Musik heimat - Lautstaerke 0.25, wiederholt sich, zweite Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_heimat.ogg` — **fehlt**
  - Musik heimat - Lautstaerke 0.25, wiederholt sich, erste Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_jahreskarte.mp3` — **fehlt**
  - Musik jahreskarte - Lautstaerke 0.30, wiederholt sich, zweite Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_jahreskarte.ogg` — **fehlt**
  - Musik jahreskarte - Lautstaerke 0.30, wiederholt sich, erste Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_lebenslauf.mp3` — **fehlt**
  - Musik lebenslauf - Lautstaerke 0.30, wiederholt sich, zweite Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_lebenslauf.ogg` — **fehlt**
  - Musik lebenslauf - Lautstaerke 0.30, wiederholt sich, erste Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_moduswahl.mp3` — **fehlt**
  - Musik moduswahl - Lautstaerke 0.30, wiederholt sich, zweite Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_moduswahl.ogg` — **fehlt**
  - Musik moduswahl - Lautstaerke 0.30, wiederholt sich, erste Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_onboarding.mp3` — **fehlt**
  - Musik onboarding - Lautstaerke 0.30, wiederholt sich, zweite Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/musik_onboarding.ogg` — **fehlt**
  - Musik onboarding - Lautstaerke 0.30, wiederholt sich, erste Wahl in ton_waehlen(), STELLENMUSIK in ton.rpy
- `audio/ort_bahnhof.mp3` — **fehlt**
  - Umgebungsklang bahnhof - Halle und Bahnsteig: Hall, Dampf, Ansage in der Ferne - Lautstaerke 0.40, wiederholt sich, zweite Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_bahnhof.ogg` — **fehlt**
  - Umgebungsklang bahnhof - Halle und Bahnsteig: Hall, Dampf, Ansage in der Ferne - Lautstaerke 0.40, wiederholt sich, erste Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_fabrik.mp3` — **fehlt**
  - Umgebungsklang fabrik - Werkhalle: Maschinen, Riemen, Signalglocke - Lautstaerke 0.40, wiederholt sich, zweite Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_fabrik.ogg` — **fehlt**
  - Umgebungsklang fabrik - Werkhalle: Maschinen, Riemen, Signalglocke - Lautstaerke 0.40, wiederholt sich, erste Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_graben.mp3` — **fehlt**
  - Umgebungsklang graben - Vorderste Stellung: Wind über der Brustwehr, ferner Einschlag - Lautstaerke 0.35, wiederholt sich, zweite Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_graben.ogg` — **fehlt**
  - Umgebungsklang graben - Vorderste Stellung: Wind über der Brustwehr, ferner Einschlag - Lautstaerke 0.35, wiederholt sich, erste Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_land.mp3` — **fehlt**
  - Umgebungsklang land - Hof und Feldweg: Wind, Vögel, ein Tier - Lautstaerke 0.25, wiederholt sich, zweite Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_land.ogg` — **fehlt**
  - Umgebungsklang land - Hof und Feldweg: Wind, Vögel, ein Tier - Lautstaerke 0.25, wiederholt sich, erste Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_lazarett.mp3` — **fehlt**
  - Umgebungsklang lazarett - Saal mit vielen Betten: gedämpft, Schritte, entfernte Stimmen - Lautstaerke 0.25, wiederholt sich, zweite Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_lazarett.ogg` — **fehlt**
  - Umgebungsklang lazarett - Saal mit vielen Betten: gedämpft, Schritte, entfernte Stimmen - Lautstaerke 0.25, wiederholt sich, erste Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_nachschub.mp3` — **fehlt**
  - Umgebungsklang nachschub - Magazin, Depot, Güterbahnhof: Kisten, Karren, Pferde - Lautstaerke 0.35, wiederholt sich, zweite Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_nachschub.ogg` — **fehlt**
  - Umgebungsklang nachschub - Magazin, Depot, Güterbahnhof: Kisten, Karren, Pferde - Lautstaerke 0.35, wiederholt sich, erste Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_quartier.mp3` — **fehlt**
  - Umgebungsklang quartier - Unterkunft hinter der Linie: Stimmen, Holz, Schritte auf Lehm - Lautstaerke 0.30, wiederholt sich, zweite Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_quartier.ogg` — **fehlt**
  - Umgebungsklang quartier - Unterkunft hinter der Linie: Stimmen, Holz, Schritte auf Lehm - Lautstaerke 0.30, wiederholt sich, erste Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_schreibstube.mp3` — **fehlt**
  - Umgebungsklang schreibstube - Amts- und Schreibstube: Feder, Stempel, halblautes Diktat - Lautstaerke 0.25, wiederholt sich, zweite Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_schreibstube.ogg` — **fehlt**
  - Umgebungsklang schreibstube - Amts- und Schreibstube: Feder, Stempel, halblautes Diktat - Lautstaerke 0.25, wiederholt sich, erste Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_strasse.mp3` — **fehlt**
  - Umgebungsklang strasse - Stadt und Wohnviertel: Schritte, Karren, ferne Stimmen - Lautstaerke 0.30, wiederholt sich, zweite Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_strasse.ogg` — **fehlt**
  - Umgebungsklang strasse - Stadt und Wohnviertel: Schritte, Karren, ferne Stimmen - Lautstaerke 0.30, wiederholt sich, erste Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_versammlung.mp3` — **fehlt**
  - Umgebungsklang versammlung - Viele Menschen in einem Raum: Stimmengewirr, Stühle, Gläser - Lautstaerke 0.35, wiederholt sich, zweite Wahl in ton_waehlen(), ORTSKLANG in ton.rpy
- `audio/ort_versammlung.ogg` — **fehlt**
  - Umgebungsklang versammlung - Viele Menschen in einem Raum: Stimmengewirr, Stühle, Gläser - Lautstaerke 0.35, wiederholt sich, erste Wahl in ton_waehlen(), ORTSKLANG in ton.rpy

---

## Vorhanden, aber unbenutzt

Diese Dateien liegen im Projekt, und keine Stelle im Code fragt nach ihnen. Sie sind nicht falsch — sie warten nur auf ihren Ort.

### `audio/stummer_morgen.mp3`

**Bleibt liegen, und das ist entschieden, kein Versäumnis.** Das Tongerüst steht seit Paket 8, Schritt 2.6: `ton_spielen()`, die Tafel `ORTSKLANG` für zehn Klangräume und `STELLENMUSIK` für sieben Stellen im Ablauf. Diese Datei bekommt dort keine Zeile.

Ihr ID3-Kopf sieht nach Inhalt aus — Titel „Stummer Morgen“, ein Interpret, der Vermerk „made with suno“, ein eingebettetes Titelbild, vier Minuten drei Sekunden. Sie ist trotzdem keiner: **Der Projektleiter hat am 6. September gesagt, es sei eine Probedatei.** Eine Tafelzeile darf eine Datei anfordern, die noch fehlt; sie darf eine vorhandene nicht vereinnahmen.

Wer sie doch einbauen will, braucht zwei Handgriffe: die Dateikennung in einer Zeile von `STELLENMUSIK` (ton.rpy) eintragen und `MUSIK_EINGESCHALTET` auf `True` setzen. **Nicht** in `ORTSKLANG` — für einen Umgebungsklang ist sie zu lang und zu gesetzt, und an der Front und in der Etappe wäre sie als Musik ohnehin gesperrt (Regel 3).

### `images/karten/front_beginn_1.png`

**Bleibt vorerst liegen, und das ist eine Entscheidung, kein Versäumnis.** Ein Ereignis `front_beginn` gibt es im Bestand nicht, und das Motiv passt auch nicht dazu: eine leere Kopfsteinstraße mit Fachwerk in der Dämmerung, also eine Heimatszene. Es stammt erkennbar aus einem frühen Entwurf.

Zuordnen ließe es sich — `heimat_sonntag` spielt in einer stillen Straße und passt gut. Dagegen spricht das Aussehen des Ganzen: **Ein einzelnes bebildertes Ereignis unter hundert unbebilderten sieht schlechter aus als hundert gleich behandelte Leerstellen.** Die Leerstelle ist seit Paket 8 ruhig und einheitlich; ein einzelnes Bild dazwischen bricht diese Ruhe auf und lässt alles andere wie einen Fehler wirken. Konsistenz schlägt hier Einzelqualität.

Sinnvoll wird das erste Bild, sobald ein **ganzer Zusammenhang** bebildert ist: ein Jahr, ein Pfad oder alle Karten eines Typs.

### `images/karten/front_beginn_2.png`

Dasselbe wie bei `front_beginn_1.png`. Das Motiv — ein Schreibtisch mit Petroleumlampe, Federkiel, Taschenuhr und einem gefalteten Brief mit Stempel — passt inhaltlich am besten zu `etappe_innendienst` ("Du gehst mir eine Woche in die Schreibstube"), nicht zu einem Frontereignis.


---

## Wenn eine Datei abgelegt ist

Nichts weiter tun. Der Code sucht bei jedem Start neu; eine Datei am richtigen Pfad wird ohne Zutun benutzt, und der Platzhalter verschwindet. Zur Kontrolle:

```
python medienbedarf.py      diese Datei neu schreiben
python probe_alles.py       Probe 6 zählt mit
```


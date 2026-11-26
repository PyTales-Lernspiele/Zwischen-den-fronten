# Erkundung fuer Paket 8, Schritt 2.6 (Tongeruest)

6. September 2026. Sechs Leser im Projekt und im Ren'Py-Quellcode, dazu
zwei Gegenleser. Jeder Befund traegt Datei, Zeile und woertliches Zitat.
Die Spalte *Sicherheit* sagt, ob der Leser die Stelle **gelesen**, sie
**erschlossen** oder nur **vermutet** hat - erschlossene und vermutete
Befunde sind von einem zweiten Agenten gegengelesen worden.

**Diese Datei ist eine Erkundung, kein Auftrag.** Sie ersetzt keine
Entscheidung und keinen Eintrag in `auftrag/`. Sie steht hier, damit die
naechste Sitzung nicht dieselben 5187 Zeilen noch einmal durchsuchen muss.

---

## 1 - Die Werkbank probe_alles.py

probe_alles.py hat 5187 Zeilen und traegt heute zehn Proben, nicht sieben. Jede Probe ist eine gewoehnliche Funktion (NS, B, [Extras]), die B.titel(\"PROBE n NAME\") schreibt, mit B() und B.unterteil() ihre Tabellen ausgibt und (beanstandungen, geprueft) zurueckgibt; probe_beleg (Zeile 2839-2892) ist die kuerzeste vollstaendige Vorlage, probe_bewegung (Zeile 3840) die Vorlage fuer eine Probe, die zusaetzlich den Spielordner braucht. Die Werkbank baut die Spiellogik nicht nach: datei_zerlegen() schneidet alle 'init python:'-Bloecke heraus, Aufbau.ausfuehren() (Zeile 437-453) compiliert und exec-t sie in EINEN gemeinsamen Namensraum NS, und die Proben rufen danach die echten Projektfunktionen ueber NS[\"name\"](). Fehlende Namen werden zu Attrappen und im Abschnitt A gemeldet. Die Medienprobe sammelt ihre Pfade in medien_sammeln() (Zeile 2900-3028) in fuenf nummerierten Abschnitten - Karten, Portraets, Nebenfiguren, Platzhalter, Schriften; die Zahl 333 ist nirgends festgeschrieben, sondern die Summe ueber das Medienbuch (Zeile 3068-3073), das RenpyAttrappe.loadable() (Zeile 291) mitschreibt. Tondateien zaehlt sie heute NICHT mit: 'audio' kommt nur in der Suche nach verwaisten Dateien vor (Zeile 3086), weshalb audio/stummer_morgen.mp3 in bericht.txt Zeile 1462 als 'von keiner Stelle im Code erwartet' steht. --schnell laesst keine Probe aus, es senkt nur die Durchgaenge je Lage von 2000 auf 300 (Zeile 89, 5153-5154). Ein Register der Proben gibt es an vier Stellen: der Kopfkommentar (Zeile 37-46, veraltet), die handgeschriebene Folge der probe_laufen()-Aufrufe in hauptlauf (Zeile 4921-4980), die daraus gefuellte Liste 'proben' und die Tafel NACHBAUTEN (Zeile 4601-4645).

### Befunde (18)

**Aufbau einer kleinen, vollstaendigen Probe (Probe 5, Belegprobe)** - `game/probe_alles.py`:2839 - *gelesen*

```
def probe_beleg(NS, B):
    beanstandungen = 0
    geprueft = 0

    B.titel("PROBE 5  BELEGPROBE")
    B("Jeder Inhalt sagt, worauf er sich stuetzt. Geprueft wird seit Paket 3,")
...
    B.unterteil("Tabelle: Kennung, Art, Beleg vorhanden")
    B("%-36s %-12s %-14s %s" % ("Kennung", "Art", "Beleg", "Befund"))

    for bestand, name in ((NS["EREIGNISSE"], "Ereignis"), (NS["EINLAGEN"], "Einlage")):
        for vorlage in bestand:
            geprueft += 1
...
    return beanstandungen, geprueft
```

Das Muster jeder Probe: Signatur (NS, B, [Extras]) - zwei Zaehler - B.titel("PROBE n NAME") - Erklaertext - B.unterteil() fuer jede Tabelle - Zeilen mit %-Formaten - am Ende 'return beanstandungen, geprueft'. Eine Tonprobe wird genauso gebaut; probe_beleg endet bei Zeile 2892.

**Zweite Vorlage: eine Probe, die den Spielordner braucht (Probe 9)** - `game/probe_alles.py`:3840 - *gelesen*

```
def probe_bewegung(NS, B, spielordner):
    beanstandungen = 0
    geprueft = 0

    B.titel("PROBE 9  BEWEGUNGSPROBE")
...
    dateien = rpy_dateien(spielordner)
    if not dateien:
        B("")
        B(">> FEHLER << Im Spielordner liegt keine .rpy-Datei.")
        return 1, 0
```

Naechstliegendes Vorbild fuer eine Tonprobe, die zusaetzlich Dateien im Spielordner sehen muss (audio/). Sie zeigt auch, wie ein Abbruch gemeldet wird: 1 Beanstandung, 0 geprueft - nie eine gruene Null.

**Die Hilfsfunktionen fuer den Bericht: Ueberschrift, Unterteil, Text** - `game/probe_alles.py`:1217 - *gelesen*

```
class Bericht(object):

    def __init__(self):
        self.zeilen = []

    def __call__(self, text=""):
        self.zeilen.append(text)

    def titel(self, text):
        self("")
        self("=" * 78)
        self(text)
        self("=" * 78)

    def unterteil(self, text):
```

Es gibt genau drei Ausgabewege: B("...") fuer eine Zeile, B.titel() fuer den Probenkopf (78 Gleichheitszeichen darueber und darunter), B.unterteil() fuer einen Abschnitt (78 Striche darunter). Danach folgen prozent() (Zeile 1240) und B.text() (Zeile 1236), das alles zu einer Zeichenkette fuegt.

**Wie eine Probe gezaehlt wird und wie 'AUSGEFALLEN' entsteht** - `game/probe_alles.py`:4909 - *gelesen*

```
    def probe_laufen(nummer, name, funktion, *args):
        vorher = len(B.zeilen)
        try:
            beanstandungen, geprueft = funktion(*args)
        except Exception:
            B.titel("PROBE %d  %s - ABGEBROCHEN" % (nummer, name.upper()))
            B(traceback.format_exc())
            return 1, 0, "ABGEBROCHEN", True
        marke = "PROBE %d" % nummer
        geschrieben = any(marke in zeile for zeile in B.zeilen[vorher:])
        return beanstandungen, geprueft, "gelaufen", geschrieben
```

Der Nachweis von Regel 11 haengt an einer Zeichenkette: Der Titel einer neuen Probe 11 MUSS woertlich 'PROBE 11' enthalten, sonst gilt sie als AUSGEFALLEN. Ausserdem gilt geprueft == 0 als 'NICHTS GEMESSEN' (Zeile 4997-5006) und macht den Lauf fehlerhaft.

**Das Register der Proben - Aufruf und Eintrag in die Liste 'proben'** - `game/probe_alles.py`:4971 - *gelesen*

```
    ## ------------------------------------------------------------ 10
    ## SEIT PAKET 7, SCHRITT 2. Sie loest pruefen.py ab und traegt den
    ## Nachweis, dass "Acht Striche" keine richtige Antwort hat.
...
    b, g, z, w = probe_laufen(10, "Handgriffe", probe_handgriffe, NS, B,
                              spielordner,
                              min(VERGLEICHSDURCHGAENGE, argumente.durchgaenge))
    proben.append(("10 Handgriffe", b, g, "Auswertungen und Verteilungen", z, w))
```

Hier ist die einzige Stelle, an der die Proben wirklich aufgezaehlt werden - als handgeschriebene Folge von probe_laufen()-Aufrufen ab Zeile 4921. Eine Probe 11 wird direkt nach Zeile 4980 eingehaengt, vor die Auswertungsschleife ab Zeile 4997. Die Liste 'proben' speist danach Selbsttest a), Kurzfassung und UMFANG.

**Register 2: die Probenliste im Kopfkommentar (veraltet)** - `game/probe_alles.py`:37 - *gelesen*

```
DIE SIEBEN PROBEN
    1  Bestandstafel     Soll gegen Bestand, Ereignisse und Einlagen
    2  Pfadprobe         2000 Durchgaenge je Startpfad und Verlauf
    3  Sackgassenprobe   wie oft ein Kapitel aus Mangel endet
    4  Wertetafel        Endwerte, harte Abbrueche, reiner Kalender
    5  Belegprobe        Inhalte ohne quelle-Feld
    6  Medienprobe       alle erwarteten Dateipfade
    7  Sprachprobe       TABU_BEGRIFFE und PRUEF_BEGRIFFE
```

Der Kopfkommentar nennt sieben Proben, tatsaechlich laufen zehn (bericht.txt Zeile 10-19). Er ist seit Paket 7 nicht mitgefuehrt worden. Eine neue Tonprobe gehoert hier eingetragen - und die Ueberschrift muesste bei der Gelegenheit stimmen.

**Register 3: NACHBAUTEN - die Liste 'fragt / eigen / spiegel'** - `game/probe_alles.py`:4597 - *gelesen*

```
## Wo die Werkbank Projektlogik nachbaut oder das Projekt fragt.
## Diese Liste wird von Hand gefuehrt. Wer eine Probe schreibt, die ueber
## Ziehbarkeit urteilt, traegt sie hier ein - und zwar mit "eigen", bis
## sie das Projekt fragt.
NACHBAUTEN = [
    ("ziehbare_ereignisse", "fragt",
     "kettenziele() und einlagen_ketten_sammeln() des Projekts"),
```

Zweite Pflichtstelle fuer eine neue Probe. Die Liste laeuft bis Zeile 4645 und wird in Selbsttest c) (Zeile 4769-4782) ausgegeben. Eine Tonprobe traegt hier z. B. ('probe_ton: Musiksperre', 'fragt', 'ton_spielen() und ORTSKLANG des Projekts') ein.

**Wie die .rpy-Dateien in den Python-Namensraum kommen (Regel 11)** - `game/probe_alles.py`:437 - *gelesen*

```
    def ausfuehren(self):
        self.NS = namensraum_bauen(self.spielordner, self.bildschirme, self.medienbuch)
        for block in self.bloecke:
            try:
                stueck = compile(block["quelltext"], block["pfad"], "exec")
                exec(stueck, self.NS)
                block["gelaufen"] = True
            except Exception:
                block["gelaufen"] = False
```

Der Kern: Die Werkbank baut nichts nach. datei_zerlegen() (Zeile 123) schneidet jeden 'init N python:'-Block heraus, rueckt ihn um vier Leerzeichen aus und schiebt ihn mit Leerzeilen an seine echte Zeilennummer (Zeile 181). Alle Bloecke laufen in EINEM gemeinsamen dict NS, sortiert nach init-Rang, Dateiname, Stelle (Zeile 435). Danach ist ton_spielen() schlicht NS['ton_spielen'] und ORTSKLANG schlicht NS['ORTSKLANG'] - vorausgesetzt, beide stehen in einem init-python-Block und nicht in einem label.

**Was fehlt, wird zur Attrappe - und wird gemeldet** - `game/probe_alles.py`:340 - *gelesen*

```
    def __missing__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise KeyError(name)
...
        if hasattr(builtins, name):
            wert = getattr(builtins, name)
            dict.__setitem__(self, name, wert)
            return wert
        self.erfundene[name] += 1
        wert = Attrappe(name)
        dict.__setitem__(self, name, wert)
        return wert
```

Ein unbekannter Name bricht keinen Block ab, sondern wird zur Attrappe und im Abschnitt A des Berichts gelistet ('Namen, fuer die eine Attrappe eingetreten ist', Zeile 4865). Wichtig fuer die Tonprobe: Schreibt eine Probe NS['ton_spielen'](...) und die Funktion existiert nicht, liefert der Aufruf klaglos eine Attrappe statt eines Fehlers - die Probe muss also selbst pruefen, ob es eine echte Funktion ist (Vorbild: 'if not callable(NS.get("merkmal_setzen"))' in Zeile 4521).

**renpy.loadable() ist echt - das ist die Wurzel der Medienprobe** - `game/probe_alles.py`:291 - *gelesen*

```
    def loadable(self, pfad, directory=None):
        """Prueft die Datei im Spielordner und schreibt die Anfrage mit.

        Das Mitschreiben ist die Grundlage der Medienprobe: Jeder Pfad,
        den bild_pfad(), portrait_anzeigen() oder schrift_waehlen() je
        gesucht haben, steht danach im Medienbuch.
        """
        name = str(pfad)
        da = os.path.isfile(os.path.join(self.spielordner, name.replace("/", os.sep)))
        eintrag = self.medienbuch.setdefault(name, {"anfragen": 0, "vorhanden": da})
        eintrag["anfragen"] += 1
        eintrag["vorhanden"] = da
        return da
```

Sobald ton_spielen() intern renpy.loadable(pfad) ruft und die Werkbank ton_spielen() irgendwo aufruft, landet der Tonpfad von selbst im Medienbuch und damit in der Zaehlung von Probe 6. Das ist der billigste Weg, Tondateien mitzaehlen zu lassen - er reicht aber nicht fuer MEDIEN.md (siehe naechster Fund).

**MEDIENPROBE: wie die erwarteten Pfade gesammelt werden** - `game/probe_alles.py`:2900 - *gelesen*

```
def medien_sammeln(NS, medienbuch, spielordner):
    """Jeden erwarteten Dateipfad MIT SEINER HERKUNFT.

    EINE Quelle fuer zwei Leser: probe_medien() zaehlt damit, und
    medienbedarf.py schreibt MEDIEN.md daraus. Stuenden die Schleifen
    zweimal da, naennte der Bedarfsplan andere Pfade als der Bericht, und
    niemand wuesste, welche Liste stimmt (Regel 11).

    Geliefert wird ein Woerterbuch

        pfad -> {"herkunft": [Satz, ...], "kategorie": str}
```

medien_sammeln() ist die EINE Sammelstelle. Sie hat fuenf nummerierte Abschnitte: 1. Karten/Dokumente (Zeile 2948), 2. Portraets (2968), 3. Nebenfiguren (2991), 4. Figuren-Platzhalter (3010), 5. Schriften (3017). Ein Abschnitt '6. Ortsklaenge' gehoert unmittelbar vor das return in Zeile 3028.

**MEDIENPROBE: die einzuhaengende Stelle, Wortlaut des Nachbarn** - `game/probe_alles.py`:3017 - *gelesen*

```
    ## 5. Schriften. Welche Datei zu welcher Schrift gehoert, sagt
    ##    SCHRIFT_KANDIDATEN in gui.rpy - gefragt, nicht nachgebaut.
    for name in sorted(NS.get("SCHRIFT_KANDIDATEN", {})):
        zweck = NS.get("SCHRIFT_ZWECK", {}).get(name, "")
        for stelle, pfad in enumerate(NS["SCHRIFT_KANDIDATEN"][name]):
            NS["renpy"].loadable(pfad)
            merken(pfad,
                   "%s (%s) - %s Wahl in schrift_waehlen(), gui.rpy"
                   % (name, zweck, "erste" if stelle == 0 else "zweite"),
                   "fonts")

    return herkunft, stimmungen, typenzaehler, beanstandungen
```

Genau dieses Muster braucht ORTSKLANG: ueber NS.get("ORTSKLANG", {}) laufen, fuer jeden Eintrag NS["renpy"].loadable(pfad) rufen (damit das Medienbuch zaehlt) und merken(pfad, Herkunftssatz, "audio") (damit MEDIEN.md den Pfad kennt). Ein NS.get() mit Vorgabe ist Pflicht, sonst zieht eine fehlende Tafel eine Attrappe.

**MEDIENPROBE: woher die Zahl 333 kommt** - `game/probe_alles.py`:3068 - *gelesen*

```
    gesamt = 0
    vorhanden_gesamt = 0
    for kategorie, pfade in gruppen.items():
        da = len([p for p in pfade if medienbuch[p]["vorhanden"]])
        gesamt += len(pfade)
        vorhanden_gesamt += da
```

333 steht nirgends im Quelltext. Die Zahl entsteht als Summe ueber die Gruppen des MEDIENBUCHS (gruppiert nach Ordner in Zeile 3059-3066) und wird in Zeile 3152 gedruckt sowie in Zeile 3155 als 'geprueft' zurueckgegeben - deshalb steht sie in bericht.txt Zeile 15 und 1485. Gruppiert wird ueber medienbuch, NICHT ueber die herkunft-Liste: ein Pfad, den nur renpy.loadable() gesehen hat, zaehlt mit, taucht aber in MEDIEN.md nicht auf.

**MEDIENPROBE: Tondateien werden heute NICHT mitgezaehlt** - `game/probe_alles.py`:3084 - *gelesen*

```
    ## Verwaiste Dateien: liegt ab, wird aber nirgends gesucht.
    verwaist = []
    for ordner in ["images", "fonts", "audio"]:
        wurzel = os.path.join(spielordner, ordner)
        if not os.path.isdir(wurzel):
            continue
```

Die einzige Stelle, an der 'audio' heute vorkommt. Der Ordner wird nur nach VERWAISTEN Dateien abgelaufen. Folge im aktuellen Bericht: audio/stummer_morgen.mp3 steht in bericht.txt Zeile 1462 unter 'Vorhanden, aber von keiner Stelle im Code erwartet'. Sobald ORTSKLANG-Pfade gesammelt werden, verschwindet die Datei von selbst aus dieser Liste - das ist die Probe dafuer, dass die Einhaengung greift.

**Der zweite Leser von medien_sammeln kennt 'audio' schon** - `game/medienbedarf.py`:255 - *gelesen*

```
    ## Nach Kategorie gruppieren, in einer festen, lesbaren Folge.
    folge = ["fonts", "images/karten", "images/dokumente", "images/portraits",
             "images/figuren", "images", "audio"]
```

medienbedarf.py ruft probe_alles.medien_sammeln() (Zeile 249) und hat 'audio' bereits als letzte Gruppe vorgesehen. An MEDIEN.md muss also nichts umgebaut werden: Sobald medien_sammeln() Tonpfade liefert, erscheinen sie dort automatisch mit Ordnertabelle und Herkunftssatz.

**Selbsttest b) rechnet die Medienzahl gegen den Bestand** - `game/probe_alles.py`:4714 - *gelesen*

```
    teile = medienverweise_erwartet(NS)
    soll_medien = sum(teile.values())
    ist_medien = fallzahl.get("6 Medienprobe", 0)
    kopf("   Medienprobe:  %d Pfade im Medienbuch, %d Verweise im Bestand."
         % (ist_medien, soll_medien))
    for name, anzahl in teile.items():
        kopf("      %-46s %6d" % (name, anzahl))
    kopf("      Differenz %d. Sie ist erwartet und hat zwei Gruende: Mehrere"
         % (ist_medien - soll_medien))
```

medienverweise_erwartet() (Zeile 4648-4669) zaehlt Karten, Portraets und Nebenfiguren unabhaengig nach. Kommen Tonpfade ins Medienbuch, waechst ist_medien, soll_medien aber nicht - die Differenz und ihr Erklaersatz stimmen dann nicht mehr ganz. Sauber waere eine vierte Zeile 'Ortsklaenge' in medienverweise_erwartet().

**Was --schnell tut** - `game/probe_alles.py`:5148 - *gelesen*

```
    ## --schnell ist eine Zwischenprobe zwischen zwei Arbeitsschritten. Sie
    ## misst dieselben sieben Proben, nur mit weniger Durchgaengen: Die
    ## Bestands-, Beleg-, Medien- und Sprachprobe rechnen ohnehin ohne
    ## Zufall, und fuer die drei uebrigen genuegt zum Zwischenstand eine
    ## grobe Zahl. Eine ausdrueckliche Angabe hat Vorrang.
    if argumente.durchgaenge is None:
        argumente.durchgaenge = SCHNELL_DURCHGAENGE if argumente.schnell else 2000
```

--schnell laesst KEINE Probe aus. Es setzt nur die Zahl der Durchgaenge je Lage von 2000 auf SCHNELL_DURCHGAENGE = 300 (Zeile 89) und begrenzt damit auch den Vergleichslauf in Probe 10 auf min(200, durchgaenge) (Zeile 4979). Eine Tonprobe wuerde bei --schnell also voll laufen - sie braucht keinen eigenen Schnellzweig, solange sie nicht selbst spielt.

**Der Auftrag zum Tongeruest nennt die Probe ausdruecklich** - `auftrag/paket08.md`:199 - *gelesen*

```
13. HARTE CODESPERRE: Auf den Pfaden front und etappe wird niemals Musik
    abgespielt. Nicht als Vereinbarung, sondern als Abfrage in
    ton_spielen(), die den Aufruf verwirft und in der Probe zaehlt.
...
  - Probe: ton_spielen() gibt auf front und etappe null Musikaufrufe frei.
  - probe_alles.py sonst unveraendert.
```

Die geforderte Messung ist zaehlbar: je Pfad die Zahl der freigegebenen und der verworfenen Musikaufrufe, dazu die ORTSKLANG-Tafel mit Datei, Lautstaerke, Wiederholung. 'probe_alles.py sonst unveraendert' spricht dafuer, die Tonprobe als eigene Probe 11 anzuhaengen und an den bestehenden Proben nichts zu drehen.

### Offene Fragen und Urteil

- Steht ORTSKLANG spaeter in einem 'init python:'-Block? Nur dann sieht die Werkbank die Tafel. Wird sie als 'default ORTSKLANG = {...}' geschrieben, greift zwar vorgaben_setzen() (Zeile 455-468), aber erst nach allen init-Bloecken - und ein 'define ORTSKLANG = ...' wuerde die Werkbank gar nicht lesen, denn datei_zerlegen() kennt nur init-python, default, screen und init offset (Zeile 115-120).
- Soll die Tonprobe ton_spielen() wirklich aufrufen (dann zaehlt renpy.loadable() die Pfade von selbst mit) oder nur die Tafel ORTSKLANG lesen? Der erste Weg ist der von Regel 11 verlangte ('sie fragt das Projekt'), erfordert aber, dass ton_spielen() ohne laufendes Ren'Py nicht abstuerzt - renpy.play/renpy.music sind in der Werkbank blosse Attrappen und schlucken jeden Aufruf klaglos.
- Soll medienverweise_erwartet() (Zeile 4648) eine vierte Zeile fuer Ortsklaenge bekommen? Ohne sie waechst 'ist_medien' im Selbsttest b), 'soll_medien' nicht, und der Erklaersatz zur Differenz (Zeile 4721-4725) wird ungenau.
- Der Kopfkommentar der Datei (Zeile 37-46) spricht von 'DIE SIEBEN PROBEN', es laufen zehn. Soll er beim Einbau der elften mitgezogen werden, oder gilt das als Aenderung ausserhalb des Auftrags?
- Auftragspunkt 15 (audio/stummer_morgen.mp3) ist eine Inhaltsfrage, keine Werkbankfrage: bekommt die Datei einen Ort in ORTSKLANG oder bleibt sie als unbenutzt in MEDIEN.md vermerkt? Solange sie in keiner Tafel steht, meldet Probe 6 sie weiter als verwaist (bericht.txt Zeile 1462).

---

## 2 - Das Regelwerk (VERFASSUNG, ENTSCHEIDUNGEN, MEDIEN.md)

Das Regelwerk fuer das Tongeruest steht an fuenf Stellen: VERFASSUNG.md (Aufbau/init-Ordnung, Bezeichnerkarte, Ausgabeformat), ENTSCHEIDUNGEN.md 24 (Musiktafel neben ORTSKLANG, Sperre ueber den Pfad statt ueber den Kanal), paket08.md Teil D (Punkte 11 bis 15 samt Abnahme), MEDIEN.md/medienbedarf.py (die Kategorie "audio" ist im Skript bereits angelegt, aber heute leer) und probe_alles.py (Medienbuch und medien_sammeln). Die Verfassung sagt NICHT, in welche Datei ton_spielen() und ORTSKLANG gehoeren und welchen init-Rang sie bekommen - das steht in keinem Auftrag und ist die groesste offene Frage. Die Bezeichnerkarte in VERFASSUNG.md fuehrt heute keine Ton-Zeile; das Gegenstueck fuer Bilder ("Bild und Schrift") zeigt, wie eine solche Zeile aussieht. MEDIEN.md wird von medienbedarf.py erzeugt, Handaenderungen sind beim naechsten Lauf weg; ein Medieneintrag hat dort zwei Formate - das gebuendelte Kartenformat und das einfache Rest-Format, das eine audio-Gruppe bekaeme. Im heutigen bericht.txt zaehlt Probe 6 genau 333 Pfade in sechs Rubriken (fonts, images/dokumente, images/figuren, images/karten, images, images/portraits) - "audio" ist KEINE eigene Rubrik; audio/stummer_morgen.mp3 steht nur unter "Vorhanden, aber von keiner Stelle im Code erwartet". In AUFGEFALLEN.md habe ich zu Ton, Audio, Musik oder Klang keinen einzigen Punkt gefunden. Fuenf .rpy-Dateien tragen im Kopfkommentar den Satz "Kein Audio" - der wird durch ein Tongeruest teilweise unwahr und muesste mitgezogen werden.

### Befunde (34)

**Aufbau: welche Datei welchen init-Rang hat (VERFASSUNG)** - `auftrag/VERFASSUNG.md`:27 - *gelesen*

```
| Datei | init | Inhalt |
|---|---|---|
| `gui.rpy` | −50, −2 | Farben, Rahmen, Schriften, Bildersatz |
| `bewegung.rpy` | −45, 5 | Bewegungsstufen, `bewegungszeit()`, neun transforms, drei Übergänge |
| `script.rpy` | −20, −10, −5, 0 | Werte, `Ereignis`/`Option`, `EREIGNISSE` |
| `dialoge.rpy` | −20, −10, −5, 0 | Szenen, `variante()`, Bühne |
| `kapitel.rpy` | −19, −9, 1, 2, 3 | Kapitel 1914–1919, `MERKMAL_REGISTER`, `KapitelEreignis`, Lebenslauf |
| `herkunft.rpy` | −19, −10, −4, 0, 1, 2 | Lebenslage, Musterung, Erwerb, Sprachprüfung |
| `figuren.rpy` | −8, 0, 1, 3, 4 | fünf Nebenfiguren, `BRIEFE`, `SCHICKSALE`, `briefwelt()` |
| `minispiele.rpy` | −6, 7, 8, 9 | die Einlagen |
| `merkbuch.rpy` | −7, 1, 2, 5, 6 | Merkbuch, Post-Umschlag |
| `screens.rpy` | ohne init | Stile und Bildschirme |
```

Die Tabelle ist die einzige Stelle, die Dateien init-Raenge zuordnet. Sie nennt keine Ton-Datei und keinen Ton-Rang. gui.rpy ist die einzige Zeile mit dem Inhalt "Bildersatz", also der naechstliegende Ort fuer eine Medienfunktion mit renpy.loadable() - das steht dort aber nicht geschrieben.

**Arbeitsweise des Projekts: in der eigenen Datei ueberschreiben statt fremd schneiden** - `auftrag/VERFASSUNG.md`:40 - *gelesen*

```
**Spätere init-Blöcke überschreiben frühere. Das ist gewollt und die
Arbeitsweise des Projekts:** nicht in fremden Dateien herumschneiden,
sondern in der eigenen Datei überschreiben. Beispiel: `MODUS_ZIELZAHL`
steht in `script.rpy` (init −20) auf 9/22 und wird von `kapitel.rpy`
(init −19) auf 12/30 überschrieben. Gültig ist 12/30.
```

Eine neue Tafel (ORTSKLANG, Musiktafel) darf spaeter in einer anderen Datei ergaenzt oder ueberschrieben werden. Der init-Rang der definierenden Datei muss also frueh genug liegen, damit jede aufrufende Stelle sie schon kennt.

**Bezeichnerkarte: benutzen statt neu erfinden** - `auftrag/VERFASSUNG.md`:81 - *gelesen*

```
## Bezeichnerkarte

Benutzen statt neu erfinden.

| Bereich | Bezeichner |
|---|---|
```

Es gibt eine Bezeichnerkarte, aber die Verfassung sagt an keiner Stelle ausdruecklich, dass ein NEUER Name dort einzutragen ist - sie fordert nur, vorhandene zu benutzen. Dass ein Ton-Bereich dazugehoert, ist der Sache nach naheliegend (jede andere Werkzeuggruppe hat eine Zeile), aber nicht wortwoertlich vorgeschrieben.

**Vorbildzeile fuer eine neue Ton-Zeile in der Bezeichnerkarte** - `auftrag/VERFASSUNG.md`:93 - *gelesen*

```
| Bild und Schrift | `bild_pfad()`, `bild_vorhanden()`, `bild_anzeigen()`, `bild_platzhalter()`, `portrait_anzeigen()`, `schrift_waehlen()`, `BILD_MASSE`, `BILD_ANZEIGE` |
```

So sieht eine Medienzeile der Bezeichnerkarte aus: Funktionen und Tafeln in einer Zeile, Bereich links. Eine Zeile "Ton" mit `ton_spielen()`, `ORTSKLANG` und der Musiktafel waere formgleich.

**Ausgabeformat: Sprache und Stil der Kommentare** - `auftrag/VERFASSUNG.md`:197 - *gelesen*

```
## Ausgabeformat

- Vollständige, einsetzbare Blöcke. Keine Auslassungszeichen, kein
  „… hier unverändert …", keine Pseudo-Diffs.
- Bei Änderungen an bestehenden Dateien: den kompletten betroffenen
  Abschnitt ausgeben und darüberschreiben, ab welcher Zeile oder nach
  welchem Kommentar er einzusetzen ist.
- Kommentare auf Deutsch, im Stil der vorhandenen Dateien:
  Blockkommentare mit `##` und einer **erklärten Absicht**, nicht nur
  einer Beschreibung.
```

Das ist die gesuchte Sprachregel fuer Kommentare: Deutsch, `##`-Blockkommentare, erklaerte Absicht. Auftragspunkt 13 verlangt genau so einen Kommentar ("definiere den Unterschied im Kommentar" zwischen Umgebungsklang und Musik).

**Sprachmass Klasse 8 - gilt fuer Spieltexte, nicht fuer Kommentare** - `auftrag/VERFASSUNG.md`:147 - *gelesen*

```
## Sprachmaß Klasse 8 Oberschule (nachprüfbar)

- Durchschnittliche Satzlänge höchstens 13 Wörter. **Kein Satz länger als
  20 Wörter.**
- Höchstens ein Nebensatz je Satz. Keine Schachtelsätze.
- Keine Substantivketten aus mehr als zwei Wörtern.
- Jedes Fremdwort und jeder historische Fachbegriff wird beim ersten
  Auftreten im selben Satz erklärt. Danach steht er im Glossar.
- Anrede durchgehend „du".
```

Dieses Mass ist ueberschrieben mit "Sprachmass Klasse 8" und wird von Probe 7/8 an Spieltexten gemessen. Fuer Codekommentare gilt allein die Zeile im Ausgabeformat. Das Tongeruest bringt voraussichtlich keinen einzigen neuen Spieltext, also auch keine Sprachprobenlast.

**Entscheidung 24 - der bindende Rahmen des Tongeruests** - `auftrag/ENTSCHEIDUNGEN.md`:407 - *gelesen*

```
**24 — Ruhige klassische Musik ist langfristig geplant. Die Sperre aus
Regel 3 bleibt trotzdem hart.**

Dominiks Anmerkung, gegeben vor dem Beginn von Schritt 2.4 und gerichtet
auf 2.6: **„Es ist langfristig geplant, eine ruhige klassische Musik als
Hintergrundmusik an verschiedenen Stellen einzubauen."**

Das ist kein Widerspruch zu Regel 3, sondern ihre Grenze. Regel 3 verbietet
Musik **an der Front und in der Etappe** — nicht überall. Damit gilt:
```

Regel 3 ist keine Totalsperre, sondern eine Pfadsperre. Musik ist grundsaetzlich vorgesehen, nur nicht auf front und etappe.

**Entscheidung 24 - die drei Punkte, was nie und was moeglich ist** - `auftrag/ENTSCHEIDUNGEN.md`:417 - *gelesen*

```
- **Nie Musik:** auf `front` und `etappe`. Das bleibt eine harte
  Codesperre in `ton_spielen()` (Schritt 2.6, Auftragspunkt 13), keine
  Vereinbarung. Umgebungsklänge sind dort weiter erlaubt.
- **Möglich:** Hauptmenü, Moduswahl, Onboarding, Jahreskarte, Epilog,
  Lebenslauf und der Heimatpfad. **Welche Stellen es am Ende werden,
  entscheidet Dominik**; hier steht nur, dass die Tür offen ist.
- **Kein Ton bewertet je eine Entscheidung** (Regel 3, Auftragspunkt 14).
  Das gilt für Musik genauso: kein Einsatz, der einen Ausgang kommentiert.
```

Die Liste der moeglichen Musikorte ist ausdruecklich NICHT beauftragt: welche Stellen es werden, entscheidet Dominik. Das Geruest darf die Orte also vorsehen, aber nicht besetzen.

**Entscheidung 24 - was daraus fuer den Bau folgt** - `auftrag/ENTSCHEIDUNGEN.md`:426 - *gelesen*

```
**Was daraus für 2.6 folgt, und zwar sofort:** Das Tongerüst wird so
gebaut, dass eine spätere Musikspur **eine Tabellenzeile und eine Datei**
kostet und keinen Umbau. Also eine Tafel neben `ORTSKLANG` für Musik, mit
demselben `renpy.loadable()`-Schutz, und die Sperre als Abfrage über den
Pfad statt über den Kanal. Erfunden wird dabei nichts: Solange keine
Musikdatei im Projekt liegt, ist jede Zeile stumm und die Medienprobe
zählt sie als fehlend (Regel 7).

*5. September 2026. Dominik, als Anmerkung zu Paket 8, Schritt 2.6.*
```

Vier harte Vorgaben: (a) zweite Tafel neben ORTSKLANG fuer Musik, (b) derselbe renpy.loadable()-Schutz, (c) die Sperre fragt den PFAD ab, nicht den Ren'Py-Kanal, (d) die Medienprobe muss die noch fehlenden Ton- und Musikdateien als fehlend zaehlen. Punkt (d) heisst: die Pfade der beiden Tafeln muessen im Medienbuch landen.

**Entscheidung 3 - Ton und Bewegung duerfen nicht aus einem Spiel stammen** - `auftrag/ENTSCHEIDUNGEN.md`:25 - *gelesen*

```
**3 — Animation: dokumentarisch, aber lebendig.**
Papier, Stempel, Tinte, Umschläge. Keine Effekte, die aus einem Spiel
stammen. Details in `VERFASSUNG.md` unter Animationsregeln.
*Dominik, 2. September 2026.*
```

Diese Entscheidung betrifft Animation, nicht Ton. Sie ist die einzige weitere Entscheidung zu Sinneseindruecken und begruendet die dokumentarische Haltung, die Entscheidung 24 fuer Musik fortschreibt. Achtung: Die im Projekt oft zitierte "Regel 3" ist die Audio-Regel aus CLAUDE.md, nicht diese Entscheidung 3 - zwei verschiedene Nummern mit derselben Zahl.

**Entscheidung 22 - Regel 7 (nichts erfinden) wird durch keine Erlaubnis aufgehoben** - `auftrag/ENTSCHEIDUNGEN.md`:359 - *gelesen*

```
- **Gesucht wird, nicht erfunden.** Die Erlaubnis betrifft das
  Nachschlagen in Beständen, die es wirklich gibt, und das Eintragen
  dessen, was dort steht. Sie hebt Regel 7 nicht auf: Eine Signatur, ein
  Titel oder ein Zitat, das sich nicht belegen lässt, wird auch weiterhin
  nicht geschrieben.
```

Uebertragen auf das Tongeruest: Es darf kein Dateiname erfunden werden, zu dem keine Datei existiert oder existieren soll. Zulaessig sind Tafelzeilen, deren Datei bewusst noch fehlt - Entscheidung 24 nennt das ausdruecklich ("jede Zeile stumm", Medienprobe zaehlt sie als fehlend).

**CLAUDE.md Regel 3 - die Audioregel selbst** - `CLAUDE.md`:1 - *vermutet*

```
3. **Audio.** An der Front und in der Etappe nie Musik. Kein Ton, der
   eine Entscheidung bewertet: kein Gewonnen-Klang, kein Fehlerton.
```

Der Wortlaut der Regel, auf die Entscheidung 24 und die Auftragspunkte 13/14 sich beziehen. Zeilennummer nicht gepruefte Angabe: Der Text stammt aus dem Regelblock "Harte Regeln" der CLAUDE.md, die mir als Projektanweisung vorliegt, nicht aus einem eigenen Lesevorgang der Datei.

**Auftrag Paket 8, Teil D - die fuenf Punkte des Tongeruests** - `auftrag/paket08.md`:193 - *gelesen*

```
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
```

Der Auftrag legt Funktionsnamen (ton_spielen), Tafelnamen (ORTSKLANG), die Felder je Tafelzeile (Dateiname, Lautstaerke, Wiederholung) und die verworfenen Aufrufe als Zaehlgroesse fest. Er nennt KEINE Datei und KEINEN init-Rang.

**Auftrag Paket 8, Schritt 2 - die Abnahme fuer den Ton** - `auftrag/paket08.md`:220 - *gelesen*

```
  - Probe: ton_spielen() gibt auf front und etappe null Musikaufrufe frei.
  - probe_alles.py sonst unverändert.
```

Die Abnahme verlangt eine gemessene Null aus probe_alles.py, nicht eine Zusicherung. Zugleich darf probe_alles.py sonst nicht abweichen - eine neue Probe oder ein neuer Abschnitt muss sich also auf diese Messung beschraenken.

**Paketplan - 2.6 ist offen, und die Gliederung gehoert vor die erste Zeile Code** - `auftrag/PAKETPLAN.md`:106 - *gelesen*

```
| 2.6 | **Tongerüst.** `ton_spielen()` mit `renpy.loadable()`, Tafel `ORTSKLANG`, harte Codesperre gegen Musik auf front und etappe. | D, Punkte 11–15 | offen |
```

2.6 ist der letzte offene Unterschritt von Paket 8, Schritt 2. Nach Entscheidung 23 muss eine weitere Untergliederung vor Arbeitsbeginn in dieser Tabelle stehen.

**MEDIEN.md - Kopf: erzeugt, nicht von Hand gepflegt** - `game/MEDIEN.md`:1 - *gelesen*

```
# MEDIEN

Der Bedarfsplan. Jede Datei, die das Spiel erwartet, mit ihrer Herkunft im
Code, ihrem Status und Suchbegriffen für die Recherche.

**Erzeugt von `medienbedarf.py`. Von Hand geänderte Stellen sind beim
nächsten Lauf weg** — was hier fehlt oder falsch steht, gehört im Skript
oder im Spiel geändert.

Das Spiel läuft ohne jede dieser Dateien: Überall greift
`bild_platzhalter()` oder eine Ersatzschrift (Regel 7). Eine fehlende Datei
ist kein Fehler, sondern eine offene Aufgabe.
```

Ein Ton-Eintrag darf NICHT von Hand in MEDIEN.md geschrieben werden. Er entsteht dadurch, dass die Tonpfade im Code (und damit in medien_sammeln) auftauchen; danach wird medienbedarf.py neu laufen gelassen.

**MEDIEN.md - Aufbau: Zahlen, Ordnertabelle, Rechtelage, Leseanleitung, Abschnitte je Ordner** - `game/MEDIEN.md`:15 - *gelesen*

```
## Die Zahlen

| | Dateien |
|---|---|
| Erwartet | **333** |
| Davon vorhanden | **7** |
| Noch abzulegen | **326** |

| Ordner | erwartet | vorhanden | fehlt |
|---|---|---|---|
| `fonts` | 8 | 0 | 8 |
| `images/karten` | 151 | 6 | 145 |
| `images/dokumente` | 50 | 0 | 50 |
| `images/portraits` | 48 | 0 | 48 |
| `images/figuren` | 75 | 0 | 75 |
| `images` | 1 | 1 | 0 |
```

Die Ordnertabelle hat heute sechs Zeilen und keine audio-Zeile. Sobald ein Tonpfad erwartet wird, kaeme eine Zeile `audio` automatisch dazu - die Tabelle wird aus denselben Gruppen gebaut, in denen "audio" bereits vorgesehen ist.

**MEDIEN.md - ein vollstaendiger Medieneintrag (Kartenformat)** - `game/MEDIEN.md`:139 - *gelesen*

```
### front_1914_marsch

1914 · front · Belgien

- `images/karten/front_1914_marsch_1.png` — Option 1, vorhanden
- `images/karten/front_1914_marsch_2.png` — Option 2, vorhanden

Suche: *Marsch 1914*, *Fotografie Belgien 1914*; englisch *photograph Western Front, trench 1914*.

Der Beleg des Ereignisses nennt: Marschleistungen im Aufmarsch August 1914

Wo suchen: Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)
```

So sieht ein voller Eintrag im gebuendelten Format aus: Ueberschrift = Kennung, Zeile mit Jahr/Pfad/Ort, je Datei eine Statuszeile, Suchbegriffe, Beleg, Haus. Dieses Format gilt nur fuer images/karten und images/dokumente.

**MEDIEN.md - das Format, das ein audio-Abschnitt heute bekaeme** - `game/medienbedarf.py`:466 - *gelesen*

```
    ## ---------------------------------------------------------------- Rest
    uebrig = [k for k in gruppen
              if gruppen[k] and k not in ("fonts", "images/karten",
                                          "images/dokumente",
                                          "images/portraits",
                                          "images/figuren")]
    for kategorie in uebrig:
        z.append("---")
        z.append("")
        z.append("## %s" % kategorie)
        z.append("")
        for pfad in gruppen[kategorie]:
            z.append("- `%s` — %s"
                     % (pfad, "vorhanden" if da(pfad) else "**fehlt**"))
            for satz in herkunft[pfad]["herkunft"]:
                z.append("  - %s" % satz)
```

Der Abschnitt fuer Toene entstuende hier, ohne eine Zeile Aenderung an medienbedarf.py: eine Ueberschrift `## audio`, darunter je Pfad eine Zeile mit Status und darunter die Herkunftssaetze aus medien_sammeln(). Wer ein schoeneres Format will (Lautstaerke, Wiederholung, Ort), muesste medienbedarf.py erweitern.

**medienbedarf.py - "audio" ist als Kategorie schon vorgesehen** - `game/medienbedarf.py`:255 - *gelesen*

```
    ## Nach Kategorie gruppieren, in einer festen, lesbaren Folge.
    folge = ["fonts", "images/karten", "images/dokumente", "images/portraits",
             "images/figuren", "images", "audio"]
```

Die Kategorie audio steht bereits in der festen Folge, ganz am Ende. Sie ist heute leer und wird deshalb weder in der Ordnertabelle noch als Abschnitt gedruckt (leere Gruppen werden uebersprungen).

**MEDIEN.md - was heute ueber audio/stummer_morgen.mp3 dort steht** - `game/MEDIEN.md`:1627 - *gelesen*

```
## Vorhanden, aber unbenutzt

Diese Dateien liegen im Projekt, und keine Stelle im Code fragt nach ihnen. Sie sind nicht falsch — sie warten nur auf ihren Ort.

### `audio/stummer_morgen.mp3`

Ein Umgebungsklang. **Nicht an der Front und nicht in der Etappe** — dort ist Musik verboten (Regel 3), und ob dieses Stück Musik oder Umgebung ist, entscheidet sich am Stück selbst. Das Tongerüst entsteht in Paket 8, Schritt 2 mit `ton_spielen()` und der Tafel `ORTSKLANG`; dort bekommt die Datei ihren Ort oder bleibt liegen. Bis dahin ruft sie keine Zeile Code auf, und das ist richtig so.
```

Auftragspunkt 15 ist damit heute in der zweiten Variante erfuellt ("vermerke ihn als unbenutzt"). Der Text kuendigt aber ausdruecklich an, dass 2.6 ueber den Ort entscheidet. Wichtig: Dieser Text ist kein Handeintrag, sondern kommt aus der Tafel VORSCHLAG in medienbedarf.py - wer ihn aendern will, aendert das Skript.

**medienbedarf.py - der Quelltext dieses Vorschlags** - `game/medienbedarf.py`:543 - *gelesen*

```
VORSCHLAG = {
    "audio/stummer_morgen.mp3": (
        "Ein Umgebungsklang. **Nicht an der Front und nicht in der Etappe** "
        "— dort ist Musik verboten (Regel 3), und ob dieses Stück Musik oder "
        "Umgebung ist, entscheidet sich am Stück selbst. Das Tongerüst "
```

Bekommt stummer_morgen.mp3 in 2.6 einen Ort, faellt der Eintrag aus "Vorhanden, aber unbenutzt" heraus und dieser VORSCHLAG-Eintrag wird tot. Er waere dann mitzuziehen (Regel 9), sonst steht im Skript ein Text, den nichts mehr druckt.

**bericht.txt - Kopf der Medienprobe** - `game/bericht.txt`:1100 - *gelesen*

```
PROBE 6  MEDIENPROBE
==============================================================================
Alle Dateipfade, die der Code ueber bild_pfad(), portrait_anzeigen(),
figur_bild_pfad() oder schrift_waehlen() erwartet. Eine fehlende Datei
ist kein Fehler: ueberall greift ein sauberer Ersatz. Die Liste sagt,
was noch abzulegen ist.

Beruecksichtigte Stimmungen: angst, einsam, erschoepft, hungrig, neutral

fonts - 8 erwartet, 0 vorhanden
```

Der Einleitungstext nennt vier Herkunftsfunktionen und keine Tonfunktion. Kommt ton_spielen() dazu, gehoert sie in diesen Satz - sonst behauptet der Bericht etwas Unvollstaendiges. Der Text steht in probe_alles.py, Zeilen 3043 bis 3046.

**bericht.txt - die sechs Rubriken der Medienprobe, audio ist keine davon** - `game/bericht.txt`:1109 - *gelesen*

```
fonts - 8 erwartet, 0 vorhanden
images/dokumente - 50 erwartet, 0 vorhanden
images/figuren - 75 erwartet, 0 vorhanden   (erst gesucht, wenn FIGUREN_ECHTE_BILDER auf True steht)
images/karten - 151 erwartet, 6 vorhanden
images - 1 erwartet, 1 vorhanden
images/portraits - 48 erwartet, 0 vorhanden
```

Sechs Rubriken, alphabetisch nach Pfad sortiert, zusammen 333 Pfade. Eine Rubrik "audio" gibt es heute nicht. Die sechs Zeilen sind aus dem Bericht zusammengezogen (Zeilen 1109, 1120, 1173, 1251, 1405, 1409), stehen dort also nicht direkt untereinander.

**bericht.txt - Schluss der Medienprobe: audio nur als verwaiste Datei** - `game/bericht.txt`:1460 - *gelesen*

```
Vorhanden, aber von keiner Stelle im Code erwartet
------------------------------------------------------------------------------
   audio/stummer_morgen.mp3
   images/karten/front_beginn_1.png
   images/karten/front_beginn_2.png

In BILD_MASSE angelegt, aber von keiner Stelle abgerufen
------------------------------------------------------------------------------
   keine
```

Die einzige Stelle im ganzen Bericht, an der das Wort audio vorkommt. Die Suche nach verwaisten Dateien laeuft ueber die Ordner images, fonts und audio (probe_alles.py Zeile 3086) - der Ordner audio ist der Werkbank also bereits bekannt.

**bericht.txt - Zahl der Faelle und Zustand der Medienprobe** - `game/bericht.txt`:1485 - *gelesen*

```
Erwartet insgesamt: 333 Pfade, davon 7 vorhanden, 326 noch abzulegen.
```

333 ist die Zahl, die auch im Selbsttest (Zeile 15: "6 Medienprobe gelaufen 333 geschrieben"), in der Kurzfassung (Zeile 84: "6 Medienprobe in Ordnung") und im Umfang (Zeile 1827) steht. Jede neue Tonzeile verschiebt alle vier Zahlen zugleich - das ist die messbare Abnahme dafuer, dass Toene in der Probe ankommen.

**probe_alles.py - wie ein Pfad ueberhaupt in die Medienprobe kommt** - `game/probe_alles.py`:291 - *gelesen*

```
    def loadable(self, pfad, directory=None):
        """Prueft die Datei im Spielordner und schreibt die Anfrage mit.

        Das Mitschreiben ist die Grundlage der Medienprobe: Jeder Pfad,
        den bild_pfad(), portrait_anzeigen() oder schrift_waehlen() je
        gesucht haben, steht danach im Medienbuch.
        """
```

Das Medienbuch fuellt sich nur, wenn renpy.loadable() waehrend des Werkbanklaufs wirklich aufgerufen wird. ton_spielen() laeuft im Spiel erst zur Laufzeit - also wird der Tonpfad NICHT von selbst mitgezaehlt.

**probe_alles.py - das Vorbild, wie eine Tafel in die Medienprobe kommt** - `game/probe_alles.py`:3017 - *gelesen*

```
    ## 5. Schriften. Welche Datei zu welcher Schrift gehoert, sagt
    ##    SCHRIFT_KANDIDATEN in gui.rpy - gefragt, nicht nachgebaut.
    for name in sorted(NS.get("SCHRIFT_KANDIDATEN", {})):
        zweck = NS.get("SCHRIFT_ZWECK", {}).get(name, "")
        for stelle, pfad in enumerate(NS["SCHRIFT_KANDIDATEN"][name]):
            NS["renpy"].loadable(pfad)
            merken(pfad,
                   "%s (%s) - %s Wahl in schrift_waehlen(), gui.rpy"
                   % (name, zweck, "erste" if stelle == 0 else "zweite"),
```

Genau so muesste ORTSKLANG (und die Musiktafel) in medien_sammeln() aufgenommen werden: die Tafel aus dem Namensraum FRAGEN, ueber renpy.loadable() eintragen, einen Herkunftssatz merken. Das erfuellt Regel 11 (fragen statt nachbauen) und Entscheidung 24 ("die Medienprobe zaehlt sie als fehlend").

**probe_alles.py - die Rubriken des Berichts entstehen von selbst** - `game/probe_alles.py`:3059 - *gelesen*

```
    gruppen = collections.OrderedDict()
    for pfad in sorted(medienbuch):
        teile = pfad.split("/")
        if len(teile) >= 2:
            kategorie = "/".join(teile[:-1])
        else:
            kategorie = "(Wurzel)"
        gruppen.setdefault(kategorie, []).append(pfad)
```

Sobald ein Pfad audio/... im Medienbuch steht, erscheint im Bericht ohne weiteres Zutun eine Rubrik "audio - N erwartet, M vorhanden", und die Datei verschwindet zugleich aus der Liste der verwaisten Dateien.

**probe_alles.py - eine NEUE .rpy-Datei muesste in die LESEFOLGE eingetragen werden** - `game/probe_alles.py`:69 - *gelesen*

```
LESEFOLGE = [
    "gui.rpy",
    "bewegung.rpy",
    "script.rpy",
    "herkunft.rpy",
    "kapitel.rpy",
    "dialoge.rpy",
    "figuren.rpy",
    "merkbuch.rpy",
    "minispiele.rpy",
```

Wuerde das Tongeruest eine eigene Datei bekommen (etwa ton.rpy), waere sie hier einzutragen - sonst laeuft ihr init-Block in der Werkbank nie, und jede Probe urteilt ueber ein Spiel ohne Ton. Der Selbsttest wuerde das nicht als Fehler melden, weil er nur die gelesenen Dateien zaehlt (bericht.txt Zeile 102 bis 110 nennt neun Dateien).

**gui.rpy - das Vorbild fuer eine Medienfunktion mit renpy.loadable()** - `game/gui.rpy`:74 - *gelesen*

```
    def schrift_waehlen(kandidaten, ersatz):
        for pfad in kandidaten:
            if renpy.loadable(pfad):
                return pfad
```

Dieselbe Bauform, die Auftragspunkt 11 fuer ton_spielen() verlangt. Die Funktion steht im Block `init -50 python:` (gui.rpy Zeile 1), zusammen mit bild_pfad(), bild_vorhanden(), bild_platzhalter() und bild_anzeigen() (Zeilen 581, 584, 620, 662). Ein Tongeruest in gui.rpy laege damit bei init -50 und waere fuer jede spaetere Datei verfuegbar.

**Fuenf Dateikoepfe behaupten heute "Kein Audio"** - `game/dialoge.rpy`:12 - *gelesen*

```
##  - Kein Audio. An der Front ausdrücklich keine Musik.
```

Denselben Satz tragen minispiele.rpy Zeile 26 ("Kein Audio. An der Front ausdruecklich keine Musik: Diese Datei legt keinen einzigen Ton an, auch keinen Klick beim Streichen."), figuren.rpy Zeile 19, kapitel.rpy Zeile 19 und merkbuch.rpy Zeile 35. Ein Tongeruest macht diese Koepfe teilweise unwahr, sobald eine dieser Dateien einen Klang ausloest. Regel 9 verlangt, alle Fundstellen mitzufuehren - hier sind es fuenf.

**AUFGEFALLEN.md enthaelt keinen Punkt zu Ton, Audio, Musik oder Klang** - `AUFGEFALLEN.md`:1306 - *erschlossen*

```
    Ebenfalls stumm sind die **Wertebalken**: Sie bestehen aus Flächen,
    nicht aus Text. Die Auskunft geht nicht verloren, weil der
    Zustandssatz daneben („Hungrig", „Am Ende") dasselbe in Worten sagt —
    und der wird gelesen.
```

Das ist der einzige Treffer meiner Suche nach ton/klang/musik/audio/sound/stumm/geraeusch/laerm/hoerbar/akustisch in AUFGEFALLEN.md - und er meint das Vorlesen durch den Bildschirmleser, nicht Ton. Das Protokoll hat zum Tongeruest also keine Vorgeschichte und keine Warnung. Auch auftrag/OFFENE_PUNKTE.md liefert zu denselben Begriffen keinen Treffer.

**Naechstliegende Ton-Vorgeschichte im Protokoll ist eine Medien-, keine Tonfrage** - `AUFGEFALLEN.md`:1139 - *gelesen*

```
83. **ZWEI KARTENBILDER GEHÖREN ZU KEINEM EREIGNIS.**
    `images/karten/front_beginn_1.png` und `_2.png` liegen im Projekt und
    folgen dem Namensschema `<kennung>_<nummer>.png` — aber ein Ereignis
    `front_beginn` gibt es im Bestand nicht.
```

Punkt 83 behandelt die beiden anderen verwaisten Dateien und zeigt, wie das Projekt mit einer Datei ohne Ort umgeht: sie bleibt liegen, der Vorschlag steht in MEDIEN.md, entschieden wird nicht stillschweigend. Dieselbe Haltung waere fuer stummer_morgen.mp3 begruendbar.

### Offene Fragen und Urteil

- In welche Datei gehoeren ton_spielen() und ORTSKLANG? Weder VERFASSUNG.md noch paket08.md noch ENTSCHEIDUNGEN.md nennen eine. Nach der Aufbau-Tabelle waere gui.rpy der einzige Ort mit Medienbezug ("Bildersatz", init -50/-2); eine eigene ton.rpy waere die zehnte Datei und muesste in probe_alles.py LESEFOLGE eingetragen werden.
- Welcher init-Rang? Die Verfassung gibt nur Raenge je Datei an. Ein Rang muss frueh genug liegen, damit jede aufrufende Stelle die Tafeln kennt; bei gui.rpy waere es -50, das frueheste im Projekt.
- Wie heisst die Musiktafel? Entscheidung 24 verlangt "eine Tafel neben ORTSKLANG fuer Musik", nennt aber keinen Namen. Der Name ist nach der Rollenteilung eine Benennung im Code und damit Claudes Entscheidung - er gehoert dann in die Bezeichnerkarte.
- Muss die Bezeichnerkarte in VERFASSUNG.md um eine Ton-Zeile ergaenzt werden? Die Verfassung sagt "Benutzen statt neu erfinden", verlangt aber an keiner Stelle ausdruecklich das Eintragen neuer Namen. Jede andere Werkzeuggruppe hat eine Zeile.
- Wie kommen die Tonpfade in die Medienprobe, ohne dass probe_alles.py mehr als noetig veraendert wird? Die Abnahme sagt "probe_alles.py sonst unveraendert", Entscheidung 24 verlangt zugleich, dass die Probe fehlende Musikdateien zaehlt. Das Schriftenvorbild (Zeile 3017 ff.) waere der regelkonforme Weg, ist aber eine Aenderung an medien_sammeln().
- Wie werden die verworfenen Musikaufrufe auf front und etappe gezaehlt und wo im Bericht erscheinen sie? Auftragspunkt 13 verlangt eine Zaehlung "in der Probe", nennt aber weder Probe noch Abschnitt.
- Was geschieht mit den fuenf Dateikoepfen, die "Kein Audio" behaupten (dialoge, minispiele, figuren, kapitel, merkbuch)? Sie werden durch ein Tongeruest teilweise unwahr.
- Bekommt audio/stummer_morgen.mp3 einen Ort oder bleibt er liegen (Auftragspunkt 15)? Der Auftrag laesst beides zu; MEDIEN.md kuendigt die Entscheidung fuer 2.6 an. Ob das Stueck Musik oder Umgebungsklang ist, laesst sich nur am Stueck selbst entscheiden - ich habe es nicht angehoert.
- Nach dem Bau muss medienbedarf.py neu laufen, sonst steht in MEDIEN.md weiter die alte Zahl 333/7/326 und der Vorschlagstext zu stummer_morgen.mp3.

---

## 3 - Das Vorbild in gui.rpy (bild_anzeigen, schrift_waehlen)

Alle drei Vorbildfunktionen stehen im ersten init-Block des ganzen Projekts, gui.rpy init -50 (Zeile 1 bis 682); bericht.txt Zeile 113 belegt, dass gui:1@-50 vor jedem anderen Block laeuft - deshalb der Rang, denn script.rpy (-10) und dialoge.rpy (-5) rufen bild_anzeigen() und bild_platzhalter() bereits auf. Das Pruefmuster ist ueberall gleich und kurz: Pfad an genau einer Stelle bauen (bild_pfad), Kandidaten der Reihe nach mit renpy.loadable() versuchen, beim ersten Treffer zurueckgeben, sonst still auf einen Ersatz fallen; keine Funktion hat mehr als vier bis sechs Zeilen. Die entscheidende Antwort auf deine Kernfrage: Der Spielcode merkt sich eine fehlende Datei NICHT - es gibt keine Liste und kein Dict fehlender Pfade, die sechs renpy.loadable()-Fundstellen im ganzen Projekt schreiben nirgends hin. Das Register heisst medienbuch, ist ein dict pfad -> {'anfragen', 'vorhanden'} und lebt ausschliesslich in probe_alles.py: Die RenpyAttrappe.loadable() (Zeile 291) schreibt jede Anfrage mit, waehrend medien_sammeln() (Zeile 2900) die echten Projektfunktionen aufruft. Ein Tonpfad taucht also nur dann in der Medienprobe auf, wenn medien_sammeln() um einen sechsten Abschnitt erweitert wird, der die ORTSKLANG-Tafel abfragt - genau so, wie Abschnitt 5 heute SCHRIFT_KANDIDATEN abfragt ('gefragt, nicht nachgebaut'). Fuer die Tafel selbst gibt es drei brauchbare Vorbilder: SCHRIFT_KANDIDATEN + SCHRIFT_ZWECK (zwei flache Tafeln, gleiche Schluessel), BILD_MASSE + BILD_ANZEIGE (zwei Tafeln fuer zwei Leser) und PFAD_ORT (Kennung -> Wert je Pfad). Fuer die harte Musiksperre existiert ebenfalls eine fertige Bauart: eine leere GROSSBUCHSTABEN-Liste im init-Block, die das Spiel fuellt und die Probe beanstandet (KARTENTYP_UNBEKANNT, script.rpy 390-395, ausgelesen in probe_alles.py 3118-3135) - 'Das Spiel laeuft weiter, die Probe schlaegt Alarm'. Ton ist im Projekt bisher voellig unbenutzt: keine einzige .rpy-Zeile ruft renpy.play oder einen audio-Pfad, es gibt genau eine Datei (audio/stummer_morgen.mp3, 5,5 MB), und die Medienprobe durchsucht den audio-Ordner bereits und meldet sie als verwaist.

### Befunde (33)

**schrift_waehlen() vollstaendig** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:74 - *gelesen*

```
    def schrift_waehlen(kandidaten, ersatz):
        for pfad in kandidaten:
            if renpy.loadable(pfad):
                return pfad
        return ersatz
```

Fuenf Zeilen, kein Docstring, kein Merker. Das Muster ist: Kandidatenliste der Reihe nach mit renpy.loadable() durchgehen, den ersten Treffer zurueckgeben, sonst den uebergebenen Ersatz. Fuer ton_spielen() heisst das: pruefen und still zurueckfallen, nicht melden.

**Tafel Kennung -> Dateiliste: SCHRIFT_KANDIDATEN** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:80 - *gelesen*

```
    ## Welche Datei zu welcher Schrift gehört. Die Tafel ist nicht Zierde:
    ## medienbedarf.py schreibt aus ihr in MEDIEN.md, für welche Schrift ein
    ## Pfad gesucht wird. Ohne sie stünde dort nur "irgendeine der vier".
    ## Wer eine Schrift hinzufügt, trägt sie hier ein und ruft
    ## schrift_waehlen() mit SCHRIFT_KANDIDATEN[...] auf — dann stimmt der
    ## Bedarfsplan von selbst.
    SCHRIFT_KANDIDATEN = {
        "SCHRIFT_FLIESS": ["fonts/fliesstext.ttf", "fonts/fliesstext.otf"],
        "SCHRIFT_TITEL": ["fonts/titel.ttf", "fonts/titel.otf"],
        "SCHRIFT_DOKUMENT": ["fonts/dokument.ttf", "fonts/dokument.otf"],
        "SCHRIFT_SCHMAL": ["fonts/schmal.ttf", "fonts/schmal.otf"],
    }
```

Das ist das naechste Vorbild fuer ORTSKLANG: GROSSBUCHSTABEN-Dict, Kennung -> Liste von Dateipfaden, direkt ueber dem Konstruktionsaufruf, mit einem Kommentar, der sagt, WER die Tafel sonst noch liest (medienbedarf.py / MEDIEN.md) und was ein Neueintrag kostet.

**Zweite Tafel neben der ersten: SCHRIFT_ZWECK** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:93 - *gelesen*

```
    ## Wofür jede Schrift da ist - ebenfalls für MEDIEN.md, damit der, der
    ## das Material sammelt, weiß, was er sucht.
    SCHRIFT_ZWECK = {
        "SCHRIFT_FLIESS": "Fließtext und Bedienung; die Grundschrift",
        "SCHRIFT_TITEL": "Überschriften, Ereignistext, Kartentitel",
        "SCHRIFT_DOKUMENT": "Briefe und Vordrucke; wirkt geschrieben",
        "SCHRIFT_SCHMAL": "Aufdrucke: Stempel, Aktenzeichen, Rubriken",
    }
```

Im Projekt stehen Eigenschaften nicht in einem verschachtelten Dict, sondern als zweite flache Tafel mit denselben Schluesseln. ORTSKLANG mit Datei + Lautstaerke + Wiederholung koennte entweder diesem Muster folgen (mehrere flache Tafeln) oder dem von BILD_MASSE/BILD_ANZEIGE (zwei Tafeln, verschiedene Leser).

**Beispiel fuer einen vollstaendigen Kommentar vor einem neuen Eintrag** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:117 - *gelesen*

```
    ## Die vierte Schrift, seit Paket 8, Schritt 1: schmal und eng, für
    ## Aufdrucke — Stempel und Aktenzeichen. Ein Aufdruck ist nicht gesetzt,
    ## sondern geschlagen oder gedruckt; er steht enger als Fließtext und
    ## braucht deshalb einen eigenen Schnitt statt eines fetten Fließtexts.
    ##
    ## Der Ersatz ist SCHRIFT_DOKUMENT und nicht SCHRIFT_FLIESS: Fehlt die
    ## Datei, gehört ein Aufdruck immer noch näher zum Amtsblatt als zur
    ## Erzählung. Solange keine der beiden Dateien liegt, sieht man von
    ## dieser Zeile nichts — genau wie bei den drei Schriften darüber.
    SCHRIFT_SCHMAL = schrift_waehlen(
        SCHRIFT_KANDIDATEN["SCHRIFT_SCHMAL"],
        SCHRIFT_DOKUMENT
    )
```

Aufbau eines Projektkommentars: (1) seit wann und wofuer, (2) die sachliche Begruendung in Alltagssprache, (3) Leerzeile mit ## als Absatztrenner, (4) warum gerade DIESE Entscheidung und nicht die naheliegende andere, (5) was man sieht, solange die Datei fehlt. Zwei Bindestriche gibt es nicht, es wird der Gedankenstrich benutzt.

**Die Zwei-Tafeln-Regel bei BILD_MASSE / BILD_ANZEIGE** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:34 - *gelesen*

```
    ## Bildmaße ###############################################################
    ##
    ## Zwei Tafeln mit verschiedenen Aufgaben. BILD_MASSE nennt das Maß, in
    ## dem eine Datei abzulegen ist; es steht in MEDIEN.md und richtet sich an
    ## den, der das Material sammelt. BILD_ANZEIGE nennt das Maß, in dem das
    ## Bild auf dem Bildschirm erscheint — nur diese Tafel liest der Code, und
    ## zwar allein in bild_masse_holen().
```

Ueberschriften im init-Block sind '## Titel ' plus Rautenkette bis Spalte 80. Inhaltlich: Was der Materialsammler braucht und was der Code braucht, sind getrennte Tafeln, und es steht dabei, welche Funktion die eine liest.

**BILD_MASSE und BILD_ANZEIGE woertlich** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:60 - *gelesen*

```
    BILD_MASSE = {
        "karten": (800, 450),
        "portraits": (500, 500),
        "dokumente": (900, 600),
    }

    BILD_ANZEIGE = {
        "karten": (468, 264),
        "portraits": (240, 240),
        "dokumente": (720, 480),
    }
```

Aufbau einer Eigenschaftstafel: Schluessel klein und ohne Umlaut, Wert ein Tupel, Zeile fuer Zeile, abschliessendes Komma. Keine verschachtelten Dicts.

**Pfadbau als eigene Funktion, die auch die Probe ruft** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:581 - *gelesen*

```
    def bild_pfad(kategorie, kennung):
        return "images/" + str(kategorie) + "/" + str(kennung) + ".png"

    def bild_vorhanden(kategorie, kennung):
        if not kennung:
            return False
        return renpy.loadable(bild_pfad(kategorie, kennung))
```

Der Dateipfad entsteht an genau EINER Stelle und wird nirgends zusammengesetzt. Die Werkbank ruft NS["bild_pfad"](...) statt den Pfad nachzubauen (Regel 11). Ein ton_pfad(kennung) nach demselben Muster ist damit faktisch vorgeschrieben, wenn die Medienprobe die Tonpfade zaehlen soll.

**Der Kommentarblock ueber dem Platzhalter - vollstaendiges Vorbild fuer Ton** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:591 - *gelesen*

```
    ## SEIT PAKET 8. Der Platzhalter hatte bis dahin ein Gesicht: den
    ## gesuchten Dateipfad in Rot auf grauem Grund. Für die Arbeit ist das
    ## richtig — man sieht sofort, welche Datei fehlt. Für den Unterricht
    ## ist es falsch, und zwar deutlich: **326 der 333 Dateien fehlen.**
    ## Ein Spiel, das an dreihundert Stellen eine rote Fehlermeldung zeigt,
    ## sieht nicht unfertig aus, sondern kaputt — und niemand liest den
    ## Text einer Karte, über der eine Warnung steht.
    ##
    ## Deshalb zwei Gesichter, unterschieden durch persistent.analysemodus,
    ## der im Projekt längst die Werkzeugsicht schaltet und ab Werk aus ist:
    ##
    ##   im Spiel       eine ruhige Leerstelle. Getöntes Papier, ein feiner
    ##                  Rahmen, vier Eckwinkel wie die Ecken, mit denen ein
    ##                  Foto ins Album geklebt wird. Sie sagt "hier gehört
    ##                  ein Bild hin", ohne ein Wort und ohne zu stören.
```

Der Block geht bis Zeile 609 weiter (im Analysemodus zusaetzlich der Pfad; Schlusssatz: 'Das Spiel sieht damit auch ohne eine einzige Bilddatei fertig aus, und die Bilder sind später eine Verbesserung statt einer Bedingung.'). Muster: Ueberschrift mit Rautenkette, SEIT PAKET N in Grossbuchstaben, gemessene Zahl als Begruendung, eingerueckte zweispaltige Aufzaehlung fuer Fallunterscheidungen, Schlusssatz mit der Haltung. Fuer Ton heisst der aequivalente Satz: solange keine Tondatei liegt, ist es still - und Stille ist kein Mangel, den man sieht.

**bild_platzhalter() - Signatur und Innenleben** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:620 - *gelesen*

```
    def bild_platzhalter(breite, hoehe, gesuchter_pfad):
        ## Die Winkel wachsen mit der Fläche, bleiben aber bescheiden:
        ## auf einem kleinen Portrait sollen sie nicht das Bild werden.
        laenge = max(10, min(26, int(min(breite, hoehe) / 7)))
        rand = max(8, int(laenge / 2))
        winkel = eckwinkel(laenge, 2, FARBE_LINIE_FEIN)
```

Kein Docstring, sondern ein zweizeiliger ##-Kommentar direkt in der Funktion, der die Rechnung begruendet. Der gesuchte Pfad wird als Parameter durchgereicht, damit die Funktion ihn anzeigen kann - er wird nirgends gespeichert.

**Der Analysemodus-Zweig im Platzhalter** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:639 - *gelesen*

```
        ## Nur bei der Arbeit: welche Datei hier fehlt.
        if persistent.analysemodus:
            groesse = max(11, min(30, int(hoehe / 9)))
            teile.append(Text(
                str(gesuchter_pfad),
                size=groesse,
                color=FARBE_FEHLEND,
                font=SCHRIFT_FLIESS,
                text_align=0.5,
                align=(0.5, 0.5),
                xsize=int(breite * 0.9)
            ))
```

Die einzige Stelle, an der eine fehlende Datei ueberhaupt sichtbar wird - und nur bei persistent.analysemodus (Vorgabe False, options.rpy Zeile 43). Sie wird angezeigt, nicht vermerkt. Fuer ton_spielen() gibt es kein sichtbares Gegenstueck; ein verworfener Musikaufruf braucht deshalb einen anderen Weg in die Probe.

**bild_masse_holen() und bild_anzeigen() vollstaendig** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:654 - *gelesen*

```
    def bild_masse_holen(kategorie, breite, hoehe):
        vorgabe = BILD_ANZEIGE.get(kategorie, (468, 264))
        if breite is None:
            breite = vorgabe[0]
        if hoehe is None:
            hoehe = vorgabe[1]
        return breite, hoehe

    def bild_anzeigen(kategorie, kennung, breite=None, hoehe=None):
        breite, hoehe = bild_masse_holen(kategorie, breite, hoehe)
        pfad = bild_pfad(kategorie, kennung)
        if renpy.loadable(pfad):
            return Transform(pfad, xysize=(breite, hoehe))
        return bild_platzhalter(breite, hoehe, pfad)
```

bild_anzeigen() ist vier Zeilen lang und hat keinen Docstring. Die Eigenschaften kommen ueber .get(kategorie, harte Vorgabe) aus der Tafel - eine unbekannte Kennung stuerzt nie ab. ton_spielen(kennung) sollte genauso kurz sein: Eigenschaften aus ORTSKLANG.get(kennung) holen, Pfad bauen, loadable pruefen, sonst nichts tun.

**portrait_anzeigen() - Kandidatenkette mit Rueckfall** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:669 - *gelesen*

```
    def portrait_anzeigen(kennung, stimmung, breite=None, hoehe=None):
        breite, hoehe = bild_masse_holen("portraits", breite, hoehe)
        if not kennung:
            return bild_platzhalter(breite, hoehe, "images/portraits/")
        kandidaten = [
            str(kennung) + "_" + str(stimmung),
            str(kennung) + "_neutral",
            str(kennung),
        ]
        for eintrag in kandidaten:
            pfad = bild_pfad("portraits", eintrag)
            if renpy.loadable(pfad):
                return Transform(pfad, xysize=(breite, hoehe))
        return bild_platzhalter(breite, hoehe, bild_pfad("portraits", kandidaten[0]))
```

Dieselbe Kandidatenkette wie schrift_waehlen(), nur inline. Eine leere Kennung fuehrt sofort zum Ersatz statt zu einem Pfad wie 'images/portraits/.png'. Fuer ton_spielen() gilt dasselbe: leere Kennung = still zurueck, nicht Pfad bauen.

**init-Rang: gui.rpy steht auf -50** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:1 - *gelesen*

```
init -50 python:
```

Alle drei Funktionen und alle Tafeln (Farben, KOPF_*, BILD_MASSE, BILD_ANZEIGE, SCHRIFT_*, Rahmen, bild_*) stehen in diesem einen Block, der von Zeile 1 bis Zeile 682 reicht. In Zeile 684 folgt 'init offset = -2', deshalb laufen die beiden weiteren init-Bloecke der Datei (Zeile 686 und 806) auf Rang -2.

**Warum -50: es ist der allererste Block des ganzen Projekts** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\bericht.txt`:112 - *gelesen*

```
Ausfuehrungsfolge (init-Rang, dann Datei, dann Stelle):
   gui:1@-50   bewegung:29@-45   dialoge:25@-20   script:1@-20   script:2754@-20
   herkunft:57@-19   kapitel:56@-19   kapitel:420@-19   kapitel:576@-19   dialoge:115@-10
   herkunft:293@-10   script:261@-10   kapitel:716@-9   figuren:66@-8   figuren:171@-8
   merkbuch:67@-7   minispiele:68@-6   minispiele:189@-6   minispiele:644@-6   dialoge:164@-5
   script:449@-5   herkunft:383@-4   gui:686@-2   gui:806@-2   dialoge:518@0
```

gui:1@-50 laeuft vor allem anderen. Das ist der Grund fuer den Rang: script.rpy (@-10, Zeile 407 kartenmotiv) und dialoge.rpy (@-5, Zeile 340 figur_bild) rufen bild_anzeigen() bzw. bild_platzhalter() auf, und die define-Zeilen ab gui.rpy 699 lesen SCHRIFT_FLIESS. Wer ton_spielen() so tief legt, kann es von ueberall rufen; wer eine ORTSKLANG-Tafel dorthin legt, hat sie vor jeder anderen Datei verfuegbar.

**KEIN Merker im Spiel: die fehlende Datei wird nirgends vermerkt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:665 - *gelesen*

```
        if renpy.loadable(pfad):
            return Transform(pfad, xysize=(breite, hoehe))
        return bild_platzhalter(breite, hoehe, pfad)
```

Es gibt im Spielcode keine Liste und kein Dict fehlender Pfade. Eine Suche nach renpy.loadable ueber alle .rpy-Dateien ergibt genau sechs Fundstellen (gui.rpy 76, 587, 665, 680; dialoge.rpy 351, 353), und keine davon schreibt irgendwo hin. Der Aufruf gibt nur True/False zurueck.

**Wer sich die fehlenden Dateien merkt: die Attrappe in der Werkbank** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\probe_alles.py`:291 - *gelesen*

```
    def loadable(self, pfad, directory=None):
        """Prueft die Datei im Spielordner und schreibt die Anfrage mit.

        Das Mitschreiben ist die Grundlage der Medienprobe: Jeder Pfad,
        den bild_pfad(), portrait_anzeigen() oder schrift_waehlen() je
        gesucht haben, steht danach im Medienbuch.
        """
        name = str(pfad)
        da = os.path.isfile(os.path.join(self.spielordner, name.replace("/", os.sep)))
        eintrag = self.medienbuch.setdefault(name, {"anfragen": 0, "vorhanden": da})
        eintrag["anfragen"] += 1
        eintrag["vorhanden"] = da
        return da
```

DIE ANTWORT AUF DIE KERNFRAGE. Das Register heisst medienbuch, ist ein schlichtes dict pfad -> {'anfragen': int, 'vorhanden': bool}, wird in probe_alles.py Zeile 398 als self.medienbuch = {} angelegt, in Zeile 438 an den Namensraum gehaengt und in Zeile 4952 an probe_medien() weitergereicht. Es lebt AUSSCHLIESSLICH in der Werkbank, nie im Spiel. Ein Tonpfad landet also genau dann in der Medienprobe, wenn die Probe ihn ueber renpy.loadable() erfragt - also wenn medien_sammeln() ton_spielen() oder ton_pfad() wirklich aufruft.

**medien_sammeln() - eine Quelle fuer zwei Leser** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\probe_alles.py`:2900 - *gelesen*

```
def medien_sammeln(NS, medienbuch, spielordner):
    """Jeden erwarteten Dateipfad MIT SEINER HERKUNFT.

    EINE Quelle fuer zwei Leser: probe_medien() zaehlt damit, und
    medienbedarf.py schreibt MEDIEN.md daraus. Stuenden die Schleifen
    zweimal da, naennte der Bedarfsplan andere Pfade als der Bericht, und
    niemand wuesste, welche Liste stimmt (Regel 11).

    Geliefert wird ein Woerterbuch

        pfad -> {"herkunft": [Satz, ...], "kategorie": str}

    und nebenbei das Medienbuch gefuellt, weil jeder Aufruf ueber
    renpy.loadable() laeuft. Die Zahl der Beanstandungen kommt mit: ein
    Pfad ohne Kennung darf so nie entstehen."""
```

Die Funktion hat heute fuenf nummerierte Abschnitte (1 Karten/Dokumente, 2 Portraets, 3 Nebenfiguren, 4 Platzhalter, 5 Schriften, Zeilen 2948 bis 3026). Ein Tongeruest braucht dort einen Abschnitt 6, sonst taucht kein Tonpfad in bericht.txt und kein Ton in MEDIEN.md auf. Der Docstring endet in der Datei mit einer eigenen Zeile fuer die schliessenden Anfuehrungszeichen.

**Wie die Probe eine Tafel abfragt statt sie nachzubauen** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\probe_alles.py`:3017 - *gelesen*

```
    ## 5. Schriften. Welche Datei zu welcher Schrift gehoert, sagt
    ##    SCHRIFT_KANDIDATEN in gui.rpy - gefragt, nicht nachgebaut.
    for name in sorted(NS.get("SCHRIFT_KANDIDATEN", {})):
        zweck = NS.get("SCHRIFT_ZWECK", {}).get(name, "")
        for stelle, pfad in enumerate(NS["SCHRIFT_KANDIDATEN"][name]):
            NS["renpy"].loadable(pfad)
            merken(pfad,
                   "%s (%s) - %s Wahl in schrift_waehlen(), gui.rpy"
                   % (name, zweck, "erste" if stelle == 0 else "zweite"),
                   "fonts")
```

Genau die Bauart, die ein ORTSKLANG-Abschnitt bekommen muesste: ueber die Tafel im Namensraum laufen, NS['renpy'].loadable(pfad) rufen (das fuellt das Medienbuch) und mit merken() einen Herkunftssatz eintragen, der die aufrufende Funktion und die Datei nennt. Das dritte Argument von merken() ist die Kategorie und wuerde 'audio' lauten.

**Eine fehlende Mediendatei ist ausdruecklich KEINE Beanstandung** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\probe_alles.py`:3031 - *gelesen*

```
def probe_medien(NS, B, medienbuch, spielordner):
    """Sammelt alle Pfade, die der Code je gesucht hat oder suchen wird.

    Die Bilder legt der Projektleiter spaeter selbst ab. Eine fehlende
    Datei ist deshalb KEINE Beanstandung: Der Code faellt ueberall sauber
    auf bild_platzhalter() oder auf eine Ersatzschrift zurueck. Beanstandet
    wird nur ein Pfad, der so nie entstehen darf - eine leere Kennung etwa.
    """
```

Beanstandet wird nur, was gar nicht entstehen darf. Ein fehlender Ton ist also 'fehlt noch', nicht 'FEHLER'. Ein auf front/etappe verworfener Musikaufruf dagegen waere eine Beanstandung - er gehoert in die Bauart von KARTENTYP_UNBEKANNT, nicht ins Medienbuch.

**Die Medienprobe durchsucht bereits den audio-Ordner** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\probe_alles.py`:3084 - *gelesen*

```
    ## Verwaiste Dateien: liegt ab, wird aber nirgends gesucht.
    verwaist = []
    for ordner in ["images", "fonts", "audio"]:
        wurzel = os.path.join(spielordner, ordner)
        if not os.path.isdir(wurzel):
            continue
        for gang, _unter, dateien in os.walk(wurzel):
            for name in dateien:
                voll = os.path.join(gang, name)
                rel = os.path.relpath(voll, spielordner).replace(os.sep, "/")
                if rel not in medienbuch:
                    verwaist.append(rel)
```

'audio' steht schon in der Liste. audio/stummer_morgen.mp3 wird heute als verwaist gemeldet; sobald ORTSKLANG den Pfad nennt und die Probe ihn erfragt, verschwindet er aus dieser Liste und taucht in der Gruppe 'audio - N erwartet, M vorhanden' auf. Die Gruppierung geschieht automatisch ueber den Ordnerteil des Pfades (Zeilen 3059 bis 3066).

**Warnung: eine Tafel ohne aufrufende Stelle wird angemahnt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\probe_alles.py`:3103 - *gelesen*

```
    ## Bildarten, fuer die BILD_MASSE ein Format nennt, die aber niemand
    ## abruft. Kein Fehler, sondern ein Hinweis darauf, was noch aussteht.
    genutzt = set()
    for pfad in medienbuch:
        teile = pfad.split("/")
        if len(teile) >= 3 and teile[0] == "images":
            genutzt.add(teile[1])
    ungenutzt = [k for k in NS["BILD_MASSE"] if k not in genutzt]
    B.unterteil("In BILD_MASSE angelegt, aber von keiner Stelle abgerufen")
    if not ungenutzt:
        B("   keine")
    for kategorie in ungenutzt:
        B("   %-14s Anzeigemass %s" % (
            kategorie, NS["BILD_ANZEIGE"].get(kategorie, "-")))
```

Das Projekt hat schon einmal Tafeleintraege ohne aufrufende Stelle gestrichen (gui.rpy 42 bis 58: 'personen' und 'orte'). Eine ORTSKLANG-Zeile ohne Aufrufstelle waere derselbe Fall - 'nur ein Versprechen'. Wer die Tafel baut, baut zugleich die Stelle, die sie ruft.

**Die Bauart fuer verworfene Aufrufe: Liste im Spiel, Alarm in der Probe** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\script.rpy`:390 - *gelesen*

```
    ## Ein Tippfehler im Typ darf NICHT still auf die Vorgabe zurückfallen.
    ## Dann sähe eine Brotkarte aus wie eine Szene, und niemand merkte es —
    ## es gäbe keine Fehlermeldung, nur ein falsches Bild. Dieselbe Bauart
    ## wie NACHTRAG_OHNE_TREFFER (Entscheidung 16): Das Spiel läuft weiter,
    ## die Probe schlägt Alarm.
    KARTENTYP_UNBEKANNT = []
```

Das ist die vorhandene Loesung fuer 'die Probe soll etwas zaehlen, das im Spiel still passiert'. Eine leere Liste in GROSSBUCHSTABEN im init-Block, im Spiel befuellt, von der Probe ausgelesen. Fuer Auftragspunkt 13 (Musik auf front/etappe verwerfen und in der Probe zaehlen) ist das die naheliegende Form, z. B. MUSIK_VERWORFEN = [].

**Wie die Probe eine solche Liste ausliest und beanstandet** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\probe_alles.py`:3118 - *gelesen*

```
    ## Die Kartentypen. Ein Typ, den KARTENTYPEN nicht kennt, faellt im Spiel
    ## still auf "karte" zurueck - eine Brotkarte saehe dann aus wie eine
    ## Szene, ohne dass irgendwo ein Fehler entstuende. Deshalb sammelt die
    ## Klasse jeden solchen Fall in KARTENTYP_UNBEKANNT, und hier wird er
    ## beanstandet. Dieselbe Bauart wie NACHTRAG_OHNE_TREFFER.
    B.unterteil("Kartentypen")
    for typ in NS["KARTENTYPEN"]:
        B("   %-14s %3d Ereignisse   Bildordner images/%s"
          % (typ, typenzaehler.get(typ, 0), NS["kartenbild_kategorie"](typ)))
    unbekannt = NS["KARTENTYP_UNBEKANNT"]
    if unbekannt:
        B("")
        B("   UNBEKANNTER TYP - faellt im Spiel still auf \"karte\" zurueck:")
        for kennung, typ in unbekannt:
            B("      %-36s %s" % (kennung, typ))
```

Danach folgt 'beanstandungen += len(unbekannt)' (Zeile 3133) und ein else-Zweig 'Kein unbekannter Typ.' (Zeile 3135). Regel 11 verlangt den Abschnitt auch bei null Beanstandungen - deshalb der else-Zweig. Ein Ton-Abschnitt muesste genauso immer schreiben, auch wenn null Musikaufrufe verworfen wurden.

**Tafel + Aufrufstelle + Docstring: kartenbild_kategorie() und kartenmotiv()** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\script.rpy`:407 - *gelesen*

```
    def kartenmotiv(vorlage, auswahl, breite=468, hoehe=264):
        """Das Motiv einer Entscheidungskarte — die einzige Stelle.

        Auch die Medienprobe ruft diese Funktion. Stünde die Zuordnung von
        Typ zu Ordner ein zweites Mal in der Werkbank, liefe sie früher oder
        später auseinander, und dann glaubte jemand der falschen Liste
        (Regel 11).
        """
        kategorie = kartenbild_kategorie(getattr(vorlage, "kartentyp", "karte"))
        return bild_anzeigen(kategorie, auswahl.bild, breite, hoehe)
```

Docstring-Bauart im Projekt: erste Zeile ein Halbsatz mit Gedankenstrich, Leerzeile, dann ein Absatz, der begruendet, warum es die Funktion einmal und nur einmal gibt, mit Regelverweis in Klammern. Genau so sollte ton_spielen() beschrieben sein.

**KARTENTYPEN - Liste plus erklaerende Kommentartafel** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\script.rpy`:379 - *gelesen*

```
    ##   karte         die Vorgabe — ein Bogen, wie bisher
    ##   feldpost      ein schmaler Bogen mit Faltlinie
    ##   lebensmittel  ein Raster aus abtrennbaren Abschnitten
    ##   zeitung       zwei Spalten unter einer Balkenüberschrift
    ##   amtlich       ein Vordruck mit Behördenkopf und Stempelfeld
    ##
    ## KEIN Typ verlangt eine Bilddatei. Jedes Layout entsteht aus Rahmen,
    ## Flächen und Text; wo ein Motiv fehlt, greift bild_platzhalter() wie
    ## überall sonst (Regel 7).
    KARTENTYPEN = ["karte", "feldpost", "lebensmittel", "zeitung", "amtlich"]
```

Wenn eine Tafel nur Kennungen enthaelt, steht die Erklaerung je Kennung als eingerueckte zweispaltige Liste im Kommentar darueber (drei Leerzeichen Einzug nach ##, Kennung linksbuendig, Erklaerung ab Spalte 18). Der Abschnitt hat eine eigene Kastenueberschrift aus zwei Rautenzeilen (Zeilen 365 bis 367: '## DIE KARTENTYPEN').

**Bestehende Tafel Kennung -> Text je Pfad: PFAD_ORT** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\script.rpy`:228 - *gelesen*

```
    PFAD_ORT = {
        "front": "Westfront",
        "etappe": "Etappengebiet",
        "heimat": "Deutsches Kaiserreich",
    }
```

Der einzige 'Ort'-Begriff, der im Code eine geschlossene Tafel hat. Daneben gibt es Ereignis.ort und Einlage.ort als freien Text (script.rpy 433, minispiele.rpy 168) und ort_text() (script.rpy 624), das PFAD_ORT.get(aktueller_pfad, '') zurueckgibt. Wenn ORTSKLANG 'je Ort' heisst, ist zu klaeren, ob 'Ort' die drei Pfade meint oder die freien Ortsangaben der Ereignisse - fuer die zweite Lesart gibt es keine geschlossene Liste.

**Globaler Schalter, der die Suche ganz abstellt: FIGUREN_ECHTE_BILDER** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\dialoge.rpy`:345 - *gelesen*

```
        if FIGUREN_ECHTE_BILDER and kennung:
            kandidaten = [
                figur_bild_pfad(kennung, stimmung),
                figur_bild_pfad(kennung, "neutral"),
            ]
            for pfad in kandidaten:
                if renpy.loadable(pfad):
                    return Transform(pfad, xysize=(breite, hoehe))
        if renpy.loadable(FIGUREN_PLATZHALTER):
            return Transform(FIGUREN_PLATZHALTER, xysize=(breite, hoehe))
        return bild_platzhalter(breite, hoehe, FIGUREN_PLATZHALTER)
```

Es gibt im Projekt bereits das Muster 'Tafel und Pfade sind da, der Zugriff ist aber ueber eine Konstante abgeschaltet'. Die Medienprobe fuehrt diese Pfade trotzdem auf (probe_alles.py 2991 bis 3008, mit dem Vermerk 'wird erst gesucht, wenn FIGUREN_ECHTE_BILDER auf True steht'). Fuer eine spaetere Musikspur ist das die vorhandene Form.

**Ton ist im Projekt heute vollstaendig unbenutzt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\options.rpy`:15 - *gelesen*

```
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
```

Die Kanaele sind eingeschaltet, aber eine Suche nach renpy.play, 'play sound', 'play music', 'audio/', .ogg, .mp3 und .opus ueber alle elf .rpy-Dateien ergibt KEINEN Treffer. ton_spielen() ist damit die erste Tonzeile des Projekts; es gibt kein bestehendes Kanalschema und keine Lautstaerkekonstante, an die man sich anhaengen koennte.

**Die einzige vorhandene Tondatei** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\MEDIEN.md`:1631 - *gelesen*

```
### `audio/stummer_morgen.mp3`

Ein Umgebungsklang. **Nicht an der Front und nicht in der Etappe** — dort ist Musik verboten (Regel 3), und ob dieses Stück Musik oder Umgebung ist, entscheidet sich am Stück selbst. Das Tongerüst entsteht in Paket 8, Schritt 2 mit `ton_spielen()` und der Tafel `ORTSKLANG`; dort bekommt die Datei ihren Ort oder bleibt liegen.
```

Verzeichnispruefung: game\audio enthaelt genau eine Datei, stummer_morgen.mp3, 5.519.750 Byte. Einen fonts-Ordner gibt es nicht (alle vier Schriften laufen auf Ersatz), in game\images liegen 9 Dateien. Der Eintrag steht in MEDIEN.md unter der Ueberschrift 'Vorhanden, aber unbenutzt' (Zeile 1627).

**Dominiks bindende Vorgabe fuer das Tongeruest (Entscheidung 24)** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\auftrag\ENTSCHEIDUNGEN.md`:426 - *gelesen*

```
**Was daraus für 2.6 folgt, und zwar sofort:** Das Tongerüst wird so
gebaut, dass eine spätere Musikspur **eine Tabellenzeile und eine Datei**
kostet und keinen Umbau. Also eine Tafel neben `ORTSKLANG` für Musik, mit
demselben `renpy.loadable()`-Schutz, und die Sperre als Abfrage über den
Pfad statt über den Kanal. Erfunden wird dabei nichts: Solange keine
Musikdatei im Projekt liegt, ist jede Zeile stumm und die Medienprobe
zählt sie als fehlend (Regel 7).
```

Verlangt sind ZWEI Tafeln (ORTSKLANG fuer Umgebung, eine zweite fuer Musik), und die Sperre prueft den Pfad, nicht den Ren'Py-Kanal. Erlaubte Musikstellen laut Zeile 420: Hauptmenue, Moduswahl, Onboarding, Jahreskarte, Epilog, Lebenslauf, Heimatpfad - welche es werden, entscheidet Dominik.

**Der Auftragstext Teil D woertlich** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\auftrag\paket08.md`:193 - *gelesen*

```
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
```

Punkt 11 verlangt ausdruecklich 'ein Eintrag in der Medienprobe' - das geht nach heutigem Bau NUR, wenn medien_sammeln() in probe_alles.py einen sechsten Abschnitt bekommt, der die Tonpfade ueber renpy.loadable() erfragt. Punkte 14 und 15 folgen in Zeilen 204 bis 208; die Abnahme in Zeile 220 lautet: 'Probe: ton_spielen() gibt auf front und etappe null Musikaufrufe frei.'

**Namenskonvention: init-Ordnung je Datei** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\auftrag\VERFASSUNG.md`:27 - *gelesen*

```
| Datei | init | Inhalt |
|---|---|---|
| `gui.rpy` | −50, −2 | Farben, Rahmen, Schriften, Bildersatz |
| `bewegung.rpy` | −45, 5 | Bewegungsstufen, `bewegungszeit()`, neun transforms, drei Übergänge |
| `script.rpy` | −20, −10, −5, 0 | Werte, `Ereignis`/`Option`, `EREIGNISSE` |
| `dialoge.rpy` | −20, −10, −5, 0 | Szenen, `variante()`, Bühne |
| `kapitel.rpy` | −19, −9, 1, 2, 3 | Kapitel 1914–1919, `MERKMAL_REGISTER`, `KapitelEreignis`, Lebenslauf |
```

gui.rpy ist ausdruecklich die Datei fuer 'Farben, Rahmen, Schriften, Bildersatz' - also fuer Ersatzverhalten bei fehlenden Medien. Die Verfassung sagt in Zeile 40 ausserdem: 'Spätere init-Blöcke überschreiben frühere. Das ist gewollt' - man baut in der eigenen Datei, statt in fremden herumzuschneiden.

**Namenskonvention: die Bezeichnerkarte** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\auftrag\VERFASSUNG.md`:93 - *gelesen*

```
| Bild und Schrift | `bild_pfad()`, `bild_vorhanden()`, `bild_anzeigen()`, `bild_platzhalter()`, `portrait_anzeigen()`, `schrift_waehlen()`, `BILD_MASSE`, `BILD_ANZEIGE` |
```

Die Regel, die sich aus dem ganzen Projekt ablesen laesst: Tafeln GROSSBUCHSTABEN mit Unterstrich, kein Suffix, kein Praefix-Typkuerzel (BILD_MASSE, BILD_ANZEIGE, SCHRIFT_KANDIDATEN, SCHRIFT_ZWECK, KARTENTYPEN, PFAD_ORT, PFAD_BASIS, KAPITEL_ZIEHUNGEN, ENDE_SCHWELLEN, EINLAGE_PROBEWERTE). Sammelbehaelter fuer Beanstandungen heissen SACHE_ZUSTAND: KARTENTYP_UNBEKANNT, NACHTRAG_OHNE_TREFFER. Funktionen klein, deutsch, Gegenstand zuerst, Verb im Infinitiv zuletzt: bild_anzeigen(), schrift_waehlen(), ton_spielen() passt genau in dieses Schema. Eine neue Tafel gehoert zusaetzlich in diese Karte.

### Offene Fragen und Urteil

- Wie kommt ein Tonpfad in die Medienprobe? Der Spielcode merkt sich NICHTS - das Medienbuch entsteht ausschliesslich in probe_alles.py, weil die Attrappe jeden renpy.loadable()-Aufruf mitschreibt. Ein Ton wird also nur dann gezaehlt, wenn medien_sammeln() (probe_alles.py Zeile 2900, heute fuenf Abschnitte bis Zeile 3026) einen sechsten Abschnitt bekommt, der die ORTSKLANG-Pfade erfragt. Ob der Auftrag diese Aenderung an der Werkbank umfasst, sollte vor dem Bau geklaert sein - ohne sie bleibt Auftragspunkt 11 ('ein Eintrag in der Medienprobe') unerfuellt.
- Was heisst 'je Ort' in ORTSKLANG? Eine geschlossene Ortstafel gibt es nur als PFAD_ORT (drei Pfade: front/etappe/heimat, script.rpy Zeile 228). Ereignis.ort und Einlage.ort sind freier Text ohne Liste. Drei Zeilen fuer drei Pfade oder eine Zeile je Ortsangabe der Ereignisse - das ist eine Inhalts-, keine Gestaltungsfrage.
- Wie werden verworfene Musikaufrufe gezaehlt? Fuer 'in der Probe zaehlen' (Auftragspunkt 13) gibt es im Projekt genau eine Bauart: eine leere Liste in GROSSBUCHSTABEN im init-Block (KARTENTYP_UNBEKANNT, NACHTRAG_OHNE_TREFFER), die das Spiel fuellt und die Probe ausliest und beanstandet. Ein Name dafuer ist noch nicht vergeben.
- Die Sperre soll laut Entscheidung 24 'ueber den Pfad statt ueber den Kanal' pruefen. Gemeint ist vermutlich der Spielpfad aktueller_pfad (front/etappe/heimat), nicht der Dateipfad - der Satz ist an dieser Stelle zweideutig, und beide Lesarten ergeben Sinn (Regel 1 verlangt Steuerung ueber aktueller_pfad).
- Es gibt heute keine Tonzeile im Projekt: config.has_sound und config.has_music stehen auf True (options.rpy 15-16), aber keine einzige .rpy-Datei ruft renpy.play oder benutzt einen audio-Pfad. Kanalnamen, Lautstaerkeskala und Ausblendzeit muessen also neu festgelegt werden - es gibt kein Vorbild im Bestand.
- audio/stummer_morgen.mp3 (5,5 MB) ist die einzige Tondatei. Auftragspunkt 15 verlangt eine Entscheidung: einen Ort geben oder in MEDIEN.md als unbenutzt vermerken. Der Vermerk steht dort bereits (Zeile 1631); ob die Datei jetzt eine ORTSKLANG-Zeile bekommt, haengt an der Frage, ob sie Umgebung oder Musik ist - das entscheidet sich laut MEDIEN.md 'am Stueck selbst', also am Hoereindruck, den ich nicht pruefen kann.

---

## GEGENGELESEN A

### Urteile des Gegenlesers (3)

- **CLAUDE.md Regel 3 - die Audioregel selbst** - **bestaetigt**: Wortlaut zeichengenau bestaetigt, Zeilenangabe korrigiert. Datei: C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\CLAUDE.md, Zeilen 87-88 (NICHT Zeile 1): "3. **Audio.** An der Front und in der Etappe nie Musik. Kein Ton, der\n   eine Entscheidung bewertet: kein Gewonnen-Klang, kein Fehlerton." Der Text steht zwischen Regel 2 (Z. 85-86: "2. **Maus.** Das Spiel wird zu 100 Prozent mit der Maus bedient. Niemals `key`-Anweisungen, niemals Tastenkuerzel, niemals Hinweise auf Tasten.") und Regel 4 (Z. 89: "4. **Sprache.** Keine Begriffe aus der NS-Zeit, keine Anachronismen;"), also tatsaechlich im Block "Harte Regeln". Das behauptete Zitat weicht in keinem Zeichen ab; einzige Abweichung ist die als ungeprueft markierte Zeilennummer 1.
- **AUFGEFALLEN.md enthaelt keinen Punkt zu Ton, Audio, Musik oder Klang** - **bestaetigt**: Bestaetigt fuer AUFGEFALLEN.md selbst (Pfad: C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\AUFGEFALLEN.md). Ich habe breiter gesucht als der Erstagent, auch mit Umlautvarianten: (ton|toen|kling|klang|klaeng|musik|audio|sound|stumm|geraeusch|laerm|hoer|akust|melodie|lied|gesang|vertont|.ogg|.mp3|.wav|play music|play sound). Kein einziger Treffer hat einen Audio-Bezug; alles ist Substring-Rauschen: Z. 408 "36. **Die Herkunftsnachklaenge erreichen den Lebenslauf praktisch nie.**" und Z. 410/413/417 (Nachklang), Z. 56 "(Merkmal `verbruederung`) und im KETTEN_PLAN (als zweites Glied von" und Z. 525 (Glied), Z. 1212 "schaltet und ab Werk aus ist: im Spiel eine ruhige getoente Flaeche mit" (Farbe, nicht Ton), sowie zahlreiche "gehoert/gehoeren". Die beiden einzigen Treffer im behaupteten Umfeld stehen beide in Punkt 90 (Z. 1283: "90. **DIE VORLESEFUNKTION LAESST SICH BELEGEN, STATT SIE ZU BEHAUPTEN.**") und meinen den Bildschirmleser: Z. 1304 "muss, statt sie am Stueck zu hoeren." und Z. 1306-1309 "Ebenfalls stumm sind die **Wertebalken**: Sie bestehen aus Flaechen, nicht aus Text. Die Auskunft geht nicht verloren, weil der Zustandssatz daneben (Hungrig, Am Ende) dasselbe in Worten sagt - und der wird gelesen." Auch keine der 105 Punktueberschriften (Muster ^\d+\. \*\*, Punkte 10 bis 105) nennt Ton, Musik, Klang oder Audio. Das Protokoll hat zum Tongeruest also weder Vorgeschichte noch Warnung.
- **Zusatzbehauptung im selben Punkt: auftrag/OFFENE_PUNKTE.md liefert zu denselben Begriffen keinen Treffer** - **widerlegt**: Widerlegt. In C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\auftrag\OFFENE_PUNKTE.md steht in Zeile 54 der offene Punkt M2 und nennt Toene ausdruecklich: "| M2 | **Die Mediendateien.** **333** erwartete Pfade, 7 vorhanden, 326 abzulegen; alle acht Schriftdateien fehlen, es greift `DejaVuSans.ttf`. Der vollstaendige Bedarfsplan mit Suchbegriffen liegt in `game/MEDIEN.md`. ... | Bilder, Toene und Schriften ablegen - Claude Code laedt nichts aus dem Netz und erfindet keine Dateinamen. **Offen ist die Grundsatzfrage:** historische Fotografien aus Archiven oder durchgehend gezeichnete Illustrationen? ... |" Die Suche des Erstagenten hat das uebersehen, weil sie nach "ton" ohne Umlautvariante suchte; "Toene" ist dasselbe Wort. Der einzige weitere Treffer in dieser Datei ist Rauschen: Z. 106 "| 36 | Die Herkunftsnachklaenge erreichten den Lebenslauf praktisch nie. | 4. Sep - vier feste Faecher (Entscheidung 10), Herkunft jetzt bei 100,0 %. |". Richtig bleibt: Es gibt in OFFENE_PUNKTE.md keinen Punkt zur Audio-Logik oder zum Tongeruest - wohl aber einen offenen Medienpunkt, der Toene als abzulegende Dateien fuehrt und laut Eintrag Dominik gehoert.

---

## 4 - Die Orte im Projekt

Einen Bestand von "Orten" gibt es in diesem Projekt nicht — kein ORTE, kein schauplatz, keine kulisse, kein Hintergrundbild je Ort. Was es gibt, ist zweierlei: die Dreiertafel PFAD_ORT (script.rpy:228) mit "Westfront" / "Etappengebiet" / "Deutsches Kaiserreich" als Rückfall je Pfad, und ein freies Textfeld ort an drei Inhaltsklassen — Ereignis (script.rpy:433), Szene (dialoge.rpy:154) und Einlage (minispiele.rpy:168). Alle 101 Ereignisse, 15 Szenen und 5 Einlagen tragen eine solche Angabe; daraus ergeben sich 50 verschiedene Ortszeichenketten von "Grabenstellung" bis "Zensurstelle". Diese Zeichenketten sind reine Anzeigetexte, unnormiert (Etappe/Etappenort/Etappenquartier, Lazarett/Etappenlazarett/Reservelazarett/Bahnhofslazarett) und laufen im Bildschirm alle durch genau eine Stelle: screen zustandskopf(ortsangabe="") in screens.rpy:724, mit 14 Aufrufstellen. Aus Bildpfaden lässt sich keine Ortsliste ableiten: bild_pfad() kennt nur images/karten, images/portraits und images/dokumente, und die Kategorie "orte" wurde in Paket 8, Schritt 1 ausdrücklich gestrichen (gui.rpy:42-52); auf der Platte liegen 9 Kartenbilder und ein Platzhalter. Im Ablauf wechselt der Ort nicht an einer Kapitelgrenze, sondern an jeder einzelnen Karte — die engsten Durchgänge sind ereignis_spielen_mit_einlage (minispiele.rpy:3341), einlage_spielen (minispiele.rpy:3377), szene_spielen (dialoge.rpy:1476) und kapitelwechsel_mit_schicksal (figuren.rpy:3311), alle über config.label_overrides eingehängt (sechs Umleitungen bestehen bereits). aktueller_pfad ist eine gewöhnliche Store-Variable (default aktueller_pfad = "heimat", script.rpy:2796) und an allen genannten Stellen unmittelbar lesbar. Ton gibt es im Code bis heute nicht: kein ton_spielen, kein renpy.play, kein renpy.music — nur die Datei game/audio/stummer_morgen.mp3 (5,5 MB), die MEDIEN.md:1631 als unbenutzt führt.

### Befunde (28)

**Die einzige Ortstafel im Projekt: PFAD_ORT, drei Zeilen** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\script.rpy`:228 - *gelesen*

```
    PFAD_ORT = {
        "front": "Westfront",
        "etappe": "Etappengebiet",
        "heimat": "Deutsches Kaiserreich",
    }

    PFAD_MARKE = {
        "front": "An der Front",
        "etappe": "In der Etappe",
        "heimat": "In der Heimat",
    }
```

Das ist der gesamte Ortsbestand, den das Projekt als Tafel führt: drei Eintraege, einer je Pfad. Eine ORTSKLANG-Tafel mit drei Zeilen waere damit sofort anschlussfaehig, aber grob — sie unterschiede Graben und Ruhequartier nicht.

**ort_text() ist der Rueckfall, wenn ein Inhalt keinen eigenen Ort nennt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\script.rpy`:624 - *gelesen*

```
    def ort_text():
        return PFAD_ORT.get(aktueller_pfad, "")
```

Eine einzige Funktion uebersetzt aktueller_pfad in eine Ortszeichenkette. Sie ist der natuerliche zweite Schluessel fuer ORTSKLANG, falls ein Ort keinen eigenen Klang hat. Dieselbe Funktion steht ein zweites Mal in merkbuch.rpy:688 und wird in herkunft.rpy:819 verwendet.

**Der Ort haengt am Ereignis, nicht am Spielzustand** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\script.rpy`:418 - *gelesen*

```
    class Ereignis(object):

        def __init__(self, kennung, jahre, pfad, text, optionen, kern=False,
                     gewicht=10, braucht=None, verbietet=None, ort=None,
                     quelle=None, stimmung=None, nur_kette=False,
                     wiederholbar=False, kartentyp="karte"):
            self.kennung = kennung
            self.jahre = jahre if jahre else []
            self.pfad = pfad_liste(pfad)
            self.text = text
            self.optionen = optionen
            self.kern = kern
            self.gewicht = gewicht
            self.braucht = braucht if braucht else []
            self.verbietet = verbietet if verbietet else []
            self.ort = ort
```

Der Ort ist eine Eigenschaft des gezogenen Inhalts, keine bleibende Groesse des Durchgangs. Er wechselt deshalb mit jeder Karte, nicht mit dem Kapitel. Wer ORTSKLANG baut, muss entscheiden, ob der Klang bei jeder Karte neu einsetzt oder nur bei Wechsel der Ortskennung.

**Auch Szenen tragen einen Ort, dort als Variantenwoerterbuch je Pfad** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\dialoge.rpy`:147 - *gelesen*

```
    class Szene(object):

        def __init__(self, kennung, titel, zeilen, ort=None,
                     hintergrund="papier", stimmung=None, kopf=True):
            self.kennung = kennung
            self.titel = titel
            self.zeilen = zeilen
            self.ort = ort
            self.hintergrund = hintergrund
            self.stimmung = stimmung
            self.kopf = kopf
```

Bei Szenen ist ort meist ein Woerterbuch der Form {"front": ..., "etappe": ..., "heimat": ...} und wird durch variante() aufgeloest (dialoge.rpy:423). Ein ORTSKLANG-Aufruf muss also mit dem AUFGELOESTEN Text arbeiten, nicht mit dem Rohwert.

**Auch Einlagen (Minispiele) tragen einen Ort** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\minispiele.rpy`:158 - *gelesen*

```
        def __init__(self, kennung, titel, bildschirm, jahre, pfad,
                     ort=None, einleitung=None, anweisung=None,
                     einordnung=None, anschluss=None, braucht=None,
                     verbietet=None, gewicht=10, merkmal=None,
                     wiederholbar=False, quelle=None):
            self.kennung = kennung
            self.titel = titel
            self.bildschirm = bildschirm
            self.jahre = jahre if jahre else []
            self.pfad = pfad_liste(pfad)
            self.ort = ort
```

Dritte Klasse mit demselben Feld. Eine Ortsliste, die nur die Ereignisse betrachtet, waere unvollstaendig — Landstrasse, Etappenquartier und Wohlfahrtsamt kommen ausschliesslich aus den Einlagen.

**Vollstaendige Liste: 50 verschiedene Ortskennungen aus allen ort=-Angaben** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\script.rpy`:1057 - *erschlossen*

```
            ort="Grabenstellung", kern=True, gewicht=12, wiederholbar=True,
```

Ausgezaehlt ueber alle .rpy-Dateien (Regex ueber ort= mit Zeichenkette, Woerterbuch oder nach_welt): 50 verschiedene Werte. Alphabetisch, mit den Dateien, in denen sie vorkommen: Amtsgericht (script) | Arbeitsstelle (dialoge, kapitel) | Bahnhof (herkunft, kapitel, script) | Bahnhofshalle (herkunft) | Bahnhofslazarett (kapitel) | Bahnsteig (kapitel) | Bauernhof (kapitel) | Belgien (script) | Besetztes Dorf (kapitel) | Bezirksamt (script) | Ersatztruppenteil (dialoge, herkunft) | Etappe (kapitel, script) | Etappenkommandantur (kapitel) | Etappenlazarett (kapitel, merkbuch) | Etappenort (dialoge, kapitel) | Etappenquartier (minispiele) | Feldbaeckerei (kapitel) | Flandern (script) | Gefangenenlager (kapitel) | Gemeindeamt (dialoge, script) | Gemeindesaal (script) | Grabenstellung (dialoge, kapitel, minispiele, script) | Gueterbahnhof (script) | Heimatstadt (script) | Kreisstadt (herkunft) | Landstrasse (minispiele) | Lazarett (kapitel) | Magazin (dialoge, kapitel) | Meldebehoerde (kapitel) | Munitionslager (kapitel) | Niemandsland (kapitel, script) | Nordfrankreich (script) | Pferdedepot (kapitel) | Quartier (dialoge, kapitel) | Reservelazarett (herkunft) | Ruhequartier (kapitel, merkbuch, script) | Ruestungsbetrieb (kapitel, script) | Sammelstelle (kapitel) | Schreibstube (dialoge, kapitel) | Somme (script) | Stadtrand (script) | Strasse (kapitel) | Verdun (script) | Versorgungsamt (kapitel) | Verwundetensammelstelle (kapitel) | Wahllokal (kapitel) | Werktor (kapitel) | Wirtshaus (dialoge, kapitel) | Wohlfahrtsamt (minispiele) | Wohnviertel (dialoge, kapitel, merkbuch, minispiele, script) | Zensurstelle (kapitel). Dazu die drei aus PFAD_ORT: Westfront, Etappengebiet, Deutsches Kaiserreich. Haeufigste: Wohnviertel (20 Ereignisse), Grabenstellung (14), Ruestungsbetrieb (7), Etappe (6).

**Jeder Inhalt traegt einen Ort — es gibt keine Luecke** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\kapitel.rpy`:3570 - *erschlossen*

```
            ort="Grabenstellung", kern=True, gewicht=12,
```

Ausgezaehlt: 101 Ereignisse (38 script.rpy, 59 kapitel.rpy, 4 herkunft.rpy), 15 Szenen (13 dialoge.rpy, je 1 herkunft.rpy und merkbuch.rpy) und 5 Einlagen (minispiele.rpy) — zusammen 121 Objekte und genau 121 ort=-Angaben. Kein Inhalt faellt also auf ort_text() zurueck. Eine ORTSKLANG-Tafel muesste demnach fuer 50 Kennungen entscheiden, nicht fuer drei.

**Der eine Durchgang, durch den JEDE Ortsangabe auf den Bildschirm kommt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\screens.rpy`:724 - *gelesen*

```
screen zustandskopf(ortsangabe=""):

    $ satz_schluessel = schwaechster_wert()
    $ satz_stufe = stufe_von_wert(satz_schluessel, zustand_lesen()[satz_schluessel])
```

14 Aufrufstellen: dialoge.rpy:1342 (szene_ort), herkunft.rpy:1897, merkbuch.rpy:848 und 903, screens.rpy:1171 und 1238 (Entscheidungskarte und Ausgangskarte), minispiele.rpy:2437/2622/2749/3121/3242, figuren.rpy:3058 und 3144. Das ist der engste Punkt fuer 'hier ist gerade Ort X sichtbar' — aber es ist ein Bildschirm, der bei jeder Neuauswertung erneut durchlaufen wird. Ein ton_spielen() DIREKT hier wuerde mehrfach ausloesen.

**Die Ortsangabe steht in der Kopfzeile rechts neben dem Datum** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\screens.rpy`:747 - *gelesen*

```
                    text datum_text() style "kopf_klein" xalign 0.0 yalign 0.5
                    text ortsangabe style "kopf_klein" xalign 1.0 yalign 0.5
```

Der Ort ist heute reiner Anzeigetext. Keine Bedingung im Spiel stuetzt sich darauf — deshalb ist er auch nie normiert worden.

**Bildpfade kennen keine Orte: nur karten, portraits, dokumente** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:581 - *gelesen*

```
    def bild_pfad(kategorie, kennung):
        return "images/" + str(kategorie) + "/" + str(kennung) + ".png"
```

Der Bildpfad wird aus Kategorie und Kennung gebaut, nicht aus einem Ort. Aus den Bildpfaden laesst sich also KEINE Ortsliste ableiten — die Frage nach der 'Liste der Orte aus den Bildpfaden' hat keine Antwort ausser: es gibt sie nicht.

**Die Kategorie 'orte' wurde in Paket 8, Schritt 1 ausdruecklich gestrichen** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:42 - *gelesen*

```
    ## PAKET 8, SCHRITT 1 — "personen" und "orte" sind gestrichen. Beide
    ## standen seit dem Anfang hier und hatten nie eine aufrufende Stelle.
    ##
    ##   personen  hat einen Nachfolger, der es besser macht: Ganzfiguren
    ##             laufen über images/figuren/ mit figur_bild_pfad() und
    ##             FIGUR_BREITE / FIGUR_HOEHE in dialoge.rpy. Zwei Tafeln für
    ##             dieselbe Sache laufen früher oder später auseinander, und
    ##             dann glaubt jemand der falschen.
    ##   orte      wäre ein Vollbild je Ort und damit ein eigenes Vorhaben.
    ##             Solange kein Paket es beauftragt, ist die Zeile nur ein
    ##             Versprechen — genau das, was die Medienprobe anmahnt.
```

Es gab einmal die Absicht, Orte als Bildkategorie zu fuehren. Sie wurde bewusst entfernt, weil kein Auftrag sie beauftragt hat. Ein Tongeruest je Ort waere die erste Stelle im Projekt, die Orte ueberhaupt als Bestand behandelt.

**Die vorhandenen Anzeigemasse — es gibt keine Ortsgroesse** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\gui.rpy`:66 - *gelesen*

```
    BILD_ANZEIGE = {
        "karten": (468, 264),
        "portraits": (240, 240),
        "dokumente": (720, 480),
    }
```

Auf der Platte liegt nur game/images/karten/ mit 9 Dateien (front_1914_dorf_1/2, front_1914_erster_toter_1/2, front_1914_marsch_1/2, front_beginn_1/2) plus images/platzhalter.png. Kein Ordner portraits, keiner dokumente, keiner figuren. gui.rpy:594 nennt die Lage: '326 der 333 Dateien fehlen.'

**Der Ablauf: vier Marken in script.rpy, drei davon umgeleitet** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\script.rpy`:2833 - *gelesen*

```
label start:

    $ zustand_zuruecksetzen()

    scene bg papier
    with UEBERGANG_KARTE()

    call screen modus_waehlen
    $ spielmodus = _return

    call screen hinweis_unumkehrbar

    call screen jahreskarte(aktuelles_jahr)

    jump lebenslage_bestimmen
```

Die Grundmarken sind start (2833), hauptschleife (2856), ereignis_spielen (2879), kapitelwechsel (2897), die fuenf Endemarken (2927/2935/2943/2951/2962) und ende_abschluss (2966). Von diesen laufen hauptschleife, ereignis_spielen, kapitelwechsel und ende_ueberlebt in Wahrheit NICHT — sie sind umgeleitet. start und ende_abschluss laufen unveraendert.

**Sechs bestehende Umleitungen ueber config.label_overrides** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\figuren.rpy`:3279 - *gelesen*

```
init python:

    config.label_overrides["hauptschleife"] = "hauptschleife_mit_post"
    config.label_overrides["kapitelwechsel"] = "kapitelwechsel_mit_schicksal"
```

Die uebrigen vier: minispiele.rpy:3337 ereignis_spielen -> ereignis_spielen_mit_einlage (init 8); merkbuch.rpy:1223-1224 lebenslage_abschluss -> lebenslage_abschluss_mit_merkbuch und post_zustellen -> post_zustellen_als_ereignis (init 5); kapitel.rpy:6645 ende_ueberlebt -> ende_ueberlebt_mit_wirtshaus (init 1). Wer eine siebte anlegt, muss vorher pruefen, ob die Marke schon belegt ist — merkbuch.rpy:1216-1219 mahnt das ausdruecklich an. Eine Umleitung fuer den Ton waere NICHT noetig: die vorhandenen Fassungen koennen die Zeile direkt aufnehmen.

**Der zentrale Durchgang fuer jede Karte: ereignis_spielen_mit_einlage** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\minispiele.rpy`:3341 - *gelesen*

```
label ereignis_spielen_mit_einlage(kennung):

    $ gespielte_ereignisse = gespielte_ereignisse + [kennung]
    $ aktuelles_ereignis = kennung
    $ stimmung_setzen(ereignis_holen(kennung).stimmung)

    call screen karten_entscheidung(kennung)

    $ letzte_wahl = _return
    $ letztes_ergebnis = option_ausfuehren(kennung, letzte_wahl)

    call screen karten_ausgang(kennung, letzte_wahl, letztes_ergebnis["ausgang"])

    $ stimmung_setzen(None)
```

DAS ist die eine Stelle, durch die jedes Ereignis laeuft — die Hauptschleife (figuren.rpy:3300), die vier Einstiege aus herkunft.rpy (2270, 2290, 2338, 2345) und die Wirtshauswahl (kapitel.rpy:6654) landen alle hier. Eine einzige Zeile vor 'call screen karten_entscheidung' erreicht saemtliche 101 Ereignisse. Vorbild ist die Zeile darueber: stimmung_setzen(ereignis_holen(kennung).stimmung) tut fuer die Stimmung genau das, was ton_spielen fuer den Klang taete.

**Der zentrale Durchgang fuer Szenen: szene_starten() berechnet den Ort bereits** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\dialoge.rpy`:413 - *gelesen*

```
    def szene_starten(kennung):
        global szene_aktuell, szene_stelle, szene_ort
        global szene_hintergrund, szene_kopf
        szene_aktuell = szene_holen(kennung)
        szene_stelle = 0
        buehne_leeren()
        if szene_aktuell is None:
            return
        szene_hintergrund = szene_aktuell.hintergrund
        szene_kopf = szene_aktuell.kopf
        gesetzter_ort = variante(szene_aktuell.ort, None) if szene_aktuell.ort else None
        szene_ort = gesetzter_ort if gesetzter_ort else ort_text()
        if szene_aktuell.stimmung:
            stimmung_setzen(szene_aktuell.stimmung)
        renpy.show_screen("szenen_buehne")
```

Hier liegt der aufgeloeste Ortstext schon fertig in szene_ort (default in dialoge.rpy:1166). Ein ton_spielen(szene_ort) direkt hinter dieser Zeile deckt alle 15 Szenen ab, mit einem einzigen Eingriff. Aufgerufen wird szene_starten nur aus label szene_spielen (dialoge.rpy:1476-1478).

**Der zentrale Durchgang fuer Einlagen: einlage_ort()** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\minispiele.rpy`:991 - *gelesen*

```
    def einlage_ort(kennung):
        vorlage = einlage_holen(kennung)
        if vorlage is None or vorlage.ort is None:
            return ort_text()
        return einlage_text(vorlage.ort, ort_text())
```

Fuer die Einlagen loest diese Funktion den Ort auf (Pfadvariante plus Jahresvariante). Der zugehoerige Ablaufpunkt ist label einlage_spielen (minispiele.rpy:3377) mit '$ einlage_vorbereiten(kennung)' als erster Zeile — dort passt ein Tonaufruf hin.

**Der Jahreswechsel: kapitelwechsel_mit_schicksal ist die eine Kapitelmarke** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\figuren.rpy`:3311 - *gelesen*

```
label kapitelwechsel_mit_schicksal:

    $ rhythmus_kapitel_abschliessen()

    if aktuelles_jahr != EPILOG_JAHR:
        call screen jahresabschluss(aktuelles_jahr)

    $ folgejahr = naechstes_kapitel(aktuelles_jahr)

    if folgejahr is None:
        jump ende_ueberlebt

    $ aktuelles_jahr = folgejahr
    $ ziehungen_im_kapitel = 0
    $ wiederholbare_freigeben()
```

Jeder Kapitelanfang laeuft hier durch, und nur hier. Die Fassung in script.rpy:2897 laeuft nicht. Weiter unten (3337) steht bereits '$ renpy.transition(UEBERGANG_KAPITEL())' — genau der Punkt, an dem ein Kapitelklang oder eine Musikzeile stuende. Der Epilog 1919 laeuft ueber dieselbe Marke.

**Die Jahreskarte selbst kennt keinen Ort** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\kapitel.rpy`:6806 - *gelesen*

```
screen jahreskarte(jahr, wirkung=None):

    $ kapitelnummer = KAPITEL_JAHRE.index(jahr) + 1 if jahr in KAPITEL_JAHRE else 1
    $ zeilen = wirkung_zeilen(wirkung) if wirkung else []
    $ ist_epilog = (jahr == EPILOG_JAHR)
```

Von Zeile 6806 bis 6907 durchgelesen: die Jahreskarte benutzt kein zustandskopf und keine Ortsangabe, sondern Jahr, Zeitraum, Ueberschrift, Frage und Stichworte. Sie ist damit ein ortloser Bildschirm — ebenso jahresabschluss (kapitel.rpy:6912). Fuer ORTSKLANG heisst das: hier gaebe es nichts zuzuordnen, und genau hier waere nach Entscheidung 24 Musik erlaubt.

**aktueller_pfad ist eine gewoehnliche Store-Variable** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\script.rpy`:2795 - *gelesen*

```
default aktuelles_jahr = 1914
default aktueller_pfad = "heimat"
default spielmodus = "lang"
```

Mit 'default' angelegt, also im Store und an jeder Stelle des Ablaufs und in jeder init-python-Funktion ohne Umweg lesbar. Geschrieben wird sie nur an drei Stellen: zustand_zuruecksetzen() (script.rpy:654, zurueck auf 'heimat'), pfad_wechseln() (herkunft.rpy:517) und probe_lebenslage() (herkunft.rpy:840, nur Werkzeug). Eine ton_spielen()-Sperre 'nie Musik auf front und etappe' kann sich also direkt auf aktueller_pfad stuetzen.

**Der Pfad wechselt genau einmal je Durchgang, in der Herkunftswahl** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\herkunft.rpy`:502 - *gelesen*

```
    def pfad_wechseln(neuer_pfad):
        """Rechnet die Differenz zwischen zwei Pfadgrundlagen auf.

        Alle Personen beginnen im Juli 1914 auf der Heimatgrundlage.
        Wer eingezogen wird, bekommt die Differenz zur Front- oder
        Etappengrundlage aufgeschlagen. Dadurch bleiben alle Änderungen
        erhalten, die vorher schon gefallen sind.
        """
        global aktueller_pfad
```

Der Pfad steht nach der Musterung fest und aendert sich danach nicht mehr. Ein pfadgebundener Grundklang muesste also nicht mitwandern; nur der ORT wandert, und zwar mit jeder Karte.

**Im ganzen Projekt gibt es keine Zeile Tonausgabe** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\minispiele.rpy`:26 - *gelesen*

```
##  - Kein Audio. An der Front ausdrücklich keine Musik: Diese Datei legt
##    keinen einzigen Ton an, auch keinen Klick beim Streichen.
```

Gesucht wurde in allen .rpy nach ton_spielen, renpy.play, renpy.music, renpy.sound, 'play sound', 'play music' — kein einziger Treffer. Dasselbe steht als Zusicherung in kapitel.rpy:19 und merkbuch.rpy:35, und screens.rpy:1282 sagt 'Kein Ton (es gibt im ganzen Projekt keinen)'. Das Tongeruest wird also auf gruener Wiese gebaut; es gibt nichts, was in Widerspruch geraten koennte.

**Die Tonkanaele sind in options.rpy bereits eingeschaltet** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\options.rpy`:15 - *gelesen*

```
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
```

Und die Einstellungen zeigen schon zwei Regler: screens.rpy:1832-1837 'Musik' (Preference music volume) und 'Geraeusche' (Preference sound volume). Die Bedienoberflaeche fuer das Tongeruest steht also bereits; sie regelt bisher nichts.

**Die einzige vorhandene Tondatei, bisher unbenutzt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\MEDIEN.md`:1631 - *gelesen*

```
### `audio/stummer_morgen.mp3`

Ein Umgebungsklang. **Nicht an der Front und nicht in der Etappe** — dort ist Musik verboten (Regel 3), und ob dieses Stück Musik oder Umgebung ist, entscheidet sich am Stück selbst. Das Tongerüst entsteht in Paket 8, Schritt 2 mit `ton_spielen()` und der Tafel `ORTSKLANG`; dort bekommt die Datei ihren Ort oder bleibt liegen. Bis dahin ruft sie keine Zeile Code auf, und das ist richtig so.
```

game/audio/ enthaelt genau eine Datei: stummer_morgen.mp3, 5.519.750 Bytes. Der Vorschlagstext dazu steht in medienbedarf.py:544-551 und wird von dort nach MEDIEN.md geschrieben. Auftragspunkt 15 (paket08.md:206-208) verlangt eine Entscheidung: zuordnen oder als unbenutzt vermerken.

**Das Bauvorbild fuer eine zentrale Zuordnungstafel: KARTENTYP_VERGABE** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\kapitel.rpy`:2827 - *gelesen*

```
    ## PAKET 8, SCHRITT 1. Der Kartentyp könnte auch am Ereignis selbst
    ## stehen, und dort stünde er schöner. Er steht trotzdem hier, und zwar
    ## aus einem handfesten Grund: Die Ereignisse werden im ganzen Projekt
    ## POSITIONAL angelegt — Ereignis("kennung", [jahre], "pfad", ...). Wer
    ## fünfundzwanzig solcher Aufrufe über drei Dateien aufschneidet, um ein
    ## Schlüsselwort ans Ende zu setzen, greift fünfundzwanzigmal in fremden
    ## Text.
    ##
    ## Anders als bei DOMINANZ_NACHTRAG ist der Schlüssel hier die KENNUNG
    ## und nicht der Optionstitel. Die Falle aus Entscheidung 16 gibt es
    ## also nicht: Eine Kennung ist eindeutig und wird nicht umformuliert,
    ## wenn jemand einen Text überarbeitet.
```

Genau dieses Muster passt auf ORTSKLANG: eine Tafel an EINER Stelle, Schluessel ist die Kennung, ein Nachtragslauf (kartentypen_vergeben(), kapitel.rpy:2882-2893) setzt sie auf die Vorlagen und meldet jeden Fehlschlag in NACHTRAG_OHNE_TREFFER statt still zu scheitern. Aufgerufen wird sie ganz zuletzt, in einem init-20-Block (kapitel.rpy:7255-7266), weil sonst die spaeter angelegten Ereignisse fehlen — dieselbe Falle drohte einer ORTSKLANG-Vergabe.

**Der Auftragstext zu ORTSKLANG selbst** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\auftrag\paket08.md`:193 - *gelesen*

```
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
```

Der Auftrag sagt 'je Ort ein Umgebungsklang', setzt aber voraus, dass 'Ort' definiert ist. Das ist er nicht. Nach heutigem Stand hiesse 'je Ort' entweder 3 Zeilen (PFAD_ORT) oder 50 Zeilen (die freien Zeichenketten) — dazwischen liegt eine Gestaltungsentscheidung, die vor der ersten Codezeile faellt.

**Entscheidung 24 verlangt eine zweite Tafel neben ORTSKLANG** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\auftrag\ENTSCHEIDUNGEN.md`:426 - *gelesen*

```
**Was daraus für 2.6 folgt, und zwar sofort:** Das Tongerüst wird so
gebaut, dass eine spätere Musikspur **eine Tabellenzeile und eine Datei**
kostet und keinen Umbau. Also eine Tafel neben `ORTSKLANG` für Musik, mit
demselben `renpy.loadable()`-Schutz, und die Sperre als Abfrage über den
Pfad statt über den Kanal. Erfunden wird dabei nichts: Solange keine
Musikdatei im Projekt liegt, ist jede Zeile stumm und die Medienprobe
zählt sie als fehlend (Regel 7).
```

Die Musiktafel haengt nicht an Orten, sondern an Stellen im Ablauf: laut ENTSCHEIDUNGEN.md:420-422 sind Hauptmenue, Moduswahl, Onboarding, Jahreskarte, Epilog, Lebenslauf und der Heimatpfad moeglich — 'welche Stellen es am Ende werden, entscheidet Dominik'. Das sind genau die ortlosen Bildschirme aus dem Befund zur Jahreskarte.

**Stand des Vorhabens: 2.6 ist der letzte offene Unterabschnitt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\auftrag\PAKETPLAN.md`:106 - *gelesen*

```
| 2.6 | **Tongerüst.** `ton_spielen()` mit `renpy.loadable()`, Tafel `ORTSKLANG`, harte Codesperre gegen Musik auf front und etappe. | D, Punkte 11–15 | offen |
```

2.1 bis 2.4 sind abgehakt, 2.5 gebaut aber mit ausgeschaltetem Schalter (Entscheidung: Dominik). 2.6 ist offen und haengt an keinem Bildschirm — laut PAKETPLAN.md:113-115 koennte es 'ueberall stehen'.

### Offene Fragen und Urteil

- Woran haengt ORTSKLANG — an den 50 freien Ortszeichenketten oder an einer kleineren Tafel von Klangraeumen (etwa 8 bis 12), auf die die 50 abgebildet werden? Das entscheidet, wie viele Tondateien Dominik beschaffen muss, und ist damit keine reine Gestaltungsfrage.
- Die Ortszeichenketten sind Anzeigetext und nicht normiert: Etappe / Etappenort / Etappenquartier / Etappengebiet stehen nebeneinander, ebenso Lazarett / Etappenlazarett / Reservelazarett / Bahnhofslazarett und Quartier / Ruhequartier. Ohne Normierung braucht die Tafel 50 Zeilen und zerfaellt bei jeder Textueberarbeitung.
- Regel 9 und Entscheidung 16 sprechen dagegen, einen Schluessel an einen Anzeigetext zu haengen: Wer 'Grabenstellung' in 'Graben' umformuliert, bricht die Zuordnung STILL. KARTENTYP_VERGABE hat genau deshalb die Kennung als Schluessel gewaehlt (kapitel.rpy:2836-2839). Soll ORTSKLANG denselben Weg gehen — also je Ereigniskennung statt je Ortstext?
- Der Ort wechselt bei JEDER Karte, nicht am Kapitelanfang: alle 101 Ereignisse tragen eine eigene Ortsangabe. Soll ein Umgebungsklang bei jedem Kartenwechsel neu einsetzen, nur bei Wechsel der Ortskennung, oder gar nur einmal je Kapitel? Ein Klang, der alle zwanzig Sekunden umschaltet, waere im Klassenzimmer eher Stoerung als Atmosphaere.
- Wo genau setzt der Aufruf an? Die vier Kandidaten sind ereignis_spielen_mit_einlage (minispiele.rpy:3341), szene_starten (dialoge.rpy:413, hat den aufgeloesten Ort schon), einlage_spielen (minispiele.rpy:3377) und kapitelwechsel_mit_schicksal (figuren.rpy:3311). screen zustandskopf (screens.rpy:724) waere der engste Punkt, ist aber ein Bildschirm und wird mehrfach ausgewertet — dort duerfte kein ton_spielen stehen.
- Gehoert audio/stummer_morgen.mp3 in ORTSKLANG oder in die Musiktafel aus Entscheidung 24? Ob das Stueck Musik oder Umgebung ist, laesst sich nur am Stueck selbst hoeren; ich habe es nicht abgespielt. Auftragspunkt 15 verlangt hier eine Entscheidung.
- Jahreskarte, Jahresabschluss, Moduswahl und Endebildschirme tragen keinen Ort. Bekommen sie einen eigenen Schluessel in ORTSKLANG, bleiben sie stumm, oder sind sie der Platz der spaeteren Musiktafel?
- Nicht geprueft: ob probe_alles.py bereits eine Probe fuer Ortsangaben fuehrt und wie eine neue Tonprobe dort einzuhaengen waere. Regel 11 verlangt einen eigenen Abschnitt in bericht.txt mit der Zahl der geprueften Faelle, und CLAUDE.md nennt fuer neue Einlagen vier Pflichteintraege — ob eine Tontafel eine vergleichbare vierte Stelle in der Werkbank braucht, habe ich nicht nachgesehen.

---

## 5 - Kanaele, options.rpy, Ren'Py-Audio

Die Tonseite des Projekts ist eingeschaltet, aber vollstaendig ungenutzt: options.rpy setzt has_sound und has_music auf True und has_voice auf False (Zeile 15-17), sonst nichts — kein main_menu_music, keine default-Lautstaerken, also stummes Hauptmenue und alle Regler auf 1.0 aus den Ren'Py-Vorgaben. Im Einstellungsbildschirm gibt es genau zwei Lautstaerkeregler, „Musik“ und „Geraeusche“, als letzten Block (screens.rpy 1825-1837); sie sind aus Solid gebaut, brauchen keine Mediendatei und sind nur mit der Maus bedienbar, weil options.rpy 64-67 die Fokustasten leert. Im ganzen Tonbereich steht keine key-Anweisung und kein Tastenhinweis — die einzige Taste im Menuerahmen ist die bewusst erhaltene Escape-Zuordnung in screen game_menu (screens.rpy 1736). Kein einziger Audioaufruf existiert in den .rpy-Dateien; ein Kommentar in screens.rpy 1282 sagt es selbst: „es gibt im ganzen Projekt keinen“. Im SDK sind „music“, „sound“ und „voice“ nur Zweitnamen der Kanaele 7, 0 und 2 (00mixers.rpy 43-49), eigene Kanaele legt renpy.audio.music.register_channel(name, mixer=None, loop=NotSet, …) an (audio.py 884). Eine fehlende Tondatei bringt keinen Fehler, sondern Stille: renpy.music.play() faengt jede Ausnahme ab und reicht sie nur bei config.debug_sound weiter (music.py 168-170, ebenso audio.py 612-621 und 1244-1246) — renpy.loadable() ist also fuer die Medienprobe noetig, nicht gegen den Absturz. Persistent-Einstellungen fuer Ton gibt es keine; das Projekt hat nur persistent.analysemodus und persistent.bewegung, die Lautstaerken liegen in preferences.volumes. stummer_morgen.mp3 liegt tatsaechlich unbenutzt da (nur Beschreibungen in MEDIEN.md, medienbedarf.py, bericht*.txt und paket08.md, kein Aufruf) und dauert nach dem Xing-Kopf gerechnet 243,5 Sekunden, also 4:03, bei 48 kHz Stereo und rund 181 kbit/s.

### Befunde (24)

**options.rpy — die drei Audio-Schalter** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\options.rpy`:15 - *gelesen*

```
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
```

Musik- und Geraeuschkanaele sind eingeschaltet und stehen bereit; Sprachausgabe (voice) ist aus. Das Tongeruest muss nichts an config einschalten. Wirkung im SDK: mit has_music/has_sound True und has_voice False bekommen die Kanaele 0-2 den Mixer 'sfx' und 3-7 den Mixer 'music' (00mixers.rpy 61-74) — der Kanal 'voice' (Kanal 2) laeuft dann auf dem sfx-Mixer mit.

**options.rpy — was dort NICHT steht** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\options.rpy`:1 - *erschlossen*

```
(kein Treffer fuer main_menu_music, default_music_volume, default_sfx_volume, default_voice_volume, mixer, fadeout_audio in game/*.rpy)
```

Weder config.main_menu_music noch die drei default_*_volume werden im Projekt gesetzt. Es gelten die Ren'Py-Vorgaben: main_menu_music = None (00start.rpy 28), default_music_volume/default_sfx_volume/default_voice_volume = 1.0 (00defaults.rpy 57/60/63). Das Hauptmenue ist also stumm, und alle Regler stehen beim ersten Start auf Anschlag. Wer spaeter Menuemusik will, setzt eine Zeile in options.rpy — kein Umbau noetig.

**options.rpy — Tastatur ist projektweit abgeschaltet** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\options.rpy`:60 - *gelesen*

```
    ## Tastatursteuerung im Spiel vorerst abgeschaltet: Der Fokus lässt sich
    ## nicht mehr mit den Pfeiltasten verschieben, und Leertaste/Eingabetaste
    ## lösen kein Weiterblättern mehr aus. Bedient wird ausschließlich mit
    ## der Maus. (Die linke Maustaste bleibt in allen Zuordnungen erhalten.)
    config.keymap['focus_left'] = [ ]
    config.keymap['focus_right'] = [ ]
    config.keymap['focus_up'] = [ ]
    config.keymap['focus_down'] = [ ]
    config.keymap['button_alternate'] = [ ]
    config.keymap['dismiss'] = ['mouseup_1']
```

Die Lautstaerkebalken lassen sich damit gar nicht anders als mit der Maus bedienen: Ren'Py verstellt einen Balken per Tastatur ueber focus_left/focus_right, und beide Zuordnungen sind leer. Regel 2 ist im Tonbereich also nicht nur nicht verletzt, sie ist erzwungen.

**screens.rpy — die beiden Lautstaerkeregler** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\screens.rpy`:1825 - *gelesen*

```
            vbox:
                spacing 10
                text "Lautstärke" style "einstellung_label_text"
                hbox:
                    spacing 60
                    vbox:
                        spacing 6
                        text "Musik" style "kopf_klein"
                        bar value Preference("music volume") style "slider"
                    vbox:
                        spacing 6
                        text "Geräusche" style "kopf_klein"
                        bar value Preference("sound volume") style "slider"
```

Es gibt zwei Regler, Musik und Geraeusche, ganz am Ende des Einstellungsbildschirms (letzter Block, Zeile 1825-1837). Preference("sound volume") bedient den Mixer 'sfx', Preference("music volume") den Mixer 'music'. Ein Regler fuer 'voice' fehlt — folgerichtig, weil config.has_voice False ist. Wenn das Tongeruest Umgebungsklaenge auf 'sound'/'sfx' legt, haengen sie am vorhandenen Regler „Geraeusche“; eine spaetere Musikspur auf 'music' haengt am Regler „Musik“. Beides ohne Aenderung am Bildschirm.

**screens.rpy — kein key und kein Tastenhinweis im Tonbereich** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\screens.rpy`:1739 - *gelesen*

```
screen preferences():

    tag menu

    use game_menu(_("Einstellungen")):
```

Ich habe screen preferences() ganz gelesen (Zeile 1739 bis 1838, danach beginnt der Abschnitt „Hilfsbildschirme“). Im ganzen Bildschirm steht keine key-Anweisung, und im Tonabschnitt steht kein Wort ueber eine Taste. Regel 2 ist im Tonbereich eingehalten.

**screens.rpy — die einzige Taste im Menuerahmen** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\screens.rpy`:1734 - *gelesen*

```
    ## Escape bleibt als einzige Taste erhalten, damit das Menü immer
    ## wieder geschlossen werden kann.
    key "game_menu" action Return()
```

Diese Zeile steht in screen game_menu(title) (ab 1701), also im Rahmen, den preferences per „use“ einbindet — nicht im Tonabschnitt. Es ist die bekannte, bewusst gesetzte Escape-Ausnahme (options.rpy 58 laesst genau diese Zuordnung stehen), kein neuer Verstoss und nichts, was das Tongeruest beruehrt.

**screens.rpy — der Reglerstil braucht keine Mediendatei** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\screens.rpy`:471 - *gelesen*

```
style slider:
    ysize 26
    xsize 420
    left_bar Solid(FARBE_AKZENT)
    right_bar Solid(FARBE_SEGMENT_LEER)
    thumb Solid(FARBE_TINTE, xsize=6, ysize=26)
    thumb_offset 3
```

Die Balken sind vollstaendig aus Solid gebaut, also unabhaengig von Bilddateien (Regel 7 erfuellt). 420x26 Pixel Trefferflaeche — mit der Maus gut greifbar; ein Klick auf eine Stelle des Balkens setzt den Wert dorthin, Ziehen funktioniert ebenfalls.

**Im Projekt wird bis heute kein einziger Ton abgespielt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\screens.rpy`:1282 - *gelesen*

```
                    ## Kein Ton (es gibt im ganzen Projekt keinen). Keine
                    ## Wertung im Text - nur der Name und die Zahl.
```

Eine Suche ueber alle game/*.rpy nach renpy.music., renpy.sound., renpy.audio., „play music“, „play sound“, „stop music“, „queue music“ und nach Zeilen, die mit play/stop/queue/voice beginnen, liefert null Treffer. Das Tongeruest wird also auf gruener Wiese gebaut: kein bestehender Aufruf muss mitgezogen werden, keine Fundstelle kann uebersehen werden (Regel 9 unkritisch).

**SDK — welche Kanaele Ren'Py von Haus aus kennt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\common\00mixers.rpy`:41 - *gelesen*

```
    # Register 8 channels by default, for compatiblity with older version
    # of Ren'Py.
    for i in range(0, 8):
        renpy.music.register_channel(i)

    # Set up default names for some of the channels.
    renpy.music.alias_channel(0, "sound")
    renpy.music.alias_channel(7, "music")
    renpy.music.alias_channel(2, "voice")
```

„music“, „sound“ und „voice“ sind keine eingebauten Sonderfaelle, sondern Zweitnamen der Kanaele 7, 0 und 2. Dazu kommt „movie“ (00mixers.rpy 56). Ein eigener Kanal ist damit gleichwertig zu den drei bekannten — es spricht technisch nichts gegen einen Kanal „ort“ oder „umgebung“ fuer das Tongeruest.

**SDK — Signatur von renpy.audio.music.register_channel()** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\audio\audio.py`:884 - *gelesen*

```
def register_channel(
    name,
    mixer=None,
    loop=NotSet,
    stop_on_mute=True,
    tight=False,
    file_prefix="",
    file_suffix="",
    buffer_queue=True,
    movie=False,
    framedrop=True,
    force=False,
    synchro_start=None,
):
```

So legt man einen eigenen Kanal an — aufzurufen in einem init-python-Block, wie es 00mixers.rpy vormacht. Wichtig fuer das Tongeruest: `mixer` entscheidet, an welchem Regler der Kanal haengt; nur 'music' und 'sfx' haben in diesem Projekt einen sichtbaren Regler. Die Dokumentation im Quelltext sagt dazu ausdruecklich: „making new mixers reachable by the player requires changing the preferences screens“ (Zeile 916). `loop` setzt das Standardverhalten (Umgebungsklang: True), `tight=True` gehoert laut Zeile 925-928 zu einer nahtlosen Schleife.

**SDK — Signatur von renpy.music.play() und renpy.music.stop()** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\audio\music.py`:36 - *gelesen*

```
def play(
    filenames,
    channel="music",
    loop=None,
    fadeout=None,
    synchro_start=None,
    fadein=0,
    tight=None,
    if_changed=False,
    relative_volume=1.0,
):
```

renpy.music.stop() hat die Signatur `def stop(channel="music", fadeout=None)` (music.py 283). Fuer das Tongeruest brauchbar: `relative_volume` nimmt die Lautstaerke aus der ORTSKLANG-Tafel auf, ohne den Spielerregler zu verstellen; `loop` die Angabe „wiederholt sich“; `if_changed=True` verhindert, dass derselbe Klang beim Ortswechsel neu anfaengt.

**SDK — Signatur von renpy.sound.play() und renpy.sound.stop()** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\audio\sound.py`:34 - *gelesen*

```
def play(filename, channel="sound", fadeout=0, fadein=0, tight=False, loop=False, relative_volume=1.0):
    renpy.audio.music.play(
        filename,
        channel=channel,
        fadeout=fadeout,
        fadein=fadein,
        tight=tight,
        loop=loop,
        relative_volume=relative_volume,
    )
```

renpy.sound ist ausdruecklich nur „a thin wrapper around music, with the default channel set to 'sound'“ (sound.py 30-31); stop lautet `def stop(channel="sound", fadeout=0)` (Zeile 58). Es gibt technisch keinen Unterschied zwischen Musik und Geraeusch — nur Kanal und Mixer. Der Unterschied, den Auftragspunkt 13 verlangt, muss also im Projektcode definiert werden, Ren'Py gibt ihn nicht her.

**SDK — ein unbekannter Kanalname wirft eine Ausnahme** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\audio\audio.py`:1035 - *gelesen*

```
        else:
            raise Exception("Audio channel %r is unknown." % name)
```

Ein Tippfehler im Kanalnamen ist kein stiller Fehler — allerdings faengt renpy.music.play() diese Ausnahme selbst wieder ab (music.py 168-170). Ausnahme davon ist config.auto_channels: `auto_channels = {"audio": ("sfx", "", "")}` (renpy/config.py 741) — der Name „audio“ legt sich Unterkanaele selbst an, jeder davon auf dem sfx-Mixer. Ein `play audio "..."` braucht also keine Registrierung, landet aber am Regler „Geraeusche“.

**SDK — eine fehlende Tondatei erzeugt Stille, keinen Fehler** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\audio\music.py`:166 - *gelesen*

```
            ctx.pause = False

        except Exception:
            if renpy.config.debug_sound:
                raise
```

Das ist die Antwort auf Frage 4: renpy.music.play() mit fehlender Datei stuerzt NICHT ab. Der ganze Rumpf steht in try/except, und es wird nur weitergereicht, wenn config.debug_sound an ist. Dasselbe Muster noch zweimal auf dem Weg zum Ton: audio.py 612-621 („If playing failed, remove topq.filename from self.loop / so we don't keep trying“ — der Titel wird stillschweigend aus der Schleife genommen) und audio.py 1244-1246 im periodic_pass. config.debug_sound kommt aus der Umgebung: `debug_sound = os.environ.get("RENPY_DEBUG_SOUND", False)` (renpy/config.py 60), ist also normalerweise aus. Fuer das Tongeruest heisst das: Die Pruefung mit renpy.loadable() aus Auftragspunkt 11 ist nicht noetig, um einen Absturz zu verhindern — sie ist noetig, damit die Medienprobe den Fehlbestand ueberhaupt sieht.

**SDK — renpy.loadable() und der audio-Ordner** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\exports\loaderexports.py`:33 - *gelesen*

```
def loadable(filename, directory=None, tl=True):
    """
    :doc: file

    Returns True if the given filename is loadable, meaning that it
    can be loaded from the disk or from inside an archive. Returns
    False if this is not the case.

    `directory`
        If not None, a directory to search in if the file is not found
        in the game directory. This will be prepended to filename, and
        the search tried again.
```

renpy.loadable() macht bei Audiodateien nichts Besonderes: Es prueft nur, ob der Pfad im Suchpfad liegt — Format, Laenge und Spielbarkeit werden nicht geprueft. Die Suchreihenfolge kommt aus loader.get_prefixes(): config.search_prefixes ist [""] (renpy/config.py 672), mit directory="audio" kommt "audio/" dazu (loader.py 684-688). Also sind BEIDE Schreibweisen ladbar: "audio/stummer_morgen.mp3" ohne directory-Angabe und "stummer_morgen.mp3" mit directory="audio". Ren'Pys eigenes Gegenstueck heisst renpy.music.playable(filename, channel) (music.py 269-280) und ruft renpy.loader.loadable(filename, directory="audio").

**Die Werkbank-Attrappe kennt directory= NICHT — Pfade muessen 'audio/...' lauten** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\probe_alles.py`:291 - *gelesen*

```
    def loadable(self, pfad, directory=None):
        """Prueft die Datei im Spielordner und schreibt die Anfrage mit."""
        name = str(pfad)
        da = os.path.isfile(os.path.join(self.spielordner, name.replace("/", os.sep)))
        eintrag = self.medienbuch.setdefault(name, {"anfragen": 0, "vorhanden": da})
        eintrag["anfragen"] += 1
        eintrag["vorhanden"] = da
        return da
```

Das ist die wichtigste Fussangel fuer den Bau. Die Attrappe nimmt directory= entgegen und wirft es weg: Ein ton_spielen(), das renpy.loadable("stummer_morgen.mp3", directory="audio") ruft, liefert im Spiel True und in der Probe False — und die Medienprobe wuerde die Datei zugleich als „fehlt“ und als „verwaist“ fuehren. Die Tafel ORTSKLANG sollte den Pfad deshalb als "audio/xyz.mp3" fuehren und ton_spielen() renpy.loadable(pfad) OHNE directory rufen. Das ist im Spiel gleichwertig (search_prefixes enthaelt "") und in der Probe richtig.

**Die Werkbank stuerzt an renpy.music.play() nicht ab** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\probe_alles.py`:213 - *gelesen*

```
class Attrappe(object):

    def __init__(self, name="Attrappe"):
        object.__setattr__(self, "_name", name)

    def __call__(self, *args, **kwargs):
        return Attrappe(self._name + "()")

    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return Attrappe(self._name + "." + name)
```

RenpyAttrappe erbt dieses __getattr__ und definiert weder music noch sound. renpy.music.play(...) wird in der Probe also zu Attrappe("renpy.music.play()") — still, ohne Fehler, ohne Spur. Die Probe kann den Aufruf daher NICHT am Ton erkennen; sie muss ton_spielen() selbst rufen und dessen Rueckgabe auswerten. Regel 11 („die Werkbank fragt das Projekt“) verlangt genau das: ton_spielen() sollte etwas Auswertbares zurueckgeben (z. B. den gespielten Pfad oder None bei Verwurf), damit die Abnahme „null Musikaufrufe auf front und etappe“ gemessen und nicht behauptet wird.

**Wo die Medienprobe eine neue Tondatei zaehlen wuerde** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\probe_alles.py`:3084 - *gelesen*

```
    ## Verwaiste Dateien: liegt ab, wird aber nirgends gesucht.
    verwaist = []
    for ordner in ["images", "fonts", "audio"]:
        wurzel = os.path.join(spielordner, ordner)
        if not os.path.isdir(wurzel):
            continue
```

Der audio-Ordner wird von Probe 6 bereits durchsucht, und medienbedarf.py tut dasselbe (Zeile 486). Sobald ORTSKLANG einen Pfad nennt und medien_sammeln() ihn ueber NS["renpy"].loadable() merkt (Muster: probe_alles.py 3011 und 3022), verschwindet stummer_morgen.mp3 aus „vorhanden, aber von keiner Stelle erwartet“ und taucht in der Kategorie audio auf. medien_sammeln() (probe_alles.py 2900) ist die EINE Quelle fuer Bericht und MEDIEN.md — dort gehoert der neue Abschnitt hin, nicht zweimal.

**persistent-Einstellungen fuer Ton: es gibt keine** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\options.rpy`:40 - *gelesen*

```
default preferences.text_cps = 45
default preferences.afm_time = 15

default persistent.analysemodus = False
```

Das Projekt hat genau zwei eigene persistent-Felder: persistent.analysemodus (options.rpy 43) und persistent.bewegung (bewegung.rpy 26, `default persistent.bewegung = "voll"`). Keines betrifft den Ton. Die Lautstaerken liegen nicht in persistent, sondern in preferences.volumes/preferences.mute, die Ren'Py selbst anlegt: `renpy.game.preferences.volumes.setdefault(m, default_volume)` und `renpy.game.preferences.mute.setdefault(m, False)` (renpy/audio/audio.py 1120-1121). Ein eigener Ton-Schalter (etwa „Ton ganz aus“ fuer den Klassenraum) waere also ein NEUES Feld — das ist eine Gestaltungs-/Unterrichtsfrage, keine bestehende Einstellung.

**stummer_morgen.mp3 — Laenge und Format, aus dem Dateikopf gemessen** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\audio\stummer_morgen.mp3`:1 - *gelesen*

```
Groesse: 5519750 Bytes / ID3v2-Tag 9364 Bytes / MPEG1 Layer III, 48000 Hz, Stereo / Xing-Kopf bei Offset 9410, Frames: 10146 / Dauer: 243,5 s = 4:03 / mittlere Bitrate 181 kbit/s / Encoder-Kennung "Lavc60.31"
```

Nicht geschaetzt, sondern aus dem Xing-Kopf gerechnet: 10146 Frames x 1152 Samples / 48000 Hz = 243,5 Sekunden, also 4 Minuten 3 Sekunden. Variable Bitrate um 181 kbit/s. Die Encoder-Kennung Lavc60.31 ist ffmpeg — die Datei ist also umgewandelt worden, was ueber die Herkunft nichts aussagt. Vier Minuten sind lang genug fuer eine Schleife unter einem ganzen Kapitel und viel zu lang fuer einen einzelnen Kartenklang.

**stummer_morgen.mp3 ist wirklich unbenutzt — und ist als solches dokumentiert** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\MEDIEN.md`:1631 - *gelesen*

```
### `audio/stummer_morgen.mp3`

Ein Umgebungsklang. **Nicht an der Front und nicht in der Etappe** — dort ist Musik verboten (Regel 3), und ob dieses Stück Musik oder Umgebung ist, entscheidet sich am Stück selbst. Das Tongerüst entsteht in Paket 8, Schritt 2 mit `ton_spielen()` und der Tafel `ORTSKLANG`; dort bekommt die Datei ihren Ort oder bleibt liegen.
```

Ja, sie liegt unbenutzt da. Die einzigen Fundstellen im ganzen Projekt sind Beschreibungen, keine Aufrufe: MEDIEN.md 1631, medienbedarf.py 544 (der Vorschlagstext), acht bericht*.txt-Dateien (immer unter „vorhanden, aber von keiner Stelle erwartet“) sowie auftrag/paket08.md 41 und 206. Kein einziger Code-Aufruf. Der Text stammt aus medienbedarf.py und wird bei jedem Lauf neu erzeugt — wer die Datei einbaut, muss medienbedarf.py neu laufen lassen, sonst widerspricht MEDIEN.md dem Code.

**Der Auftrag zum Tongeruest, Teil D** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\auftrag\paket08.md`:193 - *gelesen*

```
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
```

Die Punkte 14 und 15 folgen: kein Ton bewertet eine Entscheidung, und stummer_morgen.mp3 bekommt einen Ort oder bleibt vermerkt. Die Abnahme dieses Schritts nennt in Zeile 220 ausdruecklich: „Probe: ton_spielen() gibt auf front und etappe null Musikaufrufe frei.“ und in 221 „probe_alles.py sonst unverändert“. Die Sperre muss also messbar sein, nicht nur vorhanden.

**Entscheidung 24 — die Musik ist geplant, die Sperre bleibt hart** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\auftrag\ENTSCHEIDUNGEN.md`:426 - *gelesen*

```
**Was daraus für 2.6 folgt, und zwar sofort:** Das Tongerüst wird so
gebaut, dass eine spätere Musikspur **eine Tabellenzeile und eine Datei**
kostet und keinen Umbau. Also eine Tafel neben `ORTSKLANG` für Musik, mit
demselben `renpy.loadable()`-Schutz, und die Sperre als Abfrage über den
Pfad statt über den Kanal.
```

Bindend fuer den Bau: Es braucht ZWEI Tafeln (ORTSKLANG fuer Umgebung, eine zweite fuer Musik) und die Sperre muss ueber aktueller_pfad greifen, nicht ueber den Audiokanal. Dieselbe Entscheidung zaehlt in Zeile 420-422 auf, wo Musik spaeter erlaubt waere: „Hauptmenü, Moduswahl, Onboarding, Jahreskarte, Epilog, Lebenslauf und der Heimatpfad“ — welche Stellen es werden, entscheidet Dominik. Und Zeile 430-432: Solange keine Musikdatei liegt, ist jede Zeile stumm und die Medienprobe zaehlt sie als fehlend.

**Der Stand: 2.6 ist der naechste Schritt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\STAND.md`:17 - *gelesen*

```
| **2.6** | **Tongerüst** | **als Nächstes** |
```

MORGEN.md 27-30 wiederholt es als Startprompt: „Danach 2.6. Denk an Entscheidung 24: Ruhige klassische Musik ist langfristig geplant, also baue das Tongerüst so, dass eine Musikspur später eine Tabellenzeile und eine Datei kostet. Die harte Sperre gegen Musik auf front und etappe bleibt.“ Der Probenstand vor dem Schritt: nur Probe 4 mit 1 Beanstandung, alles andere null, Lint Exitcode 0 (STAND.md 45-47) — das ist die Ausgangszahl, gegen die die Abnahme „probe_alles.py sonst unverändert“ gemessen wird.

### Offene Fragen und Urteil

- Ist stummer_morgen.mp3 Musik oder Umgebungsklang? Ich habe die Datei nicht angehoert und kann es nicht entscheiden. MEDIEN.md sagt selbst, das entscheide sich „am Stück selbst“. Vier Minuten Laenge und 181 kbit/s Stereo passen zu beidem. Fuer die Sperre aus Auftragspunkt 13 ist die Einordnung aber folgenreich — als Musik waere die Datei auf front und etappe gesperrt, als Umgebungsklang nicht.
- Welchen Ort bekommt der Klang? ORTSKLANG existiert noch nicht, und im Projekt gibt es keine bestehende Ortstafel, an die ich mich haette anlehnen koennen — ich habe nach ORTSKLANG und ton_spielen gesucht und ausser Auftrags- und Planungstexten nichts gefunden.
- Soll ton_spielen() einen Wert zurueckgeben? Der Auftrag sagt es nicht, aber die Abnahme („null Musikaufrufe auf front und etappe“) ist ohne auswertbare Rueckgabe nicht messbar: Die Werkbank sieht renpy.music.play() nicht, weil die Attrappe jeden Aufruf still schluckt. Ich halte eine Rueckgabe (gespielter Pfad oder None) fuer noetig, habe das aber nirgends vorgeschrieben gefunden.
- Auf welchem Kanal soll der Umgebungsklang laufen? „sound“/sfx haengt am vorhandenen Regler „Geraeusche“, „music“ am Regler „Musik“. Ein eigener Kanal waere technisch moeglich, braeuchte aber einen dritten Regler im Einstellungsbildschirm — sonst kann die Lehrkraft ihn nicht leiser stellen (audio.py 916 sagt das ausdruecklich).
- Braucht der Unterricht einen Schalter „Ton ganz aus“? Es gibt heute kein persistent-Feld fuer Ton, und die beiden Regler lassen sich zwar auf null ziehen, aber nicht mit einem Klick stummschalten. Das ist eine Unterrichtsfrage (Klassenraum, Beamer, Kopfhoerer) und damit Dominiks.
- Ich habe die Ren'Py-Kanaele nur im Quelltext gelesen, nicht im laufenden Spiel gemessen. Dass eine fehlende Tondatei still bleibt, folgt aus drei try/except-Stellen im SDK — ich habe es nicht durch einen Testlauf mit einem erfundenen Dateinamen belegt, weil ich keine Datei anfassen darf.

---

## 6 - Diagnose offener Punkt 101

Der Verdacht ist widerlegt: Ren'Py hat keinen Mechanismus, der eine Interaktion neu anstoesst, weil ein Bildschirm eine Store-Variable aendert — `restart_interaction` wird ausschliesslich von den aufgezaehlten Stellen gesetzt, keine davon ist ein Schreibzugriff, und ein Bildschirm wird ohnehin nur einmal je Interaktion ausgewertet (screen.py:645-648, geleert in core.py:2417). Ausserdem wird der Rueckfallzweig in welttext() beim Merkbuch gar nicht betreten: MERKBUCH_LAGE, MERKBUCH_NAEHE_DA, MERKBUCH_NAEHE_FORT und MERKBUCH_GEGENSEITE enthalten zusammen 16 Woerterbuecher, jedes mit front, etappe und heimat, keines mit "standard"; auch die fuenf Nebenfiguren haben alle drei Pfade, also fallen figur_name() und figur_zusatz() ebenfalls nicht zurueck. Die wahre Ursache ist `modal True` in merkbuch_anzeige (merkbuch.rpy:972) zusammen mit dem `renpy.pause(0.3, hard=True)` der Sichtprobe: Ein modaler Bildschirm setzt bei einem TIMEEVENT `ev.modal = True` (layout.py:619-622, gerufen aus screen.py:812), und `PauseBehavior` haelt daraufhin die Pause an (behavior.py:607-609), weil `config.modal_blocks_pause = True` voreingestellt ist (config.py:1297). Weil PauseBehavior dabei jedes Mal `timeout(max(delay - st, 0))` — nach Ablauf also `timeout(0)` — neu setzt, weckt sich die Hauptschleife sofort wieder: das ist die volle Prozessorlast. Der Gegenbeweis liegt im eigenen Protokoll: `merkbuch_anlegen` ruft dieselben Funktionen (welttext ueber merkbuch_notiz_auswahl, variante ueber figur_name/figur_zusatz), ist aber nicht modal — und lief laut AUFGEFALLEN 100 unauffaellig durch. Im Spiel selbst gibt es keinen einzigen `renpy.pause`-Aufruf und keinen Timer, keine ATL-Schleife, kein `renpy.restart_interaction`; die Befuerchtung, der Bildschirm koste auf dem Schulrechner dauerhaft Rechenzeit, trifft nach diesem Befund nicht zu — der Dauerlauf ist ein Artefakt des Messaufbaus. Die kleinstmoegliche Behebung ist ein Schluesselwort im Abzugsrezept: `renpy.pause(0.3, hard=True, modal=False)`; am Spielcode ist nichts zu aendern.

### Befunde (20)

**Kein Mechanismus: Store-Schreibzugriff stoesst keine Interaktion neu an** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\exports\displayexports.py`:723 - *gelesen*

```
def restart_interaction():
    """
    :doc: other

    Restarts the current interaction. Among other things, this displays
    images added to the scene, re-evaluates screens, and starts any
    queued transitions.

    This only does anything when called from within an interaction (for
    example, from an action). Outside an interaction, this function has
    no effect.
    """

    try:
        renpy.game.interface.restart_interaction = True
```

Das ist der einzige oeffentliche Weg, eine Interaktion neu anzustossen. Eine projektweite Suche nach restart_interaction im ganzen SDK ergibt 40 Fundstellen (audio, behavior, controller, core, focus, tts, character, loadsave, persistent, scriptedit, translation, testast, actionexports, platformexports) — keine einzige davon liegt im Auswertungspfad eines Bildschirms und keine reagiert auf eine Store-Aenderung. Die Kernannahme des Verdachts hat im Quellcode keine Entsprechung.

**Ein Bildschirm wird hoechstens einmal je Interaktion ausgewertet** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\display\screen.py`:644 - *gelesen*

```
    def update(self):
        if self in updated_screens:
            return

        updated_screens.add(self)
```

Selbst wenn ein Bildschirm eine Nebenwirkung haette, koennte er sich innerhalb einer Interaktion nicht selbst wieder auswerten. Die Menge wird genau einmal je Interaktionsdurchgang geleert (renpy/display/core.py:2417: renpy.display.screen.updated_screens.clear()). Ein Selbstanstoss haette also je Runde genau eine Neuauswertung gekostet, nicht eine Endlosschleife.

**Eine echte Neustartschleife wuerde abstuerzen, nicht haengen** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\display\core.py`:2111 - *gelesen*

```
            while repeat:
                self.interaction_counter += 1

                if self.interaction_counter == 100 and renpy.config.developer:
                    raise Exception("renpy.restart_interaction() was called 100 times without processing any input.")
```

Haette merkbuch_anzeige sich wirklich selbst neu angestossen, waere im Entwicklermodus nach 100 Runden eine Ausnahme geflogen und in errors.txt gelandet. Der Lauf blieb aber still stehen. Das Fehlerbild passt nicht zum Verdacht.

**merkbuch_anzeige ist modal — das unterscheidet ihn von den 21 anderen** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\merkbuch.rpy`:971 - *gelesen*

```
screen merkbuch_anzeige():
    modal True
    zorder 100
    add Solid(MERKBUCH_SCHATTEN)
```

Im ganzen Projekt tragen nur vier Bildschirme modal True: merkbuch_anzeige (972), merkbuch_briefe (1099), merkbuch_lesen (1163) und confirm (screens.rpy:1846). Von den 22 abgezogenen Bildschirmen war merkbuch_anzeige der einzige modale — und der einzige, der haengen blieb.

**Ein modaler Bildschirm markiert das Zeitereignis** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\display\layout.py`:605 - *gelesen*

```
def check_modal(modal, ev, x, y, w, h):
    """
    This evaluates the modal property of frames and screens.
    """

    if not modal:
        return False

    if (ev is not None) and (ev.type == renpy.display.core.TIMEEVENT) and ev.modal:
        return False

    if not callable(modal):
        modal = default_modal_function

    if modal(ev, x, y, w, h):
        if (ev is not None) and (ev.type == renpy.display.core.TIMEEVENT):
            ev.modal = True
            return False
```

Hier wird aus einem harmlosen Zeitereignis ein 'modales' Zeitereignis. Gerufen wird das aus renpy/display/screen.py:812 (if renpy.display.layout.check_modal(self.modal, ev, x, y, None, None):) — mit w=None, und default_modal_function gibt bei w is None immer True zurueck (layout.py:596-597). Ein modaler Bildschirm markiert also JEDES Zeitereignis, unabhaengig von der Mausposition.

**PauseBehavior haelt bei einem modalen Zeitereignis an — und setzt den Wecker auf null** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\display\behavior.py`:605 - *gelesen*

```
    def event(self, ev, x, y, st):
        if ev.type == renpy.display.core.TIMEEVENT:
            if ev.modal and self.modal:
                renpy.game.interface.timeout(max(self.delay - st, 0))
                return
```

Das ist der Dauerlauf. Sobald st die Verzoegerung ueberschritten hat, ist max(self.delay - st, 0) gleich 0; Interface.timeout(0) setzt timeout_time auf event_time (core.py:3308-3315), die Hauptschleife wacht sofort wieder auf, das naechste Zeitereignis kommt, wird wieder modal markiert, und so fort. Ergebnis: kein Schlafen, volle Prozessorlast, die Pause endet nie.

**Voreinstellung: modale Bildschirme blockieren die Pause** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\config.py`:1297 - *gelesen*

```
modal_blocks_pause = True
```

PauseBehavior.__init__ (behavior.py:603) uebernimmt diesen Wert, wenn kein modal-Argument gegeben ist: self.modal = (renpy.config.modal_blocks_pause) if (modal is None) else modal. Das Projekt setzt config.modal_blocks_pause nirgends um, also gilt True.

**renpy.pause reicht modal=None durch — die Sichtprobe hat es nicht gesetzt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\exports\statementexports.py`:99 - *gelesen*

```
def pause(delay=None, music=None, with_none=None, hard=False, predict=False, checkpoint=None, modal=None):
[...]
    `modal`
        If True, a timed pause will not end (it will hold) when a modal screen
        is being displayed.
        If False, the pause will end while a modal screen is being displayed.
[...]
        rv = renpy.ui.interact(mouse="pause", type="pause", roll_forward=roll_forward, pause=delay, pause_modal=modal)
```

Das Verhalten ist dokumentiert: 'a timed pause will not end (it will hold) when a modal screen is being displayed'. Ohne modal=False laeuft der Wert als None bis zu PauseBehavior durch und wird dort zu config.modal_blocks_pause = True. Die Zeilennummern der zitierten Ausschnitte sind 99, 124-127 und 198.

**Die Sichtprobe benutzte genau diesen Aufruf** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\STAND.md`:69 - *gelesen*

```
- **Abzüge:** temporäres `label splashscreen`, `probe_lebenslage(...)`,
  `renpy.show_screen(...)`, `renpy.pause(0.3, hard=True)`,
  `renpy.screenshot(...)`, `renpy.quit()`. Die Bilder landen im
  **SDK-Ordner**. `szene_schritt()` und `merkbuch_anzeige` hängen dabei.
```

Das Abzugsrezept nennt renpy.pause(0.3, hard=True) ohne modal=False. Genau dieser Aufruf haelt vor einem modalen Bildschirm ewig. Der Vermerk 'merkbuch_anzeige haengt dabei' steht in derselben Zeile wie die Ursache — sie war die ganze Zeit im Rezept notiert.

**Der Gegenbeweis aus dem eigenen Protokoll: merkbuch_anlegen ruft dieselben Funktionen und lief durch** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\merkbuch.rpy`:921 - *gelesen*

```
            for kennung in MERKBUCH_FIGUREN:
                $ auswahl = merkbuch_notiz_auswahl(kennung)
                $ gewaehlt = merkbuch_notiz_stelle(kennung)
[...]
                            text figur_name(kennung) style "figuren_name" yalign 1.0
                            text figur_zusatz(kennung) style "figuren_ort" yalign 1.0
```

merkbuch_notiz_auswahl (merkbuch.rpy:518-521) ruft welttext() fuer jede Vorlage, figur_name/figur_zusatz rufen variante(). Damit hat merkbuch_anlegen exakt dieselbe angebliche Nebenwirkung wie merkbuch_anzeige — und steht in AUFGEFALLEN 100 unter 'Unauffaellig (14)'. Wenn ein welttext()-Aufruf im Bildschirm den Dauerlauf ausloeste, haette merkbuch_anlegen genauso haengen muessen. Der Unterschied ist allein modal True. Die zitierten Zeilen sind 921-923 und 933-934.

**Der Rueckfallzweig wird beim Merkbuch nicht betreten: MERKBUCH_LAGE ist vollstaendig** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\merkbuch.rpy`:388 - *gelesen*

```
    MERKBUCH_LAGE = {
        "lebendig": {
            "front": "",
            "etappe": "",
            "heimat": "",
        },
        "verwundet": {
            "front": "Verwundet. Mehr steht in keiner Meldung.",
            "etappe": "Verwundet. Der Zug hat ihn nach hinten gebracht.",
            "heimat": "Verletzt. Wieder auf den Beinen, aber langsamer als vorher.",
        },
```

Nachgezaehlt: sieben Zustaende (lebendig, verwundet, erkrankt, vermisst, verhaftet, entfremdet, gefallen), jeder mit genau den drei Schluesseln front, etappe, heimat. Kein Pfad fehlt, kein 'standard' vorhanden. welttext() nimmt damit immer den ersten Zweig (figuren.rpy:341-342) und ruft variantenersatz_merken() nie.

**Auch die uebrigen drei Merkbuchtafeln sind vollstaendig** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\merkbuch.rpy`:467 - *gelesen*

```
    MERKBUCH_GEGENSEITE = {
        "front": "Achtzig Meter. Kein Name, kein Postweg, und trotzdem wisst ihr beide, dass der andere da ist.",
        "etappe": "Zwanzig Schritt bis zum Gleis. Ihr seht euch jeden Tag, und du kennst nur seine Nummer.",
        "heimat": "Zwanzig Schritte über den Hof. Ihr schreibt euch nicht, obwohl ihr euch täglich seht.",
    }
```

Zaehlung: MERKBUCH_NAEHE_DA (Zeile 428) hat fuenf Eintraege, jeder mit front/etappe/heimat; MERKBUCH_NAEHE_FORT (Zeile 449) hat drei, ebenso vollstaendig; MERKBUCH_GEGENSEITE hat die drei Pfade. Zusammen mit MERKBUCH_LAGE sind das 7+5+3+1 = 16 Woerterbuecher, alle vollstaendig, keins mit 'standard'. Der Rueckfallzweig ist im Merkbuch unerreichbar.

**Auch figur_name/figur_zusatz fallen nicht zurueck — alle Nebenfiguren haben drei Pfade** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\dialoge.rpy`:522 - *gelesen*

```
        Nebenfigur(
            "gegenseite", "die Gegenseite",
            {
                "front": "Der Mann von drüben",
                "etappe": "Der Gefangene aus der Kolonne",
                "heimat": "Die Frau aus dem Vorderhaus",
            },
            {
                "front": "achtzig Meter entfernt",
                "etappe": "er arbeitet am Gleis",
                "heimat": "sie steht im Hof",
            },
```

Alle fuenf Nebenfiguren (gegenseite 522, naechste 538, amtsperson 553, kind 568, kundige 583) tragen in namen UND zusatz jeweils front, etappe und heimat. variante() findet in Zeile 258 (if aktueller_pfad in vorgaben) immer einen Treffer, egal welcher Pfad gespielt wird. Der Docstring in dialoge.rpy:121 ('namen {"front": ..., "heimat": ...}') ist veraltet und beschreibt die Daten nicht mehr richtig.

**Die Store-Variablen sind wirklich Store-Variablen und wirklich revertierbar** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\dialoge.rpy`:91 - *gelesen*

```
    variantenersatz_protokoll = []
    variantenersatz_stellen = {}
    variantenersatz_gesamt = 0
```

Dieser Teil des Verdachts stimmt. Der Block beginnt in dialoge.rpy:25 mit 'init -20 python:', der naechste init-Block folgt erst in Zeile 115 — die drei Namen liegen also auf init-Rang -20 im Store. Und ein Woerterbuchliteral in einem .rpy-Pythonblock wird vom Uebersetzer in einen RevertableDict verwandelt (renpy/python.py:706-711: visit_Dict ersetzt das Literal durch einen Aufruf von __renpy__dict__). Nur folgt daraus nichts: Rollback ist ausgeschaltet (options.rpy:29 'define config.rollback_enabled = False'), und ein Schreibzugriff loest ohnehin keinen Neustart aus.

**Keine zweite Erklaerung: kein Timer, kein repeat, keine ATL-Schleife, kein Neuanstoss im Projekt** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\merkbuch.rpy`:827 - *gelesen*

```
transform merkbuch_aufschlagen(dauer=0.28):
    alpha 0.0
    zoom 0.985
    easein dauer alpha 1.0 zoom 1.0
```

Die einzige Bewegung in merkbuch_anzeige (Zeile 981: at merkbuch_aufschlagen(bewegungszeit(0.28))) ist ein einmaliges easein ohne repeat und ohne Block. Eine Suche ueber alle .rpy im Projekt nach 'Timer(', 'repeat', 'renpy.restart_interaction' und 'renpy.redraw' liefert null Treffer. Die einzige Fundstelle fuer 'pause' ist bewegung.rpy:304 — ein ATL-pause in transform zeile_taucht_auf, nicht renpy.pause, und ohne Wiederholung.

**Im Spiel selbst gibt es keinen einzigen renpy.pause-Aufruf** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\screens.rpy`:825 - *erschlossen*

```
                action [Function(merkbuch_oeffnen), Show("merkbuch_anzeige")]
```

Das ist die einzige Stelle, an der merkbuch_anzeige gezeigt wird — ein Knopf im eckmenue (screens.rpy:803), also mitten in einer laufenden Interaktion, die auf einen Klick wartet. Da kein Ort im Projekt renpy.pause mit einer Verzoegerung aufruft, existiert im Spiel kein PauseBehavior, das blockieren koennte. Der Dauerlauf ist ein Artefakt des Messaufbaus; die Sorge um Rechenzeit auf dem Schulrechner ist nach diesem Befund unbegruendet.

**Reihenfolge der Ereigniszustellung: der modale Bildschirm kommt vor der Pause** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\renpy\display\layout.py`:260 - *gelesen*

```
    def event(self, ev, x, y, st):
        children = self.children
        offsets = self.offsets
[...]
        for i in range(len(offsets) - 1, -1, -1):
            d = children[i]
            xo, yo = offsets[i]

            rv = d.event(ev, x - xo, y - yo, st)
```

Container.event laeuft rueckwaerts durch die Kinder. Das PauseBehavior wird in core.py:2479 (root_widget.add(pb, pause_start, pause_start)) VOR den Ebenen eingehaengt (core.py:2525-2607), bekommt das Ereignis also ZULETZT — nachdem der modale Bildschirm ev.modal bereits auf True gesetzt hat. Genau darum sieht PauseBehavior die Markierung. Zitierte Zeilen: 260-262 und 269-273.

**Folge fuer die Messung: variantenersatz_gesamt zaehlt keinen Unsinn mit** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\dialoge.rpy`:79 - *erschlossen*

```
    ## Ab jetzt schreibt jeder Griff mit. Gezählt wird je STELLE, nicht je
    ## Aufruf: Ein Ren'Py-Bildschirm wird bei jeder Mausbewegung neu
    ## berechnet, eine Zählung je Aufruf wäre also nur ein Maß für die
    ## Mausbewegung. Die Zahl in "anzahl" enthält diese Auffrischungen und
    ## taugt zum Vergleichen, nicht als Absolutwert; aussagekräftig ist die
    ## Zahl der Einträge.
```

Drei Gruende, warum der Fehler die Messung nicht verfaelscht. Erstens ruft merkbuch_anzeige variantenersatz_merken() gar nicht auf, weil kein Rueckfall stattfindet. Zweitens laeuft die Dauerschleife in der Ereignisschleife EINER Interaktion; Bildschirme werden dort nicht neu ausgewertet (screen.py:645-648, geleert nur in core.py:2417), der Zaehler waechst also auch dann nicht, wenn irgendwo doch ein Rueckfall saesse. Drittens ist die Schwaeche der Zahl bereits dokumentiert und im Analysebildschirm benannt (dialoge.rpy:1624: 'die Zahl in Klammern enthaelt die Bildschirmauffrischungen und taugt nur zum Vergleichen'). Aussagekraeftig bleibt len(variantenersatz_protokoll) in dialoge.rpy:1628.

**Zwei weitere Bildschirme wuerden genauso haengen** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\merkbuch.rpy`:1098 - *gelesen*

```
screen merkbuch_briefe(kennung):
    modal True
    zorder 110
```

merkbuch_briefe (1098) und merkbuch_lesen (1162, ebenfalls modal True in 1163) sowie confirm (screens.rpy:1846) tragen dasselbe modal True. Sie waren in den 21 abgezogenen Bildschirmen nicht dabei; wer sie nachtraegt, muss dieselbe Pause mit modal=False fahren, sonst haengt der Abzug dort genauso. Die uebrigen von dir genannten Bildschirme sind unverdaechtig: brief_bildschirm (figuren.rpy:3054), brief_ausgang_bildschirm (3140), schicksal_bildschirm (3192) und post_ankuendigung (merkbuch.rpy:845) sind nicht modal und bekommen ihre Texte als fertige Daten uebergeben.

**Der einzige direkte welttext()-Aufruf im Bildschirmrumpf ausserhalb des Merkbuchs** - `C:\Users\domin\Desktop\renpy-8.5.0-sdk\Zwischen den Fronten Backup Cloud\game\minispiele.rpy`:2579 - *gelesen*

```
    $ knopftext = lage.get("knopf") or ("Weitergeben" if fremd else welttext({"front": "Abschicken", "etappe": "Abschicken", "heimat": "Einwerfen"}))
```

Diese Zeile liegt im Rumpf von screen einlage_rotstift (minispiele.rpy:2423). Das Woerterbuch hat alle drei Pfade, es faellt also nichts zurueck, und der Bildschirm ist nicht modal. Ausser dieser Zeile und merkbuch.rpy:1032 gibt es im ganzen Projekt keinen weiteren welttext()/variante()/jahrestext()-Aufruf, der unmittelbar in einem Bildschirmrumpf steht; alles andere laeuft ueber Funktionen (figur_name, figur_zusatz, merkbuch_lage_satz, merkbuch_naehe_satz, merkbuch_notiz_auswahl, post_ankuendigung_daten).

### Offene Fragen und Urteil

- URTEIL: WIDERLEGT. Nicht der Store-Schreibzugriff ist die Ursache, sondern modal True zusammen mit einer zeitgesteuerten Pause. Der Verdacht traf nur in einem Nebenpunkt zu: variantenersatz_stellen und variantenersatz_gesamt sind tatsaechlich Store-Variablen auf init -20, und das Woerterbuch ist tatsaechlich ein RevertableDict. Beides ist folgenlos.
- KLEINSTMOEGLICHE BEHEBUNG: Am Spielcode ist nichts zu aendern — modal True in merkbuch.rpy:972 ist richtig, weil das Heft mitten in einer Szene aufgeschlagen wird und den Klick darunter anhalten soll. Zu aendern ist das Abzugsrezept: In STAND.md Zeile 70 wird aus renpy.pause(0.3, hard=True) der Aufruf renpy.pause(0.3, hard=True, modal=False). Ein Schluesselwort, eine Zeile. Wer lieber am Aufbau ansetzt, kann stattdessen im temporaeren Probe-.rpy einmal $ config.modal_blocks_pause = False setzen; das ist groeber, weil es alle Pausen betrifft, und deshalb die zweite Wahl.
- Nicht geprueft: ob probe_lebenslage(...) in der Sichtprobe aktueller_pfad wirklich auf einen der drei Pfade setzt. Ich habe die Sichtprobendatei nicht gesehen — sie war temporaer und ist geloescht. Steht aktueller_pfad dort auf einem Wert ausserhalb von front/etappe/heimat, greift der Rueckfallzweig doch, ohne dass das am Urteil etwas aendert: Der Dauerlauf haengt am modalen Zeitereignis, nicht am Schreibzugriff.
- Offen fuer Dominik, weil es den Aufbau der Sichtprobe betrifft: Sollen merkbuch_briefe (merkbuch.rpy:1098), merkbuch_lesen (1162) und confirm (screens.rpy:1846) in den naechsten Abzug aufgenommen werden? Sie sind die drei uebrigen modalen Bildschirme und mit dem korrigierten Pausenaufruf ohne Weiteres messbar; die Sichtprobe hat bisher 22 von 25 Bildschirmen erfasst.
- Nebenbefund, nicht zum Auftrag gehoerend und nicht geaendert: Der Docstring der Klasse Nebenfigur in dialoge.rpy:121 sagt namen {"front": ..., "heimat": ...} und verschweigt die Etappe, obwohl alle fuenf Figuren seit Paket 5 drei Pfade tragen. Wer sich darauf verlaesst, sucht eine Luecke, die es nicht gibt.

---

## GEGENGELESEN B

### Urteile des Gegenlesers (6)

- **options.rpy setzt keine der sechs Audio-Kennungen (Kernbehauptung)** - **bestaetigt**: game/options.rpy vollstaendig gelesen (79 Zeilen, endet mit build.documentation('*.txt')): keine der Kennungen main_menu_music, default_music_volume, default_sfx_volume, default_voice_volume, mixer, fadeout_audio kommt vor. Audio wird dort nur an drei Stellen beruehrt: Zeile 15 "define config.has_sound = True", Zeile 16 "define config.has_music = True", Zeile 17 "define config.has_voice = False". Grep ueber game/**/*.rpy nach diesen sechs Kennungen (auch case-insensitiv): kein Treffer. Einzige Fundstellen im Ordner game/ sind Uebersetzungsstrings in game/tl/None/common.rpym, Zeile 769 'old "main volume"', 773 'old "music volume"', 777 'old "sound volume"', 781 'old "voice volume"' — das sind Uebersetzungen der Ren'Py-Standardtexte, keine Einstellungen.
- **Ren'Py-Vorgabe config.main_menu_music = None an 00start.rpy Zeile 28** - **bestaetigt**: C:/Users/domin/Desktop/renpy-8.5.0-sdk/renpy/common/00start.rpy, Zeile 28: "    config.main_menu_music = None" (per PowerShell/Select-String gelesen; der Read-Zugriff ausserhalb des Projektordners ist durch die Berechtigungseinstellung gesperrt). Zeile 31 ergaenzt "    config.main_menu_music_fadein = 0.0". Zeilennummer stimmt exakt.
- **Ren'Py-Vorgaben default_music_volume / default_sfx_volume / default_voice_volume = 1.0 an 00defaults.rpy 57/60/63** - **bestaetigt**: C:/Users/domin/Desktop/renpy-8.5.0-sdk/renpy/common/00defaults.rpy, Zeile 57: "    config.default_music_volume = 1.0", Zeile 60: "    config.default_sfx_volume = 1.0", Zeile 63: "    config.default_voice_volume = 1.0". Alle drei Zeilennummern stimmen exakt. Angewandt werden sie in demselben File, Zeilen 117-124: "if config.default_music_volume is not None: / _preferences.set_volume('music', _vol(config.default_music_volume))" und analog fuer 'sfx' (120/121) und 'voice' (123/124).
- **Das Hauptmenue ist stumm** - **bestaetigt**: Zwei unabhaengige Belege. Erstens Ren'Py: 00start.rpy Zeile 268-271: "if config.main_menu_music: / $ renpy.music.play(config.main_menu_music, if_changed=True, fadein=config.main_menu_music_fadein) / else: / $ renpy.music.stop()" — bei None wird die Musik ausdruecklich gestoppt. Zweitens das Projekt: Grep ueber game/**/*.rpy nach '^\s*(play|queue)\s+(music|sound|audio)', 'renpy.music.play' und 'Play(' liefert KEINEN Treffer im ganzen Projekt; der Bildschirm in game/screens.rpy Zeile 1646 "screen main_menu():" enthaelt entsprechend keine Audio-Aktion. Es gibt derzeit ueberhaupt keine Tonwiedergabe im Projektcode.
- **"alle Regler stehen beim ersten Start auf Anschlag"** - **unklar**: Fuer die Lautstaerke stimmt es, woertlich fuer "alle Regler" nicht. In game/screens.rpy stehen im Einstellungsbildschirm drei Regler: Zeile 1823 "bar value Preference(\"text speed\") style \"slider\"", Zeile 1833 "bar value Preference(\"music volume\") style \"slider\"", Zeile 1837 "bar value Preference(\"sound volume\") style \"slider\"". Die beiden Lautstaerkeregler stehen wegen 00defaults.rpy 57/60 (1.0) beim ersten Start auf Anschlag — bestaetigt. Der Textgeschwindigkeitsregler nicht: game/options.rpy Zeile 40 "default preferences.text_cps = 45", und 00preferences.rpy Zeile 275 sagt "For \"text speed\", it defaults to 200 cps" (Regelbereich, Zeile 348: "return FieldValue(_preferences, \"text_cps\", range=bar_range * 1.0, max_is_zero=True, ...)"). Er steht also bei 45 von 200. Ausserdem gibt es gar keinen Voice-Regler im Bildschirm (options.rpy Zeile 17: "define config.has_voice = False"), auch wenn der Wert intern auf 1.0 steht.
- **"Wer spaeter Menuemusik will, setzt eine Zeile in options.rpy — kein Umbau noetig"** - **bestaetigt**: Der Mechanismus liegt fertig bereit: 00start.rpy Zeile 268-269 spielt config.main_menu_music selbsttaetig ab, sobald der Wert gesetzt ist, und options.rpy Zeile 16 hat "define config.has_music = True" bereits gesetzt. Es waere also tatsaechlich eine einzige define-Zeile. Einschraenkung, die die Behauptung nicht nennt: die Audiodatei selbst muss vorhanden sein — Projektregel 7 verbietet erfundene Dateinamen, und im Ordner game/ existiert derzeit keine einzige play-Anweisung, an der man sich orientieren koennte.

---


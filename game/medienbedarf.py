# -*- coding: utf-8 -*-
"""medienbedarf.py - der Bedarfsplan zu "Zwischen Front und Heimat".

    python medienbedarf.py

Schreibt MEDIEN.md neben die .rpy-Dateien: jede Datei, die das Spiel
erwartet, mit ihrer Herkunft im Code, ihrem Status, ihrem Anzeigemass und
Suchbegriffen fuer die Recherche in Archiven.

WARUM ES DIESES SKRIPT GIBT
Das Spiel laeuft ohne eine einzige Mediendatei (Regel 7) - ueberall greift
bild_platzhalter() oder eine Ersatzschrift. Es sieht dann aber nach
Platzhalter aus. Wer das Material sammelt, braucht keine Fehlerliste,
sondern einen Einkaufszettel: was, wofuer, in welchem Mass, und wonach man
suchen muss.

ES BAUT DIE LISTE NICHT SELBST
Die Pfade kommen aus probe_alles.medien_sammeln() - derselben Funktion,
mit der die Medienprobe zaehlt. Ein zweiter Sammler wuerde frueher oder
spaeter andere Pfade nennen als der Bericht, und dann glaubte jemand der
falschen Liste (Regel 11). Deshalb wird hier importiert, nicht nachgebaut.

WAS ES NICHT TUT
Es erfindet keine Signatur, keinen Bildnachweis und keine Rechteauskunft
zu einem einzelnen Stueck. Die Rechtelage steht als allgemeine Notiz je
Haus im Kopf des Dokuments; ob ein bestimmtes Blatt frei ist, sagt das
Haus und nicht dieses Skript.
"""

import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import probe_alles


################################################################################
## 1. Woerter fuer die Recherche
################################################################################
##
## Die Suchbegriffe entstehen aus dem, was im Bestand schon steht: aus der
## Kennung eines Ereignisses, seinem Ort und seinen Jahren. Erfunden wird
## dabei nichts - eine Kennung wie "heimat_1915_brotkarte" nennt ihr Thema
## selbst. Die Tafeln unten uebersetzen nur, was die Kennung schon sagt.

## Kennungen sind ohne Umlaute geschrieben. Fuer die Suche gehoeren sie
## zurueck: Wer "zaehlung" in ein Archivformular tippt, findet nichts.
RUECKUMLAUT = [
    ("zaehlung", "Zählung"),
    ("ernaehrungsamt", "Ernährungsamt"),
    ("raeumung", "Räumung"),
    ("verbruederung", "Verbrüderung"),
    ("stosstrupp", "Stoßtrupp"),
    ("rueben", "Rüben"),
    ("kohlennot", "Kohlennot"),
    ("todesnachricht", "Todesnachricht"),
    ("arbeitsniederlegung", "Arbeitsniederlegung"),
    ("unterstuetzung", "Unterstützung"),
    ("hamsterfahrt", "Hamsterfahrt"),
    ("brotschlange", "Brotschlange"),
    ("lazarettzug", "Lazarettzug"),
    ("metallsammlung", "Metallsammlung"),
    ("schulspeisung", "Schulspeisung"),
    ("januarstreik", "Januarstreik"),
    ("grippewelle", "Grippewelle"),
    ("bekanntmachung", "Bekanntmachung"),
    ("versorgungsamt", "Versorgungsamt"),
    ("nachschubstockung", "Nachschubstockung"),
    ("bahnhofsdienst", "Bahnhofsdienst"),
    ("fronturlauber", "Fronturlauber"),
    ("zensurstelle", "Zensurstelle"),
    ("requisition", "Requisition"),
    ("kriegsanleihe", "Kriegsanleihe"),
    ("hilfsdienst", "Hilfsdienst"),
    ("unterseeboot", "Unterseeboot"),
    ("kinderarbeit", "Kinderarbeit"),
    ("denunziation", "Denunziation"),
    ("waffenstillstand", "Waffenstillstand"),
    ("ruhequartier", "Ruhequartier"),
    ("gerichtsherr", "Gerichtsherr"),
    ("erster_toter", "Gefallener am Wegrand"),
    ("verschleppt", "Zwangsarbeit Deportation"),
    ("brief_von_daheim", "Feldpostbrief"),
    ("abrechnung", "Abrechnung"),
]

## Was ein Kartentyp fuer die Suche bedeutet - deutsch und englisch.
TYP_WORT = {
    "karte": ("Fotografie", "photograph"),
    "feldpost": ("Feldpostbrief, Feldpostkarte", "field post letter, Feldpost card"),
    "lebensmittel": ("Lebensmittelkarte, Brotkarte, Bezugsschein",
                     "ration card, bread card, food coupon"),
    "zeitung": ("Zeitungsseite, Extrablatt", "newspaper page, war news"),
    "amtlich": ("Vordruck, Bescheid, Bekanntmachung, Aushang",
                "official form, decree, public notice"),
}

## Der Pfad sagt, wo das Motiv spielt.
PFAD_WORT = {
    "front": ("Westfront, Schützengraben", "Western Front, trench"),
    "etappe": ("Etappe, rückwärtiges Gebiet", "rear area, lines of communication"),
    "heimat": ("Heimatfront, deutsche Stadt", "German home front"),
}

## Zu welchem Haus ein Motiv am ehesten passt. Das ist ein Hinweis fuer die
## Suche, keine Auskunft ueber die Rechte an einem bestimmten Stueck.
HAUS_EMPFEHLUNG = {
    "feldpost": "Museum für Kommunikation / Europeana 1914-1918 (Privatbestände)",
    "lebensmittel": "Deutsches Historisches Museum (LeMO), Stadt- und Landesarchive",
    "zeitung": "Zeitungsdigitalisate der Staatsbibliotheken, ZEFYS",
    "amtlich": "Bundesarchiv, Landes- und Stadtarchive",
    "karte": "Bundesarchiv Bild, Deutsches Historisches Museum (LeMO)",
    "portraits": "Europeana 1914-1918, Stadtarchive, Fotosammlungen",
    "figuren": "Europeana 1914-1918, Stadtarchive, Fotosammlungen",
    "fonts": "Schriftanbieter mit freier Lizenz (SIL OFL), nicht Archive",
}


def rueckumlaut(wort):
    for ohne, mit in RUECKUMLAUT:
        if ohne == wort:
            return mit
    return wort.replace("_", " ").capitalize()


def thema_aus_kennung(kennung):
    """Das Thema steckt im letzten Stueck der Kennung.

    "heimat_1915_brotkarte" -> "Brotkarte". Pfadname und Jahreszahl am
    Anfang tragen fuer die Suche nichts bei; sie kommen aus den Feldern
    pfad und jahre schon mit.
    """
    teile = str(kennung).split("_")
    while teile and (teile[0] in ("front", "etappe", "heimat", "epilog",
                                 "einstieg")
                     or teile[0].isdigit()):
        teile.pop(0)
    if not teile:
        return str(kennung).replace("_", " ")
    return rueckumlaut("_".join(teile))


def jahresangabe(jahre):
    if not jahre:
        return "1914-1918"
    if len(jahre) == 1:
        return str(jahre[0])
    return "%d-%d" % (min(jahre), max(jahre))


def suchbegriffe_ereignis(vorlage, typ):
    """Zwei deutsche und ein englischer Begriff, aus dem Bestand gebildet."""
    thema = thema_aus_kennung(vorlage.kennung)
    jahr = jahresangabe(vorlage.jahre)
    typ_de, typ_en = TYP_WORT.get(typ, TYP_WORT["karte"])
    pfad = vorlage.pfad[0] if vorlage.pfad else "heimat"
    pfad_de, pfad_en = PFAD_WORT.get(pfad, PFAD_WORT["heimat"])

    deutsch = ["%s %s" % (thema, jahr)]
    if vorlage.ort:
        deutsch.append("%s %s %s" % (typ_de.split(",")[0], vorlage.ort, jahr))
    else:
        deutsch.append("%s %s" % (typ_de.split(",")[0], pfad_de))
    englisch = "%s %s %s" % (typ_en.split(",")[0], pfad_en, jahr)
    return deutsch, [englisch]


################################################################################
## 2. Das Dokument
################################################################################

KOPFTEXT = """# MEDIEN

Der Bedarfsplan. Jede Datei, die das Spiel erwartet, mit ihrer Herkunft im
Code, ihrem Status und Suchbegriffen für die Recherche.

**Erzeugt von `medienbedarf.py`. Von Hand geänderte Stellen sind beim
nächsten Lauf weg** — was hier fehlt oder falsch steht, gehört im Skript
oder im Spiel geändert.

Das Spiel läuft ohne jede dieser Dateien: Überall greift
`bild_platzhalter()` oder eine Ersatzschrift (Regel 7). Eine fehlende Datei
ist kein Fehler, sondern eine offene Aufgabe.
"""

RECHTETEXT = """## Zur Rechtelage

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
"""

ERKLAERTEXT = """## Wie diese Liste zu lesen ist

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
"""


def masse_zeile(NS, kategorie):
    kurz = kategorie.split("/")[-1]
    ablage = NS.get("BILD_MASSE", {}).get(kurz)
    anzeige = NS.get("BILD_ANZEIGE", {}).get(kurz)
    if not ablage and not anzeige:
        return ""
    return "Ablagemaß %s, Anzeigemaß %s" % (ablage or "-", anzeige or "-")


def bauen():
    ordner = probe_alles.spielordner_finden()
    aufbau = probe_alles.Aufbau(ordner)
    aufbau.lesen()
    aufbau.ausfuehren()
    NS = aufbau.NS

    herkunft, stimmungen, typenzaehler, _b = probe_alles.medien_sammeln(
        NS, aufbau.medienbuch, ordner)

    def da(pfad):
        return os.path.isfile(os.path.join(ordner, pfad.replace("/", os.sep)))

    ## Nach Kategorie gruppieren, in einer festen, lesbaren Folge.
    folge = ["fonts", "images/karten", "images/dokumente", "images/portraits",
             "images/figuren", "images", "audio"]
    gruppen = collections.OrderedDict()
    for name in folge:
        gruppen[name] = []
    for pfad in sorted(herkunft):
        teile = pfad.split("/")
        kategorie = "/".join(teile[:-1]) if len(teile) >= 2 else "(Wurzel)"
        gruppen.setdefault(kategorie, []).append(pfad)

    gesamt = len(herkunft)
    vorhanden = len([p for p in herkunft if da(p)])

    z = []
    z.append(KOPFTEXT)
    z.append("")
    z.append("## Die Zahlen")
    z.append("")
    z.append("| | Dateien |")
    z.append("|---|---|")
    z.append("| Erwartet | **%d** |" % gesamt)
    z.append("| Davon vorhanden | **%d** |" % vorhanden)
    z.append("| Noch abzulegen | **%d** |" % (gesamt - vorhanden))
    z.append("")
    z.append("| Ordner | erwartet | vorhanden | fehlt |")
    z.append("|---|---|---|---|")
    for kategorie in gruppen:
        if not gruppen[kategorie]:
            continue
        habe = len([p for p in gruppen[kategorie] if da(p)])
        z.append("| `%s` | %d | %d | %d |"
                 % (kategorie, len(gruppen[kategorie]), habe,
                    len(gruppen[kategorie]) - habe))
    z.append("")
    z.append("Berücksichtigte Stimmungen: %s." % ", ".join(stimmungen))
    z.append("")
    z.append("Kartentypen im Bestand: %s."
             % ", ".join("%d x %s" % (typenzaehler.get(t, 0), t)
                         for t in NS["KARTENTYPEN"]))
    z.append("")
    z.append(RECHTETEXT)
    z.append("")
    z.append(ERKLAERTEXT)

    ## ---------------------------------------------------------------- Schriften
    z.append("")
    z.append("---")
    z.append("")
    z.append("## fonts — die vier Schriften")
    z.append("")
    z.append("Jede Schrift wird in zwei Fassungen gesucht, `.ttf` zuerst.")
    z.append("Liegt keine, greift der Ersatz, und man sieht davon nichts —")
    z.append("außer dass alles gleich aussieht.")
    z.append("")
    kandidaten = NS.get("SCHRIFT_KANDIDATEN", {})
    zwecke = NS.get("SCHRIFT_ZWECK", {})
    for name in sorted(kandidaten):
        z.append("### %s" % name)
        z.append("")
        z.append("*%s*" % zwecke.get(name, ""))
        z.append("")
        z.append("Greift heute: `%s`" % NS.get(name, "?"))
        z.append("")
        for pfad in kandidaten[name]:
            z.append("- `%s` — %s" % (pfad, "vorhanden" if da(pfad) else "**fehlt**"))
        z.append("")
        z.append("Suche: freie Antiqua mit vollem deutschen Zeichensatz; "
                 "*free serif typeface SIL OFL*. Bezug: %s."
                 % HAUS_EMPFEHLUNG["fonts"])
        z.append("")

    ## ---------------------------------------------------------------- Karten
    for kategorie, ueberschrift, erklaerung in [
        ("images/karten", "images/karten — Szenenbilder",
         "Ein Bild je Option. Es zeigt die Lage, nicht die Entscheidung: "
         "kein Bild, auf dem schon jemand tut, was die Spielerin erst "
         "wählen soll."),
        ("images/dokumente", "images/dokumente — Dokumentmotive",
         "Dieselbe Stelle im Bildschirm, aber ein anderer Bestand: ein "
         "abfotografiertes Blatt, nah und fast quadratisch. Welche Karte "
         "hierher gehört, entscheidet ihr Kartentyp."),
    ]:
        if not gruppen.get(kategorie):
            continue
        z.append("---")
        z.append("")
        z.append("## %s" % ueberschrift)
        z.append("")
        z.append(erklaerung)
        z.append("")
        z.append("%s. %d Dateien, davon %d vorhanden."
                 % (masse_zeile(NS, kategorie), len(gruppen[kategorie]),
                    len([p for p in gruppen[kategorie] if da(p)])))
        z.append("")

        ## Nach Ereignis buendeln - eine Recherche je Ereignis, nicht je Datei.
        nach_ereignis = collections.OrderedDict()
        for vorlage in NS["EREIGNISSE"]:
            typ = getattr(vorlage, "kartentyp", "karte")
            if NS["kartenbild_kategorie"](typ) != kategorie.split("/")[-1]:
                continue
            nach_ereignis[vorlage.kennung] = vorlage

        for kennung, vorlage in nach_ereignis.items():
            typ = getattr(vorlage, "kartentyp", "karte")
            deutsch, englisch = suchbegriffe_ereignis(vorlage, typ)
            z.append("### %s" % kennung)
            z.append("")
            z.append("%s · %s · %s"
                     % (jahresangabe(vorlage.jahre),
                        ", ".join(vorlage.pfad),
                        vorlage.ort or "ohne Ort"))
            z.append("")
            nummer = 0
            for auswahl in vorlage.optionen:
                nummer += 1
                if not auswahl.bild:
                    continue
                pfad = NS["bild_pfad"](kategorie.split("/")[-1], auswahl.bild)
                z.append("- `%s` — Option %d, %s"
                         % (pfad, nummer,
                            "vorhanden" if da(pfad) else "**fehlt**"))
            z.append("")
            z.append("Suche: *%s*; englisch *%s*."
                     % ("*, *".join(deutsch), englisch[0]))
            kurz = ""
            if isinstance(vorlage.quelle, dict):
                kurz = vorlage.quelle.get("kurz", "")
            if kurz:
                z.append("")
                z.append("Der Beleg des Ereignisses nennt: %s" % kurz)
            z.append("")
            z.append("Wo suchen: %s"
                     % HAUS_EMPFEHLUNG.get(typ, HAUS_EMPFEHLUNG["karte"]))
            z.append("")

    ## ---------------------------------------------------------------- Portraits
    if gruppen.get("images/portraits"):
        z.append("---")
        z.append("")
        z.append("## images/portraits — die Spielfigur")
        z.append("")
        z.append("Das Bild in der Kopfleiste. Es wechselt mit der Stimmung; "
                 "fehlt die Stimmungsfassung, greift `_neutral`, und fehlt "
                 "auch die, das Bild ohne Zusatz. **Es genügt also, je "
                 "Herkunft und Geschlecht ein einziges Bild abzulegen** — "
                 "die Stimmungen sind eine Steigerung, keine Bedingung.")
        z.append("")
        z.append("%s. %d Dateien, davon %d vorhanden."
                 % (masse_zeile(NS, "images/portraits"),
                    len(gruppen["images/portraits"]),
                    len([p for p in gruppen["images/portraits"] if da(p)])))
        z.append("")
        for quelle in NS["HERKUENFTE"]:
            for geschlecht, wort, wort_en in [("m", "Mann", "man"),
                                              ("w", "Frau", "woman")]:
                stamm = "%s_%s" % (quelle.kennung, geschlecht)
                z.append("### %s" % stamm)
                z.append("")
                z.append("- `%s` — **das Grundbild.** Ohne Stimmung, springt "
                         "immer ein." % NS["bild_pfad"]("portraits", stamm))
                for stimmung in stimmungen:
                    pfad = NS["bild_pfad"]("portraits",
                                           "%s_%s" % (stamm, stimmung))
                    z.append("- `%s` — Stimmung %s%s"
                             % (pfad, stimmung,
                                ", vorhanden" if da(pfad) else ""))
                z.append("")
                z.append("Suche: *Porträt %s %s 1914-1918*, "
                         "*Atelierfotografie %s*; englisch "
                         "*portrait German %s %s 1915*."
                         % (wort, quelle.kennung, wort, wort_en,
                            quelle.kennung))
                z.append("")
                z.append("Wo suchen: %s" % HAUS_EMPFEHLUNG["portraits"])
                z.append("")

    ## ---------------------------------------------------------------- Figuren
    if gruppen.get("images/figuren"):
        z.append("---")
        z.append("")
        z.append("## images/figuren — die fünf Nebenfiguren")
        z.append("")
        z.append("**Diese Bilder sucht das Spiel heute gar nicht ab.** "
                 "`FIGUREN_ECHTE_BILDER` steht auf `False`; solange das so "
                 "ist, greift überall `FIGUREN_PLATZHALTER`. Die Liste steht "
                 "hier, damit sie vollständig ist, und ist von allen "
                 "Abschnitten der am wenigsten dringliche.")
        z.append("")
        z.append("%d Dateien: fünf Figuren mal drei Pfade mal %d Stimmungen."
                 % (len(gruppen["images/figuren"]), len(stimmungen)))
        z.append("")
        for kennung in NS["FIGUREN_REIHENFOLGE"]:
            z.append("### %s" % kennung)
            z.append("")
            for pfad_name in NS["PFAD_REIHENFOLGE"]:
                dateien = ["images/figuren/%s_%s_%s.png"
                           % (kennung, pfad_name, s) for s in stimmungen]
                z.append("- Pfad %s: `%s` … (%d Stimmungen)"
                         % (pfad_name, dateien[0], len(dateien)))
            z.append("")
            pfad_de, pfad_en = PFAD_WORT.get(NS["PFAD_REIHENFOLGE"][0],
                                             PFAD_WORT["heimat"])
            z.append("Suche: *Porträt %s 1914-1918*, *Gruppenfoto %s*; "
                     "englisch *portrait %s Germany 1916*."
                     % (kennung, pfad_de, pfad_en))
            z.append("")
            z.append("Wo suchen: %s" % HAUS_EMPFEHLUNG["figuren"])
            z.append("")

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
        z.append("")

    ## ------------------------------------------------- Vorhanden, unbenutzt
    verwaist = []
    for unterordner in ["images", "fonts", "audio"]:
        wurzel = os.path.join(ordner, unterordner)
        if not os.path.isdir(wurzel):
            continue
        for gang, _unter, dateien in os.walk(wurzel):
            for name in dateien:
                rel = os.path.relpath(os.path.join(gang, name),
                                      ordner).replace(os.sep, "/")
                if rel not in herkunft:
                    verwaist.append(rel)

    z.append("---")
    z.append("")
    z.append("## Vorhanden, aber unbenutzt")
    z.append("")
    if not verwaist:
        z.append("Keine. Jede abgelegte Datei wird auch gesucht.")
    else:
        z.append("Diese Dateien liegen im Projekt, und keine Stelle im Code "
                 "fragt nach ihnen. Sie sind nicht falsch — sie warten nur "
                 "auf ihren Ort.")
        z.append("")
        for rel in sorted(verwaist):
            z.append("### `%s`" % rel)
            z.append("")
            z.append(VORSCHLAG.get(rel, VORSCHLAG_ALLGEMEIN))
            z.append("")
    z.append("")

    ## ---------------------------------------------------------------- Schluss
    z.append("---")
    z.append("")
    z.append("## Wenn eine Datei abgelegt ist")
    z.append("")
    z.append("Nichts weiter tun. Der Code sucht bei jedem Start neu; eine "
             "Datei am richtigen Pfad wird ohne Zutun benutzt, und der "
             "Platzhalter verschwindet. Zur Kontrolle:")
    z.append("")
    z.append("```")
    z.append("python medienbedarf.py      diese Datei neu schreiben")
    z.append("python probe_alles.py       Probe 6 zählt mit")
    z.append("```")
    z.append("")

    ziel = os.path.join(ordner, "MEDIEN.md")
    io.open(ziel, "w", encoding="utf-8").write("\n".join(z) + "\n")
    return ziel, gesamt, vorhanden, len(verwaist)


## Wohin eine vorhandene, aber unbenutzte Datei gehoeren koennte. Das ist ein
## Vorschlag und keine Entscheidung - wo eine Datei hingehoert, entscheidet
## der Projektleiter.
VORSCHLAG_ALLGEMEIN = (
    "Kein Vorschlag. Diese Datei ist dem Skript unbekannt; wer sie abgelegt "
    "hat, weiß, wofür sie gedacht war."
)

VORSCHLAG = {
    "audio/stummer_morgen.mp3": (
        "**Bleibt liegen, und das ist entschieden, kein Versäumnis.** Das "
        "Tongerüst steht seit Paket 8, Schritt 2.6: `ton_spielen()`, die "
        "Tafel `ORTSKLANG` für zehn Klangräume und `STELLENMUSIK` für sieben "
        "Stellen im Ablauf. Diese Datei bekommt dort keine Zeile.\n\n"
        "Ihr ID3-Kopf sieht nach Inhalt aus — Titel „Stummer Morgen“, ein "
        "Interpret, der Vermerk „made with suno“, ein eingebettetes "
        "Titelbild, vier Minuten drei Sekunden. Sie ist trotzdem keiner: "
        "**Der Projektleiter hat am 6. September gesagt, es sei eine "
        "Probedatei.** Eine Tafelzeile darf eine Datei anfordern, die noch "
        "fehlt; sie darf eine vorhandene nicht vereinnahmen.\n\n"
        "Wer sie doch einbauen will, braucht zwei Handgriffe: die "
        "Dateikennung in einer Zeile von `STELLENMUSIK` (ton.rpy) eintragen "
        "und `MUSIK_EINGESCHALTET` auf `True` setzen. **Nicht** in "
        "`ORTSKLANG` — für einen Umgebungsklang ist sie zu lang und zu "
        "gesetzt, und an der Front und in der Etappe wäre sie als Musik "
        "ohnehin gesperrt (Regel 3)."
    ),
    "images/karten/front_beginn_1.png": (
        "**Bleibt vorerst liegen, und das ist eine Entscheidung, kein "
        "Versäumnis.** Ein Ereignis `front_beginn` gibt es im Bestand nicht, "
        "und das Motiv passt auch nicht dazu: eine leere Kopfsteinstraße mit "
        "Fachwerk in der Dämmerung, also eine Heimatszene. Es stammt "
        "erkennbar aus einem frühen Entwurf.\n\n"
        "Zuordnen ließe es sich — `heimat_sonntag` spielt in einer stillen "
        "Straße und passt gut. Dagegen spricht das Aussehen des Ganzen: "
        "**Ein einzelnes bebildertes Ereignis unter hundert unbebilderten "
        "sieht schlechter aus als hundert gleich behandelte Leerstellen.** "
        "Die Leerstelle ist seit Paket 8 ruhig und einheitlich; ein "
        "einzelnes Bild dazwischen bricht diese Ruhe auf und lässt alles "
        "andere wie einen Fehler wirken. Konsistenz schlägt hier "
        "Einzelqualität.\n\n"
        "Sinnvoll wird das erste Bild, sobald ein **ganzer Zusammenhang** "
        "bebildert ist: ein Jahr, ein Pfad oder alle Karten eines Typs."
    ),
    "images/karten/front_beginn_2.png": (
        "Dasselbe wie bei `front_beginn_1.png`. Das Motiv — ein Schreibtisch "
        "mit Petroleumlampe, Federkiel, Taschenuhr und einem gefalteten "
        "Brief mit Stempel — passt inhaltlich am besten zu "
        "`etappe_innendienst` (\"Du gehst mir eine Woche in die "
        "Schreibstube\"), nicht zu einem Frontereignis."
    ),
}


def main():
    ziel, gesamt, vorhanden, verwaist = bauen()
    print("MEDIEN.md geschrieben: %s" % ziel)
    print("  %d erwartete Dateien, %d vorhanden, %d noch abzulegen."
          % (gesamt, vorhanden, gesamt - vorhanden))
    print("  %d vorhanden, aber unbenutzt." % verwaist)
    return 0


if __name__ == "__main__":
    sys.exit(main())

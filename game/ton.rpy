################################################################################
## ton.rpy - Das Tongerüst
################################################################################
##
## Warum es diese Datei gibt: Bis Paket 8, Schritt 2.6 gab es im ganzen Spiel
## keine einzige Tonzeile - kein play, kein renpy.music, kein renpy.sound. Fünf
## Dateiköpfe sagten das ausdrücklich zu ("Kein Audio"). Ton kommt jetzt hinzu,
## und er kommt an genau einem Ort hinzu statt verstreut in den Bildschirmen.
## Das ist dieselbe Entscheidung wie bei bewegung.rpy in Paket 7: Wer den Ton
## abschalten, leiser stellen oder prüfen will, soll eine Datei aufschlagen und
## nicht sechs.
##
## init -45, wie bewegung.rpy. Die Datei hängt von nichts ab - keine Farbe,
## keine Schrift, kein Bestand -, und zur init-Zeit hängt nichts von ihr ab:
## Gerufen wird sie ausschließlich aus labels, also zur Laufzeit. Der Rang liegt
## trotzdem früh, damit jede spätere Datei die Tafeln schon kennt, wenn sie eine
## Zeile ergänzen will (Arbeitsweise: in der eigenen Datei überschreiben, nicht
## in fremden herumschneiden).
##
## DER UNTERSCHIED ZWISCHEN UMGEBUNGSKLANG UND MUSIK (Auftragspunkt 13)
##
##   Umgebungsklang  ist das, was am Ort ohnehin zu hören wäre, wenn niemand
##                   spielte: Wind über der Brustwehr, ein Karren auf Pflaster,
##                   die Halle eines Bahnhofs. Er gehört zum Ort, nicht zur
##                   Erzählung. Er ist überall erlaubt, auch an der Front und
##                   in der Etappe.
##   Musik           ist gesetzt. Sie kommt nicht aus der Welt, sondern von
##                   außen, und sie sagt der Spielerin, wie sie das Gesehene
##                   empfinden soll. Genau deshalb ist sie an der Front und in
##                   der Etappe VERBOTEN (Regel 3): Der Widerspruch soll im
##                   Kopf der Spielerin entstehen und nicht im Lautsprecher.
##
## Ren'Py kennt diesen Unterschied nicht - renpy.sound ist nach eigener Auskunft
## "a thin wrapper around music". Der Unterschied wird deshalb hier definiert,
## und die Sperre fragt nach dem Spielpfad, nicht nach dem Tonkanal
## (Entscheidung 24).
##
## KEIN TON BEWERTET JE EINE ENTSCHEIDUNG (Regel 3, Auftragspunkt 14). Es gibt
## in diesem Gerüst keinen Erfolgs- und keinen Fehlerklang, und es ist keine
## Stelle vorgesehen, an der einer entstehen könnte: Beide Tafeln sind über
## einen ORT und über eine STELLE IM ABLAUF geschlüsselt, nie über einen
## Ausgang, eine Wahl oder einen Wert.
##
## SOLANGE KEINE TONDATEI IM PROJEKT LIEGT, IST ES STILL. Das ist kein Mangel,
## den man sieht - anders als bei einem fehlenden Bild gibt es hier nichts zu
## verdecken und keinen Platzhalter zu zeigen. Die Zeilen der Tafeln sind
## deshalb der Bedarfsplan: Sie stehen in MEDIEN.md und werden von der
## Medienprobe als fehlend gezählt, genau wie die 326 fehlenden Bilddateien.


## Welcher Klangraum gerade läuft. Nicht welcher Ort - der wechselt mit jeder
## Karte, der Klangraum nicht. ortsklang_setzen() vergleicht dagegen und lässt
## den Klang stehen, solange er derselbe bleibt.
default ortsklang_aktuell = None


init -45 python:

    ## Die Klangräume #########################################################
    ##
    ## WORÜBER ORTSKLANG GESCHLÜSSELT WIRD - die Frage aus AUFGEFALLEN 108.
    ## Der Auftrag verlangt "je Ort ein Umgebungsklang", und einen Bestand von
    ## Orten gibt es in diesem Projekt nicht. Es gibt PFAD_ORT mit drei Zeilen
    ## und ein freies Textfeld ort an Ereignis, Szene und Einlage - ausgezählt
    ## 51 verschiedene Zeichenketten an 121 Inhalten.
    ##
    ## Beide naheliegenden Wege sind falsch:
    ##
    ##   drei Zeilen je Pfad   wäre nur eine zweite Fassung von PFAD_ORT. Auf
    ##                         front liefe sechs Kapitel lang derselbe Klang,
    ##                         und der Graben klänge wie das Ruhequartier.
    ##   51 Zeilen je Ortstext hinge den Schlüssel an ANZEIGETEXT. Wer
    ##                         "Grabenstellung" später in "Graben" umformuliert,
    ##                         bricht die Zuordnung STILL - genau die Falle, vor
    ##                         der Entscheidung 16 warnt und derentwegen
    ##                         KARTENTYP_VERGABE die Kennung als Schlüssel
    ##                         gewählt hat. Dazu sind die Texte nicht normiert
    ##                         (Lazarett, Etappenlazarett, Reservelazarett,
    ##                         Bahnhofslazarett stehen nebeneinander), und es
    ##                         hieße 51 Tondateien zu beschaffen.
    ##
    ## Deshalb ein Zwischenglied: der KLANGRAUM. Zehn Kennungen, gebildet
    ## danach, WIE ein Ort klingt, nicht danach, was er ist - eine Schreibstube
    ## und ein Bezirksamt klingen gleich, ein Wirtshaus und ein Wahllokal auch.
    ## ORT_KLANGRAUM bildet die Ortstexte darauf ab. Das ist dasselbe
    ## Zwei-Tafeln-Muster wie SCHRIFT_KANDIDATEN und SCHRIFT_ZWECK: eine Tafel
    ## für die Sache, eine für die Zuordnung.

    KLANGRAEUME = [
        "graben",
        "quartier",
        "lazarett",
        "nachschub",
        "schreibstube",
        "versammlung",
        "fabrik",
        "bahnhof",
        "strasse",
        "land",
    ]

    ## Was in jedem Klangraum zu hören wäre. Der Satz steht hier und nicht nur
    ## im Kopf des Beschaffenden: medienbedarf.py schreibt ihn nach MEDIEN.md,
    ## damit dort nicht "irgendein Ton für den Graben" steht.

    KLANGRAUM_ZWECK = {
        "graben": "Vorderste Stellung: Wind über der Brustwehr, ferner Einschlag",
        "quartier": "Unterkunft hinter der Linie: Stimmen, Holz, Schritte auf Lehm",
        "lazarett": "Saal mit vielen Betten: gedämpft, Schritte, entfernte Stimmen",
        "nachschub": "Magazin, Depot, Güterbahnhof: Kisten, Karren, Pferde",
        "schreibstube": "Amts- und Schreibstube: Feder, Stempel, halblautes Diktat",
        "versammlung": "Viele Menschen in einem Raum: Stimmengewirr, Stühle, Gläser",
        "fabrik": "Werkhalle: Maschinen, Riemen, Signalglocke",
        "bahnhof": "Halle und Bahnsteig: Hall, Dampf, Ansage in der Ferne",
        "strasse": "Stadt und Wohnviertel: Schritte, Karren, ferne Stimmen",
        "land": "Hof und Feldweg: Wind, Vögel, ein Tier",
    }

    ## Die Tafel ORTSKLANG ####################################################
    ##
    ## Auftragspunkt 12: je Ort ein Umgebungsklang, mit Dateiname, Lautstärke
    ## und der Angabe, ob er sich wiederholt. Genau diese drei Felder stehen
    ## hier, in dieser Reihenfolge:
    ##
    ##   Dateikennung  der Stamm des Dateinamens ohne Ordner und ohne Endung.
    ##                 Den vollständigen Pfad baut ton_pfad() - an einer
    ##                 einzigen Stelle, wie bild_pfad() bei den Bildern. Der
    ##                 Stamm steht trotzdem hier und wird nicht aus dem
    ##                 Klangraum abgeleitet: Eine Datei, die schon im Projekt
    ##                 liegt, behält ihren Namen, statt umbenannt zu werden.
    ##   Lautstärke    relativ, 0.0 bis 1.0, ÜBER dem Regler "Geräusche". Sie
    ##                 verstellt nichts, was die Lehrkraft eingestellt hat - sie
    ##                 sagt nur, wie laut dieser eine Klang im Verhältnis zu den
    ##                 anderen ist. Ein Umgebungsklang liegt unter dem Text und
    ##                 nicht darüber; deshalb steht keine Zeile über 0.40.
    ##   Wiederholung  True heißt: läuft in einer Schleife, solange der Ort
    ##                 derselbe bleibt. Heute steht bei allen zehn True, weil
    ##                 eine Umgebung nicht endet, während man an einem Ort ist.
    ##                 Das Feld steht trotzdem da: Ein einmaliger Klang - ein
    ##                 Glockenschlag zur vollen Stunde - bekäme False und liefe
    ##                 einmal durch.
    ##
    ## Es liegt heute keine einzige dieser Dateien im Projekt. Jede Zeile ist
    ## damit stumm, und die Medienprobe zählt sie als fehlend (Regel 7,
    ## Entscheidung 24). Das ist der Zweck der Tafel: Sie ist der Bedarfsplan.

    ORTSKLANG = {
        "graben": ("ort_graben", 0.35, True),
        "quartier": ("ort_quartier", 0.30, True),
        "lazarett": ("ort_lazarett", 0.25, True),
        "nachschub": ("ort_nachschub", 0.35, True),
        "schreibstube": ("ort_schreibstube", 0.25, True),
        "versammlung": ("ort_versammlung", 0.35, True),
        "fabrik": ("ort_fabrik", 0.40, True),
        "bahnhof": ("ort_bahnhof", 0.40, True),
        "strasse": ("ort_strasse", 0.30, True),
        "land": ("ort_land", 0.25, True),
    }

    ## Von der Ortsangabe zum Klangraum #######################################
    ##
    ## Alle 54 Ortsangaben des Projekts: die 51 Zeichenketten aus den ort=
    ## Feldern von Ereignis, Szene und Einlage, dazu die drei aus PFAD_ORT, auf
    ## die ort_text() zurückfällt. Ausgezählt am 6. September 2026 über alle
    ## .rpy-Dateien; die Tonprobe zählt sie bei jedem Lauf neu nach, indem sie
    ## den Bestand des Projekts fragt statt dieser Liste zu glauben (Regel 11).
    ##
    ## Wer einen Ortstext ändert oder einen neuen Inhalt anlegt, trägt ihn hier
    ## ein. Vergisst er es, fällt das Spiel auf den Klangraum des Pfades zurück
    ## und schreibt den Fall in ORT_OHNE_KLANGRAUM - das Spiel läuft weiter,
    ## die Probe schlägt Alarm.

    ORT_KLANGRAUM = {
        ## front - die vorderste Stellung und die Landschaften, in denen sie liegt
        "Grabenstellung": "graben",
        "Niemandsland": "graben",
        "Belgien": "graben",
        "Flandern": "graben",
        "Nordfrankreich": "graben",
        "Somme": "graben",
        "Verdun": "graben",
        "Westfront": "graben",

        ## Unterkunft - wo geschlafen, gewartet und gewechselt wird
        "Quartier": "quartier",
        "Ruhequartier": "quartier",
        "Etappenquartier": "quartier",
        "Ersatztruppenteil": "quartier",
        "Gefangenenlager": "quartier",

        ## Lazarett - vom Verbandplatz bis zum Reservelazarett in der Heimat
        "Lazarett": "lazarett",
        "Etappenlazarett": "lazarett",
        "Reservelazarett": "lazarett",
        "Bahnhofslazarett": "lazarett",
        "Verwundetensammelstelle": "lazarett",

        ## Nachschub - Kisten, Karren, Pferde
        "Magazin": "nachschub",
        "Munitionslager": "nachschub",
        "Pferdedepot": "nachschub",
        "Feldbäckerei": "nachschub",
        "Güterbahnhof": "nachschub",

        ## Schreibstube - jede Amtsstube, militärisch wie zivil. Sie klingen
        ## gleich: Feder, Stempel, ein halblautes Diktat, Warten auf dem Gang.
        "Schreibstube": "schreibstube",
        "Zensurstelle": "schreibstube",
        "Etappenkommandantur": "schreibstube",
        "Bezirksamt": "schreibstube",
        "Gemeindeamt": "schreibstube",
        "Meldebehörde": "schreibstube",
        "Versorgungsamt": "schreibstube",
        "Wohlfahrtsamt": "schreibstube",
        "Amtsgericht": "schreibstube",

        ## Versammlung - viele Menschen in einem Raum
        "Gemeindesaal": "versammlung",
        "Wahllokal": "versammlung",
        "Wirtshaus": "versammlung",

        ## Fabrik - Werkhalle und Werktor
        "Rüstungsbetrieb": "fabrik",
        "Arbeitsstelle": "fabrik",
        "Werktor": "fabrik",

        ## Bahnhof - Halle, Bahnsteig, Sammelstelle
        "Bahnhof": "bahnhof",
        "Bahnhofshalle": "bahnhof",
        "Bahnsteig": "bahnhof",
        "Sammelstelle": "bahnhof",

        ## Straße - Stadt und Wohnviertel, hier wie drüben. Der Etappenort
        ## steht mit dabei: Ein besetztes Dorf klingt nach Schritten, Karren
        ## und fernen Stimmen wie ein deutsches Wohnviertel auch. Der
        ## Unterschied liegt im Text und in den Menschen, nicht im Geräusch.
        "Wohnviertel": "strasse",
        "Straße": "strasse",
        "Stadtrand": "strasse",
        "Heimatstadt": "strasse",
        "Kreisstadt": "strasse",
        "Deutsches Kaiserreich": "strasse",
        "Etappe": "strasse",
        "Etappenort": "strasse",
        "Etappengebiet": "strasse",
        "Besetztes Dorf": "strasse",

        ## Land - Hof und Feldweg
        "Bauernhof": "land",
        "Landstraße": "land",
    }

    ## Der Klangraum, wenn ein Ortstext unbekannt ist. Der Rückfall geht über
    ## den PFAD und nicht über eine Vorgabe: Wer im Graben steht, soll den
    ## Graben hören, auch wenn jemand die Ortsangabe umformuliert hat.

    PFAD_KLANGRAUM = {
        "front": "graben",
        "etappe": "strasse",
        "heimat": "strasse",
    }

    ## Die Musiktafel #########################################################
    ##
    ## Entscheidung 24: Eine spätere Musikspur soll EINE TABELLENZEILE UND EINE
    ## DATEI kosten und keinen Umbau. Das ist diese Tabelle. Geschlüsselt ist
    ## sie nicht über Orte, sondern über STELLEN IM ABLAUF - denn genau so
    ## zählt Entscheidung 24 auf, wo Musik überhaupt möglich wäre: Hauptmenü,
    ## Moduswahl, Onboarding, Jahreskarte, Epilog, Lebenslauf und der
    ## Heimatpfad. Es sind dieselben Bildschirme, die keine Ortsangabe tragen.
    ##
    ## WELCHE DIESER STELLEN ES AM ENDE WERDEN, ENTSCHEIDET DOMINIK. Hier steht
    ## nur, dass die Tür offen ist. Der Schalter dazu ist MUSIK_EINGESCHALTET
    ## weiter unten; solange er auf False steht, gibt musik_setzen() an keiner
    ## Stelle etwas frei.
    ##
    ## Die Zeile "heimat" ist die einzige, die neben einem Umgebungsklang
    ## liefe. Wer sie einschaltet, hört beides übereinander; das ist zu
    ## bedenken, bevor der Schalter fällt.
    ##
    ## Felder wie bei ORTSKLANG: Dateikennung, Lautstärke, Wiederholung.

    STELLENMUSIK = {
        "hauptmenue": ("musik_hauptmenue", 0.30, True),
        "moduswahl": ("musik_moduswahl", 0.30, True),
        "onboarding": ("musik_onboarding", 0.30, True),
        "jahreskarte": ("musik_jahreskarte", 0.30, True),
        "epilog": ("musik_epilog", 0.30, True),
        "lebenslauf": ("musik_lebenslauf", 0.30, True),
        "heimat": ("musik_heimat", 0.25, True),
    }

    ## AUFTRAGSPUNKT 15: audio/stummer_morgen.mp3 BEKOMMT KEINE ZEILE.
    ##
    ## Die Datei liegt seit Beginn im Projekt und wird von keiner Zeile
    ## aufgerufen. Ihr ID3-Kopf sieht nach Inhalt aus - Titel "Stummer
    ## Morgen", Interpret, der Vermerk "made with suno", ein eingebettetes
    ## Titelbild, vier Minuten drei Sekunden. Sie ist trotzdem keiner:
    ## Dominik hat am 6. September gesagt, es sei **eine Probedatei**, mit der
    ## er etwas ausprobiert hat.
    ##
    ## Deshalb der zweite Weg, den Auftragspunkt 15 ausdrücklich offen lässt:
    ## Sie bleibt liegen und wird in MEDIEN.md als unbenutzt geführt. Genau
    ## so hält es das Projekt schon mit den beiden Kartenbildern
    ## front_beginn_*.png (AUFGEFALLEN 83) - eine Datei ohne Ort bleibt
    ## liegen, und entschieden wird nicht stillschweigend.
    ##
    ## Eine Tafelzeile darf eine Datei ANFORDERN, die noch fehlt - das ist
    ## der Bedarfsplan und ausdrücklich erwünscht (Entscheidung 24). Sie darf
    ## eine vorhandene Datei nicht VEREINNAHMEN.

    ## Die harte Sperre #######################################################
    ##
    ## Regel 3 und Auftragspunkt 13. Keine Vereinbarung, sondern eine Tafel,
    ## die ton_spielen() abfragt und die Probe ausliest - gefragt, nicht
    ## nachgebaut (Regel 11). Die Sperre fragt den SPIELPFAD ab und nicht den
    ## Tonkanal (Entscheidung 24): Ein Kanal ließe sich umgehen, indem jemand
    ## Musik auf dem Geräuschkanal spielt. Der Pfad lässt sich nicht umgehen.

    MUSIK_GESPERRT = ("front", "etappe")

    ## Dominiks Schalter. Solange er False ist, gibt musik_setzen() nirgends
    ## etwas frei - auch nicht dort, wo Entscheidung 24 Musik erlaubt. Die
    ## Aufrufstellen stehen trotzdem schon im Ablauf, denn sonst kostete eine
    ## spätere Musikspur mehr als die eine Tabellenzeile und die eine Datei,
    ## die Entscheidung 24 zugesagt hat. Dieselbe Bauart wie
    ## FIGUREN_ECHTE_BILDER: Tafel und Pfade sind da, der Zugriff ist aus.

    MUSIK_EINGESCHALTET = False

    ## Zwei Sammelbehälter ####################################################
    ##
    ## Bauart von KARTENTYP_UNBEKANNT und NACHTRAG_OHNE_TREFFER: Das Spiel
    ## läuft weiter, die Probe schlägt Alarm. Beide Listen sind im Spiel ohne
    ## Wirkung und werden allein von Probe 11 gelesen.
    ##
    ##   MUSIK_VERWORFEN      jeder Musikaufruf, den die harte Sperre verworfen
    ##                        hat, als (Stelle, Pfad). Die Abnahme dieses
    ##                        Schritts hängt daran: "ton_spielen() gibt auf
    ##                        front und etappe null Musikaufrufe frei" ist nur
    ##                        dann eine Messung und keine Zusicherung, wenn der
    ##                        verworfene Aufruf gezählt wird.
    ##   ORT_OHNE_KLANGRAUM   jede Ortsangabe, die ORT_KLANGRAUM nicht kennt.
    ##                        Sie ist kein Spielfehler - der Rückfall über den
    ##                        Pfad greift -, aber sie bedeutet, dass eine Zeile
    ##                        in der Tafel fehlt.

    MUSIK_VERWORFEN = []
    ORT_OHNE_KLANGRAUM = []

    ## Die Kanäle #############################################################
    ##
    ## Umgebungsklang läuft auf einem eigenen Kanal, Musik auf dem eingebauten
    ## Kanal "music". Beide hängen an einem Regler, den der
    ## Einstellungsbildschirm längst hat — am Bildschirm ist nichts zu ändern:
    ##
    ##   umgebung   eigener Kanal auf dem Mixer "sfx", also am Regler
    ##              "Geräusche". Eigen und nicht der eingebaute Kanal "sound",
    ##              damit eine Schleife nicht abbricht, sobald irgendwann ein
    ##              zweiter kurzer Ton kommt: Zwei Töne auf demselben Kanal
    ##              verdrängen einander. loop und tight gehören zu einer
    ##              nahtlosen Schleife.
    ##   music      der eingebaute Kanal auf dem Mixer "music", Regler "Musik".
    ##
    ## Ein eigener MIXER wäre der Fehler gewesen. Ren'Py legt ihn zwar
    ## klaglos an, aber er bliebe für die Lehrkraft unerreichbar, solange kein
    ## dritter Regler im Einstellungsbildschirm steht — das sagt Ren'Py in
    ## register_channel() selbst. Ein eigener KANAL auf einem vorhandenen
    ## Mixer hat dieses Problem nicht.

    renpy.music.register_channel("umgebung", mixer="sfx", loop=True, tight=True)

    TON_KANAL = {
        "umgebung": "umgebung",
        "musik": "music",
    }

    ## Ren'Py räumt beim Rücksprung ins Hauptmenü nur die Kanäle in
    ## config.main_menu_stop_channels ab, ab Werk "sound", "voice" und
    ## "movie", dazu "music" auf eigenem Weg. Ein selbst angemeldeter Kanal
    ## steht in keiner dieser Listen: Ohne diese Zeile liefe der Grabenklang
    ## unter dem Hauptmenü, unter dem Bestätigungsdialog und unter den
    ## Einstellungen weiter, bis jemand ein neues Spiel beginnt.
    config.main_menu_stop_channels = (
        list(config.main_menu_stop_channels) + ["umgebung"])

    ## Ein Klang setzt nicht schlagartig ein und bricht nicht ab. Anderthalb
    ## Sekunden sind lang genug, dass der Wechsel nicht auffällt, und kurz
    ## genug, dass zwei Klangräume sich nicht überlagern.
    TON_EINBLENDEN = 1.5
    TON_AUSBLENDEN = 1.5

    ## Kürzer als TON_AUSBLENDEN, und zwar mit Absicht: Wenn die harte Sperre
    ## eingreift, ist der Ton an diesem Ort verboten. Ein weiches Ausklingen
    ## über anderthalb Sekunden wäre anderthalb Sekunden Musik im Graben.
    TON_SPERRE_ABBRUCH = 0.4

    ## Beide Endungen sind gleichwertig; Ren'Py spielt sie ohne Unterschied.
    ## Zwei Kandidaten statt einer, damit eine Datei nicht umgewandelt werden
    ## muss, nur weil die Tafel ein Format vorschreibt — dasselbe Muster wie
    ## SCHRIFT_KANDIDATEN mit .ttf und .otf. Die Medienprobe führt beide als
    ## erwartet auf, und wie bei den Schriften genügt eine davon.
    TON_ENDUNGEN = ["ogg", "mp3"]

    ## Die Funktionen #########################################################

    def ton_pfad(dateikennung, endung):
        """Der Pfad einer Tondatei — die einzige Stelle.

        Auch die Medienprobe ruft diese Funktion, statt "audio/" ein zweites
        Mal davorzusetzen. Stünde die Regel zweimal da, liefe sie früher oder
        später auseinander, und dann glaubte jemand der falschen Liste
        (Regel 11).
        """
        return "audio/" + str(dateikennung) + "." + str(endung)

    def ton_kandidaten(dateikennung):
        return [ton_pfad(dateikennung, endung) for endung in TON_ENDUNGEN]

    def ton_waehlen(dateikennung):
        """Die erste Datei, die wirklich da ist — sonst None.

        Gebaut wie schrift_waehlen(): Kandidaten der Reihe nach, beim ersten
        Treffer zurück, sonst still zurückfallen. Der Pfad trägt den Ordner
        schon in sich; renpy.loadable() wird ABSICHTLICH ohne directory="audio"
        gerufen. Mit directory wäre der Aufruf im Spiel gleichwertig, aber die
        Werkbank wirft das Schlüsselwort weg — dieselbe Datei stünde dann
        zugleich als fehlend und als verwaist im Bericht.
        """
        for pfad in ton_kandidaten(dateikennung):
            if renpy.loadable(pfad):
                return pfad
        return None

    def musik_sperre_durchsetzen():
        """Beendet Musik, sobald der Pfad sie verbietet. Die eigentliche Sperre.

        Regel 3 verlangt, dass auf `front` und `etappe` **nie** Musik zu hören
        ist — nicht, dass dort keine gestartet wird. Der Unterschied ist nicht
        akademisch: Musik kann an einer Stelle angeworfen worden sein, an der
        sie erlaubt war (Hauptmenü, Moduswahl, Jahreskarte 1914), und der Pfad
        wird erst später entschieden. Eine Sperre, die nur das Anwerfen prüft,
        lässt sie dann bis in den Graben weiterlaufen.

        Sie wird an zwei Stellen gerufen, absichtlich doppelt: von
        `ton_spielen()`, sobald ein Aufruf verworfen wird, und von
        `pfad_wechseln()` in herkunft.rpy, sobald der Pfad feststeht. Beide
        laufen in jedem Durchgang — `lebenslage_abschluss` ruft unmittelbar
        nach der Musterung `musik_setzen("heimat")`, und jeder Kapitelwechsel
        ruft `musik_setzen("jahreskarte")`. Was an der Front angeworfen
        wurde, überlebt also höchstens bis zum nächsten dieser Punkte, und
        der erste davon liegt vor dem ersten Ereignis.

        Ausgeblendet wird kurz und nicht in der üblichen Zeit: Was hier
        endet, ist an diesem Ort verboten, und anderthalb Sekunden Musik im
        Graben sind anderthalb Sekunden zu viel.

        Geliefert wird True, wenn sie eingegriffen hat. Nur so kann Probe 11
        die Regel messen statt sie zu wiederholen.
        """
        if aktueller_pfad not in MUSIK_GESPERRT:
            return False
        if not renpy.music.get_playing(channel=TON_KANAL["musik"]):
            return False
        renpy.music.stop(channel=TON_KANAL["musik"], fadeout=TON_SPERRE_ABBRUCH)
        return True

    def musik_sperre_wacht():
        """Dieselbe Sperre, fortlaufend und ohne Ausblendung.

        Hängt in config.periodic_callbacks und ist die letzte Verteidigung:
        Sie gilt auch für Code, den es heute noch nicht gibt, und für jeden
        Weg, auf dem Musik in den Graben gelangen könnte, an den heute
        niemand denkt.

        Sie schneidet HART ab, während die beiden ausdrücklichen Stellen
        sanft ausblenden. Das hat zwei Gründe. Erstens: Wenn diese Wache
        eingreifen muss, ist schon etwas schiefgegangen — dann ist ein
        harter Schnitt richtig und nicht unhöflich. Zweitens ist es die
        Bedingung dafür, dass sie sich selbst beendet: Ein Titel, der
        ausblendet, meldet sich weiter als spielend, und die Wache liefe
        zwanzigmal je Sekunde in dieselbe Ausblendung hinein.
        """
        if aktueller_pfad not in MUSIK_GESPERRT:
            return False
        if not renpy.music.get_playing(channel=TON_KANAL["musik"]):
            return False
        renpy.music.stop(channel=TON_KANAL["musik"], fadeout=0.0)
        return True

    def ton_spielen(kennung, art="umgebung"):
        """Spielt einen Klang — die einzige Stelle, an der das Spiel Ton anlegt.

        Geliefert wird der gespielte Pfad oder None. Die Rückgabe ist nicht
        Zierde: Ren'Py verschluckt einen missglückten Tonaufruf stillschweigend
        (renpy/audio/music.py fängt jede Ausnahme ab), und in der Werkbank ist
        renpy.music ohnehin nur eine Attrappe. Ohne auswertbare Rückgabe wäre
        die Abnahme dieses Schritts — "auf front und etappe null Musikaufrufe
        freigegeben" — eine Zusicherung statt einer Messung.

        Fehlt die Datei, geschieht nichts: kein Fehler, keine Meldung im Spiel
        (Auftragspunkt 11). Sichtbar wird die Lücke allein in der Medienprobe.
        """
        if art not in TON_KANAL:
            return None

        zeile = (STELLENMUSIK if art == "musik" else ORTSKLANG).get(kennung)
        if zeile is None:
            return None

        ## DIE HARTE CODESPERRE (Regel 3, Auftragspunkt 13, Entscheidung 24).
        ## Gefragt wird der SPIELPFAD, nicht der Tonkanal: Ein Kanal ließe sich
        ## umgehen, indem jemand eine Musikdatei auf dem Geräuschkanal spielt.
        ## Der Pfad lässt sich nicht umgehen.
        ##
        ## Die Bedingung ist absichtlich umgekehrt formuliert — gesperrt ist
        ## alles AUSSER dem Umgebungsklang, nicht nur das, was heute "musik"
        ## heißt. Wer später eine dritte Art anlegt, muss sie ausdrücklich
        ## freistellen; vergisst er es, ist sie gesperrt. Eine harte Regel
        ## soll im Zweifel zu viel verbieten und nicht zu wenig.
        ##
        ## Und der verworfene Aufruf BEENDET, was läuft. Das ist der Kern:
        ## Eine Sperre, die nur das Anwerfen verhindert, ist keine. Im ersten
        ## Bau war sie genau das — `label start` wirft Musik dreimal an
        ## (Moduswahl, Onboarding, Jahreskarte), und dort steht
        ## `aktueller_pfad` noch auf der Vorgabe "heimat"; der Pfad fällt erst
        ## danach in `pfad_wechseln()`. Die Menümusik wäre also bis in den
        ## Graben durchgelaufen, ohne dass ein einziger Aufruf verworfen
        ## worden wäre.
        if art != "umgebung" and aktueller_pfad in MUSIK_GESPERRT:
            MUSIK_VERWORFEN.append((kennung, aktueller_pfad))
            musik_sperre_durchsetzen()
            return None

        dateikennung, lautstaerke, wiederholt = zeile
        pfad = ton_waehlen(dateikennung)
        if pfad is None:
            return None

        renpy.music.play(
            pfad,
            channel=TON_KANAL[art],
            loop=wiederholt,
            tight=wiederholt,
            fadein=TON_EINBLENDEN,
            relative_volume=lautstaerke,
            if_changed=True
        )
        return pfad

    def ton_still(art="umgebung"):
        """Beendet, was auf einem Kanal läuft. Ausgeblendet, nicht abgeschnitten."""
        global ortsklang_aktuell
        if art not in TON_KANAL:
            return
        if art == "umgebung":
            ortsklang_aktuell = None
        renpy.music.stop(channel=TON_KANAL[art], fadeout=TON_AUSBLENDEN)

    def ort_klangraum(ortsangabe):
        """Welcher Klangraum zu einer Ortsangabe gehört.

        Der Rückfall ist nicht still. Ein Ortstext, den ORT_KLANGRAUM nicht
        kennt, wird in ORT_OHNE_KLANGRAUM mitgeschrieben; das Spiel klingt
        deswegen nicht falsch — es klingt nach dem Pfad —, aber die Probe sagt,
        dass in der Tafel eine Zeile fehlt. Dieselbe Bauart wie
        KARTENTYP_UNBEKANNT: Das Spiel läuft weiter, die Probe schlägt Alarm.
        """
        text = (ortsangabe or "").strip()
        if text in ORT_KLANGRAUM:
            return ORT_KLANGRAUM[text]
        if text and text not in ORT_OHNE_KLANGRAUM:
            ORT_OHNE_KLANGRAUM.append(text)
        return PFAD_KLANGRAUM.get(aktueller_pfad, "strasse")

    def ortsklang_setzen(ortsangabe):
        """Der Umgebungsklang eines Ortes — die eine Stelle, die ORTSKLANG ruft.

        Sie wechselt den Klang nur, wenn der KLANGRAUM sich ändert, und nicht
        bei jeder Karte. Der Ort wechselt in diesem Spiel etwa alle zwanzig
        Sekunden; ein Klang, der so oft neu einsetzt, wäre im Klassenzimmer
        eine Störung und keine Atmosphäre. Grabenstellung und Niemandsland
        liegen im selben Klangraum — dazwischen geschieht nichts.

        Gibt nichts zurück, aus demselben Grund wie musik_setzen(): Sie darf
        in einem Bildschirm als action stehen können, ohne die Interaktion zu
        beenden.
        """
        global ortsklang_aktuell
        raum = ort_klangraum(ortsangabe)
        if raum == ortsklang_aktuell:
            return
        ortsklang_aktuell = raum
        ## Findet der neue Klangraum keine Datei, wird der ALTE beendet. Ohne
        ## diese Zeile bliebe die Schleife des vorigen Ortes stehen, während
        ## die Wechselprüfung den neuen längst als erledigt führt — und die
        ## Spielerin hörte über der Grabenkarte das Ruhequartier. Das ist der
        ## Normalfall während der Beschaffung: Es liegen ein paar Dateien,
        ## nicht zehn. Ein falscher Klang ist schlechter als kein Klang.
        if ton_spielen(raum, "umgebung") is None:
            renpy.music.stop(channel=TON_KANAL["umgebung"],
                             fadeout=TON_AUSBLENDEN)

    def musik_setzen(stelle):
        """Musik an einer Stelle im Ablauf — die eine Stelle, die STELLENMUSIK ruft.

        Der Schalter steht davor und nicht dahinter: Solange
        MUSIK_EINGESCHALTET auf False steht, wird gar nichts erst gefragt.
        Die Sperre in ton_spielen() bleibt davon unberührt — sie gilt auch
        dann, wenn der Schalter fällt, und wird von Probe 11 unabhängig vom
        Schalter gemessen.

        GIBT NICHTS ZURÜCK, und das ist keine Nachlässigkeit. Diese Funktion
        steht in screens.rpy als `on "show" action Function(...)`, und Ren'Pys
        `Function` sagt in der eigenen Dokumentation: „If the function returns
        a non-None value, the interaction stops and returns that value." Gäbe
        sie den gespielten Pfad zurück, beendete die erste Menümusik die
        Interaktion des Hauptmenüs — das Menü blitzte auf und das Spiel liefe
        von allein los, ohne dass jemand „Beginnen" geklickt hätte.
        Dasselbe gilt für ortsklang_setzen(). Was messbar sein muss, gibt
        ton_spielen() zurück; die beiden Eingänge geben nichts.
        """
        if not MUSIK_EINGESCHALTET:
            return
        ton_spielen(stelle, "musik")

    ## DIE SPERRE STEHT AUF DREI BEINEN, UND JEDES IST GEMESSEN.
    ##
    ##   1. ton_spielen() beendet, sobald es einen Aufruf verwirft. Damit
    ##      räumt jeder Musikaufruf auf einem gesperrten Pfad auf, statt nur
    ##      selbst zu schweigen — und musik_setzen("heimat") in
    ##      lebenslage_abschluss sowie musik_setzen("jahreskarte") an jedem
    ##      Kapitelwechsel laufen in jedem Durchgang durch.
    ##   2. pfad_wechseln() (herkunft.rpy) ruft die Sperre, sobald der Pfad
    ##      fällt. Das ist der früheste Punkt, an dem Regel 3 überhaupt gelten
    ##      kann, und er liegt vor dem ersten Ereignis.
    ##   3. musik_sperre_wacht() läuft fortlaufend über
    ##      config.periodic_callbacks (renpy/display/core.py:3017) und deckt
    ##      alles ab, woran heute niemand denkt.
    ##
    ## Bein 3 ist am 6. September einmal fälschlich verworfen worden: Ein
    ## Messlauf stürzte mit RecursionError ab, und ich hielt den Rückruf für
    ## die Ursache. Er war es nicht — der Absturz kam auch ohne ihn und
    ## steckte in renpy.pause() unter dem TESTRAHMEN. Gemessen wird seitdem
    ## über ein label splashscreen (offener Punkt 62), und dort läuft der
    ## Rückruf sauber durch.
    config.periodic_callbacks.append(musik_sperre_wacht)

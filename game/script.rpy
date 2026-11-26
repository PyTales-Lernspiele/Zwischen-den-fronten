init -20 python:

    WERTE_REIHENFOLGE = ["versorgung", "belastung", "aufmerksamkeit", "rueckhalt"]

    ## Die Beschriftungen benennen jetzt das Problem, nicht die Verwaltungsgröße.
    ## Dadurch bedeutet eine volle Anzeige bei allen vier Werten dasselbe:
    ## je voller, desto schlechter steht es um dich.
    WERT_BEZEICHNUNG = {
        "versorgung": "Hunger",
        "belastung": "Erschöpfung",
        "aufmerksamkeit": "Verdacht",
        "rueckhalt": "Einsamkeit",
    }

    WERT_HOCH_IST_GUT = {
        "versorgung": True,
        "belastung": False,
        "aufmerksamkeit": False,
        "rueckhalt": True,
    }

    WERT_ERKLAERUNG = {
        "versorgung": "Zeigt, wie satt du wirst. Lebensmittelkarten, lange Schlangen und teure Ware aus dem Schwarzhandel entscheiden darüber, was auf dem Tisch steht.",
        "belastung": "Zeigt, wie sehr Angst, Trauer, Gewalt und harte Arbeit an dir zehren. Schlaf, Ruhe und Menschen, die dir zuhören, bauen dich wieder auf.",
        "aufmerksamkeit": "Zeigt, wie genau Behörden, Militär und Nachbarn auf dich achten. Wer gegen Verbote verstößt oder auffällt, landet in Listen und Akten.",
        "rueckhalt": "Zeigt, wie viele Menschen zu dir halten: Familie, Kameraden, Nachbarn. Teilen, helfen und ehrlich sein bringen dir Rückhalt, Verrat kostet ihn.",
    }

    WERT_FOLGE = {
        "versorgung": "Je voller die Anzeige, desto weniger hast du zu essen. Ist sie ganz voll, endet der Durchgang.",
        "belastung": "Je voller die Anzeige, desto schwerer trägst du. Ist sie ganz voll, brichst du zusammen.",
        "aufmerksamkeit": "Je voller die Anzeige, desto genauer sieht man hin. Auf den letzten Stufen wirst du abgeholt.",
        "rueckhalt": "Eine volle Anzeige beendet den Durchgang nicht. Sie macht aber alles andere schwerer.",
    }

    WERT_MINIMUM = 0
    WERT_MAXIMUM = 12

    STUFEN_NAMEN = {
        "versorgung": ["Satt", "Knapp", "Hungrig", "Ausgezehrt", "Verhungernd"],
        "belastung": ["Ausgeruht", "Angespannt", "Erschöpft", "Am Ende", "Gebrochen"],
        "aufmerksamkeit": ["Unbekannt", "Aufgefallen", "Beobachtet", "In den Akten", "Gesucht"],
        "rueckhalt": ["Nicht allein", "Ein paar Leute", "Oft allein", "Ganz allein", "Ausgestoßen"],
    }

    ## Kurzdefinition jeder einzelnen Stufe. Wird in der Hover-Erklärung
    ## und in der Schlussauswertung angezeigt.
    STUFEN_KURZ = {
        "versorgung": [
            "Du wirst jeden Tag satt.",
            "Es reicht, wenn du gut einteilst.",
            "Du hast ständig Hunger.",
            "Du wirst schwach und schwindlig.",
            "Ohne Hilfe geht es nicht mehr weiter.",
        ],
        "belastung": [
            "Du schläfst und kommst zur Ruhe.",
            "Du bist nervös, hältst aber durch.",
            "Angst und Müdigkeit sind immer da.",
            "Du hältst kaum noch etwas aus.",
            "Du bist zusammengebrochen.",
        ],
        "aufmerksamkeit": [
            "Niemand achtet auf dich.",
            "Dein Name ist notiert worden.",
            "Man schaut dir genauer zu.",
            "Über dich wird eine Akte geführt.",
            "Man kommt, um dich zu holen.",
        ],
        "rueckhalt": [
            "Viele Menschen stehen zu dir.",
            "Einige halten noch zu dir.",
            "Du bist oft auf dich allein gestellt.",
            "Niemand fragt mehr nach dir.",
            "Alle gehen dir aus dem Weg.",
        ],
    }

    ## Hellere Fassung von FARBEN_STUFE für den dunklen Endbildschirm.
    FARBEN_STUFE_HELL = ["#8bb07f", "#c0b871", "#d3a75c", "#dc8b5f", "#d76a5e"]
    FARBE_SEGMENT_DUNKEL = "#39332b"

    ZUSTANDSSAETZE = {
        "versorgung": [
            "Es reicht. Heute denkst du nicht ans Essen.",
            "Du teilst dir das Brot ein und rechnest bis zum Wochenende.",
            "Der Gürtel sitzt zwei Löcher enger als im August 1914.",
            "Beim Aufstehen wird dir schwarz vor Augen.",
            "Deine Beine tragen dich kaum noch über die Straße.",
        ],
        "belastung": [
            "Du schläfst durch und wachst ohne Schrecken auf.",
            "Du liegst lange wach, aber am Morgen stehst du auf.",
            "Du zuckst zusammen, wenn eine Tür ins Schloss fällt.",
            "Deine Hände zittern, und du bekommst es nicht abgestellt.",
            "Du antwortest Stimmen, die niemand sonst hört.",
        ],
        "aufmerksamkeit": [
            "Bei keiner Behörde kennt jemand deinen Namen.",
            "Dein Name steht in einer Liste, die jemand angelegt hat.",
            "Man grüßt dich und sieht dabei einen Moment zu lange hin.",
            "Über dich liegt eine Akte, und sie wird dicker.",
            "Man fragt nach dir. Es ist eine Frage von Tagen.",
        ],
        "rueckhalt": [
            "Es gibt Menschen, die für dich einstehen würden.",
            "Ein paar Menschen halten zu dir, wenn du fragst.",
            "Die Grüße werden kürzer, die Gespräche seltener.",
            "Du gehst durch volle Straßen und sprichst mit niemandem.",
            "Man weicht dir aus. Niemand fragt mehr, wie es dir geht.",
        ],
    }

    STIMMUNG_STANDARD = "neutral"

    STIMMUNG_AUS_WERT = {
        "versorgung": "hungrig",
        "belastung": "erschoepft",
        "aufmerksamkeit": "angst",
        "rueckhalt": "einsam",
    }

    ## Die drei harten Abbrüche ###############################################
    ##
    ## SEIT PAKET 2, SCHRITT 3 steht aufmerksamkeit_ab auf 11 statt auf 10.
    ##
    ## Der Grund ist die Stufeneinteilung, nicht die Milde. stufe_von_wert()
    ## teilt jeden Wert in fünf Stufen; Stufe 4 ist die letzte und heißt für
    ## die Aufmerksamkeit "Gesucht - Man kommt, um dich zu holen". Sie
    ## beginnt bei 11. Die anderen beiden Abbrüche liegen genau dort:
    ##
    ##   versorgung unter 1   entspricht Stufe 4 ("Verhungernd")
    ##   belastung ab 12      entspricht Stufe 4 ("Gebrochen")
    ##   aufmerksamkeit ab 10 entsprach Stufe 3 ("In den Akten")
    ##
    ## Die Aufmerksamkeit holte also schon ab, während die Anzeige noch
    ## "Über dich liegt eine Akte" sagte. Das war ein Bruch zwischen dem,
    ## was das Spiel zeigt, und dem, was es tut. Mit 11 stimmt beides
    ## überein: Abgeholt wird, wer auf der letzten Stufe steht.
    ##
    ## Gemessen (2000 Durchgänge je Lage): Unter aufmerksamer Wahl war die
    ## Verhaftung mit 21,7 bis 87,7 Prozent der mit Abstand häufigste
    ## Ausgang - weil eine Spielerin den Verdacht erst schützt, wenn er
    ## bereits der schlechteste Wert ist, und dann ist es zu spät.
    ## SEIT PAKET 5, SCHRITT 3 steht aufmerksamkeit_ab auf 12 statt auf 11.
    ##
    ## Der Grund ist die Gleichbehandlung der beiden oberen Schwellen, und
    ## er ist aus der Zahl der Ziehungen begründet, wie es der Auftrag
    ## verlangt. Stufe 4 beginnt bei beiden Werten bei 11. Die Belastung
    ## bricht aber erst bei 12 ab, die Aufmerksamkeit brach schon bei 11 ab
    ## - also beim Eintritt in dieselbe Stufe, in der die Belastung noch
    ## einen Punkt Luft hat. Bei 17 Ziehungen fiel das kaum ins Gewicht;
    ## bei 32 ist es der Unterschied zwischen einem möglichen und dem
    ## üblichen Ausgang.
    ##
    ## Gemessen vor dieser Änderung (2000 Durchgänge je Lage, kluge Wahl):
    ## Die Verhaftung war auf allen sechs Lagen der häufigste Ausgang, von
    ## 39,7 Prozent an der Front bis 96,5 Prozent in der langen Etappe.
    ## Danach liegt sie zwischen 12 und 82 Prozent. Der Abbruch bleibt also
    ## möglich und spürbar; er ist nur nicht mehr die Regel.
    ##
    ## DIE SCHWELLEN LIEGEN DAMIT AM RAND DER SKALA. Die Werte laufen von
    ## 0 bis 12 (WERT_MAXIMUM); versorgung_unter 1 ist das Minimum,
    ## belastung_ab und aufmerksamkeit_ab 12 sind das Maximum. Wer künftig
    ## mehr Spielraum braucht, bekommt ihn nicht mehr hier, sondern nur
    ## noch über die Kosten der Karten oder über die Zahl der Ziehungen.
    ENDE_SCHWELLEN = {
        "versorgung_unter": 1,
        "belastung_ab": 12,
        "aufmerksamkeit_ab": 12,
    }

    KAPITEL_JAHRE = [1914, 1915, 1916]

    KAPITEL_UEBERSCHRIFT = {
        1914: "Der Krieg beginnt",
        1915: "Der Krieg wird Gewohnheit",
        1916: "Das Jahr der Materialschlachten",
    }

    KAPITEL_TEXT = {
        1914: "Die Mobilmachung ist angeordnet. Fast alle rechnen mit einem Feldzug von wenigen Monaten.",
        1915: "Die Fronten haben sich eingegraben. Im Februar werden in Berlin die ersten Brotkarten ausgegeben. Die Rechnung mit dem kurzen Krieg ist nicht aufgegangen.",
        1916: "Verdun und die Somme kosten Hunderttausende. In der Heimat entscheidet nicht mehr das Geld über das Essen, sondern die Karte und die Reihenfolge in der Schlange.",
    }

    KAPITEL_WIRKUNG = {
        1915: {"belastung": 1, "versorgung": -1},
        1916: {"belastung": 1, "versorgung": -2},
    }

    ## Drei Pfade seit Paket 2. Die Etappe liegt zwischen Front und
    ## Heimat: militärische Ordnung ohne Grabenkampf, bessere Verpflegung
    ## als daheim, dafür Aufsicht und Entfernung von allem Vertrauten.
    PFAD_REIHENFOLGE = ["front", "etappe", "heimat"]

    ## DER RÜCKHALT BEGINNT SEIT PAKET 5, SCHRITT 3 AUF ALLEN DREI PFADEN
    ## BEI 8. Vorher: Front 7, Etappe 6, Heimat 8.
    ##
    ## Der Grund ist keine Geschmacksfrage, sondern eine Kopplung, die
    ## niemand beabsichtigt hatte. schwaechster_wert() liefert den Wert mit
    ## der SCHLECHTESTEN STUFE, und die Kopfleiste zeigt genau diese Stufe.
    ## Wer aufmerksam spielt, schützt also den Balken, der am schlimmsten
    ## aussieht. Bei Rückhalt 7 und 6 war das zu Spielbeginn auf Front und
    ## Etappe der RÜCKHALT - und der Rückhalt ist der einzige der vier
    ## Werte OHNE Abbruchschwelle. Das Spiel brachte einer Spielerin also
    ## bei, den einen Wert zu schonen, an dem sie nicht scheitern kann,
    ## während Hunger, Erschöpfung und Verdacht weiterliefen.
    ##
    ## Gemessen (2000 Durchgänge je Lage): Unter kluger Wahl endeten an der
    ## Front 39,7 und in der Etappe 90,0 Prozent der Durchgänge mit einer
    ## Verhaftung - in der Heimat, wo die Versorgung von Anfang an die
    ## schlechteste Stufe hatte, nur 50,5. Mit Rückhalt 8 schützt die kluge
    ## Wahl auf allen drei Pfaden zuerst die Versorgung.
    ##
    ## Was die Pfade unterscheidet, steht damit nicht mehr im Rückhalt,
    ## sondern dort, wo es hingehört: Die Heimat hungert von Anfang an
    ## (Versorgung 6), die Etappe steht unter Aufsicht (Aufmerksamkeit 2)
    ## und ist dafür weniger erschöpft (Belastung 1), die Front trägt
    ## beides mittel. Die Entfernung von allem Vertrauten erzählen die
    ## Karten und der Jahreswechsel, nicht der Startwert.
    PFAD_BASIS = {
        "front": {"versorgung": 8, "belastung": 2, "aufmerksamkeit": 1, "rueckhalt": 8},
        "etappe": {"versorgung": 8, "belastung": 1, "aufmerksamkeit": 2, "rueckhalt": 8},
        "heimat": {"versorgung": 6, "belastung": 2, "aufmerksamkeit": 1, "rueckhalt": 8},
    }

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

    MODUS_BEZEICHNUNG = {
        "kurz": "Kurzer Verlauf",
        "lang": "Langer Verlauf",
    }

    ## ACHTUNG: DIESE ZAHLEN GELTEN NICHT MEHR.
    ##
    ## kapitel.rpy überschreibt MODUS_ZIELZAHL in einem init -19 Block mit
    ## 12 und 30. Da -19 nach -20 läuft, gewinnt die spätere Fassung. Was
    ## hier steht, ist der Stand vor Paket 3 und bleibt nur stehen, weil
    ## das Projekt keine fremden Dateien ausräumt, sondern in der eigenen
    ## Datei überschreibt (Regel 9).
    ##
    ## Wer die Zielzahl ändern will, ändert sie in kapitel.rpy, Abschnitt 2,
    ## zusammen mit KAPITEL_ZIEHUNGEN, MODUS_UMFANG und MODUS_DAUER. Eine
    ## Änderung HIER hat keine Wirkung.
    MODUS_ZIELZAHL = {
        "kurz": 9,
        "lang": 22,
    }

init -10 python:

    ## Seit Paket 2 gibt es keine festen Spielfiguren mehr. Der
    ## Personenstand entsteht in herkunft.rpy aus Milieu, Jahrgang,
    ## Musterung und Erwerbslage und liegt in der Variablen lebenslage.

    def pfad_liste(angabe):
        """Ein Ereignis darf für einen, mehrere oder alle Pfade gelten.

        Erlaubt sind: "front", "etappe", "heimat", "beide" (alle drei)
        oder eine Liste wie ["front", "etappe"].
        """
        if angabe is None:
            return list(PFAD_REIHENFOLGE)
        if isinstance(angabe, (list, tuple)):
            return list(angabe)
        if angabe == "beide":
            return list(PFAD_REIHENFOLGE)
        return [angabe]

    class Option(object):

        def __init__(self, titel, beschreibung, ausgang, hinweis=None,
                     aenderungen=None, merkmale=None, varianten=None,
                     sprung=None, bild=None, stimmung=None,
                     kette=None, kette_ab=0):
            self.titel = titel
            self.beschreibung = beschreibung
            self.ausgang = ausgang
            self.hinweis = hinweis
            self.aenderungen = aenderungen if aenderungen else {}
            self.merkmale = merkmale if merkmale else []
            self.varianten = varianten if varianten else []
            self.sprung = sprung
            self.bild = bild
            self.stimmung = stimmung
            self.kette = kette
            self.kette_ab = kette_ab

    ############################################################################
    ## DAS QUELLENFORMAT
    ############################################################################
    ##
    ## SEIT PAKET 3, SCHRITT 1. Vorher war quelle eine freie Zeichenkette
    ## und stand bei null von 42 Ereignissen. Ein Spiel, das im Unterricht
    ## behauptet, so sei es gewesen, muss sagen können, woher es das weiß.
    ##
    ## quelle ist ab jetzt ein Wörterbuch mit genau diesen Schlüsseln:
    ##
    ##   "kurz"        Kurzbeleg für die Anzeige, höchstens 60 Zeichen.
    ##   "voll"        Vollbeleg: Urheber, Titel, Ort, Jahr, Fundstelle.
    ##                 Wo kein Beleg vorliegt, steht dort wörtlich
    ##                 "BELEG FEHLT - zu recherchieren", und "einordnung"
    ##                 sagt, welche Quelle gesucht wird und wo sie liegen
    ##                 dürfte.
    ##   "art"         eine von: bild, akte, brief, zeitung, gesetz,
    ##                 statistik, erinnerung, darstellung.
    ##   "zitat"       wahlweise, HÖCHSTENS 15 WÖRTER, wörtlich.
    ##   "einordnung"  GENAU ZWEI SÄTZE: was die Quelle zeigt und was sie
    ##                 nicht zeigt.
    ##
    ## NICHTS WIRD ERFUNDEN. Keine Signatur, kein Zitat, kein Titel, den es
    ## nicht gibt. Ein ehrliches "BELEG FEHLT" ist mehr wert als eine
    ## erfundene Aktennummer, die im Unterricht jemand nachschlägt.
    ##
    ## Beispiel, vollständig ausgefüllt:
    ##
    ##     quelle={
    ##         "kurz": "Hilfsdienstgesetz vom 5. Dezember 1916",
    ##         "voll": "Gesetz über den vaterländischen Hilfsdienst vom "
    ##                 "5. Dezember 1916, Reichsgesetzblatt 1916",
    ##         "art": "gesetz",
    ##         "einordnung": "Das Gesetz verpflichtet jeden Mann zwischen "
    ##                       "17 und 60 zur Arbeit, wenn er nicht Soldat "
    ##                       "ist. Wie es im einzelnen Betrieb angewandt "
    ##                       "wurde, steht darin nicht.",
    ##     }
    ##
    ## Ab Paket 4 wird jedes neue Ereignis und jede neue Einlage MIT
    ## quelle geboren. Ein Inhalt ohne Beleg ist dann kein Rückstand mehr,
    ## sondern ein Fehler, und Probe 5 meldet ihn als solchen.
    ##
    ## Dasselbe Format gilt für Einlage.quelle (minispiele.rpy).

    ## Die erlaubten Werte für "art". Probe 5 prüft dagegen.
    QUELLE_ARTEN = ["bild", "akte", "brief", "zeitung", "gesetz",
                    "statistik", "erinnerung", "darstellung"]

    ## Wörtlich so, damit die Probe danach suchen kann.
    QUELLE_FEHLT = "BELEG FEHLT - zu recherchieren"

    def quelle_kurz(quelle):
        """Die eine Zeile, die im Analysemodus unter dem Text steht.

        Verträgt auch die alte Fassung, in der quelle eine schlichte
        Zeichenkette war. Wer eine solche findet, trägt sie ins neue
        Format um; abstürzen soll deswegen nichts.
        """
        if not quelle:
            return ""
        if isinstance(quelle, dict):
            return quelle.get("kurz", "")
        return str(quelle)

    ############################################################################
    ## DIE KARTENTYPEN
    ############################################################################
    ##
    ## SEIT PAKET 8, SCHRITT 1. Bis dahin sah jede Entscheidungskarte gleich
    ## aus: ein Bogen Papier mit Motiv, Titel und Beschreibung. Für eine Szene
    ## ist das richtig, für ein Dokument falsch. Eine Brotkarte ist kein Bogen
    ## Papier — sie ist ein Raster aus abtrennbaren Abschnitten. Eine Zeitung
    ## hat Spalten und eine Balkenüberschrift. Ein Bescheid hat einen
    ## Behördenkopf und ein Stempelfeld.
    ##
    ## Der Typ steht am EREIGNIS und nicht an der Option: Beide Karten eines
    ## Ereignisses zeigen dasselbe Dokument, nur zwei Wege, damit umzugehen.
    ##
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

    ## Ein Tippfehler im Typ darf NICHT still auf die Vorgabe zurückfallen.
    ## Dann sähe eine Brotkarte aus wie eine Szene, und niemand merkte es —
    ## es gäbe keine Fehlermeldung, nur ein falsches Bild. Dieselbe Bauart
    ## wie NACHTRAG_OHNE_TREFFER (Entscheidung 16): Das Spiel läuft weiter,
    ## die Probe schlägt Alarm.
    KARTENTYP_UNBEKANNT = []

    ## Welcher Bildordner zu einem Typ gehört. Ein Dokument ist eine eigene
    ## Bildsorte: Wer eine Brotkarte sucht, sucht in einem anderen Bestand
    ## als wer eine Frontszene sucht — und MEDIEN.md soll ihm das sagen.
    ## Das ist zugleich die aufrufende Stelle, die BILD_MASSE["dokumente"]
    ## bis heute gefehlt hat.
    def kartenbild_kategorie(kartentyp):
        if kartentyp and kartentyp != "karte":
            return "dokumente"
        return "karten"

    def kartenmotiv(vorlage, auswahl, breite=468, hoehe=264):
        """Das Motiv einer Entscheidungskarte — die einzige Stelle.

        Auch die Medienprobe ruft diese Funktion. Stünde die Zuordnung von
        Typ zu Ordner ein zweites Mal in der Werkbank, liefe sie früher oder
        später auseinander, und dann glaubte jemand der falschen Liste
        (Regel 11).
        """
        kategorie = kartenbild_kategorie(getattr(vorlage, "kartentyp", "karte"))
        return bild_anzeigen(kategorie, auswahl.bild, breite, hoehe)

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
            self.quelle = quelle
            self.stimmung = stimmung
            self.nur_kette = nur_kette
            self.wiederholbar = wiederholbar
            if kartentyp not in KARTENTYPEN:
                KARTENTYP_UNBEKANNT.append((kennung, kartentyp))
                kartentyp = "karte"
            self.kartentyp = kartentyp
            zaehler = 1
            for option in self.optionen:
                if not option.bild:
                    option.bild = kennung + "_" + str(zaehler)
                zaehler = zaehler + 1


init -5 python:

    def jahrestext(wert, jahr):
        if not isinstance(wert, dict):
            return wert
        if jahr in wert:
            return wert[jahr]
        gefunden = None
        schluessel = sorted([k for k in wert.keys() if isinstance(k, int)])
        for eintrag in schluessel:
            if eintrag <= jahr:
                gefunden = wert[eintrag]
        if gefunden is not None:
            return gefunden
        if schluessel:
            return wert[schluessel[0]]
        return wert.get("standard", "")

    def wert_begrenzen(zahl):
        if zahl < WERT_MINIMUM:
            return WERT_MINIMUM
        if zahl > WERT_MAXIMUM:
            return WERT_MAXIMUM
        return zahl

    ############################################################################
    ## WIE VOLL EIN WERTEBALKEN STEHT
    ############################################################################
    ##
    ## PAKET 8, SCHRITT 2.1 — die Umsetzung von Entscheidung 4:
    ## **Ein voller Balken heißt überall "hier stehst du gut da."**
    ##
    ## Der Auftrag beschreibt die Umstellung als "für belastung und
    ## aufmerksamkeit zeichnet der Balken WERT_MAXIMUM minus Wert". So war
    ## es einmal gebaut; heute ist es das nicht mehr, und die Beschreibung
    ## führt in die Irre (Regel 9 — im Auftrag steht ein Hinweis, kein
    ## Beweis). Der Balken kennt den Rohwert gar nicht: Er zeichnet die
    ## STUFE, und stufe_von_wert() dreht die Richtung längst — Stufe 0 ist
    ## bei allen vier Werten die gute Lage.
    ##
    ## Die Balken waren also schon einheitlich, nur verkehrt herum: Gefüllt
    ## wurde von Stufe 0 aufwärts, ein voller Balken hieß "am Ende". Wer in
    ## fünfundvierzig Sekunden entscheidet, liest das falsch herum.
    ##
    ## Gedreht wird deshalb an genau EINER Stelle, hier. Drei Bildschirme
    ## zeichnen einen Wertebalken — die Kopfleiste, der Endbildschirm und
    ## der Lebenslauf —, und alle drei fragen diese Funktion. Stünde die
    ## Bedingung dreimal da, würde beim nächsten Umbau eine davon vergessen,
    ## und der Auftrag sagt zu Recht: eine vergessene Stelle ist schlimmer
    ## als gar keine Änderung.
    ##
    ## NICHT geändert werden dadurch: WERT_HOCH_IST_GUT, ENDE_SCHWELLEN,
    ## stufe_von_wert(), die Stufenfarben, die Namen und die Zustandssätze.
    ## Die Rechnung bleibt, wie sie ist — probe_alles.py muss danach exakt
    ## dieselben Zahlen liefern, und genau das ist die Abnahme dieses
    ## Unterabschnitts.
    SEGMENTE_JE_BALKEN = 5

    def segment_gefuellt(feld, stufe):
        """Ob das Segment Nummer feld (von 0 an) noch gefüllt ist.

        Bei Stufe 0 sind alle fünf gefüllt, bei Stufe 4 nur noch eines —
        genau gespiegelt zu vorher, wo es umgekehrt war. Ein Restsegment
        bleibt mit Absicht stehen: Ein völlig leerer Balken ist als Balken
        nicht mehr zu erkennen, und Stufe 4 heißt "am Ende", nicht "tot".
        """
        return feld <= (SEGMENTE_JE_BALKEN - 1 - stufe)

    def stufe_von_wert(schluessel, wert):
        if WERT_HOCH_IST_GUT.get(schluessel, True):
            gemessen = WERT_MAXIMUM - wert
        else:
            gemessen = wert
        if gemessen <= 1:
            return 0
        if gemessen <= 4:
            return 1
        if gemessen <= 7:
            return 2
        if gemessen <= 10:
            return 3
        return 4

    def zustand_lesen():
        return {
            "versorgung": versorgung,
            "belastung": belastung,
            "aufmerksamkeit": aufmerksamkeit,
            "rueckhalt": rueckhalt,
        }

    def zustand_aendern(aenderungen):
        global versorgung, belastung, aufmerksamkeit, rueckhalt, letzte_aenderungen
        if not aenderungen:
            letzte_aenderungen = {}
            return
        vorher = zustand_lesen()
        versorgung = wert_begrenzen(versorgung + aenderungen.get("versorgung", 0))
        belastung = wert_begrenzen(belastung + aenderungen.get("belastung", 0))
        aufmerksamkeit = wert_begrenzen(aufmerksamkeit + aenderungen.get("aufmerksamkeit", 0))
        rueckhalt = wert_begrenzen(rueckhalt + aenderungen.get("rueckhalt", 0))
        nachher = zustand_lesen()
        ergebnis = {}
        for schluessel in WERTE_REIHENFOLGE:
            ergebnis[schluessel] = nachher[schluessel] - vorher[schluessel]
        letzte_aenderungen = ergebnis

    def schwaechster_wert():
        gewaehlt = WERTE_REIHENFOLGE[0]
        hoechste = -1
        werte = zustand_lesen()
        for schluessel in WERTE_REIHENFOLGE:
            stufe = stufe_von_wert(schluessel, werte[schluessel])
            if stufe > hoechste:
                hoechste = stufe
                gewaehlt = schluessel
        return gewaehlt

    def zustandssatz_text():
        schluessel = schwaechster_wert()
        stufe = stufe_von_wert(schluessel, zustand_lesen()[schluessel])
        return ZUSTANDSSAETZE[schluessel][stufe]

    def stimmung_bestimmen():
        if stimmung_erzwungen:
            return stimmung_erzwungen
        schluessel = schwaechster_wert()
        stufe = stufe_von_wert(schluessel, zustand_lesen()[schluessel])
        if stufe <= 1:
            return STIMMUNG_STANDARD
        return STIMMUNG_AUS_WERT.get(schluessel, STIMMUNG_STANDARD)

    def stimmung_setzen(wert):
        global stimmung_erzwungen
        stimmung_erzwungen = wert

    def portrait_kennung():
        """Bildkennung des Hauptcharakters.

        Seit Paket 2 nicht mehr der Name einer festen Figur, sondern
        Herkunft und Geschlecht. Die Funktion steht in herkunft.rpy.
        """
        return lebenslage_bildkennung()

    def analyse_text(schluessel):
        wert = zustand_lesen()[schluessel]
        veraenderung = letzte_aenderungen.get(schluessel, 0)
        if veraenderung > 0:
            zusatz = " (+" + str(veraenderung) + ")"
        elif veraenderung < 0:
            zusatz = " (" + str(veraenderung) + ")"
        else:
            zusatz = ""
        return str(wert) + "/" + str(WERT_MAXIMUM) + zusatz

    def merkmal_setzen(name):
        global merkmale
        if name and name not in merkmale:
            merkmale = merkmale + [name]

    def hat_merkmal(name):
        return name in merkmale

    def datum_text():
        return "Jahr " + str(aktuelles_jahr) + " - " + MODUS_BEZEICHNUNG.get(spielmodus, "")

    ## Beide Texte kommen aus der Lebenslage (herkunft.rpy). Sie sind
    ## reine Anzeige. Keine Bedingung im Spiel darf sich auf sie stützen.

    def rollen_text():
        return person_name()

    def berufs_text():
        return person_stand()

    def ort_text():
        return PFAD_ORT.get(aktueller_pfad, "")

    def protokoll_eintragen(kennung, wahl):
        global protokoll
        protokoll = protokoll + [{
            "jahr": aktuelles_jahr,
            "ereignis": kennung,
            "wahl": wahl,
        }]

    def zustand_zuruecksetzen():
        global versorgung, belastung, aufmerksamkeit, rueckhalt
        global merkmale, gespielte_ereignisse, protokoll, letzte_aenderungen
        global aktuelles_jahr, aktueller_pfad, lebenslage, musterungsdaten
        global vorgemerkte_ereignisse, ziehungen_im_kapitel, stimmung_erzwungen
        ## Startwerte der Heimatgrundlage. Die Herkunftswahl in
        ## herkunft.rpy setzt sie unmittelbar danach neu.
        versorgung = PFAD_BASIS["heimat"]["versorgung"]
        belastung = PFAD_BASIS["heimat"]["belastung"]
        aufmerksamkeit = PFAD_BASIS["heimat"]["aufmerksamkeit"]
        rueckhalt = PFAD_BASIS["heimat"]["rueckhalt"]
        merkmale = []
        gespielte_ereignisse = []
        protokoll = []
        letzte_aenderungen = {}
        vorgemerkte_ereignisse = []
        ziehungen_im_kapitel = 0
        stimmung_erzwungen = None
        aktuelles_jahr = KAPITEL_JAHRE[0]
        aktueller_pfad = "heimat"
        lebenslage = None
        musterungsdaten = None

    def ziehungen_pro_kapitel():
        ziel = MODUS_ZIELZAHL.get(spielmodus, 22)
        anzahl = max(1, len(KAPITEL_JAHRE))
        return max(1, int(round(float(ziel) / anzahl)))

    def wiederholbare_freigeben():
        global gespielte_ereignisse
        rest = []
        for kennung in gespielte_ereignisse:
            vorlage = EREIGNIS_INDEX.get(kennung)
            if vorlage is not None and vorlage.wiederholbar:
                continue
            rest.append(kennung)
        gespielte_ereignisse = rest

    def naechstes_kapitel(jahr):
        if jahr not in KAPITEL_JAHRE:
            return None
        stelle = KAPITEL_JAHRE.index(jahr)
        if stelle + 1 >= len(KAPITEL_JAHRE):
            return None
        return KAPITEL_JAHRE[stelle + 1]

    def ende_pruefen():
        if versorgung < ENDE_SCHWELLEN["versorgung_unter"]:
            return "ende_verhungert"
        if belastung >= ENDE_SCHWELLEN["belastung_ab"]:
            return "ende_zusammenbruch"
        if aufmerksamkeit >= ENDE_SCHWELLEN["aufmerksamkeit_ab"]:
            return "ende_verhaftet"
        return None

    def auswertung_liste():
        zeilen = []
        werte = zustand_lesen()
        for schluessel in WERTE_REIHENFOLGE:
            stufe = stufe_von_wert(schluessel, werte[schluessel])
            zeilen.append({
                "schluessel": schluessel,
                "stufe": stufe,
                "name": WERT_BEZEICHNUNG[schluessel],
                "stufenname": STUFEN_NAMEN[schluessel][stufe],
                "satz": STUFEN_KURZ[schluessel][stufe],
            })
        return zeilen

    def wert_aufzaehlung(namen):
        if not namen:
            return ""
        if len(namen) == 1:
            return namen[0]
        return ", ".join(namen[:-1]) + " und " + namen[-1]

    def auswertung_fazit():
        werte = zustand_lesen()
        stufen = {}
        for schluessel in WERTE_REIHENFOLGE:
            stufen[schluessel] = stufe_von_wert(schluessel, werte[schluessel])
        schwer = [WERT_BEZEICHNUNG[s] for s in WERTE_REIHENFOLGE if stufen[s] >= 3]
        mittel = [WERT_BEZEICHNUNG[s] for s in WERTE_REIHENFOLGE if stufen[s] == 2]
        if not schwer and not mittel:
            return "Du bist erstaunlich gut durch diese Jahre gekommen. Für die meisten Menschen im Deutschen Reich galt das nicht."
        if not schwer:
            return "Du hast durchgehalten, aber der Krieg hat Spuren hinterlassen: " + wert_aufzaehlung(mittel) + "."
        if len(schwer) == 1:
            return "Am schwersten wiegt am Ende: " + schwer[0] + ". Daran zerbrachen in diesen Jahren viele Lebenswege."
        return "Mehreres kommt zusammen: " + wert_aufzaehlung(schwer) + ". Aus solchen Lagen entstand die Erbitterung, die nach 1918 die Politik bestimmte."

    def bilanz_text():
        zeilen = []
        for eintrag in auswertung_liste():
            zeilen.append(eintrag["name"] + ": " + eintrag["stufenname"])
        return "\n".join(zeilen)

    def lebenslauf_text():
        if lebenslage is None:
            return ""
        zeilen = []
        zeilen.append(person_kurz())
        zeilen.append(person_stand())
        if lebenslage.musterung:
            zeilen.append("Musterung: " + musterung_kurztext())
        zeilen.append(PFAD_MARKE.get(aktueller_pfad, "") + ", " + PFAD_ORT.get(aktueller_pfad, ""))
        zeilen.append("August 1914 bis " + str(aktuelles_jahr))
        zeilen.append(str(len(protokoll)) + " Entscheidungen getroffen")
        return "\n".join(zeilen)

    def protokoll_text():
        if not protokoll:
            return "Keine Einträge."
        zeilen = []
        for eintrag in protokoll:
            zeilen.append(str(eintrag["jahr"]) + "  " + eintrag["ereignis"] + "  ->  " + eintrag["wahl"])
        return "\n".join(zeilen)


init python:

    ############################################################################
    ## ZAHLENDURCHGANG PAKET 2, SCHRITT 3
    ############################################################################
    ##
    ## An diesem Bestand wurde in Paket 2 kein einziger Satz geändert. Was
    ## sich geändert hat, sind zwölf Zahlen - je eine Option in zwölf
    ## Ereignissen, die vorher eine EINBAHNSTRASSE waren: Beide Optionen
    ## verschlechterten denselben Wert, meist die Erschöpfung. Wer so eine
    ## Karte zieht, entscheidet nicht mehr, er zahlt nur noch.
    ##
    ## Gemessen wurde vorher eine mittlere Erschöpfung von +0,35 bis +0,50
    ## je Ziehung. Bei dreißig Ziehungen im langen Verlauf sind das allein
    ## aus den Ereignissen zwölf Punkte - genau die Schwelle, ab der der
    ## Durchgang mit Zusammenbruch endet. Im langen Verlauf erreichten
    ## deshalb 0,6 bis 1,1 Prozent der Durchgänge das Jahr 1919.
    ##
    ## Geändert wurde immer die Option, deren AUSGANGSTEXT die Entlastung
    ## schon beschreibt. Beispiele: "aber du schläfst", "Du bist als Erster
    ## fertig und schläfst zwei Stunden", "Für drei Tage ist Ruhe", "Du
    ## bekommst Luft". Der Text stand vorher da und stand im Widerspruch
    ## zur Zahl daneben; aufgelöst wurde der Widerspruch zugunsten des
    ## Textes.
    ##
    ## Die zwölf Ereignisse:
    ##   front_1914_erster_toter   front_1914_schanzen    front_gas
    ##   front_laeuse              front_1916_verdun      front_1916_hunger
    ##   front_1916_gefangener     heimat_todesnachricht  heimat_1915_brotkarte
    ##   heimat_unterstuetzung     heimat_hamsterfahrt    heimat_1916_rueben
    ##
    ## Der Handel bleibt in jedem Fall bestehen: Wer die Erschöpfung spart,
    ## zahlt mit Hunger, Verdacht oder Einsamkeit. Keine der zwölf Karten
    ## hat dadurch eine erkennbar richtige Wahl bekommen; die Probe 4 in
    ## bericht.txt weist das mit zwei Wahlstrategien nach.
    ##
    ## Wer hier Zahlen ändert, lässt danach probe_alles.py laufen und sieht
    ## sich Probe 4 an. Die Grenzen stehen dort.

    EREIGNISSE = [

        Ereignis(
            "front_1914_marsch", [1914], "front",
            "Seit fünf Uhr früh gehst du, und die Sonne steht schon hoch. "
            "Die Riemen des Tornisters ziehen sich in die Schultern. Vierzig "
            "Kilometer sind für heute befohlen, der Wasserwagen ist seit "
            "gestern weg. Im Straßengraben liegen Konserven und Zeltbahnen "
            "von denen, die vor euch gingen.",
            [
                Option(
                    "Das Gepäck erleichtern",
                    "Zwei Konserven und die Zeltbahn bleiben im Graben.",
                    "Ab dem Mittag zieht der Riemen nicht mehr so tief. Der "
                    "Feldwebel sieht die leere Stelle am Tornister und sagt "
                    "heute nichts. Am Abend ist dein Brotbeutel leichter, als "
                    "er sein dürfte.",
                    hinweis="gegen die Vorschrift",
                    aenderungen={"belastung": -1, "aufmerksamkeit": 1, "versorgung": -1}
                ),
                Option(
                    "Alles weitertragen",
                    "Du schleppst die vorgeschriebene Last bis zum Quartier.",
                    "Am Abend bist du zu müde, um deine Ration zu essen. Die "
                    "Strümpfe kleben in den Stiefeln fest, und du lässt sie an. "
                    "Beim Aufstehen weißt du schon, wie deine Füße aussehen.",
                    aenderungen={"belastung": 2}
                ),
            ],
            ort="Belgien", kern=True, gewicht=14,
            quelle={
                "kurz": "Marschleistungen im Aufmarsch August 1914",
                "voll": QUELLE_FEHLT,
                "art": "darstellung",
                "einordnung": "Gesucht wird ein Regiments- oder Kriegstagebuch "
                              "mit Tagesmärschen und Ausfällen aus dem Aufmarsch "
                              "durch Belgien. Solche Bücher liegen in den "
                              "Landesarchiven und im Bundesarchiv, die "
                              "Marschleistung selbst steht in keiner "
                              "zusammenfassenden Statistik.",
            }
        ),

        Ereignis(
            "front_1914_dorf", [1914], "front",
            "Im Keller ist es kühl, und es riecht nach Erde und Essig. Auf "
            "dem Regal stehen zwei Reihen Einweckgläser, daneben zwei Fässer. "
            "Die Leute sind vor drei Tagen fort, die Betten sind noch "
            "gemacht. „Das verdirbt sowieso“, sagt einer hinter dir und "
            "nimmt schon das erste Glas.",
            [
                Option(
                    "Den Brotbeutel füllen",
                    "Du nimmst, was hineingeht, und teilst mit der Gruppe.",
                    "Für einen Abend seid ihr satt und redet laut. Am Morgen "
                    "steht die Kellertür offen, und niemand spricht darüber. "
                    "Der Essiggeruch hängt zwei Tage in deiner Decke.",
                    hinweis="verboten",
                    aenderungen={"versorgung": 2, "aufmerksamkeit": 1, "rueckhalt": 1}
                ),
                Option(
                    "Bei der Kommandantur melden",
                    "Du gibst den Fund weiter, wie es der Befehl verlangt.",
                    "Ein Wagen holt die Gläser noch am selben Nachmittag ab. "
                    "Der Hauptmann sagt deinen Namen und nickt dir zu. Am "
                    "Abend rückt beim Essen niemand zur Seite.",
                    aenderungen={"aufmerksamkeit": -1, "rueckhalt": -1}
                ),
            ],
            ort="Nordfrankreich", gewicht=8,
            quelle={
                "kurz": "Requisition und Plünderungsverbot im Feldheer",
                "voll": QUELLE_FEHLT,
                "art": "gesetz",
                "einordnung": "Gesucht wird die Requisitionsvorschrift des "
                              "Feldheeres, die den Umgang mit Vorräten in "
                              "geräumten Orten regelt. Sie sagt, was befohlen "
                              "war, nicht, was in den Kellern tatsächlich "
                              "geschah.",
            }
        ),

        Ereignis(
            "front_1914_erster_toter", [1914], "front",
            "Er liegt am Wegrand, und die Kolonne geht rechts an ihm vorbei. "
            "Zwanzig Jahre alt, aus dem Nachbardorf, seit gestern in deiner "
            "Gruppe. Der Staub der Vorderen legt sich auf sein Gesicht. "
            "Anhalten ist nicht befohlen, und niemand hält an.",
            [
                Option(
                    "Etwas an sich nehmen",
                    "Die Erkennungsmarke und den Brief an seine Mutter.",
                    "Du trägst beides drei Wochen in der Brusttasche. Im "
                    "nächsten Etappenort wirfst du den Brief in einen "
                    "Feldpostkasten. Was du dazugeschrieben hast, weißt du "
                    "später nicht mehr.",
                    aenderungen={"belastung": 1, "rueckhalt": 1},
                    stimmung="einsam"
                ),
                Option(
                    "Im Glied bleiben",
                    "Anhalten ist nicht vorgesehen.",
                    "Du siehst nach vorn und zählst deine Schritte bis "
                    "hundert. Dann fängst du wieder bei eins an. Nachts kommt "
                    "sein Gesicht wieder, und du schläfst trotzdem.",
                    aenderungen={"belastung": 0, "rueckhalt": -1}
                ),
            ],
            ort="Nordfrankreich", kern=True, gewicht=12,
            quelle={
                "kurz": "Erkennungsmarke und Verlustmeldung im Feldheer",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Verlustlisten und die Vorschrift "
                              "über die Erkennungsmarke, die den Weg einer "
                              "Todesnachricht vom Graben bis zur Familie "
                              "belegen. Die Listen nennen Namen und Daten, "
                              "aber nicht, wer den Toten gefunden hat.",
            }
        ),

        Ereignis(
            "front_1914_schanzen", [1914], "front",
            ## PAKET 7, SCHRITT 3, TEIL A.2: die Fassung für den, der den
            ## Mantel im Straßengraben gelassen hat. Ein Satz, kein Vorwurf,
            ## und kein Wort darüber, dass es ein Fehler war - sieben Riemen
            ## sind bis zum Abend tragbar, zehn nicht.
            ##
            ## Die Karte hat kein Jahreswörterbuch, also steht die
            ## Merkmalsfassung hier ganz außen. Wo eine Karte beides trägt,
            ## gehört sie unter das Grundjahr (AUFGEFALLEN 53).
            {
                "ohne_mantel":
                    "Der Spaten geht bis zum Stiel ins Wasser, und der Boden "
                    "gibt nach. Seit einer Woche steht der Vormarsch, und der "
                    "Befehl heißt eingraben. Es ist November, und der Mann "
                    "neben dir schlägt den Mantelkragen hoch. Du hast keinen. "
                    "„Bis Weihnachten sind wir hier weg“, sagt einer, und "
                    "keiner antwortet.",
                "standard":
                    "Der Spaten geht bis zum Stiel ins Wasser, und der Boden "
                    "gibt nach. Seit einer Woche steht der Vormarsch, und der "
                    "Befehl heißt eingraben. Es ist November, und in den "
                    "Stiefeln steht das Wasser über den Knöcheln. „Bis "
                    "Weihnachten sind wir hier weg“, sagt einer, und keiner "
                    "antwortet.",
            },
            [
                Option(
                    "Tief graben",
                    "Zwei Stunden länger in Nässe und Kälte.",
                    "Dein Loch hält, als am Morgen der erste Beschuss kommt. "
                    "Deine Hände brauchen eine Woche, bis sie wieder richtig "
                    "greifen. Der Zeigefinger bleibt steif bis in den Dezember.",
                    aenderungen={"belastung": 2, "rueckhalt": 1}
                ),
                Option(
                    "Nur das Nötigste",
                    "Flach ausheben und den Rest dem Zufall überlassen.",
                    "Du bist als Erster fertig und schläfst zwei Stunden im "
                    "Trockenen. Als der Beschuss kommt, drückst du dich in "
                    "eine Mulde. Danach zitterst du, bis es hell wird.",
                    aenderungen={"belastung": 0, "versorgung": 1}
                ),
            ],
            ort="Flandern", gewicht=10,
            quelle={
                "kurz": "Übergang zum Stellungskrieg, Herbst 1914",
                "voll": QUELLE_FEHLT,
                "art": "darstellung",
                "einordnung": "Gesucht wird eine Darstellung des Eingrabens im "
                              "November 1914, als die Front von der Nordsee bis "
                              "zur Schweiz erstarrte. Sie erklärt den Befehl, "
                              "sagt aber nichts über den Boden, der in Flandern "
                              "unter Wasser stand.",
            }
        ),

        Ereignis(
            "front_1914_weihnachten", [1914], "front",
            "Es friert, und der Boden ist zum ersten Mal seit Wochen hart. "
            "Aus dem gegnerischen Graben kommt Gesang, dreihundert Schritt "
            "entfernt. Dann steigt dort einer unbewaffnet auf die Brustwehr "
            "und hebt die Hände. Der Divisionsbefehl von gestern verbietet "
            "jede Annäherung ausdrücklich.",
            [
                Option(
                    "Über die Brustwehr steigen",
                    "Zigaretten, ein paar Wörter, ein Handschlag.",
                    "Eine Stunde lang ist zwischen den Gräben kein Krieg. Am "
                    "Abend liest der Leutnant den Divisionsbefehl noch einmal "
                    "laut vor. Dabei sieht er dich an.",
                    hinweis="ausdrücklich verboten",
                    aenderungen={"belastung": -2, "aufmerksamkeit": 2, "rueckhalt": 1},
                    merkmale=["verbruederung"]
                ),
                Option(
                    "Im Graben bleiben",
                    "Du siehst zu und rührst dich nicht.",
                    "Du siehst von unten zu, wie sie sich die Hände geben. "
                    "Deine Finger werden am Gewehr kalt und bleiben es. Am "
                    "Neujahrstag wird auf dieselben Leute wieder geschossen.",
                    aenderungen={"belastung": 1}
                ),
            ],
            ort="Flandern", gewicht=8,
            quelle={
                "kurz": "Weihnachtsfrieden 1914 und die Verbote danach",
                "voll": "Weihnachtsfrieden an der Westfront, 24. bis 26. Dezember "
                        "1914; Deutsches Historisches Museum, LeMO",
                "art": "darstellung",
                "einordnung": "Belegt sind Verbrüderungen an mehreren Abschnitten "
                              "der Westfront und die Divisionsbefehle, die jede "
                              "Annäherung untersagten. Wie viele Männer beteiligt "
                              "waren, lässt sich nicht sagen: Wer mitmachte, "
                              "meldete es nicht.",
            }
        ),

        Ereignis(
            "front_trommelfeuer", [1914, 1915, 1916], "front",
            {
                1914: "Seit dem Morgengrauen liegt Feuer auf dem Abschnitt, "
                      "und die Erde federt unter dir. Kalk rieselt aus der "
                      "Grabenwand in deinen Nacken. So etwas hat keiner von "
                      "euch vorher gehört. Der Mann neben dir hält sich die "
                      "Ohren zu und sieht dich an.",
                1915: "Es fängt um vier an, und du weißt schon, dass es bis "
                      "acht dauert. Ihr habt gelernt, wohin die Einschläge "
                      "wandern und wann die Pause kommt. In der Pause isst "
                      "du, weil du sonst nicht dazu kommst. Der Kalk in der "
                      "Luft legt sich auf die Zunge.",
                1916: "Das Feuer liegt seit zwei Tagen auf dem Abschnitt und "
                      "hört nicht auf. Der Unterstand hält, solange er hält. "
                      "Von der Nachbarkompanie ist seit gestern Abend kein "
                      "Zeichen gekommen. Deine Hände zittern auch dann, wenn "
                      "es kurz still ist.",
            },
            [
                Option(
                    "Den Kopf unten halten",
                    "Du drückst dich in die Erde und zählst die Einschläge.",
                    {
                        1914: "Nach vier Stunden hört es auf. Du zählst "
                              "weiter, obwohl nichts mehr kommt. Erst am "
                              "Abend siehst du, dass deine Finger blutig sind.",
                        1916: "Nach zwei Tagen hört es auf. Als du aufstehst, "
                              "hörst du eine Stunde lang nichts. Der Mann "
                              "neben dir spricht mit dir, und du siehst nur "
                              "seinen Mund.",
                    },
                    aenderungen={"belastung": 2},
                    stimmung="angst"
                ),
                Option(
                    "Einen Brief schreiben",
                    "Du schreibst nach Hause, dass es dir gut geht.",
                    "Du lügst über drei Seiten, und beim Schreiben glaubst du "
                    "es selbst ein wenig. Die Feldpost nimmt den Brief noch am "
                    "selben Tag mit. Deine Schrift auf dem Umschlag ist nicht "
                    "deine.",
                    aenderungen={"belastung": -1, "rueckhalt": 1}
                ),
            ],
            ort="Grabenstellung", kern=True, gewicht=12, wiederholbar=True,
            quelle={
                "kurz": "Trommelfeuer als neue Erfahrung des Materialkriegs",
                "voll": QUELLE_FEHLT,
                "art": "erinnerung",
                "einordnung": "Gesucht werden Feldpostbriefe oder Tagebücher, in "
                              "denen Dauerbeschuss beschrieben wird, samt Angaben "
                              "zur Dauer. Sie zeigen, wie es sich anfühlte, aber "
                              "nicht, wie viele Granaten wirklich fielen.",
            }
        ),

        Ereignis(
            "front_feldpost", [1914, 1915, 1916], ["front", "etappe"],
            {
                1914: "Der Postunteroffizier ruft die Namen, und deiner ist "
                      "dabei. Das Paket riecht nach Seife und nach Wolle. "
                      "Drinnen liegen Strümpfe, ein Stück Kuchen und ein "
                      "Zettel. Auf dem Zettel steht die Frage, wann du "
                      "wiederkommst.",
                1915: "Diesmal ist es kein Paket, sondern ein dünner Brief. "
                      "Das Brot werde knapp, schreibt sie, und die Kinder "
                      "fragen nach dir. Am Rand steht eine Zahl: was ein "
                      "Pfund Butter jetzt kostet. Du liest sie dreimal.",
                1916: "Kein Paket mehr, nur ein Bogen, beidseitig "
                      "beschrieben. Es gehe allen gut, steht dreimal darin. "
                      "Zwischen den Zeilen steht, dass sie hungern. Das "
                      "Papier ist rau und war vorher etwas anderes.",
            },
            [
                Option(
                    "Ehrlich antworten",
                    "Du schreibst, wie es hier wirklich ist.",
                    "Der Brief geht durch die Zensur, also die Prüfstelle der "
                    "Post, und kommt geschwärzt an. Was übrig bleibt, macht "
                    "die Sorge zu Hause größer statt kleiner. Vier Wochen "
                    "später fragt der Kompanieführer, was darin stand.",
                    aenderungen={"belastung": -1, "aufmerksamkeit": 1, "rueckhalt": 1}
                ),
                Option(
                    "Sie beruhigen",
                    "Alles halb so schlimm, gutes Quartier, warmes Essen.",
                    "Es liest sich glaubhaft. Du legst den Bogen weg und hast "
                    "das Gefühl, gerade jemanden verloren zu haben. Deine "
                    "Hand ist kalt, obwohl der Unterstand geheizt ist.",
                    aenderungen={"belastung": 1, "rueckhalt": -1}
                ),
            ],
            ort="Grabenstellung", kern=True, gewicht=12, wiederholbar=True,
            quelle={
                "kurz": "Feldpost: rund 28,7 Milliarden Sendungen 1914-1918",
                "voll": "Deutsche Feldpost im Ersten Weltkrieg; Deutsches "
                        "Historisches Museum, LeMO, Kriegsalltag",
                "art": "statistik",
                "einordnung": "Die Zahl zeigt, wie dicht der Postverkehr zwischen "
                              "Front und Heimat war und dass die Zensur nur "
                              "stichprobenweise arbeiten konnte. Was in den "
                              "Briefen stand und was weggelassen wurde, sagt sie "
                              "nicht.",
            }
        ),

        Ereignis(
            "front_kamerad", [1915, 1916], "front",
            "Er hockt neben dir im Unterstand, und seine Hände sind ruhig. "
            "Unter der Zeltbahn liegt ein Zivilanzug, den er irgendwoher hat. "
            "„Beim Appell sagst du, ich bin beim Regimentsstab“, sagt er. "
            "Draußen tropft es von der Decke, und keiner von euch sieht hoch.",
            [
                Option(
                    "Ihn decken",
                    "Du meldest ihn als abkommandiert und schweigst.",
                    "Am Morgen ist er weg, und beim Appell sagst du den Satz. "
                    "Zwei Wochen später fragt ein Feldwebel nach "
                    "Einzelheiten, die du nicht wissen kannst. Du merkst dir, "
                    "was du geantwortet hast, und sagst es dir nachts vor.",
                    aenderungen={"aufmerksamkeit": 2, "rueckhalt": 1},
                    merkmale=["kamerad_gedeckt"],
                    kette="front_nachfrage", kette_ab=1
                ),
                Option(
                    "Ihn melden",
                    "Du gehst zum Leutnant, bevor er weg ist.",
                    "Sie greifen ihn hinter der Etappe, keine zwölf Stunden "
                    "später. Das Kriegsgericht verurteilt ihn zu Gefängnis; "
                    "erschossen wird er nicht. Beim Essen ist neben dir Platz, "
                    "und er bleibt frei.",
                    aenderungen={"aufmerksamkeit": -2, "belastung": 2, "rueckhalt": -2},
                    merkmale=["kamerad_gemeldet"]
                ),
            ],
            ort="Grabenstellung", kern=True, gewicht=10,
            quelle={
                "kurz": "Unerlaubte Entfernung vor dem Kriegsgericht",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Kriegsgerichtsakten zu unerlaubter "
                              "Entfernung und Fahnenflucht, aus denen Anklage und "
                              "Strafmaß hervorgehen. Die Akten zeigen die Urteile, "
                              "nicht die Gruppe, die den Mann vorher gedeckt oder "
                              "gemeldet hat.",
            }
        ),

        Ereignis(
            "front_nachfrage", [1915, 1916], ["front", "etappe"],
            "Er sitzt auf einer Munitionskiste und hat die Mappe auf den "
            "Knien. Es ist ein Offizier des Gerichtsherrn, also des "
            "Vorgesetzten mit richterlicher Gewalt. Neben ihm brennt eine "
            "Kerze, und durch den Eingang zieht es kalt herein. Er fragt "
            "nach der Nacht, in der dein Kamerad verschwunden ist.",
            [
                Option(
                    "Bei der Aussage bleiben",
                    "Du wiederholst, was du damals gemeldet hast.",
                    "Er schreibt mit und schließt die Mappe ohne ein Wort. "
                    "Der Vermerk bleibt in der Akte, ein Verfahren wird nicht "
                    "eröffnet. Deine Stimme klingt beim Reden fremd.",
                    aenderungen={"aufmerksamkeit": 1, "belastung": 1}
                ),
                Option(
                    "Einräumen, was er weiß",
                    "Du gibst zu, dass du ihn nicht gesehen hast.",
                    "Vierzehn Tage mittlerer Arrest wegen Nachlässigkeit im "
                    "Dienst. Es ist weniger, als du befürchtet hast. Und mehr, "
                    "als du verkraftest.",
                    aenderungen={"belastung": 2, "versorgung": -2, "aufmerksamkeit": -1}
                ),
            ],
            ort="Etappe", nur_kette=True,
            quelle={
                "kurz": "Der Gerichtsherr und das militärische Ermittlungsverfahren",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine Ermittlungsakte mit dem Weg "
                              "von der Vernehmung bis zum Vermerk. Sie nennt "
                              "die Strafen, nicht das, was die Befragten "
                              "einander danach noch sagen konnten.",
            }
        ),

        Ereignis(
            "front_gas", [1915, 1916], "front",
            "Die Ratsche schlägt Gasalarm, und du greifst nach dem Beutel am "
            "Hals. Über dem Niemandsland treibt eine gelbliche Bank auf euren "
            "Abschnitt zu. Chlorgas ist schwerer als Luft und sinkt in jede "
            "Senke, also auch in euren Graben. Es riecht wie Bleiche, und "
            "dann riecht es nach nichts mehr.",
            [
                Option(
                    "Den Atemschutz aufsetzen",
                    "Der Einsatz sitzt, solange du ihn festhältst.",
                    "Die Maske hält. Du atmest flach durch den Filter und "
                    "zählst, bis der Nebel abgezogen ist. Zwei aus der Gruppe "
                    "haben zu spät gegriffen und husten bis zum Abend.",
                    aenderungen={"belastung": 2},
                    stimmung="angst"
                ),
                Option(
                    "Auf die Böschung steigen",
                    "Oben ist die Luft besser. Oben sieht man dich auch.",
                    "Du bekommst Luft. Dafür liegst du eine halbe Stunde "
                    "ungedeckt, während die Maschinengewehre den Grabenrand "
                    "absuchen. Der Boden vor deinem Gesicht spritzt zweimal auf.",
                    hinweis="ungedeckt",
                    aenderungen={"belastung": 0},
                    varianten=[
                        {"gewicht": 5, "ausgang": "Du bekommst Luft. Dafür liegst du eine halbe Stunde ungedeckt, während die Maschinengewehre den Grabenrand absuchen. Der Boden vor deinem Gesicht spritzt zweimal auf.", "aenderungen": {}},
                        {"gewicht": 1, "sprung": "ende_gefallen"},
                    ]
                ),
            ],
            ort="Grabenstellung", kern=True, gewicht=12,
            quelle={
                "kurz": "Erster Chlorgaseinsatz bei Ypern, 22. April 1915",
                "voll": "Gasangriff bei Ypern am 22. April 1915; Deutsches "
                        "Historisches Museum, LeMO, Der Erste Weltkrieg",
                "art": "darstellung",
                "einordnung": "Belegt sind Datum, Ort und die Eigenschaft des "
                              "Chlorgases, schwerer als Luft zu sein und in "
                              "Senken zu sinken. Wie zuverlässig der einzelne "
                              "Atemschutz saß, ist daraus nicht abzulesen.",
            }
        ),

        Ereignis(
            "front_laeuse", [1915, 1916], "front",
            "Es juckt seit drei Nächten, und am Bauch hast du dich blutig "
            "gekratzt. In den Nähten des Hemdes sitzen sie in Reihen. Im "
            "Feldlazarett heißt es, das Wolhynische Fieber komme davon; es "
            "wirft einen für Wochen um. „Kratz nicht“, sagt einer, „dann "
            "wird es eitrig.“",
            [
                Option(
                    "Sich krank melden",
                    "Zwei Tage Ruhe, wenn der Arzt mitspielt.",
                    "Der Stabsarzt schreibt dienstfähig und notiert etwas an "
                    "den Rand. Zwei Tage später stehst du wieder im Graben, "
                    "jetzt mit Fieber. Beim Anziehen zittern die Knie.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": 1}
                ),
                Option(
                    "Die Nähte absengen",
                    "Kerze und Kleidung, Stück für Stück, die halbe Nacht.",
                    "Es riecht die halbe Nacht nach verbranntem Stoff. Für "
                    "drei Tage ist Ruhe, dann fängt es wieder an. Du weißt "
                    "jetzt, dass es nicht aufhört.",
                    aenderungen={"belastung": 0, "versorgung": -1, "rueckhalt": 1}
                ),
            ],
            ort="Grabenstellung", gewicht=10, wiederholbar=True,
            quelle={
                "kurz": "Wolhynisches Fieber, übertragen durch Kleiderläuse",
                "voll": QUELLE_FEHLT,
                "art": "darstellung",
                "einordnung": "Gesucht wird ein sanitätsdienstlicher Bericht über "
                              "Läusebefall und Wolhynisches Fieber im Grabenkrieg. "
                              "Er nennt Erreger und Übertragungsweg, aber nicht, "
                              "wie oft ein Stabsarzt trotzdem dienstfähig "
                              "schrieb.",
            }
        ),

        Ereignis(
            "front_beute", [1915, 1916], "front",
            "Im Trichter steht Wasser, und darin liegt ein Gefallener der "
            "Gegenseite. Am Handgelenk trägt er eine Uhr, die noch geht. Im "
            "Brotbeutel sind zwei Konserven, in der Innentasche stecken "
            "Fotografien. Es ist niemand in der Nähe.",
            [
                Option(
                    "Nehmen, was brauchbar ist",
                    "Konserven und Uhr, die Bilder bleiben liegen.",
                    "Du isst zum ersten Mal seit Tagen satt und schläfst "
                    "danach sofort ein. Die Uhr tauschst du in der Etappe "
                    "gegen Tabak. Das Ticken hörst du noch, als sie längst "
                    "weg ist.",
                    aenderungen={"versorgung": 3, "belastung": 1, "rueckhalt": -1}
                ),
                Option(
                    "Ihn zuschütten",
                    "Spaten, zehn Minuten, kein Wort.",
                    "Du machst es allein, und der Spaten schneidet dir in "
                    "die Handfläche. Erzählt hast du es niemandem. Warum du "
                    "es getan hast, könntest du nicht erklären.",
                    aenderungen={"belastung": -1, "versorgung": -1, "rueckhalt": 1},
                    stimmung="einsam"
                ),
            ],
            ort="Niemandsland", gewicht=9,
            quelle={
                "kurz": "Verbot der Leichenfledderei im Feldheer",
                "voll": QUELLE_FEHLT,
                "art": "gesetz",
                "einordnung": "Gesucht wird die Bestimmung des Militärstrafrechts "
                              "über die Wegnahme von Sachen Gefallener und ihre "
                              "Anwendung im Feld. Sie sagt, was verboten war, und "
                              "nichts darüber, wie oft es im Trichter geschah.",
            }
        ),

        Ereignis(
            "front_stosstrupp", [1915, 1916], "front",
            "Der Leutnant steht im Graben und sucht Freiwillige für die "
            "Nacht. Ein Unternehmen im Niemandsland, hin und zurück, "
            "Drahtschere und Handgranaten. „Wer mitgeht, hat vierzehn Tage "
            "Urlaub“, sagt er und sieht die Reihe entlang. Neben dir atmet "
            "einer hörbar durch die Nase.",
            [
                Option(
                    "Sich melden",
                    "Vierzehn Tage sind vierzehn Tage.",
                    "Du kommst zurück. Zwei andere nicht. Das Bett zu Hause ist weich, und du liegst wach darin.",
                    hinweis="gefährlich",
                    aenderungen={"belastung": -3, "rueckhalt": 1},
                    varianten=[
                        {"gewicht": 4, "ausgang": "Du kommst zurück. Zwei andere nicht. Das Bett zu Hause ist weich, und du liegst wach darin.", "aenderungen": {}},
                        {"gewicht": 2, "ausgang": "Der Draht war nicht durchgeschnitten. Du liegst achtzehn Stunden in einem Trichter, bis es dunkel wird. Den Urlaub bekommst du.", "aenderungen": {"belastung": 5}},
                        {"gewicht": 1, "sprung": "ende_gefallen"},
                    ]
                ),
                Option(
                    "Im Graben bleiben",
                    "Du meldest dich nicht und siehst zu Boden.",
                    "Das Unternehmen findet ohne dich statt, mit vier "
                    "anderen. Der Urlaub wird danach für den ganzen "
                    "Abschnitt gestrichen. Beim Essen fragt dich niemand, "
                    "warum du nichts gesagt hast.",
                    aenderungen={"belastung": 1, "rueckhalt": -1}
                ),
            ],
            ort="Grabenstellung", gewicht=8,
            quelle={
                "kurz": "Stoßtruppunternehmen und Urlaub als Anreiz",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird ein Divisionsbefehl über Patrouillen "
                              "im Niemandsland, aus dem hervorgeht, was "
                              "Freiwilligen versprochen wurde. Er nennt die "
                              "Zusage, aber nicht, wie viele der Freiwilligen "
                              "zurückkamen.",
            }
        ),

        Ereignis(
            "front_urlaub", [1915, 1916], ["front", "etappe"],
            "In der guten Stube ist geheizt, und du sitzt am Tisch mit "
            "sauberen Händen. Auf der Anrichte liegt die Zeitung, aus der sie "
            "dir vorlesen, was an der Front geschieht. Niemand fragt, wie es "
            "dort wirklich ist. Alle sind stolz auf dich, und der Teller ist "
            "voller als deiner seit Monaten.",
            [
                Option(
                    "Erzählen, wie es ist",
                    "Du versuchst es beim Abendessen.",
                    "Nach drei Sätzen wechselt jemand das Gespräch. Deine "
                    "Mutter räumt ab, dein Vater sagt, im Krieg sei nun "
                    "einmal Krieg. Du isst weiter und schmeckst nichts mehr.",
                    aenderungen={"belastung": 1, "rueckhalt": -1},
                    stimmung="einsam"
                ),
                Option(
                    "Ihnen recht geben",
                    "Du erzählst, was sie hören wollen.",
                    "Vierzehn Tage lang bist du der Held der Straße. In der "
                    "Nacht vor der Abfahrt sitzt du in der Küche und wartest, "
                    "dass es hell wird. Der Koffer steht schon seit acht Uhr "
                    "im Flur.",
                    aenderungen={"belastung": -1, "rueckhalt": 1}
                ),
            ],
            ort="Heimatstadt", gewicht=9,
            quelle={
                "kurz": "Heimaturlaub und das Schweigen darüber",
                "voll": QUELLE_FEHLT,
                "art": "erinnerung",
                "einordnung": "Gesucht werden Feldpostbriefe oder Nachkriegs"
                              "erinnerungen über das Auseinandergehen von "
                              "Fronterfahrung und Heimatbild während des Urlaubs. "
                              "Erinnerungen wurden später geschrieben und wissen "
                              "schon, wie der Krieg ausging.",
            }
        ),

        Ereignis(
            "front_1916_verdun", [1916], "front",
            "Du kauerst auf dem Grabenbrett, und die Hand am Gewehr ist "
            "nass. Der Befehl zum Vorgehen ist vor zwei Minuten "
            "durchgegeben worden. Vor euch liegen dreihundert Meter "
            "aufgewühlter Boden im Nebel. Von der ersten Welle ist kein "
            "Zeichen zurückgekommen.",
            [
                Option(
                    "Sitzen bleiben",
                    "Du rührst dich nicht, als die anderen aufstehen.",
                    "Der Leutnant brüllt dich an und geht weiter. Im "
                    "Durcheinander verliert sich, wer wo gelegen hat. Der "
                    "Vermerk in der Akte bleibt, und du weißt, dass er "
                    "bleibt.",
                    aenderungen={"aufmerksamkeit": 3, "belastung": 0, "rueckhalt": -1}
                ),
                Option(
                    "Mit vorgehen",
                    "Du kletterst über die Brustwehr und läufst.",
                    "Ihr erreicht einen Trichter, der schon vorher da war. Von der Gruppe kommen vier zurück.",
                    aenderungen={"belastung": 2, "versorgung": -1},
                    varianten=[
                        {"gewicht": 5, "ausgang": "Ihr erreicht einen Trichter, der schon vorher da war. Von der Gruppe kommen vier zurück.", "aenderungen": {}},
                        {"gewicht": 1, "sprung": "ende_gefallen"},
                    ]
                ),
            ],
            ort="Verdun", kern=True, gewicht=16,
            quelle={
                "kurz": "Schlacht um Verdun, 21. Februar bis Dezember 1916",
                "voll": "Schlacht um Verdun 1916; Deutsches Historisches Museum, "
                        "LeMO, Der Erste Weltkrieg",
                "art": "darstellung",
                "einordnung": "Belegt sind Beginn, Dauer und die Größenordnung der "
                              "Verluste, die am Jahresende ungefähr zur "
                              "Ausgangslage zurückführten. Was in der einzelnen "
                              "Gruppe geschah, die über die Brustwehr stieg, "
                              "steht in keiner dieser Darstellungen.",
            }
        ),

        Ereignis(
            "front_1916_hunger", [1916], "front",
            "Seit vier Tagen bringt die Feldküche dieselbe dünne Suppe. Du "
            "hast den Gürtel um zwei Löcher enger geschnallt. Achtzig Meter "
            "vor der Stellung liegt ein verendetes Pferd im Niemandsland. "
            "Bei Westwind riecht man es bis in den Graben.",
            [
                Option(
                    "Nachts hinauskriechen",
                    "Mit dem Seitengewehr, im Dunkeln, allein.",
                    "Du bringst zurück, was du tragen kannst, und brätst es "
                    "auf dem Spaten. Du teilst mit niemandem, und das merken "
                    "alle. Am Morgen ist dir schlecht, und satt bist du "
                    "trotzdem.",
                    aenderungen={"versorgung": 3, "belastung": 1, "aufmerksamkeit": 1, "rueckhalt": -1}
                ),
                Option(
                    "In der Stellung bleiben",
                    "Der Hunger ist schlimm, ein Scharfschütze ist schlimmer.",
                    "Du bleibst liegen und trinkst heißes Wasser. Der Magen "
                    "krampft die halbe Nacht. Am zweiten Tag hörst du auf, an "
                    "das Pferd zu denken.",
                    aenderungen={"versorgung": -2, "belastung": 0}
                ),
            ],
            ort="Grabenstellung", gewicht=10,
            quelle={
                "kurz": "Verpflegungslage der Feldtruppe 1916",
                "voll": QUELLE_FEHLT,
                "art": "statistik",
                "einordnung": "Gesucht werden Verpflegungsnachweisungen, die "
                              "belegen, wie die Rationen im Feld 1916 zurückgingen. "
                              "Sie nennen die zugeteilte Menge, nicht die, die "
                              "vorn im Graben ankam.",
            }
        ),

        Ereignis(
            "front_1916_gefangener", [1916], "front",
            "Beim Räumen des Grabens steht plötzlich einer vor dir und hebt "
            "die Hände. Er ist unbewaffnet, höchstens achtzehn, und seine "
            "Lippen sind aufgesprungen. Zurückbringen kostet zwei Leute und "
            "eine Stunde durch das Feuer. Hinter dir ruft jemand, dass es "
            "weitergeht.",
            [
                Option(
                    "Ihn zurückbringen",
                    "Zwei Mann Begleitung, quer durch das Feuer.",
                    "Ihr kommt durch, und keiner von euch wird getroffen. In "
                    "der Etappe bekommt er Wasser und setzt sich auf den "
                    "Boden. Du hörst nie wieder von ihm.",
                    aenderungen={"belastung": 1, "rueckhalt": 1}
                ),
                Option(
                    "Ihn stehen lassen",
                    "Niemand hat Zeit, und niemand sieht hin.",
                    "Du gehst weiter und drehst dich nicht um. Was danach "
                    "geschieht, hast du nicht gesehen. Genau das erzählst du "
                    "dir noch Jahre später.",
                    aenderungen={"belastung": 0, "rueckhalt": -1},
                    stimmung="erschoepft"
                ),
            ],
            ort="Somme", kern=True, gewicht=11,
            quelle={
                "kurz": "Haager Landkriegsordnung: Schutz der Kriegsgefangenen",
                "voll": "Haager Abkommen betreffend die Gesetze und Gebräuche des "
                        "Landkriegs vom 18. Oktober 1907, Abschnitt über "
                        "Kriegsgefangene",
                "art": "gesetz",
                "einordnung": "Das Abkommen verpflichtet zur menschlichen "
                              "Behandlung dessen, der sich ergibt, und beide "
                              "Seiten hatten es unterschrieben. Was beim Räumen "
                              "eines Grabens tatsächlich geschah, ist damit "
                              "nicht belegt.",
            }
        ),

        Ereignis(
            "front_1916_zaehlung", [1916], ["front", "etappe"],
            "Auf dem Tisch liegt ein Erlass des Kriegsministeriums vom "
            "Oktober. Die jüdischen Angehörigen der Einheit sollen erfasst "
            "werden, und daneben soll stehen, wo jeder Dienst tut. Du sollst "
            "die Liste zusammenstellen, weil du eine saubere Handschrift "
            "hast. Der Bleistift liegt schon quer über dem Formular.",
            [
                Option(
                    "Die Liste ausfüllen",
                    "Ein Formular wie viele andere.",
                    "Du trägst elf Namen ein und gibst die Aufstellung ab. "
                    "Zwei Kameraden sehen dir dabei zu und sagen nichts. Das "
                    "Ergebnis der Zählung wird nie veröffentlicht.",
                    aenderungen={"aufmerksamkeit": -1, "rueckhalt": -2},
                    merkmale=["zaehlung_ausgefuellt"]
                ),
                Option(
                    "Die Bearbeitung verschleppen",
                    "Rückfragen, fehlende Angaben, verlegte Formulare.",
                    "Zweimal wird gemahnt, dann übernimmt es ein anderer. "
                    "Dein Name steht jetzt in einem Vermerk über mangelnde "
                    "Diensteifrigkeit. Die Liste wird trotzdem fertig.",
                    aenderungen={"aufmerksamkeit": 2, "rueckhalt": 1}
                ),
            ],
            ort="Etappe", gewicht=9,
            quelle={
                "kurz": "Judenzählung im Heer, Oktober 1916",
                "voll": "Erlass des Preußischen Kriegsministeriums vom 11. Oktober "
                        "1916 über die Erhebung der jüdischen Heeresangehörigen; "
                        "Deutsches Historisches Museum, LeMO",
                "art": "akte",
                "einordnung": "Belegt sind der Erlass und die Tatsache, dass das "
                              "Ergebnis nie veröffentlicht wurde. Gerade das "
                              "Schweigen wurde nach dem Krieg von "
                              "antisemitischen Verbänden als Beweis ausgegeben.",
            }
        ),

        Ereignis(
            "heimat_brotschlange", [1914, 1915, 1916], "heimat",
            {
                1914: "Seit vier Uhr stehst du an, und die Füße sind kalt "
                      "geworden. Aus dem Laden riecht es nach Brot, seit "
                      "einer halben Stunde. Der Bäcker bedient zuerst die "
                      "Kundschaft, die er kennt. Aus dem Hinterhof bietet "
                      "einer Brot an, zum dreifachen Preis.",
                1915: "Die Schlange beginnt jetzt um drei, und du hast eine "
                      "Decke dabei. Wer keine Karte hat, bekommt nichts; wer "
                      "eine hat, oft auch nicht. „Zwei Pfund, mehr geht "
                      "nicht“, ruft die Frau vorn in die Reihe. Im Hinterhof "
                      "wird weiter gehandelt.",
                1916: "Die Schlange steht seit Mitternacht, und es hat "
                      "geregnet. Vorn hat es Streit gegeben, ein Fenster ist "
                      "zu Bruch gegangen. Zwei Schutzleute stehen jetzt an "
                      "der Tür. Im Hinterhof kostet ein Brot mehr als ein "
                      "Tagelohn.",
            },
            [
                Option(
                    "Im Hinterhof kaufen",
                    "Er verlangt bar und stellt keine Fragen.",
                    {
                        1914: "Ein Schutzmann sieht in die andere Richtung, als du bezahlst. Du hast Brot und ein schlechtes Gefühl bis nach Hause.",
                        1916: "Diesmal notiert der Schutzmann etwas. Der Kettenhandel gilt inzwischen als Verbrechen am eigenen Volk, so steht es in der Zeitung.",
                    },
                    hinweis="kostet mehr, als du hast",
                    aenderungen={"versorgung": 2, "aufmerksamkeit": 1}
                ),
                Option(
                    "In der Schlange bleiben",
                    "Drei Stunden, vielleicht reicht es.",
                    "Du stehst, bis dir der Rücken wehtut und die Sonne "
                    "über den Dächern steht. Als du an der Reihe bist, "
                    "schließt der Laden; ausverkauft. Die Frau hinter dir "
                    "fängt an zu schreien.",
                    aenderungen={"belastung": 2, "versorgung": -1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=14, wiederholbar=True,
            quelle={
                "kurz": "Höchstpreise und Kettenhandel als Straftatbestand",
                "voll": QUELLE_FEHLT,
                "art": "gesetz",
                "einordnung": "Gesucht wird eine Höchstpreisverordnung des "
                              "Bundesrats samt den Strafbestimmungen gegen "
                              "Kettenhandel. Sie legt Preise fest und erklärt "
                              "nicht, warum die Ware trotzdem im Hinterhof zu "
                              "haben war.",
            }
        ),

        Ereignis(
            ## Seit Paket 6, Schritt 2 eine Fassung je Familienmerkmal.
            ## Wer fehlt, entscheidet, was das Ausbleiben der Post bedeutet:
            ## eine Ehe, ein Vater, ein Bruder. Der Vorgang bleibt derselbe.
            "heimat_1914_post", [1914, 1915], "heimat",
            {
                "ehemann_im_feld":
                    "Sechs Wochen ohne ein Wort von ihm. Du gehst jeden "
                    "Morgen zum Kasten und hörst schon am Klappern, dass "
                    "nichts da ist. Die Nachbarin nennt dir eine Frau in der "
                    "Gartenstraße, die gegen Bezahlung Auskunft gibt. „Bei "
                    "mir hat sie recht gehabt“, sagt sie.",
                "vater_im_feld":
                    "Sechs Wochen ohne eine Karte von ihm. Die Kleine fragt "
                    "jeden Abend, und du sagst jeden Abend dasselbe. Die "
                    "Nachbarin nennt dir eine Frau in der Gartenstraße, die "
                    "gegen Bezahlung Auskunft gibt. Es kostet zwei Mark.",
                "bruder_im_feld":
                    "Sechs Wochen ohne Nachricht von ihm. Die Mutter fragt "
                    "dich, nicht den Briefträger, und du hast keine Antwort. "
                    "Die Nachbarin nennt dir eine Frau in der Gartenstraße, "
                    "die gegen Bezahlung Auskunft gibt. Du weißt genau, was "
                    "davon zu halten ist.",
                "standard":
                    "Seit sechs Wochen kommt keine Feldpost. Der Kasten ist "
                    "kalt und leer, und das Klappern kennst du auswendig. Die "
                    "Nachbarin nennt dir eine Frau in der Gartenstraße, die "
                    "gegen Bezahlung Auskunft gibt.",
            },
            [
                Option(
                    "Zu der Frau gehen",
                    "Sie verspricht gute Nachrichten und nimmt das Geld vorher.",
                    "Sie sagt, was du hören willst. Es ist Unsinn, und du schläfst trotzdem eine Nacht durch.",
                    aenderungen={"versorgung": -1, "belastung": -1, "rueckhalt": -1}
                ),
                Option(
                    "Im Lazarett aushelfen",
                    "Statt zu warten, arbeitest du im Reservelazarett.",
                    "Du wäschst Verbände aus, die niemand mehr sauber bekommt. Es ist schrecklich, und es ist etwas zu tun.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": 1}
                ),
            ],
            ## Seit Paket 2, Schritt 2: braucht_eines statt braucht. Die
            ## frühere Pauschale ist in drei Merkmale zerlegt, und jedes
            ## einzelne von ihnen begründet das Warten auf Post.
            ort="Wohnviertel", gewicht=8,
            braucht_eines=["ehemann_im_feld", "vater_im_feld", "bruder_im_feld"],
            quelle={
                "kurz": "Vermisstensuche und Wahrsagerei im Krieg",
                "voll": QUELLE_FEHLT,
                "art": "zeitung",
                "einordnung": "Gesucht werden Zeitungsanzeigen und "
                              "Polizeiberichte über Kartenlegerinnen, die "
                              "Angehörigen von Vermissten gegen Geld Auskunft "
                              "versprachen. Sie belegen das Angebot, nicht die "
                              "Verzweiflung, aus der es bezahlt wurde.",
            }
        ),

        Ereignis(
            "heimat_1914_liebesgaben", [1914], "heimat",
            "Im Gemeindesaal stehen drei Waschkörbe, und es riecht nach "
            "Mottenkugeln. Der Vaterländische Frauenverein sammelt "
            "Wollsachen für die Truppe. Vor dir legt eine Frau einen ganzen "
            "Stapel hinein. „Am Sonntag wird verlesen, wer gegeben hat“, "
            "sagt die Vorsitzende und sieht dich an.",
            [
                Option(
                    "Die guten Sachen abgeben",
                    "Zwei Decken und die guten Wintersachen aus dem Schrank.",
                    "Dein Name wird am Sonntag von der Kanzel verlesen. Im "
                    "Januar sitzt ihr in kalten Zimmern und geht früh ins "
                    "Bett. Du hörst weiter, wie stolz alle auf dich sind.",
                    aenderungen={"versorgung": -1, "rueckhalt": 2}
                ),
                Option(
                    "Etwas Altes hergeben",
                    "Ein durchgescheuerter Schal, mehr sei nicht da.",
                    "Die Vorsitzende nimmt ihn entgegen und legt ihn "
                    "sichtbar auf den Rand des Korbes. Am Sonntag fällt dein "
                    "Name nicht. Im Januar sind eure Betten warm.",
                    aenderungen={"rueckhalt": -2, "aufmerksamkeit": 1}
                ),
            ],
            ort="Gemeindesaal", gewicht=9,
            quelle={
                "kurz": "Liebesgabensammlungen des Vaterländischen Frauenvereins",
                "voll": QUELLE_FEHLT,
                "art": "zeitung",
                "einordnung": "Gesucht werden Sammelaufrufe und Dankeslisten aus "
                              "Lokalzeitungen des Winters 1914, in denen die "
                              "Spenderinnen namentlich genannt werden. Sie "
                              "zeigen den öffentlichen Druck, nicht die kalten "
                              "Zimmer, die danach blieben.",
            }
        ),

        Ereignis(
            "heimat_kriegsanleihe", [1914, 1915, 1916], "heimat",
            {
                1914: "Auf dem Tisch liegt der Zeichnungsschein für die "
                      "erste Kriegsanleihe, ein Blatt mit vielen Zahlen. In "
                      "der Schule, im Betrieb und in der Kirche wird "
                      "gefragt, wer schon gezeichnet hat. In der Blechdose "
                      "im Schrank liegt, was ihr habt.",
                1915: "Die dritte Kriegsanleihe, und der Schein ist "
                      "diesmal größer gedruckt. Wer zeichnet, hilft dem "
                      "Vaterland; wer nicht zeichnet, wird gefragt, warum "
                      "nicht. Die Dose im Schrank ist leichter geworden.",
                1916: "Die fünfte Kriegsanleihe, und im Hausflur hängt eine "
                      "Liste. Darauf steht, wer welchen Betrag gezeichnet "
                      "hat. „Die Frau im dritten Stock hat nichts“, sagt "
                      "jemand im Vorbeigehen. Die Dose im Schrank ist fast "
                      "leer.",
            },
            [
                Option(
                    "Den Schein zeichnen",
                    "Die Ersparnisse gehen in Papiere mit Zinsversprechen.",
                    "Man dankt dir öffentlich, und dein Name steht weit "
                    "oben. Die Dose im Schrank ist leer und klappert nicht "
                    "mehr. Ob du das Geld je wiedersiehst, entscheidet ein "
                    "Ausgang, den heute niemand kennt.",
                    aenderungen={"versorgung": -2, "rueckhalt": 2, "aufmerksamkeit": -1}
                ),
                Option(
                    "Nicht zeichnen",
                    "Das Geld bleibt, wo es ist.",
                    "Neben deinem Namen bleibt die Zeile leer, und die "
                    "Liste hängt vier Wochen. Man rechnet dir vor, was "
                    "andere gegeben haben. Im Treppenhaus grüßt man kürzer.",
                    aenderungen={"rueckhalt": -2, "aufmerksamkeit": 1}
                ),
            ],
            ort="Wohnviertel", gewicht=10, wiederholbar=True,
            quelle={
                "kurz": "Neun Kriegsanleihen zwischen 1914 und 1918",
                "voll": "Deutsche Kriegsanleihen 1914 bis 1918; Deutsches "
                        "Historisches Museum, LeMO, Kriegsfinanzierung",
                "art": "statistik",
                "einordnung": "Belegt sind die neun Zeichnungsfristen und die "
                              "Werbung, mit der öffentlich um Beteiligung "
                              "geworben wurde. Wie stark der Druck im Hausflur "
                              "und im Betrieb war, steht in keiner "
                              "Zeichnungsliste.",
            }
        ),

        Ereignis(
            ## Seit Paket 6, Schritt 2 eine Fassung je Familienmerkmal.
            ##
            ## VORSICHT, DIE HIER BESONDERS GILT: Kein Text darf andeuten,
            ## die Spielerin hätte etwas tun können. Der Tod kommt
            ## ausschliesslich aus dem Schicksalssystem beim Jahreswechsel
            ## und nie aus einer Entscheidung. Alle vier Fassungen zeigen
            ## deshalb den Vordruck und die Formel - was ein Amt schreibt,
            ## nicht was jemand versäumt hat.
            ##
            ## GESCHACHTELT UNTER DAS GRUNDJAHR, und das ist kein Zierrat:
            ## Paket 4 hängt über KETTENGLIED_NACHTRAG eigene Fassungen für
            ## 1917 und 1918 an diese Karte. jahresfassung_mischen() legt
            ## sie NEBEN die vorhandenen Schlüssel. Stünden die Merkmale
            ## auf derselben Ebene wie die Jahreszahlen, sähe
            ## ereignistext() Jahreszahlen und liefe in jahrestext() - für
            ## 1914 bis 1916 gäbe es dort keinen passenden Schlüssel, und
            ## die Karte zeigte in allen Fällen den Text von 1917.
            ## Genau so ist es beim ersten Versuch passiert.
            "heimat_todesnachricht", [1914, 1915, 1916], "heimat",
            {
              1914: {
                "ehemann_im_feld":
                    "Der Umschlag hat einen schwarzen Rand, und dein Name "
                    "steht mit Maschine darauf. „Gefallen für das Vaterland“ "
                    "heisst die Formel, und dass er nicht gelitten habe. "
                    "Eingetragen sind Datum und Ort, sonst nichts. Auf der "
                    "Rückseite steht, wo man den Witwenantrag stellt.",
                "vater_im_feld":
                    "Der Umschlag hat einen schwarzen Rand und liegt seit "
                    "dem Mittag auf dem Tisch. „Gefallen für das Vaterland“ "
                    "heisst die Formel, und dass er nicht gelitten habe. "
                    "Eingetragen sind Datum und Ort, sonst nichts. Die "
                    "Jüngste fragt, ob er zu Weihnachten kommt.",
                "bruder_im_feld":
                    "Der Umschlag mit dem schwarzen Rand ist an die Mutter "
                    "gerichtet, und sie kann ihn nicht öffnen. „Gefallen für "
                    "das Vaterland“ heisst die Formel, und dass er nicht "
                    "gelitten habe. Eingetragen sind Datum und Ort, sonst "
                    "nichts. Du liest ihn vor, zweimal.",
                "standard":
                    "Ein Brief mit schwarzem Rand liegt im Kasten, und das "
                    "Papier ist steif. „Gefallen für das Vaterland“ heisst "
                    "die Formel, und dass er nicht gelitten habe. "
                    "Eingetragen sind Datum und Ort, sonst nichts.",
              },
            },
            [
                Option(
                    "In Trauer gehen",
                    "Schwarzes Kleid, geschlossene Vorhänge, drei Tage.",
                    "Du wirst Teil der stillen Reihe auf der Straße. Die Nachbarinnen bringen, was sie entbehren können.",
                    aenderungen={"belastung": 2, "rueckhalt": 1},
                    stimmung="einsam"
                ),
                Option(
                    "Den Brief verbrennen",
                    "Du willst das Papier nicht im Haus haben.",
                    "Du sagst laut, wofür er gestorben sein soll. Im Treppenhaus wird es still, und jemand schließt eine Tür.",
                    aenderungen={"belastung": 0, "aufmerksamkeit": 1, "rueckhalt": -1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=10,
            quelle={
                "kurz": "Gefallenenmeldung: Vordruck mit eingetragenem Namen",
                "voll": QUELLE_FEHLT,
                "art": "brief",
                "einordnung": "Gesucht wird eine erhaltene Todesnachricht an "
                              "Angehörige, aus der hervorgeht, wie viel davon "
                              "vorgedruckt war. Der Vordruck zeigt die Form der "
                              "Mitteilung, nicht, was in dem Haus danach "
                              "geschah.",
            }
        ),

        Ereignis(
            "heimat_denunziation", [1915, 1916], "heimat",
            "Im Hof steht ein Schutzmann mit einem Block, und es riecht nach "
            "Waschtag. Im Hinterhaus soll jemand Mehl gehortet haben. Zwei "
            "Nachbarinnen waren heute früh schon auf der Wache. „Sie wohnen "
            "gegenüber, Sie haben das doch gesehen“, sagt er und wartet.",
            [
                ## "Bestaetigen" hat nur ein Wort und verstoesst gegen
                ## Handwerksregel e. Umbenannt in Paket 6, Schritt 2; der
                ## Titel ist an dieser Karte KEIN Schluessel eines
                ## Nachtrags - geprueft an DOMINANZ_NACHTRAG und beiden
                ## Kettennachtraegen.
                Option(
                    "Die Aussage bestätigen",
                    "Du sagst aus, was die anderen ausgesagt haben.",
                    "Am nächsten Tag wird die Wohnung durchsucht, und "
                    "gefunden wird wenig. Die Frau trägt ihre Sachen selbst "
                    "wieder hinauf. Im Treppenhaus grüßt dich seitdem "
                    "niemand mehr aus dem Hinterhaus.",
                    aenderungen={"aufmerksamkeit": -1, "rueckhalt": -2}
                ),
                Option(
                    "Nichts sagen",
                    "Du schließt die Tür und hältst dich heraus.",
                    "Der Schutzmann notiert, dass du keine Angaben machst. "
                    "Nun wird über dich geredet. Wer nichts sagt, hat etwas "
                    "zu verbergen, heißt es im Hof.",
                    aenderungen={"aufmerksamkeit": 1, "rueckhalt": 1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=10,
            quelle={
                "kurz": "Anzeigen wegen Hortens bei der Polizei",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Polizeiakten über Anzeigen aus der "
                              "Nachbarschaft wegen zurückgehaltener Lebensmittel. "
                              "Die Akte hält die Anzeige fest und nicht, was "
                              "danach im Treppenhaus zwischen den Parteien "
                              "blieb.",
            }
        ),

        Ereignis(
            "heimat_1915_brotkarte", [1915], "heimat",
            "Auf dem Tisch liegt das Brot der Woche, und es ist kleiner als "
            "der Teller. Seit Februar gilt die Brotkarte, und die Karte "
            "rechnet nicht mit Kindern, die wachsen. Du schneidest, und alle "
            "sehen zu. Für die Erwachsenen bleibt nichts, wenn die Kinder "
            "satt werden sollen.",
            [
                Option(
                    "Deinen Anteil abgeben",
                    "Du isst, was übrig bleibt.",
                    "Die Kleinen sind satt und schlafen durch. Dir wird beim "
                    "Treppensteigen schwarz vor Augen, und du bleibst auf "
                    "dem Absatz stehen. Es geht vorbei, jedes Mal.",
                    aenderungen={"versorgung": -2, "belastung": -1, "rueckhalt": 1}
                ),
                Option(
                    "Das Brot strecken",
                    "Kartoffelmehl, später auch anderes, kommt in den Teig.",
                    "Der Teig riecht anders und geht kaum auf. Es füllt den "
                    "Magen und liegt darin wie Sand. Zwei Tage später hat "
                    "das jüngste Kind Krämpfe.",
                    aenderungen={"versorgung": 0, "belastung": 1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=12, braucht=["kinder"],
            quelle={
                "kurz": "Brotkarte in Berlin ab 22. Februar 1915",
                "voll": "Einführung der Brotkarte in Berlin am 22. Februar 1915; "
                        "Deutsches Historisches Museum, LeMO, Kriegsalltag",
                "art": "darstellung",
                "einordnung": "Belegt sind Zeitpunkt und Verfahren der "
                              "Rationierung, die im März 1915 auf das ganze Reich "
                              "ausgedehnt wurde. Wie eine Familie die zugeteilte "
                              "Menge untereinander aufteilte, regelte keine "
                              "Verordnung.",
            }
        ),

        Ereignis(
            ## Seit Paket 6, Schritt 2 eine Fassung je Familienmerkmal. Die
            ## Begründung am Schalter ist jedes Mal eine andere, und jede
            ## ist zeitgenössisch: Der Satz richtete sich nach dem
            ## Verwandtschaftsgrad und nach dem, was vorher verdient wurde.
            "heimat_unterstuetzung", [1915, 1916], "heimat",
            {
                "ehemann_im_feld":
                    "Am Schalter des Gemeindeamts riecht es nach Bohnerwachs "
                    "und nassen Mänteln. Die Familienunterstützung für "
                    "Angehörige der Eingezogenen setzt die Gemeinde fest. "
                    "Der Betrag reicht nicht. „Ihr Mann war Hilfsarbeiter“, "
                    "sagt der Beamte, „danach richtet sich der Satz.“",
                "vater_im_feld":
                    "Am Schalter des Gemeindeamts riecht es nach Bohnerwachs "
                    "und nassen Mänteln. Die Familienunterstützung setzt die "
                    "Gemeinde fest, und für Kinder gibt es einen Zuschlag. "
                    "Der Betrag reicht nicht. „Für die Älteste zahlen wir "
                    "nicht mehr“, sagt der Beamte, „die kann arbeiten.“",
                "bruder_im_feld":
                    "Am Schalter des Gemeindeamts riecht es nach Bohnerwachs "
                    "und nassen Mänteln. Unterstützung bekommt, wer von dem "
                    "Eingezogenen gelebt hat. Ein Bruder gilt dabei nicht "
                    "ohne Weiteres. „Sie sind nicht unterhaltsberechtigt“, "
                    "sagt der Beamte und legt das Blatt zur Seite.",
                "standard":
                    "Am Schalter des Gemeindeamts riecht es nach Bohnerwachs "
                    "und nassen Mänteln. Die Familienunterstützung für "
                    "Angehörige der Eingezogenen setzt die Gemeinde fest. "
                    "Der Betrag reicht nicht, und der Beamte sagt, es liege "
                    "an der Einstufung.",
            },
            [
                Option(
                    "Widerspruch einlegen",
                    "Ein Schreiben, dann noch eines, dann ein Termin.",
                    "Nach elf Wochen wird der Satz um wenige Mark erhöht. In der Akte steht jetzt, du seiest schwierig im Umgang.",
                    aenderungen={"versorgung": 1, "belastung": 0, "aufmerksamkeit": 1}
                ),
                Option(
                    "Nebenher arbeiten",
                    "Heimarbeit am Abend, Nähen im Akkord.",
                    "Es reicht knapp. Du schläfst vier Stunden und siehst deine Kinder nur noch schlafend.",
                    aenderungen={"versorgung": 2, "belastung": 2, "rueckhalt": -1}
                ),
            ],
            ## Seit Paket 2, Schritt 2: braucht_eines statt braucht.
            ## Familienunterstützung bekam der Haushalt eines Eingezogenen -
            ## gleich, in welchem Verwandtschaftsgrad.
            ort="Gemeindeamt", gewicht=11,
            braucht_eines=["ehemann_im_feld", "vater_im_feld", "bruder_im_feld"],
            quelle={
                "kurz": "Familienunterstützung für Angehörige Eingezogener",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Gemeindeakten über Festsetzung und "
                              "Widerspruch bei der Familienunterstützung, samt den "
                              "Sätzen und ihrer Berechnung. Die Akte zeigt die "
                              "Einstufung und nicht, ob der Betrag zum Leben "
                              "reichte.",
            }
        ),

        Ereignis(
            "heimat_hamsterfahrt", [1915, 1916], "heimat",
            {
                1915: "Sonntags fahren sie mit dem Zug aufs Land und kommen mit vollen Rucksäcken zurück. Auf dem Bahnsteig steht neuerdings eine Kontrolle.",
                1916: "Die Hamsterfahrten sind verboten, und alle fahren trotzdem. Auf dem Bahnsteig wird jetzt jeder Rucksack geöffnet.",
            },
            [
                Option(
                    "Aufs Land fahren",
                    "Vier Stunden Zug, ein Bauernhof, Tauschware aus dem Schrank.",
                    "Du kommst mit Kartoffeln und Speck zurück. An der Sperre nehmen sie dir die Hälfte ab und deinen Namen dazu.",
                    hinweis="verboten",
                    aenderungen={"versorgung": 3, "aufmerksamkeit": 2, "belastung": 1},
                    kette="heimat_verfahren", kette_ab=1
                ),
                Option(
                    "Zu Hause bleiben",
                    "Das Risiko ist zu groß, und der Sonntag ist kurz.",
                    "Die Nachbarin kommt mit vollem Rucksack zurück und erzählt davon im Hof. Bei dir steht am Abend dasselbe auf dem Tisch wie gestern.",
                    aenderungen={"versorgung": -1, "belastung": 0}
                ),
            ],
            ort="Bahnhof", kern=True, gewicht=12,
            quelle={
                "kurz": "Hamsterfahrten und Bahnsteigkontrollen",
                "voll": "Stadtarchiv Solingen, Bergische Arbeiterstimme 1917, "
                        "Berichte über Hamsterfahrten und Beschlagnahmen",
                "art": "zeitung",
                "einordnung": "Belegt sind das Verbot der Ausfuhr bewirtschafteter "
                              "Lebensmittel aus dem Landkreis und die Kontrollen "
                              "an Bahnhöfen. Wie viele Fahrten unentdeckt blieben, "
                              "steht in keiner Statistik.",
            }
        ),

        Ereignis(
            ## Der Schachtelsatz von hier ("... eingestellt werden, wenn du
            ## bei anderen Angaben behilflich seist") ist in Paket 6,
            ## Schritt 2 in zwei Saetze geteilt. Er war der letzte im
            ## heimat_-Bestand.
            "heimat_verfahren", [1915, 1916], "heimat",
            "Auf dem Flur des Amtsgerichts steht eine Bank, und du sitzt "
            "seit einer Stunde darauf. Die Vorladung nennt einen Verstoß "
            "gegen die Höchstpreisverordnung. Der Beamte bietet an, das "
            "Verfahren einzustellen. Dafür sollst du bei anderen Angaben "
            "behilflich sein.",
            [
                Option(
                    "Namen nennen",
                    "Er will nur wissen, wer sonst noch fährt.",
                    "Er schreibt vier Namen auf und schiebt dir das Blatt "
                    "zum Unterschreiben hin. Das Verfahren wird eingestellt. "
                    "Im Hof spricht sich schnell herum, wer geredet hat und "
                    "ab wann.",
                    aenderungen={"aufmerksamkeit": -2, "rueckhalt": -3}
                ),
                Option(
                    "Nichts sagen",
                    "Du bleibst bei deiner Aussage.",
                    "Geldstrafe, ersatzweise Haft, steht auf dem Bescheid. "
                    "Du bezahlst in Raten und legst jeden Freitag etwas "
                    "beiseite. Wovon die letzte Rate kommen soll, weißt du "
                    "nicht.",
                    aenderungen={"versorgung": -3, "aufmerksamkeit": 1, "rueckhalt": 1}
                ),
            ],
            ort="Amtsgericht", nur_kette=True,
            quelle={
                "kurz": "Verfahren wegen Verstoßes gegen die Höchstpreise",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine Amtsgerichtsakte zu einem "
                              "Höchstpreisverfahren, aus der Geldstrafe und "
                              "Ersatzhaft hervorgehen. Sie zeigt das Urteil und "
                              "nicht, wer im Hof danach mit wem noch sprach.",
            }
        ),

        Ereignis(
            "heimat_fabrik", [1915, 1916], "heimat",
            {
                1915: "Zwölf Stunden Schicht in der Granatenfüllerei. Die Prämie gibt es nur auf das Stück, und der Vorarbeiter führt eine Liste.",
                1916: "Die Schicht ist auf vierzehn Stunden verlängert. Wer in der Rüstung arbeitet, bekommt Schwerarbeiterzulage. Wer die Stückzahl nicht schafft, bekommt sie nicht.",
            },
            [
                Option(
                    "Im Akkord arbeiten",
                    "Schneller, ohne Pause, für den Zuschlag.",
                    "Am Monatsende reicht das Geld für Fett auf dem Markt. Du hustest morgens, bis du etwas hochbringst.",
                    aenderungen={"versorgung": 2, "belastung": 2}
                ),
                Option(
                    "Sich Pausen nehmen",
                    "Ein paar Minuten mehr auf dem Abort, mehrmals am Tag.",
                    "Die Stückzahl sinkt. Der Vorarbeiter notiert deinen Namen und sagt, er behalte dich im Auge.",
                    aenderungen={"aufmerksamkeit": 1, "belastung": -1}
                ),
            ],
            ort="Rüstungsbetrieb", gewicht=10, wiederholbar=True,
            braucht=["ruestung"],
            quelle={
                "kurz": "Akkord und Schwerarbeiterzulage in der Rüstung",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Lohnlisten oder "
                              "Gewerbeaufsichtsberichte aus einer "
                              "Granatenfüllerei mit Schichtdauer und Stückzahlen. "
                              "Sie belegen Lohn und Arbeitszeit, nicht den "
                              "Husten, der nach Monaten blieb.",
            }
        ),

        Ereignis(
            "heimat_lazarettzug", [1915, 1916], ["heimat", "etappe"],
            "Am Güterbahnhof steht seit dem Morgen ein Zug mit roten Kreuzen "
            "an den Wagen. Es riecht nach Karbol, schon zwanzig Schritt "
            "entfernt. „Wer tragen kann, meldet sich hier“, ruft ein "
            "Sanitäter über die Köpfe. Was in den Waggons liegt, steht in "
            "keiner Zeitung.",
            [
                Option(
                    "Mit anfassen",
                    "Sechs Stunden Bahren, ohne Pause.",
                    "Die Griffe der Bahre schneiden dir in die Finger. Du "
                    "siehst Gesichter, die keine mehr sind. Danach kannst du "
                    "drei Nächte nicht schlafen und weißt endlich, wovon "
                    "geschwiegen wird.",
                    aenderungen={"belastung": 2, "rueckhalt": 2},
                    stimmung="erschoepft"
                ),
                Option(
                    "Am Zaun vorbeigehen",
                    "Du hast selbst genug zu tragen.",
                    "Du gehst am Zaun entlang und siehst nicht hin. Am Abend "
                    "erzählt die Nachbarin, wie sie geholfen hat. Du sagst, "
                    "du hättest davon nichts gewusst.",
                    aenderungen={"rueckhalt": -1}
                ),
            ],
            ort="Güterbahnhof", gewicht=9,
            quelle={
                "kurz": "Lazarettzüge und freiwillige Helferinnen am Bahnhof",
                "voll": QUELLE_FEHLT,
                "art": "bild",
                "einordnung": "Gesucht werden Fotografien oder Berichte über das "
                              "Entladen von Lazarettzügen und die Freiwilligen, "
                              "die dabei halfen. Bilder von Bahnsteigen wurden "
                              "gezeigt, Aufnahmen aus dem Inneren der Waggons "
                              "kaum.",
            }
        ),

        Ereignis(
            "heimat_1916_rueben", [1916], "heimat",
            "Auf dem Tisch liegen vier Steckrüben und ein Merkblatt mit "
            "Kochvorschlägen. Die Kartoffelernte ist im Herbst verdorben, "
            "und zugeteilt wird jetzt das hier. Die Küche riecht seit Tagen "
            "süßlich, und der Geruch geht aus den Kleidern nicht heraus. Am "
            "Stadtrand steht ein abgeerntetes Feld, auf dem noch etwas liegt.",
            [
                Option(
                    "Nachts aufs Feld",
                    "Zwei Stunden Fußweg, mit einem Sack unter dem Mantel.",
                    "Der Boden ist gefroren, und der Sack wird schwer. Der "
                    "Pächter schießt in die Luft, als er dich sieht. Du "
                    "kommst mit drei Rüben davon, und dein Name fällt am "
                    "nächsten Tag auf der Wache.",
                    hinweis="Feldfrevel",
                    aenderungen={"versorgung": 2, "aufmerksamkeit": 2, "belastung": 1}
                ),
                Option(
                    "Zur Ausgabestelle gehen",
                    "Anstellen und nehmen, was zugeteilt wird.",
                    "Die Suppe ist heißes Wasser mit Geschmack. Sie wärmt "
                    "eine halbe Stunde. Du wirst jede Woche ein Stück "
                    "leichter.",
                    aenderungen={"versorgung": -1, "belastung": 0}
                ),
            ],
            ort="Stadtrand", kern=True, gewicht=14,
            quelle={
                "kurz": "Steckrübenwinter 1916/17 nach der Kartoffelmissernte",
                "voll": "Steckrübenwinter 1916/17; Deutsches Historisches Museum, "
                        "LeMO, Kriegsalltag",
                "art": "darstellung",
                "einordnung": "Belegt sind die verdorbene Kartoffelernte des "
                              "Herbstes 1916 und die Zuteilung von Kohlrüben an "
                              "ihrer Stelle. Wie viele Menschen nachts auf "
                              "abgeerntete Felder gingen, ist nicht gezählt "
                              "worden.",
            }
        ),

        Ereignis(
            ## Seit Paket 6, Schritt 2 eine Fassung je Familienmerkmal. Die
            ## Frage des Formulars ist immer dieselbe - wer der
            ## Haushaltsvorstand ist -, und die Antwort ist jedes Mal eine
            ## andere. Genau daran hing 1916 die Zusatzkarte.
            "heimat_1916_ernaehrungsamt", [1916], "heimat",
            {
                "ehemann_im_feld":
                    "Im Mai wird das Kriegsernährungsamt errichtet; es soll "
                    "die Zuteilung im Reich ordnen. In deinem Bezirk gibt es "
                    "zunächst neue Formulare, und das Papier ist rau und "
                    "grau. In der ersten Zeile steht "
                    "„Haushaltsvorstand“, und darunter steht sein Name. Du "
                    "führst den Haushalt seit zwanzig Monaten allein.",
                "vater_im_feld":
                    "Im Mai wird das Kriegsernährungsamt errichtet; es soll "
                    "die Zuteilung im Reich ordnen. In deinem Bezirk gibt es "
                    "zunächst neue Formulare, und das Papier ist rau und "
                    "grau. In der ersten Zeile steht "
                    "„Haushaltsvorstand“, und die Mutter schiebt dir den "
                    "Bogen hin. Unterschreiben darf nur, wer volljährig ist.",
                "bruder_im_feld":
                    "Im Mai wird das Kriegsernährungsamt errichtet; es soll "
                    "die Zuteilung im Reich ordnen. In deinem Bezirk gibt es "
                    "zunächst neue Formulare, und das Papier ist rau und "
                    "grau. In der ersten Zeile steht "
                    "„Haushaltsvorstand“, und im Haus wohnen drei Parteien "
                    "aus einer Familie. Gezählt wird nach Küchen, nicht nach "
                    "Menschen.",
                "standard":
                    "Im Mai wird das Kriegsernährungsamt errichtet; es soll "
                    "die Zuteilung im Reich ordnen. In deinem Bezirk ändert "
                    "sich zunächst nur, dass es neue Formulare gibt; das "
                    "Papier ist rau und grau. In der ersten Zeile steht "
                    "„Haushaltsvorstand“, und das Feld darunter ist zu klein.",
            },
            [
                Option(
                    "Alles beantragen",
                    "Zusatzkarten für Schwerarbeit, für Kinder, für Kranke.",
                    "Von vier Anträgen wird einer bewilligt. Für die drei anderen hast du vier Vormittage in Fluren verbracht.",
                    aenderungen={"versorgung": 1, "belastung": 2}
                ),
                Option(
                    "Es lassen",
                    "Die Zeit fehlt, und bewilligt wird ohnehin wenig.",
                    "Die Nachbarin bekommt eine Zusatzkarte und zeigt sie im Hof herum. Du rechnest aus, wie viele Vormittage sie dafür gebraucht hat, und bleibst dabei.",
                    aenderungen={"versorgung": -1, "rueckhalt": -1}
                ),
            ],
            ort="Bezirksamt", gewicht=10,
            quelle={
                "kurz": "Kriegsernährungsamt, errichtet im Mai 1916",
                "voll": "Errichtung des Kriegsernährungsamtes im Mai 1916; "
                        "Deutsches Historisches Museum, LeMO, Kriegswirtschaft",
                "art": "darstellung",
                "einordnung": "Belegt sind Gründung und Auftrag, die Zuteilung im "
                              "ganzen Reich zu ordnen. Ob sich damit vor Ort "
                              "mehr änderte als die Zahl der Formulare, ist damit "
                              "nicht gesagt.",
            }
        ),

        Ereignis(
            "heimat_1916_kohle", [1916], "heimat",
            "An der Fensterscheibe steht innen das Eis in Blumen. Sieben "
            "Grad sind es in der Wohnung, und der Atem ist zu sehen. Die "
            "Kohle wird knapp, weil die Waggons an die Front gehen. „In "
            "vierzehn Tagen vielleicht“, sagt der Händler und schließt "
            "wieder ab.",
            [
                Option(
                    "In einem Raum leben",
                    "Alle Betten in die Küche, der Rest bleibt kalt.",
                    "Ihr schlaft zu viert in einem Zimmer und hustet euch "
                    "gegenseitig an. Warm wird es nur beim Kochen. Die "
                    "anderen Türen bleiben bis März zu.",
                    aenderungen={"belastung": 2, "rueckhalt": 1}
                ),
                Option(
                    "Vom Güterbahnhof holen",
                    "Nachts, an den Waggons, wie viele andere auch.",
                    "Zwei Eimer Briketts, und die Hände sind schwarz bis "
                    "zum Handgelenk. Zu Hause wird es zum ersten Mal seit "
                    "Wochen warm. Der Bahnpolizist kennt dein Gesicht jetzt, "
                    "und du kennst seines.",
                    hinweis="Diebstahl",
                    aenderungen={"versorgung": 1, "belastung": -1, "aufmerksamkeit": 2}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=12,
            quelle={
                "kurz": "Kohlenmangel: Waggons an der Front statt in der Stadt",
                "voll": QUELLE_FEHLT,
                "art": "zeitung",
                "einordnung": "Gesucht werden städtische Bekanntmachungen oder "
                              "Zeitungsberichte über ausbleibende Kohlenlieferungen "
                              "und Kohlendiebstahl an Güterbahnhöfen. Sie belegen "
                              "die Knappheit, nicht die sieben Grad in der "
                              "Wohnung.",
            }
        ),

        Ereignis(
            "heimat_1916_zensur", [1916], "heimat",
            "Der Brief von der Front liegt auf dem Küchentisch, und das "
            "Papier ist an drei Stellen dick vom Schwärzen. Du hältst ihn "
            "gegen das Fenster, und es hilft nichts. Was übrig bleibt, "
            "ergibt keinen Sinn. Im Hof heißt es, man dürfe darüber nicht "
            "sprechen.",
            [
                Option(
                    "Im Hof darüber reden",
                    "Du zeigst den Brief den Nachbarinnen.",
                    "Drei Frauen holen ihre eigenen geschwärzten Briefe und "
                    "legen sie nebeneinander. Zum ersten Mal seit Monaten "
                    "sprechen alle Klartext. Jemand hört zu, der nicht "
                    "dazugehört.",
                    aenderungen={"belastung": -2, "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
                Option(
                    "Den Brief wegschließen",
                    "Was durchkommt, muss reichen.",
                    "Du legst ihn zu den anderen in die Schublade und drehst "
                    "den Schlüssel um. Am Abend nimmst du ihn wieder heraus. "
                    "Du liest die Lücken und nicht die Wörter.",
                    aenderungen={"belastung": 1},
                    stimmung="einsam"
                ),
            ],
            ort="Wohnviertel", gewicht=10,
            quelle={
                "kurz": "Briefzensur und Stimmungsberichte der Überwachungsstellen",
                "voll": "Militärische Briefzensur im Ersten Weltkrieg; Deutsches "
                        "Historisches Museum, LeMO, Kriegsalltag",
                "art": "darstellung",
                "einordnung": "Belegt sind die stichprobenweise Prüfung der Post "
                              "und die Berichte, die aus dem Gelesenen entstanden. "
                              "Was in den geschwärzten Zeilen gestanden hat, ist "
                              "gerade nicht überliefert.",
            }
        ),

        Ereignis(
            "heimat_1916_arbeitsniederlegung", [1916], "heimat",
            "In der Mittagspause stehen sie in der Halle zusammen, und die "
            "Maschinen laufen leer weiter. Es geht um die Löhne und um die "
            "Zuteilung. „Einer muss anfangen“, sagt eine und sieht dabei "
            "niemanden an. Wer vorangeht, steht am nächsten Morgen auf einer "
            "Liste.",
            [
                ## ACHTUNG: "Vorangehen" ist ein Schluessel in
                ## KETTEN_NACHTRAG_PAKET4 (kapitel.rpy). Der Titel bleibt,
                ## auch wenn er nur ein Wort hat - siehe Entscheidung 16.
                Option(
                    "Vorangehen",
                    "Du sprichst vor der versammelten Belegschaft.",
                    "Deine Stimme trägt weiter, als du gedacht hast. Für "
                    "zwei Stunden stehen die Maschinen still. Dann kommt die "
                    "Werkleitung mit einem Beamten des stellvertretenden "
                    "Generalkommandos.",
                    hinweis="Belagerungszustand",
                    aenderungen={"aufmerksamkeit": 3, "belastung": -1, "rueckhalt": 2},
                    merkmale=["vorangegangen"]
                ),
                Option(
                    "An der Maschine bleiben",
                    "Du bleibst stehen, als die anderen hinausgehen.",
                    "Zwei Stunden lang bist du die Einzige, die arbeitet, "
                    "und es ist sehr laut. Am Abend liegt Lohn in der Tüte. "
                    "In der Umkleide spricht dich niemand mehr an.",
                    aenderungen={"versorgung": 1, "belastung": 1, "rueckhalt": -2}
                ),
            ],
            ort="Rüstungsbetrieb", gewicht=9, braucht=["ruestung"],
            quelle={
                "kurz": "Belagerungszustandsgesetz vom 4. Juni 1851",
                "voll": "Gesetz über den Belagerungszustand vom 4. Juni 1851, "
                        "Preußische Gesetz-Sammlung 1851",
                "art": "gesetz",
                "einordnung": "Das Gesetz überträgt die vollziehende Gewalt an die "
                              "Militärbefehlshaber und ist die Grundlage für "
                              "Schutzhaft und Betriebsaufsicht im Krieg. Es "
                              "benennt die Befugnis und nicht, wie oft davon "
                              "Gebrauch gemacht wurde.",
            }
        ),

        Ereignis(
            "heimat_1916_kinderarbeit", [1916], "heimat",
            "Am Werktor hängt ein Zettel, und die Tinte ist im Regen "
            "verlaufen. Der Betrieb stellt Jugendliche ein, weil die Männer "
            "fehlen. Dein ältestes Kind ist dreizehn und könnte zwölf Mark "
            "die Woche verdienen. Es steht neben dir und liest mit.",
            [
                Option(
                    "Es arbeiten schicken",
                    "Zwölf Mark sind zwölf Mark.",
                    "Am Freitag bringt es den Lohn nach Hause und legt ihn "
                    "auf den Tisch. Es ist stolz darauf, und du siehst es. "
                    "Nach vier Wochen schläft es beim Abendessen ein.",
                    aenderungen={"versorgung": 2, "belastung": 1, "rueckhalt": -1}
                ),
                Option(
                    "In der Schule lassen",
                    "Es soll den Abschluss haben, was auch kommt.",
                    "Ihr streckt die Zuteilung weiter, und der Tisch wird "
                    "leerer. Im Hof wird gefragt, wofür ein Abschluss gut "
                    "sein soll. Das Kind hört es und sagt nichts.",
                    aenderungen={"versorgung": -2, "rueckhalt": 1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=11, braucht=["aeltere_kinder"],
            quelle={
                "kurz": "Jugendliche in der Rüstung und die Schulpflicht",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Gewerbeaufsichtsberichte oder "
                              "Schulakten über die Beschäftigung Jugendlicher in "
                              "der Kriegswirtschaft und ihre Löhne. Sie zeigen "
                              "Zahlen und Lohnsätze, nicht die Entscheidung, die "
                              "am Küchentisch fiel.",
            }
        ),

        Ereignis(
            "front_ruhequartier", [1915, 1916], "front",
            "Nach acht Kilometern Marsch stehst du auf einer Dorfstraße, und "
            "es riecht nach Kuhstall. Zehn Tage Ruhequartier, sagt der "
            "Befehl, und dann geht es zurück. In der Scheune liegt Stroh, "
            "hinter dem Haus ist ein Teich. Der Feldwebel kündigt für morgen "
            "früh einen Appell an.",
            [
                ## Paket 3, Vorweg: aufmerksamkeit -1. Zehn Tage lang so
                ## wenig tun wie möglich heißt auch: in keiner Meldung
                ## vorkommen. Wer nicht auffällt, rückt aus dem Blick.
                Option(
                    "Schlafen und schweigen",
                    "Zehn Tage lang so wenig tun wie möglich.",
                    "Du schläfst zwölf Stunden am Stück. Beim Aufwachen "
                    "weißt du einen Moment lang nicht, wo du bist. Es ist "
                    "das erste Mal seit Monaten, dass dich nichts weckt.",
                    aenderungen={"belastung": -3, "versorgung": 1, "aufmerksamkeit": -1}
                ),
                Option(
                    "Zum Dorffest gehen",
                    "Es gibt Wein, eine Ziehharmonika und Menschen, die keine Uniform tragen.",
                    "Ihr singt bis zwei Uhr, und der Wein ist sauer und "
                    "warm. Am Morgen ist dir schlecht. Du hast zum ersten "
                    "Mal seit Wochen mit jemandem geredet.",
                    aenderungen={"belastung": -2, "versorgung": -1, "rueckhalt": 2}
                ),
            ],
            ort="Ruhequartier", kern=True, gewicht=12, wiederholbar=True,
            quelle={
                "kurz": "Ablösung und Ruhequartier im Stellungskrieg",
                "voll": QUELLE_FEHLT,
                "art": "erinnerung",
                "einordnung": "Gesucht werden Feldpost oder Kriegstagebücher über "
                              "den Turnus von Stellung und Ruhequartier und über "
                              "das, was dort geschah. Sie zeigen einzelne "
                              "Quartiere, nicht die Regel, denn der Turnus war "
                              "von Abschnitt zu Abschnitt verschieden.",
            }
        ),

        Ereignis(
            "heimat_sonntag", [1914, 1915, 1916], "heimat",
            {
                1914: "Ein Sonntag ohne Schlange, und du wachst von selbst "
                      "auf. Die Sonne steht über dem Hof und wärmt die "
                      "Fensterbank. Aus dem zweiten Stock hört man ein "
                      "Klavier. Für ein paar Stunden sieht die Stadt aus wie "
                      "vorher.",
                1915: "Ein Sonntag, und im Treppenhaus riecht es nach "
                      "echtem Kaffee. Die Nachbarin hat welchen, von "
                      "irgendwoher. „Komm doch heute Nachmittag rüber“, "
                      "sagt sie im Vorbeigehen. Der Korb mit der Wäsche "
                      "steht seit Freitag da.",
                1916: "Ein Sonntag ohne Sirene und ohne Ausgabe. Zum ersten "
                      "Mal seit Wochen ist ein ganzer Tag frei. Es ist so "
                      "still, dass du die Uhr im Flur hörst. Niemand weiß, "
                      "wofür der Tag da ist.",
            },
            [
                ## Paket 3, Vorweg: aufmerksamkeit -1. Ein Tag ohne
                ## Schlange, ohne Amt, ohne Wortwechsel im Hof ist ein Tag,
                ## an dem niemand etwas über dich aufschreibt.
                Option(
                    "Den Tag verstreichen lassen",
                    "Schlafen, sitzen, nichts erledigen.",
                    "Du sitzt am Fenster, bis der Hof im Schatten liegt. Am "
                    "Abend ist nichts geschafft und der Korb noch voll. Zum "
                    "ersten Mal seit Wochen hast du an nichts gedacht.",
                    aenderungen={"belastung": -3, "aufmerksamkeit": -1}
                ),
                Option(
                    "Zu den Nachbarinnen gehen",
                    "Ein Nachmittag am Tisch, mit anderen.",
                    "Der Kaffee ist dünn und heiß, und die Tassen passen "
                    "nicht zusammen. Ihr redet über alles außer über den "
                    "Krieg, und irgendwann doch über ihn. Es ist der erste "
                    "Nachmittag seit langem, an dem gelacht wird.",
                    aenderungen={"belastung": -2, "rueckhalt": 2, "versorgung": -1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=12, wiederholbar=True,
            quelle={
                "kurz": "Sonntag als freier Tag im Kriegsalltag",
                "voll": QUELLE_FEHLT,
                "art": "erinnerung",
                "einordnung": "Gesucht werden Tagebücher oder Briefe aus der "
                              "Heimat, in denen ein Sonntag ohne Schlange und "
                              "ohne Ausgabe vorkommt. Solche Tage wurden selten "
                              "aufgeschrieben, weil an ihnen nichts geschah.",
            }
        ),

    ]


    EREIGNIS_INDEX = {}
    for vorlage in EREIGNISSE:
        EREIGNIS_INDEX[vorlage.kennung] = vorlage

    def ereignis_holen(kennung):
        return EREIGNIS_INDEX.get(kennung)

    ## JAHRESFASSUNG UND MERKMALSFASSUNG - Paket 6, Schritt 2 #################
    ##
    ## Bis hierher lief der Ereignistext ausschliesslich durch
    ## jahrestext(). Ein Wörterbuch mit Merkmalen als Schlüssel wäre nie
    ## aufgelöst worden: jahrestext() findet keine Jahreszahl und liefert
    ## den Zweig "standard" zurück. Die drei Familienmerkmale aus Paket 2
    ## liessen sich damit in keiner Karte einsetzen, obwohl die Verfassung
    ## variante() genau dafür vorsieht.
    ##
    ## ereignistext() entscheidet nach den Schlüsseln der äusseren Ebene:
    ## Jahreszahlen gehören jahrestext(), Merkmale und Pfade gehören
    ## variante(). Beides lässt sich schachteln, und der Aufruf wiederholt
    ## sich, bis kein Wörterbuch mehr übrig ist.
    ##
    ## WARUM NICHT EINFACH szenentext(): Der ruft variante() ZUERST. Eine
    ## reine Jahrestafel wie die von front_trommelfeuer fände dort weder
    ## Merkmal noch Pfad noch "standard" und liefe in die Rückfallebene -
    ## der Text wäre leer, und Probe 2c zählte einen Griff. Die Reihenfolge
    ## muss sich nach den Schlüsseln richten, nicht umgekehrt.
    def ereignistext(vorgaben):
        if not isinstance(vorgaben, dict):
            return vorgaben
        if any(isinstance(schluessel, int) for schluessel in vorgaben):
            ergebnis = jahrestext(vorgaben, aktuelles_jahr)
        else:
            ergebnis = variante(vorgaben)
        if isinstance(ergebnis, dict):
            return ereignistext(ergebnis)
        return ergebnis

    ############################################################################
    ## WIE GROSS DER EREIGNISTEXT GESETZT WIRD
    ############################################################################
    ##
    ## SEIT PAKET 8. Der Ereignistext stand in einem Feld von 1440 mal 170
    ## Pixeln, und die Schrift ist 34 Pixel hoch mit 10 Pixeln Zeilenabstand
    ## — eine Zeile braucht also 44, und in 170 passen 3,9. Gemessen am
    ## ganzen Bestand: 184 Textfassungen, davon brauchen
    ##
    ##     2 Zeilen     5 Fassungen     2,7 %
    ##     3 Zeilen    32 Fassungen    17,4 %
    ##     4 Zeilen   122 Fassungen    66,3 %
    ##     5 Zeilen    24 Fassungen    13,0 %
    ##     6 Zeilen     1 Fassung       0,5 %
    ##
    ## VIER VON FÜNF LIEFEN ÜBER. Bei vier Zeilen sind es sechs Pixel und
    ## niemand sieht es; bei fünf sind es fünfundzwanzig nach oben, und der
    ## Text steht in der Kopfleiste (AUFGEFALLEN 77). Das Feld war zu klein,
    ## nicht der Text zu lang: Die Handwerksregel verlangt drei bis fünf
    ## Sätze, und das sind vier Zeilen.
    ##
    ## Das Feld hält jetzt fünf Zeilen. Für die längsten Fassungen reicht
    ## auch das nicht, deshalb rückt die Schrift dort eine Stufe herunter.
    ## Die Grenze ist gerechnet, nicht geraten: Bei 34 Pixeln passen rund 78
    ## Zeichen in eine Zeile, fünf Zeilen sind also 390 Zeichen — aber schon
    ## ab 330 wird es eng, sobald ein langes Wort umbricht.
    EREIGNIS_TEXT_GRUND = 34
    EREIGNIS_TEXT_ENG = 30
    EREIGNIS_TEXT_GRENZE = 330

    def ereignis_schriftgroesse(text, grund=None):
        """Die Schriftgröße für einen Ereignistext.

        Nimmt die Grundgröße entgegen, statt sie festzuschreiben: Paket 8,
        Schritt 2 stellt die Schrift dreistufig, und dann muss diese Stufe
        mitwandern statt danebenzustehen.
        """
        if grund is None:
            grund = EREIGNIS_TEXT_GRUND
        if not text or len(str(text)) < EREIGNIS_TEXT_GRENZE:
            return grund
        return int(round(grund * EREIGNIS_TEXT_ENG / float(EREIGNIS_TEXT_GRUND)))

    def ereignis_text_von(vorlage):
        return ereignistext(vorlage.text)

    def option_beschreibung_von(auswahl):
        return jahrestext(auswahl.beschreibung, aktuelles_jahr)

    def option_titel_von(auswahl):
        return jahrestext(auswahl.titel, aktuelles_jahr)

    def ereignis_passt(vorlage, jahr, pfad, modus):
        if vorlage.nur_kette:
            return False
        if jahr not in vorlage.jahre:
            return False
        if pfad not in vorlage.pfad:
            return False
        if modus == "kurz" and not vorlage.kern:
            return False
        if vorlage.kennung in gespielte_ereignisse:
            return False
        for name in vorlage.braucht:
            if name not in merkmale:
                return False
        for name in vorlage.verbietet:
            if name in merkmale:
                return False
        return True

    def ereignisse_verfuegbar(jahr, pfad, modus):
        gefunden = []
        for vorlage in EREIGNISSE:
            if ereignis_passt(vorlage, jahr, pfad, modus):
                gefunden.append(vorlage)
        return gefunden

    def gewichtet_ziehen(eintraege, gewicht_von):
        gesamt = 0
        for eintrag in eintraege:
            gesamt = gesamt + max(1, gewicht_von(eintrag))
        if gesamt <= 0:
            return eintraege[0]
        wurf = renpy.random.randint(1, gesamt)
        laufend = 0
        for eintrag in eintraege:
            laufend = laufend + max(1, gewicht_von(eintrag))
            if wurf <= laufend:
                return eintrag
        return eintraege[-1]

    def ereignis_vormerken(kennung, ab_jahr):
        global vorgemerkte_ereignisse
        if not kennung:
            return
        vorgemerkte_ereignisse = vorgemerkte_ereignisse + [{"kennung": kennung, "ab_jahr": ab_jahr}]

    ## Wann ein vorgemerktes Kettenglied gezogen wird ##########################
    ##
    ## SEIT PAKET 3, SCHRITT 2 wird auch das Jahr geprüft.
    ##
    ## Vorher prüfte diese Funktion nur ab_jahr, den Pfad und ob das
    ## Ereignis schon gespielt war - NICHT sein jahre-Feld. Ein 1916
    ## vorgemerktes Glied konnte dadurch 1917, 1918 oder 1919 erscheinen,
    ## also in Jahren, für die es nie geschrieben wurde. In der Messung war
    ## das der einzige Grund, warum 1917 überhaupt noch Ereignisse gezogen
    ## wurden: 47 von 13579. Das war keine Deckung, das war ein Fehler.
    ##
    ## Was bleibt liegen, wird nicht verworfen: Ein Glied, dessen Jahr
    ## vorbei ist, bleibt vorgemerkt, solange ein späteres Jahr in seinem
    ## jahre-Feld steht. Erst wenn kein Jahr mehr kommt, in dem es stehen
    ## dürfte, wird es aussortiert - und probe_alles.py zählt, wie oft das
    ## geschieht.

    def kette_offen_zaehlen(jahr):
        """Wie viele Vormerkungen können nie mehr eingelöst werden?"""
        verfallen = 0
        for eintrag in vorgemerkte_ereignisse:
            vorlage = ereignis_holen(eintrag["kennung"])
            if vorlage is None:
                verfallen = verfallen + 1
                continue
            if not [j for j in vorlage.jahre if j >= jahr]:
                verfallen = verfallen + 1
        return verfallen

    def kette_faellig(jahr, pfad):
        global vorgemerkte_ereignisse
        for stelle in range(len(vorgemerkte_ereignisse)):
            eintrag = vorgemerkte_ereignisse[stelle]
            if eintrag["ab_jahr"] > jahr:
                continue
            vorlage = ereignis_holen(eintrag["kennung"])
            if vorlage is None:
                continue
            if eintrag["kennung"] in gespielte_ereignisse:
                continue
            if pfad not in vorlage.pfad:
                continue
            ## Neu seit Paket 3: Das Glied gehört in dieses Jahr, oder es
            ## wartet auf ein Jahr, in dem es stehen darf.
            if jahr not in vorlage.jahre:
                continue
            vorgemerkte_ereignisse = vorgemerkte_ereignisse[:stelle] + vorgemerkte_ereignisse[stelle + 1:]
            return eintrag["kennung"]
        return None

    ## Auf welche Kettenglieder zeigt überhaupt jemand? ########################
    ##
    ## SEIT PAKET 5, SCHRITT 3, TEIL D.15c. Ein Ereignis mit nur_kette wird
    ## nie frei gezogen; es erscheint nur, wenn eine Option es vormerkt. Wer
    ## wissen will, welcher Bestand im Spiel überhaupt erscheinen kann,
    ## braucht deshalb diese Liste. probe_alles.py hat sie sich bisher selbst
    ## zusammengesucht - eine zweite Formulierung derselben Regel, und die
    ## erste, die veraltet, sobald eine Kette anders gesetzt wird.
    ##
    ## Die Einlagen sind hier NICHT enthalten: Sie merken über
    ## einlage_anwenden() ebenfalls vor, gehören aber minispiele.rpy und
    ## werden dort gesammelt (einlagen_ketten_sammeln).

    def kettenziele():
        """Alle Kennungen, auf die eine Option als Kette zeigt."""
        ziele = set()
        for vorlage in EREIGNISSE:
            for auswahl in vorlage.optionen:
                if getattr(auswahl, "kette", None):
                    ziele.add(auswahl.kette)
                for eintrag in (getattr(auswahl, "varianten", None) or []):
                    if eintrag.get("kette"):
                        ziele.add(eintrag["kette"])
        return ziele

    def ereignis_ziehen(jahr, pfad, modus):
        aus_kette = kette_faellig(jahr, pfad)
        if aus_kette:
            return aus_kette
        auswahl = ereignisse_verfuegbar(jahr, pfad, modus)
        if not auswahl:
            return None
        gewaehlt = gewichtet_ziehen(auswahl, lambda e: e.gewicht)
        return gewaehlt.kennung

    def variante_ziehen(varianten):
        return gewichtet_ziehen(varianten, lambda v: v.get("gewicht", 1))

    def option_ausfuehren(kennung, stelle):
        global ziehungen_im_kapitel
        vorlage = ereignis_holen(kennung)
        gewaehlt = vorlage.optionen[stelle]
        aenderungen = dict(gewaehlt.aenderungen)
        ausgang = jahrestext(gewaehlt.ausgang, aktuelles_jahr)
        neue_merkmale = list(gewaehlt.merkmale)
        sprung = gewaehlt.sprung
        stimmung = gewaehlt.stimmung if gewaehlt.stimmung else vorlage.stimmung
        if gewaehlt.varianten:
            variante = variante_ziehen(gewaehlt.varianten)
            for schluessel, betrag in variante.get("aenderungen", {}).items():
                aenderungen[schluessel] = aenderungen.get(schluessel, 0) + betrag
            if variante.get("ausgang"):
                ausgang = jahrestext(variante["ausgang"], aktuelles_jahr)
            neue_merkmale = neue_merkmale + list(variante.get("merkmale", []))
            if variante.get("sprung"):
                sprung = variante["sprung"]
            if variante.get("stimmung"):
                stimmung = variante["stimmung"]
        protokoll_eintragen(kennung, jahrestext(gewaehlt.titel, aktuelles_jahr))
        ziehungen_im_kapitel = ziehungen_im_kapitel + 1
        if sprung:
            stimmung_setzen(None)
            return {"ausgang": ausgang, "sprung": sprung}
        zustand_aendern(aenderungen)
        for name in neue_merkmale:
            merkmal_setzen(name)
        if gewaehlt.kette:
            ereignis_vormerken(gewaehlt.kette, aktuelles_jahr + gewaehlt.kette_ab)
        stimmung_setzen(stimmung)
        return {"ausgang": ausgang, "sprung": None}


init -20 python:

    ## PAKET 8, SCHRITT 2.4 — ONBOARDING (Teil B, Punkte 5 und 6)
    ##
    ## Die drei Grundsätze des Spiels. Auf dem Bildschirm steht nur der
    ## erste Satz; der zweite erscheint, sobald die Maus den ersten
    ## berührt oder anklickt. Getrennt gehalten, damit der Bildschirm aus
    ## drei kurzen Sätzen besteht und nicht aus einem Absatz, den in
    ## dreißig Sekunden niemand liest.
    ##
    ## Die Sätze stehen hier und nicht in screens.rpy: Diese Datei liest
    ## die Werkbank, screens.rpy durchsucht sie nur nach Bildschirmnamen
    ## (NUR_BILDSCHIRME in probe_alles.py). Text, den niemand messen kann,
    ## soll im Projekt nicht entstehen.
    GRUNDSAETZE = [
        ("zurueck", "Es gibt kein Zurück."),
        ("spielstand", "Es gibt keinen Spielstand."),
        ("antwort", "Es gibt keine richtige Antwort."),
    ]

    ## Genau ein Satz je Grundsatz, wie im Auftrag verlangt.
    GRUNDSATZ_MEHR = {
        "zurueck": "Was du gewählt hast, bleibt gewählt — auch dann, wenn es sich später als Fehler herausstellt.",
        "spielstand": "Du kannst nicht speichern und nicht laden: Ein Durchgang wird von Anfang bis Ende in einem Zug gespielt.",
        "antwort": "Beide Wege sind vertretbar, und wer damals entschied, wusste nicht, was im nächsten Jahr kommen würde.",
    }

    GRUNDSATZ_AUFFORDERUNG = "Fahre mit der Maus über einen der drei Sätze, wenn du mehr dazu wissen willst."


default versorgung = 6
default belastung = 2
default aufmerksamkeit = 1
default rueckhalt = 8

default merkmale = []
default gespielte_ereignisse = []
default protokoll = []
default letzte_aenderungen = {}
default vorgemerkte_ereignisse = []

default aktuelles_jahr = 1914
default aktueller_pfad = "heimat"
default spielmodus = "lang"
default stimmung_erzwungen = None
default ziehungen_im_kapitel = 0

## PAKET 8, SCHRITT 2.4 — die Kopfleiste als bedienbar erkennbar machen
## (Teil B, Punkt 7).
##
## kopfleiste_entdeckt wird wahr, sobald die Maus zum ersten Mal einen der
## vier Werte berührt. Danach verschwindet der Hinweis und kommt in diesem
## Durchgang nicht wieder. Kein persistent: Am Schulrechner setzt sich nach
## dem Durchgang die nächste Schülerin davor, und für die wäre der Hinweis
## dann schon verbraucht.
##
## wert_gepinnt hält den Wert fest, dessen Erklärung angeheftet ist. Ohne
## das Anheften muss die Maus die ganze Lesezeit über auf einem 250 Pixel
## breiten Feld stillstehen — für einen langen Erklärkasten mit fünf Stufen
## ist das keine Bedienung, sondern eine Geschicklichkeitsübung.
default kopfleiste_entdeckt = False
default wert_gepinnt = None

## Die Lebenslage (Herkunft, Musterung, Erwerb) liegt in herkunft.rpy.
default gewaehlte_herkunft = None
default pruefungsfunde = []
default letztes_ergebnis = {}
default letzte_wahl = 0
default aktuelles_ereignis = None
default letztes_ende = None
default naechste_kennung = None
default folgejahr = None


image bg papier = Solid(FARBE_PAPIER)
image bg dunkel = Solid(FARBE_DUNKEL)
image bg blut = Solid(FARBE_BLUT)


label start:

    $ zustand_zuruecksetzen()

    ## PAKET 8, SCHRITT 2.6. Was im Hauptmenü lief, endet hier. Ohne diese
    ## Zeile liefe die Menümusik in das Spiel hinein, sobald für die Moduswahl
    ## keine eigene Datei vorliegt — und an der Front wäre sie damit doch zu
    ## hören, obwohl die Sperre sie dort nie freigegeben hätte.
    $ ton_still("musik")
    $ ton_still("umgebung")

    ## Paket 7, Schritt 1: Das eingebaute "dissolve" von Ren'Py bringt eine
    ## feste halbe Sekunde mit und hört auf keinen Schalter. Deshalb steht
    ## hier wie überall der benannte Übergang.
    scene bg papier
    with UEBERGANG_KARTE()

    ## PAKET 8, SCHRITT 2.6. Drei der Stellen, an denen Musik nach
    ## Entscheidung 24 möglich wäre. Sie liegen alle vor dem ersten Ereignis,
    ## also bevor ein Pfad feststeht — hier ist Musik unbedenklich. Solange
    ## MUSIK_EINGESCHALTET auf False steht, tun die drei Zeilen nichts.
    $ musik_setzen("moduswahl")

    call screen modus_waehlen
    $ spielmodus = _return

    $ musik_setzen("onboarding")

    call screen hinweis_unumkehrbar

    $ musik_setzen("jahreskarte")

    call screen jahreskarte(aktuelles_jahr)

    ## Paket 2: Herkunft, Musterung und Erwerbslage. Der Abschnitt steht
    ## vollständig in herkunft.rpy und endet mit einem Sprung in die
    ## hauptschleife. Die frühere Figurenwahl entfällt.
    jump lebenslage_bestimmen


label hauptschleife:

    $ letztes_ende = ende_pruefen()

    if letztes_ende:
        jump expression letztes_ende

    if ziehungen_im_kapitel >= ziehungen_pro_kapitel():
        jump kapitelwechsel

    $ naechste_kennung = ereignis_ziehen(aktuelles_jahr, aktueller_pfad, spielmodus)

    if naechste_kennung is None:
        jump kapitelwechsel

    call ereignis_spielen(naechste_kennung)

    if letztes_ergebnis["sprung"]:
        jump expression letztes_ergebnis["sprung"]

    jump hauptschleife


label ereignis_spielen(kennung):

    $ gespielte_ereignisse = gespielte_ereignisse + [kennung]
    $ aktuelles_ereignis = kennung
    $ stimmung_setzen(ereignis_holen(kennung).stimmung)

    ## PAKET 8, SCHRITT 2.6. Der Umgebungsklang des Ortes. Diese Marke wird
    ## von ereignis_spielen_mit_einlage (minispiele.rpy) überschrieben und
    ## läuft nicht; dort steht dieselbe Zeile an derselben Stelle. Sie steht
    ## hier mit, damit die beiden Fassungen nicht auseinanderlaufen (Regel 9).
    $ ortsklang_setzen(ereignis_holen(kennung).ort)

    call screen karten_entscheidung(kennung)

    $ letzte_wahl = _return
    $ letztes_ergebnis = option_ausfuehren(kennung, letzte_wahl)

    call screen karten_ausgang(kennung, letzte_wahl, letztes_ergebnis["ausgang"])

    $ stimmung_setzen(None)

    return


label kapitelwechsel:

    ## PAKET 8, SCHRITT 2.6. Ein Jahr endet: Der Umgebungsklang blendet aus.
    ## Auch diese Marke wird überschrieben; dieselbe Zeile steht in
    ## kapitelwechsel_mit_schicksal (figuren.rpy) an derselben Stelle.
    $ ton_still("umgebung")

    ## Jahresabschluss: kurzer Rückblick auf das Jahr, das zu Ende geht.
    ## Der Epilog bekommt keinen Rückblick, weil er selbst einer ist.
    if aktuelles_jahr != EPILOG_JAHR:
        call screen jahresabschluss(aktuelles_jahr)

    $ folgejahr = naechstes_kapitel(aktuelles_jahr)

    if folgejahr is None:
        jump ende_ueberlebt

    $ aktuelles_jahr = folgejahr
    $ ziehungen_im_kapitel = 0
    $ wiederholbare_freigeben()

    ## Die Kapitelwirkung hängt seit Paket 3 auch am Pfad und meldet
    ## zurück, was nach der Begrenzung wirklich angekommen ist.
    $ letzte_kapitelwirkung = kapitel_wirkung_anwenden(aktuelles_jahr)

    ## Paket 7, Schritt 1: der Fade über FARBE_DUNKEL beim Jahreswechsel.
    ## Diese Marke wird von kapitelwechsel_mit_schicksal (figuren.rpy)
    ## überschrieben; dort steht dieselbe Zeile an derselben Stelle.
    $ renpy.transition(UEBERGANG_KAPITEL())

    $ musik_setzen("epilog" if aktuelles_jahr == EPILOG_JAHR else "jahreskarte")

    call screen jahreskarte(aktuelles_jahr, letzte_kapitelwirkung)

    jump hauptschleife


## PAKET 8, SCHRITT 2.6. Vor jedem der vier harten Enden wird es still. Ein
## Ende ist ein Einschnitt; ein Grabenklang, der unter "Gefallen" weiterläuft,
## wäre der falsche Ton. Die Zeile steht viermal einzeln und nicht an einer
## gemeinsamen Stelle, weil ein Ende auch aus einer Wahl heraus angesprungen
## werden kann und dann an der hauptschleife vorbeiliefe.
label ende_verhungert:
    $ ton_still("umgebung")
    call screen ende_bildschirm(
        "Verhungert",
        "Die Kräfte reichen nicht mehr für den Weg zur Ausgabestelle. Eines Morgens stehst du nicht mehr auf. In der Sterbeurkunde steht Herzschwäche."
    )
    jump ende_abschluss


label ende_zusammenbruch:
    $ ton_still("umgebung")
    call screen ende_bildschirm(
        "Zusammengebrochen",
        "Du hörst nicht mehr auf zu zittern. Ein Arzt schreibt Kriegsneurose in die Akte, ein anderer schreibt Simulation. Behandelt wird beides gleich."
    )
    jump ende_abschluss


label ende_verhaftet:
    $ ton_still("umgebung")
    call screen ende_bildschirm(
        "Abgeholt",
        "Zwei Beamte stehen morgens vor der Tür. Das stellvertretende Generalkommando hat Schutzhaft angeordnet, gestützt auf das Gesetz über den Belagerungszustand. Ein Gericht kommt darin nicht vor, und über die Dauer entscheidet niemand, den du fragen könntest."
    )
    jump ende_abschluss


label ende_gefallen:
    $ ton_still("umgebung")
    call screen ende_bildschirm(
        "Gefallen",
        "Ein Pfeifen, ein Schlag, sonst nichts. Die Meldung geht drei Wochen später hinaus. Auf dem Formular ist der Name eingetragen, alles andere ist vorgedruckt."
    )
    jump ende_abschluss


## Wer den Epilog erreicht, bekommt seit Paket 3 kein festes Ende mehr,
## sondern einen Lebenslauf, der aus den vier Stufen, dem Pfad und den
## gesammelten Merkmalen berechnet wird. Der Ablauf steht in kapitel.rpy.
label ende_ueberlebt:
    jump ende_lebenslauf


label ende_abschluss:

    if _return == "neustart":
        jump start

    return

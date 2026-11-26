################################################################################
##
##  herkunft.rpy
##
##  Paket 2: Herkunft, Musterung und Erwerbslage
##
##  Ersetzt die feste Figurenwahl (FIGUREN_FRONT / FIGUREN_HEIMAT).
##  Der Spielweg entsteht jetzt aus drei Schritten:
##
##      1. HERKUNFT     Milieu, Geschlecht, Jahrgang. Setzt Startwerte
##                      und Merkmale.
##      2. MUSTERUNG    wird ausgewürfelt, abhängig von Alter, Herkunft
##                      und Zeitpunkt. Anzeige als Musterungsbogen.
##      3. PFAD         k.v. = Front, g.v. = Etappe, a.v. und d.u. = Heimat.
##                      Unabkömmlich gestellte und zurückgestellte Männer
##                      bleiben in der Heimat. Alle Zivilpersonen fällen
##                      danach eine Erwerbsentscheidung.
##
##  Grundsätze, die in dieser Datei gelten:
##  - Steuerung ausschließlich mit der Maus. Keine key-Anweisungen.
##  - Das Geschlecht bestimmt NICHT den Pfad. Frauen erreichen über den
##    Lazarettdienst die Etappe, Männer bleiben über u.k., a.v., d.u.
##    oder Zurückstellung in der Heimat.
##  - Varianten laufen über merkmale und aktueller_pfad, niemals über
##    Figuren- oder Personennamen. Der erzeugte Name ist reine Anzeige.
##  - Warten auf den Einberufungsbefehl ist das gesetzlich vorgesehene
##    Normalverhalten. Es kostet keinen Wert und trägt keine Strafe.
##  - Keine Begriffe aus der NS-Zeit. Die Sprachprüfung in Abschnitt 10
##    prüft den gesamten Ereignisbestand darauf.
##
##  DER ETAPPENPFAD IST SEIT PAKET 5, SCHRITT 1 WIEDER OFFEN.
##  Der Vermerk, der hier stand, ist erledigt: Der Bestand ist
##  geschrieben (18 eigene Ereignisse, kapitel.rpy Abschnitt 10f), und
##  die Etappe hat eine eigene Stimme statt der geliehenen Frontfassung.
##  ETAPPE_FREIGESCHALTET steht wieder auf True, g.v. Gemusterte kommen
##  wieder in die Etappe statt zum Ersatztruppenteil in der
##  Heimatgarnison. Die Begründung mit allen Zahlen steht über dem
##  Schalter in Abschnitt 1.
##
##  ZWEI WEGE, ZWEI ROLLEN. Wer über die Musterung kommt, ist Soldat im
##  Etappendienst; wer über den Lazarettdienst kommt, ist Lazarettkraft
##  und trägt das Merkmal lazarett zwingend. Kein Text des Pfades setzt
##  eine der beiden Rollen voraus. Siehe den Kommentar bei
##  etappe_moeglich in Abschnitt 7.
##
################################################################################


################################################################################
## 1. Konstanten
################################################################################
##
## init -19 läuft nach allen init -20 Blöcken. Dadurch stehen die Vorgaben
## aus script.rpy und dialoge.rpy hier bereits zur Verfügung und können
## erweitert werden.

init -19 python:

    ## Schalter für den Etappenpfad ###########################################
    ##
    ## SEIT DEM 4. SEPTEMBER 2026 WIEDER OFFEN — Paket 5, Schritt 1.
    ##
    ## Von Paket 2, Schritt 1 bis hierher war er geschlossen, und das aus
    ## zwei Gründen. Der erste war der Bestand: 1914 ein einziges frei
    ## ziehbares Ereignis bei einem Soll von zwei im kurzen und fünf im
    ## langen Verlauf, 1917 und 1918 gar keines. Der zweite war die
    ## stille Ersetzung: 126220 Griffe in die Rückfallebene je Messung,
    ## an 43 Stellen, ausnahmslos von der Etappe zur Front. Wer dort
    ## spielte, las Sätze, die für den Graben geschrieben waren.
    ##
    ## BEIDES IST ERLEDIGT. Womit gefüllt:
    ##
    ##   Teil A   18 eigene Etappenereignisse (kapitel.rpy, Abschnitt 10f)
    ##            über Bahnhof, Magazin, Rampe, Schreibstube, Feldbäckerei,
    ##            Munitionslager, Fuhrpark, Zensurstelle, Gefangenenlager,
    ##            Gefangenenarbeit, Requisition, Zwangsarbeit im besetzten
    ##            Gebiet, Grippe und Räumung. Dazu 1914 an
    ##            heimat_lazarettzug. Frei ziehbar je Jahr 1914 bis 1918:
    ##            kurz 6 9 10 9 10, lang 10 15 17 16 15 — jede Zeile über
    ##            Soll plus Reserve.
    ##   Teil B   201 von 204 Variantenwörterbüchern haben eine eigene
    ##            Etappenfassung; die drei übrigen gehören zur Einlage
    ##            hamsterfahrt, die nur in der Heimat vorkommt. Alle vier
    ##            Rückfallzweige laufen über eine Regel, beide Notlösungen
    ##            sind gestrichen, briefwelt() kennt drei Welten, und die
    ##            Etappe hat acht eigene Briefe.
    ##
    ## Was das Umlegen bewirkt: g.v. gemusterte Männer kommen wieder in
    ## die Etappe statt zum Ersatztruppenteil in der Heimatgarnison, und
    ## der Lazarettdienst führt wieder hinaus - einstieg_etappe wird
    ## damit von selbst wieder gerufen (siehe label lebenslage_zivil).
    ##
    ## Was noch fehlt und WISSENTLICH offen bleibt: 1919. Der Epilog hat
    ## auf keinem der drei Pfade Bestand; das ist Schritt 2 dieses
    ## Pakets. Für die Etappe heißt das dasselbe wie für Front und
    ## Heimat, nicht mehr und nicht weniger.

    ETAPPE_FREIGESCHALTET = True

    ## Merkmalsreihenfolge erweitern ##########################################
    ##
    ## dialoge.rpy prüft Textvarianten in dieser Reihenfolge. Das
    ## speziellere Merkmal steht vorn.

    ## SEIT PAKET 2, SCHRITT 2 stehen die drei Familienmerkmale hinter den
    ## Erwerbslagen und vor der Herkunft. Damit gilt für einen Text mit
    ## mehreren Fassungen: Was jemand arbeitet, sticht; wer ihm fehlt,
    ## sticht danach; woher er kommt, zuletzt. Eine Näherin, deren Mann im
    ## Feld steht, liest die Näherinnenfassung - und erst wenn es die nicht
    ## gibt, die Fassung für den fehlenden Mann.
    ##
    ## Der Auftrag nennt für diese Liste dialoge.rpy. Dort steht die
    ## Grundlage (init -20); gültig ist diese Fassung hier (init -19), weil
    ## sie später läuft. Geändert wird deshalb hier.
    MERKMALS_REIHENFOLGE = [
        "offizier",
        "adel",
        "buergertum",
        "lazarett",
        "ruestung",
        "landwirtschaft",
        "verwaltung",
        "wohlfahrt",
        "haushalt",
        "ehemann_im_feld",
        "vater_im_feld",
        "bruder_im_feld",
        "arbeiterschaft",
        "landbevoelkerung",
    ]

    ## Musterung #############################################################

    MUSTERUNG_GRADE = ["kv", "gv", "av", "du"]

    MUSTERUNG_KURZ = {
        "kv": "k. v.",
        "gv": "g. v.",
        "av": "a. v.",
        "du": "d. u.",
    }

    MUSTERUNG_LANG = {
        "kv": "kriegsverwendungsfähig",
        "gv": "garnisonsverwendungsfähig",
        "av": "arbeitsverwendungsfähig",
        "du": "dauernd untauglich",
    }

    MUSTERUNG_ERKLAERUNG = {
        "kv": "Tauglich für den Dienst im Felde. Du wirst einem Feldtruppenteil überwiesen und kommst an die Front.",
        "gv": "Tauglich für den Dienst in der Garnison und hinter der Front, nicht für den Kampf in vorderster Linie.",
        "av": "Nur für Arbeitsleistungen tauglich. Du bleibst im Reich und wirst zu Arbeiten herangezogen.",
        "du": "Für den Militärdienst untauglich. Du wirst aus der Liste gestrichen und bleibst zu Hause.",
    }

    VERMERK_KURZ = {
        "uk": "u. k.",
        "zurueck": "zurückgestellt",
    }

    VERMERK_LANG = {
        "uk": "unabkömmlich gestellt",
        "zurueck": "Jahrgang noch nicht aufgerufen",
    }

    VERMERK_ERKLAERUNG = {
        "uk": "Du bist tauglich, wirst aber in deinem Betrieb gebraucht. Die Einberufung wird zurückgestellt, solange du auf dieser Stelle bleibst. Wer die Stelle verlässt, verliert die Zurückstellung.",
        "zurueck": "Dein Jahrgang ist noch nicht aufgerufen. Du wartest auf den Einberufungsbefehl. Das ist der Regelfall und kein Makel.",
    }

    ## Altersgruppen und Heeresklassen #######################################
    ##
    ## Die Bezeichnungen entsprechen der Wehrverfassung des Kaiserreichs.

    ALTERSGRUPPEN = [
        (17, 19, "landsturm_jung", "Landsturm ersten Aufgebots"),
        (20, 22, "aktiv", "aktive Dienstpflicht"),
        (23, 27, "aktiv", "Reserve"),
        (28, 32, "landwehr", "Landwehr ersten Aufgebots"),
        (33, 38, "landwehr", "Landwehr zweiten Aufgebots"),
        (39, 45, "landsturm_alt", "Landsturm zweiten Aufgebots"),
    ]

    ## Zur Wahl stehende Lebensalter im Sommer 1914.
    ##
    ## SEIT PAKET 2, SCHRITT 2: zwei statt vier.
    ## Vorher standen 17, 23, 30 und 39 zur Wahl. Vier Alter sind für eine
    ## achte Klasse eine Wahl zu viel: Die Unterschiede zwischen 23 und 30
    ## sind für Dreizehnjährige nicht zu erkennen, und wer vier Karten
    ## nebeneinander legt, wählt die erste. Zwei Alter stellen den
    ## Unterschied heraus, um den es geht - ungebunden gegen verantwortlich.
    ##
    ## 18 fällt in den Landsturm ersten Aufgebots (17 bis 19),
    ## 35 in die Landwehr zweiten Aufgebots (33 bis 38). Siehe
    ## ALTERSGRUPPEN oben: zwei verschiedene Heeresklassen, also auch
    ## sichtbar verschiedene Musterungsaussichten.

    JAHRGANGSWAHL = [18, 35]

    ## Was auf der Wahlkarte unter dem Alter steht. Kein Urteil, eine Lage.
    JAHRGANG_MARKE = {
        18: "Gerade volljährig, ungebunden",
        35: "Mitten im Leben, Verantwortung",
    }

    ## Grundpunkte der Musterung nach Altersgruppe. Die Punkte werden
    ## addiert und danach ausgewürfelt. Sie sind keine Statistik, sondern
    ## eine spielbare Annäherung an die bekannten Größenordnungen.

    MUSTERUNG_GRUNDWERTE = {
        "landsturm_jung": {"kv": 40, "gv": 20, "av": 10, "du": 5, "zurueck": 25},
        "aktiv": {"kv": 58, "gv": 18, "av": 12, "du": 7, "zurueck": 5},
        "landwehr": {"kv": 44, "gv": 24, "av": 16, "du": 11, "zurueck": 5},
        "landsturm_alt": {"kv": 24, "gv": 28, "av": 26, "du": 17, "zurueck": 5},
    }

    ## Wer aus der Stadt kommt, ist im Schnitt schlechter ernährt und
    ## häufiger vorgeschädigt. Wer auf dem Land arbeitet, besteht die
    ## Untersuchung häufiger.

    MUSTERUNG_HERKUNFT = {
        "arbeiterschaft": {"kv": -8, "av": 6, "du": 2},
        "buergertum": {"kv": 2, "gv": 2, "av": -4},
        "landbevoelkerung": {"kv": 8, "av": -4, "du": -4},
        "adel": {"kv": 6, "gv": 2, "av": -4, "du": -4},
    }

    ## Zeitpunkt der Untersuchung. Im August 1914 waren die Kommissionen
    ## streng, weil sich mehr meldeten, als gebraucht wurden. Mit den
    ## Verlusten wurden die Maßstäbe weiter gefasst.

    MUSTERUNG_STRENGE = {
        "august_1914": {"kv": -6, "du": 4, "zurueck": 6},
        "einberufung": {"kv": 4, "zurueck": -4},
    }

    ## Wahrscheinlichkeit in Prozent, dass ein tauglicher Mann als
    ## unabkömmlich zurückgestellt wird. Entscheidend ist, ob seine
    ## Arbeit als kriegswichtig gilt.

    UK_WAHRSCHEINLICHKEIT = {
        "arbeiterschaft": 18,
        "buergertum": 10,
        "landbevoelkerung": 22,
        "adel": 14,
    }

    ## Ärztliche Befunde als Beiwerk des Bogens. Sie ändern nichts,
    ## machen die Entscheidung der Kommission aber nachvollziehbar.

    MUSTERUNG_BEFUNDE = {
        "kv": [
            "ohne Befund",
            "kräftiger Körperbau, ohne Befund",
            "Zähne mangelhaft, sonst ohne Befund",
        ],
        "gv": [
            "Kurzsichtigkeit beiderseits",
            "Plattfüße",
            "Brustumfang unter dem Maß",
            "Krampfadern am linken Bein",
        ],
        "av": [
            "allgemeine Körperschwäche",
            "Leistenbruch",
            "Herzfehler leichten Grades",
            "erhebliches Untergewicht",
        ],
        "du": [
            "schweres Herzleiden",
            "Lungenspitzenkatarrh",
            "Verlust zweier Finger der rechten Hand",
            "hochgradige Kurzsichtigkeit",
        ],
    }

    ## Bildkennungen #########################################################
    ##
    ## Porträts werden nach Herkunft und Geschlecht abgelegt, nicht nach
    ## Namen. Muster: images/portraits/<herkunft>_<geschlecht>_<stimmung>.png

    def lebenslage_bildkennung():
        if lebenslage is None:
            return None
        return str(lebenslage.herkunft) + "_" + str(lebenslage.geschlecht)


################################################################################
## 2. Datentypen
################################################################################

init -10 python:

    class Herkunft(object):
        """Ein Milieu. Setzt Startwerte, Merkmale und den Friedensberuf.

        werte     Abweichung von der Pfadgrundlage aus script.rpy
        berufe    {"m": [...], "w": [...]} Friedensberufe
        namen     {"m": [...], "w": [...]} Vornamen
        familien  Familiennamen
        """

        def __init__(self, kennung, titel, zusatz, text, folge,
                     werte=None, merkmale=None, berufe=None,
                     namen=None, familien=None):
            self.kennung = kennung
            self.titel = titel
            self.zusatz = zusatz
            self.text = text
            self.folge = folge
            self.werte = werte if werte else {}
            self.merkmale = merkmale if merkmale else [kennung]
            self.berufe = berufe if berufe else {"m": [""], "w": [""]}
            self.namen = namen if namen else {"m": [""], "w": [""]}
            self.familien = familien if familien else [""]

    class Erwerb(object):
        """Eine Erwerbslage für Zivilpersonen.

        braucht_herkunft   leere Liste bedeutet: für alle Milieus offen
        nur_geschlecht     None, "m" oder "w"
        verbietet_merkmal  Merkmale, die diese Lage ausschließen
        hinweis_fuer       Milieus, für die diese Lage unüblich war
        etappe_moeglich    stellt danach die Frage nach dem Etappendienst
        """

        def __init__(self, kennung, titel, zusatz, text, folge,
                     bezeichnung, werte=None, merkmale=None,
                     braucht_herkunft=None, nur_geschlecht=None,
                     verbietet_merkmal=None, hinweis_fuer=None,
                     etappe_moeglich=False):
            self.kennung = kennung
            self.titel = titel
            self.zusatz = zusatz
            self.text = text
            self.folge = folge
            self.bezeichnung = bezeichnung
            self.werte = werte if werte else {}
            self.merkmale = merkmale if merkmale else [kennung]
            self.braucht_herkunft = braucht_herkunft if braucht_herkunft else []
            self.nur_geschlecht = nur_geschlecht
            self.verbietet_merkmal = verbietet_merkmal if verbietet_merkmal else []
            self.hinweis_fuer = hinweis_fuer if hinweis_fuer else []
            self.etappe_moeglich = etappe_moeglich

    class Lebenslage(object):
        """Der vollständige Personenstand des Hauptcharakters.

        Ersetzt die früheren Spielfigur-Objekte. Es gibt keine feste
        Figurenliste mehr: Jede Lebenslage entsteht neu aus Wahl und Wurf.
        """

        def __init__(self):
            self.herkunft = None
            self.geschlecht = "w"
            self.alter = 0
            self.jahrgang = 0
            self.vorname = ""
            self.familienname = ""
            self.friedensberuf = ""
            self.groesse = 170
            self.brustumfang = 84
            self.heeresklasse = ""
            self.musterung = None
            self.vermerk = None
            self.befund = "ohne Befund"
            self.erwerb = None
            self.stand = ""
            self.pfad = "heimat"

        def name(self):
            return (self.vorname + " " + self.familienname).strip()


################################################################################
## 3. Funktionen
################################################################################
##
## init -4 läuft nach den Hilfsfunktionen aus script.rpy (init -5). Damit
## stehen wert_begrenzen(), zustand_aendern() und merkmal_setzen() bereit.

init -4 python:

    ## Sprachliche Beugung ####################################################
    ##
    ## Das Geschlecht darf ausschließlich die Wortform bestimmen, niemals
    ## einen Pfad oder eine Bedingung. Deshalb gibt es genau diese eine
    ## Funktion dafür und kein Merkmal "mann" oder "frau".

    def gebeugt(maennlich, weiblich):
        if lebenslage is not None and lebenslage.geschlecht == "m":
            return maennlich
        return weiblich

    ## Zugriff auf die Bestände ###############################################

    def herkunft_holen(kennung):
        return HERKUNFT_INDEX.get(kennung)

    def erwerb_holen(kennung):
        return ERWERB_INDEX.get(kennung)

    def aktuelle_herkunft():
        if lebenslage is None:
            return None
        return herkunft_holen(lebenslage.herkunft)

    ## Alter und Heeresklasse #################################################

    def altersgruppe(alter):
        for unten, oben, schluessel, bezeichnung in ALTERSGRUPPEN:
            if unten <= alter <= oben:
                return schluessel, bezeichnung
        if alter < 17:
            return "landsturm_jung", "noch nicht wehrpflichtig"
        return "landsturm_alt", "über der Wehrpflicht"

    def ist_wehrpflichtig():
        if lebenslage is None:
            return False
        if lebenslage.geschlecht != "m":
            return False
        return 17 <= lebenslage.alter <= 45

    ## Musterung würfeln ######################################################
    ##
    ## Der Wurf ist offen nachvollziehbar: verteilung_holen() liefert die
    ## Punktetabelle, die im Analysemodus angezeigt und von der
    ## Musterungsprobe in Abschnitt 10 geprüft werden kann.

    def musterung_verteilung(herkunft_kennung, alter, strenge):
        schluessel, bezeichnung = altersgruppe(alter)
        werte = dict(MUSTERUNG_GRUNDWERTE.get(schluessel, MUSTERUNG_GRUNDWERTE["aktiv"]))
        for quelle in (MUSTERUNG_HERKUNFT.get(herkunft_kennung, {}),
                       MUSTERUNG_STRENGE.get(strenge, {})):
            for name, betrag in quelle.items():
                werte[name] = max(0, werte.get(name, 0) + betrag)
        return werte

    def musterung_wuerfeln(herkunft_kennung, alter, strenge):
        verteilung = musterung_verteilung(herkunft_kennung, alter, strenge)
        gesamt = sum(verteilung.values())
        if gesamt <= 0:
            gezogen = "kv"
        else:
            wurf = renpy.random.randint(1, gesamt)
            laufend = 0
            gezogen = "kv"
            for name in ["kv", "gv", "av", "du", "zurueck"]:
                laufend = laufend + verteilung.get(name, 0)
                if wurf <= laufend:
                    gezogen = name
                    break

        ## Zurückgestellt heißt: tauglich befunden, aber noch nicht
        ## aufgerufen. Der Grad wird trotzdem eingetragen.
        if gezogen == "zurueck":
            grad = "kv" if renpy.random.randint(1, 100) <= 70 else "gv"
            vermerk = "zurueck"
        else:
            grad = gezogen
            vermerk = None

        ## Unabkömmlichkeit kommt nur für tauglich Befundene in Frage
        ## und wird vom Betrieb oder von der Gemeinde beantragt.
        if vermerk is None and grad in ("kv", "gv"):
            schwelle = UK_WAHRSCHEINLICHKEIT.get(herkunft_kennung, 12)
            if renpy.random.randint(1, 100) <= schwelle:
                vermerk = "uk"

        schluessel, bezeichnung = altersgruppe(alter)

        return {
            "grad": grad,
            "vermerk": vermerk,
            "befund": renpy.random.choice(MUSTERUNG_BEFUNDE.get(grad, ["ohne Befund"])),
            "heeresklasse": bezeichnung,
            "strenge": strenge,
        }

    def pfad_aus_musterung(ergebnis):
        """Setzt die Zuweisung aus der Aufgabenstellung um.

        k.v. an die Front, g.v. in die Etappe, a.v. und d.u. in die
        Heimat. Ein Vermerk (u.k. oder zurückgestellt) geht immer vor:
        Wer zurückgestellt ist, rückt nicht ein.
        """
        if ergebnis is None:
            return "heimat"
        if ergebnis.get("vermerk") in ("uk", "zurueck"):
            return "heimat"
        grad = ergebnis.get("grad")
        if grad == "kv":
            return "front"
        if grad == "gv":
            return "etappe" if ETAPPE_FREIGESCHALTET else "heimat"
        return "heimat"

    ## Werte und Pfad #########################################################

    def pfad_wechseln(neuer_pfad):
        """Rechnet die Differenz zwischen zwei Pfadgrundlagen auf.

        Alle Personen beginnen im Juli 1914 auf der Heimatgrundlage.
        Wer eingezogen wird, bekommt die Differenz zur Front- oder
        Etappengrundlage aufgeschlagen. Dadurch bleiben alle Änderungen
        erhalten, die vorher schon gefallen sind.
        """
        global aktueller_pfad
        alt = PFAD_BASIS.get(aktueller_pfad, PFAD_BASIS["heimat"])
        neu = PFAD_BASIS.get(neuer_pfad, PFAD_BASIS["heimat"])
        unterschied = {}
        for schluessel in WERTE_REIHENFOLGE:
            unterschied[schluessel] = neu.get(schluessel, 0) - alt.get(schluessel, 0)
        zustand_aendern(unterschied)
        aktueller_pfad = neuer_pfad
        if lebenslage is not None:
            lebenslage.pfad = neuer_pfad
        ## PAKET 8, SCHRITT 2.6. Hier fällt der Pfad, und hier greift Regel 3
        ## zum ersten Mal. Was vorher lief — Menümusik, Moduswahl,
        ## Jahreskarte 1914 —, ist an einer Stelle angeworfen worden, an der
        ## Musik erlaubt war. Ab dieser Zeile ist sie es womöglich nicht mehr,
        ## und dann endet sie sofort statt beim nächsten Tonaufruf.
        musik_sperre_durchsetzen()

    ## Aufbau der Lebenslage ##################################################

    def lebenslage_zuruecksetzen():
        global lebenslage
        lebenslage = None

    def person_erzeugen(herkunft_kennung, geschlecht, alter):
        """Legt die Lebenslage an und setzt die Startwerte.

        Der Name wird gezogen und ist reine Anzeige. Keine Bedingung im
        Spiel darf sich jemals auf ihn stützen.
        """
        global lebenslage, versorgung, belastung, aufmerksamkeit, rueckhalt

        quelle = herkunft_holen(herkunft_kennung)
        neue = Lebenslage()
        neue.herkunft = herkunft_kennung
        neue.geschlecht = geschlecht
        neue.alter = alter
        neue.jahrgang = KAPITEL_JAHRE[0] - alter
        neue.vorname = renpy.random.choice(quelle.namen.get(geschlecht, [""]))
        neue.familienname = renpy.random.choice(quelle.familien)
        neue.friedensberuf = renpy.random.choice(quelle.berufe.get(geschlecht, [""]))
        neue.groesse = renpy.random.randint(158, 184)
        neue.brustumfang = renpy.random.randint(78, 96)
        neue.heeresklasse = altersgruppe(alter)[1]
        neue.stand = neue.friedensberuf
        neue.pfad = "heimat"
        lebenslage = neue

        ## Startwerte: Heimatgrundlage plus Milieuabweichung.
        basis = PFAD_BASIS["heimat"]
        versorgung = wert_begrenzen(basis["versorgung"] + quelle.werte.get("versorgung", 0))
        belastung = wert_begrenzen(basis["belastung"] + quelle.werte.get("belastung", 0))
        aufmerksamkeit = wert_begrenzen(basis["aufmerksamkeit"] + quelle.werte.get("aufmerksamkeit", 0))
        rueckhalt = wert_begrenzen(basis["rueckhalt"] + quelle.werte.get("rueckhalt", 0))

        for name in quelle.merkmale:
            merkmal_setzen(name)

        ## Wer Kinder im Haushalt hat, bekommt später andere Ereignisse.
        ## Abgeleitet aus dem Alter, damit keine weitere Frage nötig wird.
        ## "aeltere_kinder" meint schulpflichtige Kinder, die ab 1916
        ## selbst zur Arbeit geschickt werden konnten.
        ##
        ## Seit Paket 2, Schritt 2 stehen nur noch 18 und 35 zur Wahl. Die
        ## beiden Schwellen bleiben stehen, weil sie weiter richtig
        ## trennen: 18 bekommt keines der beiden Merkmale, 35 beide. Wer
        ## JAHRGANGSWAHL wieder erweitert, sieht sich diese Zeilen an.
        if alter >= 23:
            merkmal_setzen("kinder")
        if alter >= 30:
            merkmal_setzen("aeltere_kinder")

        protokoll_eintragen("herkunft", quelle.titel + ", " + gebeugt("männlich", "weiblich") + ", Jahrgang " + str(neue.jahrgang))

    def musterung_eintragen(strenge):
        """Würfelt die Musterung und trägt sie in die Lebenslage ein."""
        if lebenslage is None:
            return None
        ergebnis = musterung_wuerfeln(lebenslage.herkunft, lebenslage.alter, strenge)
        lebenslage.musterung = ergebnis["grad"]
        lebenslage.vermerk = ergebnis["vermerk"]
        lebenslage.befund = ergebnis["befund"]
        merkmal_setzen("gemustert")
        if ergebnis["vermerk"] == "uk":
            merkmal_setzen("uk")
        if ergebnis["vermerk"] == "zurueck":
            merkmal_setzen("zurueckgestellt")
        protokoll_eintragen("musterung", musterung_kurztext())
        return ergebnis

    def musterung_kurztext():
        if lebenslage is None or lebenslage.musterung is None:
            return "nicht gemustert"
        text = MUSTERUNG_KURZ.get(lebenslage.musterung, "")
        if lebenslage.vermerk:
            text = text + ", " + VERMERK_KURZ.get(lebenslage.vermerk, "")
        return text

    ## Familienlage ###########################################################
    ##
    ## Seit Paket 2, Schritt 2. Setzt genau eines der drei Merkmale, die
    ## sagen, wer aus diesem Haushalt eingezogen worden ist. Sie stehen im
    ## MERKMAL_REGISTER (kapitel.rpy) und tragen je einen Nachklang für den
    ## Lebenslauf. Zwei von ihnen gleichzeitig gibt es nicht: Das Spiel
    ## erzählt eine Lage, keine Familienchronik.

    FAMILIE_IM_FELD = ["ehemann_im_feld", "vater_im_feld", "bruder_im_feld"]

    def familienlage_setzen():
        """Bestimmt, wer aus diesem Haushalt fort ist, und merkt es an."""
        if lebenslage is None:
            return None

        ## Achtzehn heißt: Man wohnt noch im Elternhaus. Der Vater ist
        ## eingezogen, gleich ob Tochter oder zurückgestellter Sohn.
        if lebenslage.alter <= 19:
            name = "vater_im_feld"
        elif lebenslage.geschlecht == "w":
            name = "ehemann_im_feld"
        else:
            ## SEIT PAKET 3, VORWEG: für JEDEN Mann im Zivilzweig, nicht
            ## nur für den zurückgestellten oder unabkömmlichen.
            ##
            ## Vorher stand hier eine Bedingung auf zurueckgestellt oder
            ## uk. Wer als arbeitsverwendungsfähig oder dauernd untauglich
            ## ausgemustert wurde, bekam damit gar kein Familienmerkmal -
            ## und war von heimat_1914_post und heimat_unterstuetzung
            ## ausgeschlossen, weil beide braucht_eines darauf prüfen.
            ##
            ## Das war eine Nebenwirkung, keine Absicht. Ob ein Mann
            ## selbst tauglich ist, sagt nichts darüber, ob sein Bruder
            ## eingezogen wurde. 1914 hatte fast jede Familie jemanden im
            ## Feld: Bis Kriegsende dienten rund dreizehn Millionen Männer,
            ## etwa jeder fünfte Einwohner des Reiches. Ein Haushalt ohne
            ## irgendjemanden im Feld war die Ausnahme, nicht der Regelfall.
            name = "bruder_im_feld"

        merkmal_setzen(name)
        return name

    def dienststellung_setzen():
        """Legt die Dienstbezeichnung für die Kopfleiste fest."""
        if lebenslage is None:
            return
        if lebenslage.pfad == "front":
            if hat_merkmal("offizier"):
                lebenslage.stand = "Offiziersaspirant"
            else:
                lebenslage.stand = "Musketier"
        elif lebenslage.pfad == "etappe" and lebenslage.musterung is not None:
            lebenslage.stand = "Landsturmmann, Etappe"

    ## Erwerbslage ############################################################

    def erwerb_auswahl():
        """Liefert die Erwerbslagen, die zu dieser Person passen."""
        gefunden = []
        if lebenslage is None:
            return gefunden
        for eintrag in ERWERBSLAGEN:
            if eintrag.nur_geschlecht and eintrag.nur_geschlecht != lebenslage.geschlecht:
                continue
            if eintrag.braucht_herkunft and lebenslage.herkunft not in eintrag.braucht_herkunft:
                continue
            gesperrt = False
            for name in eintrag.verbietet_merkmal:
                if hat_merkmal(name):
                    gesperrt = True
            if gesperrt:
                continue
            gefunden.append(eintrag)
        return gefunden[:4]

    ## Selten heißt nicht verboten ############################################
    ##
    ## SEIT PAKET 2, SCHRITT 2. Frauen arbeiteten 1914 in der Rüstung und im
    ## Kontor - nur sehr viel seltener als ab 1915. Diese Wege zu SPERREN
    ## würde behaupten, es habe diese Frauen nicht gegeben. Stattdessen
    ## steht auf der Karte, wie selten es war. Die Spielerin entscheidet
    ## danach selbst, und die Wahl bleibt ihre.

    ERWERB_HINWEIS_1914 = {
        "ruestung": "1914 noch selten: Die Werke stellten Frauen erst ab 1915 in größerer Zahl ein.",
        "verwaltung": "1914 noch selten: In den Kontoren saßen zu Kriegsbeginn fast nur Männer.",
    }

    def erwerb_hinweis(eintrag):
        """Stempel für Wege, die in dieser Lage unüblich waren."""
        if lebenslage is None:
            return None
        if lebenslage.herkunft in eintrag.hinweis_fuer:
            return "unüblich"
        if lebenslage.geschlecht == "w" and eintrag.kennung in ERWERB_HINWEIS_1914:
            return "1914 selten"
        return None

    def erwerb_hinweis_text(eintrag):
        """Der Satz unter dem Stempel: warum es unüblich oder selten war."""
        if lebenslage is None:
            return ""
        if lebenslage.geschlecht == "w" and eintrag.kennung in ERWERB_HINWEIS_1914:
            return ERWERB_HINWEIS_1914[eintrag.kennung]
        if lebenslage.herkunft in eintrag.hinweis_fuer:
            return "In deinem Milieu ging diesen Weg fast niemand. Offen steht er trotzdem."
        return ""

    def erwerb_uebernehmen(kennung):
        if lebenslage is None:
            return
        eintrag = erwerb_holen(kennung)
        if eintrag is None:
            return
        lebenslage.erwerb = kennung
        lebenslage.stand = eintrag.bezeichnung.get(lebenslage.geschlecht, "")
        zustand_aendern(eintrag.werte)
        for name in eintrag.merkmale:
            merkmal_setzen(name)
        protokoll_eintragen("erwerb", eintrag.titel)

    def erwerb_bezeichnung_etappe():
        """Die Bezeichnung ändert sich, wenn der Dienst in die Etappe führt."""
        if lebenslage is None:
            return
        lebenslage.stand = gebeugt("Etappenlazarett", "Etappenlazarett")

    ## Zulieferer für die Bildschirme #########################################

    def bogen_felder():
        """Die Zeilen des Musterungsbogens."""
        if lebenslage is None:
            return []
        return [
            ("Name und Stand", lebenslage.name() + ", " + lebenslage.friedensberuf),
            ("Geburtsjahr", str(lebenslage.jahrgang)),
            ("Heeresklasse", lebenslage.heeresklasse),
            ("Körpergröße", str(lebenslage.groesse) + " Zentimeter"),
            ("Brustumfang", str(lebenslage.brustumfang) + " Zentimeter"),
            ("Ärztlicher Befund", lebenslage.befund),
        ]

    def pfad_erlaeuterung(daten):
        """Sagt in einem Satz, was der Bogen für den Spielverlauf bedeutet."""
        ziel = pfad_aus_musterung(daten)
        if ziel == "front":
            return "Du wirst einem Feldregiment überwiesen. In wenigen Wochen stehst du an der Westfront."
        if ziel == "etappe":
            return "Du kommst zu einer Formation hinter der Front. Die Etappe versorgt, verwaltet und bewacht alles, was der Krieg braucht."
        if daten.get("vermerk") == "uk":
            return "Du bleibst zu Hause, solange du auf deiner Stelle bleibst. Über die Zurückstellung entscheidet nicht dein Wille, sondern der Bedarf."
        if daten.get("vermerk") == "zurueck":
            return "Du bleibst zu Hause und wartest auf den Befehl. Die meisten Männer deines Jahrgangs tun im Sommer 1914 genau das."
        return "Du bleibst in der Heimat. Für dich entscheidet sich der Krieg an anderen Stellen: an der Ladentheke, am Werktor und am Briefkasten."

    def wurf_uebersicht():
        """Legt im Analysemodus offen, mit welchen Anteilen gewürfelt wurde."""
        if lebenslage is None or musterungsdaten is None:
            return []
        verteilung = musterung_verteilung(
            lebenslage.herkunft,
            lebenslage.alter,
            musterungsdaten.get("strenge", "einberufung")
        )
        gesamt = max(1, sum(verteilung.values()))
        zeilen = []
        for name in ["kv", "gv", "av", "du"]:
            anteil = int(round(100.0 * verteilung.get(name, 0) / gesamt))
            zeilen.append((MUSTERUNG_LANG.get(name, name), str(anteil) + " Prozent"))
        anteil = int(round(100.0 * verteilung.get("zurueck", 0) / gesamt))
        zeilen.append(("Jahrgang nicht aufgerufen", str(anteil) + " Prozent"))
        zeilen.append((
            "danach unabkömmlich gestellt",
            str(UK_WAHRSCHEINLICHKEIT.get(lebenslage.herkunft, 12)) + " Prozent bei Tauglichkeit"
        ))
        return zeilen

    def offizierslaufbahn_offen():
        """Die Berechtigung zum einjährig-freiwilligen Dienst hing am
        Schulabschluss und damit faktisch am Elternhaus."""
        if lebenslage is None:
            return False
        if lebenslage.geschlecht != "m":
            return False
        if lebenslage.alter < 19:
            return False
        return lebenslage.herkunft in ("adel", "buergertum")

    def erwerb_einleitung():
        if lebenslage is None:
            return ""
        if hat_merkmal("uk"):
            return "Du bist tauglich und bleibst trotzdem hier, weil deine Arbeit gebraucht wird. Die Zurückstellung hängt an der Stelle, die du jetzt wählst."
        if hat_merkmal("zurueckgestellt"):
            return "Dein Jahrgang ist noch nicht aufgerufen. Bis der Befehl kommt, muss deine Familie von etwas leben."
        if lebenslage.geschlecht == "m":
            return "Du bleibst in der Heimat. Auch hier wird jede Hand gebraucht, und auch hier wird gezählt, was du leistest."
        return "Die Männer sind fort, die Preise steigen, und die Miete läuft weiter. Womit ihr durch diesen Krieg kommt, entscheidest du."

    def uebersicht_felder():
        if lebenslage is None:
            return []
        quelle = aktuelle_herkunft()
        felder = [
            ("Name", lebenslage.name() + ", " + str(lebenslage.alter) + " Jahre"),
            ("Herkunft", quelle.titel + " - " + quelle.zusatz),
            ("Beruf im Frieden", lebenslage.friedensberuf),
        ]
        if lebenslage.musterung:
            eintrag = MUSTERUNG_KURZ.get(lebenslage.musterung, "") + "  (" + MUSTERUNG_LANG.get(lebenslage.musterung, "") + ")"
            if lebenslage.vermerk:
                eintrag = eintrag + ", " + VERMERK_LANG.get(lebenslage.vermerk, "")
            felder.append(("Musterung", eintrag))
        else:
            felder.append(("Musterung", "nicht gemustert"))
        felder.append(("Stand ab jetzt", lebenslage.stand))
        felder.append((
            "Wo du den Krieg erlebst",
            PFAD_MARKE.get(aktueller_pfad, "") + ", " + PFAD_ORT.get(aktueller_pfad, "")
        ))
        return felder

    def lage_schlusssatz():
        if aktueller_pfad == "front":
            return "Von hier an entscheidest du nicht mehr, wo du bist. Du entscheidest nur noch, was du dort tust."
        if aktueller_pfad == "etappe":
            return "Du bist Teil des Heeres, ohne im Graben zu liegen. Das ist ein Unterschied, und es ist keiner."
        return "Der Krieg findet Hunderte Kilometer entfernt statt und bestimmt trotzdem jeden deiner Tage."

    ## Werkzeug für die Dialogprobe ###########################################
    ##
    ## Baut eine Lebenslage ohne die Bildschirme auf, damit sich die
    ## Merkmalsvarianten in den Szenen prüfen lassen.

    def probe_lebenslage(herkunft_kennung, pfad, zusatzmerkmal=None):
        global aktueller_pfad
        person_erzeugen(herkunft_kennung, "m" if pfad == "front" else "w", 30)
        if zusatzmerkmal:
            merkmal_setzen(zusatzmerkmal)
        aktueller_pfad = pfad
        lebenslage.pfad = pfad
        if pfad == "front":
            lebenslage.musterung = "kv"
            dienststellung_setzen()
        elif pfad == "etappe":
            lebenslage.stand = gebeugt("Etappenlazarett", "Etappenlazarett")
        elif zusatzmerkmal in ERWERB_INDEX:
            lebenslage.stand = ERWERB_INDEX[zusatzmerkmal].bezeichnung.get(lebenslage.geschlecht, "")

    ## Anzeigetexte für die Kopfleiste und die Auswertung #####################

    def person_name():
        if lebenslage is None:
            return ""
        return lebenslage.name()

    def person_stand():
        if lebenslage is None:
            return ""
        return lebenslage.stand

    def person_kurz():
        if lebenslage is None:
            return ""
        return lebenslage.name() + ", " + str(lebenslage.alter) + " Jahre"


################################################################################
## 4. Bestand: Herkunft
################################################################################
##
## Vier Milieus. Sie entscheiden über Startwerte, über die Aussichten bei
## der Musterung und darüber, welche Erwerbslagen offenstehen. Namen und
## Berufe werden gezogen; sie sind Anzeige und niemals Bedingung.

init python:

    HERKUENFTE = [

        Herkunft(
            "arbeiterschaft", "Arbeiterschaft",
            "Mietshaus, vierter Hof, zwei Zimmer",
            "Der Lohn kommt am Freitag und ist am Mittwoch verbraucht. Im Haus wohnen vierzehn Parteien, man kennt sich und hilft sich aus. Die Polizei weiß genau, welche Straßen sie im Auge behält.",
            "Wenig Vorrat, viele Nachbarn, ein wachsames Revier.",
            werte={"versorgung": -1, "rueckhalt": 1, "aufmerksamkeit": 1},
            berufe={
                "m": ["Dreher in der Maschinenfabrik", "Former in der Gießerei",
                      "Bauhilfsarbeiter", "Schlosser"],
                "w": ["Näherin in der Konfektion", "Wäscherin",
                      "Arbeiterin in der Zigarettenfabrik", "Dienstmädchen"],
            },
            namen={
                "m": ["Otto", "Wilhelm", "Fritz", "Emil", "Hermann", "Paul", "August"],
                "w": ["Martha", "Frieda", "Anna", "Else", "Minna", "Hedwig", "Emma"],
            },
            familien=["Müller", "Krause", "Lehmann", "Schulz", "Neumann", "Wenzel", "Pietsch"]
        ),

        Herkunft(
            "buergertum", "Bürgertum",
            "Beamten- und Kaufmannshaushalt, vier Zimmer",
            "Ein eigenes Zimmer, ein Konto und eine Stellung mit Ansehen. Über Geld spricht man leise und über das Vaterland laut. Wer hier auffällt, verliert mehr als nur den guten Ruf.",
            "Rücklagen und Ansehen, dafür Abstand zu den anderen.",
            werte={"versorgung": 1, "aufmerksamkeit": -1},
            berufe={
                "m": ["Kaufmannsgehilfe", "Volksschullehrer", "Student der Rechte",
                      "Bankbeamter"],
                "w": ["Töchterschülerin", "Kontoristin", "Lehrerin",
                      "Tochter aus dem Haus"],
            },
            namen={
                "m": ["Heinrich", "Ernst", "Walter", "Richard", "Gustav", "Rudolf"],
                "w": ["Elisabeth", "Charlotte", "Marie", "Helene", "Käthe", "Dorothea"],
            },
            familien=["Brandt", "Grunewald", "Hartmann", "Reinhold", "Sommerfeld", "Keßler"]
        ),

        Herkunft(
            "landbevoelkerung", "Landbevölkerung",
            "Hof am Dorfrand, sechs Hektar",
            "Im Keller liegen Kartoffeln, im Stall stehen zwei Kühe. Dafür beginnt der Tag um vier, und liegen bleibt, wofür die Hände fehlen. Bis zur Kreisstadt sind es zwei Stunden zu Fuß.",
            "Mehr auf dem Tisch, weniger Schlaf, wenig Behörde.",
            werte={"versorgung": 2, "belastung": 1, "aufmerksamkeit": -1},
            berufe={
                "m": ["Bauernsohn auf dem elterlichen Hof", "Knecht auf dem Gutshof",
                      "Stellmacher", "Fuhrmann"],
                "w": ["Bauerntochter", "Magd auf dem Gutshof",
                      "Bäuerin auf dem eigenen Hof", "Melkerin"],
            },
            namen={
                "m": ["Johann", "Georg", "Jakob", "Andreas", "Peter", "Christian"],
                "w": ["Katharina", "Barbara", "Margarete", "Rosa", "Maria", "Klara"],
            },
            familien=["Bauer", "Kern", "Ackermann", "Rieger", "Stadler", "Wieland"]
        ),

        Herkunft(
            "adel", "Adel",
            "Gutshaus, Pachtland, ein Name mit von",
            "Der Keller ist voll, und der Landrat kommt zum Essen. Von diesem Haus wird erwartet, dass es vorangeht, wenn der Krieg beginnt. Im Dorf grüßt man zuerst und redet hinterher.",
            "Vorräte und Verbindungen, dafür Erwartungen und Abstand.",
            werte={"versorgung": 2, "belastung": -1, "aufmerksamkeit": -2, "rueckhalt": -1},
            berufe={
                "m": ["Erbe des Guts", "Fahnenjunker außer Dienst",
                      "Student der Forstwissenschaft", "Referendar"],
                "w": ["Tochter des Hauses", "Stiftsdame",
                      "Vorsitzende des Frauenvereins", "Gutsherrin"],
            },
            namen={
                "m": ["Botho", "Curt", "Detlev", "Friedrich-Wilhelm", "Hans-Joachim"],
                "w": ["Adelheid", "Irmgard", "Viktoria", "Sophie-Charlotte", "Elisabeth"],
            },
            familien=["von Stetten", "von Thal", "von Rodenberg", "von Osterloh", "von Quernheim"]
        ),

    ]

    HERKUNFT_INDEX = {}
    for _eintrag in HERKUENFTE:
        HERKUNFT_INDEX[_eintrag.kennung] = _eintrag


################################################################################
## 5. Bestand: Erwerbslagen
################################################################################
##
## Wer nicht eingezogen wird, muss trotzdem entscheiden, wovon der Haushalt
## lebt. Diese Entscheidung ist der zivile Gegenpart zur Musterung. Sie
## bestimmt Merkmale und damit, welche Ereignisse später greifen.

init python:

    ERWERBSLAGEN = [

        Erwerb(
            "ruestung", "Rüstungsbetrieb",
            "Granatendreherei, zwölf Stunden Schicht",
            "Die Werke suchen Leute, weil die Männer fehlen. Es gibt Lohn, Schwerarbeiterzulage und eine Kantine. Der Sprengstoff färbt die Haut gelb, und der Vorarbeiter führt eine Liste über jeden.",
            "Mehr Geld und Essen, dafür Erschöpfung und Aufsicht.",
            bezeichnung={"m": "Granatendreher", "w": "Granatendreherin"},
            werte={"versorgung": 1, "belastung": 2, "aufmerksamkeit": 1},
            merkmale=["ruestung"],
            hinweis_fuer=["adel"]
        ),

        ## DIE EINZIGE ERWERBSLAGE MIT etappe_moeglich — und das hat eine
        ## Folge, die man leicht übersieht. Festgehalten in Paket 5,
        ## Schritt 1, Teil C.9, damit die nächste Suche nicht wieder bei
        ## null anfängt:
        ##
        ## In die Etappe führen zwei Wege, und sie tragen NICHT dasselbe
        ## Merkmal mit sich.
        ##
        ##   1. Musterung mit dem Grad g.v. (pfad_aus_musterung).
        ##      Soldat im Etappendienst. KEIN Merkmal lazarett.
        ##   2. Erwerbswahl Lazarettdienst, dann einstieg_etappe.
        ##      Weil etappe_moeglich AUSSCHLIESSLICH hier gesetzt ist und
        ##      diese Lage das gleichnamige Merkmal vergibt, hat JEDE
        ##      Person, die so in die Etappe kommt, lazarett zwingend.
        ##
        ## Die Etappe ist damit der einzige Pfad, dessen Bevölkerung sich
        ## in zwei Hälften teilt. Wer ein gebundenes Ereignis für sie
        ## schreibt, entscheidet mit braucht_eines, welche Hälfte es
        ## bekommt - lazarett_1918_grippestation zum Beispiel die zweite.
        ##
        ## ABSICHTLICH NICHT GEÄNDERT: Der g.v. gemusterte Soldat bekommt
        ## lazarett nicht nachträglich, auch nicht über ein
        ## Etappenereignis. Das Merkmal gehört zur Gruppe "erwerb", heißt
        ## im Register "Im Lazarettdienst" und trägt einen Nachklang über
        ## Verbände und Prothesen. Wer es einem Nachschubsoldaten gäbe,
        ## ließe den Lebenslauf einen Beruf behaupten, den er nie hatte.
        ## Ein Ereignis darf eine TAT vergeben, keine Herkunft.
        Erwerb(
            "lazarett", "Lazarettdienst",
            "Reservelazarett in der Stadt",
            "Verbände auswaschen, Eimer tragen, Nachtwachen halten. Du erfährst schnell, was in keiner Zeitung steht, und du bist unter Menschen, die dasselbe sehen wie du.",
            "Nähe zu anderen, dafür Bilder, die bleiben.",
            bezeichnung={"m": "Lazarettgehilfe", "w": "Lazarettschwester"},
            werte={"versorgung": -1, "belastung": 1, "rueckhalt": 1},
            merkmale=["lazarett"],
            etappe_moeglich=True
        ),

        Erwerb(
            "landwirtschaft", "Hof und Feld",
            "Die Arbeit bleibt, die Männer nicht",
            "Zwei Kühe, sechs Hektar und niemand, der den Pflug führt. Was hier wächst, ist erst einmal da. Wie viel davon du behalten darfst, entscheidet ab jetzt eine Verordnung.",
            "Volle Vorratskammer, dafür Arbeit ohne Ende.",
            bezeichnung={"m": "Landwirt", "w": "Landwirtin"},
            werte={"versorgung": 1, "belastung": 2, "aufmerksamkeit": -1},
            merkmale=["landwirtschaft"],
            braucht_herkunft=["landbevoelkerung", "adel"]
        ),

        Erwerb(
            "verwaltung", "Kontor und Amtsstube",
            "Schreibtisch, Listen, Stempel",
            "Meldeämter, Kriegsgesellschaften und Betriebe brauchen Leute, die sauber schreiben können. Die Arbeit ist ruhig, warm und schlechter bezahlt, als sie aussieht.",
            "Ruhe und Unauffälligkeit, dafür wenig Nähe.",
            bezeichnung={"m": "Kontorist", "w": "Kontoristin"},
            werte={"belastung": -1, "aufmerksamkeit": -1, "rueckhalt": -1},
            merkmale=["verwaltung"],
            braucht_herkunft=["buergertum", "adel", "arbeiterschaft"]
        ),

        Erwerb(
            "haushalt", "Haushalt und Heimarbeit",
            "Karten, Schlange, Nähmaschine",
            "Die Wohnung, die Lebensmittelkarten und die Reihe vor dem Laden. Dazu Näharbeit im Akkord, wenn die Kinder schlafen. Bezahlt wird davon nur die Näharbeit.",
            "Du hältst den Haushalt zusammen und zahlst dafür mit Schlaf.",
            bezeichnung={"m": "Haushalt, Heimarbeit", "w": "Haushalt, Heimarbeit"},
            werte={"versorgung": -1, "belastung": 1, "rueckhalt": 1},
            merkmale=["haushalt"],
            nur_geschlecht="w",
            verbietet_merkmal=["uk"]
        ),

        Erwerb(
            "wohlfahrt", "Kriegsfürsorge",
            "Sammlungen, Suppenküche, Vereinslazarett",
            "Wollsachen sammeln, Listen führen, bei Verwundetentransporten zufassen. Es bringt kein Geld und viel Ansehen, und man sieht dich dabei.",
            "Ansehen und Verbindungen, dafür lange Tage ohne Lohn.",
            bezeichnung={"m": "Kriegsfürsorge", "w": "Kriegsfürsorge"},
            werte={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": 1},
            merkmale=["wohlfahrt"],
            braucht_herkunft=["adel", "buergertum"],
            nur_geschlecht="w",
            verbietet_merkmal=["uk"]
        ),

    ]

    ERWERB_INDEX = {}
    for _eintrag in ERWERBSLAGEN:
        ERWERB_INDEX[_eintrag.kennung] = _eintrag


################################################################################
## 6. Ereignisse dieses Pakets
################################################################################
##
## Diese vier Ereignisse gehören zum Einstieg und werden ausschließlich
## direkt aufgerufen. Sie tragen nur_kette=True und können deshalb niemals
## in die zufällige Ziehung geraten.
##
## init 1 läuft nach dem init python Block von script.rpy. Erst dort
## bestehen EREIGNISSE und EREIGNIS_INDEX.

init 1 python:

    EREIGNISSE_PAKET2 = [

        Ereignis(
            "einstieg_meldung", [], "beide",
            "Du stehst seit zwei Stunden an, und die Reihe reicht bis auf die "
            "Straße. Über dem Platz steht die Sonne senkrecht, und niemand "
            "hat Schatten. „Der Nächste!“, ruft einer durch die offene Tür. "
            "Wer sich freiwillig meldet, wird noch heute untersucht. Die "
            "anderen bekommen die Karte, sobald ihr Jahrgang an der Reihe ist.",
            [
                Option(
                    "Sich freiwillig melden",
                    "Du stellst dich in die Reihe, bevor der Befehl kommt.",
                    "Die Kommission arbeitet schnell und streng, und von zehn "
                    "Freiwilligen wird nicht jeder genommen. Ein Schreiber "
                    "trägt deinen Namen in eine Liste ein. Noch am selben "
                    "Nachmittag stehst du in Unterhosen vor dem Arzt.",
                    aenderungen={"belastung": -1, "rueckhalt": 1},
                    merkmale=["kriegsfreiwillig"]
                ),
                Option(
                    "Den Einberufungsbefehl abwarten",
                    "Du gehst nach Hause. So sieht es das Gesetz vor, und so machen es die meisten.",
                    "Im Herbst liegt die Karte im Kasten. Ort, Tag und Stunde "
                    "stehen darauf, dazu die Aufforderung zur Musterung. Es "
                    "ist der Weg der überwiegenden Mehrheit, und niemand hat "
                    "dir daraus einen Vorwurf gemacht.",
                    merkmale=["einberufen"]
                ),
            ],
            ort="Kreisstadt", kern=True, nur_kette=True,
            quelle={
                "kurz": "Kriegsfreiwillige und der Weg über den Jahrgang",
                "voll": "Kriegsfreiwillige im August 1914; Deutsches Historisches "
                        "Museum, LeMO, Kriegsbeginn",
                "art": "darstellung",
                ## GEKÜRZT IN PAKET 6, SCHRITT 2. Der erste Satz hatte 29
                ## Wörter und war der längste im ganzen Bestand. Was
                ## herausfällt, steht in vertiefung und geht damit nicht
                ## verloren (Entscheidung 8).
                "einordnung": "Im August 1914 meldeten sich weit mehr Männer, "
                              "als die Kommissionen nehmen konnten. Wie "
                              "begeistert sie wirklich waren, ist bis heute "
                              "umstritten.",
                "vertiefung": "Die große Mehrheit ging trotzdem den regulären "
                              "Weg über den Einberufungsbefehl. Auf den Befehl "
                              "zu warten war der Normalfall und kein Zeichen "
                              "von Unwillen.",
            }
        ),

        Ereignis(
            "einstieg_offizier", [], "beide",
            "In der Schreibstube riecht es nach Bohnerwachs und nassem "
            "Tuch. Ein Feldwebel geht die Liste durch und fragt nach dem "
            "Schulabschluss. „Wer einjährig-freiwillig dienen darf, tritt "
            "vor“, sagt er. Gemeint ist der verkürzte Dienst für die mit "
            "höherer Schulbildung; Uniform und Stiefel bezahlt man selbst.",
            [
                Option(
                    "Sich als Aspirant melden",
                    "Die Familie streckt das Geld für die Ausrüstung vor.",
                    "Du bekommst ein eigenes Quartier und besseres Essen als "
                    "die anderen. Der Schneider nimmt Maß, und die Rechnung "
                    "geht nach Hause. Erwartet wird, dass du im Angriff als "
                    "Erster über die Brustwehr steigst.",
                    aenderungen={"versorgung": 2, "belastung": 1, "aufmerksamkeit": -1, "rueckhalt": -1},
                    merkmale=["offizier"]
                ),
                Option(
                    "Als Mannschaft einrücken",
                    "Du sagst nichts und stellst dich in die Reihe der anderen.",
                    "Du wirst Musketier in der zweiten Kompanie. Niemand "
                    "fragt, was dein Vater macht. Niemand erwartet, dass du "
                    "vorangehst.",
                    aenderungen={"rueckhalt": 1}
                ),
            ],
            ort="Ersatztruppenteil", kern=True, nur_kette=True,
            quelle={
                "kurz": "Der Einjährig-Freiwillige und die Offizierslaufbahn",
                "voll": QUELLE_FEHLT,
                "art": "gesetz",
                ## GEKÜRZT IN PAKET 6, SCHRITT 2. 22 Wörter im ersten Satz.
                "einordnung": "Der einjährig-freiwillige Dienst setzte einen "
                              "höheren Schulabschluss voraus. Ausrüstung und "
                              "Uniform bezahlte der Bewerber selbst.",
                "vertiefung": "Damit stand die Offizierslaufbahn faktisch nur "
                              "denen offen, deren Familie beides aufbringen "
                              "konnte. Sicher war der Weg zum Offizier "
                              "deshalb noch lange nicht.",
            }
        ),

        ## WIEDER ERREICHBAR SEIT PAKET 5, SCHRITT 1, TEIL C ##################
        ##
        ## Von Paket 2, Schritt 1 bis hierher war dies das einzige Stück
        ## Inhalt im ganzen Bestand, das niemand mehr zu sehen bekam.
        ## Gerufen wird es ausschließlich aus label lebenslage_zivil, und
        ## zwar in dem Zweig, der an ETAPPE_FREIGESCHALTET hängt.
        ##
        ## Entfernt war der Aufruf NIE - nur gesperrt. Mit dem Schalter
        ## ist er von selbst zurückgekommen; es musste nichts
        ## wiederhergestellt werden. (Der Auftrag ging davon aus, der
        ## Aufruf sei herausgenommen worden; das war er nicht.)
        ##
        ## Nachgewiesen ist es, nicht angenommen: Über 2000
        ## Etappendurchgänge je Verlauf zieht probe_alles.py es wieder,
        ## und es steht nicht mehr in der Liste "Nie gezogen".
        ##
        ## Der Hinweis von damals bleibt trotzdem stehen, weil er weiter
        ## gilt: Wer hier aufräumt, löscht das falsche Stück. Die Probe
        ## kann einen solchen Fehler nicht melden - nur_kette-Ereignisse
        ## zählen in keiner Bestandstafel mit, und "nie gezogen" ist bei
        ## ihnen der Normalfall.
        Ereignis(
            "einstieg_etappe", [], "beide",
            "Am schwarzen Brett hängt ein Aufruf, und das Papier ist noch "
            "feucht vom Leim. Für ein Etappenlazarett in Nordfrankreich "
            "werden Kräfte gesucht. Der Zug fährt in vierzehn Tagen. „Da "
            "kommst du wenigstens raus“, sagt die Oberin im Vorbeigehen.",
            [
                ## ACHTUNG: "Sich melden" ist ein Schluessel in
                ## DOMINANZ_NACHTRAG (kapitel.rpy). Wer den Titel aendert,
                ## schaltet den Nachtrag ab - siehe Entscheidung 16.
                Option(
                    "Sich melden",
                    "Ein Formular, eine Unterschrift, ein Gestellungsbefehl.",
                    "Vierzehn Tage später steigst du in einen Zug ohne "
                    "Fahrplan. Die Verpflegung ist besser als daheim, und du "
                    "schämst dich dafür. Nachts hörst du zum ersten Mal, wie "
                    "weit Artillerie zu hören ist.",
                    aenderungen={"belastung": 1, "rueckhalt": -1}
                ),
                Option(
                    "In der Heimat bleiben",
                    "Das Reservelazarett braucht dich hier genauso.",
                    "Du bleibst, wo man dich kennt und beim Namen ruft. Der "
                    "Transport fährt ohne dich ab. Zwei Wochen später kommen "
                    "die ersten Briefe von unterwegs.",
                    aenderungen={"rueckhalt": 1}
                ),
            ],
            ort="Reservelazarett", kern=True, nur_kette=True,
            quelle={
                "kurz": "Schwestern in Etappenlazaretten hinter der Front",
                "voll": QUELLE_FEHLT,
                "art": "erinnerung",
                "einordnung": "Gesucht werden Berichte von Schwestern des Roten "
                              "Kreuzes oder der Frauenvereine über den Dienst in "
                              "Etappenlazaretten. Sie zeigen einzelne Wege "
                              "hinaus, nicht wie viele Frauen ihn nahmen.",
            }
        ),

        Ereignis(
            ## ZWEI BAHNSTEIGE, ZWEI BEDEUTUNGEN - Paket 6, Schritt 2.
            ##
            ## Diese Karte und die Szene einstieg_bahnsteig spielten beide
            ## am selben Ort, getrennt nur durch die Erwerbswahl. Zweimal
            ## derselbe Bahnsteig in den ersten fünf Minuten liess den
            ## Anfang eng wirken.
            ##
            ## Getrennt sind sie jetzt nicht über die Kennung, sondern über
            ## Ort und Blickrichtung: Hier ist die HALLE vor der Abfahrt -
            ## Lärm, Kreide auf den Wagen, Bewegung. Die Szene danach ist
            ## der leere Bahnsteig, wenn der Zug weg ist. Einmal Aufbruch,
            ## einmal Zurückbleiben.
            "einstieg_abschied", [], "beide",
            "In der Halle ist es so laut, dass man sich anschreien muss. "
            "Auf die Wagen hat jemand mit Kreide geschrieben, wohin es "
            "angeblich geht. Es riecht nach Kohle und nach zu vielen "
            "Menschen. Dann pfeift es, und der Zug setzt sich in Bewegung.",
            [
                Option(
                    "Bis zuletzt winken",
                    "Du bleibst stehen, bis der letzte Wagen aus der Halle ist.",
                    "Du hebst die Hand, bis der Arm wehtut. Die Halle wird "
                    "still, und die Kreideschrift fährt mit. Erst in der "
                    "Küche merkst du, dass deine Hände zittern.",
                    aenderungen={"belastung": 2, "rueckhalt": 1}
                ),
                Option(
                    "Vorher gehen",
                    "Du drehst dich um, bevor der Zug anfährt.",
                    "Draußen ist es plötzlich still, und die Luft ist kühl. "
                    "Du gehst zwei Straßen zu weit. Zu Hause bist du später, "
                    "als du müsstest.",
                    aenderungen={"belastung": 1}
                ),
            ],
            ort="Bahnhofshalle", kern=True, nur_kette=True,
            quelle={
                "kurz": "Abschied am Bahnhof, August 1914",
                "voll": QUELLE_FEHLT,
                "art": "bild",
                "einordnung": "Gesucht werden Fotografien von Truppentransporten "
                              "im August 1914, wie sie in Sammlungen zum "
                              "Kriegsbeginn liegen. Solche Bilder wurden oft für "
                              "die Presse gemacht und zeigen den Jubel deutlicher "
                              "als das Warten danach.",
            }
        ),

    ]

    for _vorlage in EREIGNISSE_PAKET2:
        EREIGNISSE.append(_vorlage)
        EREIGNIS_INDEX[_vorlage.kennung] = _vorlage

    ############################################################################
    ## Der Bahnsteig, nachdem der Zug weg ist
    ############################################################################
    ##
    ## SEIT PAKET 2, SCHRITT 2. Der Übergang in die zivile Erwerbswahl war
    ## bisher ein Bildschirmwechsel: Musterungsbogen, dann vier Karten mit
    ## der Frage, wovon ihr lebt. Zwischen beidem fehlte der Moment, in dem
    ## klar wird, WER fort ist - und genau daran hängen die drei neuen
    ## Merkmale.
    ##
    ## Die Szene ist absichtlich klein: sechs Zeilen, kein Jubel, keine
    ## Fahnen, keine Musik. Ein Bahnsteig nach der Abfahrt, Gepäck, eine
    ## Ansage. Die Varianten laufen über variante() und die drei
    ## Familienmerkmale; wer keines davon trägt, bekommt die Standardfassung.

    EINSTIEG_BAHNSTEIG = Szene(
        "einstieg_bahnsteig", "Der Bahnsteig",
        ort="Bahnhof",
        hintergrund="papier",
        zeilen=[

            erzaehlt(
                "Der Zug ist weg. Auf dem Bahnsteig liegen Papier, Bindfaden und "
                "eine Mütze. Zwei Frauen räumen die Bank frei, auf der sie "
                "gewartet haben."
            ),

            erzaehlt({
                "ehemann_im_feld":
                    "Sein Koffer stand seit Dienstag gepackt im Flur. Jetzt steht "
                    "dort nichts mehr, und der Flur ist breiter, als du dachtest.",
                "vater_im_feld":
                    "Er hat dir seine Uhr dagelassen. Im Feld gehe sie nur kaputt, "
                    "hat er gesagt. Sie ist zu groß für dein Handgelenk.",
                "bruder_im_feld":
                    "Ihr habt euch die Hand gegeben wie sonst auch. Er hat gesagt, "
                    "du sollst auf das Haus achten, und du hast genickt.",
                "standard":
                    "Du kennst niemanden in diesem Zug. Gekommen bist du trotzdem, "
                    "weil die halbe Straße gekommen ist.",
            }),

            auftritt("mitte", "amtsperson"),
            sagt("amtsperson",
                "Der Zug um vier Uhr zwölf fällt aus. Wer eine Fahrkarte hat, "
                "behält sie. Auskunft gibt der Schalter, aber nicht heute."
            ),

            ich({
                "ehemann_im_feld":
                    "Ich weiß nicht, wovon wir am Ersten die Miete zahlen.",
                "vater_im_feld":
                    "Ich muss morgen früh raus. Irgendjemand muss ja.",
                "bruder_im_feld":
                    "Man wird mich fragen, warum ich hier stehe und nicht dort.",
                "standard":
                    "Ich sollte nach Hause gehen und anfangen.",
            }),

            abgang("mitte"),

            erzaehlt(
                "An der Tafel wird eine Zahl gedreht. Danach ist es still, bis "
                "der nächste Zug einläuft."
            ),
        ]
    )

    ## Wie in merkbuch.rpy: Die Prüfung hält den Block wiederholbar.
    if EINSTIEG_BAHNSTEIG.kennung not in SZENEN_INDEX:
        SZENEN = SZENEN + [EINSTIEG_BAHNSTEIG]
        SZENEN_INDEX[EINSTIEG_BAHNSTEIG.kennung] = EINSTIEG_BAHNSTEIG


################################################################################
## 7. Zustandsvariablen
################################################################################

default lebenslage = None
default musterungsdaten = None
default erwerbswahl = None
default probe_werte = None


################################################################################
## 8. Stile
################################################################################

init offset = -1

style bogen_marke is default:
    size 17
    color FARBE_LINIE
    kerning 3.0

style bogen_kopf is default:
    font SCHRIFT_TITEL
    size 40
    bold True
    color FARBE_TINTE
    kerning 1.5

style bogen_feld is default:
    size 21
    color FARBE_TINTE_MATT
    kerning 1.0

style bogen_wert is default:
    font SCHRIFT_DOKUMENT
    size 25
    color FARBE_TINTE

style bogen_stempel is default:
    font SCHRIFT_TITEL
    size 52
    bold True
    color FARBE_AKZENT
    kerning 4.0
    text_align 0.5

style bogen_stempel_klein is default:
    size 18
    color FARBE_AKZENT
    kerning 1.6
    text_align 0.5

style bogen_vermerk is default:
    font SCHRIFT_DOKUMENT
    size 24
    color FARBE_AKZENT

style wahl_titel is default:
    font SCHRIFT_TITEL
    size 30
    bold True
    color FARBE_AKZENT

style wahl_zusatz is default:
    size 20
    italic True
    color FARBE_LINIE

style wahl_text is default:
    size 20
    color FARBE_TINTE_MATT
    line_spacing 5

style wahl_folge is default:
    size 19
    italic True
    color FARBE_TINTE
    line_spacing 3

## Seit Paket 2, Schritt 2: der erklärende Satz unter dem Stempel.
style wahl_hinweis is default:
    size 18
    color FARBE_AKZENT_MATT
    line_spacing 3

style feld_button is default:
    background rahmen(FARBE_PAPIER_HELL, FARBE_LINIE_FEIN, 2)
    hover_background rahmen("#fffdf8", FARBE_AKZENT, 2)
    selected_background rahmen(FARBE_PAPIER_DUNKEL, FARBE_AKZENT, 3)
    selected_hover_background rahmen(FARBE_PAPIER_DUNKEL, FARBE_AKZENT, 3)
    padding (24, 16)

style feld_marke is default:
    font SCHRIFT_TITEL
    size 26
    bold True
    color FARBE_TINTE

style feld_zusatz is default:
    size 19
    color FARBE_TINTE_MATT


################################################################################
## 9. Bildschirme
################################################################################

## Eine Auswahlkarte. Wird von der Herkunftswahl und von der Erwerbswahl
## benutzt, damit beide Schritte gleich aussehen.

screen wahlkarte(titel, zusatz, inhalt, folge, hinweis, aktion, breite=430, hoehe=560, hinweis_text=""):

    button:
        xysize (breite, hoehe)
        padding (24, 22)
        background rahmen_doppelt_schatten(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)
        hover_background rahmen_doppelt_schatten("#fffdf8", FARBE_AKZENT, FARBE_AKZENT, schattenfarbe="#15130f38")
        action aktion

        fixed:
            xysize (breite - 48, hoehe - 44)

            vbox:
                xsize breite - 48
                spacing 10

                text titel style "wahl_titel" xsize breite - 48

                add Solid(FARBE_AKZENT, xsize=56, ysize=3)

                text zusatz style "wahl_zusatz" xsize breite - 48

                null height 4

                text inhalt style "wahl_text" xsize breite - 48

            vbox:
                yalign 1.0
                xsize breite - 48
                spacing 8

                if hinweis:
                    frame:
                        padding (12, 5)
                        background rahmen_leer(FARBE_AKZENT, 2)
                        text hinweis.upper() style "karte_stempel"

                ## Seit Paket 2, Schritt 2: Der Stempel sagt, DASS etwas
                ## unüblich war, dieser Satz sagt, WARUM. Ohne ihn liest
                ## eine Achtklässlerin den Stempel als Verbot.
                if hinweis_text:
                    text hinweis_text style "wahl_hinweis" xsize breite - 48

                add Solid(FARBE_LINIE_FEIN, xsize=breite - 48, ysize=1)

                text folge style "wahl_folge" xsize breite - 48


## Ein Feld im Personalbogen. Auswahl mit einem Klick, kein Eingabefeld.

screen wahlfeld(beschriftung, zusatz, ausgewaehlt, aktion, breite=280):

    button:
        xsize breite
        style_prefix "feld"
        selected ausgewaehlt
        action aktion

        vbox:
            xsize breite - 48
            spacing 3
            text beschriftung style "feld_marke" xsize breite - 48
            text zusatz style "feld_zusatz" xsize breite - 48


################################################################################
## Schritt 1: Herkunft

screen herkunft_waehlen():

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xalign 0.5
        ypos 80
        xsize 1840
        spacing 14

        text "Sommer 1914" style "abschnitt_titel" size 46 xalign 0.5 xsize 1840

        add Solid(FARBE_AKZENT, xsize=220, ysize=3) xalign 0.5

        text "Wo dein Leben beginnt, entscheidest du. Wie es weitergeht, entscheiden andere. Wähle das Haus, in dem du im Juli 1914 wohnst." style "abschnitt_text" xalign 0.5 xsize 1200

        null height 26

        hbox:
            xalign 0.5
            spacing 40

            for eintrag in HERKUENFTE:
                use wahlkarte(
                    eintrag.titel,
                    eintrag.zusatz,
                    eintrag.text,
                    eintrag.folge,
                    None,
                    Return(eintrag.kennung),
                    430,
                    560
                )

        null height 18

        text "Auswahl mit einem Mausklick." style "tastenhinweis" xalign 0.5


################################################################################
## Schritt 2: Person

screen person_waehlen(herkunft_kennung):

    default gewaehltes_geschlecht = None
    default gewaehltes_alter = None

    $ quelle = herkunft_holen(herkunft_kennung)

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xalign 0.5
        ypos 90
        xsize 1400
        spacing 14

        text "Personalbogen" style "abschnitt_titel" size 46 xalign 0.5 xsize 1400

        add Solid(FARBE_AKZENT, xsize=220, ysize=3) xalign 0.5

        text quelle.titel + " - " + quelle.zusatz style "abschnitt_text" xalign 0.5 xsize 1200

        null height 30

        frame:
            xalign 0.5
            xsize 1400
            padding (60, 44)
            background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

            vbox:
                xsize 1280
                spacing 26

                text "Geschlecht" style "einstellung_label_text"

                text "Das Geschlecht entscheidet nicht darüber, wohin du kommst. Es entscheidet darüber, ob eine Kommission über dich urteilt oder ob du selbst über deine Arbeit entscheidest." style "wahl_text" size 21 xsize 1280

                hbox:
                    spacing 30
                    use wahlfeld("Männlich", "wird gemustert", gewaehltes_geschlecht == "m", SetScreenVariable("gewaehltes_geschlecht", "m"), 340)
                    use wahlfeld("Weiblich", "wird nicht gemustert", gewaehltes_geschlecht == "w", SetScreenVariable("gewaehltes_geschlecht", "w"), 340)

                add Solid(FARBE_LINIE_FEIN, xsize=1280, ysize=1)

                text "Jahrgang" style "einstellung_label_text"

                text "Das Geburtsjahr bestimmt, welcher Heeresklasse du angehörst und wie früh dein Jahrgang aufgerufen wird." style "wahl_text" size 21 xsize 1280

                ## Seit Paket 2, Schritt 2 stehen nur noch zwei Alter zur
                ## Wahl. Die Karten dürfen deshalb breiter werden, und
                ## unter der Heeresklasse steht, was das Alter für das
                ## Leben bedeutet - nicht nur, was es für die Musterung
                ## bedeutet.
                hbox:
                    spacing 30
                    for jahre in JAHRGANGSWAHL:
                        use wahlfeld(
                            str(jahre) + " Jahre",
                            JAHRGANG_MARKE.get(jahre, "") + "  -  Jahrgang "
                            + str(KAPITEL_JAHRE[0] - jahre) + ", " + altersgruppe(jahre)[1],
                            gewaehltes_alter == jahre,
                            SetScreenVariable("gewaehltes_alter", jahre),
                            620
                        )

        null height 30

        textbutton "Weiter":
            xalign 0.5
            style_prefix "weiter"
            sensitive (gewaehltes_geschlecht is not None) and (gewaehltes_alter is not None)
            action Return((gewaehltes_geschlecht, gewaehltes_alter))


################################################################################
## Schritt 3: Musterung

screen musterungsbogen(daten):

    $ zeitpunkt = "August 1914" if daten.get("strenge") == "august_1914" else "Herbst 1914"
    $ grad = daten.get("grad", "kv")
    $ vermerk = daten.get("vermerk")

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    hbox:
        xalign 0.5
        ypos 90
        spacing 40

        ## Der Bogen selbst
        frame:
            xsize 1060
            padding (48, 40)
            background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

            vbox:
                xsize 964
                spacing 12

                fixed:
                    xfill True
                    ysize 24
                    text "Königliches Bezirkskommando" style "bogen_marke" xalign 0.0 yalign 0.5
                    text zeitpunkt style "bogen_marke" xalign 1.0 yalign 0.5

                text "Musterungsverhandlung" style "bogen_kopf"

                add Solid(FARBE_TINTE, xsize=964, ysize=2)

                null height 4

                for beschriftung, wert in bogen_felder():

                    hbox:
                        xsize 964
                        spacing 20
                        text beschriftung style "bogen_feld" xsize 300 yalign 1.0
                        text wert style "bogen_wert" xsize 644 yalign 1.0

                    add Solid(FARBE_LINIE_FEIN, xsize=964, ysize=1)

                null height 10

                hbox:
                    xsize 964
                    spacing 30

                    vbox:
                        xsize 600
                        spacing 8
                        yalign 0.5

                        text "Entscheidung der Ersatzkommission" style "bogen_feld"

                        text MUSTERUNG_LANG.get(grad, "") style "bogen_wert" xsize 600

                        if vermerk:
                            text "Vermerk: " + VERMERK_LANG.get(vermerk, "") style "bogen_vermerk" xsize 600

                    frame:
                        xalign 1.0
                        xsize 300
                        padding (18, 14)
                        background rahmen_leer(FARBE_AKZENT, 4)

                        vbox:
                            xsize 260
                            spacing 2
                            text MUSTERUNG_KURZ.get(grad, "") style "bogen_stempel" xalign 0.5
                            if vermerk:
                                text VERMERK_KURZ.get(vermerk, "") style "bogen_stempel_klein" xalign 0.5
                            else:
                                text "eingetragen" style "bogen_stempel_klein" xalign 0.5

        ## Erläuterung für die Klasse
        vbox:
            xsize 700
            spacing 16

            frame:
                xsize 700
                padding (32, 28)
                background rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE, 2)

                vbox:
                    xsize 636
                    spacing 12

                    text "Was das bedeutet" style "hinweis_titel"

                    add Solid(FARBE_LINIE_FEIN, xsize=636, ysize=1)

                    text MUSTERUNG_KURZ.get(grad, "") + "  -  " + MUSTERUNG_LANG.get(grad, "") style "hinweis_stufe_name" xsize 636

                    text MUSTERUNG_ERKLAERUNG.get(grad, "") style "hinweis_text" xsize 636

                    if vermerk:

                        add Solid(FARBE_LINIE_FEIN, xsize=636, ysize=1)

                        text VERMERK_KURZ.get(vermerk, "") + "  -  " + VERMERK_LANG.get(vermerk, "") style "hinweis_stufe_name" xsize 636

                        text VERMERK_ERKLAERUNG.get(vermerk, "") style "hinweis_text" xsize 636

                    add Solid(FARBE_LINIE_FEIN, xsize=636, ysize=1)

                    text pfad_erlaeuterung(daten) style "hinweis_folge" xsize 636

            if persistent.analysemodus:

                frame:
                    xsize 700
                    padding (32, 24)
                    background rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE, 2)

                    vbox:
                        xsize 636
                        spacing 8

                        text "Analysemodus: Punkte dieses Wurfs" style "hinweis_zwischentitel"

                        for name, punkte in wurf_uebersicht():
                            hbox:
                                xsize 636
                                text name style "hinweis_stufe_text" xsize 420
                                text punkte style "analyse_wert" xsize 200

    textbutton "Weiter":
        xalign 0.5
        ypos 940
        style_prefix "weiter"
        action Return()


screen kein_musterungsbogen():

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    frame:
        align (0.5, 0.5)
        xsize 1180
        padding (80, 60)
        background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

        vbox:
            xsize 1020
            spacing 22

            text "Keine Musterung" style "abschnitt_titel" xalign 0.5 xsize 1020

            add Solid(FARBE_AKZENT, xsize=200, ysize=3) xalign 0.5

            text "Frauen wurden im Deutschen Reich nicht gemustert. Über dich urteilt keine Kommission, und niemand schickt dir einen Einberufungsbefehl.\n\nDafür entscheidest du selbst über eine Frage, die genauso schwer wiegt: wovon dein Haushalt in diesem Krieg lebt." style "abschnitt_text" xalign 0.5 xsize 1020

            add Solid(FARBE_LINIE_FEIN, xsize=1020, ysize=1)

            text "Auch dieser Weg kann in die Etappe führen. Das Rote Kreuz und die Frauenvereine schickten Schwestern bis in die Lazarette hinter der Front." style "hinweis_folge" xalign 0.5 xsize 1020

            null height 10

            textbutton "Weiter":
                xalign 0.5
                style_prefix "weiter"
                action Return()


################################################################################
## Schritt 4: Erwerbslage

screen erwerb_waehlen(auswahl):

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xalign 0.5
        ypos 80
        xsize 1840
        spacing 14

        text "Wovon ihr lebt" style "abschnitt_titel" size 46 xalign 0.5 xsize 1840

        add Solid(FARBE_AKZENT, xsize=220, ysize=3) xalign 0.5

        text erwerb_einleitung() style "abschnitt_text" xalign 0.5 xsize 1280

        null height 26

        hbox:
            xalign 0.5
            spacing 40

            for stelle, eintrag in enumerate(auswahl):
                use wahlkarte(
                    eintrag.titel,
                    eintrag.zusatz,
                    eintrag.text,
                    eintrag.folge,
                    erwerb_hinweis(eintrag),
                    Return(eintrag.kennung),
                    430,
                    600,
                    erwerb_hinweis_text(eintrag)
                )

        null height 18

        text "Auswahl mit einem Mausklick." style "tastenhinweis" xalign 0.5


################################################################################
## Schritt 5: Übersicht

screen lebenslage_uebersicht():

    add Solid(FARBE_PAPIER)

    use zustandskopf(ort_text())

    ## OFFENER PUNKT 91: Bei Schriftstufe "sehr gross" stand der Knopf
    ## "So beginnt es" zur Haelfte unter dem Bildrand - der Knopf, mit dem
    ## es weitergeht. Die feste 268 wird zu kopfhoehe() + 64, was bei
    ## normaler Schrift dieselbe Zahl ergibt, und der Block rollt, wenn er
    ## nicht mehr hineinpasst. Der Rollbalken versteckt sich, solange
    ## nichts zu rollen ist; bei normaler Schrift sieht man ihn nie.
    viewport:
        xalign 0.5
        ypos kopfhoehe() + 64
        xsize 1422
        ysize max(240, 1080 - (kopfhoehe() + 64) - 20)
        mousewheel True
        draggable True
        scrollbars "vertical"
        vscrollbar_unscrollable "hide"

        vbox:
            xalign 0.5
            xsize 1400
            spacing 16

            text "Deine Lage im Herbst 1914" style "abschnitt_titel" size 42 xalign 0.5 xsize 1400

            add Solid(FARBE_AKZENT, xsize=200, ysize=3) xalign 0.5

            null height 12

            frame:
                xalign 0.5
                xsize 1400
                padding (60, 40)
                background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

                vbox:
                    xsize 1280
                    spacing 10

                    for beschriftung, wert in uebersicht_felder():

                        hbox:
                            xsize 1280
                            spacing 20
                            text beschriftung style "bogen_feld" xsize 320 yalign 1.0
                            text wert style "bogen_wert" xsize 940 yalign 1.0

                        add Solid(FARBE_LINIE_FEIN, xsize=1280, ysize=1)

            null height 18

            text lage_schlusssatz() style "hinweis_folge" size 22 xalign 0.5 xsize 1200 text_align 0.5

            null height 14

            textbutton "So beginnt es":
                xalign 0.5
                style_prefix "weiter"
                action Return()

    use werthinweis()

init offset = 0


################################################################################
## 10. Sprachprüfung (Werkzeug für die Entwicklung)
################################################################################
##
## Prüft den gesamten Text- und Szenenbestand auf Begriffe, die es 1914 bis
## 1918 nicht gab oder die aus der NS-Zeit stammen. Das Werkzeug ist die
## technische Absicherung der historischen Vorgabe: Es wird mit jedem
## Inhaltspaket erneut aufgerufen und muss leer bleiben.

init 2 python:

    TABU_BEGRIFFE = [
        ("Wehrkraftzersetzung",
         "NS-Straftatbestand ab 1938. Für 1914 bis 1918: Landesverrat, Kriegsverrat, Majestätsbeleidigung oder Schutzhaft nach dem Belagerungszustandsgesetz."),
        ("Strafkompanie",
         "Kein Begriff des Kaiserheeres. Zutreffend wäre Feldstrafgefangenenabteilung. Das Warten auf die Einberufung führte ohnehin nirgendwohin."),
        ("Volksgemeinschaft",
         "NS-Leitbegriff. Für 1914 heißt es Burgfrieden."),
        ("Endsieg",
         "NS-Propagandabegriff."),
        ("Blitzkrieg",
         "Begriff des Zweiten Weltkriegs."),
        ("Landser",
         "Soldatensprache des Zweiten Weltkriegs. 1914 bis 1918: Musketier, Infanterist, Kamerad."),
        ("Untermensch",
         "NS-Begriff."),
        ("Lebensraum im Osten",
         "NS-Begriff."),
        ("Konzentrationslager",
         "Falsche Epoche."),
        ("Gestapo",
         "Falsche Epoche."),
        ("Führerbefehl",
         "Falsche Epoche. Im Kaiserheer: Divisionsbefehl, Regimentsbefehl, Tagesbefehl."),
    ]

    PRUEF_BEGRIFFE = [
        ("Heimatfront",
         "Erst im Zweiten Weltkrieg geläufig. Besser schlicht: die Heimat."),
        ("totaler Krieg",
         "Begriff der Zwischenkriegszeit. Als Unterrichtsfrage zulässig, im Spieltext nicht."),
        ("Weltkrieg",
         "Zeitgenossen sagten der große Krieg oder einfach der Krieg."),
        ("Trauma",
         "Fachbegriff des späten 20. Jahrhunderts. Zeitgenössisch: Kriegsneurose, Kriegszitterer, Nervenschock."),
        ("Drückeberger",
         "Zeitgenössisches Schimpfwort. Nur in wörtlicher Rede einer Figur zulässig, niemals in der Erzählstimme und niemals als Folge einer Wahl."),
        ("Nazi",
         "Falsche Epoche."),
    ]

    def texte_sammeln(gegenstand):
        """Sammelt alle Zeichenketten aus verschachtelten Text- und
        Variantenwörterbüchern ein."""
        gefunden = []
        if gegenstand is None:
            return gefunden
        if isinstance(gegenstand, str):
            gefunden.append(gegenstand)
        elif isinstance(gegenstand, dict):
            for wert in gegenstand.values():
                gefunden.extend(texte_sammeln(wert))
        elif isinstance(gegenstand, (list, tuple)):
            for wert in gegenstand:
                gefunden.extend(texte_sammeln(wert))
        return gefunden

    def ereignis_texte(vorlage):
        gefunden = texte_sammeln(vorlage.text)
        for auswahl in vorlage.optionen:
            gefunden.extend(texte_sammeln(auswahl.titel))
            gefunden.extend(texte_sammeln(auswahl.beschreibung))
            gefunden.extend(texte_sammeln(auswahl.ausgang))
            gefunden.extend(texte_sammeln(auswahl.hinweis))
            for variante_eintrag in auswahl.varianten:
                gefunden.extend(texte_sammeln(variante_eintrag.get("ausgang")))
        return gefunden

    def szenen_texte(szene):
        gefunden = []
        for zeile in szene.zeilen:
            gefunden.extend(texte_sammeln(zeile.text))
        return gefunden

    def sprachpruefung_durchfuehren():
        """Liefert eine Liste von Funden.

        Jeder Fund: (Stufe, Ort, Begriff, Begründung, Fundstelle)
        """
        funde = []

        bestand = []
        for vorlage in EREIGNISSE:
            bestand.append(("Ereignis " + vorlage.kennung, ereignis_texte(vorlage)))
        try:
            for szene in SZENEN:
                bestand.append(("Szene " + szene.kennung, szenen_texte(szene)))
        except NameError:
            pass

        for ort, texte in bestand:
            for satz in texte:
                klein = satz.lower()
                for begriff, begruendung in TABU_BEGRIFFE:
                    if begriff.lower() in klein:
                        funde.append(("Tabu", ort, begriff, begruendung, satz[:120]))
                for begriff, begruendung in PRUEF_BEGRIFFE:
                    if begriff.lower() in klein:
                        funde.append(("Prüfen", ort, begriff, begruendung, satz[:120]))

        return funde

    def musterungsprobe_rechnen(durchgaenge=400):
        """Würfelt die Musterung sehr oft und zählt aus, wohin sie führt.

        Damit lässt sich die Verteilung prüfen, ohne hundertmal zu spielen.
        """
        zeilen = []
        for quelle in HERKUENFTE:
            for alter in JAHRGANGSWAHL:
                zaehler = {"front": 0, "etappe": 0, "heimat": 0}
                grade = {"kv": 0, "gv": 0, "av": 0, "du": 0}
                vermerke = {"uk": 0, "zurueck": 0}
                for _ in range(durchgaenge):
                    wurf = musterung_wuerfeln(quelle.kennung, alter, "einberufung")
                    zaehler[pfad_aus_musterung(wurf)] += 1
                    grade[wurf["grad"]] += 1
                    if wurf["vermerk"]:
                        vermerke[wurf["vermerk"]] += 1
                zeilen.append({
                    "herkunft": quelle.titel,
                    "alter": alter,
                    "front": int(round(100.0 * zaehler["front"] / durchgaenge)),
                    "etappe": int(round(100.0 * zaehler["etappe"] / durchgaenge)),
                    "heimat": int(round(100.0 * zaehler["heimat"] / durchgaenge)),
                    "uk": int(round(100.0 * vermerke["uk"] / durchgaenge)),
                    "zurueck": int(round(100.0 * vermerke["zurueck"] / durchgaenge)),
                })
        return zeilen


init offset = -1

style probe_kopf is default:
    size 19
    color FARBE_LINIE
    kerning 1.6

style probe_zeile is default:
    size 21
    color FARBE_TINTE

style probe_fund is default:
    size 20
    color FARBE_TINTE
    line_spacing 3


screen sprachpruefung_anzeige(funde):

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xpos 120
        ypos 70
        xsize 1680
        spacing 14

        text "Sprachprüfung" style "abschnitt_titel" size 46 text_align 0.0 xalign 0.0

        add Solid(FARBE_AKZENT, xsize=220, ysize=3)

        if funde:
            text str(len(funde)) + " Fundstellen im Text- und Szenenbestand." style "abschnitt_text" text_align 0.0 xsize 1600
        else:
            text "Keine Fundstellen. Der gesamte Bestand ist frei von den geprüften Begriffen." style "abschnitt_text" text_align 0.0 xsize 1600

        null height 10

        viewport:
            xsize 1680
            ysize 760
            scrollbars "vertical"
            mousewheel True
            draggable True

            vbox:
                xsize 1620
                spacing 14

                for stufe, ort, begriff, begruendung, stelle in funde:

                    frame:
                        xsize 1620
                        padding (24, 18)
                        background rahmen(FARBE_PAPIER_HELL, FARBE_AKZENT if stufe == "Tabu" else FARBE_LINIE, 2)

                        vbox:
                            xsize 1572
                            spacing 6

                            hbox:
                                spacing 18
                                text stufe.upper() style "karte_stempel"
                                text begriff style "hinweis_stufe_name"
                                text ort style "probe_kopf" yalign 1.0

                            text begruendung style "probe_fund" xsize 1572

                            text stelle style "probe_kopf" xsize 1572

        null height 10

        textbutton "Zurück zum Hauptmenü":
            style_prefix "weiter"
            action MainMenu(confirm=False)


screen musterungsprobe_anzeige(zeilen):

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xpos 120
        ypos 60
        xsize 1680
        spacing 12

        text "Musterungsprobe" style "abschnitt_titel" size 44 text_align 0.0 xalign 0.0

        add Solid(FARBE_AKZENT, xsize=220, ysize=3)

        text "Je 400 Würfe pro Zeile, Zeitpunkt: reguläre Einberufung. Angaben in Prozent." style "abschnitt_text" size 22 text_align 0.0 xsize 1600

        null height 8

        hbox:
            xsize 1600
            spacing 0
            text "Herkunft" style "probe_kopf" xsize 380
            text "Alter" style "probe_kopf" xsize 140
            text "Front" style "probe_kopf" xsize 180
            text "Etappe" style "probe_kopf" xsize 180
            text "Heimat" style "probe_kopf" xsize 180
            text "davon u. k." style "probe_kopf" xsize 260
            text "zurückgestellt" style "probe_kopf" xsize 260

        add Solid(FARBE_LINIE, xsize=1600, ysize=2)

        for zeile in zeilen:

            hbox:
                xsize 1600
                spacing 0
                text zeile["herkunft"] style "probe_zeile" xsize 380
                text str(zeile["alter"]) style "probe_zeile" xsize 140
                text str(zeile["front"]) style "probe_zeile" xsize 180
                text str(zeile["etappe"]) style "probe_zeile" xsize 180
                text str(zeile["heimat"]) style "probe_zeile" xsize 180
                text str(zeile["uk"]) style "probe_zeile" xsize 260
                text str(zeile["zurueck"]) style "probe_zeile" xsize 260

            add Solid(FARBE_LINIE_FEIN, xsize=1600, ysize=1)

        null height 20

        textbutton "Zurück zum Hauptmenü":
            style_prefix "weiter"
            action MainMenu(confirm=False)

init offset = 0


################################################################################
## 11. Ablauf
################################################################################
##
## Aufruf aus script.rpy:
##
##     jump lebenslage_bestimmen
##
## Der Abschnitt endet mit einem Sprung in die hauptschleife.

label lebenslage_bestimmen:

    scene bg papier

    call screen herkunft_waehlen

    $ gewaehlte_herkunft = _return

    call screen person_waehlen(gewaehlte_herkunft)

    $ person_erzeugen(gewaehlte_herkunft, _return[0], _return[1])

    if ist_wehrpflichtig():
        jump lebenslage_musterung

    jump lebenslage_zivil


label lebenslage_musterung:

    ## Die Frage nach der freiwilligen Meldung. Beide Wege sind üblich.
    ## Wer wartet, verhält sich so, wie es das Gesetz vorsieht, und
    ## verliert dadurch nichts.
    call ereignis_spielen("einstieg_meldung")

    if hat_merkmal("kriegsfreiwillig"):
        $ musterungsdaten = musterung_eintragen("august_1914")
    else:
        $ musterungsdaten = musterung_eintragen("einberufung")

    call screen musterungsbogen(musterungsdaten)

    $ pfad_wechseln(pfad_aus_musterung(musterungsdaten))

    if aktueller_pfad == "heimat":
        jump lebenslage_zivil

    $ dienststellung_setzen()

    ## Die Offiziersfrage steht nur denen offen, die die Berechtigung
    ## zum einjährig-freiwilligen Dienst nachweisen können. Das war
    ## eine Frage des Schulabschlusses und damit des Elternhauses.
    if aktueller_pfad == "front" and offizierslaufbahn_offen():
        call ereignis_spielen("einstieg_offizier")
        $ dienststellung_setzen()

    jump lebenslage_abschluss


label lebenslage_zivil:

    if lebenslage.geschlecht == "w":
        call screen kein_musterungsbogen

    ## Wer fehlt in diesem Haushalt? ##########################################
    ##
    ## SEIT PAKET 2, SCHRITT 2. Vorher stand hier ein einziges Merkmal, das
    ## jede Frau und jeden zurückgestellten Mann traf. Es hieß nur, dass
    ## irgendjemand fort ist - und sagte damit über die Lage im Haus nichts.
    ## Jetzt entscheidet die Lebenslage, WER fort ist:
    ##
    ##   35 und weiblich             der Mann
    ##   18, gleich welchen Geschlechts   der Vater
    ##   35 und männlich, zurückgestellt oder unabkömmlich   der Bruder
    ##
    ## Die Reihenfolge ist wichtig: Es wird höchstens ein Merkmal gesetzt.
    ## Wer mit achtzehn zu Hause bleibt, wartet auf den Vater, gleich ob
    ## Junge oder Mädchen - das ist der Fall, der eine achte Klasse am
    ## unmittelbarsten angeht.
    ##
    ## Ein Mann von fünfunddreißig, der als arbeitsverwendungsfähig oder
    ## dauernd untauglich gemustert wurde, bekommt keines der drei. Das ist
    ## Absicht: Bei ihm ist niemand eingezogen worden, den das Haus vermisst.
    $ familienlage_setzen()

    ## Der Bahnsteig steht NACH dem Merkmal und VOR der Erwerbswahl. Nach
    ## dem Merkmal, weil die Szene sonst nicht wüsste, wen sie vermissen
    ## soll; vor der Wahl, weil die Frage "wovon lebt ihr jetzt" erst
    ## trägt, wenn man gesehen hat, wer nicht mehr mitverdient.
    call szene_spielen("einstieg_bahnsteig")

    $ erwerbswahl = erwerb_auswahl()

    call screen erwerb_waehlen(erwerbswahl)

    $ erwerb_uebernehmen(_return)

    ## Der Lazarettdienst ist der Weg, auf dem auch Frauen in die
    ## Etappe kamen. Über die Meldung entscheidet die Person selbst.
    if erwerb_holen(lebenslage.erwerb).etappe_moeglich and ETAPPE_FREIGESCHALTET:

        call ereignis_spielen("einstieg_etappe")

        if letzte_wahl == 0:
            $ pfad_wechseln("etappe")
            $ erwerb_bezeichnung_etappe()

    if aktueller_pfad == "heimat":
        call ereignis_spielen("einstieg_abschied")

    jump lebenslage_abschluss


label lebenslage_abschluss:

    ## PAKET 8, SCHRITT 2.6. Musik auf dem Heimatpfad (Entscheidung 24). Diese
    ## Marke wird von lebenslage_abschluss_mit_merkbuch (merkbuch.rpy)
    ## überschrieben und läuft nicht; dort steht dieselbe Zeile an derselben
    ## Stelle. Sie steht hier mit, damit die Fassungen nicht auseinanderlaufen.
    $ musik_setzen("heimat")

    call screen lebenslage_uebersicht

    ## Die Entscheidungen des Einstiegs stehen im Protokoll, zählen aber
    ## nicht gegen die Ereignisse, die für 1914 vorgesehen sind.
    $ ziehungen_im_kapitel = 0

    jump hauptschleife


################################################################################
## 12. Einstiege für die Werkzeuge
################################################################################

label sprachpruefung:

    scene bg papier

    $ pruefungsfunde = sprachpruefung_durchfuehren()

    call screen sprachpruefung_anzeige(pruefungsfunde)

    return


label musterungsprobe:

    scene bg papier

    $ probe_werte = musterungsprobe_rechnen(400)

    call screen musterungsprobe_anzeige(probe_werte)

    return

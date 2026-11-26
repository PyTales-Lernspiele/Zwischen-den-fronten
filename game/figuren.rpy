################################################################################
##
##  figuren.rpy
##
##  Paket 4: Nebenfiguren mit eigenem Schicksal
##
##  Diese Datei gibt den fünf Nebenfiguren aus dialoge.rpy ein eigenes Leben:
##  einen Zustand, der sich über die Jahre verändert, einen Briefwechsel, der
##  unregelmäßig zustande kommt, und einen Verbleib, der am Ende im Lebenslauf
##  steht.
##
##      1. Zustandsmodell   Status und Verbundenheit für fünf Figuren
##      2. Briefwechsel     Post, die unregelmäßig eintrifft
##      3. Schicksale       Ketten, die niemand ganz abwenden kann
##      4. Auswertung       ein Absatz im Lebenslauf von 1919
##
##  GRUNDSÄTZE, DIE IN DIESER DATEI GELTEN
##  - Steuerung ausschließlich mit der Maus. Keine key-Anweisungen.
##  - Ton nur am Kapitelwechsel. Seit Paket 8, Schritt 2.6 blendet
##    kapitelwechsel_mit_schicksal den Umgebungsklang aus (ton_still) und
##    fragt für die Jahreskarte nach Musik (musik_setzen) — die gibt es dort
##    nur, wenn MUSIK_EINGESCHALTET umgelegt ist, und auf front und etappe
##    nie. Kein Ton bewertet ein Schicksal.
##  - Varianten laufen über aktueller_pfad und merkmale, niemals über
##    Personennamen. Der Vorname der Spielfigur erscheint ausschließlich in
##    der Anrede eines Briefes und ist reine Anzeige.
##  - Keine Begriffe aus der NS-Zeit. Abschnitt 9 hängt die Brieftexte in die
##    Sprachprüfung ein, damit sie mitgeprüft werden.
##  - Kein Tod als Belohnung oder Strafe. Siehe den Kasten unten.
##
##  KEIN TOD ALS BELOHNUNG ODER STRAFE
##  Das ist die heikelste Stelle dieses Pakets, deshalb steht die Regel hier
##  ausgeschrieben. Ob eine Figur verwundet wird, erkrankt oder stirbt, hängt
##  ausschließlich am Jahr, am Pfad und am Würfel. Die Verbundenheit
##  verändert das NICHT. Sie entscheidet nur darüber,
##      - ob eine Figur dir überhaupt noch schreibt,
##      - wie persönlich sie schreibt,
##      - ob du erfährst, was mit ihr geschehen ist,
##      - und ob sie sich von dir entfremdet.
##  Wer gut spielt, verliert also niemanden weniger. Wer gut spielt, erfährt
##  mehr und steht am Ende weniger allein da. Genau das ist der historische
##  Befund: Zuwendung hat 1914 bis 1918 niemanden gerettet, aber sie hat
##  darüber entschieden, wie einsam die Überlebenden waren.
##
##  KEIN SCHICKSAL IST GANZ ABWENDBAR
##  Jede Schicksalsstufe hat eine Grundwahrscheinlichkeit über null. Es gibt
##  keine Wahl, keinen Wert und keinen Spielstil, der sie auf null drückt.
##  Umgekehrt gibt es auch keine Stufe mit hundert Prozent: Ein Durchgang
##  kann glimpflich verlaufen, ohne dass jemand etwas richtig gemacht hätte.
##
##  EINBINDUNG OHNE ÄNDERUNG AN script.rpy
##  Labels lassen sich in Ren'Py nicht überschreiben. Statt script.rpy zu
##  ändern, leitet Abschnitt 12 die beiden Labels hauptschleife und
##  kapitelwechsel über config.label_overrides auf eigene Fassungen um. Die
##  Fassungen sind Zeile für Zeile die alten, ergänzt um je einen Aufruf.
##  Wer script.rpy lieber direkt ändert, findet die beiden Zeilen dort
##  ausdrücklich markiert und kann Abschnitt 12 dann streichen.
##
################################################################################


################################################################################
## 1. Grundbegriffe
################################################################################
##
## init -8 läuft nach den Datentypen aus script.rpy (init -10) und vor dem
## Aufbau der Bestände. Hier stehen nur Konstanten, keine Zugriffe auf
## andere Dateien.

init -8 python:

    ## Die fünf Rollen aus dialoge.rpy, in der Reihenfolge, in der sie in
    ## Listen und im Lebenslauf erscheinen. Bewusst fest eingetragen: Wer
    ## eine Figur ergänzt, soll das an genau zwei Stellen tun müssen, in
    ## dialoge.rpy und hier.
    FIGUREN_REIHENFOLGE = ["naechste", "kind", "kundige", "amtsperson", "gegenseite"]

    ## Die sieben Zustände. Mehr gibt es nicht; alles andere wird über
    ## "bei dir" oder "fort" abgebildet.
    FIGUR_ZUSTAENDE = [
        "lebendig", "verwundet", "erkrankt",
        "vermisst", "verhaftet", "entfremdet", "gefallen",
    ]

    ## Ein Zustand endet den Lebensweg einer Figur. Danach wird für sie
    ## nichts mehr gewürfelt.
    ZUSTAENDE_ENDGUELTIG = ["gefallen"]

    ## Anzeige der Zustände. Die Front sagt gefallen, die Heimat sagt
    ## gestorben. Das ist kein Schönreden, sondern der zeitgenössische
    ## Sprachgebrauch: gefallen war ein militärischer Begriff.
    ## SEIT PAKET 5, SCHRITT 1, TEIL B mit eigener Etappenspalte. Sie ist
    ## nicht die Frontspalte mit anderen Wörtern, sondern folgt daraus, WIE
    ## man in der Etappe erfährt, wie es jemandem geht: nicht durch
    ## Danebenstehen und nicht durch einen Brief nach Hause, sondern durch
    ## eine Meldung, eine Liste, einen Zug, der an der Rampe hält. Deshalb
    ## steht dort, wo die Front "gefallen" sagt und die Heimat "gestorben",
    ## in der Etappe die Verlustliste.
    ZUSTAND_ANZEIGE = {
        "lebendig":   {"front": "lebt",           "etappe": "lebt",                  "heimat": "lebt"},
        "verwundet":  {"front": "verwundet",      "etappe": "im Lazarett",           "heimat": "verletzt"},
        "erkrankt":   {"front": "krank",          "etappe": "krank gemeldet",        "heimat": "krank"},
        "vermisst":   {"front": "vermisst",       "etappe": "vermisst gemeldet",     "heimat": "verschollen"},
        "verhaftet":  {"front": "in Haft",        "etappe": "in Haft",               "heimat": "in Haft"},
        "entfremdet": {"front": "fremd geworden", "etappe": "schreibt nicht mehr",   "heimat": "fremd geworden"},
        "gefallen":   {"front": "gefallen",       "etappe": "auf der Verlustliste",  "heimat": "gestorben"},
    }

    ## Farbstufe je Zustand, für den Balken in der Figurenleiste.
    ## 0 ist ruhig, 4 ist das Ende.
    ZUSTAND_STUFE = {
        "lebendig": 0,
        "verwundet": 2,
        "erkrankt": 2,
        "entfremdet": 2,
        "verhaftet": 3,
        "vermisst": 3,
        "gefallen": 4,
    }

    ## Verbundenheit von 0 bis 10. Startwerte stehen in Abschnitt 4.
    VERBUNDENHEIT_MINIMUM = 0
    VERBUNDENHEIT_MAXIMUM = 10

    ## Ab dieser Schwelle abwärts hört eine Figur auf zu schreiben.
    VERBUNDENHEIT_SCHWEIGEN = 2

    ## Von unten nach oben gelesen: der erste Eintrag, dessen Zahl der Wert
    ## erreicht, gilt.
    VERBUNDENHEIT_STUFEN = [
        (9, "eng", 0),
        (7, "vertraut", 1),
        (4, "lose", 2),
        (2, "kaum noch", 3),
        (0, "abgerissen", 4),
    ]

    ## Grundchance auf Post nach einem Ereignis, in Prozent. Sie sinkt in
    ## den späten Kriegsjahren: Die Feldpost blieb zwar bis zuletzt in
    ## Betrieb, aber die Wege wurden länger und die Schreiber weniger.
    POST_CHANCE = {
        1914: 30,
        1915: 35,
        1916: 30,
        1917: 24,
        1918: 20,
        1919: 30,
    }

    ## So viele Ereignisse müssen mindestens zwischen zwei Briefen liegen.
    POST_ABSTAND = 2

    ## So viele Ereignisse dürfen höchstens vergehen, bevor ein wartender
    ## Brief auf jeden Fall zugestellt wird. Ohne diese Bremse fühlt sich
    ## der Zufall für Dreizehnjährige wie ein Fehler an.
    POST_SPAETESTENS = 6

    ## Höchstzahl Briefe je Kapitel. Post soll ein Ereignis bleiben.
    POST_JE_JAHR = 3

    ## Beschriftungen der Postarten.
    POST_MARKE = {
        "feldpost":   "Feldpost",
        "heimatpost": "Post aus der Heimat",
        "amtlich":    "Amtliche Mitteilung",
        "nachricht":  "Eine Nachricht",
        "fundstueck": "Fundstück",
    }


################################################################################
## 2. Datentypen
################################################################################

init -8 python:

    class Schicksalsstufe(object):
        """Eine einzelne Wendung im Leben einer Nebenfigur.

        ab_jahr        frühestes Jahr, in dem gewürfelt wird
        bis_jahr       letztes Jahr, in dem gewürfelt wird, None heißt offen
        chance         Grundwahrscheinlichkeit in Prozent, je Jahreswechsel
        braucht        Liste zulässiger Zustände vor der Wendung
        braucht_fort   None egal, True nur wenn fort, False nur wenn bei dir
        zustand        neuer Zustand, None lässt ihn unverändert
        fort           True führt weg, False bringt zurück, None unverändert
        grund          kurze Ortsangabe, erscheint in der Figurenleiste
        verbundenheit  Veränderung der Verbundenheit
        wirkung        Veränderung der vier Werte der Spielfigur
        welt           "front", "heimat" oder None für beide
        meldung        {"front": [...], "heimat": [...]} konkrete Zeilen
        """

        def __init__(self, ab_jahr, chance, meldung, braucht=None,
                     braucht_fort=None, zustand=None, fort=None, grund=None,
                     verbundenheit=0, wirkung=None, welt=None, bis_jahr=None):
            self.ab_jahr = ab_jahr
            self.bis_jahr = bis_jahr
            self.chance = chance
            self.meldung = meldung
            self.braucht = braucht if braucht else ["lebendig"]
            self.braucht_fort = braucht_fort
            self.zustand = zustand
            self.fort = fort
            self.grund = grund
            self.verbundenheit = verbundenheit
            self.wirkung = wirkung if wirkung else {}
            self.welt = welt

    class Schicksal(object):
        """Eine Kette von Wendungen. Sie läuft Stufe für Stufe ab.

        Jede Kette gehört genau einer Figur. Mehrere Ketten derselben Figur
        laufen nebeneinander, greifen aber über braucht ineinander: Wer
        gefallen ist, erfüllt keine Bedingung mehr.
        """

        def __init__(self, kennung, figur, titel, stufen, welt=None):
            self.kennung = kennung
            self.figur = figur
            self.titel = titel
            self.stufen = stufen
            self.welt = welt

    class Briefantwort(object):
        """Eine von zwei Möglichkeiten, auf einen Brief zu reagieren.

        Es gibt nie eine richtige. Die eine kostet dich etwas und hält die
        Verbindung, die andere schont dich und lockert sie.
        """

        def __init__(self, titel, beschreibung, ausgang,
                     wirkung=None, verbundenheit=0):
            self.titel = titel
            self.beschreibung = beschreibung
            self.ausgang = ausgang
            self.wirkung = wirkung if wirkung else {}
            self.verbundenheit = verbundenheit

    class Brief(object):
        """Ein Brief, ein Bescheid oder ein Fundstück.

        figur          Kennung der Nebenfigur, von der die Post stammt
        welt           "front" oder "heimat": wo die SPIELFIGUR steht
        jahre          Liste der Jahre, in denen der Brief eintreffen kann
        art            Schlüssel aus POST_MARKE
        braucht        zulässige Zustände der Figur
        braucht_fort   True nur wenn die Figur fort ist
        anrede         True setzt automatisch "Liebe/Lieber Vorname," davor
        datum          Poststempel, reine Anzeige
        kopf           ein Satz darüber, wie der Brief zu dir kommt
        zeilen         die Zeilen des Briefes, wörtlich
        wirkung        Veränderung der vier Werte allein durch das Eintreffen
        antworten      zwei Briefantworten, oder leer
        """

        def __init__(self, kennung, figur, welt, jahre, art, datum, kopf,
                     zeilen, antworten=None, braucht=None, braucht_fort=True,
                     anrede=True, wirkung=None, gewicht=10,
                     verbundenheit_ab=0):
            self.kennung = kennung
            self.figur = figur
            self.welt = welt
            self.jahre = jahre
            self.art = art
            self.datum = datum
            self.kopf = kopf
            self.zeilen = zeilen
            self.antworten = antworten if antworten else []
            self.braucht = braucht if braucht else ["lebendig"]
            self.braucht_fort = braucht_fort
            self.anrede = anrede
            self.wirkung = wirkung if wirkung else {}
            self.gewicht = gewicht
            self.verbundenheit_ab = verbundenheit_ab


################################################################################
## 3. Zustand: lesen, schreiben, anzeigen
################################################################################
##
## init 3 läuft nach script.rpy (init -5), herkunft.rpy (init 1) und
## kapitel.rpy (init 2). Erst hier lassen sich Funktionen aus diesen Dateien
## zuverlässig erweitern.

init 3 python:

    ## Welt und Text ###########################################################
    ##
    ## Für die Post gibt es nur zwei Welten. Die Etappe zählt zur Front:
    ## Der Weg der Feldpost war derselbe, und die Absender waren dieselben.

    def briefwelt():
        """Die Welt, in der die Spielfigur Post empfängt.

        SEIT PAKET 5, SCHRITT 1, TEIL B gibt es drei davon. Vorher bildete
        diese Funktion die Etappe auf "front" ab. Für den POSTWEG war das
        richtig - die Feldpost lief für Etappe und Front über dieselben
        Sammelstellen -, aber es war zugleich der Grund, warum ein
        Etappenspieler Frontsätze las: Jede Fassung, die welttext() nicht
        genau traf, kam über diesen Umweg als Frontfassung zurück.

        Jetzt hat die Etappe ihre eigene Welt. Wo der Postweg wirklich
        derselbe ist, steht das ausdrücklich da - im Aufdruck des
        Umschlags, in der Kopfzeile des Briefes, im Zielort. Das ist
        dann eine Entscheidung und kein Ersatz, den niemand zählt.
        """
        if aktueller_pfad == "heimat":
            return "heimat"
        if aktueller_pfad == "etappe":
            return "etappe"
        return "front"

    def welt_erlaubt(gemeint):
        """Passt eine gemeinte Welt zu der, in der gerade gespielt wird?

        SEIT PAKET 5, SCHRITT 1, TEIL B. Ein Inhalt darf ab jetzt mehr
        als eine Welt nennen. Das ist der Weg, den der Auftrag als
        "begründete Zuordnung" zulässt: Ein Bescheid, der jeden
        Angehörigen des Feldheeres erreicht, gilt an der Front UND in
        der Etappe, ohne dass er zweimal geschrieben werden muss. Ein
        Brief dagegen, der vom Graben handelt, bleibt bei der Front.

        Verträgt drei Formen: None (keine Angabe, also passend), eine
        einzelne Welt als Zeichenkette - so stehen sie in älteren
        Spielständen - und eine Liste von Welten.
        """
        if gemeint is None:
            return True
        if isinstance(gemeint, str):
            return gemeint == briefwelt()
        return briefwelt() in gemeint

    def welttext(vorgaben):
        """Wählt aus einem Wörterbuch die Fassung für die eigene Welt.

        Zuerst wird der genaue Pfad gesucht, damit sich die Etappe bei
        Bedarf abweichend beschreiben lässt. Danach greift die Welt,
        zuletzt "standard". Jeder Griff unterhalb des genauen Pfades
        schreibt seit Paket 2, Schritt 1 ins variantenersatz_protokoll
        (dialoge.rpy).
        """
        if not isinstance(vorgaben, dict):
            return vorgaben
        if aktueller_pfad in vorgaben:
            ergebnis = vorgaben[aktueller_pfad]
        elif briefwelt() in vorgaben:
            ergebnis = vorgaben[briefwelt()]
            variantenersatz_merken("welttext", "ersatz", briefwelt(), ergebnis)
        elif "standard" in vorgaben:
            ergebnis = vorgaben["standard"]
            if variantenersatz_pfadschluessel(vorgaben):
                variantenersatz_merken("welttext", "standard", "standard", ergebnis)
        else:
            ergebnis = ""
            variantenersatz_merken("welttext", "leer", "(leer)", ergebnis)
        if isinstance(ergebnis, dict):
            ergebnis = jahrestext(ergebnis, aktuelles_jahr)
        return ergebnis

    def anrede_text():
        """Die erste Zeile eines persönlichen Briefes.

        Der Vorname ist reine Anzeige. Keine Bedingung im Spiel darf sich
        auf ihn stützen.
        """
        if lebenslage is None or not lebenslage.vorname:
            return gebeugt("Lieber Kamerad,", "Liebe Freundin,")
        return gebeugt("Lieber ", "Liebe ") + lebenslage.vorname + ","

    ## Anlegen und Zurücksetzen ################################################

    def figuren_anlegen():
        """Legt für alle fünf Rollen einen frischen Zustand an."""
        global figuren_zustand, post_offen, post_zaehler, post_letzter
        global post_gelesen, post_im_jahr, figuren_verlauf, schicksals_stand
        neu = {}
        for kennung in FIGUREN_REIHENFOLGE:
            start = FIGUREN_START.get(kennung, {})
            neu[kennung] = {
                "zustand": "lebendig",
                "bekannt": "lebendig",
                "fort": False,
                "grund": "",
                "verbundenheit": start.get("verbundenheit", 5),
                "stufen": [],
                "post_jahr": KAPITEL_JAHRE[0],
                "seit_jahr": KAPITEL_JAHRE[0],
            }
        figuren_zustand = neu
        ## Ohne diese Zeile liefen nach einem Neustart alle Ketten dort
        ## weiter, wo sie im vorigen Durchgang aufgehört haben.
        schicksals_stand = {}
        post_offen = []
        post_gelesen = []
        post_zaehler = 0
        post_letzter = None
        post_im_jahr = 0
        figuren_verlauf = []

    ## Der Aufruf beim Spielstart hängt sich an die vorhandene Funktion an,
    ## statt sie zu ersetzen. Dadurch bleibt script.rpy unberührt.
    zustand_zuruecksetzen_grundlage = zustand_zuruecksetzen

    def zustand_zuruecksetzen():
        zustand_zuruecksetzen_grundlage()
        figuren_anlegen()

    ## Lesen ###################################################################

    def figur_zustand(kennung):
        if not figuren_zustand:
            figuren_anlegen()
        return figuren_zustand.get(kennung)

    def figur_lebt(kennung):
        eintrag = figur_zustand(kennung)
        if eintrag is None:
            return False
        return eintrag["zustand"] not in ZUSTAENDE_ENDGUELTIG

    def figur_ist_fort(kennung):
        eintrag = figur_zustand(kennung)
        if eintrag is None:
            return False
        return bool(eintrag["fort"])

    def figur_verbundenheit(kennung):
        eintrag = figur_zustand(kennung)
        if eintrag is None:
            return 0
        return eintrag["verbundenheit"]

    def zustand_anzeige(zustand):
        """Wie der Zustand einer Nebenfigur in dieser Welt heißt.

        SEIT PAKET 5, SCHRITT 1, TEIL B über welttext() statt über einen
        eigenen Rückfall auf die Heimatfassung. Der alte Zweig war der
        dritte von dreien im Projekt und fiel als einziger zusammen mit
        figur_name() nach unten in die Heimat, während variante() und
        nach_welt() zur Front fielen. Jetzt gilt eine Regel, und eine
        fehlende Fassung wird gezählt statt ersetzt.

        Kennt die Tafel den Zustand gar nicht, bleibt es beim rohen
        Schlüssel. Das ist kein Ersatz für eine fehlende Fassung, sondern
        der Schutz davor, dass ein neuer Zustand die Leiste leer lässt.
        """
        satz = ZUSTAND_ANZEIGE.get(zustand)
        if not satz:
            return zustand
        return welttext(satz)

    def verbundenheit_anzeige(wert):
        for grenze, name, stufe in VERBUNDENHEIT_STUFEN:
            if wert >= grenze:
                return name, stufe
        return "abgerissen", 4

    def figur_zeile(kennung):
        """Eine Zeile für die Figurenleiste. Zeigt nur, was du wissen kannst."""
        eintrag = figur_zustand(kennung)
        if eintrag is None:
            return None
        name, stufe = verbundenheit_anzeige(eintrag["verbundenheit"])
        gezeigt = eintrag["zustand"] if not eintrag["fort"] else eintrag["bekannt"]
        ort = eintrag["grund"] if eintrag["fort"] else ""
        return {
            "kennung": kennung,
            "name": figur_name(kennung),
            "zustand": zustand_anzeige(gezeigt),
            "stufe": ZUSTAND_STUFE.get(gezeigt, 0),
            "ort": ort,
            "naehe": name,
            "naehe_stufe": stufe,
        }

    def figurenleiste():
        zeilen = []
        for kennung in FIGUREN_REIHENFOLGE:
            zeile = figur_zeile(kennung)
            if zeile is not None:
                zeilen.append(zeile)
        return zeilen

    ## Schreiben ###############################################################
    ##
    ## Alle Änderungen laufen über diese eine Funktion. Sie legt bewusst ein
    ## neues Wörterbuch an, damit Ren'Py die Veränderung sauber
    ## zurückrollen kann.

    def figur_setzen(kennung, zustand=None, fort=None, grund=None,
                     verbundenheit=None, bekannt=None, stufe=None):
        global figuren_zustand
        if kennung not in figuren_zustand:
            return
        alt = figuren_zustand[kennung]
        neu = dict(alt)
        if zustand is not None:
            neu["zustand"] = zustand
            neu["seit_jahr"] = aktuelles_jahr
        if fort is not None:
            neu["fort"] = bool(fort)
            if not fort:
                neu["grund"] = ""
        if grund is not None:
            neu["grund"] = grund
        if verbundenheit is not None:
            wert = neu["verbundenheit"] + verbundenheit
            wert = max(VERBUNDENHEIT_MINIMUM, min(VERBUNDENHEIT_MAXIMUM, wert))
            neu["verbundenheit"] = wert
        if bekannt is not None:
            neu["bekannt"] = bekannt
        if stufe is not None:
            neu["stufen"] = list(neu["stufen"]) + [stufe]
        gesamt = dict(figuren_zustand)
        gesamt[kennung] = neu
        figuren_zustand = gesamt

    def figur_post_vermerken(kennung):
        global figuren_zustand
        if kennung not in figuren_zustand:
            return
        neu = dict(figuren_zustand[kennung])
        neu["post_jahr"] = aktuelles_jahr
        gesamt = dict(figuren_zustand)
        gesamt[kennung] = neu
        figuren_zustand = gesamt


################################################################################
## 4. Bestand: Startwerte und Schicksalsketten
################################################################################
##
## init 1 läuft nach dem Aufbau der Nebenfiguren in dialoge.rpy (init 0).
##
## AUFBAU EINER FIGUR
## Jede der fünf Rollen hat drei Ketten:
##
##   Trennung   führt die Figur von dir weg und wieder zurück. Erst wenn
##              eine Figur fort ist, kann sie dir schreiben.
##   Schlag     der Einschnitt und die mögliche Erholung davon.
##   Ende       der Ausgang, der sich nicht mehr wenden lässt.
##
## Schlag und Ende laufen nebeneinander und schließen sich gegenseitig aus:
## Wer sich erholt hat, erfüllt die Bedingung des Endes nicht mehr, und wer
## am Ende angekommen ist, erholt sich nicht mehr. Welche der beiden Ketten
## in einem Jahr zuerst gewürfelt wird, entscheidet der Zufall. Dadurch gibt
## es keine stille Bevorzugung eines Ausgangs.
##
## chance, zustand, grund und meldung dürfen überall auch ein Wörterbuch
## mit den Schlüsseln "front" und "heimat" sein.

init 1 python:

    ############################################################################
    ## DER PERSÖNLICHE FADEN
    ############################################################################
    ##
    ## SEIT PAKET 3, SCHRITT 2 festgelegt und dokumentiert.
    ##
    ## Die fünf Rollen sind der einzige Faden, der durch alle sechs Kapitel
    ## läuft. Ereignisse wechseln, Jahre wechseln, der Pfad steht fest -
    ## aber wer neben einem steht, bleibt derselbe. Damit dieser Faden
    ## trägt, gelten ab jetzt zwei Zusagen:
    ##
    ## ERSTENS: Jede Figur hat GENAU EINEN Wendepunkt, an dem sich ihr
    ## Verhältnis zur Spielerin entscheidet, und ein Jahr, in dem er
    ## fällig wird. Er liegt jeweils in der ersten Stufe der Schlagkette;
    ## alles davor ist Trennung, alles danach ist Folge.
    ##
    ##   naechste     1916   Der Einschnitt. Vermisst nach dem Angriff,
    ##                       erkrankt in der Heimat. Ab hier ist offen,
    ##                       ob sie oder er zurückkommt.
    ##   kind         1918   Der Einschnitt. Aus dem Jüngsten der Gruppe
    ##                       ist ein Soldat geworden, aus dem Kind im
    ##                       Erdgeschoss ein Arbeiter.
    ##   kundige      1917   In der Akte. Wer alles weiß, sagt irgendwann
    ##                       zu viel; ab hier entscheidet sich, ob du dich
    ##                       zu ihr stellst.
    ##   amtsperson   1916   Er ist auch nur einer. Der Wendepunkt ist
    ##                       nicht sein Schicksal, sondern der Moment, in
    ##                       dem hinter der Akte ein Mensch sichtbar wird.
    ##   gegenseite   1917   Der Einschnitt. Die einzige Figur, mit der es
    ##                       keinen Briefwechsel gibt; ihr Wendepunkt ist
    ##                       der, an dem aus dem Gegenüber ein Mensch wird
    ##                       oder endgültig keiner.
    ##
    ## ZWEITENS: In JEDEM Kapitel taucht mindestens eine Nebenfigur auf -
    ## als Brief, als Schicksalsmeldung oder in einer Szene. Ein Kapitel
    ## ohne eine einzige Nebenfigur ist ein Kapitel ohne Faden.
    ##
    ## probe_alles.py misst beides. Gemeldet wird jedes Kapitel, das ohne
    ## Nebenfigur bleibt - heute sind das 1917 bis 1919, weil dort weder
    ## Ereignisse noch Post entstehen. Das ist der Auftrag an die
    ## Inhaltspakete, nicht an diese Datei.

    FIGUR_WENDEPUNKT = {
        "naechste":   {"jahr": 1916, "kette": "naechste_schlag"},
        "kind":       {"jahr": 1918, "kette": "kind_schlag"},
        "kundige":    {"jahr": 1917, "kette": "kundige_akte"},
        "amtsperson": {"jahr": 1916, "kette": "amt_selbst"},
        "gegenseite": {"jahr": 1917, "kette": "gegen_schlag"},
    }

    FIGUREN_START = {
        "naechste":   {"verbundenheit": 6},
        "kind":       {"verbundenheit": 5},
        "kundige":    {"verbundenheit": 5},
        "amtsperson": {"verbundenheit": 2},
        "gegenseite": {"verbundenheit": 3},
    }

    SCHICKSALE = [

        ########################################################################
        ## Der oder die Nächste
        ########################################################################

        Schicksal(
            "naechste_trennung", "naechste", "Getrennt",
            [
                Schicksalsstufe(
                    1915, 42, bis_jahr=1918,
                    braucht=["lebendig"], braucht_fort=False,
                    zustand={"front": "verwundet", "etappe": "lebendig",
                             "heimat": "lebendig"},
                    fort=True,
                    grund={"front": "im Lazarett", "etappe": "bei einem Marschbataillon",
                           "heimat": "im Werksheim"},
                    meldung={
                        "front": [
                            "Ein Sprengstück hat ihm den Unterarm aufgerissen.",
                            "Er geht auf eigenen Beinen zum Verbandplatz, das ist ein gutes Zeichen.",
                            "An der Biegung dreht er sich um und hebt die gesunde Hand.",
                            "Sein Platz neben dir bleibt zwei Tage leer. Dann liegt ein anderer darin.",
                        ],
                        ## Die Trennung der Etappe ist die Auskaemmung: Eine
                        ## Kommission sucht in den Schreibstuben nach Leuten,
                        ## die noch marschieren koennen. Wer bleibt, hat
                        ## nichts dafuer getan - und weiss das.
                        "etappe": [
                            "Eine Kommission sieht die Schreibstuben durch und sucht Leute, die noch marschieren können.",
                            "Sein Name steht am Abend auf der Liste, deiner nicht.",
                            "Er packt den Tornister und sagt, vier Kilometer weiter sei es auch nicht anders.",
                            "Am Gleis dreht er sich einmal um. Dann steht der Wagen zwischen euch.",
                        ],
                        "heimat": [
                            "Sie hat sich in einer Munitionsfabrik anwerben lassen, zwei Stunden mit der Bahn.",
                            "Der Lohn ist fast doppelt so hoch. Schlafen wird sie im Werksheim.",
                            "Am Morgen trägt sie zwei Körbe zur Haltestelle. Einen davon trägst du.",
                            "Im Treppenhaus ist es von diesem Tag an leiser.",
                        ],
                    }
                ),
                Schicksalsstufe(
                    1916, 40,
                    braucht=["lebendig", "verwundet"], braucht_fort=True,
                    zustand="lebendig", fort=False,
                    meldung={
                        "front": [
                            "Er steht wieder in der Reihe, als wäre er nie weg gewesen.",
                            "Der Arm bleibt steif. Zum Tragen reicht er, zum Schießen auch.",
                            "Er erzählt nichts vom Lazarett. Du fragst nicht nach.",
                        ],
                        "etappe": [
                            "Er kommt mit einem Transport zurück, weil die Schreibstube niemanden mehr hat.",
                            "Er sagt kein Wort über die vier Wochen dazwischen.",
                            "Beim Schreiben zittert die Hand, und die Zeilen laufen nach unten.",
                        ],
                        "heimat": [
                            "Das Werk hat die Fertigung umgestellt und die Hälfte der Frauen entlassen.",
                            "Sie steht mit ihren zwei Körben wieder vor der Haustür.",
                            "Ihre Hände sind gelb. Das kommt vom Pulver und geht nicht ab.",
                        ],
                    }
                ),
            ]
        ),

        Schicksal(
            "naechste_schlag", "naechste", "Der Einschnitt",
            [
                Schicksalsstufe(
                    1916, {"front": 26, "etappe": 24, "heimat": 22}, bis_jahr=1918,
                    braucht=["lebendig", "verwundet"],
                    zustand={"front": "vermisst", "etappe": "vermisst",
                             "heimat": "erkrankt"},
                    fort=True,
                    grund={"front": "vermisst seit dem Angriff",
                           "etappe": "seit dem Transport ohne Nachricht",
                           "heimat": "im Bett"},
                    meldung={
                        "front": [
                            "Nach dem Angriff wird abgezählt. Vier Namen bleiben ohne Antwort.",
                            "Seiner ist der zweite.",
                            "Der Feldwebel schreibt ein Wort dahinter: vermisst.",
                            "Vermisst heißt, dass es niemand weiß. Es heißt nicht, dass er tot ist.",
                        ],
                        ## In der Etappe erfaehrt man den Schlag nicht im
                        ## Gefecht, sondern auf Papier - und zwar auf dem
                        ## eigenen Tisch. Das ist der Unterschied, den
                        ## dieser Pfad traegt.
                        "etappe": [
                            "Der Transport, mit dem er gefahren ist, wird unterwegs beschossen.",
                            "Zwei Tage später kommt die Liste der Verluste über deinen Tisch.",
                            "Sein Name steht darauf, und dahinter steht kein Wort.",
                            "Du trägst ihn in die Abschrift ein, sauber, wie du es gelernt hast.",
                        ],
                        "heimat": [
                            "Sie fällt in der Schlange um, zwischen dem vierten und dem fünften Wartenden.",
                            "Zwei Frauen tragen sie in den Hausflur und setzen sie auf die Treppe.",
                            "Der Arzt sagt Blutarmut und schreibt Ruhe und Kräftigung auf den Zettel.",
                            "Auf dem Zettel steht Kräftigung. Auf der Karte steht, was es gibt.",
                        ],
                    }
                ),
                Schicksalsstufe(
                    1917, 44,
                    braucht=["vermisst", "erkrankt"], braucht_fort=True,
                    zustand="lebendig",
                    ## An der Front heißt Wiederauftauchen nicht Rückkehr:
                    ## Wer in Gefangenschaft ist, lebt und bleibt fort. In
                    ## der Heimat steht sie wieder in derselben Schlange.
                    fort={"front": True, "etappe": True, "heimat": False},
                    grund={"front": "in Gefangenschaft", "etappe": "in Gefangenschaft",
                           "heimat": ""},
                    verbundenheit=1,
                    meldung={
                        "front": [
                            "Eine Karte über das Rote Kreuz in Genf, sechs Zeilen, vorgedruckt.",
                            "Er ist in Gefangenschaft. Er ist gesund. Er darf zweimal im Monat schreiben.",
                            "Mehr steht nicht darauf, und mehr brauchst du heute nicht.",
                        ],
                        "etappe": [
                            "Eine Karte über das Rote Kreuz in Genf geht durch deine Prüfstelle.",
                            "Sechs vorgedruckte Zeilen: Er lebt, er ist gefangen, er darf schreiben.",
                            "Du legst sie in den Sack und nicht in die Akte.",
                        ],
                        "heimat": [
                            "Sie steht wieder auf. Erst bis zur Tür, dann bis zur Straße.",
                            "Nach drei Wochen ist sie wieder in der Schlange, zwei Plätze weiter hinten.",
                            "Sie sagt, es sei nichts gewesen. Ihr wisst beide, dass das nicht stimmt.",
                        ],
                    }
                ),
            ]
        ),

        Schicksal(
            "naechste_ende", "naechste", "Der Ausgang",
            [
                Schicksalsstufe(
                    1916, {"front": 24, "etappe": 20, "heimat": 15}, bis_jahr=1918,
                    braucht=["vermisst", "erkrankt"],
                    zustand="gefallen", fort=True,
                    grund={"front": "gefallen", "etappe": "gefallen",
                           "heimat": "gestorben"},
                    wirkung={"belastung": 1},
                    meldung={
                        "front": [
                            "Die Bestätigung kommt über die Kompanie, Monate später.",
                            "Gefunden bei der Räumung des Grabenstücks, erkannt an der Marke.",
                            "Auf dem Bogen ist alles vorgedruckt außer dem Namen und dem Datum.",
                            "Du liest das Datum und rechnest nach, was du an diesem Tag getan hast.",
                        ],
                        "etappe": [
                            "Die Bestätigung kommt mit der Verlustliste, Monate später.",
                            "Sein Name steht zwischen zwei anderen, in derselben Spalte wie immer.",
                            "Du schreibst die Liste ab und lässt die Zeile aus.",
                            "Am Abend trägst du sie nach, weil sie sonst jemand anderem auffällt.",
                        ],
                        "heimat": [
                            "Sie ist in der Nacht gestorben. Die Tür stand offen, damit man sie hört.",
                            "In der Sterbeurkunde steht Herzschwäche. Das steht bei vielen.",
                            "Am Grab stehen sieben Leute. Für mehr reicht die Zeit nicht, alle müssen arbeiten.",
                        ],
                    }
                ),
            ]
        ),

        ########################################################################
        ## Das Kind
        ########################################################################

        Schicksal(
            "kind_trennung", "kind", "Fortgeschickt",
            [
                Schicksalsstufe(
                    1915, 55, bis_jahr=1918,
                    braucht=["lebendig"], braucht_fort=False,
                    fort=True,
                    grund={"front": "bei der Bagagekolonne", "etappe": "auf der Strecke",
                           "heimat": "bei Verwandten auf dem Land"},
                    meldung={
                        "front": [
                            "Sie brauchen jemanden, der mit Pferden umgehen kann.",
                            "Der Jüngste hebt die Hand, bevor der Feldwebel den Satz zu Ende gesprochen hat.",
                            "Er kommt zur Bagage, vier Kilometer hinter der Stellung.",
                            "Alle sagen, er habe Glück gehabt. Er selbst sagt nichts.",
                        ],
                        "etappe": [
                            "Die Eisenbahn sucht Jungen, die auf den Wagen mitfahren und bremsen können.",
                            "Der Laufbursche meldet sich, bevor der Feldwebel den Satz zu Ende hat.",
                            "Er fährt jetzt mit den Zügen bis zum vordersten Bahnhof und wieder zurück.",
                            "Auf dem Bahnsteig winkt er, bis der Zug in der Kurve ist.",
                        ],
                        "heimat": [
                            "Die Mutter hat es sich vier Wochen überlegt und schickt das Kind aufs Land.",
                            "Dort gibt es eine Tante, eine Kuh und keine Karte für Milch.",
                            "Am Bahnsteig hält es den Karton mit beiden Armen fest und weint nicht.",
                            "Der Zug fährt ab. Erst danach weint es, sagt die Mutter später.",
                        ],
                    }
                ),
                Schicksalsstufe(
                    1917, 30,
                    braucht=["lebendig"], braucht_fort=True,
                    fort=False,
                    meldung={
                        "front": [
                            "Die Bagage wird aufgelöst, die Pferde gehen an die Artillerie.",
                            "Er steht wieder in der Stellung und ist einen Kopf größer als vor zwei Jahren.",
                            "Er redet schneller als früher und lacht an Stellen, an denen nichts zu lachen ist.",
                        ],
                        "etappe": [
                            "Die Züge fahren jetzt seltener, und die Bremser werden nicht mehr gebraucht.",
                            "Er steht wieder mit den Meldungen im Gang und ist einen Kopf größer.",
                            "Er redet schneller als früher und sieht dabei aus dem Fenster.",
                        ],
                        "heimat": [
                            "Auf dem Land ist auch nichts mehr übrig. Die Tante schreibt zwei Zeilen.",
                            "Das Kind kommt zurück, mit demselben Karton und ohne die Kuh.",
                            "Es ist dreizehn und geht seit dem Frühjahr in die Fabrik. Acht Stunden, Papierhülsen.",
                        ],
                    }
                ),
            ]
        ),

        Schicksal(
            "kind_schlag", "kind", "Der Einschnitt",
            [
                Schicksalsstufe(
                    1918, {"front": 34, "etappe": 36, "heimat": 38},
                    braucht=["lebendig"],
                    zustand="erkrankt",
                    meldung={
                        "front": [
                            "Es geht eine Grippe um. Zuerst trifft es die Jungen, das ist das Merkwürdige daran.",
                            "Er hustet, dann fiebert er, dann bekommt er die Luft nicht mehr richtig.",
                            "Der Sanitäter sagt, er habe an einem Tag elf davon gesehen.",
                        ],
                        "etappe": [
                            "Im Etappenlazarett liegen seit einer Woche mehr Kranke als Verwundete.",
                            "Der Laufbursche hustet, dann fiebert er, dann bringt ihn jemand hin.",
                            "Ein Arzt sagt, heute sei er der neunte aus dieser Baracke.",
                        ],
                        "heimat": [
                            "In der Fabrik fehlen an einem Montag neunzehn Leute. Es geht eine Grippe um.",
                            "Das Kind fiebert seit zwei Tagen und hustet trocken.",
                            "Die Lippen sind blau angelaufen. Der Arzt kommt erst am Abend.",
                        ],
                    }
                ),
                Schicksalsstufe(
                    1918, 50,
                    braucht=["erkrankt"],
                    zustand="lebendig", verbundenheit=1,
                    meldung={
                        "front": [
                            "Das Fieber fällt am fünften Tag. Er kann wieder aufstehen.",
                            "Er ist dünn wie ein Streichholz und schläft im Sitzen ein.",
                            "Zurück zur Truppe darf er erst in vier Wochen. Er beschwert sich darüber.",
                        ],
                        "etappe": [
                            "Das Fieber fällt am fünften Tag, und er fragt sofort nach den Meldungen.",
                            "Er ist dünn geworden und schläft im Stehen an der Wand ein.",
                            "Laufen darf er erst in drei Wochen wieder. Er hält sich nicht daran.",
                        ],
                        "heimat": [
                            "Das Fieber fällt in der Nacht zum Sonntag. Am Morgen will es Brot.",
                            "Es bekommt eine halbe Scheibe und isst sie in kleinen Stücken.",
                            "Zwei Wochen später geht es wieder in die Fabrik. Vorher wäre kein Lohn gekommen.",
                        ],
                    }
                ),
            ]
        ),

        Schicksal(
            "kind_ende", "kind", "Der Ausgang",
            [
                Schicksalsstufe(
                    1918, {"front": 26, "etappe": 25, "heimat": 24},
                    braucht=["erkrankt"],
                    zustand="gefallen", fort=True,
                    grund={"front": "gestorben", "etappe": "gestorben",
                           "heimat": "gestorben"},
                    wirkung={"belastung": 1},
                    meldung={
                        "front": [
                            "Er ist in der Nacht gestorben, an der Grippe, nicht im Gefecht.",
                            "Auf dem Bogen steht deshalb nicht gefallen, sondern gestorben im Felde.",
                            "Für die Angehörigen ist das ein Unterschied. Für ihn ist es keiner.",
                            "Er wäre im Herbst einundzwanzig geworden.",
                        ],
                        ## Denselben Bogen, den die Front vorgelesen bekommt,
                        ## fuellt die Etappe selbst aus. Kein Satz sagt, was
                        ## das mit einem macht.
                        "etappe": [
                            "Er ist in der Nacht gestorben, an der Grippe, nicht im Gefecht.",
                            "Auf dem Bogen steht nicht gefallen, sondern gestorben im Felde.",
                            "Du füllst ihn aus, weil du in dieser Woche die Listen führst.",
                            "Er wäre im Frühjahr achtzehn geworden.",
                        ],
                        "heimat": [
                            "Es ist am Dienstagmorgen gestorben. Die Lunge, sagt der Arzt.",
                            "Auf dem Friedhof sind in dieser Woche vier Kindergräber ausgehoben worden.",
                            "Die Mutter hat drei Tage frei bekommen und geht am zweiten wieder arbeiten.",
                        ],
                    }
                ),
            ]
        ),

        ########################################################################
        ## Die Kundige
        ########################################################################

        Schicksal(
            "kundige_trennung", "kundige", "Versetzt",
            [
                Schicksalsstufe(
                    1916, 40, bis_jahr=1918,
                    braucht=["lebendig"], braucht_fort=False,
                    fort=True,
                    grund={"front": "in der Etappe", "etappe": "in einem Lager weiter hinten",
                           "heimat": "bei der Tochter"},
                    meldung={
                        "front": [
                            "Der Älteste der Gruppe ist zweiundvierzig. Das steht jetzt in einer anderen Liste.",
                            "Er kommt zur Landwehr in die Etappe, Wachdienst an einem Bahnhof.",
                            "Er packt seine Sachen in vier Minuten. So lange hat er darauf gewartet.",
                            "Bevor er geht, zeigt er dir, wo er das trockene Holz versteckt hat.",
                        ],
                        ## Die Front verliert die Kundige AN die Etappe. Die
                        ## Etappe verliert sie nach hinten - weiter weg vom
                        ## Krieg, und trotzdem ein Verlust.
                        "etappe": [
                            "Der alte Schreiber ist zweiundvierzig. Das steht jetzt in einer anderen Liste.",
                            "Er kommt als Wache in ein Gefangenenlager, drei Stationen weiter hinten.",
                            "Er packt in vier Minuten und nimmt seinen eigenen Stift mit.",
                            "Bevor er geht, zeigt er dir, in welchem Fach die alten Vordrucke liegen.",
                        ],
                        "heimat": [
                            "Ihre Tochter hat im Nachbarort geheiratet und erwartet ein Kind.",
                            "Sie zieht für ein halbes Jahr dorthin. Auf dem Land ist es leichter.",
                            "Vorher schreibt sie dir auf, an welchen Tagen welcher Laden liefert.",
                            "Der Zettel hängt danach ein Jahr lang neben deiner Tür.",
                        ],
                    }
                ),
                Schicksalsstufe(
                    1917, 34,
                    braucht=["lebendig"], braucht_fort=True,
                    fort=False,
                    meldung={
                        "front": [
                            "Der Bahnhof ist aufgelöst worden, die Landwehr kommt wieder nach vorn.",
                            "Er ist zurück und sagt, in der Etappe habe man mehr Angst als hier.",
                            "Hier wisse man wenigstens, woher es kommt.",
                        ],
                        "etappe": [
                            "Das Lager wird zusammengelegt, und die Wachen kommen zurück.",
                            "Er ist wieder an seinem Tisch und sagt, dort hinten sei es stiller gewesen.",
                            "Stiller heiße nicht besser, sagt er, und schlägt das Buch auf.",
                        ],
                        "heimat": [
                            "Sie ist zurück, weil auf dem Land auch nichts mehr abfällt.",
                            "Das Kind ihrer Tochter ist gesund. Mehr erzählt sie nicht.",
                            "Am ersten Morgen steht sie um vier wieder in der Schlange.",
                        ],
                    }
                ),
            ]
        ),

        Schicksal(
            "kundige_akte", "kundige", "In der Akte",
            [
                Schicksalsstufe(
                    1917, {"front": 24, "etappe": 26, "heimat": 30}, bis_jahr=1918,
                    braucht=["lebendig"],
                    zustand="verhaftet", fort=True,
                    grund={"front": "vor dem Kriegsgericht",
                           "etappe": "vor dem Kriegsgericht",
                           "heimat": "in Schutzhaft"},
                    wirkung={"aufmerksamkeit": 1},
                    meldung={
                        "front": [
                            "Er hat vor sechs Mann gesagt, was er vom letzten Befehl hält.",
                            "Einer davon hat es gemeldet. Es wäre gleichgültig, welcher.",
                            "Die Anklage lautet auf Beleidigung eines Vorgesetzten.",
                            "Zwei Tage später ist sein Platz leer und sein Name aus der Liste gestrichen.",
                        ],
                        ## Die Etappe kommt nicht wegen eines Wortes in die
                        ## Akte, sondern wegen einer Spalte. Das ist
                        ## dieselbe Spalte, die etappe_verpflegungsausgabe
                        ## der Spielerin selbst zum Fuellen hinlegt.
                        "etappe": [
                            "In der Abrechnung fehlen achtzig Kilo Mehl, und geprüft wird von oben.",
                            "Er hat die Spalte für Schwund geführt, seit du hier bist.",
                            "Die Anklage lautet auf Unterschlagung.",
                            "Zwei Tage später ist sein Tisch leer, und seine Bücher liegen versiegelt daneben.",
                        ],
                        "heimat": [
                            "Im April ist die Brotration gekürzt worden, und die Werke haben gestreikt.",
                            "Sie war nicht die Lauteste. Sie war nur die, die man kennt.",
                            "Zwei Beamte holen sie am Mittwoch ab. Sie darf einen Mantel mitnehmen.",
                            "Das nennt sich Schutzhaft und stützt sich auf das Gesetz über den Belagerungszustand. Ein Gericht kommt darin nicht vor.",
                        ],
                    }
                ),
                Schicksalsstufe(
                    1917, 55,
                    braucht=["verhaftet"], braucht_fort=True,
                    zustand="lebendig", fort=False, verbundenheit=1,
                    meldung={
                        "front": [
                            "Sechs Wochen Festungshaft, dann kommt er zurück in die Stellung.",
                            "Er ist grau geworden und redet nur noch, wenn er gefragt wird.",
                            "Über das Urteil sagt er einen Satz: Es hätte schlimmer kommen können.",
                        ],
                        "etappe": [
                            "Nach acht Wochen ist er zurück, ohne Urteil und ohne Erklärung.",
                            "Er führt keine Bücher mehr, sondern trägt Kisten wie die Neuen.",
                            "Über die Spalte für Schwund sagt er von da an nichts mehr.",
                        ],
                        "heimat": [
                            "Nach elf Wochen ist sie wieder da. Ein Verfahren hat es nie gegeben.",
                            "Sie hat vier Kilo verloren und eine Nummer bekommen, die bleibt.",
                            "Sie sagt: Wer einmal in der Akte steht, steht darin auch nach dem Krieg.",
                        ],
                    }
                ),
            ]
        ),

        Schicksal(
            "kundige_ende", "kundige", "Der Ausgang",
            [
                Schicksalsstufe(
                    ## Zwei Wuerfe (Eintritt in 1918 und in 1919) ergeben
                    ## zusammen rund 23 Prozent an der Front und 15 in der
                    ## Heimat. Vorher standen hier 20 und 22, das ergab in
                    ## der Probe 36 beziehungsweise 38 Prozent.
                    1918, {"front": 22, "etappe": 18, "heimat": 15}, bis_jahr=1918,
                    braucht=["lebendig", "verhaftet"],
                    zustand="gefallen", fort=True,
                    grund={"front": "gefallen", "etappe": "gefallen",
                           "heimat": "gestorben"},
                    wirkung={"belastung": 1, "rueckhalt": -1},
                    meldung={
                        "front": [
                            "Es war kein Angriff. Es war ein einzelner Einschlag am Mittag.",
                            "Er hatte sein Kochgeschirr in der Hand und stand zwei Schritte neben dir.",
                            "Wer mit ihm gesprochen hat, wird gefragt, ob er noch etwas gesagt hat.",
                            "Er hat nichts gesagt. Das schreibst du auch in den Brief an seine Frau.",
                        ],
                        ## Auch die Etappe wurde getroffen: Fliegerangriffe
                        ## auf Bahnhoefe und Magazine gehoerten ab 1916 zum
                        ## Bild. Der Tod kommt hier nicht aus dem Graben,
                        ## sondern von oben, mitten in die Arbeit.
                        "etappe": [
                            "Es war kein Angriff. Ein Flieger hat den Bahnhof am Mittag getroffen.",
                            "Er stand an der Rampe und hatte die Liste in der Hand.",
                            "Die Liste ist danach noch da, und sie ist vollständig.",
                            "Du schreibst sie ab und legst das Blatt mit seiner Schrift beiseite.",
                        ],
                        "heimat": [
                            "Sie ist im Winter gestorben. Erst die Grippe, dann die Lunge.",
                            "Sie war einundfünfzig und hat gewogen wie ein junges Mädchen.",
                            "Ihre Vorschriftenzettel liegen noch in der Schublade. Du wirfst keinen davon weg.",
                        ],
                    }
                ),
            ]
        ),

        ########################################################################
        ## Die Amtsperson
        ########################################################################

        Schicksal(
            "amt_wechsel", "amtsperson", "Ein anderer sitzt jetzt da",
            [
                Schicksalsstufe(
                    1916, 45, bis_jahr=1918,
                    braucht=["lebendig"], braucht_fort=False,
                    zustand="entfremdet", fort=True, verbundenheit=-2,
                    grund={"front": "abgelöst", "etappe": "versetzt", "heimat": "versetzt"},
                    meldung={
                        "front": [
                            "Der Feldwebel ist zur Rekrutenausbildung nach Hause versetzt worden.",
                            "Der Neue hat drei Jahre Krieg und keine Geduld.",
                            "Er liest die Liste vor und sieht dabei niemanden an.",
                            "Was der Alte durchgehen ließ, weiß der Neue nicht. Er würde es auch nicht.",
                        ],
                        "etappe": [
                            "Der Zahlmeister ist zu einer anderen Etappeninspektion versetzt worden.",
                            "Der Neue kommt aus dem Reich und hat noch keinen Zug gesehen.",
                            "Er liest die Bücher von hinten nach vorn und findet drei Fehler am ersten Tag.",
                            "Zwei davon hat der Alte gekannt und stehen lassen.",
                        ],
                        "heimat": [
                            "Am Schalter drei sitzt seit Montag ein anderer.",
                            "Der Alte ist ins Kreisamt versetzt worden, sagt der Neue, ohne aufzusehen.",
                            "Deine Anträge fangen von vorn an. Was besprochen war, ist nicht besprochen.",
                            "Der Neue sagt bei jedem zweiten Satz: Das steht so nicht in der Verordnung.",
                        ],
                    }
                ),
            ]
        ),

        Schicksal(
            "amt_selbst", "amtsperson", "Er ist auch nur einer",
            [
                Schicksalsstufe(
                    1916, 40, bis_jahr=1918,
                    braucht=["lebendig", "entfremdet"],
                    verbundenheit=2,
                    meldung={
                        "front": [
                            "Sein Sohn ist Jahrgang siebenundneunzig und seit dem Frühjahr im Feld.",
                            "Er zeigt dir das Bild, ohne dass du gefragt hast, und steckt es sofort wieder weg.",
                            "Am nächsten Morgen führt er die Liste wie immer.",
                            "Nur bei einem Namen bleibt er hängen und liest ihn zweimal.",
                        ],
                        ## Hinter der Akte wird ein Mensch sichtbar - in der
                        ## Etappe ausgerechnet dadurch, dass er dieselben
                        ## Listen liest wie die Spielerin.
                        "etappe": [
                            "Sein Sohn ist Jahrgang siebenundneunzig und seit dem Frühjahr im Feld.",
                            "Er sucht dessen Namen auf jeder Verlustliste, die durch das Buch geht.",
                            "Am Donnerstag findet er ihn nicht, und er sagt es dir nicht.",
                            "Er sagt nur, du sollst die Spalte heute selbst zusammenzählen.",
                        ],
                        "heimat": [
                            "Am Schalter hängt ein Trauerflor. Sein Sohn steht in der Verlustliste vom Donnerstag.",
                            "Er sitzt am Freitag wieder da und ruft die Nummern auf.",
                            "Als du an der Reihe bist, sagt er den Satz mit der Verordnung nicht.",
                            "Er stempelt und schiebt dir den Bogen hin. Das ist alles, was er tun kann.",
                        ],
                    }
                ),
            ]
        ),

        Schicksal(
            "amt_ende", "amtsperson", "Auch er wird krank",
            [
                Schicksalsstufe(
                    1918, {"front": 22, "etappe": 24, "heimat": 26},
                    braucht=["lebendig", "entfremdet"],
                    zustand="erkrankt", fort=True,
                    grund="krank",
                    meldung={
                        "front": [
                            "Er fehlt beim Appell. Das ist in vier Jahren nicht vorgekommen.",
                            "Die Grippe hat ihn erwischt, und er ist nicht mehr der Jüngste.",
                            "Die Liste führt jetzt ein Gefreiter, der schlecht schreibt.",
                        ],
                        "etappe": [
                            "Sein Stuhl bleibt leer, und das ist in vier Jahren nicht vorgekommen.",
                            "Die Grippe liegt seit zwei Wochen in der Baracke nebenan.",
                            "Die Bücher führt jetzt ein Schreiber, der die Spalten verwechselt.",
                        ],
                        "heimat": [
                            "Der Schalter bleibt zwei Wochen geschlossen. Ein Zettel hängt daran.",
                            "Er liegt mit der Grippe im Bett, sagt die Frau vom Nebenschalter.",
                            "Die Anträge stapeln sich. Niemand ist zuständig, und alle sind es.",
                        ],
                    }
                ),
                Schicksalsstufe(
                    1918, 60,
                    braucht=["erkrankt"], braucht_fort=True,
                    zustand="lebendig", fort=False,
                    meldung={
                        "front": [
                            "Er ist wieder da, dünner, und hustet in den Ärmel.",
                            "Er sagt, im Lazarett habe man ihn für einen Offizier gehalten, wegen der Brille.",
                            "Dann nimmt er die Liste und macht weiter, wo der Gefreite aufgehört hat.",
                        ],
                        "etappe": [
                            "Er sitzt wieder am Tisch, dünner, und schreibt langsamer als früher.",
                            "Zuerst rechnet er drei Wochen nach, die der andere geführt hat.",
                            "Dann macht er weiter, wo der Schreiber aufgehört hat.",
                        ],
                        "heimat": [
                            "Der Schalter ist wieder offen. Er sitzt dahinter und sieht aus wie Papier.",
                            "Die Stapel sind nicht kleiner geworden, während er weg war.",
                            "Er fängt oben an. Etwas anderes kann er nicht tun.",
                        ],
                    }
                ),
            ]
        ),

        ########################################################################
        ## Die Gegenseite
        ########################################################################

        Schicksal(
            "gegen_ferne", "gegenseite", "Weiter weg als achtzig Meter",
            [
                Schicksalsstufe(
                    1915, 50, bis_jahr=1918,
                    braucht=["lebendig"], braucht_fort=False,
                    fort=True, verbundenheit=-1,
                    grund={"front": "drüben abgelöst", "etappe": "in ein anderes Lager",
                           "heimat": "im Vorderhaus"},
                    meldung={
                        "front": [
                            "Drüben liegt seit vier Tagen ein anderes Regiment.",
                            "Es singt nicht, und es ruft nicht herüber.",
                            "Es schießt auch mittags, wenn gegessen wird. Das hat der andere nie getan.",
                            "Ob der Mann von drüben abgelöst wurde oder etwas anderes, erfährst du nicht.",
                        ],
                        "etappe": [
                            "Die Kolonne wird abgelöst, und am Montag stehen andere am Gleis.",
                            "Die Neuen sprechen eine andere Sprache und arbeiten schneller.",
                            "Niemand singt, und niemand hebt den Becher.",
                            "Auf deiner Liste steht ab Montag eine neue Nummer und kein Name.",
                        ],
                        "heimat": [
                            "Ihr Sohn ist seit dem Frühjahr in Gefangenschaft, irgendwo hinter Lyon.",
                            "Sie hat eine Karte bekommen, vorgedruckt, halb in einer Sprache, die sie nicht liest.",
                            "Sie steht damit im Hof und fragt jeden, der vorbeikommt.",
                            "Danach steht sie wieder da, wo sie immer steht, und sagt nichts mehr.",
                        ],
                    }
                ),
            ]
        ),

        Schicksal(
            "gegen_schlag", "gegenseite", "Der Einschnitt",
            [
                Schicksalsstufe(
                    1917, {"front": 30, "etappe": 32, "heimat": 34}, bis_jahr=1918,
                    braucht=["lebendig"],
                    zustand={"front": "vermisst", "etappe": "vermisst",
                             "heimat": "entfremdet"},
                    verbundenheit=-2,
                    meldung={
                        "front": [
                            "Bei der Räumung des Grabenstücks findet ihr einen Brotbeutel und Papiere.",
                            "In dem Beutel steckt ein Brief, gefaltet, nie abgeschickt.",
                            "Ihr könnt ihn nicht lesen. Zwei Wörter erkennt ihr trotzdem, weil sie überall gleich klingen.",
                            "Ob es der ist, der gesungen hat, weiß niemand. Es könnte jeder sein.",
                        ],
                        ## Kein Elendsbild, kein Erzaehler, der einordnet.
                        ## Zwei Meldungen widersprechen sich, beide kommen
                        ## ins Buch, und am Morgen stimmt die Zahl wieder.
                        "etappe": [
                            "Beim Abzählen am Abend fehlen zwei aus der Kolonne.",
                            "Der Posten meldet Flucht, der Bauleiter meldet Krankheit, und beides kommt ins Buch.",
                            "Am nächsten Morgen ist die Zahl wieder vollständig, mit zwei anderen darin.",
                            "Wen du gestern gezählt hast, weißt du nicht mehr genau.",
                        ],
                        "heimat": [
                            "Im Vorderhaus ist eine Anzeige eingegangen. Es ging um Butter unter der Hand.",
                            "Getroffen hat es die Familie im dritten Stock. Der Mann sitzt jetzt vier Wochen.",
                            "Sie sagt nichts dazu und sieht dich im Hof nicht mehr an.",
                            "Alle wissen es, niemand weiß es sicher, und niemand redet mehr laut im Treppenhaus.",
                        ],
                    }
                ),
            ]
        ),

        Schicksal(
            "gegen_ende", "gegenseite", "Der Ausgang",
            [
                Schicksalsstufe(
                    ## An der Front bleibt der Wert hoch: Dass der Mann von
                    ## drueben nicht mehr lebt, ist der Kern dieser Rolle.
                    ## In der Heimat stirbt eine Nachbarin an der Grippe
                    ## deutlich seltener.
                    1918, {"front": 33, "etappe": 27, "heimat": 21}, bis_jahr=1918,
                    braucht=["vermisst", "entfremdet", "lebendig"],
                    zustand={"front": "gefallen", "etappe": "gefallen",
                             "heimat": "gefallen"},
                    fort=True, grund={"front": "gefallen", "etappe": "gestorben",
                                      "heimat": "gestorben"},
                    meldung={
                        "front": [
                            "Bei einem Vorstoß kommt ihr über den alten Graben von drüben.",
                            "Er ist zugeschüttet. Was darin lag, liegt darunter.",
                            "Jemand sagt, hier hätten sie im Sommer fünfzehn gesungen. Die Neuen glauben es nicht.",
                            "Du widersprichst nicht. Du warst dabei, und es hilft niemandem.",
                        ],
                        ## Der Schluss des Bogens, den abschluss_gegenseite
                        ## begonnen hat: Auf der Liste stehen Nummern. Dass
                        ## die Spielerin weiss, WER gestorben ist, liegt
                        ## einzig daran, dass sie einmal einen Namen
                        ## danebengeschrieben hat.
                        "etappe": [
                            "Im Oktober liegt die halbe Kolonne mit Fieber in einer eigenen Baracke.",
                            "Auf der Liste werden Nummern gestrichen, nicht Namen.",
                            "Einer davon ist der, der um Wasser gebeten hat.",
                            "Du weißt es, weil du seinen Namen einmal danebengeschrieben hast.",
                        ],
                        "heimat": [
                            "Die Frau aus dem Vorderhaus ist im Oktober an der Grippe gestorben.",
                            "Ihr Sohn ist zu diesem Zeitpunkt noch in Frankreich und weiß es nicht.",
                            "Er kommt im März 1920 zurück und findet eine leere Wohnung.",
                            "Was zwischen euch stand, lässt sich jetzt nicht mehr klären.",
                        ],
                    }
                ),
            ]
        ),

    ]

    SCHICKSAL_INDEX = {}
    for _kette in SCHICKSALE:
        SCHICKSAL_INDEX[_kette.kennung] = _kette


################################################################################
## 5. Bestand: Briefe
################################################################################
##
## Der Briefwechsel ist die zweite Hälfte dieses Pakets. Es gilt eine
## einfache Regel, und sie steht auch im Spiel:
##
##   Schreiben kann dir nur, wer gerade nicht bei dir ist.
##
## Zu Beginn ist niemand fort. Deshalb kommt in den ersten Monaten nur
## amtliche Post. Erst wenn ein Schicksal jemanden wegführt, beginnt der
## Briefwechsel mit dieser Person, und er endet, sobald sie zurückkommt.
##
## Die Gegenseite schreibt nie. Genau das ist ihr Punkt: Man sieht sie, man
## hört sie, man weiß, dass sie aus Menschen besteht, und man schreibt
## einander trotzdem nicht. Von ihr kommen nur zwei Fundstücke.
##
## braucht_fort: True nur wenn die Figur fort ist, False nur wenn sie bei
## dir ist, None in beiden Fällen.

init 1 python:

    BRIEFE = [

        ########################################################################
        ## In der Heimat: amtliche Post
        ########################################################################

        Brief(
            "h_amt_unterstuetzung", "amtsperson", "heimat", [1914, 1915],
            "amtlich", "Eingegangen am 4. Oktober",
            "Ein Umschlag ohne Marke im Kasten. In der Ecke der Stempel der Gemeinde.",
            [
                "Auf Ihren Antrag vom 14. September ergeht folgender Bescheid:",
                "Die Familienunterstützung wird bewilligt. Neun Mark im Monat, dazu vier Mark für das Kind.",
                "Die Zahlung beginnt am 1. Oktober und ist am Schalter 3 persönlich abzuholen.",
                "Jede Veränderung im Haushalt ist binnen drei Tagen anzuzeigen.",
                "Gegen diesen Bescheid ist Beschwerde zulässig. Sie hat keine aufschiebende Wirkung.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "erkrankt"], braucht_fort=None,
            antworten=[
                Briefantwort(
                    "Am Schalter nachfragen, was das genau heißt",
                    "Dreizehn Mark. Du willst wissen, wofür die reichen sollen.",
                    "Du stehst zwei Stunden an. Der Beamte rechnet dir die Miete vor, dann das Brot, dann das Petroleum. Am Ende bleibt eine Zahl übrig, die er selbst nicht laut sagt. Er legt dir ein Merkblatt über die Kriegsküche dazu.",
                    wirkung={"belastung": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Den Bescheid einstecken und gehen",
                    "Es steht ohnehin fest, was darin steht.",
                    "Du faltest das Papier zweimal und steckst es zur Brotkarte. Zu Hause legst du es in die Schublade zu den anderen. Es ist der dritte Bescheid in diesem Jahr, und keiner davon hat je etwas geändert.",
                    wirkung={}, verbundenheit=-1
                ),
            ]
        ),

        Brief(
            "h_amt_kuerzung", "amtsperson", "heimat", [1916, 1917],
            "amtlich", "Angeschlagen am 11. Januar",
            "Kein Brief, ein Anschlag am Schalter. Du schreibst dir die Sätze ab, weil es nur einen Zettel gibt.",
            [
                "Bekanntmachung des Kommunalverbandes.",
                "Die Brotmenge wird ab dem 15. des Monats auf 1600 Gramm in der Woche festgesetzt.",
                "Kartoffeln stehen bis auf Weiteres nicht zur Verfügung. Zugeteilt werden Kohlrüben.",
                "Ein Merkblatt mit achtzehn Rezepten ist am Schalter 2 erhältlich.",
                "Zuwiderhandlungen gegen die Höchstpreise werden nach dem Belagerungszustandsgesetz verfolgt.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "erkrankt"], braucht_fort=None,
            wirkung={"versorgung": -1},
            antworten=[
                Briefantwort(
                    "Das Merkblatt holen",
                    "Achtzehn Rezepte für eine Rübe. Irgendeines wird gehen.",
                    "Du kochst am Abend Nummer sieben, Rübe mit Zwiebel. Es riecht bis in den zweiten Stock. Am dritten Tag isst du es, ohne es zu schmecken, und das ist die einzige Verbesserung, die eintritt.",
                    wirkung={"belastung": -1}, verbundenheit=1
                ),
                Briefantwort(
                    "Fragen, wo die Kartoffeln geblieben sind",
                    "Im Herbst standen sie noch auf den Feldern.",
                    "Der Beamte sieht dich an und sagt, das entscheide nicht dieses Zimmer. Hinter dir wird es still. Er notiert nichts, aber du merkst, dass er sich deinen Namen ansieht, bevor er den Nächsten aufruft.",
                    wirkung={"aufmerksamkeit": 1}, verbundenheit=0
                ),
            ]
        ),

        Brief(
            "h_amt_metall", "amtsperson", "heimat", [1917, 1918],
            "amtlich", "Zugestellt am 2. März",
            "Ein Bogen mit zwei Unterschriften. Eine davon ist die des Pfarrers.",
            [
                "Aufforderung zur Ablieferung von Metallgegenständen.",
                "Abzuliefern sind Gegenstände aus Kupfer, Messing, Nickel und Zinn.",
                "Darunter fallen Türbeschläge, Mörser, Leuchter, Waschkessel und Dachrinnen.",
                "Die Ablieferung erfolgt bis zum 20. März, Sammelstelle ist der Schulhof.",
                "Für abgelieferte Gegenstände wird der Wert nach der amtlichen Liste vergütet.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "erkrankt"], braucht_fort=None,
            antworten=[
                Briefantwort(
                    "Den Waschkessel bringen",
                    "Er ist aus Kupfer, und ohne ihn wird das Waschen schwerer.",
                    "Auf dem Schulhof stehen die Kessel in Reihen. Zwei Männer wiegen, ein dritter schreibt. Am Sonntag darauf werden die Glocken abgenommen. Die kleine bleibt hängen, für den Fall eines Feuers.",
                    wirkung={"belastung": 1}, verbundenheit=1
                ),
                Briefantwort(
                    "Den Kessel im Keller lassen",
                    "Nachgezählt hat bisher niemand.",
                    "Du stellst ihn hinter die Kohlenkiste und legst Säcke darüber. Zwei Wochen später geht ein Mann durch die Häuser und fragt nach Kupfer. Du sagst, ihr hättet keines. Er schreibt etwas auf und geht zur nächsten Tür.",
                    wirkung={"aufmerksamkeit": 1}, verbundenheit=-1
                ),
            ]
        ),

        ########################################################################
        ## In der Heimat: Post von den Fortgegangenen
        ########################################################################

        Brief(
            "h_kind_land", "kind", "heimat", [1915, 1916],
            "feldpost", "Poststempel: 9. Mai",
            "Ein Bogen aus einem Schulheft, in Bleistift. Die Zeilen laufen nach unten weg.",
            [
                "hier gibt es Milch. Richtig warm, morgens gleich aus dem Eimer.",
                "Die Tante sagt, ich soll nicht schreiben, dass es Milch gibt. Ich schreibe es trotzdem.",
                "In der Schule sind wir sechs. Der Lehrer ist eingezogen, jetzt kommt der alte Herr Reinhardt.",
                "Ich muss Rüben verziehen, den ganzen Nachmittag. Der Rücken tut abends weh.",
                "Wann darf ich wieder heim? Ich habe niemandem etwas getan.",
                "Schreib mir bitte zurück. Auch wenn es kurz ist.",
            ],
            braucht=["lebendig"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Ehrlich zurückschreiben",
                    "Vier Sätze. In zweien steht, wie es dir wirklich geht.",
                    "Du schreibst, dass du es auch nicht schön findest. Hier gibt es nichts zu essen, wofür es sich lohnt zurückzukommen. Die Antwort braucht elf Tage. Sie besteht aus einem Satz: Dann bleibe ich eben noch. Darunter ist eine Kuh gemalt.",
                    wirkung={"belastung": 1, "rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Schreiben, dass alles in Ordnung ist",
                    "Zwei Zeilen. Sie beantworten nichts von dem, was gefragt war.",
                    "Du schreibst, es gehe allen gut und es dauere nicht mehr lange. Die Antwort kommt schnell und ist noch kürzer als deine. Beim nächsten Brief steht die Frage nach dem Heimkommen nicht mehr darin.",
                    wirkung={}, verbundenheit=-1
                ),
            ]
        ),

        Brief(
            "h_kind_fabrik", "kind", "heimat", [1917, 1918],
            "feldpost", "Poststempel: 3. November",
            "Diesmal Tinte, und die Handschrift ist fester geworden.",
            [
                "ich arbeite jetzt beim Bauern gegen Kost. Die Tante hat keine Milch mehr, die Kuh ist weg.",
                "Vier Uhr aufstehen, Stall, dann Feld. Um acht Uhr abends bin ich fertig.",
                "Ich habe Hornhaut an beiden Händen. Ich habe sie einem Jungen gezeigt, der war neidisch.",
                "Gestern haben sie beim Nachbarn den Speicher durchsucht und Getreide gefunden.",
                "Sie haben ihn mitgenommen. Seine Frau hat im Hof gestanden und nicht geweint.",
                "Bin ich hier eigentlich sicherer als bei euch? Das frage ich mich seit gestern.",
            ],
            braucht=["lebendig"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Auf die Frage antworten",
                    "Sicher ist gerade niemand. Das kann man auch einem Kind sagen.",
                    "Du schreibst, dass niemand sicher ist, dass es aber besser sei, wo es etwas zu essen gibt. Zwei Wochen später kommt ein Päckchen: vier Eier, in Zeitungspapier, drei davon heil. Dazu ein Zettel: Für dich, nicht für die anderen.",
                    wirkung={"versorgung": 1, "rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Schreiben, dass es sich um nichts kümmern soll",
                    "Wer zu viel fragt, redet irgendwann darüber.",
                    "Du schreibst, es solle arbeiten und sonst nichts. Die nächste Post kommt erst nach Weihnachten und enthält einen einzigen Satz über die Arbeit. Über den Nachbarn steht nichts mehr darin, und über den Speicher auch nicht.",
                    wirkung={"aufmerksamkeit": -1}, verbundenheit=-2
                ),
            ]
        ),

        Brief(
            "h_naechste_werk", "naechste", "heimat", [1916, 1917],
            "feldpost", "Poststempel: 22. August",
            "Ein Bogen aus dem Werksheim, mit einem gedruckten Kopf und einer geraden Handschrift.",
            [
                "wir arbeiten zwölf Stunden, dann zwölf Stunden Pause, dann wieder zwölf.",
                "Meine Hände sind gelb bis über die Handgelenke. Das geht nicht ab, das wächst heraus.",
                "Die Kantine gibt zweimal am Tag warm. Dafür allein bin ich hergekommen.",
                "Am Sonntag sitzen wir auf den Betten und niemand redet. Alle sind zu müde zum Reden.",
                "Ich habe zweiundzwanzig Mark übrig. Soll ich sie schicken oder soll ich kommen?",
            ],
            braucht=["lebendig"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Sie soll kommen",
                    "Geld hilft. Ein Gesicht am Küchentisch hilft anders.",
                    "Sie fährt am übernächsten Sonntag, sechs Stunden hin und zurück, für einen Nachmittag. Sie bringt Brot mit, das sie sich abgespart hat, und geht um sieben wieder zur Bahn. Ihr habt fast nichts geredet, und es war trotzdem der beste Tag seit Monaten.",
                    wirkung={"rueckhalt": 1, "belastung": -1}, verbundenheit=2
                ),
                Briefantwort(
                    "Sie soll das Geld schicken",
                    "Zweiundzwanzig Mark sind auf dem Schwarzmarkt ein halbes Pfund Butter.",
                    "Das Geld kommt in einem Umschlag, ohne Zeile dazu. Du kaufst Fett und Zucker unter der Hand und zahlst das Doppelte. Es reicht drei Wochen. Beim nächsten Brief fragt sie nicht mehr, ob sie kommen soll.",
                    wirkung={"versorgung": 1, "aufmerksamkeit": 1}, verbundenheit=-1
                ),
            ]
        ),

        Brief(
            "h_kundige_land", "kundige", "heimat", [1916, 1917],
            "feldpost", "Poststempel: 14. Dezember",
            "Vier eng beschriebene Seiten. Die Hälfte davon sind Anweisungen.",
            [
                "das Kind ist da, ein Junge, und beide sind gesund. Mehr will ich gar nicht.",
                "Jetzt zu dir. Der Reichstag hat im Dezember das Hilfsdienstgesetz beschlossen.",
                "Jeder Mann zwischen siebzehn und sechzig kann zur Arbeit verpflichtet werden, wenn er nicht Soldat ist.",
                "Für uns Frauen gilt das nicht. Melden kann man sich freiwillig, und viele tun es wegen der Karte.",
                "Wer in der Rüstung arbeitet, bekommt eine Zusatzkarte für Schwerarbeit. Der Betrieb muss sie bescheinigen.",
                "Geh damit zum Schalter, bevor du zum Meister gehst. In der Reihenfolge, sonst schicken sie dich zweimal.",
            ],
            braucht=["lebendig"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Es genau so machen",
                    "Sie hat sich in vier Jahren noch nie geirrt.",
                    "Du gehst zuerst zum Schalter, dann zum Betrieb. Es dauert einen ganzen Vormittag und funktioniert. Die Zusatzkarte gilt für vier Wochen und muss danach neu bescheinigt werden. Das steht klein gedruckt unten, und sie hatte es dir aufgeschrieben.",
                    wirkung={"versorgung": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Den Brief weiterreichen",
                    "Vier Seiten Vorschriften. Im Haus können sie mehr als eine gebrauchen.",
                    "Du liest die Seiten im Treppenhaus vor. Am nächsten Tag stehen sechs Frauen aus dem Haus vor demselben Schalter, mit denselben Sätzen. Der Beamte fragt, wer ihnen das gesagt hat. Du antwortest nicht, aber er sieht dich an, während er es notiert.",
                    wirkung={"rueckhalt": 1, "aufmerksamkeit": 1}, verbundenheit=1
                ),
            ]
        ),

        ## WIRD NIE GEZOGEN (Befund Paket 2, bestaetigt Paket 3, Schritt 2) ######################
        ## Grund: nicht die Bedingung, sondern das Jahr. In 1600 gemessenen
        ## Durchgängen war dieser Brief sechsmal erlaubt - gezogen wurde er
        ## null mal, weil es in 1917 fast keine Post gibt: 16 Sendungen in
        ## 1600 Durchgängen. Post wird nur nach einem Ereignis zugestellt,
        ## und 1917 hat keinen Ereignisbestand. Die 47 Ziehungen, die 1917
        ## überhaupt zustande kommen, sind Kettenereignisse aus 1916.
        ## Zu ändern ist hier nichts. Der Brief wird erreichbar, sobald
        ## 1917 und 1918 einen Bestand haben (Paket 4 und 5).
        Brief(
            "h_kundige_haft", "kundige", "heimat", [1917, 1918],
            "feldpost", "Abgestempelt, geöffnet, wieder verschlossen",
            "Ein vorgedruckter Bogen mit einem Streifen quer darüber: Geprüft. Sechs Zeilen sind erlaubt.",
            [
                "mir geht es den Umständen nach gut. Ich bin gesund.",
                "Ich darf alle vier Wochen sechs Zeilen schreiben. Diese sind es.",
                "Bitte schicke keine Lebensmittel, sie kommen nicht an.",
                "Ein Verfahren gibt es nicht. Es gibt auch keinen Termin.",
                "Sage niemandem, dass du mir schreibst. Es nützt dir nichts und mir auch nicht.",
                "Der Zettel neben deiner Tür stimmt noch. Halte dich daran.",
            ],
            braucht=["verhaftet"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Trotzdem antworten",
                    "Sechs Zeilen sind nicht viel. Es sind mehr als keine.",
                    "Du schreibst sechs Zeilen zurück, in denen fast nichts steht: das Wetter, das Haus, der Hof. Der Brief kommt an. Zwei Wochen später steht ein Beamter vor deiner Tür und fragt, woher du sie kennst. Er notiert die Antwort und geht wieder.",
                    wirkung={"aufmerksamkeit": 1, "rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Den Brief verbrennen",
                    "Sie hat selbst geschrieben, dass es dir nichts nützt.",
                    "Du hältst ihn über den Herd, bis nichts mehr da ist. Es dauert länger, als du gedacht hast. Als sie Monate später zurückkommt, fragt sie nicht nach dem Brief. Sie fragt überhaupt nach nichts mehr.",
                    wirkung={}, verbundenheit=-2
                ),
            ]
        ),

        Brief(
            "h_gegen_karte", "gegenseite", "heimat", [1916, 1917, 1918],
            "fundstueck", "Falsch eingeworfen",
            "In deinem Kasten liegt eine Karte, die nicht dir gehört. Sie ist an das Vorderhaus adressiert.",
            [
                "Kriegsgefangenensendung. Portofrei. Vordruck des Internationalen Komitees, Genf.",
                "Angekreuzt ist: Ich bin gesund.",
                "Angekreuzt ist: Ich bin nicht verwundet.",
                "In der Zeile für die eigenen Worte stehen sieben: Liebe Mutter, das Essen reicht, sorge dich nicht.",
                "Darunter, in einer anderen Handschrift, ein Stempel und eine Nummer.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "vermisst"], braucht_fort=None,
            antworten=[
                Briefantwort(
                    "Die Karte hinübertragen",
                    "Sie steht im Hof. Du müsstest nur zehn Schritte gehen.",
                    "Sie nimmt die Karte und liest sie im Stehen dreimal. Dann fragt sie dich, was gesund auf Französisch heißt, und du weißt es nicht. Ihr steht beide im Hof und seht auf ein Stück Papier. Es kommt aus dem Land, gegen das ihr Krieg führt.",
                    wirkung={"rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Die Karte in den Kasten des Vorderhauses stecken",
                    "Sie kommt an. Mehr ist nicht deine Sache.",
                    "Du schiebst sie durch den Schlitz und gehst die Treppe hinauf. Am Abend steht sie im Hof und hat die Karte in der Hand. Sie sieht zu deinem Fenster hoch. Du trittst einen Schritt zurück, und sie sieht wieder weg.",
                    wirkung={}, verbundenheit=-1
                ),
            ]
        ),

        ########################################################################
        ## An der Front: amtliche Post
        ########################################################################

        Brief(
            "f_amt_urlaub", "amtsperson", "front", [1914, 1915],
            "amtlich", "Ausgehändigt am 12. Oktober",
            "Der Feldwebel liest die Namen vor und drückt jedem sein Papier in die Hand.",
            [
                "Auf das Urlaubsgesuch vom 2. Oktober ergeht folgender Bescheid:",
                "Das Gesuch wird zurückgestellt. Grund: dienstliche Erfordernisse.",
                "Eine erneute Eingabe ist frühestens nach acht Wochen zulässig.",
                "Urlaub wird in der Reihenfolge des Eingangs gewährt, soweit die Lage es zulässt.",
                "Zur Kenntnis genommen und zurückzugeben.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "erkrankt"], braucht_fort=None,
            antworten=[
                Briefantwort(
                    "Sofort eine neue Eingabe schreiben",
                    "Acht Wochen. Man kann sie ja vom Tag des Bescheids an rechnen.",
                    "Du schreibst dieselben Sätze noch einmal ab und gibst sie beim Feldwebel ab. Er nimmt sie, sieht das Datum und legt sie in die Mappe. Er sagt: Ich reiche alles weiter. Was oben damit geschieht, entscheidet nicht dieser Unterstand.",
                    wirkung={"belastung": 1}, verbundenheit=1
                ),
                Briefantwort(
                    "Das Papier zusammenfalten und einstecken",
                    "Es ändert nichts, ob du es zweimal einreichst.",
                    "Du steckst den Bogen zum Soldbuch. Zwei Männer aus der Gruppe fahren im November, beide haben früher eingereicht als du. Sie kommen mit Fotos zurück, und du sagst, das sei in Ordnung, und meinst es fast.",
                    wirkung={"rueckhalt": -1}, verbundenheit=0
                ),
            ]
        ),

        ## GILT IN BEIDEN FELDWELTEN. Seit Paket 5, Schritt 1, Teil B darf
        ## welt mehrere Welten nennen. Dieser Bescheid ist der einzige der
        ## zehn Frontbriefe, der ohne ein einziges geändertes Wort auch in
        ## der Etappe steht: Die Gemeinde schickt ihn an die Truppe, nicht
        ## in den Graben, und weder der Bogen noch die beiden Antworten
        ## setzen eine Stellung voraus. Die übrigen neun bleiben bei der
        ## Front - sie handeln von der Bagage, vom Grabenbereich oder von
        ## einem Schicksal, das die Etappe so nicht hat.
        Brief(
            "f_amt_heimat", "amtsperson", ["front", "etappe"], [1916, 1917],
            "amtlich", "Weitergeleitet über die Kompanie",
            "Kein Feldpostbrief. Ein amtlicher Bogen, den die Gemeinde an die Truppe geschickt hat.",
            [
                "Mitteilung an den Angehörigen zur Kenntnisnahme.",
                "Die Familienunterstützung wird ab dem 1. des Monats neu berechnet.",
                "Grund: Änderung der Zahl der unterstützungsberechtigten Personen im Haushalt.",
                "Der neue Satz beträgt monatlich elf Mark fünfzig.",
                "Einwendungen sind schriftlich beim Gemeindeamt einzulegen, nicht bei der Truppe.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "erkrankt"], braucht_fort=None,
            antworten=[
                Briefantwort(
                    "Nachrechnen, was sich geändert hat",
                    "Weniger Personen im Haushalt. Nur welche fehlt?",
                    "Du rechnest den Satz zurück und kommst auf eine Person. Es steht nicht darin, welche, und es steht auch nicht darin, warum. Du schreibst noch am selben Abend nach Hause und wartest neunzehn Tage auf die Antwort. In diesen neunzehn Tagen schläfst du schlecht.",
                    wirkung={"belastung": 2}, verbundenheit=1
                ),
                Briefantwort(
                    "Das Papier dem Feldwebel zurückgeben",
                    "Zur Kenntnis genommen. So steht es unten.",
                    "Er nimmt es und hakt deinen Namen ab. Was zu Hause geschehen ist, erfährst du erst beim nächsten Brief von dort, und der braucht drei Wochen. Bis dahin denkst du jeden Abend darüber nach, ohne es einmal auszusprechen.",
                    wirkung={"belastung": 1, "rueckhalt": -1}, verbundenheit=0
                ),
            ]
        ),

        Brief(
            "f_amt_bestand", "amtsperson", "front", [1917, 1918],
            "amtlich", "Verlesen beim Appell",
            "Ein Tagesbefehl, abgeschrieben und am Unterstand angeschlagen.",
            [
                "An sämtliche Kompanien.",
                "Die Brotportion wird ab sofort auf 400 Gramm täglich festgesetzt.",
                "Der Fleischanteil entfällt an zwei Tagen der Woche. Ersatz: Dörrgemüse.",
                "Das Sammeln von Metallteilen im Grabenbereich ist zu verstärken.",
                "Gerüchte über die Lage in der Heimat sind zu unterlassen. Zuwiderhandlungen werden geahndet.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "erkrankt"], braucht_fort=None,
            wirkung={"versorgung": -1},
            antworten=[
                Briefantwort(
                    "Den letzten Satz laut vorlesen",
                    "Es steht da. Jeder kann es lesen. Nur sagt es keiner.",
                    "Du liest ihn vor, und zwei lachen. Der Rest sieht auf den Boden. Am Abend kommt der Feldwebel und sagt, du sollest den Anschlag in Ruhe lassen. Er sagt es leise, und das ist die freundlichste Fassung, die möglich war.",
                    wirkung={"aufmerksamkeit": 1, "rueckhalt": 1}, verbundenheit=0
                ),
                Briefantwort(
                    "Den Anschlag lesen und weitergehen",
                    "Vierhundert Gramm sind vierhundert Gramm, ob man darüber redet oder nicht.",
                    "Du gehst zum Essenholen. Der Napf ist derselbe wie gestern, der Inhalt ist weniger. Zwei Tage später erzählt jemand aus dem Urlaub, wie es zu Hause aussieht. Alle hören zu, und niemand meldet es.",
                    wirkung={"belastung": 1}, verbundenheit=0
                ),
            ]
        ),

        ########################################################################
        ## An der Front: Post von den Fortgegangenen
        ########################################################################

        Brief(
            "f_kind_bagage", "kind", "front", [1915, 1916],
            "feldpost", "Feldpost, gestempelt am 17. Juni",
            "Ein Feldpostbrief aus vier Kilometer Entfernung. Er hat sechs Tage gebraucht.",
            [
                "hier hinten schlafe ich in einer Scheune. Es ist trocken, und es schießt niemand.",
                "Ich habe vier Pferde. Zwei sind gut, eins ist stur, eins ist krank.",
                "Nachts fahren wir nach vorn. Auf dem Rückweg liegen die Verwundeten auf dem Wagen.",
                "Ich rede mit ihnen, damit sie wach bleiben. Manche antworten, manche nicht.",
                "Die anderen sagen, ich hätte Glück gehabt. Stimmt das eigentlich?",
                "Ist der Graben rechts immer noch voll Wasser? Grüß den Alten von mir.",
            ],
            braucht=["lebendig"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Ihm schreiben, dass er Glück gehabt hat",
                    "Er hat es. Er soll es auch glauben dürfen.",
                    "Du schreibst, vier Kilometer seien vier Kilometer, und er solle bei den Pferden bleiben, solange es geht. Seine Antwort kommt nach neun Tagen und besteht fast nur aus Pferden. Zwischen zwei Sätzen steht: Danke, dass du das geschrieben hast.",
                    wirkung={"rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Ihm die Wahrheit über die Wagen schreiben",
                    "Er fragt. Wer fragt, hat es schon geahnt.",
                    "Du schreibst, dass die, die nicht antworten, meistens nicht mehr ankommen, und dass er trotzdem weiterreden soll. Die Antwort braucht drei Wochen. Sie ist kurz und endet mit einem Satz, den du zweimal liest: Ich rede weiter.",
                    wirkung={"belastung": 1, "rueckhalt": 1}, verbundenheit=2
                ),
            ]
        ),

        Brief(
            "f_naechste_lazarett", "naechste", "front", [1915, 1916, 1917],
            "feldpost", "Feldpost, gestempelt am 8. Februar",
            "Fremde Handschrift auf dem Umschlag, seine im Brief. Sie ist ungelenk geworden.",
            [
                "das Schreiben geht wieder, links ist es langsamer, aber es geht.",
                "Der Arm bleibt steif. Der Stabsarzt sagt, für den Dienst reicht es. Er sagt das bei allen.",
                "Hier liegen dreißig Mann in einem Saal. Nachts ist es nie still.",
                "Neben mir liegt einer aus Posen, der seit vier Wochen kein Wort sagt. Er ist unverletzt.",
                "Es gibt Kaffee und ein Bett und niemand schreit Alarm. Ich schlafe trotzdem schlecht.",
                "Sag mir, wer noch da ist. Schreib die Namen einzeln auf, nicht nur wie viele.",
            ],
            braucht=["verwundet"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Die Namen einzeln aufschreiben",
                    "Er hat ausdrücklich darum gebeten.",
                    "Du schreibst elf Namen untereinander und dahinter, wer wo ist. Bei dreien musst du nachfragen, bei zweien weiß es niemand mehr. Er antwortet mit einer Zeile: Ich habe sie gelesen und dann den Brief zerrissen. Es war trotzdem richtig.",
                    wirkung={"belastung": 1, "rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Schreiben, dass alles beim Alten ist",
                    "Er soll zuerst gesund werden.",
                    "Du schreibst vom Wetter, vom Essen und davon, dass sein Platz freigehalten wird. Sein Platz ist seit drei Wochen belegt. Als er zurückkommt, sagt er nichts dazu. Er sieht nur einmal hin und stellt seinen Tornister woanders ab.",
                    wirkung={}, verbundenheit=-1
                ),
            ]
        ),

        ## WIRD NIE GEZOGEN (Befund Paket 2, bestaetigt Paket 3, Schritt 2) ######################
        ## Dieselbe Ursache wie bei h_kundige_haft: Zehnmal wäre er in 1600
        ## Durchgängen erlaubt gewesen, aber 1917 gibt es kaum Post, weil
        ## es kaum Ereignisse gibt. Die Bedingung selbst ist in Ordnung.
        ## Erreichbar, sobald 1917 und 1918 einen Bestand haben.
        Brief(
            "f_naechste_gefangen", "naechste", "front", [1917, 1918],
            "feldpost", "Über Genf, gestempelt zweimal",
            "Ein vorgedruckter Bogen aus einem Lager in Südfrankreich. Zwei Zensurstempel.",
            [
                "ich lebe. Das ist der wichtigste Satz, deshalb steht er oben.",
                "Wir arbeiten auf einem Gut, Wein und Oliven. Die Arbeit ist hart und das Essen ist regelmäßig.",
                "Regelmäßig ist mehr wert, als ich vorher gedacht habe.",
                "Der Bauer war selbst vier Jahre Soldat. Er redet mit uns, wenn niemand zusieht.",
                "Zu Hause wissen sie noch nichts. Bitte schreibe du es ihnen, ich darf nur eine Karte im Monat.",
                "Und sage niemandem, dass es mir hier besser geht als euch. Man würde es falsch verstehen.",
            ],
            braucht=["lebendig", "vermisst"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Seiner Familie schreiben",
                    "Sie halten ihn seit dem Frühjahr für vermisst.",
                    "Du schreibst noch am selben Abend. Die Antwort kommt von seiner Mutter, in großer, langsamer Schrift, und besteht aus zwei Sätzen und vielen Ausrufezeichen. Du liest sie mehrmals und legst sie zu deinen eigenen Briefen.",
                    wirkung={"rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Den letzten Satz ernst nehmen und schweigen",
                    "Gefangenschaft ist ein Wort, mit dem man vorsichtig sein muss.",
                    "Du sagst niemandem etwas, auch seiner Familie nicht. Zwei Monate später kommt seine Karte bei ihnen an, mit einem halben Jahr Verspätung. Du hast in diesen zwei Monaten mehrmals überlegt, den Brief doch zu schreiben.",
                    wirkung={"belastung": 1}, verbundenheit=-1
                ),
            ]
        ),

        Brief(
            "f_kundige_etappe", "kundige", "front", [1916, 1917],
            "feldpost", "Feldpost, gestempelt am 30. September",
            "Zwei Seiten, sehr klein geschrieben, damit alles auf den Bogen passt.",
            [
                "Wachdienst am Bahnhof, zwölf Stunden, dann zwölf frei. Ich klage nicht.",
                "Merke dir für den Winter: Fußlappen trocken halten ist wichtiger als Stiefel putzen.",
                "Wer nasse Füße hat, bekommt Frostbeulen, und wer Frostbeulen hat, kommt nicht ins Lazarett, sondern zum Dienst.",
                "Zweitens: Wenn du ein Gesuch schreibst, schreibe kurz und nenne eine Zahl. Sätze ohne Zahl gehen unter.",
                "Drittens, und das ist das wichtigste: Melde dich nie freiwillig für etwas, das nicht erklärt wird.",
                "Hier fahren jede Nacht Züge durch. In der einen Richtung sind sie voll, in der anderen still.",
            ],
            braucht=["lebendig"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Die drei Punkte an die Gruppe weitergeben",
                    "Er hat sie nicht für dich allein aufgeschrieben.",
                    "Du liest sie am Abend im Unterstand vor. Beim dritten Punkt wird es still. Zwei Wochen später wird jemand für einen Auftrag gesucht, der nicht erklärt wird, und aus deiner Gruppe meldet sich niemand. Der Feldwebel sieht dich dabei an.",
                    wirkung={"rueckhalt": 1, "aufmerksamkeit": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Die Punkte für dich behalten",
                    "Was alle wissen, nützt am Ende niemandem.",
                    "Du schreibst dir die drei Sätze in dein Soldbuch. Deine Füße bleiben trocken, dein Gesuch enthält eine Zahl. Als sich zwei aus der Gruppe freiwillig melden, sagst du nichts. Einer von beiden kommt zurück und redet danach anders über dich.",
                    wirkung={"belastung": -1, "rueckhalt": -1}, verbundenheit=-1
                ),
            ]
        ),

        ## WIRD NIE GEZOGEN (Befund Paket 2, bestaetigt Paket 3, Schritt 2) ######################
        ## Der engste der drei: nur ein einziges Mal in 1600 Durchgängen
        ## überhaupt erlaubt. Er verlangt, dass die kundige Person in Haft
        ## und fort ist - das leistet die Kette kundige_akte ab 1917 mit 24
        ## Prozent, und in demselben Jahr müsste dann auch noch Post kommen.
        ## Erreichbar, sobald 1917 und 1918 einen Bestand haben.
        Brief(
            "f_kundige_haft", "kundige", "front", [1917, 1918],
            "feldpost", "Geprüft. Vier Zeilen sind durchgestrichen",
            "Ein Bogen aus der Festungshaft. Was er über das Verfahren geschrieben hat, ist geschwärzt.",
            [
                "mir geht es gut. Die Zelle ist trocken, das ist mehr, als der Graben war.",
                "Über das Urteil darf ich nichts schreiben. Du siehst ja, was davon übrig ist.",
                "Sechs Wochen sind sechs Wochen. Andere haben für weniger mehr bekommen.",
                "Merke dir: Was du sagst, sagst du vor Zeugen, auch wenn nur zwei dabei sind.",
                "Ich bin nicht wütend auf den, der es gemeldet hat. Ich weiß nur nicht, welcher es war.",
                "Das ist das Schlechte daran. Es könnte jeder gewesen sein, und so sieht man sie dann auch an.",
            ],
            braucht=["verhaftet"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Ihm schreiben, dass sein Platz frei bleibt",
                    "Sechs Wochen kann man einen Platz freihalten.",
                    "Du legst seinen Tornister an dieselbe Stelle und sagst den Neuen, dass da schon jemand liegt. Zwei nehmen es hin, einer fragt, was mit ihm ist. Du sagst: Er kommt wieder. Als er wiederkommt, sagt er nichts dazu und legt sich hin, als wäre nichts gewesen.",
                    wirkung={"rueckhalt": 1, "aufmerksamkeit": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Den Brief nicht beantworten",
                    "Wer einem Verurteilten schreibt, steht danach mit im Buch.",
                    "Du legst ihn unter die Decke und lässt ihn dort. Nach vier Wochen ist das Papier weich geworden von der Feuchtigkeit. Als er zurückkommt, fragt er, ob der Brief angekommen ist. Du sagst ja. Mehr fragt er nicht.",
                    wirkung={}, verbundenheit=-2
                ),
            ]
        ),

        Brief(
            "f_gegen_fundstueck", "gegenseite", "front", [1915, 1916, 1917],
            "fundstueck", "Kein Absender, kein Empfänger, den ihr lesen könnt",
            "Beim Räumen des Grabenstücks findet ihr einen Brotbeutel. Darin steckt ein gefalteter Bogen.",
            [
                "Der Bogen ist einmal nass geworden und wieder getrocknet. Die Tinte ist an den Rändern verlaufen.",
                "Ihr könnt kein Wort lesen. Zwei erkennt ihr trotzdem, weil sie fast gleich klingen wie bei euch.",
                "Das eine steht ganz oben, in der ersten Zeile, dort, wo bei euch der Name steht.",
                "Das andere steht ganz unten, allein, vor der Unterschrift.",
                "Der Brief ist nie abgeschickt worden. Eine Marke ist nicht darauf, ein Datum auch nicht.",
            ],
            anrede=False,
            braucht=["lebendig", "vermisst", "gefallen"], braucht_fort=None,
            antworten=[
                Briefantwort(
                    "Den Brief weitergeben, damit er ankommt",
                    "Es gibt Stellen, die so etwas über das Rote Kreuz weiterleiten.",
                    "Du gibst ihn beim Feldwebel ab. Er sieht ihn an, dann dich, dann legt er ihn in die Mappe zu den Papieren. Er sagt, er reiche alles weiter. Ob der Brief je angekommen ist, wirst du nie erfahren, und du wirst noch Jahre später daran denken.",
                    wirkung={"rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Den Brief zurücklegen",
                    "Er gehört jemandem, den du nicht kennst und nicht kennen sollst.",
                    "Du faltest ihn wieder zusammen und steckst ihn in den Brotbeutel zurück. Am Abend ist das Grabenstück eingeebnet. Jemand fragt, was in dem Beutel war. Du sagst: Nichts, Papier. Das ist die einzige Lüge, die du an diesem Tag erzählst.",
                    wirkung={"belastung": 1}, verbundenheit=-1
                ),
            ]
        ),

        ########################################################################
        ## In der Etappe: eigene Post
        ########################################################################
        ##
        ## SEIT PAKET 5, SCHRITT 1, TEIL B. Solange briefwelt() die Etappe
        ## auf "front" abbildete, bekam sie stillschweigend alle zehn
        ## Frontbriefe - auch den von der Bagagekolonne und den aus der
        ## Festungshaft, die beide an einem Schicksal hängen, das die
        ## Etappe gar nicht hat. Mit der eigenen Welt fiel das weg, und
        ## übrig blieben zwei geteilte Bescheide. Diese sechs Briefe
        ## schliessen die Lücke, die dadurch entstanden ist.
        ##
        ## Sie hängen an den Etappenfassungen der Schicksale aus den
        ## Gruppen 6 und 7: Wer bei einem Marschbataillon ist, schreibt
        ## von vorn; wer als Bremser fährt, schreibt von der Strecke; wer
        ## ein Gefangenenlager bewacht, schreibt vom Zählen. Zwei
        ## amtliche Bogen kommen dazu, weil die Etappe ihre eigenen
        ## Anweisungen bekam - und mit der Auskämmung die eine, die alles
        ## andere überschattete.

        Brief(
            "et_amt_dienstweg", "amtsperson", "etappe", [1914, 1915],
            "amtlich", "Ausgehändigt am 3. November",
            "Ein Bogen, den der Zahlmeister an das Brett neben der Tür heftet.",
            [
                "Dienstanweisung für die Schreibstuben des Etappenbereichs.",
                "Jede Ausgabe ist am Tag der Ausgabe einzutragen, nicht später.",
                "Fehlmengen sind gesondert auszuweisen und vom Vorgesetzten abzuzeichnen.",
                "Eintragungen sind mit Tinte vorzunehmen. Bleistift gilt als vorläufig.",
                "Wer einen Bestand nicht belegen kann, haftet dafür persönlich.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "erkrankt"], braucht_fort=None,
            antworten=[
                Briefantwort(
                    "Alles mit Tinte nachtragen",
                    "Drei Wochen Bleistift stehen noch im Buch.",
                    "Du sitzt zwei Abende und ziehst jede Zeile nach. Zweimal weißt du nicht mehr, was in der Spalte stand. Du schreibst dann, was plausibel ist. Danach ist das Buch sauber und stimmt an zwei Stellen nicht.",
                    wirkung={"belastung": 1, "aufmerksamkeit": -1}, verbundenheit=0
                ),
                Briefantwort(
                    "Es beim Bleistift lassen",
                    "Was vorläufig ist, lässt sich noch ändern.",
                    "Du machst weiter wie bisher. Vier Wochen später fragt ein Prüfer, warum die Seiten grau sind, und schreibt einen Vermerk. Der Zahlmeister sagt nichts dazu, und das ist schlimmer als eine Rüge.",
                    wirkung={"aufmerksamkeit": 2}, verbundenheit=-1
                ),
            ]
        ),

        ## Die Auskämmung. Sie ist der Bescheid, der über dem ganzen Pfad
        ## steht: Wer hier arbeitet, arbeitet auf Widerruf. Dasselbe
        ## Verfahren trennt in naechste_trennung den Schichtnachbarn ab.
        Brief(
            "et_amt_auskaemmung", "amtsperson", "etappe", [1916, 1917],
            "amtlich", "Verlesen beim Antreten",
            "Ein Tagesbefehl, abgeschrieben und an der Baracke angeschlagen.",
            [
                "An sämtliche Formationen des Etappenbereichs.",
                "Die Dienststellen sind auf Mannschaften zu durchsehen, die felddienstfähig sind.",
                "Unabkömmlich bleibt nur, wer namentlich bezeichnet und begründet ist.",
                "Ersatz durch Landsturm, Kriegsgefangene oder weibliche Kräfte ist zu prüfen.",
                "Die Listen sind bis zum Fünfzehnten des Monats vorzulegen.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "erkrankt"], braucht_fort=None,
            wirkung={"aufmerksamkeit": 1},
            antworten=[
                Briefantwort(
                    "Den eigenen Namen begründen",
                    "Wer die Bücher führt, ist schwer zu ersetzen.",
                    "Du schreibst drei Sätze über die Abrechnung und legst sie dem Zahlmeister vor. Er zeichnet ab, ohne aufzusehen. Auf der Liste stehen am Ende zwei Namen aus deiner Schicht, deiner nicht.",
                    wirkung={"rueckhalt": -2}, verbundenheit=0
                ),
                Briefantwort(
                    "Die Liste ohne Begründung abgeben",
                    "Sollen die entscheiden, die es angeordnet haben.",
                    "Du gibst den Bogen ab, wie er ist. Drei Wochen bleibt es still, dann kommt er zurück, mit einem Haken hinter einem anderen Namen. Wer den Haken gesetzt hat, steht nirgends, und du fragst nicht.",
                    wirkung={"belastung": 1, "rueckhalt": 1}, verbundenheit=0
                ),
            ]
        ),

        Brief(
            "et_naechste_marsch", "naechste", "etappe", [1915, 1916],
            "feldpost", "Feldpost, gestempelt am 4. April",
            "Ein Feldpostbrief aus derselben Richtung, in die eure Züge fahren.",
            [
                "hier vorn ist es ungefähr so, wie du es dir aus den Listen zusammengereimt hast.",
                "Nur riecht es anders. Das steht in keiner Meldung.",
                "Das Brot kommt mit dem Wagen, den du abgefertigt hast. Es war acht Tage unterwegs.",
                "Sag es niemandem, aber ich habe deinen Haken auf dem Begleitschein erkannt.",
                "Schreib mir, wer noch an der Rampe steht. Namen, nicht Zahlen.",
            ],
            braucht=["lebendig"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Die Namen einzeln aufschreiben",
                    "Er hat ausdrücklich darum gebeten.",
                    "Du schreibst neun Namen untereinander, mit der Schicht dahinter. Bei zweien musst du im Buch nachsehen, weil du sie nur als Nummer kennst. Er antwortet nach elf Tagen mit einer Zeile: Das war mehr wert als das Brot.",
                    wirkung={"rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Vom Dienst schreiben",
                    "Er soll nicht hören, dass hier alles beim Alten bleibt.",
                    "Du schreibst von den Zügen, vom Wetter und davon, dass sein Platz frei ist. Sein Platz ist seit zwei Wochen besetzt. Die Antwort kommt spät und ist höflich, und höflich wart ihr nie.",
                    wirkung={}, verbundenheit=-1
                ),
            ]
        ),

        ## Die Gegenkarte zu etappe_gefangenenarbeit: Wer hier Kolonnen
        ## abzählt, bekommt Post von jemandem, der drüben abgezählt wird.
        ## Kein Satz zieht die Verbindung. Sie steht nur da.
        Brief(
            "et_naechste_gefangen", "naechste", "etappe", [1917, 1918],
            "feldpost", "Über Genf, gestempelt zweimal",
            "Ein vorgedruckter Bogen aus einem Lager in Südfrankreich. Zwei Zensurstempel.",
            [
                "ich lebe. Das ist der wichtigste Satz, deshalb steht er oben.",
                "Wir arbeiten an einer Bahnstrecke. Schwellen, Schotter, dieselbe Arbeit wie zu Hause.",
                "Ich zähle jetzt für die anderen, weil ich es kann. Das ist merkwürdig.",
                "Der Posten sieht zu, wie ich schreibe. Er ist ungefähr so alt wie du.",
                "Zu Hause wissen sie noch nichts. Bitte schreibe du es ihnen.",
            ],
            braucht=["lebendig"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Es der Familie schreiben",
                    "Er darf nur eine Karte im Monat schicken.",
                    "Du schreibst den Brief noch am selben Abend und suchst die Anschrift aus dem Buch. Die Antwort von zu Hause kommt nach fünf Wochen und ist an ihn gerichtet, nicht an dich. Du legst sie in den Sack und schickst sie weiter.",
                    wirkung={"belastung": 1, "rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Warten, bis er selbst schreibt",
                    "Eine Karte im Monat ist eine Karte im Monat.",
                    "Du legst den Bogen in die Mappe und nimmst dir vor, es morgen zu tun. Zwei Monate später kommt eine Karte mit einer Frage darauf: Wissen sie es inzwischen? Du beantwortest sie nicht sofort.",
                    wirkung={}, verbundenheit=-1
                ),
            ]
        ),

        Brief(
            "et_kind_strecke", "kind", "etappe", [1915, 1916],
            "feldpost", "Feldpost, gestempelt am 17. Juni",
            "Ein Brief von der Strecke. Er hat drei Tage gebraucht und riecht nach Öl.",
            [
                "ich fahre jetzt auf dem letzten Wagen und drehe die Bremse, wenn gepfiffen wird.",
                "Nachts sieht man von oben, wo es vorn hell wird. Es ist weiter weg, als ich dachte.",
                "Auf dem Rückweg sind die Wagen voll, und wir halten oft. Ich reiche Wasser durch.",
                "Ein Mann hat mich gefragt, wie alt ich bin. Ich habe sechzehn gesagt.",
                "Ist der Zahlmeister noch böse wegen der Meldung? Grüß den Alten von mir.",
            ],
            braucht=["lebendig"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Ihm schreiben, dass er gut aufgehoben ist",
                    "Auf dem Wagen ist er sicherer als am Gleis.",
                    "Du schreibst, er solle bei den Bremsen bleiben, solange es geht. Die Antwort kommt nach acht Tagen und besteht fast nur aus Lokomotiven. Am Ende steht: Danke, dass du das geschrieben hast.",
                    wirkung={"rueckhalt": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Ihm schreiben, was in den Wagen liegt",
                    "Er fragt nicht danach. Wer nicht fragt, ahnt es schon.",
                    "Du schreibst, dass er weiter Wasser reichen soll, auch wenn niemand antwortet. Die Antwort braucht drei Wochen und ist kurz. Sie endet mit: Ich reiche weiter.",
                    wirkung={"belastung": 1}, verbundenheit=1
                ),
            ]
        ),

        Brief(
            "et_kundige_lager", "kundige", "etappe", [1916, 1917],
            "feldpost", "Feldpost, gestempelt am 30. September",
            "Zwei Seiten, sehr klein geschrieben, damit alles auf den Bogen passt.",
            [
                "Wachdienst am Lager, zwölf Stunden, dann zwölf frei. Ich klage nicht.",
                "Merke dir dreierlei, dann kommst du durch den Winter.",
                "Erstens: Schreib jede Ausgabe am selben Tag ein. Ein Tag Rückstand wird eine Woche.",
                "Zweitens: Wenn du ein Gesuch schreibst, nenne eine Zahl. Sätze ohne Zahl gehen unter.",
                "Drittens, und das ist das wichtigste: Zähl die Leute laut. Dann zählt jemand mit.",
            ],
            braucht=["lebendig"], braucht_fort=True,
            antworten=[
                Briefantwort(
                    "Die drei Punkte an die Schicht weitergeben",
                    "Er hat sie nicht für dich allein aufgeschrieben.",
                    "Du liest sie am Abend in der Schreibstube vor. Beim dritten Punkt wird es still. Zwei Wochen später zählt an der Rampe jemand laut mit, und der Posten dreht sich um.",
                    wirkung={"rueckhalt": 1, "aufmerksamkeit": 1}, verbundenheit=2
                ),
                Briefantwort(
                    "Die Punkte für dich behalten",
                    "Was alle wissen, nützt am Ende niemandem.",
                    "Du schreibst die drei Sätze auf die Innenseite deines Buches. Dein Rückstand bleibt klein, dein Gesuch enthält eine Zahl. Beim Abzählen sagst du nichts, und danach fehlen zwei, die niemand vermisst.",
                    wirkung={"belastung": -1, "rueckhalt": -1}, verbundenheit=-1
                ),
            ]
        ),

        ########################################################################
        ## 1919: Post nach dem Krieg
        ########################################################################

        ## WIRD NIE GEZOGEN (Befund Paket 2, bestaetigt Paket 3, Schritt 2) ######################
        ## Anderer Fall als die drei oben: Dieser Brief war in 1600
        ## Durchgängen KEIN EINZIGES MAL erlaubt, nicht einmal beinahe.
        ## 1919 wird nie ein Ereignis gezogen, weil der Epilog keinen
        ## Bestand hat. post_zustellen läuft aber nur nach einem Ereignis.
        ## Kein Ereignis, keine Post, kein Brief - die Bedingung wird gar
        ## nicht erst geprüft. Das ist eine strukturelle Sperre, kein
        ## Zufall. Sie fällt, sobald der Epilog Ereignisse bekommt
        ## (Paket 4 und 5).
        Brief(
            "e_amt_suche", "amtsperson", "heimat", [1919],
            "amtlich", "Eingegangen am 26. Februar",
            "Ein Formular mit drei Durchschlägen. Zwei davon musst du selbst ausfüllen.",
            [
                "Betrifft: Nachforschung nach vermissten Angehörigen.",
                "Anträge sind bei der Nachweisestelle einzureichen, nicht bei der Gemeinde.",
                "Beizufügen sind: Feldpostnummer, letzte Nachricht mit Datum, zwei Zeugen aus der Truppe.",
                "Die Bearbeitung dauert derzeit sechs bis vierzehn Monate.",
                "Eine Todeserklärung kann frühestens ein Jahr nach der letzten Nachricht beantragt werden.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "erkrankt"], braucht_fort=None,
            antworten=[
                Briefantwort(
                    "Das Formular ausfüllen",
                    "Zwei Zeugen aus der Truppe. Irgendwo wird es sie geben.",
                    "Du füllst aus, was du weißt, und lässt vier Felder leer. Die Antwort kommt im November des nächsten Jahres: Nachforschung ergebnislos abgeschlossen. Das Papier ist grau und dünn, und darunter steht eine Nummer statt einer Unterschrift.",
                    wirkung={"belastung": 1}, verbundenheit=1
                ),
                Briefantwort(
                    "Das Formular liegen lassen",
                    "Sechs bis vierzehn Monate. Du weißt heute schon, was am Ende darauf stehen wird.",
                    "Du legst es zu den anderen Papieren in die Schublade. Zwei Jahre später räumst du die Schublade aus und findest es wieder, ungefaltet und leer. Du wirfst es nicht weg, sondern legst es zurück.",
                    wirkung={}, verbundenheit=0
                ),
            ]
        ),

        ## WIRD NIE GEZOGEN (Befund Paket 2, bestaetigt Paket 3, Schritt 2) ######################
        ## Dieselbe strukturelle Sperre wie bei e_amt_suche: kein Ereignis
        ## im Epilog, also keine Post im Epilog. Auch dieser Brief war in
        ## 1600 Durchgängen kein einziges Mal erlaubt. Er ist zugleich der
        ## letzte Bogen des Frontpfads - dass ausgerechnet er nie ankommt,
        ## ist der sichtbarste Verlust in diesem Bestand.
        ## GILT IN BEIDEN FELDWELTEN, wie f_amt_heimat. Der Entlassungs-
        ## schein ging an jeden Angehörigen des Feldheeres, und dazu
        ## gehörte, wer die vier Jahre am Magazin oder in der Schreibstube
        ## gestanden hat. Kein Satz darin setzt eine Stellung voraus.
        Brief(
            "e_amt_entlassung", "amtsperson", ["front", "etappe"], [1919],
            "amtlich", "Ausgehändigt bei der Entlassung",
            "Der letzte Bogen, den dir jemand vom Heer in die Hand drückt.",
            [
                "Entlassungsschein. Der Inhaber ist mit dem heutigen Tage aus dem Heeresdienst entlassen.",
                "Ausgehändigt: ein Mantel, ein Paar Stiefel, ein Löffel, fünfzig Mark Entlassungsgeld.",
                "Die Waffe ist abzugeben. Ausrüstungsstücke sind Eigentum des Reiches.",
                "Der Entlassene hat sich binnen drei Tagen bei der Meldebehörde seines Wohnortes zu melden.",
                "Für Ansprüche aus Verwundung ist das Versorgungsamt zuständig.",
            ],
            anrede=False,
            braucht=["lebendig", "entfremdet", "erkrankt"], braucht_fort=None,
            antworten=[
                Briefantwort(
                    "Den Schein sorgfältig einstecken",
                    "Ohne dieses Papier bist du auf dem Amt niemand.",
                    "Du faltest ihn und steckst ihn in die Innentasche, dorthin, wo vier Jahre lang das Soldbuch war. Du wirst ihn in den nächsten drei Jahren fünfmal vorlegen müssen, und jedes Mal wird jemand anders die Nummer abschreiben.",
                    wirkung={}, verbundenheit=1
                ),
                Briefantwort(
                    "Zuerst die fünfzig Mark zählen",
                    "Fünfzig Mark. Dafür bekommt man im Frühjahr 1919 nicht viel.",
                    "Du zählst nach, es stimmt. Auf dem Bahnhof kostet ein Brot am Schalter mehr als vor dem Krieg ein Paar Schuhe. Du kaufst nichts und behältst das Geld, bis du zu Hause bist. Dort reicht es für elf Tage.",
                    wirkung={"versorgung": 1}, verbundenheit=0
                ),
            ]
        ),

    ]

    BRIEF_INDEX = {}
    for _brief in BRIEFE:
        BRIEF_INDEX[_brief.kennung] = _brief


################################################################################
## 6. Schicksale wenden
################################################################################
##
## Gewürfelt wird ausschließlich beim Jahreswechsel, nie mitten im Kapitel.
## Dadurch bleibt nachvollziehbar, wann sich etwas verändert hat, und es
## entsteht nicht der Eindruck, eine bestimmte Entscheidung habe jemanden
## das Leben gekostet.

init 3 python:

    def figur_frei(kennung):
        """Für wen überhaupt noch gewürfelt wird."""
        eintrag = figur_zustand(kennung)
        if eintrag is None:
            return False
        return eintrag["zustand"] not in ZUSTAENDE_ENDGUELTIG

    def stufe_faellig(kette, stufe):
        """Prüft alle Bedingungen außer dem Würfel."""
        if aktuelles_jahr < stufe.ab_jahr:
            return False
        ## Nach dem 11. November 1918 fällt niemand mehr im Gefecht und
        ## niemand kommt mehr in Schutzhaft nach dem Belagerungszustand.
        ## Stufen, deren Text den Krieg voraussetzt, tragen bis_jahr 1918.
        if stufe.bis_jahr is not None and aktuelles_jahr > stufe.bis_jahr:
            return False
        if kette.welt and not welt_erlaubt(kette.welt):
            return False
        if stufe.welt and not welt_erlaubt(stufe.welt):
            return False
        eintrag = figur_zustand(kette.figur)
        if eintrag is None:
            return False
        if eintrag["zustand"] in ZUSTAENDE_ENDGUELTIG:
            return False
        if eintrag["zustand"] not in stufe.braucht:
            return False
        if stufe.braucht_fort is not None:
            if bool(eintrag["fort"]) != bool(stufe.braucht_fort):
                return False
        return True

    def stufe_anwenden(kette, stufe):
        """Trägt eine Wendung ein und liefert die Meldung dazu zurück."""
        global schicksals_stand, figuren_verlauf
        eintrag = figur_zustand(kette.figur)
        war_fort = bool(eintrag["fort"])

        neuer_zustand = welttext(stufe.zustand) if stufe.zustand is not None else None
        neu_fort = welttext(stufe.fort) if stufe.fort is not None else None
        neuer_grund = welttext(stufe.grund) if stufe.grund is not None else None

        figur_setzen(
            kette.figur,
            zustand=neuer_zustand,
            fort=neu_fort,
            grund=neuer_grund,
            verbundenheit=stufe.verbundenheit,
            stufe=kette.kennung,
        )

        if stufe.wirkung:
            zustand_aendern(stufe.wirkung)

        stand = dict(schicksals_stand)
        stand[kette.kennung] = stand.get(kette.kennung, 0) + 1
        schicksals_stand = stand

        zeilen = welttext(stufe.meldung)
        jetzt = figur_zustand(kette.figur)

        figuren_verlauf = figuren_verlauf + [{
            "jahr": aktuelles_jahr,
            "figur": kette.figur,
            "kette": kette.kennung,
            "zustand": jetzt["zustand"],
        }]

        ## Wer bei dir ist, dessen Wendung siehst du selbst. Wer fort ist,
        ## von dem erfährst du es erst durch Post. Bis dahin bleibt der
        ## Stand, den du kennst, unverändert.
        ## Wer gerade erst fortgegangen ist, gilt als eben noch erreicht.
        ## Sonst begänne der Verfall der Verbundenheit am Tag der Trennung.
        if neu_fort is True and not war_fort:
            figur_post_vermerken(kette.figur)

        if war_fort:
            nachricht_vormerken(kette.figur, zeilen, jetzt["zustand"])
            return None

        figur_setzen(kette.figur, bekannt=jetzt["zustand"])
        return {
            "figur": kette.figur,
            "name": figur_name(kette.figur),
            "titel": kette.titel,
            "zeilen": zeilen,
            "zustand": zustand_anzeige(jetzt["zustand"]),
            "stufe": ZUSTAND_STUFE.get(jetzt["zustand"], 0),
        }

    def entfremdung_pruefen():
        """Wer lange nichts hört und wenig gibt, wird fremd.

        Das ist die einzige Veränderung im ganzen Paket, die am Verhalten
        der Spielfigur hängt. Sie kostet niemandem das Leben.
        """
        meldungen = []
        for kennung in FIGUREN_REIHENFOLGE:
            eintrag = figur_zustand(kennung)
            if eintrag is None or not figur_frei(kennung):
                continue
            if eintrag["zustand"] != "lebendig" or not eintrag["fort"]:
                continue
            if eintrag["verbundenheit"] > VERBUNDENHEIT_SCHWEIGEN:
                continue
            if aktuelles_jahr - eintrag["post_jahr"] < 2:
                continue
            if renpy.random.randint(1, 100) > 45:
                continue
            figur_setzen(kennung, zustand="entfremdet", bekannt="entfremdet")
            meldungen.append({
                "figur": kennung,
                "name": figur_name(kennung),
                "titel": "Es kommt nichts mehr",
                "zeilen": welttext({
                    "front": [
                        "Von ihm ist seit über einem Jahr keine Zeile gekommen.",
                        "Du hast zuletzt selbst nicht geantwortet, und danach war es einfach vorbei.",
                        "Ein Brief geht nicht verloren, weil die Post schlecht ist. Er geht verloren, weil niemand ihn schreibt.",
                    ],
                    "etappe": [
                        "Von ihm ist seit über einem Jahr keine Zeile gekommen.",
                        "Du hast zuletzt selbst nicht geantwortet, und danach war es einfach vorbei.",
                        "Durch deine Hände geht jeden Tag Post. Seine war nie dabei.",
                    ],
                    "heimat": [
                        "Seit über einem Jahr ist nichts mehr gekommen.",
                        "Du hast zuletzt selbst nicht geantwortet, und danach war es einfach vorbei.",
                        "Es ist nichts geschehen. Genau das ist es: Es ist nichts geschehen.",
                    ],
                }),
                "zustand": zustand_anzeige("entfremdet"),
                "stufe": ZUSTAND_STUFE.get("entfremdet", 2),
            })
        return meldungen

    def verbundenheit_verfallen():
        """Wer fort ist und ein Jahr lang nicht schreibt, rückt weg."""
        for kennung in FIGUREN_REIHENFOLGE:
            eintrag = figur_zustand(kennung)
            if eintrag is None or not figur_frei(kennung):
                continue
            if not eintrag["fort"]:
                continue
            if aktuelles_jahr - eintrag["post_jahr"] >= 2:
                figur_setzen(kennung, verbundenheit=-1)

    def schicksale_wuerfeln():
        """Ein Durchgang über alle Ketten. Liefert die sichtbaren Meldungen."""
        global post_im_jahr
        post_im_jahr = 0
        meldungen = []

        reihenfolge = list(SCHICKSALE)
        renpy.random.shuffle(reihenfolge)

        for kette in reihenfolge:
            stelle = schicksals_stand.get(kette.kennung, 0)
            if stelle >= len(kette.stufen):
                continue
            stufe = kette.stufen[stelle]
            if not stufe_faellig(kette, stufe):
                continue
            chance = welttext(stufe.chance)
            if not isinstance(chance, int):
                chance = 20
            if renpy.random.randint(1, 100) > chance:
                continue
            meldung = stufe_anwenden(kette, stufe)
            if meldung is not None:
                meldungen.append(meldung)

        verbundenheit_verfallen()
        meldungen.extend(entfremdung_pruefen())
        return meldungen


################################################################################
## 7. Post: was ankommt und wann
################################################################################
##
## Unregelmäßig heißt hier nicht beliebig. Drei Regeln halten den Zufall in
## der Spur, damit er sich nicht wie ein Fehler anfühlt:
##
##   POST_ABSTAND      nie zwei Briefe unmittelbar hintereinander,
##   POST_SPAETESTENS  nach so vielen Ereignissen kommt sicher etwas,
##   POST_JE_JAHR      mehr als drei Sendungen im Jahr gibt es nicht.
##
## Wartende Nachrichten über eine Wendung haben Vorrang vor gewöhnlichen
## Briefen und erhöhen zusätzlich die Chance, dass überhaupt Post kommt.

init 3 python:

    ## Weltprüfung der Post ####################################################
    ##
    ## Seit Paket 2, Schritt 1. Eine Wendung wird beim JAHRESWECHSEL
    ## eingereiht, ihre Zeilen werden dabei mit welttext() aufgelöst.
    ## Zugestellt wird sie irgendwann später. Zwischen beidem lag bisher
    ## keine Prüfung: Wer den Pfad wechselte, machte einen Umschlag auf,
    ## dessen Inhalt für eine andere Welt geschrieben war.
    ##
    ## Heute kann das nicht vorkommen, weil aktueller_pfad nach dem
    ## Einstieg feststeht. Genau deshalb ist jetzt der richtige Zeitpunkt,
    ## die Prüfung einzuziehen: Sie kostet nichts und fängt den Fall ab,
    ## sobald ein späteres Paket jemanden zwischen den Pfaden bewegt.
    ##
    ## Verworfen wird nichts. Eine Sendung aus einer fremden Welt bleibt
    ## liegen, bis sie passt, und steht bis dahin im Analysemodus.

    postwelt_protokoll = []

    def postwelt_merken(ort, kennung, gemeint, jetzt):
        """Hält fest, dass eine Sendung nicht zur eigenen Welt passt."""
        postwelt_protokoll.append({
            "ort": ort,
            "kennung": str(kennung),
            "gemeint": str(gemeint),
            "jetzt": str(jetzt),
            "pfad": str(aktueller_pfad),
            "jahr": aktuelles_jahr,
        })

    def nachricht_vormerken(figur, zeilen, zustand):
        global post_offen
        art = "amtlich" if zustand in ("gefallen", "vermisst", "verhaftet") else "nachricht"
        post_offen = post_offen + [{
            "figur": figur,
            "zeilen": list(zeilen),
            "zustand": zustand,
            "art": art,
            ## Die Welt, in der diese Zeilen geschrieben wurden.
            "welt": briefwelt(),
        }]

    ## Wie eine Nachricht ankommt, ist in jeder Welt eine andere Geste.
    ## In der Etappe kommt sie über denselben Tisch wie alles andere -
    ## und die private Post hat die Prüfstelle schon gelesen, in der man
    ## selbst sitzt.
    NACHRICHT_KOPF = {
        "amtlich": {
            "front": "Der Feldwebel ruft dich beiseite und hat einen Bogen in der Hand.",
            "etappe": "Der Zahlmeister legt dir einen Bogen hin und geht danach hinaus.",
            "heimat": "Ein Umschlag mit dem Stempel der Behörde. Du machst ihn im Stehen auf.",
        },
        "nachricht": {
            "front": "Ein Brief, aber nicht von ihm. Die Handschrift auf dem Umschlag kennst du nicht.",
            "etappe": "Ein Brief mit fremder Handschrift, und er ist schon durch die Prüfstelle gegangen.",
            "heimat": "Ein Brief in einer fremden Handschrift. Der Absender steht klein auf der Rückseite.",
        },
    }

    def nachricht_passt(eintrag):
        """Gehört diese wartende Wendung in die Welt, in der du gerade bist?

        Ältere Einträge tragen kein welt-Feld. Sie gelten als passend:
        Sie stammen aus einem Spielstand, der vor dieser Prüfung entstand.
        """
        return welt_erlaubt(eintrag.get("welt"))

    def brief_aus_nachricht(eintrag):
        """Baut aus einer wartenden Wendung eine zustellbare Sendung."""
        kopf = NACHRICHT_KOPF.get(eintrag["art"], NACHRICHT_KOPF["nachricht"])
        ## Zweite Prüfung, kurz vor dem Aufmachen. Die erste steht in
        ## brief_ziehen(); diese hier fängt jeden anderen Weg ab, auf dem
        ## eine Wendung hierher gelangen könnte.
        if not nachricht_passt(eintrag):
            postwelt_merken("brief_aus_nachricht", eintrag["figur"],
                            eintrag.get("welt"), briefwelt())
        return {
            "kennung": "nachricht_" + eintrag["figur"],
            "figur": eintrag["figur"],
            "art": eintrag["art"],
            "marke": POST_MARKE.get(eintrag["art"], "Post"),
            "absender": figur_name(eintrag["figur"]),
            "zusatz": figur_zusatz(eintrag["figur"]),
            "datum": "Ohne Datum",
            "kopf": welttext(kopf),
            "zeilen": list(eintrag["zeilen"]),
            "antworten": [],
            "wirkung": {},
            "nachricht": True,
            "zustand": eintrag["zustand"],
            "welt": eintrag.get("welt", briefwelt()),
        }

    def brief_erlaubt(vorlage):
        if not welt_erlaubt(vorlage.welt):
            return False
        if aktuelles_jahr not in vorlage.jahre:
            return False
        if vorlage.kennung in post_gelesen:
            return False
        eintrag = figur_zustand(vorlage.figur)
        if eintrag is None:
            return False
        if eintrag["zustand"] not in vorlage.braucht:
            return False
        if vorlage.braucht_fort is not None:
            if bool(eintrag["fort"]) != bool(vorlage.braucht_fort):
                return False
        if eintrag["verbundenheit"] < vorlage.verbundenheit_ab:
            return False
        ## Wer sich abgewendet hat, schreibt keine persönlichen Briefe mehr.
        ## Amtliche Post und Fundstücke kommen trotzdem.
        if vorlage.art in ("feldpost", "heimatpost"):
            if eintrag["verbundenheit"] <= VERBUNDENHEIT_SCHWEIGEN:
                return False
        return True

    def briefe_verfuegbar():
        return [vorlage for vorlage in BRIEFE if brief_erlaubt(vorlage)]

    def brief_aufbereiten(vorlage):
        zeilen = list(vorlage.zeilen)
        if vorlage.anrede:
            zeilen = [anrede_text()] + zeilen
        antworten = []
        for antwort in vorlage.antworten:
            antworten.append({
                "titel": antwort.titel,
                "beschreibung": antwort.beschreibung,
            })
        return {
            "kennung": vorlage.kennung,
            "figur": vorlage.figur,
            "art": vorlage.art,
            "marke": POST_MARKE.get(vorlage.art, "Post"),
            "absender": figur_name(vorlage.figur),
            "zusatz": figur_zusatz(vorlage.figur),
            "datum": vorlage.datum,
            "kopf": vorlage.kopf,
            "zeilen": zeilen,
            "antworten": antworten,
            "wirkung": dict(vorlage.wirkung),
            "nachricht": False,
            "zustand": None,
            ## Seit Paket 2, Schritt 1: Jede Sendung trägt ihre Welt mit
            ## sich, damit die Zustellung sie prüfen kann.
            "welt": vorlage.welt,
        }

    def post_chance_heute(dringend):
        chance = POST_CHANCE.get(aktuelles_jahr, 25)
        if dringend:
            chance = chance + 30
        return chance

    def brief_ziehen():
        """Entscheidet, ob heute Post kommt, und wenn ja, welche."""
        if not figuren_zustand:
            return None
        if post_im_jahr >= POST_JE_JAHR:
            return None

        ## DER EPILOG HAT SEINE EIGENE REGEL. Seit Paket 5, Schritt 2,
        ## Teil C2, und zwar aus einer Messung.
        ##
        ## Der Abstand von zwei Ereignissen ist in den Kriegsjahren
        ## richtig: Post soll ein Ereignis bleiben und nicht zur Beilage
        ## werden. 1919 gibt es aber nur EINE Ziehung im kurzen und ZWEI
        ## im langen Verlauf. Wer im Dezember 1918 einen Brief bekommen
        ## hat, kann den Epilog damit gar nicht mehr erreichen.
        ##
        ## Dahinter liegen die beiden letzten Bogen des ganzen Spiels:
        ## der Suchantrag bei der Nachweisestelle und der
        ## Entlassungsschein. Gemessen über 24000 Durchgänge kam der
        ## Entlassungsschein bei geltendem Abstand in 32 Fällen an, bei
        ## rund 540 Durchgängen, die 1919 auf Front oder Etappe
        ## erreichen - also in etwa jedem sechzehnten.
        ##
        ## Nicht angetastet sind POST_CHANCE und POST_JE_JAHR. Der
        ## Engpass war nie die Wahrscheinlichkeit, sondern die Zahl der
        ## Ziehungen, die für den Abstand nicht reicht.
        ##
        ## PAKET 8, SCHRITT 2.5: Bei offener Schuld aus dem letzten Kapitel
        ## reicht EINE Ziehung Abstand statt zweier. Der Grund ist derselbe
        ## wie im Epilog: Ein Kapitel hat nach KAPITEL_ZIEHUNGEN ein bis
        ## drei Ziehungen, und mit dem vollen Abstand käme die Nachziehregel
        ## in den kurzen Kapiteln nie zum Zuge. Zwei Briefe unmittelbar
        ## hintereinander bleiben ausgeschlossen.
        mindestabstand = 1 if post_schuld else POST_ABSTAND
        if aktuelles_jahr < EPILOG_JAHR and post_zaehler < mindestabstand:
            return None

        ## Die erste wartende Wendung, die in diese Welt gehört. Eine, die
        ## nicht passt, bleibt liegen und blockiert die Warteschlange
        ## nicht - sonst käme überhaupt keine Post mehr.
        dringend = None
        for eintrag in post_offen:
            if nachricht_passt(eintrag):
                dringend = eintrag
                break

        auswahl = briefe_verfuegbar()

        if dringend is None and not auswahl:
            return None

        chance = post_chance_heute(dringend is not None)
        if post_zaehler >= POST_SPAETESTENS:
            chance = 100
        ## PAKET 8, SCHRITT 2.5: Wer im letzten Kapitel keine Post hatte,
        ## bekommt sie hier ohne Wurf.
        if post_schuld:
            chance = 100
        if renpy.random.randint(1, 100) > chance:
            return None

        if dringend is not None:
            return brief_aus_nachricht(dringend)

        vorlage = gewichtet_ziehen(auswahl, lambda eintrag: eintrag.gewicht)
        return brief_aufbereiten(vorlage)

    def brief_zustellen(brief):
        """Trägt ein, dass die Sendung angekommen ist."""
        global post_gelesen, post_offen, post_zaehler, post_letzter, post_im_jahr
        global post_schuld

        ## Letzte Weltprüfung, an der Zustellung selbst. Sie greift auch
        ## für gewöhnliche Briefe, deren welt aus dem Bestand kommt.
        gemeint = brief.get("welt")
        if not welt_erlaubt(gemeint):
            postwelt_merken("brief_zustellen", brief["kennung"], gemeint, briefwelt())

        post_zaehler = 0
        post_letzter = brief["kennung"]
        post_im_jahr = post_im_jahr + 1
        ## Bezahlt wird bei der Zustellung, nicht beim Ziehen (Schritt 2.5).
        post_schuld = False
        figur_post_vermerken(brief["figur"])

        if brief["nachricht"]:
            ## Entfernt wird genau die Wendung, die eben aufgemacht wurde:
            ## dieselbe Figur UND dieselbe Welt. Ohne die zweite Bedingung
            ## verschwände eine wartende Sendung aus einer anderen Welt.
            rest = []
            entfernt = False
            for eintrag in post_offen:
                if (not entfernt
                        and eintrag["figur"] == brief["figur"]
                        and nachricht_passt(eintrag)):
                    entfernt = True
                    continue
                rest.append(eintrag)
            post_offen = rest
            figur_setzen(brief["figur"], bekannt=brief["zustand"])
        else:
            post_gelesen = post_gelesen + [brief["kennung"]]

        if brief["wirkung"]:
            zustand_aendern(brief["wirkung"])

    def brief_beantworten(brief, stelle):
        """Führt die gewählte Antwort aus und liefert den Ausgangstext."""
        if stelle is None:
            return None
        vorlage = BRIEF_INDEX.get(brief["kennung"])
        if vorlage is None:
            return None
        if stelle < 0 or stelle >= len(vorlage.antworten):
            return None
        antwort = vorlage.antworten[stelle]
        zustand_aendern(antwort.wirkung)
        if antwort.verbundenheit:
            figur_setzen(brief["figur"], verbundenheit=antwort.verbundenheit)
        protokoll_eintragen("brief_" + brief["kennung"], antwort.titel)
        return {
            "titel": antwort.titel,
            "ausgang": antwort.ausgang,
        }


################################################################################
## 8. Auswertung: der Verbleib im Lebenslauf
################################################################################
##
## Der Lebenslauf von 1919 bekommt einen zusätzlichen Eintrag: einen Absatz
## darüber, was aus den fünf geworden ist. Er steht bewusst nach dem
## Kriegsende und vor Versailles, weil er zum Privatleben gehört und nicht
## zur großen Politik.
##
## Der Absatz sagt die Wahrheit, auch dort, wo die Spielfigur sie nie
## erfahren hat. In diesem Fall wird genau das dazugesagt. Ein Ende, das
## verschweigt, was der Spieler nicht wissen konnte, wäre unehrlich; ein
## Ende, das so tut, als hätte man alles erfahren, wäre es auch.

init 3 python:

    VERBLEIB = {

        "lebendig_da": {
            "front": " hat den Krieg überstanden. Am Bahnhof habt ihr euch die Hand gegeben, ohne Adressen auszutauschen.",
            "etappe": " hat den Krieg überstanden. Bei der Auflösung habt ihr die Bücher verbrannt und euch die Hand gegeben.",
            "heimat": " wohnt im Frühjahr 1919 noch immer im selben Haus. Ihr grüßt euch auf der Treppe wie vor dem Krieg.",
        },
        "lebendig_fort": {
            "front": " ist irgendwo im Reich entlassen worden. Der letzte Brief kam im Januar 1919, mit einer Adresse, die es nicht mehr gibt.",
            "etappe": " ist mit dem letzten Transport heimgefahren. Eine Karte kam im Januar, ohne Absender.",
            "heimat": " ist nicht zurückgekommen, sondern dort geblieben, wo Arbeit war. Zweimal im Jahr kommt eine Karte.",
        },
        "verwundet": {
            "front": " trägt den steifen Arm bis an sein Lebensende. Beim Versorgungsamt bekommt er zwei Drittel Rente zugesprochen, nach dem dritten Gutachten.",
            "etappe": " trägt vom Fliegerangriff eine Narbe am Bein. Beim Versorgungsamt ist der dritte Antrag noch offen.",
            "heimat": " ist wieder auf den Beinen und war es nie ganz. Was der Krieg gekostet hat, sieht man erst, wenn sie eine Treppe steigt.",
        },
        "erkrankt": {
            "front": " liegt im Frühjahr 1919 noch immer im Lazarett. Die Lunge, sagen sie, sei von der Grippe geblieben.",
            "etappe": " hustet seit dem Herbst 1918 und arbeitet trotzdem weiter. Die Grippe, sagen sie, sei in der Baracke geblieben.",
            "heimat": " hustet seit dem Winter 1918 und hört nicht damit auf. Der Arzt spricht von Schwindsucht und schreibt Kräftigung auf.",
        },
        "vermisst": {
            "front": " gilt weiter als vermisst. Eine Todeserklärung darfst du frühestens ein Jahr nach der letzten Nachricht beantragen.",
            "etappe": " steht bis heute in der Liste der Vermissten. Du hast sie selbst geführt und den Namen nie streichen können.",
            "heimat": " ist verschollen. Die Nachweisestelle antwortet 1921, dass die Nachforschung ergebnislos abgeschlossen ist.",
        },
        "verhaftet": {
            "front": " ist im Dezember 1918 aus der Festungshaft entlassen worden, zusammen mit allen anderen. Das Urteil steht trotzdem in seinen Papieren.",
            "etappe": " ist im Dezember 1918 aus der Haft entlassen worden. Der Vermerk über die Bücher steht weiter in den Papieren.",
            "heimat": " ist im November 1918 freigekommen. Die Akte über sie ist geblieben und liegt jetzt bei der Polizeibehörde.",
        },
        "entfremdet": {
            "front": " lebt. Mehr weißt du nicht, und mehr willst du seit einer Weile auch nicht wissen.",
            "etappe": " lebt. Ihr habt zwei Jahre nebeneinander geschrieben und danach kein Wort mehr gewechselt.",
            "heimat": " wohnt zwei Türen weiter und redet nicht mehr mit dir. Angefangen hat das mit nichts, und es hört mit nichts auf.",
        },
        "gefallen": {
            "front": " ist gefallen. Auf der Tafel am Denkmal steht sein Name zwischen zwei anderen, die du auch gekannt hast.",
            ## Der Satz gilt fuer alle fuenf Rollen, auch fuer die
            ## Gegenseite. Deshalb nennt er keinen Bogen, den die
            ## Spielerin ausgefuellt haette, sondern nur den Tisch, ueber
            ## den ohnehin alles ging.
            "etappe": " ist gefallen. Sein Name ist über deinen Tisch gegangen wie tausend andere.",
            "heimat": " ist gestorben, bevor der Krieg zu Ende war. Auf dem Denkmal steht dieser Name nicht: Es zählt nur, wer im Feld geblieben ist.",
        },
    }

    ## Zusatzsatz, wenn du erst spät oder nie erfahren hast, was geschehen ist.
    VERBLEIB_UNGEWISS = " Erfahren hast du es erst, als der Krieg längst vorbei war."

    ## Zusatzsatz nach der Verbundenheit. Nur für Lebende.
    VERBLEIB_NAEHE = {
        "eng": " Ihr schreibt euch bis heute.",
        "abgerissen": " Geschrieben habt ihr euch zuletzt vor Jahren.",
    }

    def verbleib_schluessel(eintrag):
        zustand = eintrag["zustand"]
        if zustand == "lebendig":
            return "lebendig_fort" if eintrag["fort"] else "lebendig_da"
        return zustand

    def verbleib_satz(kennung):
        eintrag = figur_zustand(kennung)
        if eintrag is None:
            return ""
        schluessel = verbleib_schluessel(eintrag)
        vorlage = VERBLEIB.get(schluessel, VERBLEIB["lebendig_da"])
        satz = figur_name(kennung) + welttext(vorlage)

        if eintrag["bekannt"] != eintrag["zustand"] and eintrag["zustand"] != "lebendig":
            satz = satz + VERBLEIB_UNGEWISS

        if eintrag["zustand"] in ("lebendig", "verwundet", "erkrankt"):
            name, _stufe = verbundenheit_anzeige(eintrag["verbundenheit"])
            if name in VERBLEIB_NAEHE:
                satz = satz + VERBLEIB_NAEHE[name]

        return satz

    def nebenfiguren_absatz():
        saetze = []
        for kennung in FIGUREN_REIHENFOLGE:
            satz = verbleib_satz(kennung)
            if satz:
                saetze.append(satz)
        return " ".join(saetze)

    def nebenfiguren_bilanz():
        """Zahlen für den Analysemodus."""
        tot = 0
        fort = 0
        nah = 0
        for kennung in FIGUREN_REIHENFOLGE:
            eintrag = figur_zustand(kennung)
            if eintrag is None:
                continue
            if eintrag["zustand"] in ZUSTAENDE_ENDGUELTIG:
                tot = tot + 1
            elif eintrag["fort"]:
                fort = fort + 1
            if eintrag["verbundenheit"] >= 7:
                nah = nah + 1
        return {"tot": tot, "fort": fort, "nah": nah}

    ## Der Eintrag hängt sich an die vorhandene Zusammenstellung an, statt
    ## sie zu ersetzen. kapitel.rpy bleibt dadurch unverändert.
    ende_zusammenstellen_grundlage = ende_zusammenstellen

    def ende_zusammenstellen():
        daten = ende_zusammenstellen_grundlage()
        absatz = nebenfiguren_absatz()
        if absatz:
            eintraege = list(daten["eintraege"])
            eintrag = {
                "jahr": 1919,
                "marke": "Was aus den anderen geworden ist",
                "text": absatz,
                "quelle": "Nebenfiguren",
            }
            ## Stelle 2 liegt hinter Kriegsende und Ausgang. Weil sort()
            ## stabil ist, bleibt der Absatz damit auch dann vor Lage und
            ## Versailles, wenn alle drei das Jahr 1919 tragen.
            eintraege.insert(min(2, len(eintraege)), eintrag)
            eintraege.sort(key=lambda e: e["jahr"])
            daten["eintraege"] = eintraege
        return daten


################################################################################
## 9. Sprachprüfung erweitern
################################################################################
##
## herkunft.rpy prüft Ereignisse und Szenen, kapitel.rpy hat Kapitel- und
## Endtexte ergänzt. Ab hier laufen auch sämtliche Brieftexte, Meldungen und
## Verbleibsätze durch dieselbe Liste. Das Werkzeug muss leer bleiben.

init 4 python:

    sprachpruefung_vor_paket4 = sprachpruefung_durchfuehren

    def brieftexte_sammeln():
        bestand = []
        for vorlage in BRIEFE:
            texte = [vorlage.kopf, vorlage.datum]
            texte.extend(vorlage.zeilen)
            for antwort in vorlage.antworten:
                texte.append(antwort.titel)
                texte.append(antwort.beschreibung)
                texte.append(antwort.ausgang)
            bestand.append(("Brief " + vorlage.kennung, [t for t in texte if t]))
        return bestand

    def schicksalstexte_sammeln():
        bestand = []
        for kette in SCHICKSALE:
            texte = [kette.titel]
            for stufe in kette.stufen:
                texte.extend(texte_sammeln(stufe.meldung))
                texte.extend(texte_sammeln(stufe.grund))
            bestand.append(("Schicksal " + kette.kennung, [t for t in texte if t]))
        for schluessel, vorlage in VERBLEIB.items():
            bestand.append(("Verbleib " + schluessel, texte_sammeln(vorlage)))
        bestand.append(("Verbleib Zusatz", [VERBLEIB_UNGEWISS] + list(VERBLEIB_NAEHE.values())))
        for art, vorlage in NACHRICHT_KOPF.items():
            bestand.append(("Nachricht " + art, texte_sammeln(vorlage)))
        return bestand

    def sprachpruefung_durchfuehren():
        funde = sprachpruefung_vor_paket4()
        for ort, texte in brieftexte_sammeln() + schicksalstexte_sammeln():
            for satz in texte:
                klein = satz.lower()
                for begriff, begruendung in TABU_BEGRIFFE:
                    if begriff.lower() in klein:
                        funde.append(("Tabu", ort, begriff, begruendung, satz[:120]))
                for begriff, begruendung in PRUEF_BEGRIFFE:
                    if begriff.lower() in klein:
                        funde.append(("Prüfen", ort, begriff, begruendung, satz[:120]))
        return funde


################################################################################
## 10. Zustandsvariablen
################################################################################

default figuren_zustand = {}
default schicksals_stand = {}
default figuren_verlauf = []

default post_offen = []
default post_gelesen = []
default post_zaehler = 0
default post_letzter = None
default post_im_jahr = 0

## PAKET 8, SCHRITT 2.5: offene Schuld aus dem letzten Kapitel. Gesetzt
## wird sie von rhythmus_kapitel_abschliessen() in minispiele.rpy — die
## Regel gilt für Einlagen und Post gemeinsam und wird deshalb an einer
## einzigen Stelle gebucht.
default post_schuld = False

default brief_aktuell = None
default brief_wahl = None
default brief_folge = None
default schicksals_meldungen = []
default briefprobe_wahl = None
default briefprobe_stelle = 0


################################################################################
## 11. Stile und Bildschirme
################################################################################
##
## Alles wird mit der Maus bedient. Es gibt in dieser Datei keine einzige
## key-Anweisung. Lange Briefe laufen in einem viewport, der sich mit Rad
## und Ziehen bewegen lässt; eine Taste ist dafür nirgends nötig.

init offset = -1

## Stile #######################################################################

style brief_marke is default:
    font SCHRIFT_TITEL
    size 20
    bold True
    color FARBE_AKZENT
    kerning 2.2

## ACHTUNG, DER NAME TAEUSCHT: Das ist kein Aufdruck, sondern die kleine
## kursive Zeile mit dem Datum eines Briefes (merkbuch.rpy:1179). Die drei
## echten Aufdrucke im Projekt heissen karte_stempel, bogen_stempel und
## post_stempel_text; sie sind fett, gesperrt und stehen seit Paket 8 in
## SCHRIFT_SCHMAL. Dieser hier bleibt bewusst, wie er ist.
##
## Umbenannt wird er trotzdem nicht (AUFGEFALLEN 82). Der Name steht in
## den Kopplungen der Verfassung und an drei Stellen im Code; ihn zu
## aendern kostet vier Eingriffe und bringt nichts, was dieser Kommentar
## nicht auch leistet. Regel 9 raet in genau solchen Faellen zur Ruhe.

style brief_stempel is default:
    size 19
    italic True
    color FARBE_LINIE

style brief_absender is default:
    font SCHRIFT_TITEL
    size 30
    bold True
    color FARBE_TINTE

style brief_zusatz is default:
    size 19
    italic True
    color FARBE_LINIE

style brief_kopf is default:
    size 24
    italic True
    color FARBE_TINTE_MATT
    line_spacing 6

style brief_zeile is default:
    font SCHRIFT_DOKUMENT
    size 28
    color FARBE_TINTE
    line_spacing 9

style brief_antwort_titel is default:
    font SCHRIFT_TITEL
    size 26
    bold True
    color FARBE_TINTE

style brief_antwort_text is default:
    size 22
    color FARBE_TINTE_MATT
    line_spacing 5

style figuren_titel is default:
    font SCHRIFT_TITEL
    size 21
    bold True
    color FARBE_TINTE_MATT
    kerning 1.2

style figuren_name is default:
    font SCHRIFT_TITEL
    size 23
    bold True
    color FARBE_TINTE

style figuren_lage is default:
    size 20
    color FARBE_TINTE_MATT

style figuren_ort is default:
    size 18
    italic True
    color FARBE_LINIE

style schicksal_titel is default:
    font SCHRIFT_TITEL
    size 30
    bold True
    color FARBE_TINTE

style schicksal_zeile is default:
    size 27
    color FARBE_TINTE
    line_spacing 9

style brief_pruefung is default:
    size 16
    color FARBE_LINIE

## Die Figurenleiste ###########################################################
##
## Zeigt ausschließlich, was die Spielfigur wissen kann. Wer fort ist und
## dessen Nachricht noch unterwegs ist, steht hier weiter so da, wie er
## zuletzt bekannt war. Das ist Absicht.

## Antwortkarte ################################################################

screen briefantwort_karte(antwort, stelle):

    button:
        xysize (560, 196)
        padding (28, 24)
        background rahmen_doppelt_schatten(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)
        hover_background rahmen_doppelt_schatten("#fffdf8", FARBE_AKZENT, FARBE_AKZENT, schattenfarbe="#15130f38")
        action Return(stelle)

        vbox:
            xsize 504
            yalign 0.5
            spacing 12

            text antwort["titel"] style "brief_antwort_titel" xsize 504

            add Solid(FARBE_AKZENT, xsize=54, ysize=3)

            text antwort["beschreibung"] style "brief_antwort_text" xsize 504

## Der Brief ###################################################################

screen brief_bildschirm(brief):

    add Solid(FARBE_PAPIER)

    use zustandskopf(ort_text())

    vbox:
        xalign 0.5
        ypos 236
        spacing 26

        hbox:
            xalign 0.5

            ## Der Bogen steht seit Paket 4.1 allein. Wer einen Brief liest,
            ## soll nichts anderes tun. Der Vermerk unter dem Absender ist
            ## der Satz, den der Spieler sich selbst notiert hat.
            ##
            ## Paket 7, Schritt 1: Der Umschlag geht auf - die Lasche klappt,
            ## der Bogen fährt heraus. Beides steckt in einem Aufruf.
            frame:
                xsize 1400
                ysize 520
                padding (46, 30)
                background rahmen_schatten(FARBE_PAPIER_HELL, FARBE_AKZENT, 3)
                at umschlag_oeffnet(bewegungszeit(0.4))

                vbox:
                    xsize 1308
                    spacing 12

                    hbox:
                        xsize 1308
                        text brief["marke"].upper() style "brief_marke" yalign 1.0
                        text brief["datum"] style "brief_stempel" xalign 1.0 yalign 1.0

                    add Solid(FARBE_LINIE_FEIN, xsize=1308, ysize=1)

                    hbox:
                        spacing 16
                        text brief["absender"] style "brief_absender" yalign 1.0
                        text brief["zusatz"] style "brief_zusatz" yalign 1.0
                        if persistent.analysemodus:
                            text brief["kennung"] style "brief_pruefung" yalign 1.0

                    $ eigener_vermerk = merkbuch_notiz(brief["figur"])

                    if eigener_vermerk:
                        text ("„" + eigener_vermerk + "“") style "merkbuch_notiz_text" xsize 1308

                    text brief["kopf"] style "brief_kopf" xsize 1308

                    add Solid(FARBE_AKZENT, xsize=90, ysize=2)

                    viewport:
                        xsize 1308
                        ysize 262
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        vbox:
                            xsize 1264
                            spacing 12

                            for satz in brief["zeilen"]:
                                text satz style "brief_zeile" xsize 1264

        ## Antworten. Gibt es keine, führt ein einzelner Knopf weiter.
        if brief["antworten"]:
            hbox:
                xalign 0.5
                spacing 40
                for stelle, antwort in enumerate(brief["antworten"]):
                    use briefantwort_karte(antwort, stelle)
        else:
            textbutton "Weiter":
                xalign 0.5
                style_prefix "weiter"
                action Return(None)

    use eckmenue()
    use werthinweis()

## Was aus der Antwort geworden ist ############################################

screen brief_ausgang_bildschirm(brief, folge):

    add Solid(FARBE_PAPIER)

    use zustandskopf(ort_text())

    fixed:
        xalign 0.5
        ypos 240
        xsize 1400
        ysize 800

        vbox:
            align (0.5, 0.5)
            spacing 56

            frame:
                xalign 0.5
                xsize 1280
                padding (72, 46)
                background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

                vbox:
                    xsize 1136
                    spacing 22

                    text "Deine Antwort" style "ausgang_marke" xalign 0.5

                    text folge["titel"] style "ausgang_titel" xalign 0.5 xsize 1136

                    add Solid(FARBE_AKZENT, xsize=180, ysize=3) xalign 0.5

                    text folge["ausgang"] style "ausgang_text" xalign 0.5 xsize 1136

                    if persistent.analysemodus:
                        hbox:
                            xalign 0.5
                            spacing 28
                            for schluessel in WERTE_REIHENFOLGE:
                                if letzte_aenderungen.get(schluessel, 0) != 0:
                                    text WERT_BEZEICHNUNG[schluessel] + " " + ("+" + str(letzte_aenderungen[schluessel]) if letzte_aenderungen[schluessel] > 0 else str(letzte_aenderungen[schluessel])) style "analyse_wert"

            textbutton "Weiter":
                xalign 0.5
                style_prefix "weiter"
                action Return()

    use eckmenue()
    use werthinweis()

## Was sich im Jahreswechsel verändert hat #####################################

screen schicksal_bildschirm(meldungen):

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    hbox:
        xalign 0.5
        ypos 70
        spacing 40

        vbox:
            xsize 1400
            spacing 18

            text "Seit dem letzten Jahr" style "abschnitt_titel" size 46 text_align 0.0 xalign 0.0

            add Solid(FARBE_AKZENT, xsize=220, ysize=3)

            text "Nicht alles hängt an dir. Das hier ist geschehen, während du getan hast, was du tun konntest." style "abschnitt_text" size 22 xsize 1120

            viewport:
                xsize 1400
                ysize 750
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    xsize 1356
                    spacing 22

                    for meldung in meldungen:

                        frame:
                            xsize 1356
                            padding (34, 26)
                            background rahmen(FARBE_PAPIER_HELL, FARBE_LINIE_FEIN, 2)

                            vbox:
                                xsize 1288
                                spacing 12

                                hbox:
                                    spacing 16
                                    text meldung["name"] style "schicksal_titel" yalign 1.0
                                    text meldung["zustand"] style "brief_zusatz" yalign 1.0
                                    if persistent.analysemodus:
                                        text meldung["figur"] style "brief_pruefung" yalign 1.0

                                add Solid(FARBEN_STUFE[meldung["stufe"]], xsize=90, ysize=3)

                                for satz in meldung["zeilen"]:
                                    text satz style "schicksal_zeile" xsize 1008



    textbutton "Weiter":
        xalign 0.5
        yalign 0.955
        style_prefix "weiter"
        action Return()

init offset = 0


################################################################################
## 12. Ablauf
################################################################################
##
## Labels lassen sich in Ren'Py nicht überschreiben. Damit script.rpy
## unverändert bleiben kann, werden hier zwei Labels umgeleitet. Die beiden
## Fassungen unten sind Zeile für Zeile die alten, ergänzt um je einen
## einzigen Aufruf:
##
##   hauptschleife    ->  call post_zustellen      nach jedem Ereignis
##   kapitelwechsel   ->  call schicksale_wenden   nach der Jahreskarte
##
## WER LIEBER script.rpy ÄNDERT
## Dann sind es genau diese zwei Zeilen, und der ganze Abschnitt 12 mitsamt
## den beiden Labels unten kann entfallen:
##
##   in label hauptschleife, vor "jump hauptschleife":     call post_zustellen
##   in label kapitelwechsel, vor "jump hauptschleife":    call schicksale_wenden
##
## Beides gleichzeitig zu tun, wäre falsch: Dann käme nach jedem Ereignis
## zweimal Post.

init python:

    config.label_overrides["hauptschleife"] = "hauptschleife_mit_post"
    config.label_overrides["kapitelwechsel"] = "kapitelwechsel_mit_schicksal"


label hauptschleife_mit_post:

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

    ## Paket 4: Kommt heute Post?
    call post_zustellen

    jump hauptschleife


label kapitelwechsel_mit_schicksal:

    ## PAKET 8, SCHRITT 2.5: Was in diesem Kapitel gefehlt hat, wird hier
    ## gebucht — ganz oben, weil schicksale_wuerfeln() weiter unten
    ## post_im_jahr zurücksetzt und danach niemand mehr sähe, ob Post kam.
    ## Diese Marke ersetzt kapitelwechsel über config.label_overrides; die
    ## Fassung in script.rpy läuft nicht.
    $ rhythmus_kapitel_abschliessen()

    ## PAKET 8, SCHRITT 2.6. Ein Jahr endet: Der Umgebungsklang blendet aus,
    ## und Jahresabschluss wie Jahreskarte sind still. Sie tragen keine
    ## Ortsangabe — es gibt hier keinen Ort, der klingen könnte. Dieselbe
    ## Zeile steht in der Fassung in script.rpy, die nicht läuft.
    $ ton_still("umgebung")

    if aktuelles_jahr != EPILOG_JAHR:
        call screen jahresabschluss(aktuelles_jahr)

    $ folgejahr = naechstes_kapitel(aktuelles_jahr)

    if folgejahr is None:
        jump ende_ueberlebt

    $ aktuelles_jahr = folgejahr
    $ ziehungen_im_kapitel = 0
    $ wiederholbare_freigeben()

    $ letzte_kapitelwirkung = kapitel_wirkung_anwenden(aktuelles_jahr)

    ## Paket 7, Schritt 1: der Fade über FARBE_DUNKEL beim Jahreswechsel.
    ## Er ist die einzige Stelle, an der das Bild ganz dunkel wird - ein
    ## Jahr endet, ein neues fängt an.
    $ renpy.transition(UEBERGANG_KAPITEL())

    ## PAKET 8, SCHRITT 2.6. Die Jahreskarte ist eine der Stellen, an denen
    ## Musik nach Entscheidung 24 möglich wäre — 1919 ist es der Epilog. Ob
    ## dort je etwas läuft, hängt an MUSIK_EINGESCHALTET; solange der Schalter
    ## aus ist, tut diese Zeile nichts. Sie steht trotzdem hier, damit eine
    ## spätere Musikspur eine Tabellenzeile und eine Datei kostet und nicht
    ## die Suche nach der richtigen Stelle im Ablauf.
    $ musik_setzen("epilog" if aktuelles_jahr == EPILOG_JAHR else "jahreskarte")

    call screen jahreskarte(aktuelles_jahr, letzte_kapitelwirkung)

    ## Paket 4: Was ist mit den anderen geschehen?
    call schicksale_wenden

    jump hauptschleife


label post_zustellen:

    $ post_zaehler = post_zaehler + 1
    $ brief_aktuell = brief_ziehen()

    if brief_aktuell is None:
        return

    $ brief_zustellen(brief_aktuell)

    call screen brief_bildschirm(brief_aktuell)

    $ brief_wahl = _return
    $ brief_folge = brief_beantworten(brief_aktuell, brief_wahl)

    if brief_folge:
        call screen brief_ausgang_bildschirm(brief_aktuell, brief_folge)

    $ brief_aktuell = None
    $ brief_folge = None

    return


label schicksale_wenden:

    $ schicksals_meldungen = schicksale_wuerfeln()

    if not schicksals_meldungen:
        return

    call screen schicksal_bildschirm(schicksals_meldungen)

    $ schicksals_meldungen = []

    return


################################################################################
## 13. Briefprobe (Werkzeug für die Entwicklung)
################################################################################
##
## Spielt sämtliche Briefe und sämtliche Schicksalsmeldungen einer Welt
## hintereinander ab, ohne Bedingungen und ohne Würfel. Damit lässt sich
## der ganze Textbestand dieses Pakets in wenigen Minuten durchsehen.
##
## Ins Hauptmenü kommt der Aufruf mit einer Zeile in screens.rpy, im Block
## "if persistent.analysemodus" des Bildschirms main_menu:
##
##     textbutton _("Briefprobe") action Start("briefprobe")

default briefprobe_liste = []

init 3 python:

    def briefprobe_sammeln():
        """Alle Briefe und Meldungen der gewählten Welt, ungefiltert."""
        gesammelt = []

        for vorlage in BRIEFE:
            if not welt_erlaubt(vorlage.welt):
                continue
            gesammelt.append(brief_aufbereiten(vorlage))

        for kette in SCHICKSALE:
            if kette.welt and not welt_erlaubt(kette.welt):
                continue
            for nummer, stufe in enumerate(kette.stufen):
                if stufe.welt and not welt_erlaubt(stufe.welt):
                    continue
                gesammelt.append({
                    "kennung": kette.kennung + "_" + str(nummer + 1),
                    "figur": kette.figur,
                    "art": "nachricht",
                    "marke": "Schicksal",
                    "absender": figur_name(kette.figur),
                    "zusatz": kette.titel,
                    "datum": "ab " + str(stufe.ab_jahr),
                    "kopf": welttext(NACHRICHT_KOPF["nachricht"]),
                    "zeilen": list(welttext(stufe.meldung)),
                    "antworten": [],
                    "wirkung": {},
                    "nachricht": False,
                    "zustand": None,
                })

        return gesammelt


screen briefprobe_auswahl():

    default probe_herkunft = "arbeiterschaft"
    default probe_pfad = "front"
    default probe_jahr = 1916

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xpos 120
        ypos 70
        xsize 1680
        spacing 14

        text "Briefprobe" style "abschnitt_titel" size 46 text_align 0.0 xalign 0.0

        add Solid(FARBE_AKZENT, xsize=220, ysize=3)

        text "Zeigt alle Briefe und alle Schicksalsmeldungen einer Welt hintereinander, ohne Bedingungen und ohne Zufall. Das Jahr bestimmt nur die Anzeige der Kopfleiste; gezeigt werden die Texte aller Jahre." style "abschnitt_text" text_align 0.0 xsize 1400

        null height 20

        hbox:
            spacing 90

            vbox:
                spacing 10
                text "Herkunft" style "einstellung_label_text"
                vbox:
                    style_prefix "navigation"
                    for eintrag in HERKUENFTE:
                        textbutton eintrag.titel:
                            action SetScreenVariable("probe_herkunft", eintrag.kennung)
                            selected probe_herkunft == eintrag.kennung

            vbox:
                spacing 10
                text "Pfad" style "einstellung_label_text"
                vbox:
                    style_prefix "navigation"
                    for kennung in PFAD_REIHENFOLGE:
                        textbutton PFAD_MARKE.get(kennung, kennung):
                            action SetScreenVariable("probe_pfad", kennung)
                            selected probe_pfad == kennung

            vbox:
                spacing 10
                text "Jahr" style "einstellung_label_text"
                vbox:
                    style_prefix "navigation"
                    for jahr in KAPITEL_JAHRE:
                        textbutton str(jahr):
                            action SetScreenVariable("probe_jahr", jahr)
                            selected probe_jahr == jahr

        null height 40

        hbox:
            spacing 40
            style_prefix "weiter"
            textbutton "Briefe durchsehen" action Return((probe_herkunft, probe_pfad, probe_jahr))
            textbutton "Zurück zum Hauptmenü" action MainMenu(confirm=False)


label briefprobe:

    $ zustand_zuruecksetzen()

    scene bg papier
    with UEBERGANG_KARTE()

    call screen briefprobe_auswahl

    $ briefprobe_wahl = _return

    $ probe_lebenslage(briefprobe_wahl[0], briefprobe_wahl[1], None)

    $ aktuelles_jahr = briefprobe_wahl[2]
    $ figuren_anlegen()

    ## Für die Probe wird jede Figur als fort angenommen, damit auch die
    ## Briefe erscheinen, die eine Trennung voraussetzen.
    python:
        for _kennung in FIGUREN_REIHENFOLGE:
            figur_setzen(_kennung, fort=True, grund="in der Probe")

    $ briefprobe_liste = briefprobe_sammeln()
    $ briefprobe_stelle = 0

    while briefprobe_stelle < len(briefprobe_liste):
        call screen brief_bildschirm(briefprobe_liste[briefprobe_stelle])
        $ briefprobe_stelle = briefprobe_stelle + 1

    jump briefprobe

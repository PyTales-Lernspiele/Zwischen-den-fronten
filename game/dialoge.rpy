################################################################################
##
##  dialoge.rpy
##
##  Paket 1: Dialogebene
##  - fünf abstrakte Nebenfiguren mit Front- und Heimatausprägung
##  - Sprechblasen-Bildschirm statt Standard-Textbox
##  - zwölf kurze Platzhalterszenen
##
##  Grundsätze, die in dieser Datei gelten:
##  - Steuerung ausschließlich mit der Maus. Keine key-Anweisungen.
##  - Ton nur als Umgebungsklang. Seit Paket 8, Schritt 2.6 legt
##    szene_starten() den Klang des Ortes an (ortsklang_setzen). Musik legt
##    diese Datei nirgends an, und an der Front und in der Etappe verwirft
##    ton_spielen() sie hart. Kein Ton bewertet eine Entscheidung.
##  - Varianten des Hauptcharakters laufen NUR über merkmale und
##    aktueller_pfad, niemals über Figurennamen.
##  - Keine Wertveränderungen in dieser Datei. Werte gehören in die
##    Ereignisse (Paket 6 bis 8), nicht in die Dialogebene.
##
################################################################################


################################################################################
## 1. Maße und Konstanten
################################################################################

init -20 python:

    ## Die drei Standplätze auf der Bühne.
    PLAETZE = ["links", "mitte", "rechts"]

    ## Waagerechte Mitte jedes Platzes bei 1920 Pixel Breite.
    FIGUR_MITTE = {"links": 340, "mitte": 960, "rechts": 1580}

    ## Figurenmaße. Die Standlinie liegt so, dass die Kopfleiste (204 Pixel
    ## plus Trennlinien) frei bleibt und unten Platz für die Blase ist.
    FIGUR_BREITE = 300
    FIGUR_HOEHE = 480
    FIGUR_BODEN = 770
    FIGUR_SCHILD = 34

    ## Blasenband am unteren Bildrand.
    BLASE_BREITE = 880
    BLASE_OBEN = 812
    BLASE_RAND = 60
    ICH_BREITE = 1240
    ERZAEHLER_BREITE = 1400

    ## Bildquelle. In Paket 1 bekommen ALLE Figuren denselben Platzhalter.
    ## Sobald echte Bilder vorliegen, wird nur dieser Schalter umgelegt und
    ## die Dateien nach dem Muster images/figuren/<kennung>_<pfad>_<stimmung>.png
    ## abgelegt. Es muss keine Szene angefasst werden.
    FIGUREN_PLATZHALTER = "images/platzhalter.png"
    FIGUREN_ECHTE_BILDER = False

    ## Reihenfolge, in der Merkmale bei Textvarianten geprüft werden.
    ## Das speziellere Milieu steht vorn: Wer offizier ist, ist meist auch
    ## buergertum, soll aber die Offizierszeile bekommen.
    ## Die Liste wird in herkunft.rpy (init -19) überschrieben und dort um
    ## die Erwerbslagen erweitert. Diese Fassung hier ist die Grundlage;
    ## gültig ist die spätere.
    MERKMALS_REIHENFOLGE = [
        "offizier",
        "adel",
        "buergertum",
        "lazarett",
        "ruestung",
        "arbeiterschaft",
        "landbevoelkerung",
    ]

    ## Protokoll der Rückfallebene ############################################
    ##
    ## Seit Paket 2, Schritt 1. variante() und welttext() haben eine
    ## Rückfallebene: Fehlt die Fassung für den aktuellen Pfad, nehmen sie
    ## eine andere. Das ist Absicht und hält das Spiel lauffähig - aber es
    ## geschah bisher lautlos. Die Bestandsprobe außerhalb des Spiels zählte
    ## 126220 solcher Griffe an 43 Stellen, im Spiel selbst war davon nichts
    ## zu sehen.
    ##
    ## Ab jetzt schreibt jeder Griff mit. Gezählt wird je STELLE, nicht je
    ## Aufruf: Ein Ren'Py-Bildschirm wird bei jeder Mausbewegung neu
    ## berechnet, eine Zählung je Aufruf wäre also nur ein Maß für die
    ## Mausbewegung. Die Zahl in "anzahl" enthält diese Auffrischungen und
    ## taugt zum Vergleichen, nicht als Absolutwert; aussagekräftig ist die
    ## Zahl der Einträge.
    ##
    ## Rollback ist abgeschaltet (options.rpy), deshalb darf hier ohne
    ## Bedenken in eine Liste geschrieben werden.

    VARIANTENERSATZ_HOECHSTZAHL = 200

    variantenersatz_protokoll = []
    variantenersatz_stellen = {}
    variantenersatz_gesamt = 0

    ## Farbstimmung der Bühne. "dunkel" ist vorbereitet, wird in Paket 1
    ## aber noch nicht benutzt, weil die Kopfleiste auf Papier ausgelegt ist.
    BUEHNE_FARBEN = {
        "papier": {
            "grund": FARBE_PAPIER,
            "boden": FARBE_PAPIER_DUNKEL,
            "linie": FARBE_LINIE_FEIN,
        },
        "dunkel": {
            "grund": FARBE_DUNKEL,
            "boden": FARBE_DUNKEL_HELL,
            "linie": FARBE_LINIE,
        },
    }


################################################################################
## 2. Datentypen
################################################################################

init -10 python:

    class Nebenfigur(object):
        """Eine abstrakte Rolle mit zwei Ausprägungen.

        rolle       abstrakte Bezeichnung, nur für Dokumentation und Analysemodus
        namen       {"front": ..., "heimat": ...}
        zusatz      kurze Einordnung, erscheint klein neben dem Namen
        aufgabe     wofür die Figur im Spiel da ist
        """

        def __init__(self, kennung, rolle, namen, zusatz, aufgabe):
            self.kennung = kennung
            self.rolle = rolle
            self.namen = namen
            self.zusatz = zusatz
            self.aufgabe = aufgabe

    class Zeile(object):
        """Eine einzelne Anweisung innerhalb einer Szene.

        art   "auftritt", "abgang", "sagt", "ich", "erzaehlt"
        text  Zeichenkette oder Variantenwörterbuch (siehe variante())
        """

        def __init__(self, art, kennung=None, platz=None, text=None, stimmung=None):
            self.art = art
            self.kennung = kennung
            self.platz = platz
            self.text = text
            self.stimmung = stimmung

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


################################################################################
## 3. Funktionen
################################################################################

init -5 python:

    ## Textvarianten ###########################################################
    ##
    ## Ein Variantenwörterbuch darf folgende Schlüssel haben, in dieser
    ## Vorrangfolge:
    ##
    ##   "front:offizier"   Pfad und Merkmal zusammen, am speziellsten
    ##   "buergertum"       nur Merkmal
    ##   "front" / "heimat" nur Pfad
    ##   "standard"         Rückfallebene
    ##
    ## Ein Figurenname taucht hier bewusst nirgends auf.

    ## Wer den Ersatz ausgelöst hat #############################################
    ##
    ## Die Stelle wird erst dann bestimmt, wenn wirklich ein Griff in die
    ## Rückfallebene stattfindet. Im Regelfall - und das ist der weitaus
    ## häufigere - kostet das Protokoll deshalb gar nichts.

    def variantenersatz_aufrufer(tiefe=3):
        """Datei und Zeile der Stelle, die den Ersatz ausgelöst hat."""
        import sys
        import os
        try:
            rahmen = sys._getframe(tiefe)
        except Exception:
            return "unbekannt"
        return "%s in %s:%d" % (
            rahmen.f_code.co_name,
            os.path.basename(rahmen.f_code.co_filename),
            rahmen.f_lineno)

    def variantenersatz_merken(funktion, zweig, schluessel, ergebnis):
        """Trägt einen Griff in die Rückfallebene ein.

        Ein Eintrag je Stelle. Kommt dieselbe Stelle wieder, wächst nur
        ihre Zählung. Ist die Höchstzahl erreicht, wird weitergezählt,
        aber nichts Neues mehr eingetragen: Ein Protokoll, das ins
        Uferlose wächst, liest niemand mehr.
        """
        global variantenersatz_gesamt

        variantenersatz_gesamt = variantenersatz_gesamt + 1

        aufrufer = variantenersatz_aufrufer()
        stelle = (funktion, zweig, str(schluessel), str(aktueller_pfad),
                  aufrufer, aktuelles_jahr)

        vorhanden = variantenersatz_stellen.get(stelle)
        if vorhanden is not None:
            vorhanden["anzahl"] = vorhanden["anzahl"] + 1
            return

        if len(variantenersatz_protokoll) >= VARIANTENERSATZ_HOECHSTZAHL:
            return

        text = ergebnis if isinstance(ergebnis, str) else str(ergebnis)
        eintrag = {
            "funktion": funktion,
            "zweig": zweig,
            "schluessel": str(schluessel),
            "pfad": str(aktueller_pfad),
            "jahr": aktuelles_jahr,
            "aufrufer": aufrufer,
            "text": text[:40],
            "anzahl": 1,
        }
        variantenersatz_stellen[stelle] = eintrag
        variantenersatz_protokoll.append(eintrag)

    def variantenersatz_pfadschluessel(vorgaben):
        """Ist dieses Wörterbuch überhaupt nach Pfaden getrennt?

        Ein Wörterbuch nur mit "standard" ist keine Lücke, sondern eine
        Fassung für alle. Gemeldet wird deshalb nur, wo jemand nach Pfaden
        getrennt hat und ein Pfad dabei leer geblieben ist.
        """
        for name in PFAD_REIHENFOLGE:
            if name in vorgaben:
                return True
        return False

    def variante(vorgaben, standard=""):
        if not isinstance(vorgaben, dict):
            return vorgaben
        for name in MERKMALS_REIHENFOLGE:
            if hat_merkmal(name):
                zusammen = str(aktueller_pfad) + ":" + name
                if zusammen in vorgaben:
                    return vorgaben[zusammen]
        for name in MERKMALS_REIHENFOLGE:
            if hat_merkmal(name) and name in vorgaben:
                return vorgaben[name]
        if aktueller_pfad in vorgaben:
            return vorgaben[aktueller_pfad]
        ## HIER STAND DIE NOTLÖSUNG. Bis Paket 5, Schritt 1, Teil B fiel
        ## die Etappe an dieser Stelle auf die Frontfassung zurück. Das
        ## war als Übergang gedacht und hat 126220 Griffe je Messung
        ## gekostet; gestrichen ist sie, weil jetzt jede Fassung da ist,
        ## die sie ersetzt hätte - zwölf Szenen, vier Einlagen, alle
        ## Schicksale, Briefe und das ganze Merkbuch.
        ##
        ## Zusammen mit ihr fiel nach_welt() in merkbuch.rpy, das den
        ## Schlüssel "etappe" still mit der Frontfassung besetzte. Wäre
        ## nur diese Abfrage hier gestrichen worden, meldete die Probe
        ## weiterhin null, und der Ersatz stünde trotzdem im Text.
        ##
        ## Eine fehlende Etappenfassung ist ab jetzt ein echter Fehler:
        ## Sie läuft in "standard" oder in "leer" und wird gezählt.
        if "standard" in vorgaben:
            if variantenersatz_pfadschluessel(vorgaben):
                variantenersatz_merken("variante", "standard", "standard",
                                       vorgaben["standard"])
            return vorgaben["standard"]
        ## Hier ist gar nichts übrig. Das ist immer eine Lücke, auch wenn
        ## der Aufrufer einen Vorgabewert mitgegeben hat.
        variantenersatz_merken("variante", "leer", "(Vorgabewert)", standard)
        return standard

    def szenentext(vorgaben):
        """Wie variante(), löst danach aber noch Jahreszahlen auf.

        Damit lässt sich schachteln:
        {"front": {1914: "...", 1916: "..."}, "heimat": "..."}
        """
        ergebnis = variante(vorgaben)
        if isinstance(ergebnis, dict):
            ergebnis = jahrestext(ergebnis, aktuelles_jahr)
        return ergebnis

    ## Zugriff auf die Nebenfiguren ############################################

    def nebenfigur_holen(kennung):
        return NEBENFIGUR_INDEX.get(kennung)

    ## Eine Regel statt dreier ################################################
    ##
    ## SEIT PAKET 5, SCHRITT 1, TEIL B. Beide Funktionen haben vorher
    ## selbst gewählt: erst der eigene Pfad, sonst still die Heimatfassung.
    ## Damit gab es im Projekt drei verschiedene Rückfallrichtungen -
    ## variante() fiel zur Front, nach_welt() ebenfalls, diese beiden und
    ## zustand_anzeige() zur Heimat. Ein Ersatz, der je nach Aufrufer in
    ## eine andere Richtung fällt, ist nicht mehr nachvollziehbar.
    ##
    ## Jetzt entscheidet ausschliesslich variante(). Das kostet nichts und
    ## bringt zweierlei: Die Vorrangfolge mit Merkmalen gilt auch für
    ## Namen, und jede fehlende Fassung wird GEZÄHLT statt ersetzt. Wer
    ## hier eine Lücke lässt, sieht sie in Probe 2c.

    def figur_name(kennung):
        figur = nebenfigur_holen(kennung)
        if figur is None:
            return ""
        return variante(figur.namen, "")

    def figur_zusatz(kennung):
        figur = nebenfigur_holen(kennung)
        if figur is None:
            return ""
        return variante(figur.zusatz, "")

    def figur_rolle(kennung):
        figur = nebenfigur_holen(kennung)
        if figur is None:
            return ""
        return figur.rolle

    ## Zentrale Bildfunktion ###################################################
    ##
    ## Einziger Ort im Projekt, an dem ein Figurenbild entsteht.

    def figur_bild_pfad(kennung, stimmung):
        return ("images/figuren/" + str(kennung) + "_"
                + str(aktueller_pfad) + "_" + str(stimmung) + ".png")

    def figur_bild(kennung, stimmung="neutral", breite=None, hoehe=None):
        if breite is None:
            breite = FIGUR_BREITE
        if hoehe is None:
            hoehe = FIGUR_HOEHE
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

    ## Bühne ###################################################################

    def buehne_leeren():
        global buehne, buehne_stimmung, buehne_sprecher
        buehne = {"links": None, "mitte": None, "rechts": None}
        buehne_stimmung = {"links": "neutral", "mitte": "neutral", "rechts": "neutral"}
        buehne_sprecher = None

    def buehne_setzen(platz, kennung, stimmung="neutral"):
        global buehne, buehne_stimmung
        if platz not in PLAETZE:
            return
        neu = dict(buehne)
        neu[platz] = kennung
        buehne = neu
        neue_stimmung = dict(buehne_stimmung)
        neue_stimmung[platz] = stimmung if stimmung else "neutral"
        buehne_stimmung = neue_stimmung

    def buehne_platz_von(kennung):
        for platz in PLAETZE:
            if buehne.get(platz) == kennung:
                return platz
        return None

    def buehne_freier_platz():
        for platz in ["mitte", "rechts", "links"]:
            if not buehne.get(platz):
                return platz
        return "mitte"

    def buehne_farbe(stelle):
        satz = BUEHNE_FARBEN.get(szene_hintergrund, BUEHNE_FARBEN["papier"])
        return satz[stelle]

    ## Blasenposition #########################################################

    def blase_mitte(platz):
        ziel = FIGUR_MITTE.get(platz, 960)
        halb = BLASE_BREITE // 2
        links = BLASE_RAND + halb
        rechts = 1920 - BLASE_RAND - halb
        if ziel < links:
            return links
        if ziel > rechts:
            return rechts
        return ziel

    def zipfel_versatz(platz):
        return FIGUR_MITTE.get(platz, 960) - blase_mitte(platz)

    ## Szenenablauf ###########################################################

    def szene_holen(kennung):
        return SZENEN_INDEX.get(kennung)

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
        ## PAKET 8, SCHRITT 2.6. Der Umgebungsklang der Szene. Er steht hier
        ## und nicht in label szene_spielen, weil der aufgelöste Ortstext erst
        ## in dieser Zeile darüber entsteht — im label stünde noch das
        ## Wörterbuch.
        ortsklang_setzen(szene_ort)
        if szene_aktuell.stimmung:
            stimmung_setzen(szene_aktuell.stimmung)
        renpy.show_screen("szenen_buehne")

    def szene_fertig():
        if szene_aktuell is None:
            return True
        return szene_stelle >= len(szene_aktuell.zeilen)

    def szene_schritt():
        global szene_stelle, buehne_sprecher

        zeile = szene_aktuell.zeilen[szene_stelle]
        szene_stelle = szene_stelle + 1

        if zeile.art == "auftritt":
            buehne_setzen(zeile.platz, zeile.kennung, zeile.stimmung)
            return

        if zeile.art == "abgang":
            if buehne_sprecher == zeile.platz:
                buehne_sprecher = None
            buehne_setzen(zeile.platz, None)
            return

        if zeile.art == "sagt":
            platz = buehne_platz_von(zeile.kennung)
            if platz is None:
                platz = buehne_freier_platz()
                buehne_setzen(platz, zeile.kennung, zeile.stimmung)
            elif zeile.stimmung:
                buehne_setzen(platz, zeile.kennung, zeile.stimmung)
            buehne_sprecher = platz
            renpy.say(szenen_stimme, szenentext(zeile.text))
            return

        if zeile.art == "ich":
            buehne_sprecher = None
            renpy.say(ich_stimme, szenentext(zeile.text))
            return

        buehne_sprecher = None
        renpy.say(erzaehler_stimme, szenentext(zeile.text))

    def szene_beenden():
        global szene_aktuell, szene_stelle
        if szene_aktuell is not None and szene_aktuell.stimmung:
            stimmung_setzen(None)
        renpy.hide_screen("szenen_buehne")
        buehne_leeren()
        szene_aktuell = None
        szene_stelle = 0

    ## Kurzschreibweisen für die Szenen ########################################

    def auftritt(platz, kennung, stimmung="neutral"):
        return Zeile("auftritt", kennung=kennung, platz=platz, stimmung=stimmung)

    def abgang(platz):
        return Zeile("abgang", platz=platz)

    def sagt(kennung, text, stimmung=None):
        return Zeile("sagt", kennung=kennung, text=text, stimmung=stimmung)

    def ich(text):
        return Zeile("ich", text=text)

    def erzaehlt(text):
        return Zeile("erzaehlt", text=text)


################################################################################
## 4. Figurenbestand
################################################################################
##
## Fünf Rollen, jede mit einer Ausprägung je Pfad. Die Rollen sind
## absichtlich abstrakt: Jede erfüllt auf allen drei Pfaden dieselbe
## Funktion, nur mit anderem Gesicht. Dadurch bleibt jede Szene überall
## spielbar, ohne dass Figuren dreifach geschrieben werden müssen.
##
## SEIT PAKET 5, SCHRITT 1, TEIL B trägt jede Rolle eine dritte
## Ausprägung. Vorher fiel figur_name() für die Etappe still auf die
## HEIMATfassung zurück - als einzige Stelle im Projekt, die nach
## unten in diese Richtung fiel, während alles andere zur Front fiel.
## Im Merkbuch stehen diese Namen groß auf jeder der vier Seiten; dort
## las ein Etappenspieler von der Nachbarin aus demselben Haus.
##
## WORAN DIE ETAPPENFASSUNG SICH HÄLT: Die Etappe kennt keinen Graben
## und keinen Hof, sondern Rampe, Magazin, Schreibstube und Gleis. Ihre
## Leute sind eingeteilt, nicht eingezogen oder daheim. Und die
## Gegenseite ist hier nicht achtzig Meter entfernt, sondern arbeitet
## in Sichtweite - das ist der Unterschied, den dieser Pfad trägt.

init python:

    NEBENFIGUREN = [

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
            "Zeigt, dass die andere Seite aus Menschen besteht, ohne den "
            "Gegensatz aufzulösen."
        ),

        Nebenfigur(
            "naechste", "der oder die Nächste",
            {
                "front": "Dein Nebenmann",
                "etappe": "Dein Schichtnachbar",
                "heimat": "Die Nachbarin",
            },
            {
                "front": "aus deiner Gruppe",
                "etappe": "ihr steht an derselben Rampe",
                "heimat": "aus demselben Haus",
            },
            "Trägt den Wert Einsamkeit. Wer hier verliert, verliert am meisten."
        ),

        Nebenfigur(
            "amtsperson", "die Amtsperson",
            {
                "front": "Der Feldwebel",
                "etappe": "Der Zahlmeister",
                "heimat": "Der Beamte",
            },
            {
                "front": "er führt die Liste",
                "etappe": "er führt das Buch",
                "heimat": "er führt die Akte",
            },
            "Trägt den Wert Verdacht. Nicht böse, sondern zuständig."
        ),

        Nebenfigur(
            "kind", "das Kind",
            {
                "front": "Der Jüngste",
                "etappe": "Der Laufbursche",
                "heimat": "Das Kind",
            },
            {
                "front": "siebzehn Jahre",
                "etappe": "er trägt die Meldungen",
                "heimat": "aus dem Erdgeschoss",
            },
            "Stellt die Fragen, die Erwachsene sich abgewöhnt haben."
        ),

        Nebenfigur(
            "kundige", "die Kundige",
            {
                "front": "Der Landwehrmann",
                "etappe": "Der alte Schreiber",
                "heimat": "Die Frau aus dem Hinterhaus",
            },
            {
                "front": "der Älteste der Gruppe",
                "etappe": "er kennt jedes Formular",
                "heimat": "sie kennt die Vorschriften",
            },
            "Erklärt Regeln und Tricks. Über sie kommt Sachwissen ins Spiel, "
            "ohne dass jemand doziert."
        ),

    ]

    NEBENFIGUR_INDEX = {}
    for _figur in NEBENFIGUREN:
        NEBENFIGUR_INDEX[_figur.kennung] = _figur


################################################################################
## 5. Szenen
################################################################################
##
## Zwölf kurze Platzhalterszenen. Sie enthalten bewusst keine Entscheidungen
## und keine Wertveränderungen: Sie sollen Bindung aufbauen, damit die
## Entscheidungen aus Paket 6 bis 8 später etwas kosten.

init python:

    SZENEN = [

        ########################################################################
        ## Prolog 1914
        ########################################################################

        Szene(
            "prolog_ankunft", "Prolog: Ankommen",
            ort={"front": "Grabenstellung", "etappe": "Etappenort", "heimat": "Wohnviertel"},
            zeilen=[
                erzaehlt({
                    "front": "Der Zug ist bis zur letzten Station gefahren, den Rest geht ihr zu Fuß. Seit einer Stunde hört ihr ein Grollen, das nicht vom Wetter kommt.",
                    "etappe": "Der Zug hat dich hier abgesetzt und fährt ohne dich weiter nach vorn. Vom Rangierbahnhof her hört man Puffer, die aneinanderstoßen. Es riecht nach Kohle.",
                    "heimat": "Der Zug ist weg. Der Bahnsteig leert sich schneller, als du gedacht hast. Zu Hause steht das Frühstücksgeschirr noch auf dem Tisch.",
                }),
                auftritt("rechts", "naechste"),
                sagt("naechste", {
                    "front:offizier": "Herr Leutnant. Der Zugang zur Stellung ist links. Rechts steht sie seit vorgestern unter Wasser.",
                    "etappe:offizier": "Herr Leutnant. Schreibstube links, Magazin rechts. Gemeldet wird bei dem, der das Buch führt.",
                    "front": "Du bist neu. Geh hinter mir und mach nach, was ich mache.",
                    "etappe": "Du bist neu. Halt dich an mich, dann findest du die Rampe und das Essen.",
                    "heimat:adel": "Gnädige Frau. Morgen früh brauchen Sie auch eine Nummer. Anstellen muss sich jeder selbst.",
                    "heimat": "Ich habe dich am Fenster gesehen. Morgen stellen wir uns zusammen an. Zu zweit hält man das Stehen besser aus.",
                }),
                ich({
                    "front": "Wie lange seid ihr schon hier?",
                    "etappe": "Was wird hier gemacht?",
                    "heimat": "Wann muss man denn da sein?",
                }),
                sagt("naechste", {
                    "front": "Sechs Wochen. Am Anfang zählt man die Tage. Später lässt man das.",
                    "etappe": "Alles, was nach vorn geht, geht hier durch. Und alles, was zurückkommt, auch.",
                    "heimat": "Um vier. Wer um fünf kommt, sieht nur noch Rücken.",
                }),
                erzaehlt({
                    "front": "Du merkst dir den Weg, das Wasser und den Namen. Mehr schaffst du heute nicht.",
                    "etappe": "Du merkst dir das Gleis, die Baracke und den Namen. Das Grollen von vorn hörst du erst in der Nacht.",
                    "heimat": "Du merkst dir den Namen und die Uhrzeit. Mehr brauchst du heute nicht.",
                }),
            ]
        ),

        Szene(
            "prolog_ordnung", "Prolog: Die Ordnung",
            ## Die Frontfassung trug hier bis Paket 5, Schritt 1 den Ort
            ## "Etappe". Das war richtig, solange die Etappe kein eigener
            ## Pfad war - der Feldwebel mit der Stammrolle sitzt hinter
            ## der Stellung. Jetzt liest sich dieselbe Zeile so, als
            ## stünde die Figur auf dem anderen Pfad. "Ersatztruppenteil"
            ## meint denselben Ort und heißt nicht wie ein Pfad.
            ort={"front": "Ersatztruppenteil", "etappe": "Schreibstube",
                 "heimat": "Gemeindeamt"},
            zeilen=[
                erzaehlt({
                    "front": "Am Abend wird die Gruppe zusammengerufen. Der Feldwebel hat ein Buch dabei, in das er alles einträgt.",
                    "etappe": "In der Schreibstube brennt Licht, bis die Meldung heraus ist. Auf dem Tisch liegen drei Bücher, und jedes will denselben Namen.",
                    "heimat": "Auf dem Amt gibt es eine Nummer, einen Stuhl und einen Schalter. Über dem Schalter hängt eine Verordnung.",
                }),
                auftritt("mitte", "amtsperson"),
                sagt("amtsperson", {
                    "front:offizier": "Herr Leutnant, die Stärkemeldung geht um acht heraus. Was bis dahin nicht gemeldet ist, gibt es nicht.",
                    "etappe:offizier": "Herr Leutnant, ich führe hier drei Bücher. Wenn eines nicht stimmt, stimmt keines.",
                    "front": "Sie stehen in meiner Liste. Wer sich meldet, meldet sich bei mir. Wer fehlt, fehlt bei mir.",
                    "etappe": "Sie stehen in drei Listen. Verpflegung, Dienst, Unterkunft. Was in keiner steht, gibt es nicht.",
                    "heimat:adel": "Gnädige Frau, für Ihre Sammlung brauche ich eine Bescheinigung. Für alles Übrige gilt dieselbe Liste wie für alle.",
                    "heimat": "Sie werden hier geführt. Name, Wohnung, Haushalt. Was in der Liste steht, gilt. Was Sie mir erzählen, gilt erst, wenn es darin steht.",
                }),
                ich({
                    "front": "Und wenn etwas passiert?",
                    "etappe": "Und wenn zwei Bücher sich widersprechen?",
                    "heimat": "Und wenn etwas nicht stimmt?",
                }),
                sagt("amtsperson", {
                    "front": "Dann meldet es jemand, und ich schreibe es auf. Dafür bin ich da.",
                    "etappe": "Dann gilt das obere. Und Sie schreiben das untere ab, bis es passt.",
                    "heimat": "Dann stellen Sie einen Antrag. Der wird geprüft. Der Nächste, bitte.",
                }),
                erzaehlt(
                    "Du unterschreibst neben deinem Namen. Von hier an gibt es dich zweimal: einmal als Mensch und einmal als Zeile."
                ),
            ]
        ),

        Szene(
            "prolog_kind", "Prolog: Bis Weihnachten",
            ort={"front": "Grabenstellung", "etappe": "Etappenort", "heimat": "Wohnviertel"},
            zeilen=[
                erzaehlt({
                    "front": "Der Jüngste der Gruppe ist siebzehn. Er sagt es nicht, aber alle wissen es.",
                    "etappe": "Der Laufbursche ist fünfzehn und trägt die Meldungen zwischen den Baracken. Er wartet am Gleis, bis der Zug nach vorn abfährt.",
                    "heimat": "Das Kind aus dem Erdgeschoss wartet jeden Abend an der Haustür, bis die Post durch ist.",
                }),
                auftritt("links", "kind"),
                sagt("kind", {
                    "front": "Mein Vater hat unterschrieben. Ohne Unterschrift nehmen sie einen unter einundzwanzig nicht als Kriegsfreiwilligen.",
                    "etappe": "Mein Bruder ist mit dem Zug am Dienstag nach vorn. Zu Weihnachten ist er wieder hier, sagt der Feldwebel.",
                    "heimat": "Der Lehrer hat gesagt, zu Weihnachten sind sie wieder da.",
                }),
                ich({
                    "front": "Und, wolltest du das?",
                    "etappe": "Das steht auf keinem Fahrplan.",
                    "heimat": "Das haben viele gesagt.",
                }),
                sagt("kind", {
                    "front": "Alle aus meiner Klasse sind gegangen. Ich weiß nur nicht, wann es anfängt.",
                    "etappe": "Auf dem Rückweg halten die Züge hier. Dann sehe ich ihn.",
                    "heimat": "Also stimmt es?",
                }),
                abgang("links"),
                erzaehlt({
                    "front": "Du sagst ihm nicht, dass es längst angefangen hat.",
                    "etappe": "Du hast heute gesehen, welche Züge zurückkommen. Wer darin liegt, sagst du ihm nicht.",
                    "heimat:lazarett": "Du hast heute im Lazarett gesehen, was von Weihnachten übrig ist. Du sagst es nicht.",
                    "heimat": "Du überlegst zu lange. Das Kind merkt es und fragt nicht weiter.",
                }),
            ]
        ),

        ########################################################################
        ## 1915: Feldpost
        ########################################################################

        Szene(
            "feldpost_1915_regeln", "1915: Was man schreiben darf",
            ort={"front": "Grabenstellung", "etappe": "Schreibstube", "heimat": "Wohnviertel"},
            zeilen=[
                erzaehlt({
                    "front": "Die Feldpost geht zweimal in der Woche zurück. Papier hat, wer eines abbekommt.",
                    "etappe": "Die Post für den ganzen Abschnitt geht über deinen Tisch. Deinen eigenen Brief schreibst du zuletzt.",
                    "heimat": "Der Bogen liegt seit gestern auf dem Tisch. Angefangen hast du dreimal.",
                }),
                auftritt("rechts", "kundige"),
                sagt("kundige", {
                    "front": "Schreib nichts über die Stellung, keine Ortsnamen, keine Zahlen. Sonst kommt der Brief geschwärzt an, und du bekommst Ärger dazu.",
                    "etappe": "Schreib nichts über Züge und nichts über Mengen. Du weißt genau, was hier gestrichen wird.",
                    "heimat": "Schreib ihm nichts von den Preisen. Ändern kann er daran nichts, und lesen wird er es zehnmal.",
                }),
                ich({
                    "buergertum": "Ein Brief soll doch die Wahrheit sagen.",
                    "front": "Was bleibt dann übrig?",
                    "etappe": "Ich streiche das den ganzen Tag.",
                    "heimat": "Soll ich ihn anlügen?",
                }),
                sagt("kundige", {
                    "front:buergertum": "Ein Brief soll ankommen. Die Wahrheit kommt nicht durch die Zensur.",
                    "etappe:buergertum": "Ein Brief soll ankommen. Du hast heute selbst gesehen, was nicht ankommt.",
                    "heimat:buergertum": "Ein Brief soll ankommen. Und er soll ihm nicht die Nacht kaputt machen.",
                    "front": "Das Wetter. Das Essen. Dass du lebst. Das ist mehr, als du denkst.",
                    "etappe": "Eben. Und deiner geht durch dieselben Hände.",
                    "heimat": "Du sollst auswählen. Das ist nicht dasselbe wie lügen.",
                }),
                erzaehlt(
                    "Du schreibst vier Sätze und streichst zwei davon wieder durch."
                ),
            ]
        ),

        Szene(
            "feldpost_1915_schweigen", "1915: Was niemand schreibt",
            ort={"front": "Grabenstellung", "etappe": "Quartier", "heimat": "Wohnviertel"},
            zeilen=[
                erzaehlt({
                    "front": "Am Abend liegen drei Briefe auf dem Brett und warten auf die Post.",
                    "etappe": "Der Sack mit der Post steht schon zu. Deiner liegt obenauf, weil du ihn zuletzt geschrieben hast.",
                    "heimat": "Der Brief ist fertig. Auf dem Umschlag steht eine Feldpostnummer, keine Stadt.",
                }),
                auftritt("mitte", "naechste"),
                sagt("naechste", {
                    "front": "Was hast du geschrieben?",
                    "etappe": "Was hast du geschrieben, wo du bist?",
                    "heimat": "Ich habe ihm geschrieben, dass wir gut zurechtkommen.",
                }),
                ich({
                    "front": "Dass es mir gut geht.",
                    "etappe": "Im Westen. Mehr steht da nicht.",
                    "heimat": "Und stimmt das?",
                }),
                sagt("naechste", {
                    "front": "Ich auch. Wir schreiben alle dasselbe, und zu Hause halten sie es für die Wahrheit.",
                    "etappe": "Ich schreibe: bei der Truppe. Zu Hause denken sie sich den Graben dazu, und ich lasse sie.",
                    "heimat": "An drei Tagen in der Woche stimmt es.",
                }),
                erzaehlt({
                    "front": "Die Post nimmt die Briefe am Morgen mit. Was darin steht, wird zu Hause vorgelesen.",
                    "etappe": "Am Morgen fährt der Sack mit dem ersten Zug. Was darin steht, hast du selbst geprüft, deinen Brief ausgenommen.",
                    "heimat": "Du klebst den Umschlag zu. Was darin steht, wird dort drüben zehnmal gelesen.",
                }),
            ]
        ),

        Szene(
            "alltag_1915_gegenseite", "1915: Achtzig Meter",
            ort={"front": "Grabenstellung", "etappe": "Arbeitsstelle", "heimat": "Wohnviertel"},
            zeilen=[
                erzaehlt({
                    "front": "Nachts trägt der Wind. Der andere Graben liegt achtzig Meter weiter, und heute singt dort jemand.",
                    "etappe": "Die Kolonne arbeitet seit dem Morgen am Gleis, zwanzig Schritt von deinem Tisch. Einer von ihnen singt beim Schaufeln, halblaut.",
                    "heimat": "Die Frau aus dem Vorderhaus steht im Hof, wenn du gehst, und steht dort, wenn du wiederkommst.",
                }),
                auftritt("links", "gegenseite"),
                sagt("gegenseite", {
                    "front": "Kamerad! Heute Nacht nicht schießen. Heute Nacht ist Sonntag.",
                    "etappe": "Kamerad. Wasser gibt es um zwölf. Es ist schon nach eins.",
                    "heimat": "Sie waren lange weg. Mit einem Rucksack.",
                }),
                ich({
                    "front": "Heute Nacht nicht.",
                    "etappe": "Ich hole den Eimer.",
                    "heimat:landbevoelkerung": "Ich war bei meinen Leuten auf dem Dorf.",
                    "heimat": "Ich war bei meiner Schwester.",
                }),
                sagt("gegenseite", {
                    "front": "Gut. Morgen wieder.",
                    "etappe": "Danke. Morgen um zwölf?",
                    "heimat": "Natürlich. Ich sage ja nichts.",
                }),
                erzaehlt({
                    "front": "Am Morgen wird wieder geschossen. Ihr wisst beide vorher, dass es so kommt.",
                    "etappe": "Am nächsten Tag ist die Kolonne eine andere. Wohin die alte gekommen ist, steht in keinem deiner Bücher.",
                    "heimat": "Sie sagt nichts. Sie merkt es sich. Das ist etwas anderes.",
                }),
            ]
        ),

        ########################################################################
        ## Wendepunkt 1916
        ########################################################################

        Szene(
            "wendepunkt_1916_zaehlen", "1916: Zählen",
            ort={"front": "Grabenstellung", "etappe": "Schreibstube", "heimat": "Wohnviertel"},
            zeilen=[
                erzaehlt({
                    "front": "Februar 1916. In der Zeitung steht Verdun. Was in der Zeitung steht, erkennst du nicht wieder.",
                    "etappe": "Sommer 1916. Die Verlustlisten kommen jetzt gebündelt und werden bei dir abgeschrieben. Die Bögen sind eng beschrieben, und die Namen sind fremd.",
                    "heimat": "Herbst 1916. Die Kartoffelernte ist verdorben. Zugeteilt wird Steckrübe, dazu ein Merkblatt mit Rezepten.",
                }),
                auftritt("rechts", "kundige"),
                sagt("kundige", {
                    "front": "Zähl nicht die Toten. Zähl die Tage bis zur Ablösung. Bei den Toten hörst du irgendwann nicht mehr auf.",
                    "etappe": "Zähl nicht mit, während du schreibst. Zähl die Bögen, dann bist du abends fertig.",
                    "heimat": "Achtzehn Rezepte für eine Rübe. Wer das aufgeschrieben hat, hat sie nie gegessen.",
                }),
                ich({
                    "front": "Wie viele Tage sind es?",
                    "etappe": "Wie viele Bögen sind es?",
                    "heimat": "Und was machst du damit?",
                }),
                sagt("kundige", {
                    "front": "Neun. Frag mich morgen wieder, dann sind es acht. Das hilft, auch wenn es dumm klingt.",
                    "etappe": "Vierzig. Morgen sind es wieder vierzig. Frag lieber nicht, aus welchem Abschnitt.",
                    "heimat": "Kochen, bis sie weich ist. Und beim Essen an nichts denken.",
                }),
                erzaehlt({
                    "front:landbevoelkerung": "Zu Hause hast du die Tage bis zur Ernte gezählt. Es ist genau dasselbe, und das erschreckt dich.",
                    "front": "Du fängst an zu zählen. Es hilft. Das ist das Merkwürdige daran.",
                    "etappe": "Du schreibst sauber und gleichmäßig, weil es sonst länger dauert. Am dritten Tag liest du die Namen nicht mehr.",
                    "heimat": "Ihr esst Rübe mittags und Rübe abends. Nach vier Wochen riecht die ganze Treppe danach.",
                }),
            ]
        ),

        Szene(
            "wendepunkt_1916_amt", "1916: Von oben",
            ## Wie bei prolog_ordnung: kein Pfadname als Ortsangabe. Der
            ## Text der Frontfassung nennt den Anschlag am Unterstand,
            ## also die Stellung selbst.
            ort={"front": "Grabenstellung", "etappe": "Magazin",
                 "heimat": "Gemeindeamt"},
            zeilen=[
                erzaehlt({
                    "front": "Ein Anschlag am Unterstand. Der Urlaub für den Abschnitt ist bis auf Weiteres gestrichen.",
                    "etappe": "Am Magazin hängt eine neue Anweisung. Die Sätze für den Abschnitt werden gekürzt, ab Montag.",
                    "heimat": "Am Schalter hängt ein neuer Zettel. Die Zuteilung wird noch einmal gekürzt.",
                }),
                auftritt("mitte", "amtsperson"),
                auftritt("links", "naechste"),
                sagt("amtsperson", {
                    "front": "Ich habe das nicht entschieden. Ich gebe es weiter. Beschwerden nehme ich trotzdem entgegen.",
                    "etappe": "Ich habe die Zahl nicht gemacht. Ich gebe aus, was sie mir schicken.",
                    "heimat": "Das kommt von oben, nicht aus diesem Zimmer. Ich verteile nur, was da ist.",
                }),
                ich({
                    "front": "Und wenn ich mich beschwere?",
                    "etappe": "Und was sage ich den Fahrern?",
                    "heimat": "Und wovon leben wir?",
                }),
                sagt("amtsperson", {
                    "front": "Dann schreibe ich auf, dass Sie sich beschwert haben. Es geht weiter nach oben und ändert nichts.",
                    "etappe": "Dasselbe wie ich. Und dann schreiben Sie es in die Spalte für Fehlmengen.",
                    "heimat:ruestung": "Sie arbeiten in der Rüstung. Für Schwerarbeit gibt es eine Zusatzkarte, wenn der Betrieb sie bescheinigt.",
                    "heimat": "Von der Karte. Wie alle.",
                }),
                sagt("naechste", {
                    "front": "Lass es. Er kann nichts dafür.",
                    "etappe": "Lass gut sein. Draußen stehen noch drei Kolonnen.",
                    "heimat": "Komm. Hinter uns warten auch noch welche.",
                }),
                erzaehlt(
                    "Er sagt den Satz heute nicht zum ersten Mal. Man hört es ihm an."
                ),
            ]
        ),

        Szene(
            "wendepunkt_1916_bruch", "1916: Drei Tage still",
            ort={"front": "Grabenstellung", "etappe": "Quartier", "heimat": "Wohnviertel"},
            stimmung="erschoepft",
            zeilen=[
                erzaehlt({
                    "front": "Dein Nebenmann redet seit drei Tagen nicht mehr.",
                    "etappe": "Dein Schichtnachbar hat sich seit drei Tagen nicht zur Ausgabe gemeldet.",
                    "heimat": "Die Nachbarin war heute Morgen nicht in der Schlange. Zum ersten Mal seit zwei Jahren.",
                }),
                auftritt("mitte", "naechste", "erschoepft"),
                ich({
                    "front": "Was ist los?",
                    "etappe": "Du fehlst in der Liste.",
                    "heimat": "Du warst nicht da.",
                }),
                sagt("naechste", {
                    "front": "Nichts. Frag nicht.",
                    "etappe": "Trag mich ein. Ich stehe gleich auf.",
                    "heimat": "Ich bin nicht aufgestanden.",
                }),
                ich({
                    "front": "Gut.",
                    "etappe": "Seit wann?",
                    "heimat": "Und jetzt?",
                }),
                sagt("naechste", {
                    "front": "Mein Bruder steht in der Verlustliste. Ich habe sie zweimal gelesen, weil ich dachte, ich hätte mich verlesen.",
                    "etappe": "Ich habe den Bogen abgeschrieben, auf dem mein Bruder steht. Mit meiner eigenen Hand, und zweimal, weil die erste Zeile verwischt war.",
                    "heimat": "Ich kann nicht mehr um vier aufstehen und um neun mit leeren Händen zurückkommen. Heute nicht.",
                }),
                erzaehlt({
                    "front": "Du legst ihm die Hand auf die Schulter. Mehr fällt dir nicht ein, und mehr erwartet er nicht.",
                    "etappe": "Du nimmst ihm den Stift aus der Hand und schreibst den Rest allein. Er sieht zu und sagt nichts dazu.",
                    "heimat": "Am nächsten Morgen steht sie wieder da. Zwei Plätze weiter hinten als sonst.",
                }),
            ]
        ),

        ########################################################################
        ## Abschluss
        ########################################################################

        Szene(
            "abschluss_kind", "Abschluss: Er fragt nicht mehr",
            ort={"front": "Grabenstellung", "etappe": "Etappenort", "heimat": "Wohnviertel"},
            zeilen=[
                erzaehlt({
                    "front": "Der Jüngste ist jetzt zwei Jahre älter. Es sind Neue gekommen, jünger als er damals.",
                    "etappe": "Der Laufbursche ist siebzehn und steht jetzt auf der Musterungsliste. Er trägt die Meldungen noch, aber nicht mehr lange.",
                    "heimat": "Das Kind ist dreizehn und geht seit dem Frühjahr in die Fabrik.",
                }),
                auftritt("links", "kind"),
                sagt("kind", {
                    "front": "Sie fragen mich Sachen, und ich antworte, als wüsste ich es.",
                    "etappe": "Ich weiß jetzt, welche Züge nach vorn fahren und welche zurück.",
                    "heimat": "Ich frage nicht mehr, wann Vater wiederkommt.",
                }),
                ich({
                    "front": "Weißt du es denn?",
                    "etappe": "Und was machst du damit?",
                    "heimat": "Warum nicht?",
                }),
                sagt("kind", {
                    "front": "Ich weiß, wo man den Kopf einzieht. Der Rest ist Glück, und das sage ich denen nicht.",
                    "etappe": "Nichts. Ich steige trotzdem in den, der nach vorn fährt.",
                    "heimat": "Weil du dann so guckst.",
                }),
                erzaehlt({
                    "front": "Er redet wie der Landwehrmann damals. Du überlegst, wann das angefangen hat.",
                    "etappe": "Er sagt es wie einen Fahrplan, ohne Stolz und ohne Angst. Genau das bleibt bei dir hängen.",
                    "heimat": "Es sagt das ohne Vorwurf, so wie man das Wetter sagt. Genau das ist das Schlimmere.",
                }),
            ]
        ),

        Szene(
            "abschluss_gegenseite", "Abschluss: Dieselbe Schlange",
            ort={"front": "Grabenstellung", "etappe": "Arbeitsstelle", "heimat": "Wohnviertel"},
            zeilen=[
                erzaehlt({
                    "front": "Ein Gefangener wird durch den Graben geführt. Er ist ungefähr so alt wie du.",
                    "etappe": "Die Kolonne ist seit dem Frühjahr dieselbe. Ihr kennt eure Gesichter, eure Namen nicht.",
                    "heimat": "Die Frau aus dem Vorderhaus steht in derselben Schlange wie du. Seit Wochen, jeden Morgen.",
                }),
                auftritt("rechts", "gegenseite"),
                sagt("gegenseite", {
                    "front": "Wasser. Bitte.",
                    "etappe": "Sie schreiben jeden Tag mit. Steht mein Name da auch?",
                    "heimat": "Sie sind jeden Tag vor mir hier. Wie machen Sie das?",
                }),
                ich({
                    "front": "Hier.",
                    "etappe": "Eine Nummer steht da.",
                    "heimat": "Ich stehe seit halb vier.",
                }),
                sagt("gegenseite", {
                    "front": "Danke. Ich habe zu Hause auch Kinder.",
                    "etappe": "Dann schreiben Sie ihn einmal dazu. Nur einmal.",
                    "heimat": "Halb vier schaffe ich nicht mehr.",
                }),
                erzaehlt({
                    "front": "Er gibt die Flasche zurück, dann führen sie ihn weiter. Wohin, erfährst du nicht.",
                    "etappe": "Am Abend steht in deiner Spalte eine Zahl und daneben ein Wort in deiner Schrift. Ob es der richtige Name ist, weißt du nicht.",
                    "heimat": "Ihr steht nebeneinander, bis der Laden schließt. Danach sagt sie nichts mehr, und du auch nicht.",
                }),
            ]
        ),

        Szene(
            "abschluss_bilanz", "Abschluss: Frag mich noch mal",
            ort={"front": "Grabenstellung", "etappe": "Etappenort", "heimat": "Wohnviertel"},
            zeilen=[
                erzaehlt(
                    "Zwei Jahre. Du rechnest nicht mehr in Wochen."
                ),
                auftritt("rechts", "naechste"),
                sagt("naechste", {
                    "front": "Weißt du noch, im Herbst vierzehn? Da hast du gefragt, wie lange wir hier schon stehen.",
                    "etappe": "Weißt du noch, am ersten Tag? Da hast du gefragt, was hier gemacht wird.",
                    "heimat": "Weißt du noch, am Anfang? Da hast du gefragt, wann man da sein muss.",
                }),
                ich({
                    "front": "Sechs Wochen, hast du gesagt.",
                    "etappe": "Alles geht hier durch, hast du gesagt.",
                    "heimat": "Um vier, hast du gesagt.",
                }),
                sagt("naechste",
                    "Frag mich heute noch mal."
                ),
                ich({
                    "front": "Wie lange?",
                    "etappe": "Was wird hier gemacht?",
                    "heimat": "Wann muss man da sein?",
                }),
                sagt("naechste", {
                    "front": "Weiß ich nicht mehr. Und das ist die Antwort.",
                    "etappe": "Gezählt wird. Und das ist die Antwort.",
                    "heimat": "Immer. Und das ist die Antwort.",
                }),
                erzaehlt(
                    "Der Krieg geht weiter. Was dich diese Jahre gekostet haben, merkst du erst, wenn dich jemand danach fragt."
                ),
            ]
        ),

        ########################################################################
        ## Der Wirtshaustisch, Frühjahr 1919
        ########################################################################
        ##
        ## SEIT PAKET 5, SCHRITT 2. Pflichtszene vor dem Lebenslauf, auf
        ## jedem Pfad und in jedem Durchgang, der 1919 erreicht.
        ##
        ## DER FREMDE IST KEINE NEBENFIGUR und bekommt deshalb kein
        ## Gesicht und keinen Namen. Er spricht ausschließlich über
        ## erzaehlt() in wörtlicher Rede. Das ist Absicht: Wer die
        ## Behauptung aufstellt, ist austauschbar - sie ist es nicht.
        ##
        ## KEIN ERZÄHLER STELLT RICHTIG. Nirgends steht, dass die
        ## Behauptung falsch ist. Was ihr entgegensteht, sind die vier
        ## Jahre, die die Spielerin selbst gespielt hat, und der Satz der
        ## Kundigen, die dabei war. Die letzte Zeile vor der Wahl sagt
        ## nichts weiter, als dass alle zu dir sehen.
        ##
        ## Die Zeile der Kundigen ist die einzige, die nach MERKMALEN
        ## unterscheidet. Sie steht in der Vorrangfolge von variante()
        ## vor den Pfadschlüsseln: Wer in der Rüstung war, hört etwas
        ## anderes als wer im Lazarett war.

        Szene(
            "wirtshaus_1919", "Frühjahr 1919: Der Tisch",
            ort={"front": "Wirtshaus", "etappe": "Wirtshaus",
                 "heimat": "Wirtshaus"},
            zeilen=[
                erzaehlt({
                    "front": "Der erste Abend, an dem du wieder in einem Wirtshaus sitzt. Es riecht nach nassem Holz und dünnem Bier. An deinem Tisch sitzen vier Leute, von denen du zwei kennst.",
                    "etappe": "Der erste Abend, an dem du wieder in einem Wirtshaus sitzt. Es riecht nach nassem Holz und dünnem Bier. An deinem Tisch sitzen vier Leute, von denen du zwei kennst.",
                    "heimat": "Im Wirtshaus an der Ecke ist seit dem Frühjahr wieder offen. Es riecht nach nassem Holz und dünnem Bier. An deinem Tisch sitzen vier Leute, von denen du zwei kennst.",
                }),
                auftritt("rechts", "naechste"),
                erzaehlt(
                    "Am Kopfende sitzt einer, den niemand vorgestellt hat. Er redet seit einer Weile lauter als die anderen."
                ),
                erzaehlt(
                    "„Im Felde ist das Heer unbesiegt geblieben“, sagt er und stellt das Glas ab. „Zusammengebrochen ist es zu Hause.“"
                ),
                sagt("naechste", {
                    "front": "Er war nicht da. Das hört man.",
                    "etappe": "Frag ihn, wo er die vier Jahre gestanden hat.",
                    "heimat": "Der redet so, seit die Läden wieder aufhaben.",
                }),
                ich("Woher will er das wissen?"),
                erzaehlt(
                    "„Von denen, die es wissen müssen“, sagt er. „Es steht in der Zeitung, und es steht bald in jedem Buch.“"
                ),
                erzaehlt(
                    "Zwei am Tisch nicken. Einer von ihnen war nie fort."
                ),
                auftritt("links", "kundige"),
                sagt("kundige", {
                    "ruestung": "In der Halle haben sie bis November geschuftet. Frag die mal, wer zusammengebrochen ist.",
                    "offizier": "Sie sagen das jetzt überall. In den Kompanien hat es anders ausgesehen.",
                    "lazarett": "Ich habe die Züge kommen sehen, jede Woche. Unbesiegt sah das nicht aus.",
                    "front": "Ich habe das Frühjahr mitgemacht. Danach war nichts mehr da.",
                    "etappe": "Ich habe die Listen geführt. Die Zahlen wurden jeden Monat kleiner.",
                    "heimat": "Ich habe vier Jahre angestanden. Von unbesiegt habe ich nichts gemerkt.",
                }),
                erzaehlt(
                    "Der Fremde hört nicht zu. Er wiederholt den Satz, langsamer, und sieht dabei in die Runde."
                ),
                erzaehlt(
                    "Der Wirt stellt zwei Gläser hin und sagt nichts dazu."
                ),
                erzaehlt({
                    "front": "Du hast vier Jahre lang gesehen, was vorn übrig blieb. Du legst die Hände um das Glas.",
                    "etappe": "Du hast vier Jahre lang aufgeschrieben, was ankam und was nicht. Du legst die Hände um das Glas.",
                    "heimat": "Du hast vier Jahre lang angestanden und die Listen im Flur gelesen. Du legst die Hände um das Glas.",
                }),
                sagt("naechste", {
                    "front": "Sag du was. Auf dich hören sie eher.",
                    "etappe": "Sag du was. Du hast die Zahlen gesehen.",
                    "heimat": "Sag du was. Du warst jeden Morgen dabei.",
                }),
                erzaehlt(
                    "Am Tisch wird es still. Vier Gesichter drehen sich zu dir, und der Wirt wischt schon ab."
                ),
            ]
        ),

    ]

    SZENEN_INDEX = {}
    for _szene in SZENEN:
        SZENEN_INDEX[_szene.kennung] = _szene


################################################################################
## 6. Zustandsvariablen
################################################################################

default buehne = {"links": None, "mitte": None, "rechts": None}
default buehne_stimmung = {"links": "neutral", "mitte": "neutral", "rechts": "neutral"}
default buehne_sprecher = None

default szene_aktuell = None
default szene_stelle = 0
default szene_ort = ""
default szene_hintergrund = "papier"
default szene_kopf = True

default probe_stelle = 0
default probe_wahl = None


################################################################################
## 7. Stile, Bewegungen, Bildschirme
################################################################################

init offset = -1

## Stile #######################################################################

style blase_name is default:
    font SCHRIFT_TITEL
    size 25
    bold True
    color FARBE_AKZENT
    kerning 1.2

style blase_zusatz is default:
    size 17
    italic True
    color FARBE_LINIE

style blase_text is default:
    size 30
    color FARBE_TINTE
    line_spacing 8

style ich_marke is default:
    size 16
    color FARBE_AKZENT
    kerning 2.4

style ich_name is default:
    font SCHRIFT_TITEL
    size 25
    bold True
    color FARBE_TINTE
    kerning 1.2

style ich_text is default:
    size 30
    color FARBE_TINTE
    line_spacing 8

style erzaehler_text is default:
    size 28
    italic True
    color FARBE_TINTE_MATT
    line_spacing 9
    text_align 0.5
    layout "subtitle"

style figur_schild is default:
    font SCHRIFT_TITEL
    size 19
    bold True
    color FARBE_TINTE_MATT
    text_align 0.5
    kerning 1.0

style figur_schild_still is figur_schild:
    bold False
    color FARBE_LINIE

style figur_pruefung is default:
    size 15
    color FARBE_LINIE
    text_align 0.5

## Bewegungen ##################################################################
##
## Der Sprecher steht aufrecht und in voller Farbe, alle anderen sind
## abgedunkelt und einen Fingerbreit tiefer.

transform figur_spricht:
    alpha 1.0
    yoffset 0

transform figur_still:
    alpha 0.85
    yoffset 10
    matrixcolor SaturationMatrix(0.30) * BrightnessMatrix(-0.24)

## Weiter-Zeichen. Bewusst eine Raute aus Farbflächen statt eines
## Schriftzeichens, damit es in jeder Schrift gleich aussieht.
##
## PAKET 7, SCHRITT 1, TEIL E.7 UND ENTSCHEIDUNG 18: Das Zeichen pulsierte bisher dauerhaft
## zwischen alpha 1,0 und 0,20, mit einem Takt von 1,25 Sekunden und ohne
## Ende. Die Animationsregeln der Verfassung schließen das aus: "Nichts
## wackelt dauerhaft, nichts blinkt, nichts pulsiert im Hintergrund."
##
## Von den drei erlaubten Wegen - beibehalten, verlangsamen, durch ein
## ruhendes Zeichen ersetzen - ist der dritte gewählt. Verlangsamen hätte
## das Pulsieren nur gedehnt, nicht beendet, und die Aufgabe des Zeichens
## erfüllt ein ruhendes genauso: Es erscheint erst, wenn der Satz zu Ende
## geschrieben ist, und sagt damit "hier ist mehr". Eine Dreizehnjährige
## liest daneben einen Text; was im Augenwinkel taktet, zieht den Blick vom
## Satz weg.
##
## DER NAME IST MITGEZOGEN (Entscheidung 18): aus "blase_blinken" ist
## "zeichen_wartet" geworden. Ein transform, der "blinken" heißt und nicht
## blinkt, ist die Art Falle, die in der übernächsten Sitzung jemanden eine
## Stunde kostet. Beide Fundstellen liegen in dieser Datei; außerhalb wird
## nur ZEICHEN_WEITER benutzt, und das heißt weiter so.
##
## Ohne Dauer braucht dieses Zeichen auch keine: Es kann am Schalter für die
## Bewegung nicht vorbeilaufen, weil es sich nicht bewegt.

transform zeichen_wartet:
    xoffset 12
    yoffset 7
    alpha 0.8

define ZEICHEN_WEITER = At(
    Transform(Solid(FARBE_AKZENT, xsize=13, ysize=13), rotate=45),
    zeichen_wartet
)

## Bühne #######################################################################
##
## Eigener Bildschirm, damit die Figuren zwischen den Zeilen stehen bleiben.
## Die Sprechblasen liegen mit höherem zorder darüber.

screen szenen_buehne():

    zorder 0

    add Solid(buehne_farbe("grund"))

    add Solid(buehne_farbe("boden"), xsize=1920, ysize=1080 - FIGUR_BODEN) ypos FIGUR_BODEN
    add Solid(buehne_farbe("linie"), xsize=1920, ysize=1) ypos FIGUR_BODEN

    for platz in PLAETZE:

        if buehne.get(platz):

            $ steh_kennung = buehne.get(platz)
            $ steh_stimmung = buehne_stimmung.get(platz, "neutral")
            $ steh_spricht = (buehne_sprecher == platz)

            fixed:
                xpos FIGUR_MITTE[platz]
                xanchor 0.5
                ypos FIGUR_BODEN - FIGUR_SCHILD
                yanchor 1.0
                xysize (FIGUR_BREITE, FIGUR_HOEHE)

                if steh_spricht:
                    add figur_bild(steh_kennung, steh_stimmung) at figur_spricht
                    add Solid(FARBE_AKZENT, xsize=FIGUR_BREITE, ysize=3) yalign 1.0
                else:
                    add figur_bild(steh_kennung, steh_stimmung) at figur_still

            vbox:
                xpos FIGUR_MITTE[platz]
                xanchor 0.5
                ypos FIGUR_BODEN - 2
                yanchor 1.0
                xsize FIGUR_BREITE + 80
                spacing 1

                if persistent.analysemodus:
                    text steh_kennung + " / " + steh_stimmung style "figur_pruefung" xsize FIGUR_BREITE + 80

                if steh_spricht:
                    text figur_name(steh_kennung) style "figur_schild" xsize FIGUR_BREITE + 80
                else:
                    text figur_name(steh_kennung) style "figur_schild_still" xsize FIGUR_BREITE + 80

    if szene_kopf:
        use zustandskopf(szene_ort)

    use eckmenue()
    use werthinweis()

## Sprechblase einer Nebenfigur ################################################

screen sprechblase(who, what):

    zorder 50

    $ blasen_platz = buehne_sprecher if buehne_sprecher in PLAETZE else "mitte"
    $ blasen_kennung = buehne.get(blasen_platz)
    $ blasen_mitte = blase_mitte(blasen_platz)

    ## Zipfel: zeigt von der Blase hinauf zur sprechenden Figur.
    add Transform(Solid(FARBE_AKZENT, xsize=30, ysize=30), rotate=45):
        xpos blasen_mitte + zipfel_versatz(blasen_platz)
        xanchor 0.5
        ypos BLASE_OBEN + 6
        yanchor 0.5

    frame:
        xpos blasen_mitte
        xanchor 0.5
        ypos BLASE_OBEN
        xsize BLASE_BREITE
        padding (38, 24, 38, 28)
        background rahmen_schatten(FARBE_PAPIER_HELL, FARBE_AKZENT, 3)

        vbox:
            xsize BLASE_BREITE - 76
            spacing 9

            hbox:
                spacing 16

                text figur_name(blasen_kennung) style "blase_name" yalign 1.0

                text figur_zusatz(blasen_kennung) style "blase_zusatz" yalign 1.0

                if persistent.analysemodus:
                    text figur_rolle(blasen_kennung) style "figur_pruefung" yalign 1.0

            add Solid(FARBE_AKZENT, xsize=90, ysize=2)

            text what id "what" style "blase_text" xsize BLASE_BREITE - 76

## Sprechblase der Spielfigur ##################################################
##
## Bewusst anders gerahmt und ohne Zipfel: Die Spielfigur steht nicht auf
## der Bühne, sondern ist die Kamera.

screen ich_blase(who, what):

    zorder 50

    frame:
        xalign 0.5
        ypos BLASE_OBEN
        xsize ICH_BREITE
        padding (46, 24, 46, 30)
        background rahmen_doppelt(FARBE_PAPIER_DUNKEL, FARBE_AKZENT, FARBE_LINIE_FEIN)

        vbox:
            xsize ICH_BREITE - 92
            spacing 9

            hbox:
                spacing 16
                text "DU" style "ich_marke" yalign 1.0
                text rollen_text() style "ich_name" yalign 1.0
                text berufs_text() style "blase_zusatz" yalign 1.0

            add Solid(FARBE_AKZENT, xsize=90, ysize=2)

            text what id "what" style "ich_text" xsize ICH_BREITE - 92

## Erzähltext ##################################################################

screen szenen_erzaehler(who, what):

    zorder 50

    frame:
        xalign 0.5
        ypos BLASE_OBEN
        xsize ERZAEHLER_BREITE
        padding (70, 30, 70, 34)
        background rahmen_oben(FARBE_PAPIER_DUNKEL, FARBE_AKZENT, 3)

        text what id "what" style "erzaehler_text" xsize ERZAEHLER_BREITE - 140 xalign 0.5

## Stimmen #####################################################################
##
## Alle drei tragen keinen festen Namen. Der Name entsteht im Bildschirm
## aus Bühnenzustand und aktueller_pfad. Dadurch kann keine Szene versehentlich
## an einen Figurennamen gebunden werden.

define szenen_stimme = Character(
    None,
    screen="sprechblase",
    what_style="blase_text",
    ctc=ZEICHEN_WEITER
)

define ich_stimme = Character(
    None,
    screen="ich_blase",
    what_style="ich_text",
    ctc=ZEICHEN_WEITER
)

define erzaehler_stimme = Character(
    None,
    screen="szenen_erzaehler",
    what_style="erzaehler_text",
    ctc=ZEICHEN_WEITER
)

init offset = 0


################################################################################
## 8. Ablauf
################################################################################
##
## Aufruf aus dem Spiel:
##
##     call szene_spielen("prolog_ankunft")
##
## Die Einbindung in den Kapitelablauf gehört zu Paket 3 und wird hier
## bewusst noch nicht vorgenommen.

label szene_spielen(kennung):

    $ szene_starten(kennung)

    ## Paket 7, Schritt 1: Die beiden festen Sekundenzahlen sind durch den
    ## benannten Übergang ersetzt. Die Szene beginnt und endet damit genauso
    ## wie jeder andere Bildwechsel im Spiel.
    with UEBERGANG_KARTE()

    while not szene_fertig():
        $ szene_schritt()

    $ szene_beenden()

    with UEBERGANG_KARTE()

    return


################################################################################
## 9. Dialogprobe (Werkzeug für die Entwicklung)
################################################################################
##
## Spielt alle Szenen aus Paket 1 hintereinander mit einer frei gewählten
## Lebenslage. Seit Paket 2 wird nicht mehr eine feste Figur gewählt,
## sondern die Kombination aus Milieu, Pfad und Stellung. Genau daran
## hängen die Textvarianten: Wer offizier, lazarett oder ruestung trägt,
## bekommt an mehreren Stellen andere Sätze.

screen dialogprobe_wahl():

    default probe_herkunft = "arbeiterschaft"
    default probe_pfad = "front"
    default probe_merkmal = None

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xpos 120
        ypos 70
        xsize 1680
        spacing 14

        text "Dialogprobe" style "abschnitt_titel" size 46 text_align 0.0 xalign 0.0

        add Solid(FARBE_AKZENT, xsize=220, ysize=3)

        text "Stelle eine Lebenslage zusammen. Danach laufen alle zwölf Szenen aus Paket 1 nacheinander durch. Der Analysemodus zeigt zusätzlich Kennung, Stimmung und Rolle an." style "abschnitt_text" text_align 0.0 xsize 1400

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
                text "Zusätzliches Merkmal" style "einstellung_label_text"
                vbox:
                    style_prefix "navigation"
                    textbutton "ohne":
                        action SetScreenVariable("probe_merkmal", None)
                        selected probe_merkmal is None
                    for kennung in ["offizier", "lazarett", "ruestung", "landwirtschaft"]:
                        textbutton kennung:
                            action SetScreenVariable("probe_merkmal", kennung)
                            selected probe_merkmal == kennung

        null height 40

        hbox:
            spacing 40
            style_prefix "weiter"
            textbutton "Szenen abspielen" action Return((probe_herkunft, probe_pfad, probe_merkmal))
            textbutton "Zurück zum Hauptmenü" action MainMenu(confirm=False)


label dialogprobe:

    $ zustand_zuruecksetzen()

    scene bg papier
    with UEBERGANG_KARTE()

    call screen dialogprobe_wahl

    $ probe_wahl = _return

    $ probe_lebenslage(probe_wahl[0], probe_wahl[1], probe_wahl[2])

    $ aktuelles_jahr = KAPITEL_JAHRE[0]
    $ probe_stelle = 0

    while probe_stelle < len(SZENEN):
        call szene_spielen(SZENEN[probe_stelle].kennung)
        $ probe_stelle = probe_stelle + 1

    jump dialogprobe


################################################################################
## 9. Ersatzprobe (Werkzeug für die Entwicklung)
################################################################################
##
## Zeigt, wo variante() und welttext() in die Rückfallebene gegriffen haben,
## seit das Spiel gestartet wurde. Die Liste ist leer, solange jeder Pfad
## seine eigene Fassung hat - und genau das ist das Ziel.
##
## Ins Hauptmenü kommt der Aufruf mit einer Zeile in screens.rpy, im Block
## "if persistent.analysemodus" des Bildschirms main_menu:
##
##     textbutton _("Ersatzprobe") action Start("ersatzprobe")

screen ersatzprobe_anzeige():

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xpos 110
        ypos 50
        xsize 1740
        spacing 12

        text "Ersatzprobe" style "abschnitt_titel" size 44 text_align 0.0 xalign 0.0

        add Solid(FARBE_AKZENT, xsize=220, ysize=3)

        text "Jede Stelle, an der eine Textfassung für den gespielten Pfad fehlte und eine andere eingesprungen ist. 'ersatz' heißt: die Etappe hat die Frontfassung bekommen. 'standard' heißt: es gibt eine allgemeine Fassung, aber keine für diesen Pfad. 'leer' heißt: es gab überhaupt nichts. Gezählt wird je Stelle; die Zahl in Klammern enthält die Bildschirmauffrischungen und taugt nur zum Vergleichen." style "abschnitt_text" size 21 text_align 0.0 xalign 0.0 xsize 1740

        hbox:
            spacing 24
            text ("Stellen: " + str(len(variantenersatz_protokoll))) style ("probe_fehlt" if variantenersatz_protokoll else "probe_zeile") size 24
            text ("Griffe insgesamt: " + str(variantenersatz_gesamt)) style "probe_zeile" size 24
            if len(variantenersatz_protokoll) >= VARIANTENERSATZ_HOECHSTZAHL:
                text ("Höchstzahl erreicht, weitere Stellen werden nicht mehr eingetragen") style "probe_fehlt" size 24

        frame:
            xsize 1740
            ysize 800
            padding (24, 20)
            background rahmen(FARBE_PAPIER_HELL, FARBE_LINIE_FEIN, 2)

            vbox:
                spacing 8

                hbox:
                    spacing 0
                    text "Funktion" style "probe_kopf" xsize 130
                    text "Zweig" style "probe_kopf" xsize 110
                    text "Pfad" style "probe_kopf" xsize 100
                    text "Jahr" style "probe_kopf" xsize 80
                    text "Ersatz" style "probe_kopf" xsize 110
                    text "Aufrufer" style "probe_kopf" xsize 420
                    text "Text" style "probe_kopf" xsize 500

                add Solid(FARBE_LINIE_FEIN, xsize=1680, ysize=1)

                viewport:
                    xsize 1680
                    ysize 710
                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 4

                        if not variantenersatz_protokoll:
                            text "Keine einzige Ersetzung. Jeder gespielte Pfad hatte seine eigene Fassung." style "probe_zeile"

                        for eintrag in variantenersatz_protokoll:
                            hbox:
                                spacing 0
                                text eintrag["funktion"] style "probe_zeile" xsize 130
                                text eintrag["zweig"] style ("probe_fehlt" if eintrag["zweig"] == "leer" else "probe_zeile") xsize 110
                                text eintrag["pfad"] style "probe_zeile" xsize 100
                                text str(eintrag["jahr"]) style "probe_zeile" xsize 80
                                text eintrag["schluessel"] style "probe_zeile" xsize 110
                                text (eintrag["aufrufer"] + "  (" + str(eintrag["anzahl"]) + ")") style "probe_zeile" xsize 420
                                text eintrag["text"] style "probe_zeile" xsize 500

    hbox:
        xpos 110
        yalign 0.955
        style_prefix "navigation"

        textbutton "Zurück zum Hauptmenü" action Return()


label ersatzprobe:

    scene bg papier

    call screen ersatzprobe_anzeige

    return

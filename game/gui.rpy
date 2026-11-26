init -50 python:

    ## Farbwelt ###############################################################

    FARBE_PAPIER = "#efe9dc"
    FARBE_PAPIER_HELL = "#f7f3ea"
    FARBE_PAPIER_DUNKEL = "#e2dbca"
    FARBE_TINTE = "#1f1c18"
    FARBE_TINTE_MATT = "#57514a"
    FARBE_LINIE = "#8d8578"
    FARBE_LINIE_FEIN = "#b6ae9e"
    FARBE_AKZENT = "#8a3324"
    FARBE_AKZENT_MATT = "#a85c4a"
    FARBE_DUNKEL = "#15130f"
    FARBE_DUNKEL_HELL = "#241f19"
    FARBE_BLUT = "#3d1010"
    FARBE_SEGMENT_LEER = "#cfc7b6"
    FARBE_TEXT_HELL = "#ded7c9"
    FARBE_FEHLEND = "#c02718"

    FARBEN_STUFE = ["#3f5b3a", "#6d6a3a", "#8a6a2c", "#8f4a20", "#7c1d14"]

    ## Feste Maße der Kopfleiste ##############################################
    ## Diese Werte werden von screens.rpy und von wert_spalte_mitte() genutzt.
    ## Wer hier etwas ändert, ändert die Tooltip-Position automatisch mit.

    KOPF_HOEHE = 204
    KOPF_RAND = 56
    KOPF_LEISTE_BREITE = 1450
    KOPF_SPALTE_BREITE = 318
    WERT_SPALTE_BREITE = 250
    WERT_SPALTE_ABSTAND = 24

    ## Bildmaße ###############################################################
    ##
    ## Zwei Tafeln mit verschiedenen Aufgaben. BILD_MASSE nennt das Maß, in
    ## dem eine Datei abzulegen ist; es steht in MEDIEN.md und richtet sich an
    ## den, der das Material sammelt. BILD_ANZEIGE nennt das Maß, in dem das
    ## Bild auf dem Bildschirm erscheint — nur diese Tafel liest der Code, und
    ## zwar allein in bild_masse_holen().
    ##
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
    ##
    ## Fällt eines von beiden später an, ist seine Zeile in einer Minute
    ## wieder da. "dokumente" bleibt und bekommt in Gruppe 2 seine aufrufende
    ## Stelle: Die Kartentypen machen daraus eine eigene Bildsorte. Ein
    ## abfotografiertes Blatt ist kein Szenenbild — es steht nah und fast
    ## quadratisch, nicht im Breitbild einer Szene.

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

    ## Schriften ##############################################################

    def schrift_waehlen(kandidaten, ersatz):
        for pfad in kandidaten:
            if renpy.loadable(pfad):
                return pfad
        return ersatz

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

    ## Wofür jede Schrift da ist - ebenfalls für MEDIEN.md, damit der, der
    ## das Material sammelt, weiß, was er sucht.
    SCHRIFT_ZWECK = {
        "SCHRIFT_FLIESS": "Fließtext und Bedienung; die Grundschrift",
        "SCHRIFT_TITEL": "Überschriften, Ereignistext, Kartentitel",
        "SCHRIFT_DOKUMENT": "Briefe und Vordrucke; wirkt geschrieben",
        "SCHRIFT_SCHMAL": "Aufdrucke: Stempel, Aktenzeichen, Rubriken",
    }

    SCHRIFT_FLIESS = schrift_waehlen(
        SCHRIFT_KANDIDATEN["SCHRIFT_FLIESS"],
        "DejaVuSans.ttf"
    )

    SCHRIFT_TITEL = schrift_waehlen(
        SCHRIFT_KANDIDATEN["SCHRIFT_TITEL"],
        SCHRIFT_FLIESS
    )

    SCHRIFT_DOKUMENT = schrift_waehlen(
        SCHRIFT_KANDIDATEN["SCHRIFT_DOKUMENT"],
        SCHRIFT_FLIESS
    )

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

    ## Rahmen #################################################################

    def rahmen(fuellung, randfarbe=None, staerke=2):
        if randfarbe is None:
            randfarbe = FARBE_LINIE
        seite = 60
        return Frame(
            Composite(
                (seite, seite),
                (0, 0), Solid(randfarbe, xsize=seite, ysize=seite),
                (staerke, staerke), Solid(fuellung, xsize=seite - staerke * 2, ysize=seite - staerke * 2)
            ),
            20, 20
        )

    def rahmen_leer(randfarbe=None, staerke=2):
        if randfarbe is None:
            randfarbe = FARBE_LINIE
        seite = 60
        return Frame(
            Composite(
                (seite, seite),
                (0, 0), Solid(randfarbe, xsize=seite, ysize=staerke),
                (0, seite - staerke), Solid(randfarbe, xsize=seite, ysize=staerke),
                (0, 0), Solid(randfarbe, xsize=staerke, ysize=seite),
                (seite - staerke, 0), Solid(randfarbe, xsize=staerke, ysize=seite)
            ),
            20, 20
        )

    def rahmen_doppelt(fuellung, aussenfarbe=None, innenfarbe=None, staerke=2, abstand=5):
        if aussenfarbe is None:
            aussenfarbe = FARBE_LINIE
        if innenfarbe is None:
            innenfarbe = FARBE_LINIE_FEIN
        seite = 100
        innen = staerke + abstand
        return Frame(
            Composite(
                (seite, seite),
                (0, 0), Solid(aussenfarbe, xsize=seite, ysize=seite),
                (staerke, staerke), Solid(fuellung, xsize=seite - staerke * 2, ysize=seite - staerke * 2),
                (innen, innen), Solid(innenfarbe, xsize=seite - innen * 2, ysize=seite - innen * 2),
                (innen + 1, innen + 1), Solid(fuellung, xsize=seite - (innen + 1) * 2, ysize=seite - (innen + 1) * 2)
            ),
            34, 34
        )

    def rahmen_oben(fuellung, randfarbe=None, staerke=3):
        if randfarbe is None:
            randfarbe = FARBE_LINIE
        seite = 60
        return Frame(
            Composite(
                (seite, seite),
                (0, 0), Solid(randfarbe, xsize=seite, ysize=staerke),
                (0, staerke), Solid(fuellung, xsize=seite, ysize=seite - staerke)
            ),
            20, 20
        )

    def rahmen_schatten(fuellung, randfarbe=None, staerke=3, versatz=10, schattenfarbe="#15130f38"):
        if randfarbe is None:
            randfarbe = FARBE_LINIE
        seite = 80
        gesamt = seite + versatz
        return Frame(
            Composite(
                (gesamt, gesamt),
                (versatz, versatz), Solid(schattenfarbe, xsize=seite, ysize=seite),
                (0, 0), Solid(randfarbe, xsize=seite, ysize=seite),
                (staerke, staerke), Solid(fuellung, xsize=seite - staerke * 2, ysize=seite - staerke * 2)
            ),
            30, 30
        )
    
    def rahmen_doppelt_schatten(fuellung, aussenfarbe=None, innenfarbe=None, staerke=2, abstand=5, versatz=10, schattenfarbe="#00000000"):
        if aussenfarbe is None:
            aussenfarbe = FARBE_LINIE
        if innenfarbe is None:
            innenfarbe = FARBE_LINIE_FEIN
        seite = 100
        innen = staerke + abstand
        gesamt = seite + versatz
        return Frame(
            Composite(
                (gesamt, gesamt),
                (versatz, versatz), Solid(schattenfarbe, xsize=seite, ysize=seite),
                (0, 0), Solid(aussenfarbe, xsize=seite, ysize=seite),
                (staerke, staerke), Solid(fuellung, xsize=seite - staerke * 2, ysize=seite - staerke * 2),
                (innen, innen), Solid(innenfarbe, xsize=seite - innen * 2, ysize=seite - innen * 2),
                (innen + 1, innen + 1), Solid(fuellung, xsize=seite - (innen + 1) * 2, ysize=seite - (innen + 1) * 2)
            ),
            34, 34
        )

    ## Schriftgröße für die letzte Reihe #######################################
    ##
    ## SEIT PAKET 8, SCHRITT 2.3. In der letzten Reihe sitzt jemand sechs
    ## Meter vom Beamer entfernt, und was dort nicht zu lesen ist, findet
    ## nicht statt.
    ##
    ## Gedreht wird an Ren'Pys eigener Einstellung `font size`, nicht an
    ## einer nachgebauten. Sie skaliert JEDEN Text im Spiel, auch die in
    ## Einlagen und im Merkbuch, ohne dass irgendwo eine Liste von Stilen
    ## gepflegt werden müsste — und eine solche Liste hätte spätestens beim
    ## nächsten neuen Stil ein Loch.
    ##
    ## GEMESSEN, bevor die Stufen festgelegt wurden: Der längste
    ## Ereignistext braucht bei Faktor 1,0 genau 201 Pixel Höhe, bei 1,3
    ## sind es 250 und bei 1,6 schon 289. Das Textfeld hat 250 zur
    ## Verfügung. Deshalb endet die Skala bei 1,3 und nicht höher: Was
    ## darüber liegt, wäre nicht mehr lesbarer, sondern nur noch
    ## abgeschnitten — und die Karte selbst wächst nicht mit.
    SCHRIFT_STUFEN = [
        ("normal", 1.0, "Normal"),
        ("gross", 1.15, "Groß"),
        ("sehr_gross", 1.3, "Sehr groß"),
    ]

    def schriftfaktor():
        """Der geltende Faktor, notfalls die Vorgabe."""
        wert = getattr(_preferences, "font_size", 1.0)
        try:
            return float(wert)
        except (TypeError, ValueError):
            return 1.0

    def schriftstufe_ist(faktor):
        """Ob diese Stufe gerade gewählt ist. Vergleich mit Spielraum,
        weil ein Fließkommawert nie genau trifft."""
        return abs(schriftfaktor() - faktor) < 0.02

    ## Was mitwachsen muss, wenn die Schrift wächst ############################
    ##
    ## Ren'Pys `font size` vergrößert die SCHRIFT, nicht das Layout. Das ist
    ## richtig so — sonst sähe man bei großer Schrift einfach ein größeres
    ## Bild und nicht mehr Text. Es heißt aber, dass jedes Feld mit fester
    ## Höhe zu klein wird, sobald der Text darin wächst.
    ##
    ## GEMESSEN, was ohne diese Funktionen passiert (Faktor 1,3): Die
    ## Kopfleiste bleibt 204 Pixel hoch, "Ein paar Leute" bricht auf zwei
    ## Zeilen um und schiebt sich über die Trennlinie; der Ereignistext
    ## wandert nach oben und überdeckt den Zustandssatz. Beides war auf dem
    ## Abzug deutlich zu sehen.
    ##
    ## Der Bildschirm ist 1080 Pixel hoch, und daran ändert keine
    ## Einstellung etwas. Also wird von unten gerechnet:
    ##
    ##   die KARTE steht fest. Sie ist 560 hoch und muss ganz sichtbar
    ##   sein — man kann nicht zwischen zwei Optionen wählen, von denen
    ##   man eine nur halb sieht.
    ##   die KOPFLEISTE wächst mit der Schrift, sonst quillt sie über.
    ##   der EREIGNISTEXT bekommt, was übrig bleibt, und scrollt in
    ##   seinem Feld, wenn das nicht reicht. Ein Erzähltext verträgt das:
    ##   man liest ihn von oben, und der Rest kommt mit dem Mausrad.

    def kopfhoehe():
        return int(round(KOPF_HOEHE * schriftfaktor()))

    def wert_spalte_breite():
        """Breiter, damit die Zustandssätze nicht umbrechen.

        Platz ist da: Vier Spalten zu 250 plus drei Abstände sind 1072 von
        1450 Pixeln der Kopfleiste. Selbst bei 1,3 bleiben es 1372.
        """
        return int(round(WERT_SPALTE_BREITE * schriftfaktor()))

    ## Die feste Zeile: Wo die Karten anfangen und wie viel darunter frei
    ## bleibt. 1080 - 560 - 26 = 494.
    KARTEN_YPOS = 494
    KARTEN_HOEHE = 560

    def ereignisstrich_ypos():
        return KARTEN_YPOS - 16

    def ereignisfeld_ypos():
        return kopfhoehe() + 12

    ## Die wirkliche Zeilenhöhe — gemessen, nicht geschätzt #################
    ##
    ## OFFENER PUNKT 97. Bis hierher rechnete das Feld mit
    ## "Schriftgröße + Zeilenabstand", also 34 + 10 = 44 Pixel je Zeile.
    ## Gemessen sind es 51: Eine Schrift ist höher als ihre Punktgröße —
    ## bei DejaVuSans etwa das 1,2-Fache —, und der Zeilenabstand kommt
    ## obendrauf. Die Folge stand im Abzug: Das Feld von 220 Pixeln hielt
    ## nicht fünf Zeilen, sondern 4,31, und die fünfte war waagerecht
    ## durchgeschnitten. **Auch bei normaler Schrift.** Die Zahl "fünf
    ## Zeilen" aus AUFGEFALLEN 77 war von Anfang an eine Zeile zu viel.
    ##
    ## Gemessen wird jetzt am gerenderten Text: zwei Zeilen minus eine
    ## Zeile ist der Vorschub, und der gilt für die Schrift, die wirklich
    ## geladen ist. Das überlebt den Tag, an dem in fonts/ echte Dateien
    ## liegen statt DejaVuSans — eine festgeschriebene Zahl täte das nicht.
    ##
    ## Gemessen wird einmal je Größe und Schriftstufe. Schlägt die Messung
    ## fehl (die Werkbank hat keine Grafikschicht, und Ren'Py sagt beim
    ## Vorausberechnen von Bildschirmen nein), greift die Rechnung mit dem
    ## gemessenen Faktor 1,205 — und wird NICHT gemerkt, damit die nächste
    ## Gelegenheit wieder misst.
    ZEILENHOEHE_GEMESSEN = {}
    ZEILENHOEHE_FAKTOR = 1.205
    ZEILENABSTAND_EREIGNIS = 10

    def ereignis_zeilenhoehe(size=None):
        if size is None:
            size = EREIGNIS_TEXT_GRUND
        stufe = int(round(schriftfaktor() * 100))
        schluessel = (size, stufe)
        if schluessel in ZEILENHOEHE_GEMESSEN:
            return ZEILENHOEHE_GEMESSEN[schluessel]

        try:
            eine = Text("Hgq", style="ereignis_text", size=size)
            zwei = Text("Hgq\nHgq", style="ereignis_text", size=size)
            hoch_eine = renpy.render(eine, 1440, 2000, 0, 0).get_size()[1]
            hoch_zwei = renpy.render(zwei, 1440, 2000, 0, 0).get_size()[1]
            vorschub = int(hoch_zwei) - int(hoch_eine)
        except Exception:
            vorschub = 0

        if 8 < vorschub < 400:
            ZEILENHOEHE_GEMESSEN[schluessel] = vorschub
            return vorschub

        ## Rückfallebene: gemessener Faktor, aufgerundet wie Ren'Py rundet.
        wirksam = int(size * schriftfaktor() + 0.5)
        return int(wirksam * ZEILENHOEHE_FAKTOR + 0.5) + ZEILENABSTAND_EREIGNIS

    def ereignisfeld_hoehe(text=None):
        """Der Rest zwischen Kopfleiste und Akzentstrich.

        Abgerundet auf volle Zeilen: Sonst endet das Feld mitten in einer
        Zeile, und die letzte sichtbare ist waagerecht durchgeschnitten.
        Eine halbe Zeile sieht nach Fehler aus; eine ganze sieht nach
        "hier geht es weiter" aus, und genau das ist gemeint.

        Der Text kommt mit, weil lange Fassungen eine Stufe kleiner
        gesetzt werden (ereignis_schriftgroesse). Ohne ihn rundete das
        Feld auf die Zeilen der großen Schrift und schnitte die kleine
        wieder an — dieselbe Falle, nur eine Ebene tiefer.
        """
        roh = max(120, ereignisstrich_ypos() - 14 - ereignisfeld_ypos())
        zeile = max(1, ereignis_zeilenhoehe(ereignis_schriftgroesse(text)))
        return max(zeile, (roh // zeile) * zeile)

    ## PAKET 8, SCHRITT 2.4: das Vertiefungsfeld im Onboarding.
    ##
    ## Es hat eine FESTE Höhe, und zwar aus einem Grund: Wüchse es mit dem
    ## Satz, der gerade darin steht, dann spränge der ganze Kasten jedes Mal,
    ## wenn der Zeiger einen der drei Grundsätze berührt — und mit ihm sprängen
    ## die drei Sätze darüber, also genau die Fläche, über der die Maus steht.
    ## Man jagte dem Satz hinterher, den man lesen will.
    ##
    ## Zwei Zeilen zu 23 Pixeln plus Zeilenabstand und Rand ergeben 104. Der
    ## längste der drei Sätze braucht 104 Zeichen und bleibt damit auch bei
    ## Faktor 1,3 zweizeilig; mitwachsen muss die Höhe trotzdem, weil
    ## font_size seit Schritt 2.3 jeden Text vergrößert, das Feld aber nicht.
    def vertiefungsfeld_hoehe():
        return int(round(104 * schriftfaktor()))

    ## PAKET 8, SCHRITT 2.4: der Platz für den Erklärkasten der Kopfleiste.
    ##
    ## GEMESSEN im Abzug: Bei Schriftstufe "sehr groß" ist der Kasten rund
    ## 950 Pixel hoch, die Kopfleiste beginnt bei 281 — die letzten drei
    ## Zeilen standen unter dem Bildrand, darunter die Zeile, die sagt, wie
    ## man den Kasten wieder zumacht. Ein Hinweis, den man nicht sehen kann,
    ## ist keiner.
    ##
    ## Die Antwort ist dieselbe wie beim Ereignistext in Schritt 2.3: Was
    ## nicht mehr passt, rollt in seinem eigenen Feld, statt abgeschnitten zu
    ## werden oder die Karte zu sprengen. Gerollt wird mit dem Mausrad, und
    ## das geht nur am angehefteten Kasten — der unter dem Zeiger hängende
    ## verschwände, sobald die Maus ihn verlässt. Das Anheften ist damit
    ## nicht Bequemlichkeit, sondern bei großer Schrift die Bedingung dafür,
    ## dass der ganze Text erreichbar ist.
    ##
    ## Abgezogen werden: der Abstand unter der Kopfleiste (16), ein Rand zum
    ## Bildboden (20), Polster oben und unten des Kastens (50) und die
    ## Schlusszeile, die außerhalb des Rollfelds stehen bleibt (46).
    def werthinweis_raum():
        return max(240, 1080 - (kopfhoehe() + 16) - 20 - 50 - 46)

    ## GEMESSEN am Abzug: Der höchste der vier Kästen ist bei Faktor 1,0
    ## 643 Pixel hoch — versorgung, weil seine Erklärung vier Zeilen braucht.
    ## 660 gibt etwas Luft, damit ein Wort mehr in einer Erklärung nicht
    ## sofort einen Rollbalken erzeugt.
    ##
    ## Ein viewport nimmt sich IMMER den Platz, den sein ymaximum erlaubt —
    ## er schrumpft nicht auf seinen Inhalt. Ohne diese Höhe stand unter dem
    ## letzten Satz ein handbreites leeres Feld (im Abzug nachgesehen).
    WERTHINWEIS_INHALT = 660

    def werthinweis_hoehe():
        """So hoch wie der Inhalt, höchstens so hoch wie der Platz."""
        return min(int(round(WERTHINWEIS_INHALT * schriftfaktor())), werthinweis_raum())

    ## 488 Inhalt + 14 Rollbalken + 8 Abstand + 62 Polster des Rahmens.
    ## Der Balken versteckt sich, solange nichts zu rollen ist
    ## (vscrollbar_unscrollable "hide"), die Breite bleibt trotzdem
    ## reserviert - sonst spränge der Kasten in der Breite, sobald jemand
    ## die Schriftstufe wechselt.
    WERTHINWEIS_BREITE = 572

    def werthinweis_xpos(schluessel):
        """Mitte über dem Wert, aber nie über den Bildrand hinaus.

        GEMESSEN im Abzug: Bei Schriftstufe "sehr groß" wandert die erste
        Wertspalte nach links (breitere Spalten, dieselbe Kopfleiste), ihre
        Mitte liegt bei 257. Ein 572 Pixel breiter Kasten mittig darüber
        begänne bei -29 und wäre am linken Rand angeschnitten. Deshalb die
        Klammer: Der Kasten zeigt weiter auf seinen Wert, solange er kann,
        und bleibt am Rand stehen, wenn er sonst hinausliefe.
        """
        rand = 20
        halb = WERTHINWEIS_BREITE // 2
        mitte = wert_spalte_mitte(schluessel)
        return min(max(mitte, rand + halb), 1920 - rand - halb)

    ## Die Papiersorte einer Entscheidungskarte ################################
    ##
    ## SEIT PAKET 8, SCHRITT 1. Die fünf Kartentypen sollen ohne eine einzige
    ## Bilddatei auseinanderzuhalten sein, und der Rahmen trägt davon den
    ## größten Teil: Man erkennt eine Zeitung am grauen Papier, bevor man ein
    ## Wort gelesen hat. Beim Überfahren wechselt überall nur die Randfarbe
    ## auf den Akzent — die Papiersorte bleibt dieselbe, sonst spränge die
    ## Karte unter der Maus in eine andere Sorte.

    def kartenpapier(kartentyp, ueberfahren=False):
        rand = FARBE_AKZENT if ueberfahren else FARBE_LINIE
        innen = FARBE_AKZENT if ueberfahren else FARBE_LINIE_FEIN

        if kartentyp == "feldpost":
            ## Ein leichter Bogen: ein Rand, kein zweiter Strich.
            return rahmen_schatten(
                "#fffdf8" if ueberfahren else FARBE_PAPIER_HELL, rand, 2)

        if kartentyp == "lebensmittel":
            ## Karton, nüchtern und ohne Schatten. Er lag in der Tasche.
            return rahmen(
                "#f4efe2" if ueberfahren else FARBE_PAPIER, rand, 2)

        if kartentyp == "zeitung":
            ## Zeitungspapier ist gräulicher als Schreibpapier.
            return rahmen(
                "#eae3d2" if ueberfahren else FARBE_PAPIER_DUNKEL, rand, 2)

        if kartentyp == "amtlich":
            ## Ein Vordruck steht im Doppelrahmen, ohne Schatten: Er liegt
            ## nicht lose auf dem Tisch, er ist zugestellt worden.
            return rahmen_doppelt(
                "#fffdf8" if ueberfahren else FARBE_PAPIER_HELL, rand, innen, 2, 5)

        ## "karte" — der Bogen, wie ihn Paket 7 hinterlassen hat.
        return rahmen_doppelt_schatten(
            "#fffdf8" if ueberfahren else FARBE_PAPIER_HELL, rand, innen,
            schattenfarbe="#15130f38" if ueberfahren else "#00000000")

    ## Gestrichelte Linien und Spaltensatz #####################################
    ##
    ## SEIT PAKET 8, SCHRITT 1, für die Kartentypen. Ren'Py kennt weder einen
    ## gestrichelten Strich noch Spaltensatz. Beides als Bilddatei zu lösen
    ## hieße, zwei weitere Dateien zu verlangen, die jemand ablegen muss
    ## (Regel 7) — also entstehen sie aus Bordmitteln.

    def linie_gestrichelt(breite, farbe=None, staerke=1, strich=7, luecke=5):
        """Eine waagerechte Perforation, wie sie eine Marke abtrennt.

        Zusammengesetzt aus lauter kleinen Flächen. Bei 468 Pixeln sind das
        rund vierzig Stück; sie entstehen einmal beim Bau des Bildschirms
        und nicht in jedem Einzelbild.
        """
        if farbe is None:
            farbe = FARBE_LINIE_FEIN
        teile = []
        stelle = 0
        while stelle < breite:
            laenge = min(strich, breite - stelle)
            teile.append((stelle, 0))
            teile.append(Solid(farbe, xsize=laenge, ysize=staerke))
            stelle = stelle + strich + luecke
        return Composite((breite, staerke), *teile)

    def linie_gestrichelt_senkrecht(hoehe, farbe=None, staerke=1, strich=7, luecke=5):
        if farbe is None:
            farbe = FARBE_LINIE_FEIN
        teile = []
        stelle = 0
        while stelle < hoehe:
            laenge = min(strich, hoehe - stelle)
            teile.append((0, stelle))
            teile.append(Solid(farbe, xsize=staerke, ysize=laenge))
            stelle = stelle + strich + luecke
        return Composite((staerke, hoehe), *teile)

    def rahmen_gestrichelt(breite, hoehe, farbe=None, staerke=1, strich=7, luecke=5):
        """Ein leeres, gestricheltes Feld — das Stempelfeld eines Vordrucks."""
        if farbe is None:
            farbe = FARBE_LINIE_FEIN
        return Composite(
            (breite, hoehe),
            (0, 0), linie_gestrichelt(breite, farbe, staerke, strich, luecke),
            (0, hoehe - staerke), linie_gestrichelt(breite, farbe, staerke, strich, luecke),
            (0, 0), linie_gestrichelt_senkrecht(hoehe, farbe, staerke, strich, luecke),
            (breite - staerke, 0), linie_gestrichelt_senkrecht(hoehe, farbe, staerke, strich, luecke)
        )

    def in_zwei_spalten(text):
        """Teilt einen Text an der Satzgrenze, die der Mitte am nächsten liegt.

        Zwei Textfelder nebeneinander sehen nur dann nach Zeitung aus, wenn
        der Umbruch an einem Satzende liegt und nicht mitten im Wort. Findet
        sich kein Satzende, wird am Leerzeichen vor der Mitte getrennt;
        findet sich auch das nicht, bleibt die zweite Spalte leer. Der Text
        geht dabei nie verloren — im schlechtesten Fall steht er ganz links.
        """
        if not text:
            return "", ""
        mitte = len(text) // 2
        beste = -1
        for zeichen in [". ", "! ", "? "]:
            stelle = text.find(zeichen)
            while stelle >= 0:
                ende = stelle + len(zeichen)
                if beste < 0 or abs(ende - mitte) < abs(beste - mitte):
                    beste = ende
                stelle = text.find(zeichen, ende)
        if beste < 0:
            beste = text.rfind(" ", 0, mitte)
        if beste <= 0:
            return text, ""
        return text[:beste].strip(), text[beste:].strip()

    ## Position der Hover-Erklärung ###########################################

    def wert_spalte_mitte(schluessel):
        ## Rechnet mit wert_spalte_breite() statt mit der Konstanten:
        ## Wächst die Spalte mit der Schrift, wandert die Hover-Erklärung
        ## mit. Sonst zeigte sie bei großer Schrift neben den Wert.
        if schluessel not in WERTE_REIHENFOLGE:
            return 960
        breite = wert_spalte_breite()
        anzahl = len(WERTE_REIHENFOLGE)
        stelle = WERTE_REIHENFOLGE.index(schluessel)
        gesamt = anzahl * breite + (anzahl - 1) * WERT_SPALTE_ABSTAND
        links = KOPF_RAND + (KOPF_LEISTE_BREITE - gesamt) // 2
        return links + stelle * (breite + WERT_SPALTE_ABSTAND) + breite // 2

    ## Bilder #################################################################

    def bild_pfad(kategorie, kennung):
        return "images/" + str(kategorie) + "/" + str(kennung) + ".png"

    def bild_vorhanden(kategorie, kennung):
        if not kennung:
            return False
        return renpy.loadable(bild_pfad(kategorie, kennung))

    ## Die Leerstelle ####################################################
    ##
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
    ##   im Analysemodus zusätzlich der gesuchte Pfad, wie bisher.
    ##
    ## Das Spiel sieht damit auch ohne eine einzige Bilddatei fertig aus,
    ## und die Bilder sind später eine Verbesserung statt einer Bedingung.

    def eckwinkel(laenge, staerke, farbe):
        """Vier Winkel in den Ecken - die Ecken eines eingeklebten Fotos."""
        seite = laenge
        return Composite(
            (seite, seite),
            (0, 0), Solid(farbe, xsize=seite, ysize=staerke),
            (0, 0), Solid(farbe, xsize=staerke, ysize=seite)
        )

    def bild_platzhalter(breite, hoehe, gesuchter_pfad):
        ## Die Winkel wachsen mit der Fläche, bleiben aber bescheiden:
        ## auf einem kleinen Portrait sollen sie nicht das Bild werden.
        laenge = max(10, min(26, int(min(breite, hoehe) / 7)))
        rand = max(8, int(laenge / 2))
        winkel = eckwinkel(laenge, 2, FARBE_LINIE_FEIN)

        teile = [
            rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE_FEIN, 2),
            Transform(winkel, pos=(rand, rand)),
            Transform(winkel, xzoom=-1.0, pos=(breite - rand, rand),
                      xanchor=1.0),
            Transform(winkel, yzoom=-1.0, pos=(rand, hoehe - rand),
                      yanchor=1.0),
            Transform(winkel, xzoom=-1.0, yzoom=-1.0,
                      pos=(breite - rand, hoehe - rand), xanchor=1.0,
                      yanchor=1.0),
        ]

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

        return Fixed(*teile, xysize=(breite, hoehe))

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

init offset = -2

init python:
    gui.init(1920, 1080)


define gui.accent_color = FARBE_AKZENT
define gui.idle_color = FARBE_TINTE_MATT
define gui.idle_small_color = FARBE_LINIE
define gui.hover_color = FARBE_TINTE
define gui.selected_color = FARBE_AKZENT
define gui.insensitive_color = "#8d857880"
define gui.text_color = FARBE_TINTE
define gui.interface_text_color = FARBE_TINTE

define gui.text_font = SCHRIFT_FLIESS
define gui.name_text_font = SCHRIFT_TITEL
define gui.interface_text_font = SCHRIFT_FLIESS

define gui.text_size = 34
define gui.name_text_size = 40
define gui.interface_text_size = 28
define gui.label_text_size = 34
define gui.notify_text_size = 24
define gui.title_text_size = 78

define gui.main_menu_background = None
define gui.game_menu_background = None

define gui.textbox_height = 300
define gui.textbox_yalign = 1.0

define gui.name_xpos = 360
define gui.name_ypos = 0
define gui.name_xalign = 0.0
define gui.namebox_width = None
define gui.namebox_height = None
define gui.namebox_borders = Borders(5, 5, 5, 5)
define gui.namebox_tile = False

define gui.dialogue_xpos = 402
define gui.dialogue_ypos = 90
define gui.dialogue_width = 1116
define gui.dialogue_text_xalign = 0.0

define gui.button_width = None
define gui.button_height = None
define gui.button_borders = Borders(8, 8, 8, 8)
define gui.button_tile = False
define gui.button_text_font = gui.interface_text_font
define gui.button_text_size = gui.interface_text_size
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color
define gui.button_text_xalign = 0.0

define gui.radio_button_borders = Borders(27, 6, 6, 6)
define gui.check_button_borders = Borders(27, 6, 6, 6)
define gui.confirm_button_text_xalign = 0.5
define gui.page_button_borders = Borders(15, 6, 15, 6)
define gui.quick_button_borders = Borders(15, 6, 15, 0)
define gui.quick_button_text_size = 21
define gui.quick_button_text_idle_color = gui.idle_small_color
define gui.quick_button_text_selected_color = gui.accent_color

define gui.choice_button_width = 1185
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(150, 8, 150, 8)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = gui.text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = FARBE_TINTE_MATT
define gui.choice_button_text_hover_color = FARBE_AKZENT

define gui.navigation_xpos = 80
define gui.skip_ypos = 15
define gui.notify_ypos = 68
define gui.choice_spacing = 33
define gui.navigation_spacing = 10
define gui.pref_spacing = 15
define gui.pref_button_spacing = 0
define gui.page_spacing = 0
define gui.slot_spacing = 18
define gui.main_menu_text_xalign = 0.0

define gui.frame_borders = Borders(8, 8, 8, 8)
define gui.confirm_frame_borders = Borders(60, 60, 60, 60)
define gui.skip_frame_borders = Borders(24, 8, 75, 8)
define gui.notify_frame_borders = Borders(24, 8, 60, 8)
define gui.frame_tile = False

define gui.bar_size = 34
define gui.scrollbar_size = 16
define gui.slider_size = 34
define gui.bar_tile = False
define gui.scrollbar_tile = False
define gui.slider_tile = False
define gui.bar_borders = Borders(6, 6, 6, 6)
define gui.scrollbar_borders = Borders(6, 6, 6, 6)
define gui.slider_borders = Borders(6, 6, 6, 6)
define gui.vbar_borders = Borders(6, 6, 6, 6)
define gui.vscrollbar_borders = Borders(6, 6, 6, 6)
define gui.vslider_borders = Borders(6, 6, 6, 6)
define gui.unscrollable = "hide"

define config.history_length = 250
define gui.history_height = 210
define gui.history_spacing = 0
define gui.history_name_xpos = 233
define gui.history_name_ypos = 0
define gui.history_name_width = 233
define gui.history_name_xalign = 1.0
define gui.history_text_xpos = 255
define gui.history_text_ypos = 3
define gui.history_text_width = 1110
define gui.history_text_xalign = 0.0

define gui.language = "unicode"


init python:

    @gui.variant
    def touch():
        gui.quick_button_borders = Borders(60, 21, 60, 0)

    @gui.variant
    def small():
        gui.text_size = 44
        gui.name_text_size = 52
        gui.notify_text_size = 36
        gui.interface_text_size = 42
        gui.button_text_size = 42
        gui.label_text_size = 48
        gui.textbox_height = 360
        gui.name_xpos = 120
        gui.dialogue_xpos = 135
        gui.dialogue_width = 1650
        gui.slider_size = 54
        gui.choice_button_width = 1860
        gui.choice_button_text_size = 44
        gui.navigation_spacing = 30
        gui.pref_button_spacing = 15
        gui.quick_button_text_size = 30

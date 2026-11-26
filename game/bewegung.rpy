################################################################################
## bewegung.rpy - Das Bewegungsvokabular
################################################################################
##
## Warum es diese Datei gibt: Bis Paket 7 lagen die vier bis sechs Bewegungen
## des Spiels dort, wo sie zufällig gebraucht wurden - in screens.rpy, in
## dialoge.rpy, in merkbuch.rpy -, jede mit ihrer eigenen Sekundenzahl. Wer
## Bewegung abschalten wollte, hätte an sechs Stellen suchen müssen, und die
## siebte hätte er übersehen. Deshalb gibt es ab jetzt genau einen Ort für das
## Vokabular und genau eine Funktion, die eine Dauer ausrechnet:
## bewegungszeit(). Keine Sekundenzahl steht mehr in einem Bildschirm.
##
## init -45, weil gui.rpy bei -50 die Farben und Rahmen setzt. Die Übergänge
## greifen auf FARBE_DUNKEL zu; sie müssen also nach gui.rpy stehen und vor
## allem, was sie benutzt. Die transform-Blöcke stehen auf Dateiebene, weil
## Ren'Py sie nicht in einem init-python-Block annimmt.
##
## Der zweite Block steht bei init 5 und damit NACH options.rpy (init 0). Er
## überschreibt die dort gesetzten Menü-Übergänge. Das ist die Arbeitsweise
## des Projekts: nicht in fremden Dateien herumschneiden, sondern in der
## eigenen Datei überschreiben.


## Vorgabe für die Bewegungsstufe. bewegungsstufe() fängt zusätzlich ab, dass
## in einer alten persistent-Datei etwas anderes steht.
default persistent.bewegung = "voll"


init -45 python:

    ## Die drei Stufen ########################################################
    ##
    ## "voll" ist die Vorgabe. "sparsam" ist für schwache Schulrechner und für
    ## den Beamer gedacht, "aus" für alle, die von Bewegung abgelenkt werden -
    ## und für die Vorführung, in der nichts wackeln soll. Bei "aus" wird
    ## nichts übersprungen und nichts weggelassen: Jede Bewegung dauert null
    ## Sekunden und steht damit sofort auf ihrem Endzustand.

    BEWEGUNG_STUFEN = ["voll", "sparsam", "aus"]

    BEWEGUNG_ANTEIL = {
        "voll": 1.0,
        "sparsam": 0.6,
        "aus": 0.0,
    }

    BEWEGUNG_BEZEICHNUNG = {
        "voll": "Voll",
        "sparsam": "Sparsam",
        "aus": "Aus",
    }

    BEWEGUNG_ERKLAERUNG = (
        "Karten legen sich auf den Tisch, Stempel setzen auf, ein Umschlag "
        "geht auf. Sparsam kürzt jede Bewegung auf gut die Hälfte. Aus zeigt "
        "sofort das fertige Bild. Am Spiel ändert sich nichts: Es wird nichts "
        "übersprungen und nichts weggelassen."
    )

    ## Die Grenzen der Verfassung #############################################
    ##
    ## Drei Klassen, seit Entscheidung 17. Die Zahlen stehen hier, damit die
    ## Bewegungsprobe sie messen kann, statt sie ein zweites Mal zu
    ## formulieren.
    ##
    ##   Handgriff    0,45  Was zwischen der Spielerin und ihrem nächsten
    ##                      Klick liegt. Die Grenze schützt die Hand.
    ##   Kapitel      0,8   Der Jahreswechsel. Er darf sich Zeit nehmen,
    ##                      weil danach ohnehin gelesen wird.
    ##   Rückmeldung  1,2   Was nur gesehen werden will und nichts aufhält.
    ##                      Gesehen werden dauert länger als angeklickt
    ##                      werden: Erst muss die Bewegung auffallen, dann
    ##                      wandert der Blick hin, dann wird gelesen.

    BEWEGUNG_HOECHSTDAUER = 0.45
    BEWEGUNG_HOECHSTDAUER_KAPITEL = 0.8
    BEWEGUNG_HOECHSTDAUER_RUECKMELDUNG = 1.2

    ## Der Versatz für gestaffelte Listen. Er steht hier und nicht im
    ## Bildschirm, weil auch er eine Dauer ist und durch bewegungszeit() muss.

    ZEILEN_VERSATZ = 0.05
    ZEILEN_HOECHSTENS = 8

    ## Die Dauern der drei Übergänge. UEBERGANG_KAPITEL und UEBERGANG_ENDE
    ## sind Kapitelwechsel im Sinne der Verfassung und dürfen daher bis 0,8.

    UEBERGANG_DAUER = {
        "karte": 0.28,
        "kapitel": (0.25, 0.10, 0.25),
        "ende": (0.30, 0.15, 0.35),
    }

    def bewegungsstufe():
        """Die gültige Stufe - notfalls die Vorgabe.

        Eine persistent-Datei aus einer älteren Fassung kann alles Mögliche
        enthalten. Wer hier nicht abfängt, bekommt einen KeyError mitten in
        einer Bewegung, und der fällt erst im Unterricht auf.
        """
        stufe = getattr(persistent, "bewegung", None)
        if stufe not in BEWEGUNG_ANTEIL:
            return "voll"
        return stufe

    def bewegungszeit(sekunden):
        """Die einzige Stelle, an der eine Bewegungsdauer entsteht.

        JEDE Bewegung im Projekt holt ihre Dauer hier. Steht in einem
        Bildschirm eine Sekundenzahl, dann ist sie an dieser Funktion vorbei
        entstanden - und die Bewegungsprobe beanstandet sie.
        """
        anteil = BEWEGUNG_ANTEIL[bewegungsstufe()]
        if anteil <= 0.0:
            return 0.0
        return round(float(sekunden) * anteil, 3)

    def bewegung_waehlen(stufe):
        """Stellt die Stufe um und zieht die Menü-Übergänge nach.

        Die Übergänge des Spielmenüs sind Ren'Py-Einstellungen und keine
        transforms; sie werden einmal gesetzt und nicht bei jedem Bild neu
        gelesen. Deshalb reicht es nicht, persistent.bewegung zu ändern.
        """
        if stufe in BEWEGUNG_ANTEIL:
            persistent.bewegung = stufe
        uebergaenge_nachziehen()

    ## Die drei Übergänge #####################################################
    ##
    ## Sie sind Funktionen und keine define-Zuweisungen, und das hat einen
    ## Grund: Ein define wird einmal beim Programmstart ausgerechnet. Ein
    ## Übergang, der auf den Schalter hören soll, muss aber bei jedem Aufruf
    ## neu entscheiden. Deshalb heißt es im Ablauf "with UEBERGANG_KARTE()".
    ##
    ## Bei "aus" liefern alle drei None. "with None" ist in Ren'Py der
    ## Übergang ohne Übergang - das neue Bild steht sofort da. Ein Dissolve
    ## mit der Dauer 0 wäre kein gültiger Übergang.

    def UEBERGANG_KARTE():
        """Kurzer Dissolve, zwischen zwei Entscheidungskarten."""
        dauer = bewegungszeit(UEBERGANG_DAUER["karte"])
        if dauer <= 0.0:
            return None
        return Dissolve(dauer)

    def UEBERGANG_KAPITEL():
        """Fade über FARBE_DUNKEL, beim Jahreswechsel."""
        aus, halt, ein = UEBERGANG_DAUER["kapitel"]
        aus = bewegungszeit(aus)
        halt = bewegungszeit(halt)
        ein = bewegungszeit(ein)
        if aus + halt + ein <= 0.0:
            return None
        return Fade(aus, halt, ein, color=FARBE_DUNKEL)

    def UEBERGANG_ENDE():
        """Langsamer Fade, vor dem Lebenslauf."""
        aus, halt, ein = UEBERGANG_DAUER["ende"]
        aus = bewegungszeit(aus)
        halt = bewegungszeit(halt)
        ein = bewegungszeit(ein)
        if aus + halt + ein <= 0.0:
            return None
        return Fade(aus, halt, ein, color=FARBE_DUNKEL)


################################################################################
## Das Vokabular
################################################################################
##
## Jeder transform nimmt seine Dauer als Parameter entgegen, damit der Aufruf
## "at karte_kommt(bewegungszeit(0.32))" lauten kann. Die Vorgabe hinter dem
## Gleichheitszeichen nennt die gedachte Dauer; sie ist Dokumentation und
## nicht der Weg, auf dem die Dauer ins Bild kommt.
##
## WER EINEN DIESER TRANSFORMS OHNE KLAMMERN AUFRUFT - "at karte_kommt" statt
## "at karte_kommt(bewegungszeit(0.32))" -, GEHT AM SCHALTER VORBEI. Die
## Bewegungsprobe in probe_alles.py sucht genau danach.
##
## Bei der Dauer 0 laufen alle Schritte in null Sekunden ab. Das Ergebnis ist
## der Endzustand, kein übersprungener Zwischenschritt.


## Die Entscheidungskarte legt sich auf den Tisch: Sie kommt von unten, ist
## einen Sekundenbruchteil schief und richtet sich aus. Anklickbar ist sie ab
## dem ersten Bild - der Versatz ist klein genug, dass die Maus trifft.
##
## rotate_pad False IST NICHT KOSMETIK, SONDERN NOTWENDIG. Ren'Py polstert
## ein gedrehtes Bild auf seine DIAGONALE auf, damit bei 45 Grad keine Ecke
## abgeschnitten wird. Bei einer Karte von 520 mal 560 sind das
## Wurzel(520² + 560²) = 764 Pixel Kantenlänge - die Karte sitzt dann
## mittig in einem 764er Kasten und damit (764 - 560) / 2 = 102 Pixel
## tiefer, als der Bildschirm sagt.
##
## Genau das ist bis Paket 8 passiert: Die hbox stand auf ypos 448, die
## Karte sass bei 550 und ragte unten 30 Pixel aus dem Bild. Aufgefallen
## ist es nicht, weil der Versatz symmetrisch ist und unten nur leeres
## Papier abgeschnitten wurde - erst das Stempelfeld des amtlichen
## Vordrucks hat die Zone sichtbar gemacht (AUFGEFALLEN 76).
##
## Bei 1,2 Grad wird keine Ecke abgeschnitten: Der Ueberstand einer um 1,2
## Grad gedrehten Karte betraegt 560 * sin(1,2°) = 11,7 Pixel in der
## Breite, und die deckt der Rahmen des Buttons ab. Wer den Winkel je
## deutlich vergroessert, muss das hier neu bedenken.

transform karte_kommt(dauer=0.32):
    rotate_pad False
    yoffset 34
    alpha 0.0
    rotate 1.2
    easeout dauer yoffset 0 alpha 1.0 rotate 0.0


## Die gewählte Karte wird vom Tisch genommen.

transform karte_geht(dauer=0.22):
    yoffset 0
    alpha 1.0
    easein dauer yoffset -18 alpha 0.0


## Der Stempel setzt auf: groß heruntergeführt, einen Hauch zu tief, dann auf
## Maß. Der Drehwinkel gehört NICHT hierher - er wird beim Erzeugen einmal
## fest gewürfelt und von außen mitgegeben, sonst zittert der Stempel bei
## jedem Neuzeichnen.

transform stempel_setzt(dauer=0.22):
    alpha 0.0
    zoom 1.6
    parallel:
        easeout dauer zoom 0.97
        easein (dauer * 0.27) zoom 1.0
    parallel:
        linear (dauer * 0.5) alpha 1.0


## Ein Plus- oder Minuszeichen steigt auf und wird durchsichtig. Die Farbe
## kommt von außen: Der transform weiß nicht, ob der Wert gestiegen oder
## gefallen ist, und soll es auch nicht wissen.
##
## 1,1 Sekunden, und das ist Absicht (Entscheidung 17). Dieses Zeichen ist
## keine Handbewegung, sondern eine Rückmeldung: Es liegt über einer Karte,
## die gerade gelesen wird, hält nichts auf und lässt sich wegklicken. Bei
## 0,45 Sekunden merkt man, dass sich etwas bewegt hat, aber nicht mehr was
## — und genau das ist der ganze Zweck des Zeichens.

transform wert_schwebt(dauer=1.1):
    yoffset 0
    alpha 1.0
    parallel:
        easeout dauer yoffset -46
    parallel:
        linear dauer alpha 0.0


## Ein Strich wächst von links nach rechts auf - der Rotstift auf der Zeile,
## der Balken im Rucksack.

transform strich_waechst(dauer=0.22):
    xanchor 0.0
    xzoom 0.0
    easeout dauer xzoom 1.0


## Das Jahresblatt kommt von oben. Es gehört zum Kapitelwechsel und darf
## deshalb länger dauern als 0,45 Sekunden.

transform kalenderblatt(dauer=0.5):
    yoffset -60
    alpha 0.0
    ease dauer yoffset 0 alpha 1.0


## Der Umschlag geht auf. Zweiteilig in einem Aufruf: Die Lasche klappt
## (rotate), der Bogen fährt heraus (yoffset). Wer den transform auf den
## Bogen legt, sieht beides zugleich.

## rotate_pad False aus demselben Grund wie bei karte_kommt: Sonst sitzt
## der Bogen mittig in einem Kasten von der Groesse seiner Diagonale und
## damit sichtbar zu tief. Bei 1,4 Grad wird nichts abgeschnitten.

transform umschlag_oeffnet(dauer=0.4):
    rotate_pad False
    alpha 0.0
    yoffset 26
    rotate -1.4
    parallel:
        easeout dauer yoffset 0 alpha 1.0
    parallel:
        ease dauer rotate 0.0


## Für Listen: Zeile 0 kommt sofort, jede weitere einen Wimpernschlag später.
## Ab der neunten Zeile kommen alle zugleich - sonst wartet man am Ende einer
## langen Liste sekundenlang auf den letzten Eintrag.
##
## Der Versatz geht ebenfalls durch bewegungszeit(), damit "aus" wirklich aus
## ist. Die Dauer bekommt der transform schon umgerechnet von außen; der
## Versatz kann es nicht, weil ZEILEN_VERSATZ in keinem Bildschirm stehen soll.

transform zeile_taucht_auf(nummer, dauer=0.18):
    alpha 0.0
    pause (bewegungszeit(min(nummer, ZEILEN_HOECHSTENS) * ZEILEN_VERSATZ))
    linear dauer alpha 1.0


## Beim Überfahren mit der Maus hebt sich der Knopf um zwei Pixel. Mehr
## nicht: Ein Knopf, der beim Zeigen aufleuchtet oder springt, bewertet die
## Entscheidung, die dahinter steht.

transform knopf_hebt(dauer=0.12):
    yoffset 0
    on hover:
        easeout dauer yoffset -2
    on idle:
        easeout dauer yoffset 0


################################################################################
## Die Menü-Übergänge nachziehen
################################################################################
##
## init 5 und damit nach options.rpy (init 0). Ohne diesen Block bliebe das
## Aufblenden des Spielmenüs auch bei "aus" stehen - und die Abnahme "bei aus
## bewegt sich nichts" wäre eine Behauptung statt einer Tatsache.

init 5 python:

    def uebergaenge_nachziehen():
        """Setzt die fünf Menü-Übergänge auf die gewählte Stufe."""
        config.enter_transition = UEBERGANG_KARTE()
        config.exit_transition = UEBERGANG_KARTE()
        config.intra_transition = UEBERGANG_KARTE()
        config.window_show_transition = UEBERGANG_KARTE()
        config.window_hide_transition = UEBERGANG_KARTE()

    uebergaenge_nachziehen()

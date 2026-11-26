init offset = -1


################################################################################
## Textstile
################################################################################

style default:
    properties gui.text_properties()
    language gui.language
    font SCHRIFT_FLIESS
    color FARBE_TINTE

## Kopfleiste

style kopf_marke is default:
    size 16
    color FARBE_LINIE
    kerning 2.5

style kopf_klein is default:
    size 19
    color FARBE_TINTE_MATT
    kerning 1.2

## PAKET 8, SCHRITT 2.4: der ruhige Hinweis in der Datumszeile. Erbt von
## kopf_klein, damit er sich in die Zeile einfügt, und trägt als einziges
## Zeichen die Akzentfarbe — er soll auffallen, ohne zu rufen.
style kopf_fingerzeig is kopf_klein:
    color FARBE_AKZENT
    italic True

style kopf_name is default:
    font SCHRIFT_TITEL
    size 23
    bold True
    color FARBE_TINTE
    text_align 1.0
    line_spacing 2

style kopf_beruf is default:
    size 17
    color FARBE_TINTE_MATT
    text_align 1.0

style wert_beschriftung is default:
    size 19
    color FARBE_TINTE_MATT
    kerning 1.4

style stufen_name is default:
    font SCHRIFT_TITEL
    size 24
    bold True

style analyse_wert is default:
    size 17
    color FARBE_LINIE

style zustandssatz is default:
    size 22
    italic True
    color FARBE_TINTE_MATT

style zustandssatz_marke is default:
    size 17
    bold True
    kerning 2.0

## Hover-Erklärung

style hinweis_titel is default:
    font SCHRIFT_TITEL
    size 23
    bold True
    color FARBE_AKZENT
    kerning 1.4

style hinweis_text is default:
    size 20
    color FARBE_TINTE
    line_spacing 4

style hinweis_zwischentitel is default:
    size 17
    color FARBE_LINIE
    kerning 2.0

style hinweis_stufe_name is default:
    font SCHRIFT_TITEL
    size 19
    bold True

style hinweis_stufe_text is default:
    size 18
    color FARBE_TINTE_MATT
    line_spacing 2

style hinweis_folge is default:
    size 19
    italic True
    color FARBE_TINTE_MATT
    line_spacing 3

## Ereignis und Karten

style ereignis_text is default:
    font SCHRIFT_TITEL
    size 34
    color FARBE_TINTE
    line_spacing 10
    text_align 0.5
    layout "subtitle"

style karte_titel is default:
    font SCHRIFT_TITEL
    size 28
    bold True
    color FARBE_AKZENT
    text_align 0.5
    layout "subtitle"

style karte_text is default:
    size 21
    color FARBE_TINTE_MATT
    line_spacing 5
    text_align 0.5
    layout "subtitle"

style karte_titel_links is karte_titel:
    text_align 0.0
    layout "greedy"

style karte_text_links is karte_text:
    text_align 0.0
    layout "greedy"

style karte_hinweis is default:
    size 19
    italic True
    color FARBE_LINIE
    text_align 0.5
    layout "subtitle"

style karte_stempel is default:
    font SCHRIFT_SCHMAL
    size 17
    bold True
    color FARBE_AKZENT
    kerning 2.0

style karte_nummer is default:
    font SCHRIFT_TITEL
    size 20
    bold True
    color FARBE_TINTE_MATT

## Das Wertefeedback, seit Paket 8, Schritt 2.2 ################################
##
## Der Name steht ruhig daneben, die Zahl trägt die Farbe. Beide sind klein
## genug, dass sie den Ausgangstext nicht überstimmen: Das Zeichen will
## gesehen und nicht gelesen werden, und es ist nach gut einer Sekunde weg.

style feedback_name is default:
    size 22
    color FARBE_TINTE_MATT

style feedback_zahl is default:
    font SCHRIFT_TITEL
    size 26
    bold True

## Die Kartentypen, seit Paket 8, Schritt 1 ####################################
##
## Jeder Typ bekommt so wenige eigene Stile wie möglich. Was gleich bleiben
## kann, erbt von karte_titel_links und karte_text_links; verschieden ist nur,
## was die Papiersorte wirklich verschieden macht. Eine Rubrik ist die
## gedruckte Beschriftung eines Vordrucks ("Akt.-Z.", "Feldpost-Nr.") und
## steht deshalb überall in derselben schmalen Schrift.

style karte_rubrik is default:
    font SCHRIFT_SCHMAL
    size 14
    color FARBE_LINIE
    kerning 1.6

## Feldpost: ein Brief ist geschrieben, nicht gesetzt.
style karte_feldpost_titel is karte_titel_links:
    font SCHRIFT_DOKUMENT
    size 26

style karte_feldpost_text is karte_text_links:
    font SCHRIFT_DOKUMENT
    size 20
    line_spacing 6

## Lebensmittelkarte: die Ziffern der abtrennbaren Abschnitte.
style karte_abschnitt is default:
    font SCHRIFT_SCHMAL
    size 15
    color FARBE_TINTE_MATT
    text_align 0.5

## Zeitung: die Balkenüberschrift steht hell auf dunkel, der Spaltentext
## enger als sonst. So setzt eine Zeitung, und so sieht man es von weitem.
style karte_balken_titel is default:
    font SCHRIFT_SCHMAL
    size 22
    bold True
    color FARBE_TEXT_HELL
    kerning 2.4
    text_align 0.5
    layout "subtitle"

style karte_spalte is karte_text_links:
    size 18
    line_spacing 2

## Amtlich: der Behördenkopf, gesperrt und in Versalien wie ein Briefkopf.
style karte_behoerde is default:
    font SCHRIFT_SCHMAL
    size 16
    bold True
    color FARBE_TINTE
    kerning 2.2

style karte_amtlich_text is karte_text_links:
    size 20

## Ausgang

style ausgang_marke is default:
    size 17
    color FARBE_LINIE
    kerning 2.5

style ausgang_titel is default:
    font SCHRIFT_TITEL
    size 32
    bold True
    color FARBE_AKZENT
    text_align 0.5
    layout "subtitle"

style ausgang_text is default:
    font SCHRIFT_TITEL
    size 32
    color FARBE_TINTE
    line_spacing 12
    text_align 0.5
    layout "subtitle"

## Abschnitte und Kapitel

style abschnitt_titel is default:
    font SCHRIFT_TITEL
    size 44
    bold True
    color FARBE_AKZENT
    text_align 0.5
    layout "subtitle"

style abschnitt_text is default:
    size 26
    color FARBE_TINTE_MATT
    line_spacing 9
    text_align 0.5
    layout "subtitle"

## PAKET 8, SCHRITT 2.4: die drei Grundsätze im Onboarding. Der Satz trägt
## die Titelschrift, weil er eine Überschrift ist und kein Fließtext; die
## Vertiefung darunter bleibt bewusst kleiner und matter — sie ist das
## Angebot, nicht die Botschaft.
style grundsatz_satz is default:
    font SCHRIFT_TITEL
    size 30
    bold True
    color FARBE_TINTE
    text_align 0.5
    layout "subtitle"

style grundsatz_mehr is default:
    size 23
    color FARBE_TINTE_MATT
    line_spacing 5
    text_align 0.5
    layout "subtitle"

style kapitel_marke is default:
    size 20
    color FARBE_LINIE
    kerning 3.0

style kapitel_jahr is default:
    font SCHRIFT_TITEL
    size 130
    bold True
    color FARBE_AKZENT
    text_align 0.5
    kerning 4.0

style tastenhinweis is default:
    size 18
    italic True
    color FARBE_LINIE
    text_align 0.5

## Ende

style ende_marke is default:
    size 18
    color FARBE_LINIE
    kerning 3.0

style ende_titel is default:
    font SCHRIFT_TITEL
    size 54
    bold True
    color FARBE_PAPIER
    text_align 0.5
    kerning 2.0

style ende_text is default:
    font SCHRIFT_TITEL
    size 27
    color FARBE_TEXT_HELL
    line_spacing 10
    text_align 0.5
    layout "subtitle"

style ende_bilanz is default:
    size 22
    color FARBE_TEXT_HELL
    line_spacing 7

style ende_bilanz_titel is default:
    font SCHRIFT_TITEL
    size 21
    bold True
    color FARBE_PAPIER
    kerning 2.0

style ende_wert_name is default:
    font SCHRIFT_TITEL
    size 23
    bold True
    color FARBE_TEXT_HELL

style ende_wert_stufe is default:
    font SCHRIFT_TITEL
    size 23
    bold True

style ende_wert_satz is default:
    size 20
    color FARBE_LINIE_FEIN
    line_spacing 3

style ende_fazit is default:
    size 24
    italic True
    color FARBE_TEXT_HELL
    line_spacing 5
    text_align 0.5
    layout "subtitle"

style ende_protokoll is default:
    size 20
    color FARBE_LINIE_FEIN
    line_spacing 6

## Hauptmenü

style menue_marke is default:
    size 21
    color FARBE_LINIE
    kerning 3.5

style menue_titel is default:
    font SCHRIFT_TITEL
    size 68
    bold True
    color FARBE_AKZENT
    layout "subtitle"

style menue_untertitel is default:
    size 25
    color FARBE_TINTE_MATT
    line_spacing 6

style menue_fuss is default:
    size 19
    color FARBE_LINIE
    kerning 1.2


################################################################################
## Schaltflächen
################################################################################

style weiter_button is default:
    background rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE, 2)
    hover_background rahmen(FARBE_AKZENT, FARBE_AKZENT, 2)
    padding (52, 16)

style weiter_button_text is default:
    font SCHRIFT_TITEL
    size 26
    color FARBE_TINTE
    hover_color FARBE_PAPIER
    kerning 1.5
    xalign 0.5

style dunkel_button is default:
    background rahmen(FARBE_DUNKEL, FARBE_LINIE, 2)
    hover_background rahmen(FARBE_AKZENT, FARBE_AKZENT, 2)
    padding (40, 14)

style dunkel_button_text is default:
    font SCHRIFT_TITEL
    size 24
    color FARBE_TEXT_HELL
    hover_color FARBE_PAPIER
    kerning 1.2
    xalign 0.5

## Der Menü-Knopf ist jetzt dauerhaft sichtbar, bleibt aber zurückhaltend.

style ecke_button is default:
    background rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE, 2)
    hover_background rahmen(FARBE_AKZENT, FARBE_AKZENT, 2)
    padding (26, 10)

style ecke_button_text is default:
    font SCHRIFT_TITEL
    size 22
    bold True
    color FARBE_TINTE_MATT
    hover_color FARBE_PAPIER
    kerning 1.4

style navigation_button is default:
    background None
    padding (0, 8)

style navigation_button_text is default:
    font SCHRIFT_TITEL
    size 34
    color FARBE_TINTE_MATT
    hover_color FARBE_AKZENT
    selected_color FARBE_AKZENT
    kerning 1.0

style einstellung_button is default:
    background None
    padding (0, 6)

style einstellung_button_text is default:
    size 26
    color FARBE_TINTE_MATT
    hover_color FARBE_TINTE
    selected_color FARBE_AKZENT

style einstellung_label_text is default:
    font SCHRIFT_TITEL
    size 28
    bold True
    color FARBE_TINTE
    kerning 1.5

style slider:
    ysize 26
    xsize 420
    left_bar Solid(FARBE_AKZENT)
    right_bar Solid(FARBE_SEGMENT_LEER)
    thumb Solid(FARBE_TINTE, xsize=6, ysize=26)
    thumb_offset 3

style vscrollbar:
    xsize 14
    base_bar Solid(FARBE_SEGMENT_LEER)
    thumb Solid(FARBE_LINIE)

style scrollbar:
    ysize 14
    base_bar Solid(FARBE_SEGMENT_LEER)
    thumb Solid(FARBE_LINIE)


################################################################################
## Dialogfenster (Grundlage für die Visual-Novel-Szenen)
################################################################################

style say_fenster is default:
    background rahmen_oben(FARBE_PAPIER_DUNKEL, FARBE_AKZENT, 3)
    xfill True
    ysize 300
    yalign 1.0
    padding (400, 34)

style say_name is default:
    font SCHRIFT_TITEL
    size 34
    bold True
    color FARBE_AKZENT
    kerning 1.2

style say_text is default:
    size 33
    color FARBE_TINTE
    line_spacing 10


################################################################################
## Zustandsanzeige
################################################################################

screen zustandsblock(schluessel):

    $ wert = zustand_lesen()[schluessel]
    $ stufe = stufe_von_wert(schluessel, wert)

    button:
        xsize wert_spalte_breite()
        padding (12, 10)

        ## PAKET 8, SCHRITT 2.4 (Teil B, Punkt 7): DIE VIER WERTE SEHEN
        ## JETZT AUS WIE VIER FELDER.
        ##
        ## Vorher stand hier "background None": Ohne Zeiger darauf gab es
        ## kein einziges Zeichen, dass an dieser Stelle etwas zu holen ist
        ## — wer nie zufällig darüberfuhr, erfuhr nie, was die Balken
        ## bedeuten. Der Auftrag beziffert, was das kostet: 19,2
        ## Prozentpunkte an der Front, 29,2 in der Heimat.
        ##
        ## Drei Zustände, drei Rahmen: ruhend eine feine Linie, unter dem
        ## Zeiger der kräftige Rahmen, angeheftet derselbe in Akzentfarbe.
        background (rahmen(FARBE_PAPIER_HELL, FARBE_AKZENT, 2) if wert_gepinnt == schluessel else rahmen_leer(FARBE_LINIE_FEIN, 1))
        hover_background rahmen(FARBE_PAPIER_HELL, FARBE_AKZENT, 2)
        keyboard_focus False

        ## Der Klick heftet die Erklärung an, der zweite nimmt sie wieder
        ## weg. Ohne das Anheften müsste die Maus die ganze Lesezeit über
        ## stillstehen.
        action SetVariable("wert_gepinnt", None if wert_gepinnt == schluessel else schluessel)

        ## Berührt reicht: Wer den Zeiger einmal hier hatte, braucht den
        ## Hinweis unter dem Datum nicht mehr. Die Abfrage davor spart die
        ## Neuzeichnung bei jeder weiteren Berührung.
        hovered (NullAction() if kopfleiste_entdeckt else SetVariable("kopfleiste_entdeckt", True))

        tooltip schluessel

        vbox:
            xsize wert_spalte_breite() - 24
            spacing 6

            fixed:
                xfill True
                ysize 23

                text WERT_BEZEICHNUNG[schluessel] style "wert_beschriftung" xalign 0.0 yalign 0.5

                if persistent.analysemodus:
                    text analyse_text(schluessel) style "analyse_wert" xalign 1.0 yalign 0.5

            ## Voll heißt gut, bei allen vier Werten (Entscheidung 4).
            ## Ob ein Segment steht, entscheidet segment_gefuellt() in
            ## script.rpy — die einzige Stelle im Projekt, die das weiß.
            hbox:
                spacing 6
                for feld in range(SEGMENTE_JE_BALKEN):
                    if segment_gefuellt(feld, stufe):
                        add Solid(FARBEN_STUFE[stufe], xsize=40, ysize=14)
                    else:
                        add Solid(FARBE_SEGMENT_LEER, xsize=40, ysize=14)

            text STUFEN_NAMEN[schluessel][stufe] style "stufen_name" color FARBEN_STUFE[stufe]


screen werthinweis():

    ## PAKET 8, SCHRITT 2.4: Was der Zeiger berührt, hat Vorrang vor dem,
    ## was angeheftet ist — sonst könnte man von einem angehefteten Wert
    ## aus die anderen drei nicht mehr ansehen.
    $ beruehrt = GetTooltip()
    $ hinweis_schluessel = beruehrt if beruehrt in WERT_ERKLAERUNG else wert_gepinnt

    ## Die Fangfläche für den angehefteten Kasten. Sie liegt unter der
    ## Erklärung und über der Karte und macht aus jedem Klick daneben ein
    ## Zumachen. Das ist nicht nur bequem, sondern notwendig: Ohne sie
    ## würde derselbe Klick, der die Erklärung schließen soll, eine Option
    ## wählen — unumkehrbar, in einem Spiel ohne Zurück.
    ##
    ## Sie beginnt erst unter der Kopfleiste. Die vier Felder bleiben
    ## anklickbar, damit man von einem Wert direkt zum nächsten wechseln
    ## kann, statt zwischendurch zumachen zu müssen.
    if wert_gepinnt:

        button:
            ypos kopfhoehe()
            xysize (1920, 1080 - kopfhoehe())
            background None
            keyboard_focus False
            action SetVariable("wert_gepinnt", None)

    if hinweis_schluessel in WERT_ERKLAERUNG:

        $ hinweis_stufe = stufe_von_wert(hinweis_schluessel, zustand_lesen()[hinweis_schluessel])

        frame:
            xpos werthinweis_xpos(hinweis_schluessel)
            xanchor 0.5
            ypos kopfhoehe() + 16
            xsize WERTHINWEIS_BREITE
            padding (26, 20, 36, 30)
            background rahmen_schatten("#fffdf8", FARBE_AKZENT, 3)

            vbox:
                xsize 510
                spacing 10

                ## PAKET 8, SCHRITT 2.4: Der Inhalt rollt, wenn er nicht mehr
                ## unter die Kopfleiste passt — siehe werthinweis_raum() in
                ## gui.rpy. Bei Schriftstufe "sehr groß" standen sonst die
                ## letzten drei Zeilen unter dem Bildrand.
                ##
                ## Mit sichtbarem Rollbalken, wie die neun anderen Rollfelder
                ## des Projekts: Ein Feld, das nur auf das Mausrad hört, sagt
                ## niemandem, dass darunter noch etwas steht. Der Balken
                ## verschwindet von selbst, wenn alles hineinpasst — bei
                ## normaler Schrift sieht man ihn also gar nicht.
                viewport:
                    xsize 510
                    ysize werthinweis_hoehe()
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    vscrollbar_unscrollable "hide"

                    vbox:
                        xsize 488
                        spacing 10

                        text WERT_BEZEICHNUNG[hinweis_schluessel] style "hinweis_titel"

                        add Solid(FARBE_LINIE_FEIN, xsize=488, ysize=1)

                        text WERT_ERKLAERUNG[hinweis_schluessel] style "hinweis_text" xsize 488

                        add Solid(FARBE_LINIE_FEIN, xsize=488, ysize=1)

                        ## PAKET 8, SCHRITT 2.1: Derselbe Balken wie in der
                        ## Kopfleiste, dazu der Satz, der ihn erklärt. Wer den
                        ## Zeiger über einen Wert hält, sieht dort oben einen
                        ## Balken — dann muss der Hover genau diesen Balken
                        ## erklären und nicht nur die Stufen aufzählen.
                        hbox:
                            spacing 6
                            for feld in range(SEGMENTE_JE_BALKEN):
                                if segment_gefuellt(feld, hinweis_stufe):
                                    add Solid(FARBEN_STUFE[hinweis_stufe], xsize=92, ysize=14)
                                else:
                                    add Solid(FARBE_SEGMENT_LEER, xsize=92, ysize=14)

                        text "Der Balken zeigt, wie viel dir noch bleibt." style "hinweis_text" xsize 488

                        add Solid(FARBE_LINIE_FEIN, xsize=488, ysize=1)

                        text "DIE FÜNF STUFEN" style "hinweis_zwischentitel"

                        vbox:
                            spacing 9

                            for stufe in range(5):

                                hbox:
                                    spacing 12

                                    ## Die Liste ist eine LEGENDE, kein Balken,
                                    ## und wird deshalb nicht mitgedreht: Sie
                                    ## zählt die fünf Stufen von der guten zur
                                    ## schlechten auf, und diese Reihenfolge
                                    ## trägt die Namen und die Sätze daneben.
                                    ## Bis Paket 8 waren hier alle Stufen bis
                                    ## zur erreichten gefärbt — das war ein
                                    ## zweiter Balken mit umgekehrter Richtung
                                    ## und stand ab jetzt im Widerspruch zum
                                    ## ersten. Jetzt trägt jede Zeile ihre
                                    ## eigene Farbe; kräftig steht die, in der
                                    ## man gerade ist.
                                    if stufe == hinweis_stufe:
                                        add Solid(FARBEN_STUFE[stufe], xsize=8, ysize=44)
                                    else:
                                        add Solid(FARBEN_STUFE[stufe] + "55", xsize=8, ysize=44)

                                    vbox:
                                        xsize 446
                                        spacing 2

                                        if stufe == hinweis_stufe:
                                            text STUFEN_NAMEN[hinweis_schluessel][stufe] + "  (jetzt)" style "hinweis_stufe_name" color FARBEN_STUFE[stufe] xsize 446
                                        else:
                                            text STUFEN_NAMEN[hinweis_schluessel][stufe] style "hinweis_stufe_name" color FARBE_TINTE_MATT xsize 446

                                        text STUFEN_KURZ[hinweis_schluessel][stufe] style "hinweis_stufe_text" xsize 446

                        add Solid(FARBE_LINIE_FEIN, xsize=488, ysize=1)

                        text WERT_FOLGE[hinweis_schluessel] style "hinweis_folge" xsize 488

                ## Nur im angehefteten Zustand, und AUSSERHALB des Rollfeldes:
                ## Ein Kasten, der von selbst verschwindet, braucht keine
                ## Anleitung; einer, der stehen bleibt, muss sagen, wie er
                ## wieder weggeht — und zwar sichtbar, ohne dass man erst
                ## dorthin rollen müsste.
                if wert_gepinnt == hinweis_schluessel:

                    add Solid(FARBE_LINIE_FEIN, xsize=510, ysize=1)

                    text "Klicke irgendwo daneben, um wieder zuzumachen." style "tastenhinweis" xsize 510


screen zustandskopf(ortsangabe=""):

    $ satz_schluessel = schwaechster_wert()
    $ satz_stufe = stufe_von_wert(satz_schluessel, zustand_lesen()[satz_schluessel])

    frame:
        background Solid(FARBE_PAPIER_DUNKEL)
        xfill True
        ysize kopfhoehe()
        yalign 0.0
        padding (KOPF_RAND, 12)

        hbox:
            xfill True
            spacing 40

            vbox:
                xsize KOPF_LEISTE_BREITE
                spacing 10

                fixed:
                    xfill True
                    ysize 22
                    text datum_text() style "kopf_klein" xalign 0.0 yalign 0.5
                    text ortsangabe style "kopf_klein" xalign 1.0 yalign 0.5

                    ## PAKET 8, SCHRITT 2.4 (Teil B, Punkt 7): DER RUHIGE
                    ## HINWEIS. Er steht in der freien Mitte der Datumszeile,
                    ## also unmittelbar über den vier Feldern, und zeigt damit
                    ## selbst dorthin. Kein eigener Kasten, keine Bewegung,
                    ## keine Fläche, die etwas verdeckt.
                    ##
                    ## Er geht weg, sobald der Zeiger einmal ein Feld berührt
                    ## hat, und spätestens mit dem ersten Kapitel. Ein Hinweis,
                    ## der auch im vierten Kapitel noch dasteht, ist keiner
                    ## mehr, sondern Möblierung.
                    if not kopfleiste_entdeckt and aktuelles_jahr == KAPITEL_JAHRE[0]:
                        text "Fahre mit der Maus über die vier Felder." style "kopf_fingerzeig" xalign 0.5 yalign 0.5

                hbox:
                    xalign 0.5
                    spacing WERT_SPALTE_ABSTAND
                    for schluessel in WERTE_REIHENFOLGE:
                        use zustandsblock(schluessel)

                hbox:
                    xalign 0.5
                    spacing 14

                    add Solid(FARBEN_STUFE[satz_stufe], xsize=4, ysize=26) yalign 0.5

                    text WERT_BEZEICHNUNG[satz_schluessel].upper() style "zustandssatz_marke" color FARBEN_STUFE[satz_stufe] yalign 0.5

                    text zustandssatz_text() style "zustandssatz" yalign 0.5

            vbox:
                xsize KOPF_SPALTE_BREITE
                yalign 0.0

                hbox:
                    xalign 1.0
                    spacing 18

                    vbox:
                        xsize 172
                        spacing 3
                        text "Deine Rolle" style "kopf_marke" xsize 172 text_align 1.0
                        text rollen_text() style "kopf_name" xsize 172
                        text berufs_text() style "kopf_beruf" xsize 172

                    frame:
                        padding (3, 3)
                        background Solid(FARBE_LINIE)
                        add portrait_anzeigen(portrait_kennung(), stimmung_bestimmen(), 122, 122)

    add Solid(FARBE_AKZENT, xsize=1920, ysize=3) ypos kopfhoehe()
    add Solid(FARBE_LINIE_FEIN, xsize=1920, ysize=1) ypos kopfhoehe() + 5


screen eckmenue():

    hbox:
        xalign 1.0
        yalign 1.0
        xoffset -30
        yoffset -22
        spacing 16
        style_prefix "ecke"

        ## Paket 4.1: Das Merkbuch. Es erscheint erst, wenn es in der
        ## Vorstellungsszene angelegt worden ist, und trägt einen Punkt,
        ## solange eine Sendung neu darin liegt.
        ##
        ## Show statt call screen: Dadurch lässt sich das Heft mitten in
        ## einer Szene, einem Brief oder einer Entscheidung aufschlagen,
        ## ohne den Ablauf zu unterbrechen.
        if merkbuch_verfuegbar():

            $ merkbuch_knopf = merkbuch_knopf_text()

            textbutton merkbuch_knopf:
                action [Function(merkbuch_oeffnen), Show("merkbuch_anzeige")]

        textbutton "Menü" action ShowMenu("preferences")


################################################################################
## Entscheidungskarten
################################################################################

screen entscheidungskarte(auswahl, stelle, vorlage=None):

    ## Paket 7, Schritt 1: Die Karte legt sich auf den Tisch. Sie ist dabei
    ## ab dem ersten Bild anklickbar - der Versatz ist klein genug, dass die
    ## Maus trifft, und niemand wartet auf das Ende der Bewegung.
    ##
    ## karten_entscheidung bekommt seine Bewegung hierüber: Der Bildschirm
    ## zeigt nichts anderes als diese Karten.
    ##
    ## PAKET 8, SCHRITT 1: Welches Papier die Karte ist, entscheidet der
    ## Kartentyp des EREIGNISSES - beide Karten einer Entscheidung zeigen
    ## dasselbe Dokument. Deshalb kommt die Vorlage jetzt mit herein. Sie
    ## darf fehlen: Dann ist es der Bogen von früher, und nichts bricht.
    ##
    ## Die Innenfläche ist bei allen fünf Typen 468 x 512 (520 x 560 abzüglich
    ## des Randes von 26 x 24). Jedes Blatt teilt genau diese 512 Pixel auf;
    ## wer eine Höhe ändert, muss eine andere anpassen.
    $ typ = getattr(vorlage, "kartentyp", "karte")

    button:
        xysize (520, 560)
        padding (26, 24)
        background kartenpapier(typ, False)
        hover_background kartenpapier(typ, True)
        action Return(stelle)
        at karte_kommt(bewegungszeit(0.32))

        vbox:
            xsize 468
            spacing 0

            if typ == "feldpost":
                use kartenblatt_feldpost(auswahl, vorlage)
            elif typ == "lebensmittel":
                use kartenblatt_lebensmittel(auswahl, vorlage)
            elif typ == "zeitung":
                use kartenblatt_zeitung(auswahl, vorlage)
            elif typ == "amtlich":
                use kartenblatt_amtlich(auswahl, vorlage)
            else:
                use kartenblatt_karte(auswahl, vorlage)


## Der Bogen - unverändert seit Paket 7. 264 + 22 + 226 = 512.

screen kartenblatt_karte(auswahl, vorlage):

    fixed:
        xysize (468, 264)

        add kartenmotiv(vorlage, auswahl, 468, 264)
        add rahmen_leer(FARBE_LINIE_FEIN, 2)

        if auswahl.hinweis:
            frame:
                xpos 16
                yalign 1.0
                yoffset -16
                padding (14, 7)
                background rahmen(FARBE_PAPIER_HELL, FARBE_AKZENT, 2)
                text auswahl.hinweis.upper() style "karte_stempel"

    null height 22

    fixed:
        xysize (468, 226)

        vbox:
            xsize 468
            yalign 0.5
            spacing 14

            text option_titel_von(auswahl) style "karte_titel_links" xsize 468

            add Solid(FARBE_AKZENT, xsize=64, ysize=3)

            text option_beschreibung_von(auswahl) style "karte_text_links" xsize 468


## Der Feldpostbogen. 31 + 1 + 12 + 178 + 14 + 1 + 14 + 261 = 512.
##
## Schmal wird der Bogen dadurch, dass rundum Papier stehen bleibt: Das Motiv
## ist 380 statt 468 breit. Klein sieht man nur im Vergleich zum Rand.
## Die Feldpostnummer steht als leere Rubrik da, und das ist Absicht - eine
## Nummer, die niemand belegen kann, wird hier nicht erfunden.

screen kartenblatt_feldpost(auswahl, vorlage):

    fixed:
        xysize (468, 31)

        hbox:
            xalign 1.0
            yalign 0.5
            spacing 8

            text "Feldpost-Nr." style "karte_rubrik" yalign 0.5
            add Solid(FARBE_LINIE_FEIN, xsize=86, ysize=1) yalign 1.0 yoffset -5

    add linie_gestrichelt(468, FARBE_LINIE_FEIN, 1)

    null height 12

    fixed:
        xysize (468, 178)

        fixed:
            xysize (380, 178)
            xalign 0.5

            add kartenmotiv(vorlage, auswahl, 380, 178)
            add rahmen_leer(FARBE_LINIE_FEIN, 1)

            if auswahl.hinweis:
                frame:
                    xpos 12
                    yalign 1.0
                    yoffset -12
                    padding (12, 6)
                    background rahmen(FARBE_PAPIER_HELL, FARBE_AKZENT, 2)
                    text auswahl.hinweis.upper() style "karte_stempel"

    null height 14

    ## Die Faltlinie. Ein Feldpostbrief wurde gefaltet, bevor er in den Sack
    ## kam; der Knick blieb.
    add Solid(FARBE_LINIE_FEIN, xsize=468, ysize=1)

    null height 14

    fixed:
        xysize (468, 261)

        vbox:
            xsize 468
            yalign 0.5
            spacing 12

            text option_titel_von(auswahl) style "karte_feldpost_titel" xsize 468

            text option_beschreibung_von(auswahl) style "karte_feldpost_text" xsize 468


## Die Lebensmittelkarte. 170 + 10 + 60 + 16 + 256 = 512.
##
## Eine Lebensmittelkarte war kein Blatt, sondern ein Bogen aus Marken: Wer
## etwas bekam, verlor einen Abschnitt. Fünf Felder genügen, um das zu zeigen.
## Die Ziffern sind Abschnittsnummern und behaupten nichts über die Ration.

screen kartenblatt_lebensmittel(auswahl, vorlage):

    fixed:
        xysize (468, 170)

        add kartenmotiv(vorlage, auswahl, 468, 170)
        add rahmen_leer(FARBE_LINIE_FEIN, 2)

        if auswahl.hinweis:
            frame:
                xpos 14
                yalign 1.0
                yoffset -12
                padding (12, 6)
                background rahmen(FARBE_PAPIER_HELL, FARBE_AKZENT, 2)
                text auswahl.hinweis.upper() style "karte_stempel"

    null height 10

    vbox:
        xsize 468
        spacing 0

        add linie_gestrichelt(464, FARBE_LINIE, 1) xalign 0.5

        hbox:
            xalign 0.5
            spacing 0

            for nummer in range(5):

                if nummer > 0:
                    add linie_gestrichelt_senkrecht(58, FARBE_LINIE, 1)

                fixed:
                    xysize (92, 58)
                    text str(nummer + 1) style "karte_abschnitt" align (0.5, 0.5)

        add linie_gestrichelt(464, FARBE_LINIE, 1) xalign 0.5

    null height 16

    fixed:
        xysize (468, 256)

        vbox:
            xsize 468
            yalign 0.5
            spacing 14

            text option_titel_von(auswahl) style "karte_titel_links" xsize 468

            add Solid(FARBE_AKZENT, xsize=64, ysize=3)

            text option_beschreibung_von(auswahl) style "karte_text_links" xsize 468


## Die Zeitung. 38 + 10 + 150 + 12 + 302 = 512.
##
## Der Titel steht oben im Balken statt unten unter dem Bild - eine Zeitung
## setzt ihre Überschrift nach oben. Die Beschreibung läuft in zwei Spalten,
## getrennt an einer Satzgrenze durch in_zwei_spalten().

screen kartenblatt_zeitung(auswahl, vorlage):

    fixed:
        xysize (468, 38)

        add Solid(FARBE_TINTE)
        text option_titel_von(auswahl) style "karte_balken_titel" align (0.5, 0.5) xsize 438

    null height 10

    fixed:
        xysize (468, 150)

        add kartenmotiv(vorlage, auswahl, 468, 150)
        add rahmen_leer(FARBE_LINIE_FEIN, 1)

        if auswahl.hinweis:
            frame:
                xpos 12
                yalign 1.0
                yoffset -10
                padding (12, 6)
                background rahmen(FARBE_PAPIER_DUNKEL, FARBE_AKZENT, 2)
                text auswahl.hinweis.upper() style "karte_stempel"

    null height 12

    $ spalte_links, spalte_rechts = in_zwei_spalten(option_beschreibung_von(auswahl))

    fixed:
        xysize (468, 302)

        hbox:
            xsize 468
            yalign 0.0
            spacing 11

            text spalte_links style "karte_spalte" xsize 222

            add Solid(FARBE_LINIE_FEIN, xsize=1, ysize=290)

            text spalte_rechts style "karte_spalte" xsize 222


## Der amtliche Vordruck. 34 + 2 + 12 + 150 + 12 + 190 + 12 + 100 = 512.
##
## Das Stempelfeld sass eine Zeit lang hoeher und liess die letzten vierzig
## Pixel frei: Bis zur Behebung von AUFGEFALLEN 76 stand jede Karte dreissig
## Pixel ueber dem unteren Bildrand, und in dieser Zone war das Feld
## angeschnitten. Die Ursache lag in rotate_pad (siehe bewegung.rpy) und ist
## behoben - die Karte sitzt jetzt dort, wo der Bildschirm es sagt, und das
## Feld darf wieder bis unten reichen.
##
## Links im Kopf die ausstellende Stelle: der Ort des Ereignisses, in
## Versalien und gesperrt wie ein Briefkopf. Rechts die Rubrik für das
## Aktenzeichen mit einer leeren Schreiblinie - ein Vordruck trägt sein
## Aktenzeichen erst, wenn ihn jemand ausgefüllt hat, und eine erfundene
## Nummer hätte im Unterricht nichts zu suchen.
##
## Der Hinweis wandert hier ins Stempelfeld: Wo ein Amt schreibt, steht der
## Vermerk im dafür vorgesehenen Feld und nicht als Zettel am Bildrand.

screen kartenblatt_amtlich(auswahl, vorlage):

    fixed:
        xysize (468, 34)

        text (vorlage.ort if vorlage and vorlage.ort else ort_text()).upper() style "karte_behoerde" xalign 0.0 yalign 0.5 xsize 258

        hbox:
            xalign 1.0
            yalign 0.5
            spacing 7

            text "Akt.-Z." style "karte_rubrik" yalign 0.5
            add Solid(FARBE_LINIE_FEIN, xsize=78, ysize=1) yalign 1.0 yoffset -5

    add Solid(FARBE_TINTE, xsize=468, ysize=2)

    null height 12

    fixed:
        xysize (468, 150)

        add kartenmotiv(vorlage, auswahl, 468, 150)
        add rahmen_leer(FARBE_LINIE_FEIN, 1)

    null height 12

    fixed:
        xysize (468, 190)

        vbox:
            xsize 468
            yalign 0.5
            spacing 10

            text option_titel_von(auswahl) style "karte_titel_links" xsize 468

            text option_beschreibung_von(auswahl) style "karte_amtlich_text" xsize 468

    null height 12

    fixed:
        xysize (468, 100)

        fixed:
            xysize (150, 90)
            xalign 1.0
            yalign 0.5

            add rahmen_gestrichelt(150, 90, FARBE_LINIE_FEIN, 1)

            if auswahl.hinweis:
                text auswahl.hinweis.upper() style "karte_stempel" align (0.5, 0.5) xsize 126 text_align 0.5
            else:
                text "Stempel" style "karte_rubrik" align (0.5, 0.5)


screen karten_entscheidung(kennung):

    $ vorlage = ereignis_holen(kennung)

    add Solid(FARBE_PAPIER)

    use zustandskopf(vorlage.ort if vorlage.ort else ort_text())

    ## PAKET 8: Das Feld hält jetzt fünf Zeilen statt knapp vier — 5 mal 44
    ## macht 220, dazu vier Pixel Luft. Vier von fünf Ereignistexten liefen
    ## vorher über, und bei fünf Zeilen stand die erste in der Kopfleiste
    ## (AUFGEFALLEN 77). Der Strich und die Karten rücken entsprechend nach
    ## unten; die Karte endet damit bei 1022 und hat 58 Pixel Luft.
    $ ereignistext = ereignis_text_von(vorlage)

    ## PAKET 8, SCHRITT 2.3: Das Feld hält 250 Pixel — genau so viel, wie
    ## der längste Text bei der größten Schriftstufe braucht (gemessen:
    ## 201 / 231 / 250 Pixel bei den Faktoren 1,0 / 1,15 / 1,3).
    ##
    ## Der viewport darunter ist das Netz und nicht der Normalfall: Solange
    ## der Text passt, ist er unsichtbar und ändert nichts. Passt er nicht
    ## — weil jemand später einen längeren Text schreibt —, schiebt sich
    ## der Rest mit dem Mausrad ins Bild, statt in der Kopfleiste zu landen
    ## oder abgeschnitten zu werden (AUFGEFALLEN 77).
    ##
    ## Kein Scrollbalken: Er säße quer über dem Erzähltext und wäre in
    ## neunundneunzig von hundert Fällen ein Balken ohne Zweck. Der
    ## erklärende Satz in den Einstellungen nennt das Mausrad.
    ## Alle Höhen kommen aus gui.rpy und wachsen mit der Schrift mit. Bei
    ## normaler Schrift ist das Feld 248 Pixel hoch, bei "sehr groß" rückt
    ## die Kopfleiste nach unten und es bleiben rund 190 — dann scrollt der
    ## Text in seinem Feld. Die Karte steht immer an derselben Stelle und
    ## ist immer ganz zu sehen.
    ##
    ## DER TEXT STEHT OBEN, NICHT MITTIG, und das ist der Unterschied
    ## zwischen lesbar und unbrauchbar: Ein zentrierter Text, der nicht
    ## passt, ragt an BEIDEN Enden heraus, und der viewport schneidet
    ## beide ab. Auf dem ersten Abzug bei großer Schrift fehlte dadurch der
    ## ganze erste Satz — man sah die Mitte eines Textes und merkte nicht,
    ## dass ein Anfang fehlt. Oben ausgerichtet fehlt höchstens das Ende,
    ## und das holt das Mausrad.
    viewport:
        xalign 0.5
        ypos ereignisfeld_ypos()
        xsize 1440
        ysize ereignisfeld_hoehe(ereignistext)
        mousewheel True

        vbox:
            xsize 1440

            text ereignistext style "ereignis_text" size ereignis_schriftgroesse(ereignistext) xalign 0.5 xsize 1440

    add Solid(FARBE_AKZENT, xsize=80, ysize=3) xalign 0.5 ypos ereignisstrich_ypos()

    hbox:
        xalign 0.5
        ypos KARTEN_YPOS
        spacing 80
        for stelle, auswahl in enumerate(vorlage.optionen):
            use entscheidungskarte(auswahl, stelle, vorlage)

    use eckmenue()
    use werthinweis()


screen karten_ausgang(kennung, stelle, ausgangstext):

    $ vorlage = ereignis_holen(kennung)
    $ auswahl = vorlage.optionen[stelle]

    add Solid(FARBE_PAPIER)

    use zustandskopf(vorlage.ort if vorlage.ort else ort_text())

    fixed:
        xalign 0.5
        ypos 240
        xsize 1400
        ysize 800

        vbox:
            align (0.5, 0.5)
            spacing 56

            ## Paket 7, Schritt 1: Auch der Ausgang ist ein Blatt, das sich
            ## legt. Es ist dieselbe Bewegung wie bei der Karte davor,
            ## damit der Bildschirmwechsel eine Fortsetzung ist und kein
            ## Schnitt.
            frame:
                xalign 0.5
                xsize 1280
                padding (72, 46)
                background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)
                at karte_kommt(bewegungszeit(0.32))

                vbox:
                    xsize 1136
                    spacing 22

                    text "Deine Entscheidung" style "ausgang_marke" xalign 0.5

                    text option_titel_von(auswahl) style "ausgang_titel" xalign 0.5 xsize 1136

                    add Solid(FARBE_AKZENT, xsize=180, ysize=3) xalign 0.5

                    text ausgangstext style "ausgang_text" xalign 0.5 xsize 1136

                    ## PAKET 8, SCHRITT 2.2 — das Wertefeedback.
                    ##
                    ## Was die Entscheidung gekostet oder gebracht hat,
                    ## steigt einmal auf und wird durchsichtig. Bis hierher
                    ## stand an dieser Stelle dieselbe Auskunft als nackter
                    ## Text und NUR im Analysemodus; sie war ein Vorläufer
                    ## und ist jetzt für alle da.
                    ##
                    ## Vier Dinge, die der Auftrag ausdrücklich verlangt:
                    ## Kein Ton. Seit Paket 8, Schritt 2.6 gibt es Ton im
                    ## Projekt, aber nur für Orte und Stellen im Ablauf -
                    ## nie für einen Ausgang (Regel 3, Auftragspunkt 14).
                    ## Hier gäbe es die einzige Stelle, an der ein Klang
                    ## eine Wahl bewerten könnte; deshalb steht der Satz
                    ## weiter hier und nicht als Selbstverständlichkeit.
                    ## Keine
                    ## Wertung im Text - nur der Name und die Zahl. Nichts
                    ## bei null: wirkung_zeilen() überspringt unveränderte
                    ## Werte, und bleibt die Liste leer, entsteht hier gar
                    ## kein Element. Und die Farbe kommt aus "schlechter"
                    ## und nicht aus dem Vorzeichen.
                    ##
                    ## Es sind dieselben zwei Farben wie auf der
                    ## Jahreskarte: Akzent für schlechter, die gute
                    ## Stufenfarbe für besser.
                    ##
                    ## Ein Sprung überspringt die Wertung ganz - dann ist
                    ## nichts zu melden.
                    if not letztes_ergebnis.get("sprung"):

                        $ feedback = wirkung_zeilen(letzte_aenderungen)

                        if feedback:
                            hbox:
                                xalign 0.5
                                spacing 44
                                at wert_schwebt(bewegungszeit(1.1))

                                for zeile in feedback:
                                    hbox:
                                        spacing 10
                                        text zeile["name"] style "feedback_name" yalign 0.5
                                        text zeile["zeichen"] style "feedback_zahl" color (FARBE_AKZENT if zeile["schlechter"] else FARBEN_STUFE[0]) yalign 0.5

            textbutton "Weiter":
                xalign 0.5
                style_prefix "weiter"
                action Return()
                at knopf_hebt(bewegungszeit(0.12))

    use eckmenue()
    use werthinweis()


################################################################################
## Kapitel, Einstieg, Auswahl
################################################################################

## HIER STAND BIS ZUM 5. SEPTEMBER 2026 DER BILDSCHIRM kapitelkarte.
##
## Er ist gelöscht (Entscheidung 19). Seit Paket 3 ruft ihn kein Ablauf mehr
## auf: An seine Stelle ist jahreskarte in kapitel.rpy getreten, die
## dasselbe zeigt und zusätzlich Zeitraum, Stichworte, die Frage des Jahres
## und die Wirkung des Jahreswechsels. Im ganzen Projekt gab es kein
## "call screen kapitelkarte" mehr.
##
## Ein Bildschirm, den niemand sieht, ist kein harmloser Rest: Paket 7 hat
## ihm eine Bewegung eingebaut, Paket 8 hätte ihm Bilder und Rückmeldung
## eingebaut, und beides wäre Arbeit an einem toten Ding gewesen. Wer ihn
## wiederhaben will, holt ihn aus dem Git-Verlauf.


screen hinweis_unumkehrbar():

    ## PAKET 8, SCHRITT 2.4 (Teil B, Punkte 5 und 6).
    ##
    ## VORHER standen hier zwei Absätze Fließtext, 350 Zeichen am Stück, und
    ## darunter noch einer über die Steuerung. Das ist der erste Bildschirm
    ## nach der Moduswahl; wer ihn in einer Doppelstunde vor sich hat, klickt
    ## ihn weg. Was auf ihm steht, ist aber die Spielregel selbst — dass es
    ## kein Zurück gibt, ist die Aussage des Spiels und nicht sein Kleingedrucktes.
    ##
    ## JETZT drei Sätze, jeder für sich, jeder in einem eigenen Feld. Wer
    ## mehr wissen will, fährt mit der Maus darüber und bekommt genau einen
    ## Satz mehr. Wer nicht, hat in fünf Sekunden alles gelesen.
    ##
    ## Der Bildschirm bringt sich dabei selbst bei, was die Kopfleiste später
    ## verlangt: Hier lernt man ohne Schaden, dass Überfahren etwas zeigt und
    ## Klicken es festhält (Punkt 7).

    default gewaehlter_satz = None

    ## Berührt schlägt angeheftet — dieselbe Vorrangfolge wie bei den vier
    ## Werten in der Kopfleiste, damit die Geste im ganzen Spiel dasselbe tut.
    $ beruehrt = GetTooltip()
    $ gezeigt = beruehrt if beruehrt in GRUNDSATZ_MEHR else gewaehlter_satz

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    frame:
        align (0.5, 0.5)
        xsize 1100
        padding (76, 54)
        background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

        vbox:
            xsize 948
            spacing 22

            text "Bevor du beginnst" style "abschnitt_titel" xalign 0.5 xsize 948

            add Solid(FARBE_AKZENT, xsize=200, ysize=3) xalign 0.5

            vbox:
                xsize 948
                spacing 12

                for kennung, satz in GRUNDSAETZE:

                    button:
                        xsize 948
                        padding (24, 16)
                        ## Zwei Pixel, nicht einer: Der Kasten steht mittig im
                        ## Bild, und bei ungerader Gesamthöhe verliert eine
                        ## Haarlinie an der Oberkante ihre Zeile - im Abzug war
                        ## der erste der drei Rahmen oben offen. Zwei Pixel
                        ## überstehen das, und auf sechs Meter Entfernung ist
                        ## eine Haarlinie ohnehin keine Linie mehr.
                        background (rahmen(FARBE_PAPIER, FARBE_AKZENT, 2) if gewaehlter_satz == kennung else rahmen_leer(FARBE_LINIE_FEIN, 2))
                        hover_background rahmen(FARBE_PAPIER, FARBE_AKZENT, 2)
                        keyboard_focus False
                        action SetScreenVariable("gewaehlter_satz", None if gewaehlter_satz == kennung else kennung)
                        tooltip kennung

                        text satz style "grundsatz_satz" xalign 0.5 xsize 900

            ## Feste Höhe, siehe vertiefungsfeld_hoehe() in gui.rpy: Ein Feld,
            ## das mit seinem Inhalt wächst, verschiebt die drei Sätze darüber
            ## — also die Fläche, über der die Maus gerade steht.
            frame:
                xsize 948
                ysize vertiefungsfeld_hoehe()
                padding (24, 16)
                background rahmen(FARBE_PAPIER, FARBE_LINIE_FEIN, 1)

                fixed:
                    xysize (900, vertiefungsfeld_hoehe() - 32)

                    if gezeigt in GRUNDSATZ_MEHR:
                        text GRUNDSATZ_MEHR[gezeigt] style "grundsatz_mehr" align (0.5, 0.5) xsize 900
                    else:
                        ## Dieselbe Größe wie die Vertiefung, nur kursiv: Die
                        ## Aufforderung ist der Satz, der die ganze Geste
                        ## beibringt - sie darf nicht die leiseste Zeile des
                        ## Bildschirms sein.
                        text GRUNDSATZ_AUFFORDERUNG style "grundsatz_mehr" italic True align (0.5, 0.5) xsize 900

            add Solid(FARBE_LINIE_FEIN, xsize=948, ysize=1)

            ## Die Steuerung in einer Zeile statt in einem Absatz, und mit dem
            ## Zeigefinger auf die Kopfleiste: Dort wird dieselbe Geste
            ## gebraucht, und dort kostet es etwas, sie nicht zu kennen.
            text "Du spielst nur mit der Maus. Oben stehen später vier Felder — fahre auch dort darüber, dann erfährst du, was sie bedeuten." style "abschnitt_text" size 22 xalign 0.5 xsize 948

            null height 6

            textbutton "Ich habe verstanden":
                xalign 0.5
                style_prefix "weiter"
                action Return()


screen moduskarte(kennung, titel, umfang, dauer, einsatz):

    button:
        xysize (560, 480)
        padding (36, 32)
        background rahmen_doppelt_schatten(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)
        hover_background rahmen_doppelt_schatten("#fffdf8", FARBE_AKZENT, FARBE_AKZENT, schattenfarbe="#15130f38")
        action Return(kennung)

        fixed:
            xysize (488, 416)

            vbox:
                xsize 488
                spacing 16

                text titel style "karte_titel" size 34 xsize 488

                add Solid(FARBE_LINIE_FEIN, xsize=180, ysize=2) xalign 0.5

                text umfang style "karte_text" size 24 xsize 488

                text dauer style "karte_text" size 24 xsize 488

                text einsatz style "karte_hinweis" size 21 xsize 488 yalign 1.0


screen modus_waehlen():

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    ## Alles liegt in einem einzigen vbox-Fluss. Kein ypos an den Kindern,
    ## sonst addieren sich die Werte und der Inhalt läuft unten aus dem Bild.
    vbox:
        xalign 0.5
        ypos 130
        xsize 1300
        spacing 16

        text "Zwischen Front und Heimat" style "abschnitt_titel" size 52 xalign 0.5 xsize 1300

        add Solid(FARBE_AKZENT, xsize=220, ysize=3) xalign 0.5

        text "Wähle den Umfang des Durchgangs." style "abschnitt_text" xalign 0.5 xsize 1300

        null height 44

        hbox:
            xalign 0.5
            spacing 90

            use moduskarte(
                "kurz",
                MODUS_BEZEICHNUNG["kurz"],
                MODUS_UMFANG["kurz"],
                MODUS_DAUER["kurz"],
                "Für einen Einstieg oder mehrere Durchgänge in einer Stunde."
            )

            use moduskarte(
                "lang",
                MODUS_BEZEICHNUNG["lang"],
                MODUS_UMFANG["lang"],
                MODUS_DAUER["lang"],
                "Für eine Doppelstunde mit anschließender Auswertung."
            )

        null height 24

        text "Auswahl mit einem Mausklick." style "tastenhinweis" xalign 0.5


################################################################################
## Endbildschirm
################################################################################

screen ende_bildschirm(titel, beschreibung):

    $ ende_breite = 1180 if persistent.analysemodus else 1400
    $ ende_xpos = 660 if persistent.analysemodus else 960

    add Solid(FARBE_DUNKEL)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xanchor 0.5
        xpos ende_xpos
        yalign 0.5
        xsize ende_breite
        spacing 18

        text "Ende des Durchgangs" style "ende_marke" xalign 0.5

        text titel style "ende_titel" xalign 0.5 xsize ende_breite

        add Solid(FARBE_AKZENT, xsize=300, ysize=3) xalign 0.5

        text beschreibung style "ende_text" xalign 0.5 xsize (ende_breite - 160)

        null height 2

        hbox:
            xalign 0.5
            spacing 30

            frame:
                xsize 480
                padding (28, 24)
                background rahmen(FARBE_DUNKEL_HELL, FARBE_LINIE, 2)

                vbox:
                    xsize 424
                    spacing 12

                    text "Lebenslauf" style "ende_bilanz_titel"

                    add Solid(FARBE_LINIE, xsize=424, ysize=1)

                    text lebenslauf_text() style "ende_bilanz" xsize 424

            frame:
                xsize 620
                padding (28, 24)
                background rahmen(FARBE_DUNKEL_HELL, FARBE_LINIE, 2)

                vbox:
                    xsize 564
                    spacing 14

                    text "Wie es dir am Ende geht" style "ende_bilanz_titel"

                    add Solid(FARBE_LINIE, xsize=564, ysize=1)

                    for eintrag in auswertung_liste():

                        vbox:
                            xsize 564
                            spacing 4

                            hbox:
                                spacing 14

                                text eintrag["name"] style "ende_wert_name" xsize 170 yalign 0.5

                                hbox:
                                    spacing 4
                                    yalign 0.5
                                    for feld in range(SEGMENTE_JE_BALKEN):
                                        if segment_gefuellt(feld, eintrag["stufe"]):
                                            add Solid(FARBEN_STUFE_HELL[eintrag["stufe"]], xsize=26, ysize=10)
                                        else:
                                            add Solid(FARBE_SEGMENT_DUNKEL, xsize=26, ysize=10)

                                text eintrag["stufenname"] style "ende_wert_stufe" color FARBEN_STUFE_HELL[eintrag["stufe"]] yalign 0.5

                            text eintrag["satz"] style "ende_wert_satz" xsize 564

        null height 2

        text auswertung_fazit() style "ende_fazit" xalign 0.5 xsize (ende_breite - 200)

        null height 6

        hbox:
            xalign 0.5
            spacing 40
            style_prefix "dunkel"

            textbutton "Von vorn beginnen" action Return("neustart")
            textbutton "Hauptmenü" action MainMenu(confirm=False)
            textbutton "Beenden" action Quit(confirm=True)

    if persistent.analysemodus:
        frame:
            align (1.0, 0.5)
            xoffset -40
            xsize 520
            ysize 700
            padding (26, 24)
            background rahmen(FARBE_DUNKEL_HELL, FARBE_LINIE, 2)

            vbox:
                spacing 12
                xsize 468

                text "Entscheidungsprotokoll" style "ende_bilanz_titel"

                add Solid(FARBE_LINIE, xsize=468, ysize=1)

                viewport:
                    xsize 468
                    ysize 600
                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    vbox:
                        xsize 440
                        text protokoll_text() style "ende_protokoll" xsize 440


################################################################################
## Haupt- und Spielmenü
################################################################################

screen main_menu():

    tag menu

    ## PAKET 8, SCHRITT 2.6. Die erste der Stellen aus Entscheidung 24. "on
    ## show" löst genau einmal aus, wenn der Bildschirm erscheint, und nicht
    ## bei jeder Neuauswertung — ein ton_spielen() im Rumpf eines Bildschirms
    ## liefe mehrfach. Solange MUSIK_EINGESCHALTET auf False steht, geschieht
    ## nichts; label start schaltet den Musikkanal beim Beginnen wieder still.
    on "show" action Function(musik_setzen, "hauptmenue")

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0
    add Solid(FARBE_LINIE_FEIN, xsize=1, ysize=1080) xpos 16

    vbox:
        xpos 120
        yalign 0.5
        xsize 1400
        spacing 0

        text "Ein Serious Game zum Ersten Weltkrieg" style "menue_marke"

        null height 20

        text "Zwischen Front und Heimat" style "menue_titel" xsize 1400

        null height 24

        add Solid(FARBE_AKZENT, xsize=260, ysize=3)

        null height 24

        text "Deutschland 1914 bis 1919. Woher du kommst, wählst du. Wohin der Krieg dich stellt, entscheiden andere." style "menue_untertitel" xsize 880

        null height 54

        vbox:
            style_prefix "navigation"
            spacing 12

            textbutton _("Beginnen") action Start()
            textbutton _("Einstellungen") action ShowMenu("preferences")

            ## Werkzeuge für die Entwicklung. Sie erscheinen nur, wenn der
            ## Analysemodus in den Einstellungen eingeschaltet ist.
            if persistent.analysemodus:
                textbutton _("Dialogprobe") action Start("dialogprobe")
                textbutton _("Sprachprüfung") action Start("sprachpruefung")
                textbutton _("Musterungsprobe") action Start("musterungsprobe")
                textbutton _("Bestandsprobe") action Start("bestandsprobe")
                textbutton _("Briefprobe") action Start("briefprobe")
                textbutton _("Einlagenprobe") action Start("einlagenprobe")
                ## Seit Paket 2, Schritt 1: zeigt, wo eine Textfassung für
                ## den gespielten Pfad gefehlt hat und eingesprungen wurde.
                textbutton _("Ersatzprobe") action Start("ersatzprobe")

            textbutton _("Beenden") action Quit(confirm=False)

    text "Version [config.version]" style "menue_fuss" xpos 120 yalign 0.94


screen game_menu(title):

    tag menu

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0
    add Solid(FARBE_LINIE_FEIN, xsize=1, ysize=1080) xpos 16

    vbox:
        xpos 120
        ypos 80
        xsize 1700
        spacing 22

        text title style "abschnitt_titel" size 52 text_align 0.0 xalign 0.0

        add Solid(FARBE_AKZENT, xsize=260, ysize=3)

        transclude

    hbox:
        xpos 120
        yalign 0.93
        spacing 46
        style_prefix "navigation"

        textbutton _("Zurück") action Return()

        if not main_menu:
            textbutton _("Hauptmenü") action MainMenu(confirm=True)

        textbutton _("Beenden") action Quit(confirm=True)

    ## Escape bleibt als einzige Taste erhalten, damit das Menü immer
    ## wieder geschlossen werden kann.
    key "game_menu" action Return()


screen preferences():

    tag menu

    use game_menu(_("Einstellungen")):

        vbox:
            spacing 34

            vbox:
                spacing 10
                text "Anzeige" style "einstellung_label_text"
                hbox:
                    spacing 40
                    style_prefix "einstellung"
                    textbutton _("Fenster") action Preference("display", "window")
                    textbutton _("Vollbild") action Preference("display", "fullscreen")

            add Solid(FARBE_LINIE_FEIN, xsize=960, ysize=1)

            ## Paket 7, Schritt 1: der Schalter für die Bewegung. Drei
            ## Stufen, drei Schaltflächen, alles mit der Maus. Die Stufe
            ## kommt aus bewegungsstufe(), damit ein ungültiger Wert in
            ## einer alten persistent-Datei hier nicht durchschlägt.
            vbox:
                spacing 10
                text "Bewegung" style "einstellung_label_text"
                hbox:
                    spacing 40
                    style_prefix "einstellung"
                    for stufe in BEWEGUNG_STUFEN:
                        textbutton BEWEGUNG_BEZEICHNUNG[stufe]:
                            action Function(bewegung_waehlen, stufe)
                            selected (bewegungsstufe() == stufe)
                text BEWEGUNG_ERKLAERUNG style "abschnitt_text" size 22 text_align 0.0 xsize 960

            add Solid(FARBE_LINIE_FEIN, xsize=960, ysize=1)

            vbox:
                spacing 10
                text "Auswertung" style "einstellung_label_text"
                vbox:
                    style_prefix "einstellung"
                    textbutton ("Analysemodus: eingeschaltet" if persistent.analysemodus else "Analysemodus: ausgeschaltet") action ToggleField(persistent, "analysemodus")
                    text "Der Analysemodus zeigt die verdeckten Werte, ihre Veränderung und das Entscheidungsprotokoll an. Für Vorbereitung und Auswertung gedacht, nicht für den ersten Durchgang." style "abschnitt_text" size 22 text_align 0.0 xsize 960

            add Solid(FARBE_LINIE_FEIN, xsize=960, ysize=1)

            ## PAKET 8, SCHRITT 2.3 — Schriftgröße und Vorlesen.
            ##
            ## Drei Knöpfe statt eines Schiebers: Ein Schieber verlangt
            ## Ziehen mit gedrückter Taste, drei Knöpfe verlangen einen
            ## Klick. Für eine Lehrkraft, die das im Stehen vor der Klasse
            ## einstellt, ist das der Unterschied.
            vbox:
                spacing 10
                text "Schriftgröße" style "einstellung_label_text"
                hbox:
                    style_prefix "einstellung"
                    spacing 16
                    for kennung, faktor, bezeichnung in SCHRIFT_STUFEN:
                        textbutton bezeichnung:
                            action Preference("font size", faktor)
                            selected schriftstufe_ist(faktor)
                text "Vergrößert jeden Text im Spiel. Für die letzte Reihe am Beamer. Bei „Sehr groß“ läuft nichts über — längere Texte lassen sich in ihrem Feld mit dem Mausrad weiterschieben." style "abschnitt_text" size 22 text_align 0.0 xsize 960

            add Solid(FARBE_LINIE_FEIN, xsize=960, ysize=1)

            ## Ren'Pys eigene Vorlesefunktion. KEIN Tastenhinweis (Regel 2),
            ## auch wenn Ren'Py selbst einen nennt.
            vbox:
                spacing 10
                text "Vorlesen" style "einstellung_label_text"
                vbox:
                    style_prefix "einstellung"
                    textbutton ("Vorlesen: eingeschaltet" if _preferences.self_voicing else "Vorlesen: ausgeschaltet"):
                        action Preference("self voicing", "toggle")
                text "Liest vor, was gerade auf dem Bildschirm steht, und nennt beim Überfahren mit der Maus auch die Schaltflächen. Gedacht für alle, denen Lesen schwerfällt." style "abschnitt_text" size 22 text_align 0.0 xsize 960

            add Solid(FARBE_LINIE_FEIN, xsize=960, ysize=1)

            vbox:
                spacing 10
                text "Textgeschwindigkeit" style "einstellung_label_text"
                bar value Preference("text speed") style "slider"

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


################################################################################
## Hilfsbildschirme
################################################################################

screen confirm(message, yes_action, no_action):

    modal True
    zorder 200

    add Solid("#15130fcc")

    frame:
        align (0.5, 0.5)
        xsize 900
        padding (60, 50)
        background rahmen_doppelt(FARBE_PAPIER, FARBE_AKZENT, FARBE_AKZENT)

        vbox:
            xsize 780
            spacing 32

            text _(message) style "abschnitt_text" size 30 color FARBE_TINTE xalign 0.5 xsize 780

            hbox:
                xalign 0.5
                spacing 50
                style_prefix "weiter"
                textbutton _("Ja") action yes_action
                textbutton _("Nein") action no_action

    key "game_menu" action no_action


screen notify(message):

    zorder 100

    frame:
        xalign 0.5
        ypos 40
        padding (24, 12)
        background rahmen(FARBE_AKZENT, FARBE_AKZENT, 2)
        at notify_erscheinen(bewegungszeit(0.25))
        text "[message!tq]" size 22 color FARBE_PAPIER

    ## 3,25 Sekunden ist eine Standzeit und keine Bewegung: So lange bleibt
    ## die Meldung lesbar stehen. Sie gehört deshalb nicht an bewegungszeit().
    timer 3.25 action Hide("notify")


## Seit Paket 7, Schritt 1 nimmt auch diese Bewegung ihre Dauer von außen.
## Das Ausblenden dauert doppelt so lang wie das Einblenden - eine Meldung,
## die sich davonstiehlt, reißt den Blick weniger vom Text weg.

transform notify_erscheinen(dauer=0.25):
    on show:
        alpha 0.0
        linear dauer alpha 1.0
    on hide:
        linear (dauer * 2.0) alpha 0.0


screen input(prompt):

    add Solid("#15130fcc")

    frame:
        align (0.5, 0.5)
        xsize 900
        padding (60, 50)
        background rahmen(FARBE_PAPIER, FARBE_LINIE, 3)

        vbox:
            xalign 0.5
            spacing 24
            text prompt size 28 color FARBE_TINTE xalign 0.5
            input id "input" size 30 color FARBE_AKZENT xalign 0.5


screen choice(items):

    vbox:
        align (0.5, 0.5)
        spacing 22

        for eintrag in items:
            textbutton eintrag.caption:
                style_prefix "weiter"
                action eintrag.action


screen say(who, what):

    window:
        id "window"
        style "say_fenster"

        vbox:
            spacing 12

            if who is not None:
                vbox:
                    spacing 6
                    text who id "who" style "say_name"
                    add Solid(FARBE_AKZENT, xsize=90, ysize=2)

            text what id "what" style "say_text"


screen quick_menu():
    null


screen skip_indicator():
    null

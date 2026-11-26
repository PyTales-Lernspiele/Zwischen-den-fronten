################################################################################
##
##  kapitel.rpy
##
##  Paket 3: Kapitelgerüst 1914 bis 1919 und Endensystem
##
##  Diese Datei erweitert das Spiel von drei auf sechs Abschnitte und
##  ersetzt den festen Schlussbildschirm durch einen berechneten Lebenslauf.
##
##      1914  Der Krieg beginnt
##      1915  Der Krieg wird Gewohnheit
##      1916  Das Jahr der Materialschlachten
##      1917  Hunger, Streik und ein neuer Gegner
##      1918  Das letzte Jahr
##      1919  Epilog: Was bleibt
##
##  Grundsätze, die in dieser Datei gelten:
##  - Steuerung ausschließlich mit der Maus. Keine key-Anweisungen.
##  - Ton nur am Lebenslauf. Seit Paket 8, Schritt 2.6 blendet
##    ende_lebenslauf den Umgebungsklang aus (ton_still) und fragt nach
##    Musik (musik_setzen) — die gibt es dort nur, wenn
##    MUSIK_EINGESCHALTET umgelegt ist. Der Lebenslauf bewertet nicht, und
##    ein Ton, der ihn bewertete, gäbe es hier ebenso wenig.
##  - Varianten laufen über merkmale und aktueller_pfad, niemals über
##    Figuren- oder Personennamen. Auch der Lebenslauf am Ende kennt keine
##    Namen, sondern nur Stufen, Pfad und Merkmale.
##  - Keine Begriffe aus der NS-Zeit. Die Sprachprüfung aus herkunft.rpy
##    wird in Abschnitt 12 so erweitert, dass sie ab jetzt auch die
##    Kapitel- und Endtexte erfasst.
##  - Kein Tod als Belohnung oder Strafe. Die harten Abbrüche entstehen
##    ausschließlich aus den vier Werten, nie aus einer einzelnen Wahl,
##    die als "falsch" markiert wäre.
##
##  ARBEITSWEISE
##  Diese Datei überschreibt bewusst einige Vorgaben und Funktionen aus
##  script.rpy, statt sie dort zu ändern. Das ist dasselbe Verfahren, das
##  herkunft.rpy in Paket 2 verwendet: Ein späterer init-Block gewinnt.
##  In script.rpy sind nur drei kleine Eingriffe nötig, weil Labels sich
##  nicht überschreiben lassen. Sie stehen in PAKET3_AENDERUNGEN.md.
##
##  OFFENE ABHÄNGIGKEIT ZU PAKET 7 UND 8
##  Das Gerüst für 1917, 1918 und 1919 steht vollständig, der
##  Ereignisbestand dieser Jahre ist aber noch leer. Ein Kapitel ohne
##  ziehbare Ereignisse endet deshalb sofort nach der Jahreskarte, statt
##  abzustürzen. Wie viel fehlt, zeigt die Bestandsprobe im Hauptmenü
##  (Analysemodus). Abschnitt 5 legt außerdem fest, welche Merkmale aus
##  1914 bis 1916 in den späten Jahren wieder aufgegriffen werden müssen.
##
################################################################################


################################################################################
## 1. Kapitelgerüst
################################################################################
##
## init -19 läuft nach den Vorgaben aus script.rpy (init -20) und
## überschreibt sie. KAPITEL_JAHRE, KAPITEL_UEBERSCHRIFT, KAPITEL_TEXT,
## KAPITEL_WIRKUNG und MODUS_ZIELZAHL stehen ab hier in dieser Datei.

init -19 python:

    KAPITEL_JAHRE = [1914, 1915, 1916, 1917, 1918, 1919]

    ## Der Epilog zählt als Kapitel, ist aber kein Kriegsjahr. Er trägt
    ## weniger Ziehungen und beendet den Durchgang mit dem Lebenslauf.
    EPILOG_JAHR = 1919

    KRIEGSJAHRE = [1914, 1915, 1916, 1917, 1918]

    KAPITEL_ZEITRAUM = {
        1914: "August bis Dezember 1914",
        1915: "Januar bis Dezember 1915",
        1916: "Januar bis Dezember 1916",
        1917: "Januar bis Dezember 1917",
        1918: "Januar bis November 1918",
        1919: "November 1918 bis Dezember 1919",
    }

    KAPITEL_UEBERSCHRIFT = {
        1914: "Der Krieg beginnt",
        1915: "Der Krieg wird Gewohnheit",
        1916: "Das Jahr der Materialschlachten",
        1917: "Hunger, Streik und ein neuer Gegner",
        1918: "Das letzte Jahr",
        1919: "Was bleibt",
    }

    ## Einführungstexte. Drei bis vier Sätze, sachlich, ohne Wertung.
    ## Jeder Text nennt mindestens eine Jahreszahl oder ein Datum, damit
    ## sich das Spiel im Unterricht an den Zeitstrahl anschließen lässt.
    KAPITEL_TEXT = {
        1914: (
            "Am 1. August wird die Mobilmachung angeordnet. In den Zeitungen steht, "
            "dass alle Parteien zusammenstehen; man nennt das den Burgfrieden. Vor "
            "den Meldestellen stehen die Männer bis auf die Straße, und fast alle "
            "rechnen mit einem Feldzug von wenigen Monaten."
        ),
        1915: (
            "Die Fronten haben sich eingegraben, von der Nordsee bis zur Schweizer "
            "Grenze. Im Februar werden in Berlin die ersten Brotkarten ausgegeben. "
            "Im April lässt die Heeresleitung bei Ypern zum ersten Mal Chlorgas "
            "abblasen. Die Rechnung mit dem kurzen Krieg ist nicht aufgegangen."
        ),
        1916: (
            "Verdun seit Februar, die Somme seit Juli. Beide Schlachten zusammen "
            "kosten mehr als eine Million Männer das Leben oder die Gesundheit, und "
            "keine Frontlinie verschiebt sich weit. Im August übernehmen Hindenburg "
            "und Ludendorff die Oberste Heeresleitung; ihr Rüstungsprogramm zieht "
            "noch mehr Menschen und Kohle aus dem Land. Zu Hause entscheidet nicht "
            "mehr das Geld über das Essen, sondern die Karte und der Platz in der "
            "Schlange."
        ),
        1917: (
            "Der Winter 1916 auf 1917 heißt später der Steckrübenwinter: Die "
            "Kartoffelernte ist verfault, und die Zuteilung besteht wochenlang aus "
            "Kohlrüben. Im April wird die Brotration gekürzt; in Berlin und Leipzig "
            "legen Hunderttausende die Arbeit nieder. Im selben Monat erklären die "
            "Vereinigten Staaten dem Deutschen Reich den Krieg. In Russland stürzt "
            "im März der Zar, im November übernehmen die Bolschewiki die Macht."
        ),
        1918: (
            "Im März greift das Heer im Westen noch einmal an, mit Truppen, die im "
            "Osten frei geworden sind. Bis zum Sommer ist der Angriff verbraucht. "
            "Seit dem Frühjahr geht eine Grippe um, an der besonders junge und "
            "ausgezehrte Menschen sterben. Anfang November meutern die Matrosen in "
            "Kiel. Am 9. November wird die Abdankung des Kaisers bekannt gegeben, "
            "am 11. November schweigen die Waffen."
        ),
        1919: (
            "Die Waffen schweigen, die Seeblockade nicht. Erst im März werden "
            "begrenzte Lebensmitteleinfuhren zugelassen, aufgehoben wird die "
            "Blockade im Juli. Am 19. Januar wählen Frauen zum ersten Mal, im "
            "Februar tritt in Weimar die Nationalversammlung zusammen. Für dich "
            "beginnt in diesem Jahr das, was danach kommt."
        ),
    }

    ## Drei Stichworte je Kapitel. Sie stehen klein unter dem Einführungs-
    ## text und dienen als Anschluss an das Schulbuch.
    KAPITEL_STICHWORTE = {
        1914: ["Mobilmachung", "Burgfrieden", "Marne"],
        1915: ["Stellungskrieg", "Brotkarte", "Gaskrieg"],
        1916: ["Verdun", "Somme", "Hilfsdienstgesetz"],
        1917: ["Steckrübenwinter", "Aprilstreik", "Revolution in Russland"],
        1918: ["Frühjahrsoffensive", "Grippe", "Novemberrevolution"],
        1919: ["Nationalversammlung", "Versailles", "Dolchstoßlegende"],
    }

    ## Rückblick am Jahresende. Er schließt das Kapitel ab und trägt die
    ## Ereignisse nach, die kein Alltagsereignis abbilden kann. Der Epilog
    ## bekommt keinen Rückblick, weil er selbst einer ist.
    KAPITEL_RUECKBLICK = {
        1914: (
            "Im September wird der Vormarsch an der Marne gestoppt. Bis Dezember "
            "gräbt sich die Front von der Nordsee bis zur Schweiz ein. Aus dem "
            "Feldzug von wenigen Monaten ist ein Krieg ohne Bewegung geworden. Die "
            "Verlustlisten in den Zeitungen werden von Woche zu Woche länger."
        ),
        1915: (
            "Nach dem Brot kommen Mehl, Butter und Kartoffeln unter Bewirtschaftung. "
            "Höchstpreise sollen die Preise halten und treiben die Ware in den "
            "Schwarzhandel. An der Front bleiben die Linien fast dort, wo sie im "
            "Januar lagen."
        ),
        1916: (
            "Verdun endet im Dezember ungefähr dort, wo es im Februar begonnen hat. "
            "Im selben Monat beschließt der Reichstag das Vaterländische "
            "Hilfsdienstgesetz. Jeder Mann zwischen 17 und 60 kann zur Arbeit "
            "verpflichtet werden, wenn er nicht Soldat ist. Die Kartoffelernte "
            "fällt aus. Der Winter, der jetzt beginnt, wird später der "
            "Steckrübenwinter heißen."
        ),
        1917: (
            "Im Juli fordert der Reichstag mit der Friedensresolution einen Frieden "
            "ohne Eroberungen; die Oberste Heeresleitung geht darüber hinweg. Im "
            "Dezember beginnen in Brest-Litowsk die Verhandlungen mit Russland. Wer "
            "im Westen liegt, hört, dass Truppen aus dem Osten kommen sollen."
        ),
        1918: (
            "Am 11. November wird in einem Eisenbahnwagen bei Compiègne der "
            "Waffenstillstand unterschrieben. Innerhalb weniger Tage entstehen "
            "Arbeiter- und Soldatenräte, die Front löst sich in Marschkolonnen auf. "
            "In vier Jahren sind rund zwei Millionen deutsche Soldaten gefallen. "
            "Wie viele Menschen in der Heimat an Unterernährung starben, wird bis "
            "heute geschätzt."
        ),
    }

    ############################################################################
    ## DER JAHRESBOGEN
    ############################################################################
    ##
    ## SEIT PAKET 3, SCHRITT 2. Das Spiel zieht Ereignisse aus einem Vorrat.
    ## Das hält es offen, aber ohne Ordnung bleibt es eine Folge von
    ## Episoden. Eine achte Klasse soll nach dem Spielen erzählen können,
    ## was ihrer Figur zugestoßen ist - in einer Reihenfolge, die einen Sinn
    ## ergibt. Der Jahresbogen legt diese Ordnung fest, BEVOR die
    ## Inhaltspakete Hunderte von Zeilen hinzufügen.
    ##
    ## Je Jahr und Pfad drei Angaben:
    ##
    ##   "frage"  Die eine Frage, die das Jahr an die Spielerin stellt. Ein
    ##            Satz, keine Wertung, keine Antwort darin. Sie steht auf
    ##            der Jahreskarte.
    ##   "kippt"  Was sich im Lauf des Jahres unwiderruflich verändert -
    ##            gleich, wie gewählt wurde. Steht im Jahresabschluss.
    ##   "träger" Die Ereignisse, die dieses Jahr tragen. Solange keines
    ##            davon gezogen wurde, bekommen sie in ereignis_gewicht()
    ##            einen Zuschlag. Kein Zwang: Die Ziehung bleibt offen, sie
    ##            bekommt nur ein Gefälle.
    ##
    ## SEIT PAKET 4, VORWEG heißt dieser Schlüssel "träger" und nicht mehr
    ## "kern". Der alte Name meinte etwas anderes als Ereignis.kern, das
    ## über die Ziehbarkeit im kurzen Verlauf entscheidet. Zwei Dinge unter
    ## einem Namen kosten früher oder später einen Fehler, den niemand
    ## sucht, weil beide Stellen richtig aussehen.
    ##
    ## Ein Träger, der im kurzen Verlauf gar nicht gezogen werden kann,
    ## trägt nichts: Sein Zuschlag bleibt bis zum Kapitelende offen und
    ## verhindert, dass die übrigen Ereignisse wieder gleichberechtigt zum
    ## Zug kommen. Jeder Träger hat deshalb kern=True; probe_alles.py prüft
    ## das seit Paket 4 nach.
    ##
    ## Die Fragen sind vom Alltag her gestellt, nicht von der Politik. 1916
    ## fragt nicht nach Verdun, sondern danach, wem die eigene Arbeit
    ## gehört; die Materialschlacht steht im Kapiteltext daneben.
    ##
    ## 1917 bis 1919 tragen leere kern-Listen, weil es dort noch keinen
    ## Bestand gibt. Frage und Kipppunkt stehen trotzdem schon da: Sie sind
    ## der Auftrag an die Pakete, die diese Jahre füllen.

    KAPITEL_BOGEN = {

        1914: {
            "front": {
                "frage": "Wie weit gehst du mit, solange alle mitgehen?",
                "kippt": "Aus dem Feldzug von wenigen Monaten ist ein Krieg ohne Bewegung geworden.",
                "träger": ["front_1914_marsch", "front_1914_erster_toter"],
            },
            "etappe": {
                "frage": "Wie weit gehst du mit, solange alle mitgehen?",
                "kippt": "Du bist Teil des Heeres geworden, ohne je im Graben gelegen zu haben.",
                "träger": ["front_feldpost"],
            },
            "heimat": {
                "frage": "Wie weit gehst du mit, solange alle mitgehen?",
                "kippt": "Wer fort ist, ist fort. Der Haushalt rechnet ab jetzt ohne ihn.",
                "träger": ["heimat_brotschlange", "heimat_1914_liebesgaben"],
            },
        },

        1915: {
            "front": {
                "frage": "Was tust du, wenn das erste Mal etwas fehlt?",
                "kippt": "Der Krieg hat eine Waffe bekommen, gegen die Mut nichts hilft.",
                "träger": ["front_gas", "front_kamerad"],
            },
            "etappe": {
                "frage": "Was tust du, wenn das erste Mal etwas fehlt?",
                "kippt": "Du siehst, was vorn ankommt, und was vorher unterwegs verschwindet.",
                "träger": ["front_feldpost", "heimat_lazarettzug"],
            },
            "heimat": {
                "frage": "Was tust du, wenn das erste Mal etwas fehlt?",
                "kippt": "Über das Essen entscheidet ab jetzt die Karte, nicht das Geld.",
                "träger": ["heimat_1915_brotkarte", "heimat_hamsterfahrt"],
            },
        },

        1916: {
            "front": {
                "frage": "Wem gehört dein Leben - dir oder der Stellung?",
                "kippt": "Der Krieg zählt keine Männer mehr, sondern Material und Meter.",
                "träger": ["front_1916_verdun", "front_1916_gefangener"],
            },
            "etappe": {
                "frage": "Wem gehört deine Arbeit - dir oder der Verwaltung?",
                "kippt": "Was du aufschreibst, gilt. Was du weglässt, hat es nicht gegeben.",
                "träger": ["front_1916_zaehlung", "front_urlaub"],
            },
            "heimat": {
                "frage": "Wem gehört deine Arbeit - dir oder der Verwaltung?",
                "kippt": "Die Kartoffelernte fällt aus. Der Winter, der kommt, hat schon einen Namen.",
                "träger": ["heimat_1916_rueben", "heimat_1916_kohle"],
            },
        },

        ## TRÄGER FÜR 1917 UND 1918 NACHGETRAGEN, Paket 5, Schritt 1.
        ##
        ## Der Kommentar oben sagte, diese Jahre trügen leere Listen,
        ## weil es dort noch keinen Bestand gebe. Seit Paket 4 stimmt das
        ## für Front und Heimat nicht mehr, seit Teil A auch für die
        ## Etappe nicht - die Listen blieben trotzdem leer. Zwei von
        ## sechs Kriegsjahren liefen damit ohne tragenden Moment: eine
        ## Folge von Episoden, genau das, was der Jahresbogen verhindern
        ## soll. Probe 1 konnte es nicht melden, weil sie nur prüfen
        ## kann, was in der Liste steht.
        ##
        ## Gewählt sind ausschliesslich FREIE Kernereignisse. Ein Träger
        ## mit Merkmalsbedingung kann ausbleiben, und dann bliebe sein
        ## Zuschlag bis zum Kapitelende offen und hielte alle übrigen
        ## Ereignisse klein - genau der Fehler, vor dem der Kommentar zu
        ## bogen_traeger_offen() warnt. heimat_1917_aprilstreik wäre
        ## thematisch der Träger von 1917 gewesen; er hängt an
        ## "vorangegangen" und scheidet deshalb aus.
        1917: {
            "front": {
                "frage": "Woher nimmst du, was du brauchst, wenn nichts mehr da ist?",
                "kippt": "Aus dem Osten kommen Truppen. Alle wissen, wofür sie gebraucht werden.",
                "träger": ["front_1917_steckruebe", "front_1917_geruecht_osten"],
            },
            "etappe": {
                "frage": "Woher nimmst du, was du brauchst, wenn nichts mehr da ist?",
                "kippt": "Die Etappe verwaltet den Mangel, statt den Nachschub zu verteilen.",
                "träger": ["etappe_1917_nachschubstockung", "etappe_verpflegungsausgabe"],
            },
            "heimat": {
                "frage": "Woher nimmst du, was du brauchst, wenn nichts mehr da ist?",
                "kippt": "Zum ersten Mal legen Hunderttausende die Arbeit nieder, und es geht ums Brot.",
                "träger": ["heimat_1917_kohlennot", "heimat_1917_metallsammlung"],
            },
        },

        ## 1918: NICHT der Waffenstillstand als Träger. Er ist das
        ## späteste Ereignis des Jahres, und ein Zuschlag würde ihn nach
        ## vorn ziehen - der Krieg endete dann mitten im Kapitel. Genommen
        ## sind die beiden Momente, an denen die Ordnung ins Rutschen
        ## kommt, ohne schon zu Ende zu sein.
        1918: {
            "front": {
                "frage": "Was gilt noch, wenn die Ordnung selbst ins Rutschen kommt?",
                "kippt": "Der letzte Angriff ist verbraucht. Ab jetzt geht es zurück.",
                "träger": ["front_1918_offensive", "front_1918_kokarde"],
            },
            "etappe": {
                "frage": "Was gilt noch, wenn die Ordnung selbst ins Rutschen kommt?",
                "kippt": "Die Formation löst sich auf, bevor ein Befehl dazu eintrifft.",
                "träger": ["etappe_1918_raeumung", "etappe_1918_grippe"],
            },
            "heimat": {
                "frage": "Was gilt noch, wenn die Ordnung selbst ins Rutschen kommt?",
                "kippt": "Am 9. November ist der Kaiser fort, und niemand hält ihn.",
                "träger": ["heimat_1918_januarstreik", "heimat_1918_matrosen"],
            },
        },

        ## TRÄGER FÜR 1919 NACHGETRAGEN, Paket 5, Schritt 3, Punkt 13a.
        ##
        ## Als der Bogen in Paket 2 entstand, war 1919 leer; seit Schritt 2
        ## dieses Pakets hat das Jahr acht Karten, die Trägerliste blieb
        ## trotzdem leer. Damit lief das Jahr, in dem das Spiel seine
        ## Auswertung leisten soll, als einziges ohne tragenden Moment.
        ## Probe 1 konnte es bis heute nicht melden - traeger_ohne_kern()
        ## prüft, ob ein eingetragener Träger taugt, nicht ob überhaupt
        ## einer dasteht. traeger_fehlend() schließt diese Lücke.
        ##
        ## DAS EPILOGJAHR IST KURZ: eine Ziehung im kurzen Verlauf, zwei im
        ## langen. Zwei Träger je Pfad ziehen die Wahl deshalb stärker an
        ## sich als in einem Jahr mit sieben Ziehungen. Das ist gewollt:
        ## Wer 1919 erreicht, soll den Moment sehen, auf den das Spiel
        ## zuläuft, und nicht eine beliebige der sieben Karten. Ein Zwang
        ## bleibt es nicht - gemessen erscheint ein Träger in gut der
        ## Hälfte der kurzen Durchgänge.
        ##
        ## Gewählt ist je Pfad die Karte, die den Satz unter "kippt"
        ## einlöst, dazu die Gegenkarte dazu:
        ##   front   die Ankunft und die Nachricht vom Vertrag - was du
        ##           gesehen hast gegen das, was erzählt wird
        ##   etappe  der Entlassungsschein und die Ankunft - das Papier
        ##           sagt, wo du warst, und niemand glaubt es
        ##   heimat  der Heimkehrer in der Küche und die Blockade, die
        ##           nach dem Waffenstillstand weitergeht
        1919: {
            "front": {
                "frage": "Wie erzählst du das, was war?",
                "kippt": "Was du gesehen hast, passt nicht zu dem, was erzählt wird.",
                "träger": ["epilog_1919_heimkehr", "epilog_1919_vertrag"],
            },
            "etappe": {
                "frage": "Wie erzählst du das, was war?",
                "kippt": "Du warst dabei und wirst gefragt, ob du wirklich dabei warst.",
                "träger": ["epilog_1919_papiere", "epilog_1919_heimkehr"],
            },
            "heimat": {
                "frage": "Wie erzählst du das, was war?",
                "kippt": "Die Waffen schweigen. Auf dem Tisch ändert das zunächst nichts.",
                "träger": ["epilog_1919_rueckkehrer", "epilog_1919_blockade"],
            },
        },
    }

    def kapitel_bogen(jahr, pfad):
        """Der Bogen eines Kapitels. Liefert immer ein vollständiges Feld."""
        eintrag = KAPITEL_BOGEN.get(jahr, {}).get(pfad)
        if eintrag is None:
            return {"frage": "", "kippt": "", "träger": []}
        return eintrag

    ## Hinweis für die Lehrkraft. Erscheint ausschließlich im Analysemodus
    ## und wird von der Sprachprüfung nicht erfasst, weil hier fachliche
    ## Begriffe stehen dürfen, die im Spieltext nichts zu suchen haben.
    KAPITEL_LEHRPLAN = {
        1914: "Kl. 8, LB 4: Nationalismus, Bündnispolitik, Mobilmachung. Sprachlich: Burgfrieden, nicht Volksgemeinschaft.",
        1915: "Kl. 8, WB 1: neue Dimension der Kriegsführung (Stellungskrieg, Giftgas). WB 2: Beginn der Rationierung.",
        1916: "Kl. 8, WB 1: Materialschlacht, Frage nach dem \"Totalen Krieg\". WB 2: Kriegswirtschaft, Hilfsdienstgesetz.",
        1917: "Kl. 8, WB 2: Alltag und Versorgung. Kl. 9, LB 1: Oktoberrevolution als Voraussetzung der Sowjetherrschaft.",
        1918: "Kl. 9, LB 1: Novemberrevolution. Kl. 8, WB 3: Propaganda gegen die Erfahrung der Betroffenen.",
        1919: "Kl. 9, LB 1: Versailles, Völkerbund, Weimarer Verfassung. LB 2: Mentalitäten, Dolchstoßlegende.",
    }


################################################################################
## 2. Ziehungszahlen
################################################################################
##
## Die Ziehungen sind bewusst ungleich verteilt. 1916 und 1918 sind die
## dichtesten Jahre: 1916 wegen der Materialschlachten und des
## Hilfsdienstgesetzes, 1918 wegen Offensive, Grippe und Umsturz. Der
## Epilog trägt am wenigsten, weil er auswertet statt zu erzählen.
##
## MODUS_ZIELZAHL nennt die Summe der Kriegsjahre 1914 bis 1918. Der
## Epilog kommt hinzu: kurz also 12 + 1, lang 30 + 2.

init -19 python:

    ## DER KURZE VERLAUF HAT NEUN ZIEHUNGEN, DER LANGE ACHTZEHN.
    ## Seit Paket 6, Vorweg B — Entscheidung 12 des Projektleiters.
    ##
    ## Vorher waren es dreizehn und einunddreißig. Zwei Gründe für die
    ## Kürzung, und der zweite wiegt schwerer als der erste.
    ##
    ## ERSTENS DIE STUNDE. Dreizehn Entscheidungen in fünfundvierzig
    ## Minuten sind für Dreizehnjährige knapp gerechnet. Wer eine Karte
    ## liest, nachdenkt, die Kopfleiste ansieht und im Zweifel die
    ## Nachbarin fragt, braucht mehr als eine Minute; dazu kommen
    ## Handgriffe und Post. Neun Entscheidungen füllen die Stunde und
    ## lassen Zeit für den Lebenslauf und den Vergleich am Ende — und
    ## darauf läuft das Spiel zu.
    ##
    ## ZWEITENS DIE RECHNUNG. Paket 5, Schritt 3 hat gemessen, dass eine
    ## gezogene Karte unter kluger Wahl 0,57 bis 0,93 Punkte kostet. Bei
    ## einunddreißig Ziehungen sind das 18 bis 29 Punkte gegen eine Skala,
    ## die 12 hergibt: Der lange Verlauf war arithmetisch nicht zu
    ## überstehen. Nicht die Karten sind zu teuer, der Durchgang war zu
    ## lang.
    ##
    ## WEGGENOMMEN WURDE, WO EIN JAHR MEHR ALS SEINEN ANTEIL HATTE, nicht
    ## gleichmäßig überall. 1916 und 1918 bleiben die dichtesten Jahre —
    ## Materialschlachten und Hilfsdienstgesetz, Offensive und Umsturz.
    ## 1914 bleibt das dünnste: fünf Monate von der Mobilmachung bis
    ## Weihnachten. Der Epilog trägt weiter am wenigsten, weil er
    ## auswertet statt zu erzählen.
    ##
    ## DER LANGE VERLAUF GEHT AUF DREIZEHN, NICHT AUF ACHTZEHN.
    ## Entscheidung 13, 4. September 2026 — von Dominik an mich delegiert.
    ##
    ## Entscheidung 12 nannte achtzehn bis zwanzig Ziehungen, Entscheidung
    ## 11 einen Korridor von 20 bis 35 Prozent bei zufälliger und 60 bei
    ## kluger Wahl. Beide zusammen gehen nicht auf. Gemessen, 800
    ## Durchgänge je Lage, zufällig / klug:
    ##
    ##   Ziehungen lang     18          16          15          14          13
    ##   Front         16,8/47,0   18,2/54,0   23,5/55,5   29,2/59,6   31,1/64,4
    ##   Etappe         5,1/13,6    9,8/26,4   14,0/34,6   17,6/39,2   25,5/48,8
    ##   Heimat        13,6/50,4   15,0/59,0   16,8/60,6   20,5/63,2   23,4/69,8
    ##
    ## Bei dreizehn liegen fünf von sechs Lagen in ihrem Korridor, und sie
    ## liegen mit Abstand darin - nicht auf der Kante. Das ist der Grund
    ## für dreizehn statt vierzehn: Eine Eichung, die nur eben so hält,
    ## reißt beim nächsten Paket wieder, und die Pakete 6 bis 10 fassen
    ## keine Zahl mehr an. Übrig bleibt der lange Etappenverlauf mit 48,8
    ## bei kluger Wahl; das ist eine Sache des Etappenbestands und nicht
    ## der Ziehungszahl.
    ##
    ## WAS DEN LANGEN VERLAUF WEITER VOM KURZEN UNTERSCHEIDET, ist nicht
    ## nur die Länge, sondern der Bestand: Der kurze zieht ausschließlich
    ## Kernkarten, der lange den ganzen Vorrat. Dreizehn Ziehungen aus 95
    ## Karten sind ein anderes Spiel als neun aus den Kernkarten - auch
    ## dann, wenn der Unterschied in der Zahl kleiner geworden ist.
    ##
    ## DER BESTAND BLEIBT VOLLSTÄNDIG. Es ist nichts gelöscht und nichts
    ## stillgelegt; es wird nur weniger je Durchgang gezogen.
    ##
    ## WEGGENOMMEN WURDE, WO EIN JAHR MEHR ALS SEINEN ANTEIL HATTE. 1916
    ## bleibt das dichteste Jahr - Verdun, die Somme und das
    ## Hilfsdienstgesetz in zwölf Monaten.
    ##
    ## 1914 BEHÄLT IM LANGEN VERLAUF ZWEI ZIEHUNGEN, und das ist keine
    ## Dramaturgie, sondern eine Kopplung. Post kommt nur NACH einem
    ## Ereignis, und zwischen zwei Briefen liegen mindestens POST_ABSTAND
    ## Ziehungen. Mit einer einzigen Ziehung im ersten Kapitel erreicht
    ## kein Brief das Jahr 1914 - Probe 2 meldete daraufhin auf allen drei
    ## Pfaden "kein Kapitel mit Nebenfigur". Die fünf Nebenfiguren werden
    ## aber 1914 eingeführt; ein Jahr ohne sie nimmt dem Merkbuch seinen
    ## Anfang. 1918 gibt die Ziehung dafür ab: Der November trägt sich
    ## auch mit zweien, weil dort die Karten ohnehin die stärksten sind.
    MODUS_ZIELZAHL = {
        "kurz": 8,
        "lang": 11,
    }

    KAPITEL_ZIEHUNGEN = {
        "kurz": {1914: 1, 1915: 1, 1916: 2, 1917: 2, 1918: 2, 1919: 1},
        "lang": {1914: 2, 1915: 2, 1916: 3, 1917: 2, 1918: 2, 1919: 2},
    }

    ## Anzeigetexte für die Moduswahl. Wer die Tabelle oben ändert, ändert
    ## diese Sätze mit, sonst steht auf der Karte eine falsche Zahl.
    ##
    ## NACHGERECHNET IN PAKET 2, SCHRITT 3
    ## Die Versprechen "etwa zehn" und "etwa fünfundzwanzig Minuten" waren
    ## beide zu niedrig. Gerechnet wird mit 45 Sekunden je Entscheidungs-
    ## karte, 90 Sekunden je Einlage und 30 Sekunden je Brief. Wie viele
    ## Einlagen und Briefe auf eine Ziehung kommen, ist nicht geschätzt,
    ## sondern in 8000 Durchgängen gemessen (bericht.txt, Probe 2): 0,27
    ## Einlagen und 0,24 Briefe je Ziehung.
    ##
    ## NACHGERECHNET IN PAKET 6, VORWEG B. Gemessen kommen 0,18 Einlagen
    ## und 0,24 Briefe auf eine Ziehung.
    ##
    ##   kurz   9 Ziehungen (1+1+2+2+2+1)
    ##          9 x 45 s               =  405 s
    ##          9 x 0,18 x 90 s        =  146 s
    ##          9 x 0,24 x 30 s        =   65 s
    ##                                 =  616 s, also gut 10 Minuten
    ##
    ##   lang  13 Ziehungen (1+2+3+2+3+2)
    ##         13 x 45 s               =  585 s
    ##         13 x 0,18 x 90 s        =  211 s
    ##         13 x 0,24 x 30 s        =   96 s
    ##                                 =  892 s, also knapp 15 Minuten
    ##
    ## DIESE RECHNUNG IST DIE UNTERGRENZE, NICHT DIE UNTERRICHTSZEIT. Sie
    ## unterstellt fünfundvierzig Sekunden je Karte, und das ist die Zeit
    ## eines geübten Lesers, der sich schon entschieden hat. Entscheidung
    ## 12 rechnet für die Klasse anders: Neun Entscheidungen füllen eine
    ## Einzelstunde, wenn Lesen, Nachdenken und Zwischenfragen dazukommen.
    ## Die Angaben in MODUS_DAUER folgen deshalb der Klasse und nicht der
    ## Stoppuhr — wer sie ändert, ändert beides zusammen.
    ##
    ## Die Zahlen gelten für einen VOLLSTÄNDIGEN Durchgang, also für einen,
    ## der 1919 erreicht. Seit Paket 5 haben alle sechs Jahre Bestand; ein
    ## Durchgang endet nicht mehr vorzeitig, weil das Kapitel leer ist,
    ## sondern nur noch an den vier Werten.
    ##
    ## Die Spielzeit selbst bleibt unangetastet: Der kurze Verlauf passt
    ## damit in eine Einzelstunde, der lange in eine Doppelstunde. Genau
    ## dafür sind die beiden gedacht.
    MODUS_UMFANG = {
        "kurz": "Acht Entscheidungen entlang der wichtigsten Stationen, dazu der Epilog. Dazwischen einzelne Handgriffe und Post.",
        "lang": "Elf Entscheidungen aus dem gesamten Vorrat, dazu zwei im Epilog. Hier kommen auch die Karten vor, die der kurze Weg auslässt.",
    }

    MODUS_DAUER = {
        "kurz": "Etwa fünfundzwanzig Minuten. Passt in eine Einzelstunde, mit Zeit für den Lebenslauf.",
        "lang": "Etwa fünfunddreißig Minuten. Dafür braucht es eine Doppelstunde.",
    }


################################################################################
## 3. Kapitelwirkung
################################################################################
##
## Beim Jahreswechsel verschieben sich die vier Werte, unabhängig davon,
## was gespielt wurde. Das bildet ab, dass die Lage sich verschlechterte,
## ohne dass jemand etwas falsch gemacht hätte.
##
## Vorzeichen: versorgung und rueckhalt sind hohe Werte, wenn es gut
## steht. Ein Minus bedeutet dort mehr Hunger beziehungsweise mehr
## Einsamkeit. belastung und aufmerksamkeit laufen umgekehrt.
##
## WERTEBUDGET (wichtig für Paket 7 und 8)
## Über alle Jahreswechsel zusammen verliert die Versorgung je nach Pfad
## fünf bis sechs Punkte. Wer in der Heimat mit 6 beginnt, steht ohne
## jedes Ereignis am Ende bei etwa 1 und damit an der Grenze zum
## Verhungern. Die Ereignisse der Jahre 1917 und 1918 müssen deshalb
## Wege enthalten, Versorgung zurückzugewinnen, sonst wird der Durchgang
## unabhängig von jeder Entscheidung tödlich.

init -19 python:

    ## GEEICHT AM 4. SEPTEMBER 2026, Paket 5, Schritt 3.
    ##
    ## Gemessen wurde gegen den VOLLSTÄNDIGEN Bestand: sechs Jahre, drei
    ## Pfade, 97 Ereignisse, 5 Einlagen, 26 Briefe, mit 2000 Durchgängen je
    ## Lage und Wahlstrategie, also 24000 Durchgängen. Die Grenzen davor
    ## waren an einem Bestand geeicht, in dem 1917 bis 1919 leer waren und
    ## vier von sechs Kapiteln ohne eine einzige Ziehung endeten.
    ##
    ## GEÄNDERT IST AN DIESER TABELLE GENAU EINES: 1917 trägt keine
    ## aufmerksamkeit mehr. Der Grund steht in der Sache. 1916 hebt den
    ## Verdacht bereits um eins, und KAPITEL_WIRKUNG_PFAD legte 1917 auf
    ## der Etappe noch einmal eins darauf; damit stiegen drei Jahreswechsel
    ## hintereinander denselben Wert, den nur 17 bis 27 Prozent der
    ## Optionen überhaupt senken können. Der Steckrübenwinter ist Hunger
    ## und Erschöpfung, nicht Überwachung - die Überwachung von 1917
    ## erzählen die Karten (Metallsammlung, Ablieferung, Zensur), und sie
    ## tun es seit Paket 4 reichlich.
    ##
    ## WAS DIESE EICHUNG NICHT ERREICHT HAT, steht in der Meldung zu
    ## Schritt 3 und in AUFGEFALLEN: Die Grenzen aus Entscheidung 1 - bei
    ## zufälliger Wahl 40 bis 60 Prozent, bei kluger über 80 - werden im
    ## LANGEN Verlauf auf keinem Pfad erreicht. Gemessen wurde die
    ## Obergrenze dessen, was diese Tabellen überhaupt hergeben: mit
    ## leerem Kalender, ohne Einlagen, ohne Post und mit den bestmöglichen
    ## Startwerten erreicht die lange Etappe 2,0 Prozent bei zufälliger und
    ## 8,7 bei kluger Wahl. Der Hebel liegt also nicht mehr hier, sondern
    ## bei den Kosten der einzelnen Karte.
    KAPITEL_WIRKUNG = {
        1915: {"versorgung": -1},
        1916: {"versorgung": -1, "belastung": 1, "aufmerksamkeit": 1},
        1917: {"versorgung": -1, "belastung": 1},
        1918: {"belastung": 1, "rueckhalt": -1},
        ## SEIT PAKET 3, VORWEG: aufmerksamkeit -2 beim Übergang in 1919.
        ## Der einzige Jahreswechsel, an dem die Aufsicht selbst zerfällt.
        ## Im November 1918 verlieren die stellvertretenden Generalkommandos
        ## ihre Befugnisse, der Belagerungszustand endet, und in vielen
        ## Orten übernehmen Arbeiter- und Soldatenräte die Verwaltung. Wer
        ## in einer Akte stand, stand weiter darin - aber niemand las sie
        ## mehr. Das ändert nichts am Überleben, denn im Epilog greift
        ## ende_pruefen() nicht mehr; es ändert die Stufe, mit der der
        ## Lebenslauf am Ende rechnet, und das ist der Punkt.
        1919: {"rueckhalt": -1, "aufmerksamkeit": -2},
    }

    ## Zusatz je nach Pfad. Der Steckrübenwinter traf die Heimat härter,
    ## das Frühjahr 1918 die Front, und im Januar 1918 wurden bestreikte
    ## Betriebe unter militärische Aufsicht gestellt.
    KAPITEL_WIRKUNG_PFAD = {
        ## SEIT PAKET 5, SCHRITT 3 trägt die Etappe 1917 belastung statt
        ## aufmerksamkeit. Gezählt im Bestand: Auf der Etappe können 27
        ## Prozent der Optionen den Verdacht senken - mehr als auf den
        ## anderen beiden Pfaden -, aber nur 13 Prozent die Erschöpfung,
        ## gegen 24 an der Front und 21 in der Heimat. Der Jahreswechsel
        ## legte also ausgerechnet auf den Wert, für den die Etappe Wege
        ## hat, und ließ den unangetastet, für den sie keine hat. 1917
        ## heißt in der Etappe Nachschubstockung: Arbeit, nicht Verdacht.
        1917: {
            "front": {"belastung": 1},
            "etappe": {"belastung": 1},
            "heimat": {"versorgung": -1},
        },
        ## SEIT PAKET 2, SCHRITT 3: Die Heimat trug hier belastung +1 UND
        ## aufmerksamkeit +1, zusätzlich zur allgemeinen Kapitelwirkung, die
        ## 1918 bereits belastung +1 für alle enthält. Damit war die Heimat
        ## der einzige Pfad mit +2 Erschöpfung in einem einzigen
        ## Jahreswechsel - und sie war zugleich der Pfad mit der höchsten
        ## Abbruchquote. Die Erschöpfung von Grippe und Kohlenmangel steckt
        ## schon im allgemeinen Teil; hier bleibt, was nur die Heimat traf:
        ## die militärische Aufsicht über bestreikte Betriebe seit Januar
        ## 1918 und die Kontrollen an jedem Bahnsteig.
        1918: {
            "front": {"versorgung": -1},
            "etappe": {"versorgung": -1},
            "heimat": {"aufmerksamkeit": 1},
        },
        1919: {
            "front": {"belastung": 1},
            "etappe": {"belastung": 1},
            "heimat": {"belastung": 1},
        },
    }

    ## Kontrollrechnung, neu gerechnet in Paket 5, Schritt 3. Ohne ein
    ## einziges Ereignis erreicht der Jahreswechsel allein diese Endwerte
    ## (Rohwerte, Stand 1919):
    ##
    ##   Front    Hunger 4   Erschöpfung 7   Verdacht 0   Einsamkeit 6
    ##   Etappe   Hunger 4   Erschöpfung 6   Verdacht 1   Einsamkeit 6
    ##   Heimat   Hunger 2   Erschöpfung 7   Verdacht 1   Einsamkeit 6
    ##
    ## Die Sterbeschwellen liegen bei Versorgung unter 1, Belastung ab 12
    ## und Aufmerksamkeit ab 12 (ENDE_SCHWELLEN in script.rpy). Niemand
    ## stirbt also am Kalender allein; über Leben und Tod entscheiden die
    ## Ereignisse. Wer die Tabellen oben ändert, rechnet diese sechs Zeilen
    ## neu - Probe 4 druckt sie bei jedem Lauf aus, man muss sie nur
    ## abschreiben.
    ##
    ## Der Verdacht steht am Ende niedriger als in den Jahren davor. Das
    ## ist der Abschlag von 1919 (aufmerksamkeit -2): Im November 1918
    ## verlieren die stellvertretenden Generalkommandos ihre Befugnisse,
    ## und die Akte wird nicht mehr gelesen. Höchststand ist 1916 bis 1918
    ## Verdacht 2 an der Front und 3 in der Etappe.

    ## Ein Satz, der die Veränderung begründet. Er steht auf der
    ## Jahreskarte über der Auflistung.
    KAPITEL_WIRKUNG_TEXT = {
        1915: "Die Rationen werden kleiner, und der Krieg wird länger, als alle gerechnet haben.",
        1916: "Zwei Materialschlachten und ein Rüstungsprogramm, das Menschen, Kohle und Kartoffeln verbraucht.",
        1917: "Der Steckrübenwinter, gekürzte Rationen und ein Belagerungszustand, der genauer hinsieht.",
        1918: "Kohlenmangel, Grippe und ein Frühjahr, das noch einmal alles verlangt.",
        1919: "Der Krieg ist vorbei. Das Jahr danach ist es nicht.",
    }


################################################################################
## 4. Erweiterte Ereignisklasse
################################################################################
##
## init -9 läuft nach der Klassendefinition in script.rpy (init -10) und
## vor dem Aufbau des Bestands (init 0). Dadurch entstehen ALLE Ereignisse
## bereits mit den neuen Feldern, ohne dass script.rpy geändert wird.
##
##   braucht_eines   Liste. Mindestens eines dieser Merkmale muss
##                   vorliegen. Ergänzt braucht (dort müssen alle
##                   Merkmale vorliegen).
##   gewicht_bonus   {"merkmal": Zahl}. Erhöht die Ziehungschance, wenn
##                   das Merkmal vorliegt. Kein Zwang, nur ein Sog.
##   knuepft_an      Liste von Merkmalen, auf die das Ereignis im Text
##                   zurückgreift. Reine Dokumentation für die
##                   Bestandsprobe, ohne Wirkung auf die Ziehung.
##
## ACHTUNG bei Änderungen an diesem Block
## Die Basisklasse muss unter einem eigenen Namen festgehalten werden.
## Ein Aufruf von Ereignis.__init__ im Rumpf der Unterklasse schlägt den
## Namen erst zur Laufzeit im Store nach. Da dort am Ende dieses Blocks
## die Unterklasse steht, riefe sie sich selbst auf, bis Ren'Py mit
## RecursionError abbricht.

init -9 python:

    ## Die Prüfung hält den Block wiederholbar. Ohne sie würde ein
    ## Neuladen des Skripts eine Unterklasse der Unterklasse anlegen.
    if not getattr(Ereignis, "kapitel_erweitert", False):

        EREIGNIS_GRUNDLAGE = Ereignis

        class KapitelEreignis(EREIGNIS_GRUNDLAGE):

            kapitel_erweitert = True

            def __init__(self, *args, **kwargs):
                braucht_eines = kwargs.pop("braucht_eines", None)
                gewicht_bonus = kwargs.pop("gewicht_bonus", None)
                knuepft_an = kwargs.pop("knuepft_an", None)
                EREIGNIS_GRUNDLAGE.__init__(self, *args, **kwargs)
                self.braucht_eines = braucht_eines if braucht_eines else []
                self.gewicht_bonus = gewicht_bonus if gewicht_bonus else {}
                self.knuepft_an = knuepft_an if knuepft_an else []

        Ereignis = KapitelEreignis


################################################################################
## 5. Merkmalsregister und Rückbezüge
################################################################################
##
## Das Register ist das Verzeichnis aller Merkmale, die im Spiel vergeben
## werden. Es hat drei Aufgaben:
##
##   1. Es legt den Wortschatz fest. Paket 6 bis 8 vergeben ausschließlich
##      Merkmale, die hier eingetragen sind. Was nicht im Register steht,
##      taucht später nirgends wieder auf.
##   2. Es liefert den Nachklang: den Satz, mit dem ein Merkmal im
##      Lebenslauf von 1919 bis 1924 wieder auftaucht.
##   3. Es trägt den Rang. Bei mehreren Merkmalen entscheidet er, welche
##      zwei im Lebenslauf erscheinen. Selbst getroffene Entscheidungen
##      stehen über Herkunft und Zuweisung, damit der Schluss von dem
##      erzählt, was die Spielerin oder der Spieler getan hat.
##
## gruppe:  herkunft  aus der Milieuwahl
##          erwerb    aus der Erwerbslage (Paket 2)
##          stellung  aus Musterung und Dienststellung
##          lage      aus den Umständen, nicht gewählt
##          haltung   eine Grundentscheidung des Einstiegs
##          tat       eine Entscheidung im Spielverlauf

init 1 python:

    MERKMAL_REGISTER = {

        ## Der Wirtshaustisch, Frühjahr 1919 ##################################
        ##
        ## SEIT PAKET 5, SCHRITT 2. Die drei stehen bewusst ganz oben und
        ## tragen den höchsten Rang im Register: Sie kommen aus der
        ## letzten Entscheidung des Spiels, und im Lebenslauf soll sie
        ## niemand verdrängen.
        ##
        ## KEIN NACHKLANG BEWERTET DIE WAHL. Der eine hört den Satz
        ## später überall, der andere liest ihn in der Zeitung, dem
        ## dritten sagt man nach, er habe widersprochen - und keiner der
        ## drei Sätze sagt, was davon richtig war.

        "wirtshaus_widersprochen": {
            "gruppe": "tat",
            "name": "Am Wirtshaustisch widersprochen",
            "rang": 86,
            "nachklang": (1922, "1922", (
                "Im Betrieb wird gestritten, wer schuld war. Zwei sagen, du seist "
                "der Einzige gewesen, der damals widersprochen hat. Sie sagen es "
                "nicht als Lob."
            )),
        },

        "wirtshaus_geschwiegen": {
            "gruppe": "tat",
            "name": "Am Wirtshaustisch geschwiegen",
            "rang": 84,
            "nachklang": (1924, "1924", (
                "Zum zehnten Jahrestag steht in der Zeitung derselbe Satz wie "
                "damals im Wirtshaus. Du liest ihn zu Ende und legst das Blatt "
                "weg. Es ist nicht das erste Mal, dass du nichts sagst."
            )),
        },

        "wirtshaus_zugestimmt": {
            "gruppe": "tat",
            "name": "Am Wirtshaustisch zugestimmt",
            "rang": 86,
            "nachklang": (1923, "1923", (
                "Der Satz von damals ist inzwischen überall. Du hörst ihn von "
                "deinem Nachbarn, von deinem Meister und einmal von einem Kind. "
                "Woher du ihn selbst hast, weißt du nicht mehr."
            )),
        },

        ## Taten ##############################################################

        "verbruederung": {
            "gruppe": "tat",
            "name": "An Weihnachten 1914 hinübergegangen",
            "rang": 80,
            "nachklang": (1919, "1919", (
                "Wenn jemand behauptet, drüben hätten keine Menschen gelegen, sagst "
                "du nichts. Du hast einem von ihnen die Hand gegeben. Du weißt, dass "
                "dir das kaum jemand glauben würde."
            )),
        },

        "kamerad_gedeckt": {
            "gruppe": "tat",
            "name": "Einen Kameraden gedeckt",
            "rang": 78,
            "nachklang": (1919, "Frühjahr 1919", (
                "Ein Brief aus Rotterdam. Er hat es hinübergeschafft und fragt, ob er "
                "zurückkommen kann, jetzt, wo niemand mehr sucht. Unterschrieben hat "
                "er mit dem Namen, den er damals im Zivilanzug getragen hat."
            )),
        },

        "kamerad_gemeldet": {
            "gruppe": "tat",
            "name": "Einen Kameraden gemeldet",
            "rang": 78,
            "nachklang": (1921, "1921", (
                "Auf der Straße erkennst du jemanden aus der Kompanie. Er sieht dich, "
                "geht weiter und grüßt nicht. Du drehst dich nicht um."
            )),
        },

        "vorangegangen": {
            "gruppe": "tat",
            "name": "Bei einer Arbeitsniederlegung vorangegangen",
            "rang": 76,
            "nachklang": (1919, "November 1918", (
                "Im Betrieb wird ein Arbeiterrat gewählt. Man kennt deinen Namen von "
                "damals, und man setzt ihn auf die Liste. Der Beamte, der dich 1916 "
                "aufgeschrieben hat, sitzt inzwischen woanders."
            )),
        },

        "zaehlung_ausgefuellt": {
            "gruppe": "tat",
            "name": "Die Zählung von 1916 ausgefüllt",
            "rang": 74,
            "nachklang": (1920, "1920", (
                "Das Ergebnis der Zählung ist nie veröffentlicht worden. Trotzdem "
                "behaupten Verbände und Zeitungen, sie habe bewiesen, was sie ohnehin "
                "sagen wollten. Du weißt, wer die Liste geschrieben hat."
            )),
        },

        ## Haltung des Einstiegs ##############################################

        "kriegsfreiwillig": {
            "gruppe": "haltung",
            "name": "Kriegsfreiwillig gemeldet",
            "rang": 60,
            "nachklang": (1924, "1924", (
                "Zum zehnten Jahrestag laden die Verbände die Freiwilligen von 1914 "
                "ein. Es wird von Begeisterung gesprochen und von Opferbereitschaft. "
                "Du erkennst im Saal drei Gesichter."
            )),
        },

        "einberufen": {
            "gruppe": "haltung",
            "name": "Auf den Einberufungsbefehl gewartet",
            "rang": 30,
            "nachklang": None,
        },

        ## Stellung ###########################################################

        "offizier": {
            "gruppe": "stellung",
            "name": "Offiziersaspirant",
            "rang": 58,
            "nachklang": (1920, "1920", (
                "Das Heer wird auf hunderttausend Mann verkleinert, so steht es im "
                "Vertrag. Für dich ist darin kein Platz. Dein Rang steht noch auf "
                "einem Papier, das niemand mehr sehen will."
            )),
        },

        "uk": {
            "gruppe": "stellung",
            "name": "Unabkömmlich gestellt",
            "rang": 52,
            "nachklang": (1919, "1919", (
                "Zurückgekommene fragen, wo du gewesen bist. Du sagst: im Werk. Sie "
                "sagen nichts darauf und meinen trotzdem etwas."
            )),
        },

        "zurueckgestellt": {
            "gruppe": "stellung",
            "name": "Jahrgang nicht aufgerufen",
            "rang": 28,
            "nachklang": None,
        },

        "gemustert": {
            "gruppe": "stellung",
            "name": "Gemustert",
            "rang": 10,
            "nachklang": None,
        },

        ## Erwerbslagen #######################################################

        "ruestung": {
            "gruppe": "erwerb",
            "name": "Im Rüstungsbetrieb",
            "rang": 50,
            "nachklang": (1919, "Frühjahr 1919", (
                "Das Werk stellt auf Friedensware um. Entlassen wird zuerst, wer "
                "zuletzt gekommen ist. Die Haut an deinen Händen ist immer noch "
                "gelb, und der Arzt sagt, das gehe wieder weg."
            )),
        },

        "lazarett": {
            "gruppe": "erwerb",
            "name": "Im Lazarettdienst",
            "rang": 50,
            "nachklang": (1920, "1920", (
                "Du kennst inzwischen jeden Verband und jede Prothese. In der Stadt "
                "gibt es mehr Männer ohne Bein als Ärzte, die damit umgehen können."
            )),
        },

        "landwirtschaft": {
            "gruppe": "erwerb",
            "name": "Auf Hof und Feld",
            "rang": 48,
            "nachklang": (1919, "Sommer 1919", (
                "Im Sommer stehen wieder Städter mit Rucksäcken auf dem Hof. Ihr habt "
                "zu essen. In der Stadt habt ihr niemanden mehr, der euch grüßt."
            )),
        },

        "verwaltung": {
            "gruppe": "erwerb",
            "name": "In Kontor und Amtsstube",
            "rang": 46,
            "nachklang": (1920, "1920", (
                "Aus der Kriegsgesellschaft wird eine Behörde. Die Listen bleiben, "
                "die Namen darauf ändern sich, und deiner steht weiter unten am Rand."
            )),
        },

        "haushalt": {
            "gruppe": "erwerb",
            "name": "Haushalt und Heimarbeit",
            "rang": 54,
            "nachklang": (1919, "19. Januar 1919", (
                "Du gehst zum ersten Mal wählen. Die Schlange vor dem Wahllokal ist "
                "kürzer als die vor der Ausgabestelle, und sie bewegt sich schneller."
            )),
        },

        "wohlfahrt": {
            "gruppe": "erwerb",
            "name": "In der Kriegsfürsorge",
            "rang": 46,
            "nachklang": (1920, "1920", (
                "Die Sammlungen gehen weiter, jetzt für Kriegswaisen. Es sind mehr, "
                "als eine Stadt zählen möchte."
            )),
        },

        ## Herkunft ###########################################################

        "arbeiterschaft": {
            "gruppe": "herkunft",
            "name": "Arbeiterschaft",
            "rang": 34,
            "nachklang": (1919, "1919", (
                "Der Achtstundentag steht seit November auf dem Papier. Im Betrieb "
                "wird darüber gestritten, ob er auch für deine Abteilung gilt."
            )),
        },

        "buergertum": {
            "gruppe": "herkunft",
            "name": "Bürgertum",
            "rang": 34,
            "nachklang": (1923, "Herbst 1923", (
                "Was die Familie gespart hatte, lag in Kriegsanleihen. Im Herbst 1923 "
                "reicht die Summe für ein Brot, wenn du dich beeilst."
            )),
        },

        "landbevoelkerung": {
            "gruppe": "herkunft",
            "name": "Landbevölkerung",
            "rang": 32,
            "nachklang": (1920, "1920", (
                "Die Zwangsbewirtschaftung läuft weiter. Wer abliefert, verliert; wer "
                "nicht abliefert, bekommt Besuch von einer Kommission."
            )),
        },

        "adel": {
            "gruppe": "herkunft",
            "name": "Adel",
            "rang": 34,
            "nachklang": (1919, "August 1919", (
                "Die Fürstenhöfe sind fort. Die neue Verfassung erklärt Adels"
                "bezeichnungen zum Bestandteil des Namens, mehr nicht. Das Gut bleibt, "
                "der Vorrang nicht."
            )),
        },

        ## Lage ###############################################################

        "kinder": {
            "gruppe": "lage",
            "name": "Kinder im Haushalt",
            "rang": 40,
            "nachklang": (1920, "1920", (
                "Der Schularzt schreibt bei deinem Kind Unterernährung in den Bogen. "
                "Es ist ein Wort, das er an diesem Vormittag oft schreibt."
            )),
        },

        "aeltere_kinder": {
            "gruppe": "lage",
            "name": "Schulpflichtige Kinder",
            "rang": 38,
            "nachklang": None,
        },

        ## SEIT PAKET 2, SCHRITT 2: drei Merkmale statt einer Pauschale ######
        ##
        ## Vorher stand hier ein einziger Eintrag mit dem Namen "Ernährer
        ## im Feld". Er wurde jeder Frau und jedem zurückgestellten Mann
        ## gegeben und sagte über die Lage im Haus nichts: Ob der Mann, der
        ## Vater oder der Bruder fort ist, macht für eine Achtklässlerin
        ## den ganzen Unterschied. Wer mit achtzehn zu Hause bleibt, wartet
        ## auf den Vater; wer mit fünfunddreißig zu Hause bleibt, hält
        ## einen Haushalt ohne den Mann zusammen.
        ##
        ## Die Ränge liegen zwischen 40 und 44, also über "kinder" (40) und
        ## unter "haushalt" (54): Die Lage im Haus wiegt im Lebenslauf
        ## schwerer als die Zahl der Kinder und leichter als die Arbeit,
        ## die man selbst getan hat.

        "ehemann_im_feld": {
            "gruppe": "lage",
            "name": "Der Mann im Feld",
            "rang": 44,
            "nachklang": (1920, "1920", (
                "Die Familienunterstützung läuft aus. An ihre Stelle tritt eine "
                "Versorgung nach Gesetz, berechnet nach Sätzen und Punkten. Vier "
                "Jahre lang hast du entschieden, was gekauft und was geflickt "
                "wird. Jetzt sitzt wieder jemand am Tisch, der gefragt werden "
                "will."
            )),
        },

        "vater_im_feld": {
            "gruppe": "lage",
            "name": "Der Vater im Feld",
            "rang": 42,
            "nachklang": (1919, "1919", (
                "Er kommt im Februar zurück, magerer und langsamer. Er fragt "
                "nach der Schule und nach dem Hof, und du merkst, dass er die "
                "Antworten nicht mehr einordnen kann. Vier Jahre lang hast du "
                "seine Arbeit getan. Er bedankt sich nicht dafür, und du "
                "verlangst es auch nicht."
            )),
        },

        "bruder_im_feld": {
            "gruppe": "lage",
            "name": "Der Bruder im Feld",
            "rang": 40,
            "nachklang": (1920, "1920", (
                "Er ist zurück und redet nicht darüber. Beim Essen sitzt ihr "
                "nebeneinander wie früher. Einmal fragt er, warum du nicht "
                "gezogen bist, und du erklärst ihm den Bescheid, den du damals "
                "bekommen hast. Er nickt und wechselt das Thema."
            )),
        },

        ## Was im Straßengraben blieb #########################################
        ##
        ## SEIT PAKET 7, SCHRITT 3. Die sieben Stücke aus dem Tornister.
        ##
        ## GRUPPE "tat" UND NICHT "lage", ANDERS ALS IM AUFTRAG. Zwei
        ## Gründe, und der zweite wiegt schwerer als der erste.
        ##
        ## Erstens sagt das Register selbst, was die Gruppen bedeuten:
        ## "lage" heißt "aus den Umständen, nicht gewählt", "tat" heißt
        ## "eine Entscheidung im Spielverlauf". Den Mantel wegzuwerfen ist
        ## eine Entscheidung unter Zwang, aber eine Entscheidung.
        ##
        ## Zweitens, und das ist der eigentliche Grund: Fach 0 des
        ## Lebenslaufs heißt "Woher du kamst" und zieht aus "herkunft" UND
        ## "lage". Die vier Herkunftsmerkmale tragen Rang 32 bis 34, die
        ## Lagemerkmale 38 bis 44 - die Herkunft verliert dort schon heute
        ## jedes Mal. Sieben weitere Lagemerkmale mit einem Rang, der hoch
        ## genug wäre, um im Lebenslauf zu erscheinen, würden sie noch
        ## weiter verdrängen. Genau davor steht Entscheidung 10: "Fällt die
        ## Herkunft heraus, dann vergleichen zwei Schülerinnen nur noch,
        ## was ihnen zugestoßen ist - nicht, woher sie gestartet sind."
        ##
        ## In "tat" liegen sie unter allen Kriegsentscheidungen (74 bis 86)
        ## und erscheinen deshalb genau dann, wenn nichts Größeres passiert
        ## ist. Das ist die richtige Reihenfolge: Wer einen Kameraden
        ## gedeckt hat, erinnert sich nicht an den Mantel.
        ##
        ## KEIN NACHKLANG WIRFT ETWAS VOR. Sie erzählen, was danach anders
        ## war, und nicht, dass es falsch war, das Stück wegzuwerfen. Sieben
        ## Riemen sind bis zum Abend tragbar, zehn nicht - irgendetwas muss
        ## in den Graben.

        "ohne_briefe": {
            "gruppe": "tat",
            "name": "Die Briefe zurückgelassen",
            "rang": 38,
            "nachklang": (1921, "1921", (
                "Zu Hause fragt jemand nach der Fotografie, die er dir "
                "geschickt hat. Du sagst, sie sei unterwegs geblieben. "
                "Das stimmt."
            )),
        },

        "ohne_portion": {
            "gruppe": "tat",
            "name": "Die eiserne Portion zurückgelassen",
            "rang": 36,
            "nachklang": (1920, "1920", (
                "In deinen Papieren steht ein Vermerk über fehlendes Gerät. "
                "Der Beamte auf dem Amt liest ihn laut vor, bevor er "
                "weiterblättert."
            )),
        },

        "ohne_mantel": {
            "gruppe": "tat",
            "name": "Den Mantel zurückgelassen",
            "rang": 34,
            "nachklang": (1919, "1919", (
                "Der Husten aus dem zweiten Kriegswinter ist geblieben. "
                "Im Oktober fängt er wieder an, und im März hört er auf."
            )),
        },

        "ohne_stiefel": {
            "gruppe": "tat",
            "name": "Die Ersatzstiefel zurückgelassen",
            "rang": 32,
            "nachklang": (1920, "1920", (
                "Die Ferse ist verheilt und drückt trotzdem. Bei nassem "
                "Wetter merkst du, welcher Fuß es war."
            )),
        },

        "ohne_zeltbahn": {
            "gruppe": "tat",
            "name": "Die Zeltbahn zurückgelassen",
            "rang": 30,
            "nachklang": (1921, "1921", (
                "Du schläfst schlecht, wenn es regnet. Zu Hause sagt man, "
                "das sei früher nicht so gewesen."
            )),
        },

        "ohne_kochgeschirr": {
            "gruppe": "tat",
            "name": "Das Kochgeschirr zurückgelassen",
            "rang": 28,
            "nachklang": (1922, "1922", (
                "Beim Essen bist du der Erste, der fertig ist. Es ist "
                "niemandem aufgefallen außer dir."
            )),
        },

        "ohne_putzzeug": {
            "gruppe": "tat",
            "name": "Das Putzzeug zurückgelassen",
            "rang": 26,
            "nachklang": (1919, "1919", (
                "Auf deinen Entlassungspapieren steht eine Zeile über "
                "Nachlässigkeit im Dienst. Sie kostet dich nichts und steht "
                "trotzdem da."
            )),
        },

        ## Die fremde Last ####################################################
        ##
        ## Sie steht nicht bei den sieben, sondern bei den Entscheidungen:
        ## Das Kochgeschirr des Jüngsten zu tragen ist kein Verzicht,
        ## sondern eine Zuwendung, und der Rang 72 stellt sie unmittelbar
        ## unter die Kriegsentscheidungen statt unter das Weggeworfene.

        "last_getragen": {
            "gruppe": "tat",
            "name": "Fremde Last getragen",
            "rang": 72,
            "nachklang": (1923, "1923", (
                "Der Jüngste von damals schreibt dir zum dritten Mal. Er ist "
                "jetzt Schlosser und fragt jedes Mal, ob du etwas brauchst."
            )),
        },

        ## Marken, keine Erinnerungen #########################################
        ##
        ## SEIT PAKET 7, SCHRITT 3, ALS NACHTRAG. Diese fünf setzen die
        ## Einlagen, seit es sie gibt - und keine stand im Register. Sie
        ## waren damit im ganzen Spiel unsichtbar: Der Lebenslauf
        ## überspringt jedes Merkmal, das er nicht kennt, und das Merkbuch
        ## hätte den Bezeichner selbst angezeigt.
        ##
        ## Sie bekommen einen Namen und einen niedrigen Rang, aber KEINEN
        ## Nachklang. Der Grund: Sie sagen nur, DASS ein Handgriff
        ## stattgefunden hat, nicht wie er ausgegangen ist - "geteilt" trägt
        ## jeder, der acht Striche gezogen hat, gleich wie. Ein Nachklang
        ## müsste also etwas erzählen, das für alle gleich wäre, und das ist
        ## kein Lebenslauf. Was daraus wirklich folgt, steht in den
        ## Merkmalen, die die Auswertung setzt.

        "rotstift_gefuehrt": {
            "gruppe": "tat",
            "name": "Einen Bogen durchgesehen",
            "rang": 22,
            "nachklang": None,
        },

        "geteilt": {
            "gruppe": "tat",
            "name": "Brot aufgeteilt",
            "rang": 22,
            "nachklang": None,
        },

        "gehamstert": {
            "gruppe": "tat",
            "name": "Aufs Land gefahren",
            "rang": 22,
            "nachklang": None,
        },

        "tornister_erleichtert": {
            "gruppe": "tat",
            "name": "Den Tornister erleichtert",
            "rang": 22,
            "nachklang": None,
        },

        "antrag_gestellt": {
            "gruppe": "tat",
            "name": "Einen Antrag gestellt",
            "rang": 22,
            "nachklang": None,
        },

        "vorrat_angelegt": {
            "gruppe": "tat",
            "name": "Vorrat angelegt",
            "rang": 24,
            "nachklang": None,
        },
    }

    ## Reihenfolge bei Ranggleichheit. Sorgt dafür, dass der Lebenslauf
    ## bei identischer Lage immer dieselbe Auswahl trifft und sich damit
    ## im Unterricht wiederholen lässt.
    ## Seit Paket 2, Schritt 2 stehen die drei Familienmerkmale an der
    ## Stelle, an der vorher die eine Pauschale stand, in der Reihenfolge
    ## ihrer Ränge.
    MERKMAL_REIHENFOLGE_LEBENSWEG = [
        ## Die letzte Entscheidung des Spiels steht vorn. Seit Paket 5,
        ## Schritt 2.
        "wirtshaus_widersprochen", "wirtshaus_zugestimmt",
        "wirtshaus_geschwiegen",
        "verbruederung", "kamerad_gedeckt", "kamerad_gemeldet", "vorangegangen",
        "zaehlung_ausgefuellt",
        ## Paket 7, Schritt 3: die fremde Last steht unmittelbar unter den
        ## Kriegsentscheidungen, das Weggeworfene weit darunter.
        "last_getragen",
        "kriegsfreiwillig", "offizier", "haushalt",
        "uk", "ruestung", "lazarett", "landwirtschaft", "verwaltung", "wohlfahrt",
        "ehemann_im_feld", "vater_im_feld", "bruder_im_feld",
        "kinder", "adel", "buergertum", "arbeiterschaft",
        "landbevoelkerung", "aeltere_kinder", "einberufen", "zurueckgestellt",
        ## Die sieben Stücke aus dem Tornister, in der Reihenfolge ihrer
        ## Ränge. Bei Ranggleichheit entscheidet diese Liste - so wählt der
        ## Lebenslauf bei gleicher Lage immer dasselbe, und der Vergleich
        ## zweier Durchgänge im Unterricht trägt.
        "ohne_briefe", "ohne_portion", "ohne_mantel", "ohne_stiefel",
        "ohne_zeltbahn", "ohne_kochgeschirr", "ohne_putzzeug",
        "vorrat_angelegt", "rotstift_gefuehrt", "geteilt", "gehamstert",
        "tornister_erleichtert", "antrag_gestellt",
        "gemustert",
    ]

    ## Nachhallplan: Welches frühe Merkmal muss in welchem späten Jahr
    ## wieder auftauchen? Das ist der Auftrag an Paket 7 und 8. Die
    ## Bestandsprobe prüft, ob die genannten Ereignisse schon bestehen.
    ##
    ## Eintrag: (Merkmal, Jahr, Pfad, geplante Kennung, Arbeitstitel)
    NACHHALL_PLAN = [
        ("verbruederung", 1917, "front", "front_1917_verbruederung_nachhall",
         "Ein neuer Leutnant liest den alten Divisionsbefehl noch einmal vor."),
        ("kamerad_gedeckt", 1917, "front", "front_1917_gerichtsherr",
         "Das Verfahren wird wieder aufgenommen, weil ein Name aufgetaucht ist."),
        ("kamerad_gemeldet", 1918, "front", "front_1918_abrechnung",
         "Im November fragt jemand aus der alten Gruppe nach der Nacht von damals."),
        ("vorangegangen", 1917, "heimat", "heimat_1917_aprilstreik",
         "Die Brotration wird gekürzt. Man erwartet, dass du wieder vorne stehst."),
        ("vorangegangen", 1918, "heimat", "heimat_1918_rat",
         "Im November wird ein Arbeiter- und Soldatenrat gebildet."),
        ## Pfadangabe seit Paket 5, Schritt 1, Teil C: Das Ereignis trägt
        ## front und etappe, weil das erste Glied der Kette es auch tut.
        ## Die Angabe hier ist reine Anzeige im zusammengeführten Plan;
        ## sie wird trotzdem mitgeführt, damit der Plan nicht etwas
        ## anderes behauptet als der Bestand.
        ("zaehlung_ausgefuellt", 1918, "front/etappe", "front_1918_liste",
         "Wieder eine Liste, wieder eine Unterschrift, diesmal über Heimkehrer."),
        ("kriegsfreiwillig", 1918, "front", "front_1918_freiwillig_von_1914",
         "Von den Freiwilligen des ersten Sommers ist die Kompanie fast leer."),
        ("offizier", 1918, "front", "front_1918_befehl",
         "Der Befehl zum Rückmarsch trifft ein, und du sollst ihn durchgeben."),
        ("uk", 1917, "heimat", "heimat_1917_hilfsdienst",
         "Das Hilfsdienstgesetz stellt die Zurückstellung auf eine neue Grundlage."),
        ("haushalt", 1918, "heimat", "heimat_1918_grippe",
         "Die Grippe kommt ins Haus, und die Ausgabestelle öffnet trotzdem."),
        ("landwirtschaft", 1917, "heimat", "heimat_1917_ablieferung",
         "Die Ablieferungspflicht wird verschärft, die Kommission kommt auf den Hof."),
        ("ruestung", 1917, "heimat", "heimat_1917_akkord",
         "Der Akkord wird erhöht, der Lohn nicht."),
        ("kinder", 1917, "heimat", "heimat_1917_schulspeisung",
         "Die Schulspeisung wird eingeführt, und sie reicht nicht für alle."),
        ("lazarett", 1918, "beide", "lazarett_1918_grippestation",
         "Die Grippestation füllt sich schneller als die Verwundetenstation."),
    ]

    ############################################################################
    ## DER KETTENPLAN
    ############################################################################
    ##
    ## SEIT PAKET 3, SCHRITT 2. Option.kette und Option.kette_ab gibt es
    ## seit Paket 1, benutzt werden sie an genau zwei Stellen. Damit ist
    ## fast jede Entscheidung eine Einzelkarte: Sie kostet etwas und ist
    ## danach vorbei. Erinnern kann man sich an so etwas nicht.
    ##
    ## Eine Kette beantwortet eine Entscheidung ein bis zwei Ereignisse
    ## später. Das ist der Unterschied zwischen einer Folge von Episoden
    ## und einer Handlung, die sich nacherzählen lässt.
    ##
    ## DIESES PAKET SCHREIBT NUR DEN PLAN. Die Texte entstehen in den
    ## Inhaltspaketen. Jeder Eintrag nennt:
    ##
    ##   ("kennung_glied_eins", "kennung_glied_zwei", pfad, abstand,
    ##    "was das erste Glied fragt", "was das zweite Glied beantwortet")
    ##
    ## abstand ist der Wert für kette_ab: 0 heißt noch im selben Jahr,
    ## 1 heißt im nächsten. Seit Paket 3 wird beim Ziehen zusätzlich das
    ## jahre-Feld des zweiten Glieds geprüft; wer eine Kette plant, gibt
    ## dem zweiten Glied deshalb ALLE Jahre, in denen es fallen darf.
    ##
    ## Die beiden bestehenden Ketten stehen mit in der Liste, damit sie
    ## nicht getrennt gepflegt werden müssen.
    ##
    ## SEIT PAKET 4, VORWEG: Drei Kennungen stehen auch im NACHHALL_PLAN.
    ## Sie sind unten mit "auch im Nachhallplan" gekennzeichnet. Geführt
    ## wird dort, nicht hier: Der Nachhallplan nennt die Bedingung, die
    ## im Ereignis stehen muss, dieser Plan nur die Vorgeschichte. Wer
    ## eine der drei baut, baut sie EINMAL. Die zusammengeführte Liste
    ## liefert inhaltsplan() in Abschnitt 10b, und probe_alles.py druckt
    ## sie aus.
    ##
    ## REGEL FÜR JEDE NEUE KETTE (Paket 4, Vorweg, D): Das zweite Glied
    ## muss mindestens ein Jahr abdecken, das nach dem spätesten Jahr des
    ## ersten Glieds liegt. Sonst bleibt die Frage in einem Teil der
    ## Durchgänge ohne Antwort. ketten_ohne_spaeteres_jahr() prüft das.

    KETTEN_PLAN = [

        ## Bestehend seit Paket 1 ############################################
        ("front_kamerad", "front_nachfrage", "front", 1,
         "Du deckst einen Kameraden, der sich absetzen will.",
         "Ein Offizier des Gerichtsherrn kommt mit einer Liste zurück."),

        ("heimat_hamsterfahrt", "heimat_verfahren", "heimat", 1,
         "Du fährst aufs Land und wirst an der Sperre aufgeschrieben.",
         "Eine Vorladung wegen Verstoßes gegen die Höchstpreise."),

        ## Geplant, Texte in den Inhaltspaketen ##############################
        ## auch im Nachhallplan (Merkmal zaehlung_ausgefuellt) - dort geführt
        ("front_1916_zaehlung", "front_1918_liste", "front/etappe", 2,
         "Du füllst die Zählung von 1916 aus oder verschleppst sie.",
         "1918 liegt wieder eine Liste da, diesmal über Heimkehrer."),

        ## auch im Nachhallplan (Merkmal vorangegangen) - dort geführt
        ("heimat_1916_arbeitsniederlegung", "heimat_1917_aprilstreik", "heimat", 1,
         "Du gehst bei einer Arbeitsniederlegung voran oder bleibst an der Maschine.",
         "Im April wird die Brotration gekürzt, und man sieht dich an."),

        ## auch im Nachhallplan (Merkmal verbruederung) - dort geführt
        ("front_1914_weihnachten", "front_1917_verbruederung_nachhall", "front", 3,
         "Du gehst an Weihnachten 1914 hinüber oder bleibst im Graben.",
         "Ein neuer Leutnant liest den alten Divisionsbefehl noch einmal vor."),
    ]

    ## DREI EINTRÄGE SIND GESTRICHEN, Paket 5, Schritt 3, Punkt 14.
    ##
    ## Sie standen hier als geplante Ketten, aber KEINE von ihnen war je
    ## begonnen: Das erste Glied gibt es zwar in jedem der drei Fälle, doch
    ## keine seiner Optionen trägt ein kette=. Damit war das, was hier
    ## stand, kein Plan für ein zweites Glied, sondern eine Absichts-
    ## erklärung ohne erstes. inhaltsplan() wies sie als "fehlt" aus, und
    ## bei jeder Prüfung entstand dieselbe Beanstandung neu.
    ##
    ## Warum gestrichen und nicht gebaut: Ein Kettenglied zu bauen heißt,
    ## ein Ereignis zu schreiben und eine bestehende Option zu ändern.
    ## Dieser Schritt ist ausdrücklich ein Zahlendurchgang; Ereignistexte
    ## und Bedingungen bleiben unangetastet. Ein Plan, in dem Kennungen
    ## stehen, die niemand baut, ist beim nächsten Mal wieder eine
    ## Beanstandung - also steht der Vorrat jetzt hier als Kommentar und
    ## nicht als Zeile, die eine Probe für einen Auftrag hält.
    ##
    ## Die drei Ideen im Wortlaut, damit nichts verlorengeht. Wer eine
    ## davon in einem Inhaltspaket baut, trägt sie oben wieder ein UND
    ## gibt dem ersten Glied die Option, die die Kette setzt:
    ##
    ##   heimat_denunziation -> heimat_1917_hinterhaus, heimat, +1
    ##     "Du bestätigst eine Anzeige gegen das Hinterhaus oder schweigst."
    ##     "Die Familie aus dem Hinterhaus steht ein Jahr später vor
    ##      deiner Tür."
    ##     Erstes Glied trägt 1915 bis 1918; das zweite bräuchte 1916
    ##     bis 1919, damit die Antwort in jedem Fall kommen kann.
    ##
    ##   heimat_1916_kinderarbeit -> heimat_1918_schulbank, heimat, +2
    ##     "Du schickst dein ältestes Kind arbeiten oder lässt es in der
    ##      Schule."
    ##     "1918 entscheidet sich, was aus dem Kind geworden ist."
    ##     Erstes Glied trägt nur 1916; 1918 reicht dem zweiten also.
    ##
    ##   front_1916_gefangener -> front_1918_wiedersehen, front, +2
    ##     "Du bringst einen Gefangenen zurück oder lässt ihn stehen."
    ##     "Beim Rückmarsch begegnet dir jemand, der dabei war."
    ##     Erstes Glied trägt nur 1916; 1918 reicht dem zweiten also.

    def kettenplan_bericht():
        """Zeilen für die Bestandsprobe: welches Glied besteht schon?"""
        zeilen = []
        for eins, zwei, pfad, abstand, frage, antwort in KETTEN_PLAN:
            zeilen.append({
                "eins": eins,
                "zwei": zwei,
                "pfad": pfad,
                "abstand": abstand,
                "frage": frage,
                "antwort": antwort,
                "eins_da": eins in EREIGNIS_INDEX,
                "zwei_da": zwei in EREIGNIS_INDEX,
            })
        return zeilen

    ## Nachträge an bestehenden Ereignissen. Sie verändern keinen Text,
    ## sondern nur die Ziehungschance: Wer eine Sache kennt, dem begegnet
    ## sie eher wieder. Beim Schreiben von Paket 6 wandern diese Angaben
    ## in die Ereignisse selbst; bis dahin stehen sie hier an einer Stelle.
    ##
    ## Eintrag: Kennung -> {"gewicht_bonus": {...}, "braucht_eines": [...]}
    ## Seit Paket 2, Schritt 2 stehen an den drei Stellen, an denen vorher
    ## die eine Pauschale stand, alle drei Familienmerkmale mit demselben
    ## Zuschlag. Nur eines von ihnen kann gleichzeitig vorliegen, die Summe
    ## bleibt also dieselbe wie vorher - der Sog ist derselbe, er hängt nur
    ## nicht mehr an einer Pauschale.
    RUECKBEZUG_NACHTRAG = {
        "front_stosstrupp": {"gewicht_bonus": {"kriegsfreiwillig": 4, "offizier": 3}},
        "front_kamerad": {"gewicht_bonus": {"verbruederung": 4}},
        "front_1916_zaehlung": {"gewicht_bonus": {"verwaltung": 4, "offizier": 3}},
        "front_urlaub": {"gewicht_bonus": {
            "kinder": 3,
            "ehemann_im_feld": 2, "vater_im_feld": 2, "bruder_im_feld": 2}},
        "heimat_kriegsanleihe": {"gewicht_bonus": {"buergertum": 5, "adel": 5}},
        "heimat_hamsterfahrt": {"gewicht_bonus": {"landbevoelkerung": 4}},
        "heimat_lazarettzug": {"gewicht_bonus": {"lazarett": 6, "wohlfahrt": 4}},
        "heimat_1916_arbeitsniederlegung": {"gewicht_bonus": {"arbeiterschaft": 5}},
        "heimat_denunziation": {"gewicht_bonus": {
            "uk": 3,
            "ehemann_im_feld": 2, "vater_im_feld": 2, "bruder_im_feld": 2}},
        "heimat_unterstuetzung": {"gewicht_bonus": {
            "kinder": 3,
            "ehemann_im_feld": 5, "vater_im_feld": 5, "bruder_im_feld": 5}},

        ## PAKET 7, SCHRITT 3, TEIL A.2: Der Mantel im Straßengraben.
        ##
        ## Wer ihn weggeworfen hat, dem begegnet die Kälte häufiger. Das ist
        ## kein Strafmechanismus, sondern dieselbe Regel wie überall hier:
        ## Wer eine Sache kennt, dem begegnet sie eher wieder. Nur zieht
        ## sie diesmal nicht an einer Erinnerung, sondern an einem Frieren.
        ##
        ## Die vier Karten sind die, in denen Kälte und Nässe im Text
        ## wirklich vorkommen - das Schanzen im ersten Herbst, der Frost an
        ## Weihnachten 1914, die Winterstellung und der nasse Graben von
        ## 1917. Der Zuschlag ist mit 3 bis 4 bewusst niedriger als der von
        ## "verbruederung" (4) oder "buergertum" (5): Er soll die Karten
        ## wahrscheinlicher machen, nicht unausweichlich.
        ##
        ## DASS DARAUS KEIN ZWANGSLÄUFIGES ENDE WIRD, IST GEMESSEN, nicht
        ## angenommen - Probe 10e spielt Durchgänge mit allen sieben
        ## ohne_-Merkmalen und vergleicht die Abbruchquote.
        "front_1914_schanzen": {"gewicht_bonus": {"ohne_mantel": 4}},
        "front_1914_weihnachten": {"gewicht_bonus": {"ohne_mantel": 3}},
        "front_1917_winterstellung": {"gewicht_bonus": {"ohne_mantel": 4}},
        "front_1917_geruecht_osten": {"gewicht_bonus": {"ohne_mantel": 3}},
    }


################################################################################
## 6. Funktionen: Kapitel und Ziehung
################################################################################
##
## init 2 läuft nach dem Aufbau des Ereignisbestands (init 0) und nach den
## Nachträgen aus herkunft.rpy (init 1). Erst hier lassen sich Funktionen
## aus script.rpy zuverlässig überschreiben.

init 2 python:

    ## Nachträge einspielen ###################################################

    def rueckbezuege_nachtragen():
        for kennung, angaben in RUECKBEZUG_NACHTRAG.items():
            vorlage = EREIGNIS_INDEX.get(kennung)
            if vorlage is None:
                continue
            if "gewicht_bonus" in angaben:
                bestand = dict(getattr(vorlage, "gewicht_bonus", {}))
                bestand.update(angaben["gewicht_bonus"])
                vorlage.gewicht_bonus = bestand
            if "braucht_eines" in angaben:
                vorlage.braucht_eines = list(angaben["braucht_eines"])

    rueckbezuege_nachtragen()

    ## Ziehungszahlen #########################################################

    def ziehungen_pro_kapitel(jahr=None, modus=None):
        """Wie viele Ereignisse dieses Kapitel vorsieht.

        Ersetzt die gleichmäßige Verteilung aus script.rpy. Die Zahlen
        stehen in KAPITEL_ZIEHUNGEN und sind absichtlich ungleich.
        """
        if jahr is None:
            jahr = aktuelles_jahr
        if modus is None:
            modus = spielmodus
        tabelle = KAPITEL_ZIEHUNGEN.get(modus, KAPITEL_ZIEHUNGEN["lang"])
        return max(0, tabelle.get(jahr, 1))

    def ziehungen_summe(modus, nur_kriegsjahre=True):
        """Kontrollrechnung für die Bestandsprobe."""
        tabelle = KAPITEL_ZIEHUNGEN.get(modus, {})
        gesamt = 0
        for jahr, anzahl in tabelle.items():
            if nur_kriegsjahre and jahr == EPILOG_JAHR:
                continue
            gesamt = gesamt + anzahl
        return gesamt

    ## Kapitelwirkung #########################################################

    def kapitel_wirkung(jahr, pfad):
        """Grundwirkung des Jahreswechsels plus Zuschlag für den Pfad."""
        wirkung = dict(KAPITEL_WIRKUNG.get(jahr, {}))
        zusatz = KAPITEL_WIRKUNG_PFAD.get(jahr, {}).get(pfad, {})
        for schluessel, betrag in zusatz.items():
            wirkung[schluessel] = wirkung.get(schluessel, 0) + betrag
        return wirkung

    def wirkung_entschaerfen(wirkung):
        """Der Jahreswechsel in den Epilog tötet nicht.

        Wer den 11. November 1918 erlebt hat, soll den Durchgang mit einem
        Lebenslauf beenden und nicht daran sterben, dass eine Tabelle
        einen Punkt abzieht. Innerhalb des Epilogs bleibt die Lage
        trotzdem so schlecht, wie sie ist.
        """
        sicher = dict(wirkung)
        werte = zustand_lesen()

        grenze = ENDE_SCHWELLEN["versorgung_unter"]
        if werte["versorgung"] + sicher.get("versorgung", 0) < grenze:
            sicher["versorgung"] = grenze - werte["versorgung"]

        grenze = ENDE_SCHWELLEN["belastung_ab"] - 1
        if werte["belastung"] + sicher.get("belastung", 0) > grenze:
            sicher["belastung"] = grenze - werte["belastung"]

        grenze = ENDE_SCHWELLEN["aufmerksamkeit_ab"] - 1
        if werte["aufmerksamkeit"] + sicher.get("aufmerksamkeit", 0) > grenze:
            sicher["aufmerksamkeit"] = grenze - werte["aufmerksamkeit"]

        for schluessel in list(sicher.keys()):
            if sicher[schluessel] == 0:
                del sicher[schluessel]
        return sicher

    def kapitel_wirkung_anwenden(jahr):
        """Trägt die Wirkung ein und meldet zurück, was wirklich ankam."""
        wirkung = kapitel_wirkung(jahr, aktueller_pfad)
        if jahr >= EPILOG_JAHR:
            wirkung = wirkung_entschaerfen(wirkung)
        zustand_aendern(wirkung)
        ergebnis = {}
        for schluessel, betrag in letzte_aenderungen.items():
            if betrag:
                ergebnis[schluessel] = betrag
        return ergebnis

    def wirkung_zeilen(wirkung):
        """Bereitet eine Werteveränderung für die Anzeige auf.

        EINE QUELLE FÜR ZWEI ANZEIGEN. Die Jahreskarte nennt die Richtung
        in Worten ("Hunger steigt"), das Wertefeedback aus Paket 8,
        Schritt 2.2 nennt Zeichen und Zahl ("Hunger +2"). Beide holen sich
        dasselbe hier, damit die Frage, was gut und was schlecht ist, im
        ganzen Projekt genau einmal beantwortet wird.

        DAS VORZEICHEN GILT FÜR DEN ANGEZEIGTEN NAMEN, NICHT FÜR DEN
        ROHWERT — und das ist der Punkt, an dem man sich vertun kann. Der
        Wert heißt intern `versorgung` und wird als "Hunger" angezeigt.
        Steigt die Versorgung um 2, dann SINKT der Hunger; "Hunger +2"
        wäre also schlicht falsch, obwohl der Rohwert um +2 gestiegen ist.

        Der frühere Kommentar an dieser Stelle nannte genau dieses Risiko
        als Grund, gar keine Zahlen zu zeigen: Ein Minus dürfe nicht als
        etwas Gutes missverstanden werden. Das Missverständnis ist mit der
        Umrechnung nicht nur vermieden, sondern umgekehrt aufgelöst — denn
        **alle vier Anzeigenamen benennen etwas Schlechtes**: Hunger,
        Erschöpfung, Verdacht, Einsamkeit. Dadurch gilt ohne Ausnahme:

            ein Plus ist immer schlecht, ein Minus immer gut.

        Zeichen und Farbe sagen damit dasselbe, statt sich zu widersprechen.

        Geliefert wird je verändertem Wert:
            name        der angezeigte Name ("Hunger")
            richtung    "steigt" / "sinkt", auch "deutlich" ab 2
            schlechter  True, wenn die Lage schlechter wird
            betrag      die ROHE Änderung, wie sie in aenderungen steht
            gezeigt     dieselbe Änderung in der Sprache des Namens
            zeichen     gezeigt als Text, mit Vorzeichen ("+2", "-1")
        """
        zeilen = []
        if not wirkung:
            return zeilen
        for schluessel in WERTE_REIHENFOLGE:
            betrag = wirkung.get(schluessel, 0)
            if not betrag:
                continue
            if WERT_HOCH_IST_GUT.get(schluessel, True):
                schlechter = betrag < 0
                gezeigt = -betrag
            else:
                schlechter = betrag > 0
                gezeigt = betrag
            stark = abs(betrag) >= 2
            if schlechter:
                richtung = "steigt deutlich" if stark else "steigt"
            else:
                richtung = "sinkt deutlich" if stark else "sinkt"
            zeilen.append({
                "name": WERT_BEZEICHNUNG[schluessel],
                "richtung": richtung,
                "schlechter": schlechter,
                "betrag": betrag,
                "gezeigt": gezeigt,
                "zeichen": ("+" + str(gezeigt)) if gezeigt > 0 else str(gezeigt),
            })
        return zeilen

    ## Ziehung mit Rückbezug ##################################################

    def ereignis_passt(vorlage, jahr, pfad, modus):
        """Wie in script.rpy, zusätzlich mit braucht_eines."""
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
        eines = getattr(vorlage, "braucht_eines", [])
        if eines:
            treffer = False
            for name in eines:
                if name in merkmale:
                    treffer = True
            if not treffer:
                return False
        return True

    ## Zuschlag für das tragende Ereignis des Jahres ###########################
    ##
    ## SEIT PAKET 3, SCHRITT 2. Solange in diesem Kapitel noch keines der
    ## Trägerereignisse aus KAPITEL_BOGEN gezogen wurde, bekommen sie einen
    ## Zuschlag. Ist eines gefallen, ist der Zuschlag weg, und die übrigen
    ## Ereignisse kommen wieder gleichberechtigt zum Zug.
    ##
    ## Warum ein Sog und kein Zwang: Ein festgesetztes Pflichtereignis
    ## machte aus jedem Durchgang dieselbe Geschichte, und die Spielerin
    ## merkte es beim zweiten Mal. Ein Zuschlag sorgt dafür, dass der
    ## tragende Moment fast immer vorkommt und trotzdem nicht immer an
    ## derselben Stelle.

    BOGEN_ZUSCHLAG = 10

    def bogen_traeger_offen(jahr, pfad):
        """Steht der tragende Moment dieses Kapitels noch aus?

        Hieß bis Paket 4 bogen_kern_offen(). Der alte Name stammte aus
        KAPITEL_BOGEN["kern"] und stand neben Ereignis.kern, das etwas
        ganz anderes bedeutet: die Ziehbarkeit im kurzen Verlauf.

        Der Filter unten bleibt trotzdem stehen. Er ist die zweite
        Sicherung: Fiele ein Träger doch einmal ohne kern=True in die
        Liste, bliebe sein Zuschlag bis zum Kapitelende offen und hielte
        alle übrigen Ereignisse klein. Seit Paket 4 meldet probe_alles.py
        einen solchen Träger, statt ihn nur stillschweigend zu übergehen.
        """
        traeger = kapitel_bogen(jahr, pfad).get("träger", [])
        if not traeger:
            return []

        ## Nur Ereignisse, die in diesem Verlauf überhaupt fallen können.
        erreichbar = []
        for kennung in traeger:
            vorlage = EREIGNIS_INDEX.get(kennung)
            if vorlage is None:
                continue
            if spielmodus == "kurz" and not vorlage.kern:
                continue
            erreichbar.append(kennung)
        if not erreichbar:
            return []

        offen = [k for k in erreichbar if k not in gespielte_ereignisse]
        return offen if len(offen) == len(erreichbar) else []

    def ereignis_gewicht(vorlage):
        """Grundgewicht, Zuschlag für Merkmale, Zuschlag für den Jahresbogen."""
        gewicht = vorlage.gewicht
        for name, betrag in getattr(vorlage, "gewicht_bonus", {}).items():
            if name in merkmale:
                gewicht = gewicht + betrag
        if vorlage.kennung in bogen_traeger_offen(aktuelles_jahr, aktueller_pfad):
            gewicht = gewicht + BOGEN_ZUSCHLAG
        return max(1, gewicht)

    def ereignis_ziehen(jahr, pfad, modus):
        aus_kette = kette_faellig(jahr, pfad)
        if aus_kette:
            return aus_kette
        auswahl = ereignisse_verfuegbar(jahr, pfad, modus)
        if not auswahl:
            return None
        gewaehlt = gewichtet_ziehen(auswahl, ereignis_gewicht)
        return gewaehlt.kennung

    ## Verjährung des Verdachts ###############################################
    ##
    ## SEIT PAKET 3, VORWEG. Die Aufmerksamkeit war der einzige der vier
    ## Werte, der praktisch nur steigen konnte. Gemessen im ganzen Bestand:
    ##
    ##   versorgung      15 von 72 Optionen können ihn senken  (20,8 %)
    ##   belastung       17 von 72                             (23,6 %)
    ##   aufmerksamkeit   6 von 72                             ( 8,3 %)
    ##   rueckhalt       26 von 72                             (36,1 %)
    ##
    ## Und alle sechs Wege nach unten hießen dasselbe: melden, zeichnen,
    ## unterschreiben, bestätigen. Wer sich nicht anpasste, hatte gar keinen
    ## Weg. Dazu hebt KAPITEL_WIRKUNG den Wert 1916 und 1917 noch einmal an.
    ## Ein Wert, der nur steigen kann, ist keine Entscheidung mehr, sondern
    ## ein Countdown. Im langen Heimatverlauf endeten 82,5 Prozent der klug
    ## gespielten Durchgänge mit einer Verhaftung.
    ##
    ## Die Verjährung ist der Weg nach unten, der KEINE Anpassung verlangt.
    ## Historisch trägt sie: Die Überwachung lief über Akten, Vermerke und
    ## Listen, die von wechselnden Beamten geführt wurden. Dienststellen
    ## wurden verlegt, Sachbearbeiter eingezogen, Vorgänge blieben liegen.
    ## Wer eine Weile in keiner Meldung vorkam, verschwand aus dem Blick -
    ## nicht weil man ihm verzieh, sondern weil andere Namen nachrückten.
    ##
    ## Gezählt wird in Ziehungen, nicht in Jahren, und gemessen wird gegen
    ## den Stand bei der letzten Ziehung. Dadurch setzt auch ein Brief oder
    ## eine Einlage, die den Verdacht hebt, die Ruhe zurück.
    ##
    ## Kein Freikaufen: Die Verjährung lässt sich nicht wählen, nicht
    ## beschleunigen und nicht erzwingen. Sie tritt ein, wenn drei
    ## Ziehungen lang nichts dazugekommen ist, und senkt dann um eins.
    ##
    ## Gemessen wurde 4 und 3. Mit 3 erreichen im langen Heimatverlauf
    ## 32,3 statt 27,8 Prozent der klug gespielten Durchgänge das Jahr
    ## 1919. Beide Zahlen sind gleich gut begründbar; genommen wurde die
    ## wirksamere.

    VERDACHT_RUHE = 3

    def verdacht_verjaehren():
        """Senkt den Verdacht, wenn lange nichts dazugekommen ist.

        Liefert die Änderung zurück, damit der Aufrufer sie in die
        Anzeige der letzten Änderungen aufnehmen kann.
        """
        global verdacht_ruhig, verdacht_stand

        jetzt = zustand_lesen()["aufmerksamkeit"]

        if jetzt > verdacht_stand:
            ## Es ist etwas dazugekommen. Die Ruhe beginnt von vorn.
            verdacht_ruhig = 0
            verdacht_stand = jetzt
            return 0

        verdacht_stand = jetzt
        verdacht_ruhig = verdacht_ruhig + 1

        if verdacht_ruhig < VERDACHT_RUHE:
            return 0

        verdacht_ruhig = 0
        if jetzt <= 0:
            return 0

        zustand_aendern({"aufmerksamkeit": -1})
        verdacht_stand = zustand_lesen()["aufmerksamkeit"]
        return -1

    ## Die Verjährung hängt sich um option_ausfuehren, statt in script.rpy
    ## einzugreifen. Der festgehaltene Name verhindert, dass die neue
    ## Fassung sich selbst aufruft.
    option_ausfuehren_vor_verjaehrung = option_ausfuehren

    def option_ausfuehren(kennung, stelle):
        global letzte_aenderungen

        ergebnis = option_ausfuehren_vor_verjaehrung(kennung, stelle)

        if ergebnis.get("sprung"):
            return ergebnis

        ## Die Anzeige in der Kopfleiste liest letzte_aenderungen. Ein
        ## zweiter Aufruf von zustand_aendern() würde sie überschreiben und
        ## die Wirkung der eben getroffenen Wahl verschlucken. Deshalb wird
        ## gemerkt, verjährt und danach zusammengezählt.
        gemerkt = dict(letzte_aenderungen)
        if verdacht_verjaehren():
            zusammen = dict(gemerkt)
            for schluessel, betrag in letzte_aenderungen.items():
                zusammen[schluessel] = zusammen.get(schluessel, 0) + betrag
            letzte_aenderungen = zusammen
        else:
            letzte_aenderungen = gemerkt

        return ergebnis

    ## Beim Neustart beginnt auch die Ruhe von vorn.
    zustand_zuruecksetzen_vor_verjaehrung = zustand_zuruecksetzen

    def zustand_zuruecksetzen():
        global verdacht_ruhig, verdacht_stand
        zustand_zuruecksetzen_vor_verjaehrung()
        verdacht_ruhig = 0
        verdacht_stand = zustand_lesen()["aufmerksamkeit"]

    ## Harte Abbrüche #########################################################

    def ende_pruefen():
        """Verhungern, Zusammenbruch und Verhaftung bleiben Abbrüche.

        Im Epilog greifen sie nicht mehr. Wer das Kriegsende erlebt hat,
        bekommt den Lebenslauf; wie schlecht es ihm dabei geht, steht
        dort und nicht in einer Todesmeldung.
        """
        if aktuelles_jahr >= EPILOG_JAHR:
            return None
        if versorgung < ENDE_SCHWELLEN["versorgung_unter"]:
            return "ende_verhungert"
        if belastung >= ENDE_SCHWELLEN["belastung_ab"]:
            return "ende_zusammenbruch"
        if aufmerksamkeit >= ENDE_SCHWELLEN["aufmerksamkeit_ab"]:
            return "ende_verhaftet"
        return None

    ## Bestand ################################################################

    def bestand_liste(jahr, pfad, modus):
        """Welche Ereignisse für dieses Kapitel überhaupt bestehen.

        Liefert zwei Listen: die frei ziehbaren und die, die an einem
        Merkmal hängen. Merkmalsbedingungen werden hier NICHT geprüft,
        weil sie von Durchgang zu Durchgang verschieden sind; sie werden
        getrennt geführt, damit sichtbar wird, wie viel Bestand nur unter
        Bedingungen erreichbar ist.

        SEIT PAKET 5, SCHRITT 3, TEIL D.15c. Vorher gab es nur die
        Zählung, und wer die LISTE brauchte, baute die Bedingung ein
        zweites Mal nach - probe_alles.py tat das an drei Stellen mit
        einem eigenen Ausdruck, der modus gar nicht ansah. Zwei
        Formulierungen derselben Regel laufen früher oder später
        auseinander, und dann misst die Werkbank etwas anderes als das
        Spiel spielt. Jetzt gibt es eine Stelle, und bestand_zaehlen()
        zählt nur noch, was hier steht.
        """
        frei = []
        bedingt = []
        for vorlage in EREIGNISSE:
            if vorlage.nur_kette:
                continue
            if jahr not in vorlage.jahre:
                continue
            if pfad not in vorlage.pfad:
                continue
            if modus == "kurz" and not vorlage.kern:
                continue
            if vorlage.braucht or getattr(vorlage, "braucht_eines", []):
                bedingt.append(vorlage)
            else:
                frei.append(vorlage)
        return frei, bedingt

    def bestand_zaehlen(jahr, pfad, modus):
        """Wie viele Ereignisse für dieses Kapitel überhaupt bestehen."""
        frei, bedingt = bestand_liste(jahr, pfad, modus)
        return len(frei), len(bedingt)

    ## Die drei Stufen der Bestandslage ########################################
    ##
    ## Seit Paket 2, Schritt 1. "frei >= soll" allein genügt nicht als
    ## Entwarnung: Wer genau so viele Ereignisse hat, wie er ziehen soll,
    ## spielt in jedem Durchgang dieselben - und sobald eines davon an ein
    ## Merkmal gebunden ist, das gerade fehlt, endet das Kapitel doch aus
    ## Mangel. Der Abstand von zwei Ereignissen ist die Reserve, aus der
    ## Abwechslung entsteht.

    BESTAND_RESERVE = 2

    def bestandslage(frei, soll):
        """Liefert (Kennung, Beschriftung) für die Spalte Lage."""
        if frei < soll:
            return "unterdeckung", "Unterdeckung"
        if frei < soll + BESTAND_RESERVE:
            return "knapp", "knapp"
        return "ordnung", "in Ordnung"

    def bestandsbericht():
        """Zeilen für die Bestandsprobe im Hauptmenü."""
        zeilen = []
        for modus in ["kurz", "lang"]:
            for jahr in KAPITEL_JAHRE:
                for pfad in PFAD_REIHENFOLGE:
                    frei, bedingt = bestand_zaehlen(jahr, pfad, modus)
                    soll = ziehungen_pro_kapitel(jahr, modus)
                    lage, lage_text = bestandslage(frei, soll)
                    zeilen.append({
                        "modus": MODUS_BEZEICHNUNG.get(modus, modus),
                        "jahr": jahr,
                        "pfad": PFAD_MARKE.get(pfad, pfad),
                        "soll": soll,
                        "frei": frei,
                        "bedingt": bedingt,
                        "fehlt": max(0, soll - frei),
                        "lage": lage,
                        "lage_text": lage_text,
                    })
        return zeilen

    def bestandslage_summe(zeilen):
        """Zählt aus, wie viele Zeilen in welcher Lage stehen."""
        gezaehlt = {"unterdeckung": 0, "knapp": 0, "ordnung": 0}
        for zeile in zeilen:
            gezaehlt[zeile.get("lage", "ordnung")] = gezaehlt.get(zeile.get("lage", "ordnung"), 0) + 1
        return gezaehlt

    def nachhallbericht():
        """Welche geplanten Rückbezüge bestehen schon, welche fehlen."""
        zeilen = []
        for merkmal, jahr, pfad, kennung, titel in NACHHALL_PLAN:
            vorhanden = kennung in EREIGNIS_INDEX
            zeilen.append({
                "merkmal": MERKMAL_REGISTER.get(merkmal, {}).get("name", merkmal),
                "jahr": jahr,
                "pfad": pfad,
                "kennung": kennung,
                "titel": titel,
                "vorhanden": vorhanden,
            })
        return zeilen


################################################################################
## 7. Endensystem: die Ausgänge
################################################################################
##
## Vier harte Abbrüche bestehen weiter und liegen in script.rpy:
## ende_verhungert, ende_zusammenbruch, ende_verhaftet, ende_gefallen.
##
## Wer den Epilog erreicht, bekommt stattdessen einen berechneten
## Lebenslauf. Er entsteht aus drei Quellen:
##
##   1. den vier Stufen (0 bis 4) am Ende des Durchgangs,
##   2. dem Pfad, auf dem der Krieg verbracht wurde,
##   3. den gesammelten Merkmalen.
##
## Der Ausgang mit dem höchsten Rang, dessen Bedingung zutrifft, gibt dem
## Ende Titel und Deutung. Zehn Ausgänge stehen bereit; der letzte trifft
## immer zu und fängt alle übrigen Lagen auf.
##
## Die Reihenfolge folgt der Schwere: Ein Körper, der den Hunger nicht
## loswird, bestimmt das Leben stärker als eine politische Haltung. Was
## dabei untergeht, kehrt über die Merkmale in der Zeitleiste zurück.

init 1 python:

    class Ausgang(object):

        def __init__(self, kennung, titel, rang, bedingung, deutung,
                     eintrag, lehrplan=""):
            self.kennung = kennung
            self.titel = titel
            self.rang = rang
            self.bedingung = bedingung
            self.deutung = deutung
            self.eintrag = eintrag
            self.lehrplan = lehrplan

    def ende_stufen():
        werte = zustand_lesen()
        stufen = {}
        for schluessel in WERTE_REIHENFOLGE:
            stufen[schluessel] = stufe_von_wert(schluessel, werte[schluessel])
        return stufen

    def eines_der_merkmale(namen):
        for name in namen:
            if name in merkmale:
                return True
        return False


init 2 python:

    ENDE_AUSGAENGE = [

        Ausgang(
            "gezeichnet",
            "Gezeichnet",
            90,
            lambda stufen, pfad: stufen["versorgung"] >= 3,
            "Der Krieg ist zu Ende. Dein Hunger ist es nicht.",
            (1920, "1919 bis 1921", (
                "Du wiegst weniger als im August 1914 und nimmst nicht zu, auch als "
                "es wieder Brot gibt. Ein Arzt schreibt Hungerödem in den Bogen und "
                "gibt dir eine Bescheinigung, mit der du nichts anfangen kannst. Zwei "
                "Winter später hustest du immer noch."
            )),
            lehrplan="Kl. 8, WB 2: Langzeitfolgen der Mangelernährung, Tuberkulose in den Nachkriegsjahren."
        ),

        Ausgang(
            "nervenkrank",
            "Nicht mehr derselbe Mensch",
            88,
            lambda stufen, pfad: stufen["belastung"] >= 3,
            "Der Körper ist zurückgekommen. Etwas anderes nicht.",
            (1920, "1920", (
                "Du zuckst zusammen, wenn eine Tür ins Schloss fällt, und du bekommst "
                "es nicht abgestellt. In der Akte des Versorgungsamts steht "
                "Kriegsneurose. Ob dafür eine Rente gezahlt wird, entscheidet ein "
                "Gutachter, der dich zwanzig Minuten sieht."
            )),
            lehrplan="Kl. 8, WB 1/2: Kriegszitterer, Reichsversorgungsgesetz 1920, Gutachterpraxis. Zeitgenössischer Begriff: Kriegsneurose."
        ),

        Ausgang(
            "aktenkundig",
            "Aktenkundig",
            86,
            lambda stufen, pfad: stufen["aufmerksamkeit"] >= 3,
            "Man hat dich nicht geholt. Aufgeschrieben hat man dich trotzdem.",
            (1919, "1919", (
                "Das stellvertretende Generalkommando wird aufgelöst, deine Akte "
                "nicht. Sie wandert in ein Regal der Polizeibehörde und bleibt dort "
                "liegen. Eine Stelle im öffentlichen Dienst bekommst du nicht, und "
                "niemand sagt dir, warum."
            )),
            lehrplan="Kl. 8: Belagerungszustandsgesetz 1851, Schutzhaft, Fortbestand der Akten über 1918 hinaus."
        ),

        Ausgang(
            "vereinsamt",
            "Allein zurück",
            84,
            lambda stufen, pfad: stufen["rueckhalt"] >= 3,
            "Du hast überlebt. Es ist niemand mehr da, dem das etwas bedeutet.",
            (1919, "1919", (
                "Die Wohnung ist dieselbe, die Menschen darin sind es nicht. Im "
                "Treppenhaus wird gegrüßt, mehr nicht. Es gibt niemanden, dem du "
                "diese Jahre erzählen müsstest. Nach einer Weile hörst du auf, "
                "es zu versuchen."
            )),
            lehrplan="Kl. 8, WB 2: Zerfall von Nachbarschaft und Familie unter Mangel, Denunziation und Verlust."
        ),

        Ausgang(
            "nicht_angekommen",
            "Zurück, aber nicht angekommen",
            70,
            ## Verschlissen oder entfremdet, eines von beidem genügt.
            ## Beides zusammen zu verlangen, hat diesen Ausgang in der
            ## Probe auf unter zwei Prozent gedrückt, obwohl er der
            ## lehrplanrelevanteste des Frontpfads ist.
            lambda stufen, pfad: (
                pfad in ("front", "etappe")
                and (stufen["belastung"] >= 2 or stufen["rueckhalt"] >= 2)
            ),
            "Du bist heimgekommen. Angekommen bist du woanders.",
            (1920, "1920", (
                "In der Wirtschaft am Markt treffen sich die, die dabei waren. Dort "
                "wird erzählt, das Heer sei im Feld unbesiegt geblieben und zu Hause "
                "verraten worden. Du weißt, wie der Napf aussah und was in den Gräben "
                "lag. Du widersprichst nicht, weil es die Einzigen sind, die "
                "überhaupt fragen."
            )),
            lehrplan="Kl. 9, LB 2: Entstehung der Dolchstoßlegende aus der Erfahrung der Heimkehrer, Frontkämpferverbände."
        ),

        Ausgang(
            "in_der_bewegung",
            "In der Bewegung",
            68,
            lambda stufen, pfad: (
                eines_der_merkmale(["arbeiterschaft", "ruestung"])
                and (hat_merkmal("vorangegangen") or stufen["aufmerksamkeit"] >= 2)
            ),
            "Was im Betrieb angefangen hat, hört mit dem Krieg nicht auf.",
            (1919, "1919", (
                "Im Werk wird ein Rat gewählt, und dein Name steht auf der Liste. Es "
                "gibt den Achtstundentag und Verhandlungen mit der Werkleitung. Ob "
                "davon etwas bleibt, weiß in diesem Frühjahr niemand; gestritten wird "
                "darüber schon jetzt mit Waffen."
            )),
            lehrplan="Kl. 9, LB 1: Novemberrevolution, Räte, Stinnes-Legien-Abkommen, Betriebsrätegesetz 1920."
        ),

        Ausgang(
            "auf_eigenen_beinen",
            "Auf eigenen Beinen",
            66,
            lambda stufen, pfad: (
                lebenslage is not None
                and lebenslage.geschlecht == "w"
                and eines_der_merkmale(["ruestung", "verwaltung", "lazarett", "haushalt", "wohlfahrt"])
                and stufen["belastung"] <= 2
            ),
            "Du hast vier Jahre lang getragen, was sonst andere getragen hätten.",
            (1919, "1919", (
                "Am 19. Januar gehst du zum ersten Mal wählen. Im selben Frühjahr "
                "kommen die Verordnungen über die Demobilmachung: Stellen, die Frauen "
                "im Krieg übernommen haben, sollen an Heimkehrer zurück. Du bekommst "
                "eine Abfindung von zwei Wochenlöhnen und die Auskunft, das sei "
                "gerecht."
            )),
            lehrplan="Kl. 9, LB 1: Frauenwahlrecht 19.1.1919, Weimarer Verfassung; zugleich Verdrängung der Frauen aus der Erwerbsarbeit 1919/20."
        ),

        Ausgang(
            "bewahrt_und_verloren",
            "Bewahrt und verloren",
            64,
            lambda stufen, pfad: (
                eines_der_merkmale(["buergertum", "adel"])
                and stufen["versorgung"] <= 1
            ),
            "Ihr seid durchgekommen, ohne etwas zu entbehren. Behalten habt ihr es nicht.",
            (1923, "1923", (
                "Die Familie hat den Krieg mit ihrem Vermögen überstanden. Neun "
                "Zehntel davon liegen in Kriegsanleihen, gezeichnet aus Überzeugung. "
                "Im Herbst 1923 reicht die Summe für ein Brot, wenn du dich beeilst."
            )),
            lehrplan="Kl. 9, LB 2: Kriegsanleihen, Inflation 1923, Enttäuschung des Bürgertums als Mentalitätsfaktor."
        ),

        Ausgang(
            "zusammengeblieben",
            "Zusammengeblieben",
            40,
            lambda stufen, pfad: (
                stufen["rueckhalt"] <= 1
                and stufen["belastung"] <= 2
                and stufen["versorgung"] <= 2
            ),
            "Ihr seid vollzählig. In dieser Straße ist das die Ausnahme.",
            (1919, "1919", (
                "Am Sonntag sitzt ihr am Tisch, und es ist genug für alle da. Über "
                "die vier Jahre wird nicht gesprochen. Die Nachbarin gegenüber hat "
                "zwei Söhne verloren und kommt nicht mehr herüber."
            )),
            lehrplan="Kl. 8, WB 2: Ungleichheit der Kriegserfahrung; Überleben war auch eine Frage von Milieu und Zufall."
        ),

        Ausgang(
            "weitergelebt",
            "Weitergelebt",
            0,
            lambda stufen, pfad: True,
            "Der Krieg ist vorbei, und es geht weiter. Etwas anderes ist nicht vorgesehen.",
            (1919, "1919", (
                "Du gehst wieder arbeiten, weil es weitergehen muss. Später wirst du "
                "gefragt, wie es gewesen ist, und du merkst, dass die Antwort nicht "
                "in einen Satz passt. Also sagst du: Es war Krieg."
            )),
            lehrplan="Auffangausgang. Erscheint, wenn keine Lage besonders heraussticht."
        ),
    ]

    ENDE_AUSGANG_INDEX = {}
    for _ausgang in ENDE_AUSGAENGE:
        ENDE_AUSGANG_INDEX[_ausgang.kennung] = _ausgang


################################################################################
## 8. Endensystem: der Lebensweg
################################################################################
##
## Die Zeitleiste besteht aus höchstens sechs Einträgen:
##
##   1. November 1918, abhängig vom Pfad
##   2. der Haupteintrag des Ausgangs
##   3. bis zu zwei Einträge aus den Merkmalen (Nachklang, Abschnitt 5)
##   4. ein Zusatzeintrag zur politischen Lage
##   5. Versailles, immer
##
## Sortiert wird nach Jahr. Dadurch entsteht aus festen Bausteinen eine
## Abfolge, die sich zwischen zwei Durchgängen deutlich unterscheidet,
## ohne dass ein einziger Satz erfunden werden müsste.

init 2 python:

    LEBENSWEG_KRIEGSENDE = {
        "front": (1918, "November 1918", (
            "Der Rückmarsch dauert Wochen. In den Dörfern hängen Fahnen, in Berlin "
            "werden die Truppen mit dem Satz begrüßt, kein Feind habe sie "
            "überwunden. In deiner Kompanie sind von den Männern des letzten "
            "Sommers elf übrig."
        )),
        "etappe": (1918, "November 1918", (
            "Die Formation löst sich auf, bevor der Befehl dazu eintrifft. Züge "
            "werden von Soldatenräten eingeteilt, Vorräte verschwinden über Nacht. "
            "Du fährst nach Hause mit dem, was in einen Brotbeutel passt."
        )),
        "heimat": (1918, "November 1918", (
            "Im Ort werden Arbeiter- und Soldatenräte gebildet. Am Rathaus hängt "
            "eine rote Fahne, dann wieder keine. Die Läden bleiben leer, aber zum "
            "ersten Mal seit vier Jahren fährt kein Zug mehr an die Front."
        )),
    }

    ## Zusatzeintrag zur politischen Lage. Der erste zutreffende gilt.
    LEBENSWEG_LAGE = [
        {
            "kennung": "dolchstoss",
            "bedingung": lambda stufen, pfad: pfad in ("front", "etappe"),
            "eintrag": (1919, "November 1919", (
                "Vor einem Untersuchungsausschuss des Reichstags sagt Hindenburg, "
                "das deutsche Heer sei von hinten erdolcht worden. Der Satz steht am "
                "nächsten Tag in jeder Zeitung. Wer im Feld war, wird von nun an "
                "gefragt, auf welcher Seite er dabei gestanden hat."
            )),
        },
        {
            "kennung": "verfassung",
            "bedingung": lambda stufen, pfad: eines_der_merkmale(
                ["haushalt", "wohlfahrt", "arbeiterschaft", "ruestung", "verwaltung"]
            ),
            "eintrag": (1919, "August 1919", (
                "Am 11. August wird die neue Verfassung unterschrieben. Sie gibt "
                "allen ab zwanzig das Wahlrecht, Männern wie Frauen. Ob die Republik "
                "hält, entscheidet sich an anderen Stellen als in der Wahlkabine."
            )),
        },
        {
            "kennung": "denkmal",
            "bedingung": lambda stufen, pfad: True,
            "eintrag": (1922, "1922", (
                "Im Ort wird ein Denkmal eingeweiht. Auf der Tafel stehen "
                "vierundsechzig Namen aus einer Gemeinde mit achthundert Einwohnern. "
                "Ein Pfarrer spricht, ein Verband legt einen Kranz, danach geht man "
                "nach Hause."
            )),
        },
    ]

    LEBENSWEG_VERSAILLES = (1919, "28. Juni 1919", (
        "In Versailles unterschreibt die deutsche Abordnung einen Vertrag, über den "
        "sie nicht verhandeln durfte. Er nimmt dem Reich Gebiete, das Heer und sehr "
        "viel Geld. In Artikel 231 steht, wer den Krieg zu verantworten habe. In "
        "den Zeitungen heißt er von der ersten Zeile an das Diktat."
    ))


################################################################################
## 9. Endensystem: Berechnung
################################################################################

init 2 python:

    def ende_ausgang_bestimmen():
        stufen = ende_stufen()
        gefunden = None
        for eintrag in ENDE_AUSGAENGE:
            try:
                trifft = eintrag.bedingung(stufen, aktueller_pfad)
            except Exception:
                trifft = False
            if not trifft:
                continue
            if gefunden is None or eintrag.rang > gefunden.rang:
                gefunden = eintrag
        if gefunden is None:
            gefunden = ENDE_AUSGANG_INDEX["weitergelebt"]
        return gefunden

    ## DIE VIER FÄCHER DES LEBENSLAUFS #########################################
    ##
    ## SEIT PAKET 5, SCHRITT 3, TEIL E. Entscheidung 10 des Projektleiters.
    ##
    ## Der Lebenslauf zeigte bis hierher die höchstrangigen Merkmale mit
    ## Nachklang, gleich aus welchem Bereich sie kamen. Das Ergebnis war
    ## messbar schief: Die Herkunft liegt bei Rang 32 bis 34, Erwerbslage
    ## und Stellung bei 46 bis 60, und jede Figur trägt mindestens eine
    ## davon. Wer aus dem Adel kam oder vom Land, bekam das am Ende
    ## praktisch nie zu sehen. Drei Plätze statt zwei haben das gemildert,
    ## nicht behoben.
    ##
    ## Der Grund für die Änderung liegt nicht in der Technik, sondern im
    ## Unterricht: Das Spiel läuft auf den Vergleich zweier Lebensläufe zu.
    ## Fällt die Herkunft heraus, vergleichen zwei Schülerinnen nur noch,
    ## was ihnen zugestoßen ist - nicht, woher sie gestartet sind. Genau
    ## dieser Unterschied ist die Stunde.
    ##
    ## Ab jetzt gibt es vier feste Fächer. Jedes zieht seinen obersten
    ## Eintrag; der Rang entscheidet nur noch INNERHALB eines Fachs. Ist
    ## ein Fach leer, bleibt es leer - es rückt nichts nach.
    ##
    ## Die Zuordnung ist nicht neu erfunden: MERKMAL_REGISTER führt seit
    ## Paket 2 zu jedem Merkmal eine "gruppe", und die sechs Gruppen gehen
    ## ohne Rest in den vier Fächern auf. Nur die drei Wirtshausmerkmale
    ## werden aus "tat" herausgenommen, weil sie der Schluss sind und
    ## nicht eine Entscheidung des Krieges.
    LEBENSLAUF_FAECHER = [
        ("Woher du kamst", ["herkunft", "lage"]),
        ("Wohin es dich brachte", ["haltung", "stellung", "erwerb"]),
        ("Was du entschieden hast", ["tat"]),
        ("Wie es ausging", []),
    ]

    LEBENSLAUF_SCHLUSSMERKMALE = [
        "wirtshaus_widersprochen", "wirtshaus_geschwiegen",
        "wirtshaus_zugestimmt",
    ]

    def lebenslauf_fach(name):
        """In welches der vier Fächer gehört dieses Merkmal? Sonst None."""
        if name in LEBENSLAUF_SCHLUSSMERKMALE:
            return 3
        eintrag = MERKMAL_REGISTER.get(name)
        if eintrag is None:
            return None
        gruppe = eintrag.get("gruppe")
        for stelle in range(len(LEBENSLAUF_FAECHER)):
            if gruppe in LEBENSLAUF_FAECHER[stelle][1]:
                return stelle
        return None

    def nachklaenge_nach_faechern():
        """Je Fach der oberste Eintrag mit Nachklang.

        Sortiert wird innerhalb eines Fachs wie vorher im ganzen Feld:
        erst nach Rang, bei Gleichstand nach der Stelle in
        MERKMAL_REIHENFOLGE_LEBENSWEG. Damit trifft der Lebenslauf bei
        gleicher Lage immer dieselbe Auswahl und lässt sich im Unterricht
        wiederholen.
        """
        beste = {}
        for name in merkmale:
            eintrag = MERKMAL_REGISTER.get(name)
            if eintrag is None or not eintrag.get("nachklang"):
                continue
            fach = lebenslauf_fach(name)
            if fach is None:
                continue
            if name in MERKMAL_REIHENFOLGE_LEBENSWEG:
                stelle = MERKMAL_REIHENFOLGE_LEBENSWEG.index(name)
            else:
                stelle = 999
            schluessel = (-eintrag.get("rang", 0), stelle, name)
            if fach not in beste or schluessel < beste[fach][0]:
                beste[fach] = (schluessel, name)

        gewaehlt = []
        for fach in range(len(LEBENSLAUF_FAECHER)):
            if fach not in beste:
                continue
            name = beste[fach][1]
            jahr, marke, text = MERKMAL_REGISTER[name]["nachklang"]
            gewaehlt.append({
                "jahr": jahr,
                "marke": marke,
                "text": text,
                ## Im Analysemodus steht neben der Jahresmarke, aus welchem
                ## Fach der Eintrag kommt. Für die Lehrkraft ist das die
                ## Auskunft, die den Vergleich zweier Lebensläufe trägt.
                "quelle": LEBENSLAUF_FAECHER[fach][0] + ": "
                          + MERKMAL_REGISTER[name]["name"],
                "fach": LEBENSLAUF_FAECHER[fach][0],
                "merkmal": name,
            })
        return gewaehlt

    ## ÜBERHOLT SEIT PAKET 5, SCHRITT 3, aber nicht entfernt (Regel 9).
    ## Die Rangliste über alle Bereiche hinweg; sie hat den Lebenslauf bis
    ## zu diesem Schritt gefüllt. Wer wissen will, was die Fächer geändert
    ## haben, ruft beide auf und vergleicht.
    def nachklaenge_waehlen(hoechstens=2):
        """Sucht die zwei gewichtigsten Merkmale mit Nachklang heraus."""
        kandidaten = []
        for name in merkmale:
            eintrag = MERKMAL_REGISTER.get(name)
            if eintrag is None:
                continue
            if not eintrag.get("nachklang"):
                continue
            if name in MERKMAL_REIHENFOLGE_LEBENSWEG:
                stelle = MERKMAL_REIHENFOLGE_LEBENSWEG.index(name)
            else:
                stelle = 999
            kandidaten.append((-eintrag.get("rang", 0), stelle, name))
        kandidaten.sort()
        gewaehlt = []
        for _rang, _stelle, name in kandidaten[:hoechstens]:
            jahr, marke, text = MERKMAL_REGISTER[name]["nachklang"]
            gewaehlt.append({
                "jahr": jahr,
                "marke": marke,
                "text": text,
                "quelle": MERKMAL_REGISTER[name]["name"],
            })
        return gewaehlt

    def lage_eintrag_waehlen():
        stufen = ende_stufen()
        for eintrag in LEBENSWEG_LAGE:
            try:
                trifft = eintrag["bedingung"](stufen, aktueller_pfad)
            except Exception:
                trifft = False
            if trifft:
                jahr, marke, text = eintrag["eintrag"]
                return {"jahr": jahr, "marke": marke, "text": text, "quelle": "Lage"}
        return None

    def ende_fazit_text(ausgang):
        """Der Satz unter der Zeitleiste. Ordnet ein, ohne zu bewerten."""
        stufen = ende_stufen()
        schwer = [WERT_BEZEICHNUNG[s] for s in WERTE_REIHENFOLGE if stufen[s] >= 3]
        if ausgang.kennung == "weitergelebt" and not schwer:
            return (
                "Von rund dreizehn Millionen eingezogenen Männern kamen etwa elf "
                "Millionen zurück. Ein Leben wie deines war der Regelfall, und auch "
                "dieser Regelfall war kein leichtes Leben."
            )
        if schwer:
            return (
                "Am schwersten wiegt am Ende: " + wert_aufzaehlung(schwer) + ". Aus "
                "Millionen solcher Lebensläufe entstand die Stimmung, in der die "
                "Republik von 1919 verteidigt oder abgelehnt wurde."
            )
        return (
            "Was aus diesen Jahren folgte, entschied sich selten an einem einzigen "
            "Tag. Es entschied sich daran, was Menschen danach über sie erzählten."
        )

    def ende_zusammenstellen():
        """Baut den vollständigen Schlussbildschirm als einfache Daten auf.

        Es werden bewusst nur Zeichenketten, Zahlen und Listen
        zurückgegeben, damit der Bildschirm keine Objekte halten muss.
        """
        ausgang = ende_ausgang_bestimmen()

        eintraege = []

        jahr, marke, text = LEBENSWEG_KRIEGSENDE.get(
            aktueller_pfad, LEBENSWEG_KRIEGSENDE["heimat"]
        )
        eintraege.append({"jahr": jahr, "marke": marke, "text": text, "quelle": "Kriegsende"})

        jahr, marke, text = ausgang.eintrag
        eintraege.append({"jahr": jahr, "marke": marke, "text": text, "quelle": "Ausgang"})

        ## VIER FÄCHER STATT EINER RANGLISTE, seit Paket 5, Schritt 3,
        ## Teil E (Entscheidung 10). Die Begründung steht bei
        ## LEBENSLAUF_FAECHER. Der Unterschied zur Fassung davor: Es sind
        ## nicht mehr die drei höchstrangigen Merkmale überhaupt, sondern
        ## je Fach das oberste - und damit steht die Herkunft in jedem
        ## Lebenslauf, statt in fast keinem.
        eintraege.extend(nachklaenge_nach_faechern())

        lage = lage_eintrag_waehlen()
        if lage is not None:
            eintraege.append(lage)

        jahr, marke, text = LEBENSWEG_VERSAILLES
        eintraege.append({"jahr": jahr, "marke": marke, "text": text, "quelle": "Versailles"})

        ## Stabil sortieren: gleiche Jahre behalten die Reihenfolge, in
        ## der sie eingetragen wurden.
        eintraege.sort(key=lambda e: e["jahr"])

        return {
            "kennung": ausgang.kennung,
            "titel": ausgang.titel,
            "deutung": ausgang.deutung,
            "lehrplan": ausgang.lehrplan,
            "eintraege": eintraege,
            "fazit": ende_fazit_text(ausgang),
        }


################################################################################
## 10. Sprachprüfung erweitern
################################################################################
##
## Die Prüfung aus herkunft.rpy erfasst bisher nur Ereignisse und Szenen.
## Ab jetzt laufen auch die Kapiteltexte, die Rückblicke und sämtliche
## Endtexte durch dieselbe Liste. Ausgenommen bleiben die Hinweise für die
## Lehrkraft (KAPITEL_LEHRPLAN, Ausgang.lehrplan): Dort dürfen fachliche
## Begriffe wie "Totaler Krieg" stehen, weil sie Unterrichtsgegenstand
## sind und nie im Spieltext erscheinen.

init 3 python:

    sprachpruefung_grundlage = sprachpruefung_durchfuehren

    def kapiteltexte_sammeln():
        bestand = []
        for jahr in KAPITEL_JAHRE:
            texte = [
                KAPITEL_UEBERSCHRIFT.get(jahr, ""),
                KAPITEL_TEXT.get(jahr, ""),
                KAPITEL_RUECKBLICK.get(jahr, ""),
                KAPITEL_WIRKUNG_TEXT.get(jahr, ""),
            ]
            texte.extend(KAPITEL_STICHWORTE.get(jahr, []))
            bestand.append(("Kapitel " + str(jahr), [t for t in texte if t]))
        return bestand

    def endtexte_sammeln():
        bestand = []
        for eintrag in ENDE_AUSGAENGE:
            texte = [eintrag.titel, eintrag.deutung, eintrag.eintrag[2]]
            bestand.append(("Ausgang " + eintrag.kennung, texte))
        for pfad, eintrag in LEBENSWEG_KRIEGSENDE.items():
            bestand.append(("Kriegsende " + pfad, [eintrag[2]]))
        for eintrag in LEBENSWEG_LAGE:
            bestand.append(("Lage " + eintrag["kennung"], [eintrag["eintrag"][2]]))
        bestand.append(("Versailles", [LEBENSWEG_VERSAILLES[2]]))
        for name, eintrag in MERKMAL_REGISTER.items():
            if eintrag.get("nachklang"):
                bestand.append(("Nachklang " + name, [eintrag["nachklang"][2]]))
        return bestand

    def sprachpruefung_durchfuehren():
        funde = sprachpruefung_grundlage()
        for ort, texte in kapiteltexte_sammeln() + endtexte_sammeln():
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
## 10b. Paket 4, Vorweg: Nachträge an bestehendem Bestand
################################################################################
##
## Vier Nachträge, die vor den Inhalten von 1917 und 1918 erledigt sein
## müssen. Sie stehen hier in EINEM Block und nicht verstreut in script.rpy
## und herkunft.rpy, weil sie zusammen gelesen werden müssen: Jeder von
## ihnen ändert nur Zahlen, Jahre oder Felder - keinen einzigen Satz, den
## eine Spielerin liest.
##
## init 3 läuft nach dem Aufbau des Bestands (init 0), nach den Nachträgen
## aus herkunft.rpy (init 1) und nach denen aus Abschnitt 6 (init 2). Erst
## hier steht der vollständige Bestand.

init 3 python:

    ## ------------------------------------------------------------------ A
    ## Träger, die im kurzen Verlauf nicht gezogen werden können
    ##
    ## KAPITEL_BOGEN nennt je Jahr und Pfad die Ereignisse, die das Jahr
    ## tragen. Vier von ihnen hatten kern=False und waren damit im kurzen
    ## Verlauf gar nicht ziehbar. Ein solcher Träger trägt nichts: Sein
    ## Zuschlag bleibt bis zum Kapitelende offen, und die übrigen
    ## Ereignisse bleiben so lange klein.
    ##
    ## Der Nachtrag setzt kern=True, statt die vier aus dem Bogen zu
    ## nehmen. Sachlich passt jedes von ihnen in einen kurzen Verlauf:
    ##
    ##   heimat_1914_liebesgaben  Die Sammlung für die Front ist der
    ##                            Moment, in dem 1914 in der Heimat alle
    ##                            mitmachen. Ohne ihn fehlt dem kurzen
    ##                            Verlauf genau die Frage des Jahres.
    ##   heimat_lazarettzug       Der ankommende Zug ist die erste Stelle,
    ##                            an der die Heimat sieht, was vorn
    ##                            geschieht.
    ##   front_1916_zaehlung      Die Liste ist der tragende Moment der
    ##                            Etappe: Was aufgeschrieben wird, gilt.
    ##   front_urlaub             Der Urlaub ist der einzige Ort, an dem
    ##                            Front und Heimat aufeinandertreffen.
    ##
    ## Nebenwirkung, die beabsichtigt ist: Der kurze Verlauf bekommt vier
    ## Ereignisse mehr Bestand. Die Zeile 1914/Heimat stand vorher auf
    ## 'knapp'.
    TRAEGER_KERN_NACHTRAG = [
        "heimat_1914_liebesgaben",
        "heimat_lazarettzug",
        "front_1916_zaehlung",
        "front_urlaub",
    ]

    def traeger_kern_nachtragen():
        for kennung in TRAEGER_KERN_NACHTRAG:
            vorlage = EREIGNIS_INDEX.get(kennung)
            if vorlage is None:
                continue
            vorlage.kern = True

    traeger_kern_nachtragen()

    def traeger_ohne_kern():
        """Träger, die im kurzen Verlauf nicht gezogen werden können.

        Liefert (jahr, pfad, kennung, grund). Grund ist entweder 'fehlt'
        (die Kennung gibt es nicht) oder 'kern' (es gibt sie, aber sie
        ist im kurzen Verlauf nicht ziehbar).
        """
        funde = []
        for jahr in KAPITEL_JAHRE:
            for pfad in PFAD_REIHENFOLGE:
                for kennung in kapitel_bogen(jahr, pfad).get("träger", []):
                    vorlage = EREIGNIS_INDEX.get(kennung)
                    if vorlage is None:
                        funde.append((jahr, pfad, kennung, "fehlt"))
                    elif not vorlage.kern:
                        funde.append((jahr, pfad, kennung, "kern"))
        return funde

    def traeger_fehlend():
        """Felder von KAPITEL_BOGEN ohne einen einzigen Träger.

        SEIT PAKET 5, SCHRITT 3, PUNKT 13a. traeger_ohne_kern() prüft, ob
        ein eingetragener Träger taugt. Es konnte nie melden, dass gar
        keiner eingetragen ist - und genau das war für 1917 bis 1919 auf
        allen drei Pfaden der Fall. BOGEN_ZUSCHLAG griff dort nirgends,
        neun Felder lang, und keine Zahl im Bericht zeigte es. Ein Feld
        ohne Träger ist kein leeres Feld, sondern ein Jahr ohne tragenden
        Moment.

        Liefert (jahr, pfad). Ein Jahr, das auf diesem Pfad gar keinen
        Bestand hat, wird trotzdem gemeldet: Dann fehlt eben beides.
        """
        funde = []
        for jahr in KAPITEL_JAHRE:
            for pfad in PFAD_REIHENFOLGE:
                if not kapitel_bogen(jahr, pfad).get("träger", []):
                    funde.append((jahr, pfad))
        return funde

    ## ------------------------------------------------------------------ B
    ## Dominierte Optionen
    ##
    ## Eine Option ist dominiert, wenn eine andere Option derselben Karte
    ## in allen vier Werten mindestens gleich gut ist und in einem besser -
    ## und wenn die schlechtere dafür nichts anderes bietet. Wer so eine
    ## Karte zieht, entscheidet nicht; er liest ab.
    ##
    ## Die Einbahnstraßenprüfung findet das nicht: Sie sucht Karten, bei
    ## denen ALLE Optionen denselben Wert verschlechtern. Hier ist genau
    ## eine Option zu gut, nicht jede zu schlecht.
    ##
    ## Drei Fälle, alle über Zahlen geheilt und keinen Satz geändert. Die
    ## Begründung steht jeweils im vorhandenen Ausgangstext:
    ##
    ##   front_trommelfeuer / "Einen Brief schreiben"
    ##     Der Text sagt: "Du lügst über drei Seiten." Ein Trostbrief nach
    ##     Hause beruhigt beim Schreiben (belastung -1), aber er schafft
    ##     keinen Rückhalt - er sorgt dafür, dass zu Hause niemand weiß,
    ##     was du trägst. rueckhalt +1 wird deshalb zu rueckhalt -1. Der
    ##     Handel heißt jetzt: Ruhe gegen Abstand.
    ##
    ##   front_urlaub / beide Optionen
    ##     "Mitspielen" war in beiden Werten besser. Der Text des
    ##     Mitspielens nennt selbst den Preis: "In der Nacht vor der
    ##     Abfahrt sitzt du in der Küche und wartest, dass es hell wird."
    ##     Vierzehn Tage den Helden spielen kostet Schlaf. Also
    ##     belastung -1 zu +1. Wer stattdessen erzählt, wie es ist, hat es
    ##     wenigstens gesagt und muss es nicht weiter tragen: belastung
    ##     +1 zu -1. Der Handel heißt jetzt: Rückhalt gegen Ruhe.
    ##
    ##   einstieg_etappe / "Sich melden"
    ##     Der Text sagt: "Die Verpflegung ist besser als daheim." Genau
    ##     das stand in keiner Zahl. versorgung +1 kommt dazu, damit die
    ##     Meldung etwas kostet UND etwas bringt. Die Karte fällt erst,
    ##     wenn Paket 5 die Etappe wieder öffnet; falsch war sie schon
    ##     vorher.
    ##
    ## NICHT beanstandet und deshalb unverändert:
    ##   front_gas und front_stosstrupp. Ihre bessere Option trägt eine
    ##   Variante, die zu ende_gefallen springt. Dieses Risiko steht in
    ##   keiner der vier Zahlen, ist aber der eigentliche Preis.
    ##   einstieg_meldung. Die schlechtere Option vergibt das Merkmal
    ##   'einberufen'. Auf den Befehl zu warten ist Normalverhalten und
    ##   darf nie bestraft werden (harte Regel 4).
    ##
    ## ACHTUNG: DER OPTIONSTITEL IST HIER EIN BEZEICHNER, KEIN TEXT.
    ##
    ## Diese Tabelle und die beiden Kettennachträge weiter unten finden
    ## ihre Option über den TITEL. Wer einen Titel umschreibt - und in
    ## einem Textpaket schreibt man Titel um -, schaltet den Nachtrag
    ## still ab. Das Ereignis fällt dann auf die Werte zurück, die in
    ## script.rpy stehen, und niemand merkt es.
    ##
    ## GENAU DAS IST IN PAKET 6, SCHRITT 1 PASSIERT. Aus "Mitspielen"
    ## wurde "Ihnen recht geben", und damit war front_urlaub wieder die
    ## dominierte Karte, die Paket 4 hier repariert hatte. Aus
    ## "Hinübergehen" wurde "Über die Brustwehr steigen", und damit war
    ## die Verbrüderungskette abgeschaltet. Gemessen hat es Probe 4: Der
    ## kurze Etappenverlauf sprang von 53,8 auf 61,0 Prozent.
    ##
    ## Deshalb sammelt NACHTRAG_OHNE_TREFFER ab jetzt jeden Schlüssel, der
    ## auf keine Option passt, und Probe 1 meldet ihn. Ein Nachtrag, der
    ## ins Leere greift, ist damit keine stille Änderung mehr.
    NACHTRAG_OHNE_TREFFER = []

    ## Eintrag: Kennung -> {Optionstitel -> neue aenderungen}
    DOMINANZ_NACHTRAG = {
        "front_trommelfeuer": {
            "Einen Brief schreiben": {"belastung": -1, "rueckhalt": -1},
        },
        "front_urlaub": {
            "Erzählen, wie es ist": {"belastung": -1, "rueckhalt": -1},
            ## Hieß bis Paket 6, Schritt 1 "Mitspielen".
            "Ihnen recht geben": {"belastung": 1, "rueckhalt": 1},
        },
        "einstieg_etappe": {
            "Sich melden": {"versorgung": 1, "belastung": 1, "rueckhalt": -1},
        },
    }

    def dominanz_nachtragen():
        for kennung, angaben in DOMINANZ_NACHTRAG.items():
            vorlage = EREIGNIS_INDEX.get(kennung)
            if vorlage is None:
                NACHTRAG_OHNE_TREFFER.append(("Dominanz", kennung, "-",
                                              "Ereignis gibt es nicht"))
                continue
            getroffen = []
            for auswahl in vorlage.optionen:
                titel = auswahl.titel
                if not isinstance(titel, str):
                    continue
                if titel in angaben:
                    auswahl.aenderungen = dict(angaben[titel])
                    getroffen.append(titel)
            for titel in angaben:
                if titel not in getroffen:
                    NACHTRAG_OHNE_TREFFER.append(
                        ("Dominanz", kennung, titel,
                         "kein Optionstitel passt - der Nachtrag greift nicht"))

    dominanz_nachtragen()

    ## ------------------------------------------------------------------ B2
    ## Welche Karte welches Papier ist
    ##
    ## PAKET 8, SCHRITT 1. Der Kartentyp könnte auch am Ereignis selbst
    ## stehen, und dort stünde er schöner. Er steht trotzdem hier, und zwar
    ## aus einem handfesten Grund: Die Ereignisse werden im ganzen Projekt
    ## POSITIONAL angelegt — Ereignis("kennung", [jahre], "pfad", ...). Wer
    ## fünfundzwanzig solcher Aufrufe über drei Dateien aufschneidet, um ein
    ## Schlüsselwort ans Ende zu setzen, greift fünfundzwanzigmal in fremden
    ## Text. Das ist die Art von Arbeit, bei der man beim zwanzigsten Mal
    ## eine Klammer verliert.
    ##
    ## Anders als bei DOMINANZ_NACHTRAG ist der Schlüssel hier die KENNUNG
    ## und nicht der Optionstitel. Die Falle aus Entscheidung 16 gibt es
    ## also nicht: Eine Kennung ist eindeutig und wird nicht umformuliert,
    ## wenn jemand einen Text überarbeitet.
    ##
    ## AUFGENOMMEN IST NUR, WAS DAS DOKUMENT WIRKLICH ZEIGT. Nicht, wo eines
    ## bloß erwähnt wird: "Der Befehl heißt eingraben" ist kein Blatt
    ## Papier, und eine Erkennungsmarke ist keine Lebensmittelmarke. Von
    ## hundert Ereignissen sind es fünfundzwanzig; die anderen bleiben der
    ## Bogen, der sie immer waren.
    KARTENTYP_VERGABE = {

        ## Vordrucke, Bescheide, Verfügungen und amtliche Aushänge.
        "front_1916_zaehlung": "amtlich",          ## Erlass und Formular
        "front_1917_gerichtsherr": "amtlich",      ## die wieder geöffnete Akte
        "front_1918_befehl": "amtlich",            ## der Befehl im Umschlag
        "einstieg_etappe": "amtlich",              ## Aufruf am schwarzen Brett
        "heimat_kriegsanleihe": "amtlich",         ## der Zeichnungsschein
        "heimat_todesnachricht": "amtlich",        ## die Formel, eingetragen
        "heimat_unterstuetzung": "amtlich",        ## die Einstufung am Schalter
        "heimat_verfahren": "amtlich",             ## die Vorladung
        "heimat_1916_ernaehrungsamt": "amtlich",   ## "Haushaltsvorstand"
        "heimat_1917_hilfsdienst": "amtlich",      ## Vordruck und Abkehrschein
        "heimat_1917_schulspeisung": "amtlich",    ## das Blatt am Schultor
        "heimat_1918_bekanntmachung": "amtlich",   ## zwei Anschläge übereinander
        "heimat_1918_grippewelle": "amtlich",      ## der Anschlag an der Säule
        "etappe_1916_verschleppt": "amtlich",      ## Verordnung und Liste
        "etappe_requisition": "amtlich",           ## Bogen und Schein
        "epilog_1919_versorgungsamt": "amtlich",   ## der Bogen zur Rente
        "epilog_1919_papiere": "amtlich",          ## das fehlende Blatt

        ## Briefe, die über die Feldpost gelaufen sind.
        "front_feldpost": "feldpost",
        "heimat_1916_zensur": "feldpost",          ## dreimal geschwärzt
        "etappe_brief_von_daheim": "feldpost",
        "etappe_zensurstelle": "feldpost",         ## dreißig Stück auf dem Tisch

        ## Karten mit abtrennbaren Abschnitten.
        "heimat_1915_brotkarte": "lebensmittel",
        "heimat_1918_grippe": "lebensmittel",      ## der Tag des Abstempelns

        ## Gedrucktes, in Spalten.
        "heimat_1917_unterseeboot": "zeitung",     ## laut vorgelesen
        "epilog_1919_vertrag": "zeitung",          ## "stehen in Spalten"
    }

    def kartentypen_vergeben():
        for kennung, typ in KARTENTYP_VERGABE.items():
            vorlage = EREIGNIS_INDEX.get(kennung)
            if vorlage is None:
                NACHTRAG_OHNE_TREFFER.append(("Kartentyp", kennung, typ,
                                              "Ereignis gibt es nicht"))
                continue
            if typ not in KARTENTYPEN:
                NACHTRAG_OHNE_TREFFER.append(("Kartentyp", kennung, typ,
                                              "diesen Kartentyp gibt es nicht"))
                continue
            vorlage.kartentyp = typ

    ## AUFGERUFEN WIRD SIE NICHT HIER, sondern in einem init-4-Block am Ende
    ## der Datei. Der Grund ist gemessen und war eine Falle: Fünfzehn der
    ## fünfundzwanzig Ereignisse entstehen WEITER UNTEN in dieser Datei, im
    ## selben init-Rang — und bei gleichem Rang entscheidet die Stelle in der
    ## Datei. An dieser Stelle aufgerufen, fand die Vergabe nur die zehn aus
    ## script.rpy und herkunft.rpy; die anderen fünfzehn gab es noch nicht.
    ## Sie sind nicht stillschweigend verschwunden — NACHTRAG_OHNE_TREFFER
    ## hat jeden einzelnen gemeldet, und genau dafür ist die Liste da.

    ## ------------------------------------------------------------------ C
    ## Ein Plan statt zweier
    ##
    ## NACHHALL_PLAN (Abschnitt 5) und KETTEN_PLAN (Abschnitt 5) nennen
    ## dieselben künftigen Ereignisse aus zwei Blickwinkeln: der eine
    ## fragt, welches frühe Merkmal wiederkehren soll, der andere, welche
    ## Entscheidung eine Antwort bekommt. Drei Kennungen stehen in beiden
    ## Listen. Ohne Zusammenführung wird eines davon zweimal geplant und
    ## einmal zu viel gebaut.
    ##
    ## ES FÜHRT DER NACHHALL_PLAN. Er ist älter, Probe 1 prüft gegen ihn,
    ## und er nennt die Bedingung (braucht_eines), die im Ereignis stehen
    ## muss. Der KETTEN_PLAN trägt für dieselben Kennungen nur nach, aus
    ## welcher Entscheidung sie hervorgehen und wie viele Jahre später.
    ## Beide Listen bleiben stehen, weil jede etwas sagt, was die andere
    ## nicht sagt; zusammengesetzt werden sie hier.
    def inhaltsplan():
        """Die zusammengeführte Planliste. Jede Kennung genau einmal."""
        zeilen = []
        stelle = {}

        for merkmal, jahr, pfad, kennung, titel in NACHHALL_PLAN:
            eintrag = {
                "kennung": kennung,
                "jahr": jahr,
                "pfad": pfad,
                "merkmal": merkmal,
                "titel": titel,
                "kette_von": None,
                "abstand": None,
                "herkunft": "Nachhall",
                "vorhanden": kennung in EREIGNIS_INDEX,
            }
            stelle[kennung] = eintrag
            zeilen.append(eintrag)

        for eins, zwei, pfad, abstand, frage, antwort in KETTEN_PLAN:
            if zwei in stelle:
                eintrag = stelle[zwei]
                eintrag["kette_von"] = eins
                eintrag["abstand"] = abstand
                eintrag["herkunft"] = "beide"
                continue
            eintrag = {
                "kennung": zwei,
                "jahr": None,
                "pfad": pfad,
                "merkmal": None,
                "titel": antwort,
                "kette_von": eins,
                "abstand": abstand,
                "herkunft": "Kette",
                "vorhanden": zwei in EREIGNIS_INDEX,
            }
            stelle[zwei] = eintrag
            zeilen.append(eintrag)

        return zeilen

    def inhaltsplan_doppelte():
        """Kennungen, die in beiden Plänen stehen."""
        return [z["kennung"] for z in inhaltsplan() if z["herkunft"] == "beide"]

    ## ------------------------------------------------------------------ D
    ## Kettenglieder brauchen ein späteres Jahr
    ##
    ## REGEL FÜR JEDE KETTE: Das zweite Glied muss mindestens ein Jahr
    ## abdecken, das NACH dem spätesten Jahr des ersten Glieds liegt.
    ## Sonst ist die Kette in einem Teil der Durchgänge von vornherein
    ## unauflösbar - wer die erste Karte im letzten gemeinsamen Jahr
    ## zieht, bekommt nie eine Antwort.
    ##
    ## front_nachfrage und heimat_verfahren trugen beide jahre=[1915,
    ## 1916] bei kette_ab=1. Wer die erste Karte 1916 zog, wartete
    ## vergebens. Seit der Reparatur an kette_faellig() in Paket 3 ist das
    ## messbar: 977 offene Vormerkungen in 16000 Durchgängen.
    ##
    ## Beide bekommen 1917 und 1918 dazu. Weil sich ein Ereignis nicht
    ## über vier Jahre gleich erzählen lässt, bekommt jedes zwei neue
    ## Jahresfassungen: 1917 ist die Militärjustiz eingespielt, 1918
    ## arbeitet sie im Stapel. Die Fassungen unterscheiden sich in der
    ## Sache, nicht in einem Wort.
    ##
    ## front_kamerad, das erste Glied der Frontkette, bekommt in Schritt 1
    ## dieses Pakets 1917 dazu - aber NICHT 1918, damit die Regel oben
    ## eingehalten bleibt.
    KETTENGLIED_NACHTRAG = {

        "front_nachfrage": {
            "jahre": [1915, 1916, 1917, 1918],
            "text": {
                1917: "Der Unterstand riecht nach nassem Papier. Ein Offizier "
                      "des Gerichtsherrn klappt eine Mappe auf. Die Liste von "
                      "damals liegt obenauf, daneben ein leeres Blatt. Er fragt "
                      "nach der Nacht, in der dein Kamerad verschwunden ist.",
                1918: "Zwei Männer vom Kriegsgericht stehen im Graben. Ihre "
                      "Mäntel sind sauber, ihre Stiefel auch. Seit dem Frühjahr "
                      "wird jede Fahnenflucht geprüft, also jedes Weglaufen von "
                      "der Truppe. Sie fragen nach der Nacht, in der dein "
                      "Kamerad verschwunden ist.",
            },
        },

        ## heimat_verfahren bekommt zusätzlich 1919, und zwar aus einem
        ## Grund, den der Auftrag nicht kennen konnte: Nicht nur
        ## heimat_hamsterfahrt merkt dieses Glied vor, sondern auch die
        ## EINLAGE hamsterfahrt (minispiele.rpy, Abschnitt 5). Sie läuft
        ## bis 1918 und merkt für dasselbe Jahr vor. Wird sie im letzten
        ## Kapitel des Jahres gespielt, bleibt keine Ziehung mehr übrig,
        ## und die Vormerkung fällt ins Jahr 1919. Nach der Regel oben
        ## braucht das zweite Glied deshalb 1919 mit.
        ##
        ## Für die Bestandstafel ändert das nichts: heimat_verfahren
        ## trägt nur_kette=True und wird nie frei gezogen. Es füllt das
        ## Jahr 1919 also nicht, es beantwortet nur eine Frage, die sonst
        ## offen bliebe.
        "heimat_verfahren": {
            "jahre": [1915, 1916, 1917, 1918, 1919],
            "text": {
                1917: "Der Flur des Amtsgerichts ist kalt und voll. Vor dir "
                      "sitzen sieben Frauen mit derselben Vorladung. Der "
                      "Beamte hat heute wenig Zeit. Er bietet an, das "
                      "Verfahren einzustellen. Dafür sollst du bei anderen "
                      "Angaben helfen.",
                1918: "Die Vorladung liegt seit acht Wochen auf dem Tisch und "
                      "ist an den Rändern weich geworden. Das Amtsgericht "
                      "arbeitet die Höchstpreisverfahren nur noch stapelweise "
                      "ab. Der Beamte blättert und findet deinen Namen erst "
                      "beim zweiten Mal. Er bietet dasselbe an wie allen: "
                      "Angaben über andere gegen die Einstellung.",
                1919: "Der Umschlag liegt zwischen zwei Rechnungen. Das "
                      "Verfahren wegen der Höchstpreise läuft weiter, obwohl "
                      "der Krieg vorbei ist. Im Amtszimmer riecht es nach "
                      "kaltem Ofen. Der Beamte bietet an, es einzustellen, "
                      "wenn du bei anderen Angaben hilfst.",
            },
        },
    }

    def jahresfassung_mischen(bestand, neu, grundjahr):
        """Aus einer festen Fassung wird eine nach Jahren.

        Steht im Ereignis bisher eine schlichte Zeichenkette, wird sie
        zur Fassung des Grundjahres. Steht dort schon ein Wörterbuch,
        werden die neuen Jahre nur ergänzt. So geht keine bestehende
        Fassung verloren, gleich in welcher Form sie vorlag.
        """
        if isinstance(bestand, dict):
            gemischt = dict(bestand)
        else:
            gemischt = {grundjahr: bestand}
        gemischt.update(neu)
        return gemischt

    def kettenglieder_nachtragen():
        for kennung, angaben in KETTENGLIED_NACHTRAG.items():
            vorlage = EREIGNIS_INDEX.get(kennung)
            if vorlage is None:
                continue
            grundjahr = vorlage.jahre[0] if vorlage.jahre else 1914
            if "jahre" in angaben:
                vorlage.jahre = list(angaben["jahre"])
            if "text" in angaben:
                vorlage.text = jahresfassung_mischen(
                    vorlage.text, angaben["text"], grundjahr)

    kettenglieder_nachtragen()

    def ketten_ohne_spaeteres_jahr():
        """Ketten, deren zweites Glied kein Jahr nach dem ersten hat.

        Liefert (eins, zwei, letztes Jahr des ersten Glieds, Jahre des
        zweiten). Ein Glied, das es noch nicht gibt, wird übergangen -
        es steht schon als Fehlstelle im Plan.
        """
        funde = []
        for eins, zwei, pfad, abstand, frage, antwort in KETTEN_PLAN:
            eine = EREIGNIS_INDEX.get(eins)
            zwote = EREIGNIS_INDEX.get(zwei)
            if eine is None or zwote is None:
                continue
            if not eine.jahre or not zwote.jahre:
                continue
            spaetestes = max(eine.jahre)
            if not [j for j in zwote.jahre if j > spaetestes]:
                funde.append((eins, zwei, spaetestes, list(zwote.jahre)))
        return funde


################################################################################
## 10c. Paket 4, Schritt 1: Jahresausweitung nach 1917 und 1918
################################################################################
##
## Zwölf neue Ereignisse füllen zwei leere Jahre rechnerisch nicht. Sieben
## von ihnen hängen an einem Merkmal und zählen in der Bestandstafel als
## "gebunden", nicht als "frei". Der zweite Weg ist deshalb der wichtigere:
## Vorgänge, die es 1917 und 1918 genauso gab, dürfen auch dort fallen.
##
## GEPRÜFT WURDE JEDES EINZELN, nicht pauschal. Aufgenommen ist nur, was
## sachlich in beiden Jahren stimmt; die Begründung steht jeweils daneben.
## Wer ein Jahr nachträgt, schreibt eine eigene Jahresfassung dazu - eine
## Brotschlange von 1917 ist nicht die von 1915, und ein Ereignis, das in
## fünf Jahren denselben Satz zeigt, verrät sich beim zweiten Durchgang.
##
## NICHT AUFGENOMMEN:
##   front_kamerad bekommt 1917, aber NICHT 1918. Seine Kette antwortet mit
##   front_nachfrage, und nach der Regel aus dem Vorweg braucht das zweite
##   Glied ein Jahr nach dem spätesten des ersten. front_nachfrage reicht
##   bis 1918; 1918 als erstes Glied wäre eine Frage ohne Antwort.
##
##   heimat_verfahren und front_nachfrage stehen schon im Vorweg-Block.
##
## ZUSÄTZLICH GEGENÜBER DER LISTE IM AUFTRAG: heimat_lazarettzug. Es endet
## heute bei 1916, trägt keine Jahreszahl im Namen und ist damit ein
## wiederkehrender Vorgang wie die übrigen. Lazarettzüge fuhren bis zum
## Kriegsende. Ohne dieses Ereignis erreicht die Heimat 1917 im langen
## Verlauf die Reserve nicht.
##
## Eintrag: Kennung -> {"jahre": [...], "text": {Jahr: Fassung},
##                      "ausgang": {Optionsstelle: {Jahr: Fassung}}}

init 3 python:

    JAHRESAUSWEITUNG_PAKET4 = {

        ## ---------------------------------------------------------- Front

        ## Trommelfeuer gab es 1917 in Flandern und am Chemin des Dames und
        ## 1918 vor jedem Angriff. Der Vorgang bleibt, seine Länge ändert
        ## sich: 1918 dauert das Feuer Stunden statt Tage, weil danach der
        ## Sturm kommt.
        "front_trommelfeuer": {
            "jahre": [1914, 1915, 1916, 1917, 1918],
            "text": {
                1917: "Die Erde riecht nach aufgerissenem Lehm. Ihr liegt "
                      "seit dem dritten Tag unter Feuer, und der Unterstand "
                      "ist eingedrückt. Zwischen zwei Einschlägen ruft "
                      "jemand nach seiner Mutter. Danach ist es still, und "
                      "niemand kann hinüber.",
                1918: "Der Boden schlägt dir bei jedem Einschlag gegen die "
                      "Rippen. Das Feuer liegt jetzt Stunden auf einem "
                      "Abschnitt, nicht mehr Tage. Danach kommt der Angriff, "
                      "und ihr wisst das inzwischen. Der Mann neben dir "
                      "zählt nicht mehr mit. Er sagt, es lohne die Mühe "
                      "nicht.",
            },
            "ausgang": {
                0: {
                    1917: "Nach dem dritten Tag hört es auf. Du kriechst aus "
                          "dem Loch und findest deinen Tornister nicht wieder.",
                    1918: "Nach drei Stunden hört es auf. Du liegst noch "
                          "flach, als neben dir schon jemand aufsteht.",
                },
            },
        },

        ## Feldpost lief bis zum letzten Kriegstag. Was sich ändert, ist der
        ## Inhalt: 1917 kommt kein Paket mehr, 1918 schreibt eine andere
        ## Hand, weil die erste krank ist.
        "front_feldpost": {
            "jahre": [1914, 1915, 1916, 1917, 1918],
            "text": {
                1917: "Post von zu Hause. Der Brief ist dünn und riecht nach "
                      "nichts. Sie schreiben von Kohlrüben zu jeder Mahlzeit "
                      "und fragen nach nichts mehr.",
                1918: "Post von zu Hause. Auf dem Umschlag steht eine fremde "
                      "Handschrift. Das Papier ist rau und grau, der Brief "
                      "ist kurz. Am Ende steht die Frage, ob du Brot "
                      "schicken kannst.",
            },
        },

        ## Unerlaubte Entfernung nahm 1917 zu, und die Verfolgung wurde
        ## schärfer. 1918 fehlt, siehe Kopf dieses Abschnitts.
        "front_kamerad": {
            "jahre": [1915, 1916, 1917],
            "text": {
                1917: "Ein Kamerad aus deiner Gruppe hält einen Marschbefehl "
                      "in der Hand, der nicht für ihn gilt. Das Papier ist "
                      "an den Falten schon weich. Er will damit über die "
                      "Grenze in die Schweiz. Er fragt, ob du ihn beim "
                      "Appell deckst.",
            },
        },

        ## Läuse blieben in jedem Kriegsjahr. Neu ist 1917, dass die
        ## Entlausungsanstalten den Andrang nicht mehr schaffen, und 1918,
        ## dass niemand mehr krankgeschrieben wird.
        "front_laeuse": {
            "jahre": [1915, 1916, 1917, 1918],
            "text": {
                1917: "Die Nähte sind grau von Nissen, den Eiern der Läuse. "
                      "Seit vier Wochen wart ihr nicht mehr in der "
                      "Entlausung, dem heißen Bad mit ausgekochter Kleidung. "
                      "Nachts hörst du die anderen kratzen, und du kratzt "
                      "mit. Auf den Unterarmen sind die Stellen offen.",
                1918: "Die Läuse sitzen jetzt auch in den Augenbrauen. Ein "
                      "Sanitäter sagt, das Fieber komme davon, und schreibt "
                      "trotzdem niemanden krank. Im Unterstand riecht es "
                      "nach Karbol, einem scharfen Mittel gegen Ungeziefer. "
                      "Du ziehst das Hemd über den Kopf und suchst zum "
                      "dritten Mal heute.",
            },
        },

        ## Beute vom Gefallenen der Gegenseite: 1917 ein weggeworfener
        ## Tornister, 1918 der eroberte Graben mit englischen Vorräten. Der
        ## Tote bleibt in beiden Fassungen im Bild, weil die zweite Option
        ## ihn zuschüttet.
        "front_beute": {
            "jahre": [1915, 1916, 1917, 1918],
            "text": {
                1917: "Im Trichter liegt ein Tornister, den jemand "
                      "abgeworfen hat. Darin sind Zwieback, eine Blechdose "
                      "und ein Paar trockene Socken. Der Regen hat alles "
                      "durchweicht, den Zwieback nicht. Zwei Schritte weiter "
                      "liegt der, dem es gehört hat.",
                1918: "In dem eroberten Graben liegt ein Gefallener der "
                      "Gegenseite. Neben ihm steht sein Tornister offen, und "
                      "es riecht nach Rindfleisch aus der Büchse. Dazu ein "
                      "Beutel mit weißem Mehl und ein Paar feste Stiefel. So "
                      "viel habt ihr seit zwei Jahren nicht gesehen.",
            },
        },

        ## Ruhequartiere blieben, wurden aber kürzer und ärmer. 1918 ist
        ## die Gruppe zur Hälfte ausgetauscht - das ist der Unterschied,
        ## den die Fassung zeigt.
        "front_ruhequartier": {
            "jahre": [1915, 1916, 1917, 1918],
            "text": {
                1917: "Ablösung, aber nur für vier Tage. Das Dorf ist voll, "
                      "ihr liegt in einer Scheune ohne Stroh. Es gibt heißes "
                      "Wasser in der Badeanstalt und eine Kantine ohne "
                      "Fleisch. Der Feldwebel hat für morgen einen Appell "
                      "angesetzt.",
                1918: "Ablösung im Herbst, drei Tage in einem Dorf hinter "
                      "der Front. Die Feldküche steht auf dem Kirchplatz und "
                      "hat nur Rübensuppe. Im Quartier riecht es nach nassem "
                      "Stroh und nach Karbol. Von zwanzig aus deiner Gruppe "
                      "sind sieben noch dieselben wie im Frühjahr.",
            },
        },

        ## Heimaturlaub gab es 1917 noch regelmäßig, 1918 gekürzt und oft
        ## verschoben. Die Frage der Karte bleibt dieselbe: Was erzählst du
        ## zu Hause?
        "front_urlaub": {
            "jahre": [1915, 1916, 1917, 1918],
            "text": {
                1917: "Heimaturlaub, vierzehn Tage. Auf dem Bahnsteig "
                      "kontrolliert ein Posten deinen Urlaubsschein. Zu "
                      "Hause ist die Küche kalt, und auf dem Tisch stehen "
                      "Kohlrüben. Sie fragen nach der Front und hören nach "
                      "zwei Sätzen weg.",
                1918: "Urlaub gibt es selten, und deiner ist von zehn Tagen "
                      "auf sechs gekürzt. Der Zug steht viermal auf freier "
                      "Strecke, und im Abteil bleibt es kalt. Zu Hause reden "
                      "sie nicht mehr über den Sieg, sondern über die "
                      "Grippe. Jemand fragt dich, ob es bald vorbei ist.",
            },
        },

        ## --------------------------------------------------------- Heimat

        ## Die Brotschlange ist der Ort, an dem der Mangel jedes Jahr eine
        ## andere Gestalt hat: 1917 der Frost und das Streckmehl, 1918 die
        ## kurze Schlange, weil die halbe Straße krank liegt.
        "heimat_brotschlange": {
            "jahre": [1914, 1915, 1916, 1917, 1918],
            "text": {
                1917: "Seit zwei Uhr stehst du an, und der Frost geht durch "
                      "die Sohlen. Die Karte gilt für den halben Laib, den "
                      "es vielleicht gibt. Vorn sagt eine Frau, das Brot sei "
                      "aus Rüben und Streckmehl. Hinter dir zählt jemand "
                      "halblaut die Leute vor sich.",
                1918: "Die Schlange steht heute nur bis zur Ecke, weil viele "
                      "krank im Bett liegen. Auf dem Anschlag steht eine "
                      "neue, kleinere Menge je Kopf. Der Bäcker hat gestern "
                      "nicht geöffnet und sagt heute nichts dazu. Es riecht "
                      "nicht nach Brot. Aus dem Hinterhof winkt jemand, den "
                      "du kennst.",
            },
            "ausgang": {
                0: {
                    1918: "Diesmal fragt niemand nach. Der Preis ist so hoch, "
                          "dass du zweimal nachrechnest und trotzdem zahlst.",
                },
            },
        },

        ## Neun Kriegsanleihen bis September 1918. Die siebte fiel in den
        ## Herbst 1917, die neunte in den Herbst 1918. Was sich ändert, ist
        ## nicht die Werbung, sondern wer noch zeichnet.
        "heimat_kriegsanleihe": {
            "jahre": [1914, 1915, 1916, 1917, 1918],
            "text": {
                1917: "Die siebte Kriegsanleihe. Im Hausflur hängt die "
                      "Liste, und daneben steht, wie viel die Straße "
                      "gezeichnet hat. Ein Herr von der Sparkasse klingelt "
                      "an jeder Tür. Er hat kalte Hände und einen Bleistift "
                      "hinter dem Ohr.",
                1918: "Die neunte Kriegsanleihe, und diesmal kommt niemand "
                      "mehr an die Tür. Im Flur ist es so kalt, dass du "
                      "deinen Atem siehst. Im Schaufenster der Sparkasse "
                      "hängt ein Plakat mit einem Soldaten. Die Nachbarin "
                      "sagt, sie habe achtzehnhundert Mark gezeichnet. Auf "
                      "der Liste im Flur stehen weniger Namen als im "
                      "Vorjahr.",
            },
        },

        ## Der freie Sonntag bleibt der einzige Ort, an dem sich Kraft
        ## zurückholen lässt. 1918 steht er unter dem Husten im Haus.
        "heimat_sonntag": {
            "jahre": [1914, 1915, 1916, 1917, 1918],
            "text": {
                1917: "Ein Sonntag ohne Ausgabe. Im Hof scheint die Sonne "
                      "auf die Teppichstangen, und es ist still. Die "
                      "Nachbarin hat Lindenblütentee und einen Rest Zucker. "
                      "Sie fragt, ob du am Nachmittag herüberkommst.",
                1918: "Ein Sonntag im Herbst, und im Treppenhaus hustet "
                      "jemand hinter jeder zweiten Tür. Draußen ist es warm "
                      "für die Jahreszeit. Die Kirche hat den Gottesdienst "
                      "abgesagt, weil zu viele krank sind. Vor deiner Tür "
                      "liegt ein Zettel von der Nachbarin.",
            },
        },

        ## Todesnachrichten kamen bis zuletzt, 1918 oft mit Wochen
        ## Verspätung und gleich mit dem Formular der Versorgungsbehörde
        ## dahinter.
        "heimat_todesnachricht": {
            "jahre": [1914, 1915, 1916, 1917, 1918],
            "text": {
                1917: "Ein Brief mit schwarzem Rand, und diesmal kennst du "
                      "die Handschrift nicht. Gefallen bei einem Angriff, "
                      "steht darin, mehr nicht. Das Papier ist dünn und an "
                      "einer Stelle durchgedrückt. In eurer Straße hängt der "
                      "dritte schwarze Streifen in diesem Monat.",
                1918: "Der Brief mit dem schwarzen Rand kommt sechs Wochen "
                      "zu spät. Die Kanten sind abgegriffen, als hätte ihn "
                      "schon jemand gelesen. Gefallen im Juli, steht darin, "
                      "bei einem Rückzug. Auf dem Tisch liegt ein zweiter "
                      "Umschlag von der Behörde. Er fragt nach der Anschrift "
                      "für die Rente der Hinterbliebenen, also der "
                      "Angehörigen.",
            },
        },

        ## Anzeigen wegen Hortens und Kettenhandels nahmen zu, je knapper
        ## es wurde. 1918 genügt schon, dass jemand neu im Haus ist.
        "heimat_denunziation": {
            "jahre": [1915, 1916, 1917, 1918],
            "text": {
                1917: "Im Hinterhaus soll jemand Kartoffeln unter dem Bett "
                      "haben. Die Frau von oben war schon auf der Wache und "
                      "nennt jetzt Namen. Im Treppenhaus riecht es nach "
                      "gekochten Rüben aus drei Wohnungen. Man fragt dich, "
                      "ob du bestätigst, was alle gesehen haben wollen.",
                1918: "Im Hinterhaus ist jemand eingezogen, den niemand "
                      "kennt. Es heißt, dort werde mit Brotkarten gehandelt. "
                      "Im Zimmer der Wache riecht es nach Bohnerwachs und "
                      "nassen Mänteln. Auf dem Tisch liegt eine Anzeige, und "
                      "es fehlt nur eine zweite Stimme. Der Beamte sieht "
                      "dich an und wartet, bis du etwas sagst.",
            },
        },

        ## Hamsterfahrten wurden mit jedem Jahr riskanter und teurer. 1918
        ## nehmen die Höfe kein Geld mehr, sondern nur noch Ware.
        "heimat_hamsterfahrt": {
            "jahre": [1915, 1916, 1917, 1918],
            "text": {
                1917: "Auf dem Bahnsteig ist es kalt, und der Zug um halb "
                      "fünf ist schon voll. Auf dem Land geben die Höfe nur "
                      "noch gegen Ware ab, nicht gegen Geld. In deinem "
                      "Schrank hängt ein Mantel, den du nicht brauchst. An "
                      "der Sperre stehen heute zwei Gendarmen statt einem.",
                1918: "Die Bauern kennen die Gesichter aus der Stadt "
                      "inzwischen. Für einen Sack Kartoffeln willst du "
                      "Bettwäsche und zwei Löffel aus Silber geben. Im Zug "
                      "sitzen mehr Kinder als Erwachsene, weil Kinder "
                      "weniger kontrolliert werden. Deine Beine schlafen "
                      "ein, so eng steht ihr.",
            },
        },

        ## Lazarettzüge fuhren bis zum Kriegsende. 1918 halten sie
        ## außerhalb, weil die Grippe im Zug ist. Nicht in der Liste des
        ## Auftrags, siehe Kopf dieses Abschnitts.
        "heimat_lazarettzug": {
            "jahre": [1915, 1916, 1917, 1918],
            "text": {
                1917: "Am Güterbahnhof steht seit dem Morgen ein "
                      "Lazarettzug. Es riecht nach Karbol und nach nassem "
                      "Verbandstoff. Eine Schwester ruft nach Leuten, die "
                      "Kaffee ausschenken. In den letzten Waggons liegen "
                      "die, die nicht weitertransportiert werden.",
                1918: "Der Zug hält heute außerhalb, hinter dem Stellwerk. "
                      "Man sagt, es sei wegen der Grippe, und niemand soll "
                      "näher heran. Trotzdem stehen zwanzig Leute am Zaun "
                      "und rufen Namen. Ein Sanitäter winkt ab und zieht "
                      "sich ein Tuch vors Gesicht.",
            },
        },

        ## Die Rüstungsschicht bleibt, die Stückzahl steigt. 1918 fehlt
        ## jede zehnte Kraft, und die Arbeit wird trotzdem verteilt.
        "heimat_fabrik": {
            "jahre": [1915, 1916, 1917, 1918],
            "text": {
                1917: "Die Schicht beginnt um sechs, und die Halle ist nicht "
                      "geheizt. An deinen Händen ist die Haut gelb von der "
                      "Füllmasse. Der Vorarbeiter hat die Stückzahl wieder "
                      "heraufgesetzt. An der Wand hängt eine Liste mit den "
                      "Namen derer, die sie nicht schaffen.",
                1918: "In der Halle fehlen heute vierzehn Leute, die meisten "
                      "wegen der Grippe. Die Schicht läuft trotzdem mit "
                      "derselben Stückzahl. Der Vorarbeiter teilt die Arbeit "
                      "der Fehlenden auf die Übrigen auf. Deine Finger sind "
                      "steif, bevor die Hälfte um ist.",
            },
        },
    }

    def jahresausweitung_nachtragen(tabelle):
        """Trägt Jahre und Jahresfassungen an bestehenden Ereignissen nach.

        Verändert keinen bestehenden Satz. Wo bisher eine feste Fassung
        stand, wird sie zur Fassung des ersten Jahres; die neuen Jahre
        kommen daneben. jahrestext() nimmt danach zu jedem Jahr die
        jüngste Fassung, die nicht später liegt.
        """
        for kennung, angaben in tabelle.items():
            vorlage = EREIGNIS_INDEX.get(kennung)
            if vorlage is None:
                continue
            grundjahr = vorlage.jahre[0] if vorlage.jahre else 1914
            if "jahre" in angaben:
                vorlage.jahre = list(angaben["jahre"])
            if "text" in angaben:
                vorlage.text = jahresfassung_mischen(
                    vorlage.text, angaben["text"], grundjahr)
            for stelle, fassungen in angaben.get("ausgang", {}).items():
                if stelle >= len(vorlage.optionen):
                    continue
                auswahl = vorlage.optionen[stelle]
                auswahl.ausgang = jahresfassung_mischen(
                    auswahl.ausgang, fassungen, grundjahr)

    jahresausweitung_nachtragen(JAHRESAUSWEITUNG_PAKET4)

    ## Ketten, die dieses Paket schließt #######################################
    ##
    ## Der KETTEN_PLAN nennt sie seit Paket 3; die Antwortkarten entstehen
    ## erst jetzt. Erst mit dem Nachtrag hier wird aus dem Plan eine Kette:
    ## Die Option des ersten Glieds merkt das zweite vor.
    ##
    ## Eintrag: Kennung -> {Optionstitel: (zweites Glied, Abstand in Jahren)}
    ##
    ## AUCH HIER IST DER OPTIONSTITEL EIN BEZEICHNER. Siehe die Warnung
    ## über DOMINANZ_NACHTRAG: Wer ihn umschreibt, schaltet die Kette ab,
    ## ohne dass eine Zahl es meldet. Seit Paket 6, Schritt 1 sammelt
    ## NACHTRAG_OHNE_TREFFER die Schlüssel, die ins Leere greifen.
    KETTEN_NACHTRAG_PAKET4 = {
        "front_1914_weihnachten": {
            ## Hieß bis Paket 6, Schritt 1 "Hinübergehen".
            "Über die Brustwehr steigen": ("front_1917_verbruederung_nachhall", 3),
        },
        "heimat_1916_arbeitsniederlegung": {
            "Vorangehen": ("heimat_1917_aprilstreik", 1),
        },
    }

    def ketten_nachtragen(tabelle):
        for kennung, angaben in tabelle.items():
            vorlage = EREIGNIS_INDEX.get(kennung)
            if vorlage is None:
                NACHTRAG_OHNE_TREFFER.append(("Kette", kennung, "-",
                                              "Ereignis gibt es nicht"))
                continue
            getroffen = []
            for auswahl in vorlage.optionen:
                titel = auswahl.titel
                if not isinstance(titel, str) or titel not in angaben:
                    continue
                ziel, abstand = angaben[titel]
                if ziel not in EREIGNIS_INDEX:
                    NACHTRAG_OHNE_TREFFER.append(
                        ("Kette", kennung, titel,
                         "zweites Glied " + ziel + " gibt es nicht"))
                    continue
                auswahl.kette = ziel
                auswahl.kette_ab = abstand
                getroffen.append(titel)
            for titel in angaben:
                if titel not in getroffen:
                    NACHTRAG_OHNE_TREFFER.append(
                        ("Kette", kennung, titel,
                         "kein Optionstitel passt - die Kette wird nicht gesetzt"))


################################################################################
## 10d. Paket 4, Schritt 1: die Ereignisse von 1917
################################################################################
##
## Das Jahr des Mangels. Der Bezugspunkt ist der Winter 1916/17: Die
## Kartoffelernte war ausgefallen, Kohlrüben ersetzten sie, Brot wurde
## gestreckt. Der Name dieses Winters fällt in keinem Spieltext - gezeigt
## wird, was im Kochgeschirr liegt und wie lange man dafür ansteht.
##
## DREI BLICKWINKEL, wie es der Auftrag verlangt:
##   Front        Verpflegung, Winterstellung, Ersatztransport, ein Gerücht
##                aus dem Osten
##   Fabrik/Hof   Akkord, Ablieferung, Aprilstreik
##   Amt/Bürger   Hilfsdienstgesetz, Schulspeisung, Kriegsanleihe,
##                Zeitungsmeldung zum U-Boot-Krieg
## Kein allwissender Überblick. Was die Figur 1917 nicht wissen kann, steht
## nirgends: kein Wort über den Ausgang des Krieges, keines über den
## Oktober in Russland, keines über die Wirkung des U-Boot-Kriegs.
##
## SIEBEN DAVON SIND RÜCKBEZÜGE aus NACHHALL_PLAN. Sie tragen
## braucht_eines und zählen in der Bestandstafel als gebunden. Ihr erster
## Satz rührt an die alte Entscheidung, ohne sie zu erklären.
##
## Der freie Bestand des Jahres kommt zum größeren Teil aus der
## Jahresausweitung in Abschnitt 10c. Wer hier Ereignisse hinzufügt oder
## Bedingungen verschärft, sieht danach in die Bestandstafel.

init 3 python:

    EREIGNISSE_1917 = [

        ## ------------------------------------------------------ Rückbezüge

        Ereignis(
            "front_1917_verbruederung_nachhall", [1917], "front",
            "Im Nieselregen lässt der neue Leutnant antreten und liest einen "
            "alten Befehl vor. Jede Verständigung mit dem Gegner sei "
            "Landesverrat, sagt er, also Verrat am eigenen Land. Der Befehl "
            "ist von Weihnachten 1914 und wird heute noch einmal verlesen. "
            "Neben dir steht einer, der damals dabei war. Er sieht geradeaus "
            "und sagt nichts.",
            [
                Option(
                    "Nachts hinüberrufen",
                    "Beim Wasserholen sind es fünfzig Schritt bis zum anderen Graben.",
                    "Eine Stimme antwortet, und kurz darauf fliegt eine "
                    "Blechdose herüber. Darin sind Zwieback und ein Streifen "
                    "Speck. Am Morgen fragt der Leutnant, wer in der Nacht "
                    "gerufen hat.",
                    hinweis="gegen den Befehl",
                    aenderungen={"versorgung": 1, "aufmerksamkeit": 2, "rueckhalt": 1}
                ),
                Option(
                    "Den Befehl weitergeben",
                    "Du wiederholst den Wortlaut für die Neuen in deiner Gruppe.",
                    "Der Leutnant nickt dir zu und merkt sich deinen Namen. "
                    "Der Mann von damals rückt beim Essen ein Stück von dir "
                    "ab. Nachts bleibt es still im Abschnitt, und niemand "
                    "ruft.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": -2},
                    stimmung="einsam"
                ),
            ],
            ort="Grabenstellung", gewicht=11,
            braucht_eines=["verbruederung"],
            knuepft_an=["verbruederung"],
            quelle={
                "kurz": "Divisionsbefehle gegen Verbrüderung nach 1914",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird ein Divisionsbefehl, der jede "
                              "Verständigung mit dem Gegner verbietet. Ein "
                              "solcher Befehl sagt, was verboten war, und "
                              "nicht, wie oft es trotzdem geschah.",
            }
        ),

        Ereignis(
            "front_1917_gerichtsherr", [1917], "front",
            "Ein Schreiber holt dich aus dem Unterstand in die Baracke des "
            "Stabes. Drinnen ist es warm, zum ersten Mal seit Wochen. Auf "
            "dem Tisch liegt eine Akte, die zwei Jahre alt ist. Wieder "
            "aufgemacht hat sie der Gerichtsherr, der Offizier mit der Macht "
            "zur Anklage. Ein Name ist aufgetaucht, und deiner steht daneben.",
            [
                Option(
                    "Die Akte bestätigen",
                    "Du nickst zu dem, was der Schreiber dir vorliest.",
                    "Der Gerichtsherr schließt die Mappe und lässt dich "
                    "gehen. Zwei Wochen später kommt die Nachricht, dass ein "
                    "Urteil ergangen ist. In deiner Gruppe weiß jeder, wer "
                    "geholt wurde und zurückkam.",
                    ## Ohne Aufschlag auf die Erschöpfung: Sonst wäre diese
                    ## Karte eine Einbahnstraße, weil beide Optionen sie
                    ## erhöhen. Die Sache ist abgeschlossen; was bleibt,
                    ## steht in der Gruppe, nicht im Körper.
                    aenderungen={"aufmerksamkeit": -2, "rueckhalt": -2}
                ),
                Option(
                    "Nichts hinzufügen",
                    "Du wiederholst Wort für Wort, was du damals gemeldet hast.",
                    "Der Schreiber schreibt langsam mit, und du hörst die "
                    "Feder kratzen. Vierzehn Tage verschärfter Arrest wegen "
                    "widersprüchlicher Angaben. Danach steht dein Name in "
                    "der Akte, aber nicht als Zeuge.",
                    aenderungen={"versorgung": -1, "belastung": 2,
                                 "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
            ],
            ort="Etappe", gewicht=11,
            braucht_eines=["kamerad_gedeckt"],
            knuepft_an=["kamerad_gedeckt"],
            quelle={
                "kurz": "Kriegsgerichtsverfahren wegen Entfernung",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine Kriegsgerichtsakte zur "
                              "unerlaubten Entfernung von der Truppe. Sie "
                              "zeigt Anklage und Urteil, nicht das Gespräch "
                              "vor der Vernehmung.",
            }
        ),

        Ereignis(
            "heimat_1917_aprilstreik", [1917], "heimat",
            "Am Werktor hängt der Anschlag seit dem Morgen. Der Wind drückt "
            "das Papier gegen das Blech. Die Brotmenge wird gekürzt, steht "
            "darauf, mit Wirkung von Montag. Um dich herum wird es still, "
            "und dann sehen sie dich an. „Du hast doch letztes Jahr "
            "angefangen“, sagt eine Frau neben dir.",
            [
                Option(
                    "Wieder vorangehen",
                    "Du steigst auf eine Kiste und sagst, was alle denken.",
                    "In zwei Stunden steht die Halle still, und draußen wird "
                    "es laut. Am dritten Tag holen sie drei von euch ab. Du "
                    "bist nicht dabei, und das macht es nicht leichter.",
                    hinweis="kann Schutzhaft bedeuten",
                    aenderungen={"belastung": 1, "aufmerksamkeit": 3, "rueckhalt": 3}
                ),
                Option(
                    "An der Maschine bleiben",
                    "Du drehst dich weg und arbeitest weiter.",
                    "Der Vorarbeiter sieht es und schreibt nichts auf. In "
                    "der Pause setzt sich niemand zu dir an den Tisch. Am "
                    "Freitag ist dein Lohn vollständig, und im Korb liegt "
                    "mehr als sonst.",
                    aenderungen={"versorgung": 1, "aufmerksamkeit": -1, "rueckhalt": -3},
                    stimmung="einsam"
                ),
            ],
            ort="Rüstungsbetrieb", gewicht=12,
            braucht_eines=["vorangegangen"],
            knuepft_an=["vorangegangen"],
            quelle={
                "kurz": "Aprilstreiks 1917 nach der Kürzung der Brotration",
                "voll": QUELLE_FEHLT,
                "art": "zeitung",
                "einordnung": "Gesucht wird ein Zeitungs- oder Polizeibericht "
                              "zu den Arbeitsniederlegungen vom April 1917 in "
                              "Berlin. Solche Berichte nennen Zahlen und "
                              "Forderungen, nicht die Gespräche am Werktor.",
            }
        ),

        Ereignis(
            "heimat_1917_hilfsdienst", [1917], "heimat",
            "Der Meister ruft dich ins Kontor, und es riecht nach Öl und "
            "Papier. Auf dem Tisch liegt ein Vordruck vom Hilfsdienstgesetz, "
            "das seit Dezember 1916 gilt. Es verpflichtet Männer zwischen "
            "siebzehn und sechzig zur Arbeit, wenn sie nicht Soldat sind. Deine "
            "Zurückstellung gilt weiter, steht jetzt aber in dieser Liste. "
            "Wer den Betrieb wechseln will, braucht einen Abkehrschein, also "
            "die Erlaubnis des alten Werks.",
            [
                Option(
                    "Den Wechsel beantragen",
                    "Im Werk nebenan zahlen sie mehr und haben eine Kantine.",
                    "Der Ausschuss gibt dir den Abkehrschein nach drei "
                    "Wochen. Im neuen Werk gibt es mittags eine warme "
                    "Mahlzeit. Die Leute an deiner alten Bank grüßen dich "
                    "seitdem knapp.",
                    aenderungen={"versorgung": 2, "belastung": 1, "rueckhalt": -2}
                ),
                Option(
                    "Im Betrieb bleiben",
                    "Du unterschreibst und schiebst den Vordruck zurück.",
                    "Der Meister legt das Blatt in eine Mappe und sagt, das "
                    "sei vernünftig. Du kennst hier jeden Griff und jeden "
                    "Namen. Am Monatsende reicht der Lohn wieder nicht bis "
                    "zum Ersten.",
                    aenderungen={"versorgung": -1, "aufmerksamkeit": -1, "rueckhalt": 1}
                ),
            ],
            ort="Rüstungsbetrieb", gewicht=11,
            braucht_eines=["uk"],
            knuepft_an=["uk"],
            quelle={
                "kurz": "Hilfsdienstgesetz vom 5. Dezember 1916",
                "voll": "Gesetz über den vaterländischen Hilfsdienst vom "
                        "5. Dezember 1916, Reichsgesetzblatt 1916",
                "art": "gesetz",
                "einordnung": "Das Gesetz verpflichtet Männer zwischen 17 und "
                              "60 zur Arbeit, wenn sie nicht Soldat sind. Wie "
                              "ein einzelner Betrieb den Abkehrschein "
                              "handhabte, steht darin nicht.",
            }
        ),

        Ereignis(
            "heimat_1917_ablieferung", [1917], "heimat",
            "Im Stall ist es warm, und draußen steht seit einer Stunde die "
            "Kommission. Drei Männer zählen die Säcke und stechen mit einem "
            "Eisen in den Haufen. Die Ablieferungspflicht heißt, dass fast "
            "alles zu festen Preisen an den Staat geht. Für euch bleibt, was "
            "auf einem Zettel steht. Im Heu liegen zwei Säcke, die auf "
            "keiner Liste stehen.",
            [
                Option(
                    "Die Säcke zeigen",
                    "Du führst die Kommission zum Heuboden hinauf.",
                    "Der Vorsitzende trägt beide Säcke nach und dankt dir "
                    "vor den anderen. Beim Abfahren nimmt der Wagen mehr "
                    "mit, als ihr gerechnet habt. Im Dorf spricht sich bis "
                    "zum Abend herum, wer freiwillig gezeigt hat.",
                    aenderungen={"versorgung": -2, "aufmerksamkeit": -2, "rueckhalt": -1}
                ),
                Option(
                    "Die Säcke liegen lassen",
                    "Du schweigst und hältst die Stalltür offen.",
                    "Die Kommission fährt ab, und die Säcke bleiben im Heu. "
                    "Vier Wochen später gibt es abends wieder Kartoffeln. "
                    "Der Nachbar hat zugesehen und sagt nichts, noch nicht.",
                    hinweis="strafbar",
                    aenderungen={"versorgung": 2, "aufmerksamkeit": 2}
                ),
            ],
            ort="Bauernhof", gewicht=11,
            braucht_eines=["landwirtschaft"],
            knuepft_an=["landwirtschaft"],
            quelle={
                "kurz": "Ablieferungspflicht und Erntekommissionen",
                "voll": QUELLE_FEHLT,
                "art": "gesetz",
                "einordnung": "Gesucht wird eine Verordnung über die "
                              "Ablieferung von Getreide und Kartoffeln samt "
                              "den Sätzen für den Eigenbedarf. Sie sagt, was "
                              "abzuliefern war, und nicht, was auf den Höfen "
                              "blieb.",
            }
        ),

        Ereignis(
            "heimat_1917_akkord", [1917], "heimat",
            "An der Wand hängt seit heute früh eine neue Zahl. "
            "Vierzehnhundert Zünder je Schicht statt zwölfhundert, bei "
            "gleichem Lohn. Im Akkord wird nach Stückzahl bezahlt, nicht "
            "nach Stunden. Deine Fingerkuppen sind seit Wochen taub. „Die "
            "Zahl schafft keine von uns“, sagt die Frau an der Bank neben "
            "dir.",
            [
                Option(
                    "Die Zahl schaffen",
                    "Du lässt die Pause aus und arbeitest schneller.",
                    "Am Freitag steht die Zulage auf deinem Lohnzettel. Zu "
                    "Hause gibt es zum ersten Mal seit Wochen Fett. Deine "
                    "rechte Hand zittert abends so, dass du den Löffel "
                    "wechselst.",
                    aenderungen={"versorgung": 2, "belastung": 2}
                ),
                Option(
                    "Das Tempo halten",
                    "Du arbeitest weiter wie bisher und machst deine Pause.",
                    "Die Zulage bleibt aus, und der Lohn reicht bis "
                    "Mittwoch. In der Pause rückt die Kolonne zusammen und "
                    "redet über die Zahl. Der Vorarbeiter schreibt deinen "
                    "Namen auf ein Blatt.",
                    aenderungen={"versorgung": -1, "aufmerksamkeit": 1, "rueckhalt": 2}
                ),
            ],
            ort="Rüstungsbetrieb", gewicht=11,
            braucht_eines=["ruestung"],
            knuepft_an=["ruestung"],
            quelle={
                "kurz": "Akkordarbeit in der Munitionsfertigung",
                "voll": QUELLE_FEHLT,
                "art": "darstellung",
                "einordnung": "Gesucht wird eine Darstellung zur Frauenarbeit "
                              "in der Munitionsfertigung mit Angaben zu "
                              "Akkord und Zulagen. Sie nennt Löhne und "
                              "Stückzahlen, aber nicht, was die Arbeit mit "
                              "den Händen machte.",
            }
        ),

        Ereignis(
            "heimat_1917_schulspeisung", [1917], "heimat",
            "Am Schultor hängt ein Blatt, und davor stehen mehr Mütter als "
            "sonst. Ab Montag gibt es mittags eine Suppe für Kinder, die sie "
            "nötig haben. Bei der Anmeldung fragen sie nach dem Verdienst zu "
            "Hause. Dein Kind zieht an deinem Ärmel und fragt, ob es Suppe "
            "gibt.",
            [
                Option(
                    "Das Kind anmelden",
                    "Du gibst an, was ihr im Monat zur Verfügung habt.",
                    "Ab Montag kommt dein Kind satt aus der Schule. Auf der "
                    "Liste im Flur steht euer Name unter der Überschrift "
                    "bedürftig. Eine Nachbarin sagt nichts dazu und sieht "
                    "trotzdem hin.",
                    ## Der Preis dieser Wahl ist das Ansehen im Haus, nicht
                    ## die Akte. Die Schulspeisung war eine Leistung der
                    ## Stadt und keine Auffälligkeit; ein Aufschlag auf den
                    ## Verdacht wäre an dieser Stelle erfunden.
                    aenderungen={"versorgung": 2, "rueckhalt": -1}
                ),
                Option(
                    "Ohne Anmeldung gehen",
                    "Du faltest das Blatt zusammen und gehst nach Hause.",
                    "Mittags isst dein Kind, was du morgens abgezweigt hast. "
                    "Niemand im Haus weiß, wie knapp es steht. Abends fragt "
                    "es nicht mehr nach der Suppe.",
                    aenderungen={"versorgung": -1, "belastung": 1, "rueckhalt": 1}
                ),
            ],
            ort="Wohnviertel", gewicht=11,
            braucht_eines=["kinder"],
            knuepft_an=["kinder"],
            quelle={
                "kurz": "Schulspeisung und Kriegsküchen in den Städten",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine städtische Akte zur "
                              "Schulspeisung mit den Bedingungen für die "
                              "Teilnahme. Sie nennt Portionen und "
                              "Vorschriften, nicht das Ansehen im Haus.",
            }
        ),

        ## --------------------------------------------------- Freier Bestand

        Ereignis(
            "front_1917_steckruebe", [1917, 1918], "front",
            {
                1917: "Du sitzt auf einem Munitionskasten und hältst das "
                      "Kochgeschirr auf den Knien. Darin schwimmt "
                      "Dörrgemüse, also getrocknetes Gemüse aus der Fabrik. "
                      "Dazu liegen Stücke Kohlrübe in der Brühe, sonst "
                      "Futter für das Vieh. Der Mann neben dir kaut lange "
                      "und sagt: „Riecht wie der Stall zu Hause.“",
                1918: "Du stehst in der Schlange und hältst das kalte "
                      "Kochgeschirr fest. Vor dir wartet ein Junge, der im "
                      "Frühjahr achtzehn geworden ist. Der Koch schöpft "
                      "Dörrgemüse, also getrocknetes Gemüse aus der Fabrik. "
                      "Dein Riemen sitzt zwei Löcher enger als im Sommer. "
                      "Der Alte hinter dir sagt: „Drahtverhau, so nennen wir "
                      "das seit zwei Jahren.“",
            },
            [
                Option(
                    "Essen holen gehen",
                    "Du meldest dich, die schweren Kübel von der Feldküche zu holen.",
                    "Der Henkel schneidet dir zwei Stunden lang in die "
                    "Finger. Beim Ausgeben bleibt für dich noch eine zweite "
                    "Kelle. Die Gruppe rückt zusammen, als du den Kübel "
                    "absetzt.",
                    aenderungen={"versorgung": 2, "belastung": 2, "rueckhalt": 1}
                ),
                Option(
                    "Das Brot abgeben",
                    "Du schiebst deine Scheibe dem Jüngsten hin und behältst die Brühe.",
                    "Er isst die Scheibe in drei Bissen und nickt dir zu. "
                    "Dein Magen knurrt bis in die Nacht. Am Morgen rückt er "
                    "im Unterstand für dich zur Seite.",
                    aenderungen={"versorgung": -1, "rueckhalt": 2}
                ),
            ],
            ort="Grabenstellung", kern=True, gewicht=12, stimmung="hungrig",
            quelle={
                "kurz": "Verpflegung im Feldheer 1917 und 1918",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine Verpflegungsliste, wie sie "
                              "eine Feldküche im Winter 1917 führte. Solche "
                              "Listen nennen Mengen und Sorten, aber nicht "
                              "den Geschmack im Kochgeschirr.",
            }
        ),

        Ereignis(
            "front_1917_geruecht_osten", [1917], "front",
            ## Paket 7, Schritt 3, Teil A.2: die dritte Fassung. Hier
            ## genügt ein halber Satz - wer keinen Mantel hat, sitzt näher
            ## am Kochgeschirr.
            {
                "ohne_mantel":
                    "Du hockst im nassen Graben und hältst die Hände dicht "
                    "am Kochgeschirr; einen Mantel hast du nicht mehr. "
                    "Neben dir sitzt ein Mann, den sie vom Krieg im Osten "
                    "hergeschickt haben. „Der Zar ist fort, der Kaiser von "
                    "Russland“, sagt er leise. „Drüben legen viele die "
                    "Gewehre hin, ich hab es nur gehört.“ Zwei Schritte "
                    "weiter steht dein Vorgesetzter und hört mit.",
                "standard":
                    "Du hockst im nassen Graben und wärmst die Hände am "
                    "Kochgeschirr. Neben dir sitzt ein Mann, den sie vom "
                    "Krieg im Osten hergeschickt haben. „Der Zar ist fort, "
                    "der Kaiser von Russland“, sagt er leise. „Drüben legen "
                    "viele die Gewehre hin, ich hab es nur gehört.“ Zwei "
                    "Schritte weiter steht dein Vorgesetzter und hört mit.",
            },
            [
                Option(
                    "Die Nachricht weitersagen",
                    "Beim Essenholen erzählst du zwei Männern aus dem nächsten Graben davon.",
                    "Am Abend kommen drei Leute zu dir und fragen nach. Du "
                    "redest, bis deine Stimme rau wird. Am nächsten Morgen "
                    "fragt der Feldwebel, wer damit angefangen hat.",
                    hinweis="gegen die Vorschrift",
                    aenderungen={"belastung": -1, "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
                Option(
                    "Den Satz behalten",
                    "Du gibst das Gehörte an niemanden weiter.",
                    "Du löffelst deine Suppe und sagst nichts. Die anderen "
                    "reden über Post und über Läuse. Der Satz aus dem Osten "
                    "bleibt bei dir und wird schwer.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": -2},
                    stimmung="einsam"
                ),
            ],
            ort="Grabenstellung", kern=True, gewicht=12,
            quelle={
                "kurz": "Feldpost 1917 über Gerüchte aus dem Osten",
                "voll": QUELLE_FEHLT,
                "art": "brief",
                "einordnung": "Gesucht wird Feldpost, also Briefe von "
                              "Soldaten, mit Gerüchten aus dem Osten. Solche "
                              "Briefe liegen in Landesarchiven und zeigen "
                              "einzelne Gerüchte, nicht ihre Verbreitung.",
            }
        ),

        Ereignis(
            "front_1917_winterstellung", [1917, 1918], "front",
            ## PAKET 7, SCHRITT 3, TEIL A.2. Die Merkmalsfassung steht UNTER
            ## dem Grundjahr und nicht daneben. Stünde sie auf derselben
            ## Ebene wie 1917 und 1918, sähe ereignistext() Jahreszahlen,
            ## liefe in jahrestext() und fände für 1917 keinen Schlüssel -
            ## genau der Fehler aus AUFGEFALLEN 53.
            ##
            ## Nur 1917 bekommt sie: Die Fassung von 1918 steht schon bei
            ## fünf Sätzen, und die Handwerksregel lässt drei bis fünf zu.
            ## Ein sechster Satz wäre teurer als der Gewinn.
            {
                1917: {
                    "ohne_mantel":
                        "Deine Füße stehen seit dem Morgen im eiskalten "
                        "Wasser. Über der Jacke hast du nichts mehr. Heute "
                        "Nacht sollt ihr die Brustwehr höher bauen, den "
                        "Schutzwall vorn am Graben. Ein Posten flüstert: "
                        "„Wer Feuer macht, verrät die ganze Stellung.“",
                    "standard":
                        "Deine Füße stehen seit dem Morgen im eiskalten "
                        "Wasser. Das Grundwasser steigt im Graben, und die "
                        "Pumpe ist eingefroren. Heute Nacht sollt ihr die "
                        "Brustwehr höher bauen, den Schutzwall vorn am "
                        "Graben. Ein Posten flüstert: „Wer Feuer macht, "
                        "verrät die ganze Stellung.“",
                },
                1918: "Du hockst im Graben und wringst deine Fußlappen aus, "
                      "die Tücher in den Stiefeln. Seit Wochen fehlt Kohle, "
                      "und der kleine Ofen bleibt kalt. Draußen stapelt ein "
                      "Arbeitstrupp Balken für die neue Stellung. Ein "
                      "Unteroffizier zählt die Balken und trägt sie in eine "
                      "Liste ein. Ein Mann neben dir sagt leise: „Einer "
                      "fällt niemandem auf.“",
            },
            [
                Option(
                    "Holz zum Heizen holen",
                    "Du nimmst Holz aus der Stellung und heizt den kleinen Ofen.",
                    "Die Füße werden warm, und du schläfst zwei Stunden am "
                    "Stück. Die anderen rücken an den Ofen und sagen nichts. "
                    "Am Morgen fehlt das Holz, und ein Unteroffizier fragt "
                    "nach.",
                    hinweis="gegen die Vorschrift",
                    aenderungen={"belastung": -2, "aufmerksamkeit": 2, "rueckhalt": 1}
                ),
                Option(
                    "Ohne Feuer bleiben",
                    "Du lässt das Holz liegen und hältst dich in Bewegung.",
                    "Du stampfst bis zum Morgen auf der Stelle und wirst "
                    "nicht warm. Das Holz bleibt liegen, und niemand fragt "
                    "nach dir. Die anderen holen sich Glut woanders und "
                    "lassen dich sitzen.",
                    aenderungen={"belastung": 2, "aufmerksamkeit": -1, "rueckhalt": -1},
                    stimmung="erschoepft"
                ),
            ],
            ort="Grabenstellung", kern=True, gewicht=12,
            quelle={
                "kurz": "Soldatenbrief über Kälte und Brennholz im Winter",
                "voll": QUELLE_FEHLT,
                "art": "brief",
                "einordnung": "Gesucht wird ein Feldpostbrief über Kälte und "
                              "fehlendes Brennholz in der Stellung. Ein "
                              "solcher Brief zeigt das Erleben eines "
                              "Einzelnen, nicht die Lage der ganzen Front.",
            }
        ),

        Ereignis(
            "front_1917_ablosung", [1917], "front",
            "Du hockst im Graben und wärmst die Hände am Kochgeschirr. "
            "Zwanzig neue Männer kommen den Graben herunter, ihre Mäntel "
            "riechen noch nach neuem Tuch. Zwei von ihnen sind kaum "
            "siebzehn, drei gehören zum Landsturm, also zu den ältesten "
            "eingezogenen Männern. „Trifft es einen auch, wenn man den Kopf "
            "unten lässt?“, fragt einer von ihnen. Die anderen stehen dabei "
            "und warten auf deine Antwort.",
            [
                Option(
                    "Ihre Fragen beantworten",
                    "Du erklärst ihnen den Weg zum Unterstand und die Regeln beim Beschuss.",
                    "Du redest lange, und deine Stimme wird rau. Ein "
                    "Unteroffizier bleibt hinter dir stehen und hört zu. Am "
                    "Abend sitzen zwei von ihnen neben dir im Unterstand.",
                    aenderungen={"belastung": 2, "aufmerksamkeit": 1, "rueckhalt": 2}
                ),
                Option(
                    "Nichts dazu sagen",
                    "Du zuckst mit den Schultern und gehst zum Unterstand.",
                    "Du legst dich hin und schläfst zwei Stunden am Stück. "
                    "Die Neuen bleiben unter sich und reden leise weiter. Am "
                    "nächsten Morgen kennst du keinen von ihnen beim Namen.",
                    aenderungen={"belastung": -1, "rueckhalt": -2},
                    stimmung="einsam"
                ),
            ],
            ort="Grabenstellung", kern=True, gewicht=12,
            quelle={
                "kurz": "Ersatztransporte und Landsturm an der Front 1917",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird das Kriegstagebuch einer "
                              "Kompanie, das einen Ersatztransport von 1917 "
                              "verzeichnet. Solche Bände nennen Zahlen und "
                              "Jahrgänge, aber nicht die Gespräche im Graben.",
            }
        ),

        Ereignis(
            "heimat_1917_unterseeboot", [1917], "heimat",
            "In der Schlange treibt der Wind Schneeregen über die Wartenden. "
            "Eine Frau liest die Zeitung laut vor. Seit Februar greifen die "
            "U-Boote, also die Unterseeboote, jedes Schiff ohne Warnung an. "
            "In sechs Monaten sei England am Ende, steht da. Neben dir sagt "
            "jemand halblaut: „Und bis dahin?“",
            [
                Option(
                    "Die Meldung weitersagen",
                    "Du erzählst im Hof, was in der Zeitung stand.",
                    "Am Abend stehen fünf Leute auf der Treppe und rechnen "
                    "die Monate durch. Jemand holt den letzten Rest "
                    "Malzkaffee. Für einen Abend ist es leichter, und am "
                    "Morgen steht dieselbe Schlange da.",
                    aenderungen={"versorgung": -1, "belastung": -1, "rueckhalt": 2}
                ),
                Option(
                    "Laut daran zweifeln",
                    "Du sagst, dass so etwas schon zweimal versprochen wurde.",
                    "Zwei Frauen drehen sich weg, eine gibt dir recht. Am "
                    "nächsten Tag fragt der Hauswirt, wer das gesagt hat. "
                    "Die Frau, die dir recht gab, bringt dir abends zwei "
                    "Eier.",
                    hinweis="fällt auf",
                    aenderungen={"versorgung": 1, "aufmerksamkeit": 1, "rueckhalt": -1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=12,
            quelle={
                "kurz": "Unbeschränkter U-Boot-Krieg ab 1. Februar 1917",
                "voll": QUELLE_FEHLT,
                "art": "zeitung",
                "einordnung": "Gesucht wird eine Tageszeitung vom Februar "
                              "1917 mit der amtlichen Ankündigung des "
                              "U-Boot-Kriegs. Sie zeigt, was verkündet wurde, "
                              "nicht was die Lesenden davon hielten.",
            }
        ),

        Ereignis(
            "heimat_1917_kohlennot", [1917, 1918], "heimat",
            {
                1917: "Im Zimmer siehst du deinen Atem, obwohl es Mittag "
                      "ist. Die Kohlenhandlung gibt seit einer Woche nichts "
                      "mehr aus. Auf dem Anschlag steht, die Züge kämen "
                      "nicht durch. Auf der Straße tragen zwei Kinder "
                      "Bretter von einem Bauzaun nach Hause.",
                1918: "Der Ofen ist seit gestern aus, und die Wand ist "
                      "feucht. Kohle gibt es nur noch gegen einen Schein vom "
                      "Amt. Die Schule ist geschlossen, weil dort auch nicht "
                      "geheizt wird. Aus dem Hof holt jemand nachts die "
                      "letzten Latten vom Schuppen.",
            },
            [
                Option(
                    "Holz vom Zaun holen",
                    "Nachts ist die Straße leer, und der Bauzaun steht schon halb offen.",
                    "Zwei Stunden später brennt der Ofen, und es gibt heiße "
                    "Suppe. Am Morgen steht ein Schutzmann am Rest des Zauns "
                    "und schreibt. Im Zimmer ist es zum ersten Mal seit "
                    "Tagen warm.",
                    hinweis="verboten",
                    aenderungen={"versorgung": 1, "belastung": -2, "aufmerksamkeit": 2}
                ),
                Option(
                    "In ein Zimmer ziehen",
                    "Ihr räumt die kalten Zimmer und schlaft alle in der Küche.",
                    "Zu viert wird die Küche warm, auch ohne Kohle. Nachts "
                    "hört jeder jeden atmen und husten. Am Morgen ist der "
                    "Rücken steif, und niemand beschwert sich.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": 2}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=12,
            quelle={
                "kurz": "Kohlennot in den Kriegswintern 1917 und 1918",
                "voll": QUELLE_FEHLT,
                "art": "zeitung",
                "einordnung": "Gesucht wird ein Zeitungsbericht oder eine "
                              "Stadtakte zur Kohlenzuteilung im Kriegswinter. "
                              "Solche Quellen nennen Mengen und Sperrtage, "
                              "nicht die Kälte in den Wohnungen.",
            }
        ),

        ## Dieses Ereignis steht hier aus einem Bestandsgrund, nicht aus
        ## einem inhaltlichen. Die Bestandstafel zählt den ganzen Vorrat
        ## eines Jahres; die Sackgassenprobe zählt, was in einem einzelnen
        ## Durchgang noch übrig ist. Vier der freien Heimatereignisse
        ## (Todesnachricht, Denunziation, Hamsterfahrt, Lazarettzug) sind
        ## nicht wiederholbar und können 1915 oder 1916 verbraucht sein.
        ## Dann bleiben für die sechs Ziehungen von 1917 nur fünf Karten,
        ## und das Kapitel endet aus Mangel. Gemessen waren das 1,8 Prozent
        ## der langen Heimatdurchgänge. Mit dieser Karte sind es sechs
        ## Karten für sechs Ziehungen.
        Ereignis(
            "heimat_1917_metallsammlung", [1917, 1918], "heimat",
            {
                1917: "An der Tür steht ein Mann mit einer Liste und einem "
                      "Handwagen. Kupfer, Messing und Zinn sind abzuliefern, "
                      "auch aus der Küche. Auf dem Regal stehen der kupferne "
                      "Kessel deiner Großmutter und zwei Leuchter. Draußen "
                      "wird die kleinere Kirchenglocke abgeseilt, und sie "
                      "schlägt ein letztes Mal an.",
                1918: "Der Mann mit dem Handwagen kommt zum dritten Mal in "
                      "diesem Jahr. Diesmal stehen auch Türklinken aus "
                      "Messing auf der Liste. Er hat eine Bescheinigung "
                      "dabei und einen Betrag, der nichts wert ist. Im "
                      "Treppenhaus klappert der Wagen, weil kaum noch etwas "
                      "darin liegt.",
            },
            [
                Option(
                    "Alles abgeben",
                    "Du legst Kessel und Leuchter auf den Wagen.",
                    "Er quittiert dir den Empfang und schreibt einen Betrag "
                    "daneben. Das Regal ist leer, und die Küche klingt "
                    "anders. Am nächsten Tag hängt im Flur eine Liste mit "
                    "den Namen, die gegeben haben.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": 2}
                ),
                Option(
                    "Den Kessel behalten",
                    "Du gibst die Leuchter und schiebst den Kessel hinter das Mehl.",
                    "Er hakt zwei Stücke ab und sieht sich im Zimmer um. Der "
                    "Kessel bleibt, wo er ist, und du kochst abends leise "
                    "darin. Die Nachbarin von gegenüber hat mehr gegeben als "
                    "du.",
                    hinweis="Ablieferung ist Pflicht",
                    aenderungen={"versorgung": 1, "aufmerksamkeit": 1, "rueckhalt": -1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=11,
            quelle={
                "kurz": "Metallsammlungen und Glockenabgabe ab 1917",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine Gemeindeakte über die "
                              "Ablieferung von Kupfer, Messing und "
                              "Kirchenglocken. Sie nennt Mengen und "
                              "Vergütungen, nicht das, was in den Küchen "
                              "blieb.",
            }
        ),

    ]

    for _vorlage in EREIGNISSE_1917:
        if _vorlage.kennung not in EREIGNIS_INDEX:
            EREIGNISSE.append(_vorlage)
            EREIGNIS_INDEX[_vorlage.kennung] = _vorlage

    ## Erst jetzt, wo die Antwortkarten bestehen, wird aus dem Plan eine
    ## Kette. Vorher liefe die Vormerkung ins Leere.
    ketten_nachtragen(KETTEN_NACHTRAG_PAKET4)


################################################################################
## 10e. Paket 4, Schritt 2: die Ereignisse von 1918
################################################################################
##
## Das dichteste Jahr des Spiels: sieben Ziehungen im langen Verlauf, drei
## im kurzen. Es beginnt mit einem Streik im Januar, hat im Frühjahr den
## letzten großen Angriff, im Herbst die Grippe und endet am 11. November.
##
## VIER HARTE VORGABEN, an die sich jeder Text hier hält:
##
##   1. KEIN AUSBLICK. Was die Figur im November 1918 nicht wissen kann,
##      steht nirgends. Kein Wort über Weimar, über Versailles, über 1919
##      oder darüber, wie der Krieg ausgegangen ist. Auch nicht andeutend.
##   2. KEIN DATUM NACH DEM 11. NOVEMBER 1918. Das späteste Ereignis ist
##      front_1918_waffenstillstand, und es spielt am Vormittag dieses
##      Tages.
##   3. MIKRO-MOMENTE STATT ÜBERBLICK. Der Umsturz kommt als abgerissene
##      Kokarde, als Zug, den keiner bestellt hat, als zweiter Anschlag
##      über dem ersten. Niemand erklärt ihn, niemand ordnet ihn ein.
##   4. DIE GRIPPE IST KEINE STRAFE. Sie trifft unabhängig von jeder
##      Entscheidung. Die Optionen betreffen den Umgang damit, nie die
##      Ansteckung, und niemand stirbt an einer Wahl.
##
## DREI BLICKWINKEL:
##   Front        Offensive, Räumungsbefehl, Bahnhof, Waffenstillstand
##   Fabrik/Rat   Januarstreik, Arbeiter- und Soldatenrat, Matrosen
##   Amt/Bürger   Bekanntmachung am Rathaus, Grippeanschlag, Heimkehrer-
##                bogen, Lazarettstation
##
## SIEBEN NEUE FRONTEREIGNISSE STATT SECHS. Der Auftrag nennt sechs. Mit
## sechs bleibt der lange Frontverlauf 1918 im schlechtesten Fall unter
## Deckung: Vier der freien Frontereignisse sind wiederholbar und stehen
## in jedem Kapitel wieder bereit, die übrigen vier (Beute, Urlaub,
## Steckrübe, Winterstellung) können 1915 bis 1917 verbraucht sein. Dann
## bleiben für sieben Ziehungen nur sechs Karten. front_1918_kokarde ist
## die siebte.

init 3 python:

    EREIGNISSE_1918 = [

        ## ------------------------------------------------------ Rückbezüge

        Ereignis(
            "front_1918_abrechnung", [1918], "front",
            "Die Kolonne wartet am Straßenrand auf den Marschbefehl. Neben "
            "dir steht einer aus deiner alten Gruppe, den du zwei Jahre "
            "nicht gesehen hast. Es riecht nach nassem Mantel und kaltem "
            "Rauch. „Der aus dem Zweiten Zug schanzt jetzt bei einer "
            "Strafabteilung, also unter Bewachung“, sagt er. Dann fragt er, "
            "wer damals geredet hat.",
            [
                Option(
                    "Es zugeben",
                    "Du sagst, dass du damals zum Leutnant gegangen bist.",
                    "Er nickt langsam und wirft die Zigarette weg. Bis zum "
                    "Abend spricht keiner mehr mit dir. In der Nacht liegt "
                    "dein Brotbeutel offen, und es fehlt nichts.",
                    aenderungen={"belastung": -1, "rueckhalt": -2},
                    stimmung="einsam"
                ),
                Option(
                    "Bei nichts bleiben",
                    "Du zuckst mit den Schultern und siehst die Straße hinunter.",
                    "Er sieht dich einen Moment zu lange an und lässt es. Ihr "
                    "marschiert am Nachmittag nebeneinander und redet über "
                    "die Verpflegung. Nachts wachst du zweimal auf und weißt "
                    "nicht, wovon.",
                    aenderungen={"belastung": 2, "rueckhalt": 1}
                ),
            ],
            ort="Straße", gewicht=11,
            braucht_eines=["kamerad_gemeldet"],
            knuepft_an=["kamerad_gemeldet"],
            quelle={
                "kurz": "Feldstrafgefangenenabteilungen im Feldheer",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine Akte über die "
                              "Feldstrafgefangenenabteilungen, in denen "
                              "Verurteilte unter Bewachung arbeiteten. Sie "
                              "nennt Zahlen und Vorschriften, nicht das, was "
                              "die alte Gruppe darüber sprach.",
            }
        ),

        Ereignis(
            ## SEIT PAKET 5, SCHRITT 1, TEIL C AUCH IN DER ETAPPE. Das ist
            ## keine Ausweitung, sondern die Behebung eines Bruchs, den
            ## erst das Öffnen des Pfades sichtbar gemacht hat: Das erste
            ## Glied dieser Kette, front_1916_zaehlung, trägt "etappe" seit
            ## jeher. Wer die Zählung dort zog, merkte eine Antwort vor,
            ## die auf seinem Pfad nie fallen konnte - 86 offene
            ## Vormerkungen in 24000 Durchgängen, gemessen unmittelbar
            ## nach dem Umlegen des Schalters.
            ##
            ## Der Text braucht dafür kein Wort: Er spielt in der kalten
            ## Schreibstube über einem Bogen mit Spalten und trug schon
            ## vorher ort="Etappe". Geschrieben wurde er für die Front,
            ## gemeint war immer dieser Ort.
            "front_1918_liste", [1918], ["front", "etappe"],
            "In der kalten Schreibstube liegt wieder ein Bogen mit Spalten. "
            "Diesmal geht es um die, die aus russischer Gefangenschaft "
            "zurückkommen. Der Bogen fragt nach Ort, Dauer und Umgang in der "
            "Gefangenschaft. Draußen warten sechzig Männer in geliehenen "
            "Mänteln. Der Schreiber schiebt dir den Federhalter hin, und die "
            "Tinte fließt zäh.",
            [
                Option(
                    "Alles eintragen",
                    "Du füllst jede Spalte aus, so wie es der Bogen verlangt.",
                    "Am Abend sind sechzig Zeilen voll und deine Hand ist "
                    "steif. Vier Namen werden noch am selben Tag "
                    "herausgerufen. Was mit ihnen geschieht, erfährst du "
                    "nicht.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -2, "rueckhalt": -1}
                ),
                Option(
                    "Die Spalten leer lassen",
                    "Du trägst nur Namen und Truppenteil ein und lässt den Rest offen.",
                    "Der Bogen geht so hinaus, wie du ihn gelassen hast. Zwei "
                    "Tage später kommt er zurück, mit rotem Strich und einer "
                    "Frage. Beim Essen rückt ein Heimkehrer neben dich und "
                    "teilt seinen Zwieback.",
                    hinweis="gegen die Anweisung",
                    aenderungen={"versorgung": 1, "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
            ],
            ort="Etappe", gewicht=11,
            braucht_eines=["zaehlung_ausgefuellt"],
            knuepft_an=["zaehlung_ausgefuellt"],
            quelle={
                "kurz": "Rückkehr aus russischer Gefangenschaft 1918",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine Akte aus einem "
                              "Heimkehrerlager von 1918 mit den "
                              "Erhebungsbögen. Sie zeigt, was gefragt wurde, "
                              "nicht was die Befragten verschwiegen.",
            }
        ),

        Ereignis(
            "front_1918_freiwillig_von_1914", [1918], "front",
            "Der Regen läuft dir in den Kragen, während ihr auf den Appell "
            "wartet. Von denen, die im August 1914 mit dir eingerückt sind, "
            "steht noch einer neben dir. Ein Leutnant verliest die Namen der "
            "Kompanie. Er ist jünger, als du 1914 warst. Bei jedem dritten "
            "Namen antwortet niemand.",
            [
                Option(
                    "Von damals erzählen",
                    "Abends fragen die Neuen, wie es im ersten Sommer war.",
                    "Du erzählst vom Bahnhof und von der Kreide auf den "
                    "Waggons. Zwei hören zu, einer lacht an der falschen "
                    "Stelle. Danach liegst du wach und rechnest die Namen "
                    "durch.",
                    aenderungen={"belastung": 2, "rueckhalt": 2}
                ),
                Option(
                    "Nichts davon erzählen",
                    "Du sagst, das sei lange her, und drehst dich zur Wand.",
                    "Du schläfst früh ein und wachst ohne Traum auf. Am "
                    "Morgen fragt keiner mehr. Der Mann von 1914 sitzt beim "
                    "Essen zwei Plätze weiter.",
                    aenderungen={"belastung": -1, "rueckhalt": -2},
                    stimmung="einsam"
                ),
            ],
            ort="Ruhequartier", gewicht=11,
            braucht_eines=["kriegsfreiwillig"],
            knuepft_an=["kriegsfreiwillig"],
            quelle={
                "kurz": "Kriegsfreiwillige von 1914 und ihre Verluste",
                "voll": QUELLE_FEHLT,
                "art": "statistik",
                "einordnung": "Gesucht wird eine Regimentsgeschichte mit "
                              "Angaben zu den Kriegsfreiwilligen des ersten "
                              "Sommers. Solche Quellen nennen Zahlen, aber "
                              "nicht, wer am Ende noch antwortete.",
            }
        ),

        Ereignis(
            "front_1918_befehl", [1918], "front",
            "Der Meldegänger bringt den Umschlag um vier Uhr früh. Die "
            "Stellung soll bis zum Abend geräumt sein, alles Schwere bleibt "
            "zurück. Du sollst den Befehl an drei Gruppen durchgeben. "
            "Draußen ist es noch dunkel, und der Boden ist hart gefroren. "
            "Zwei der Gruppen halten die Stellung seit sechs Wochen.",
            [
                Option(
                    "Den Wortlaut durchgeben",
                    "Du gibst den Befehl weiter, so wie er dasteht.",
                    "Bis Mittag ist alles verpackt, was zwei Männer tragen "
                    "können. Der Rest steht noch in der Stellung, als ihr "
                    "abmarschiert. Niemand fragt dich, warum, und das ist "
                    "schlimmer.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": -1}
                ),
                Option(
                    "Zeit dazugeben",
                    "Du sagst, die Räumung sei erst zum Morgen befohlen.",
                    "Die Gruppen nehmen mit, was sie sonst hätten liegen "
                    "lassen. Beim Abmarsch trägt jeder eine Decke mehr und "
                    "zwei Konserven. In der Meldung am Abend steht eine "
                    "Uhrzeit, die nicht stimmt.",
                    hinweis="gegen den Befehl",
                    aenderungen={"versorgung": 2, "aufmerksamkeit": 2, "rueckhalt": 1}
                ),
            ],
            ort="Grabenstellung", gewicht=11,
            braucht_eines=["offizier"],
            knuepft_an=["offizier"],
            quelle={
                "kurz": "Räumung von Stellungen im Herbst 1918",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird ein Regimentsbefehl aus dem "
                              "Herbst 1918 über die Räumung einer Stellung. "
                              "Er nennt Fristen und Gerät, nicht die Stunden, "
                              "die dabei verschoben wurden.",
            }
        ),

        Ereignis(
            "heimat_1918_rat", [1918], "heimat",
            "In der Halle steht die Maschine still, und es ist zum ersten "
            "Mal leise. Ein Soldat mit rotem Band liest vor, dass ein Rat "
            "gebildet wird. Ein Arbeiter- und Soldatenrat, sagt er, "
            "entscheidet ab heute über Brot und Ordnung. Sie suchen Leute, "
            "die schon einmal vorne gestanden haben. Zwei Frauen drehen sich "
            "zu dir um.",
            [
                Option(
                    "Dich wählen lassen",
                    "Du trittst vor die Kiste und lässt deinen Namen aufschreiben.",
                    "Bis Mitternacht sitzt ihr zu acht und teilt Mehl und "
                    "Kohle ein. Am Morgen kommt der Direktor und redet zum "
                    "ersten Mal mit dir. Dein Name steht jetzt auf einer "
                    "Liste, die zwei Ämter kennen.",
                    aenderungen={"versorgung": 1, "belastung": 2,
                                 "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
                Option(
                    "Nach Hause gehen",
                    "Du nimmst deinen Mantel und gehst durch den Seitenausgang.",
                    "Zu Hause ist es still, und du kochst dir etwas Warmes. "
                    "Am nächsten Tag ist eingeteilt, wer wie viel bekommt. "
                    "Deine Nachbarin sagt, sie habe deinen Namen vermisst.",
                    aenderungen={"belastung": -1, "aufmerksamkeit": -1, "rueckhalt": -2}
                ),
            ],
            ort="Rüstungsbetrieb", gewicht=12,
            braucht_eines=["vorangegangen"],
            knuepft_an=["vorangegangen"],
            quelle={
                "kurz": "Arbeiter- und Soldatenräte im November 1918",
                "voll": QUELLE_FEHLT,
                "art": "darstellung",
                "einordnung": "Belegt ist, dass sich im November 1918 in "
                              "vielen Städten Arbeiter- und Soldatenräte "
                              "bildeten. Wer in einem einzelnen Betrieb "
                              "gewählt wurde, steht in keiner Übersicht.",
            }
        ),

        Ereignis(
            "heimat_1918_grippe", [1918], "heimat",
            "Seit vorgestern liegt jemand im Haus mit Fieber und trockenem "
            "Husten. Die Grippe geht um, und die Zeitung nennt sie die "
            "spanische. Heute ist der Tag, an dem die Ausgabestelle die "
            "Karten abstempelt. Wer nicht kommt, bekommt für diese Woche "
            "nichts. Auf der Treppe hörst du zwei Türen weiter dasselbe "
            "Husten.",
            [
                Option(
                    "Zur Ausgabestelle gehen",
                    "Du lässt den Kranken allein und stellst dich in die Reihe.",
                    "Nach zwei Stunden hast du die Stempel für die ganze "
                    "Woche. Zu Hause ist das Fieber gestiegen, und niemand "
                    "war da. Du wäschst dir lange die Hände, obwohl das "
                    "Wasser kalt ist.",
                    aenderungen={"versorgung": 2, "belastung": 2, "rueckhalt": -1}
                ),
                Option(
                    "Im Haus bleiben",
                    "Du bleibst am Bett und legst kalte Tücher auf.",
                    "Am Abend sinkt das Fieber ein wenig, und der Husten wird "
                    "lockerer. Die Karten bleiben ungestempelt bis zur "
                    "nächsten Woche. Die Nachbarin bringt abends eine halbe "
                    "Schüssel Suppe herüber.",
                    aenderungen={"versorgung": -2, "belastung": -1, "rueckhalt": 2}
                ),
            ],
            ort="Wohnviertel", gewicht=12,
            braucht_eines=["haushalt"],
            knuepft_an=["haushalt"],
            quelle={
                "kurz": "Grippewelle im Herbst 1918",
                "voll": QUELLE_FEHLT,
                "art": "zeitung",
                "einordnung": "Gesucht wird ein Zeitungsbericht vom Herbst "
                              "1918 über die Grippe und die Maßnahmen der "
                              "Städte. Solche Berichte nennen Anordnungen, "
                              "nicht die Lage in den einzelnen Wohnungen.",
            }
        ),

        Ereignis(
            ## PFAD UM "etappe" ERWEITERT, Paket 5, Schritt 1, Teil C.9.
            ##
            ## Der Auftrag ging davon aus, diese Karte trage schon beide
            ## Pfade und greife nur deshalb nicht, weil das Merkmal
            ## fehle. Nachgemessen stimmt beides nicht: Sie trug
            ## ["front", "heimat"] - die Etappe stand gar nicht darin -,
            ## und der NACHHALL_PLAN behauptete daneben "beide".
            ##
            ## Für die Etappe ist sie genau richtig. Die Kriegslazarette
            ## lagen dort, und wer über einstieg_etappe kommt, HAT das
            ## Merkmal lazarett zwingend (siehe erwerb_moeglich in
            ## herkunft.rpy). Der Text passt ohne ein Wort Änderung: eine
            ## Station, acht Schwestern, eine Oberin.
            ##
            ## "front" bleibt stehen, obwohl das Merkmal dort heute nicht
            ## zu bekommen ist. Krankenträger gab es an der Front, aber
            ## sie wären eine eigene Lebenslage; kommt sie einmal, ist der
            ## Pfad schon da. Bis dahin ist die Zeile dort wirkungslos und
            ## kostet nichts.
            "lazarett_1918_grippestation", [1918], ["front", "etappe", "heimat"],
            "Die Grippestation ist seit einer Woche voller als die "
            "Verwundetenstation. Die Kranken sind jung und liegen zu zweit "
            "in einem Bett. Es riecht nach Kampfer und nach ungelüfteter "
            "Wäsche. Zwei Schwestern von acht sind selbst krank geworden. "
            "Die Oberin fragt, wer heute Nacht die Station allein nimmt.",
            [
                Option(
                    "Die Nacht übernehmen",
                    "Du meldest dich für die Station und die zwölf Stunden.",
                    "Du gehst die Reihe zwölfmal ab und wechselst Tücher. "
                    "Gegen vier wird es ruhiger, und du setzt dich auf den "
                    "Boden. Am Morgen bekommst du eine Tasse echten Kaffee "
                    "und ein Bett bis Mittag.",
                    aenderungen={"versorgung": 1, "belastung": 2, "rueckhalt": 2}
                ),
                Option(
                    "Die Nacht abgeben",
                    "Du sagst, dass du noch eine Nacht nicht durchhältst.",
                    "Die Oberin nickt und schreibt einen anderen Namen auf. "
                    "Du schläfst acht Stunden und wachst ohne Kopfschmerzen "
                    "auf. In der Frühstückspause redet niemand mit dir.",
                    aenderungen={"belastung": -2, "rueckhalt": -2}
                ),
            ],
            ort="Lazarett", gewicht=12,
            braucht_eines=["lazarett"],
            knuepft_an=["lazarett"],
            quelle={
                "kurz": "Grippestationen in Lazaretten im Herbst 1918",
                "voll": QUELLE_FEHLT,
                "art": "erinnerung",
                "einordnung": "Gesucht wird der Bericht einer Schwester über "
                              "den Dienst auf einer Grippestation. Ein "
                              "solcher Bericht zeigt einzelne Nächte, nicht "
                              "die Zahl der Kranken im ganzen Reich.",
            }
        ),

        ## --------------------------------------------------- Freier Bestand

        Ereignis(
            "front_1918_offensive", [1918], "front",
            "Seit fünf Uhr früh liegt das Feuer auf den Gräben gegenüber. Um "
            "halb zehn sollt ihr hinüber, hinter den Sturmtrupps her. Ein "
            "Pionier legt Bretter über den eigenen Draht. In deinem Magen "
            "ist nichts als Ersatzkaffee. „Diesmal kommen wir durch“, sagt "
            "einer und meint es.",
            [
                Option(
                    "Mit dem Sturmtrupp vor",
                    "Du gehst in der ersten Welle mit, dort wo die Lücke ist.",
                    "Ihr seid am Mittag vier Kilometer weiter als je zuvor. "
                    "Am Abend liegt ihr ohne Nachschub in fremdem Gelände. "
                    "Deine Beine zittern, und niemand weiß, wo die eigene "
                    "Küche steht.",
                    aenderungen={"versorgung": -2, "belastung": 1, "rueckhalt": 2}
                ),
                Option(
                    "Hinter der Welle bleiben",
                    "Du hältst dich hinter denen, die die Lücke schlagen.",
                    "Du kommst am Nachmittag durch einen Graben, in dem es "
                    "still ist. In einem Unterstand stehen Kisten mit "
                    "Zwieback und Marmelade. Der Zugführer sieht, dass du "
                    "hinten warst, und sagt es laut.",
                    aenderungen={"versorgung": 2, "aufmerksamkeit": 1, "rueckhalt": -2}
                ),
            ],
            ort="Niemandsland", kern=True, gewicht=13, stimmung="angst",
            quelle={
                "kurz": "Deutsche Frühjahrsoffensive ab 21. März 1918",
                "voll": QUELLE_FEHLT,
                "art": "darstellung",
                "einordnung": "Belegt sind Beginn und Verlauf der deutschen "
                              "Angriffe des Frühjahrs 1918 sowie die Rolle "
                              "der Sturmtruppen. Wie der einzelne Mann diese "
                              "Tage erlebte, steht in keiner Übersicht.",
            }
        ),

        Ereignis(
            "front_1918_kokarde", [1918], "front",
            "Auf dem Etappenbahnhof riecht es nach Kohlenrauch und nassem "
            "Tuch. Aus einem Zug steigen Männer, die keiner erwartet hat. An "
            "ihren Mützen fehlt die Kokarde, das runde Abzeichen mit den "
            "Landesfarben. Einer trägt ein rotes Band am Ärmel. Ein "
            "Hauptmann geht vorbei, und niemand grüßt.",
            [
                Option(
                    "Mit ihnen sprechen",
                    "Du fragst, woher sie kommen und was in der Stadt los ist.",
                    "Sie erzählen von Kiel und von einem Rat, der jetzt "
                    "entscheidet. Einer drückt dir ein Blatt in die Hand, das "
                    "du nicht liest. Am Abend fragen dich drei aus deiner "
                    "Gruppe, was du gehört hast.",
                    aenderungen={"belastung": -1, "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
                Option(
                    "Zum Wagen weitergehen",
                    "Du siehst zur Seite und gehst zum Verpflegungswagen.",
                    "Am Wagen bekommst du deine Ration ohne Wartezeit. Hinter "
                    "dir wird es laut, und du drehst dich nicht um. Am Abend "
                    "weißt du weniger als alle anderen.",
                    aenderungen={"versorgung": 1, "aufmerksamkeit": -1, "rueckhalt": -2}
                ),
            ],
            ort="Etappe", kern=True, gewicht=12,
            quelle={
                "kurz": "Matrosen und Novembertage 1918",
                "voll": QUELLE_FEHLT,
                "art": "darstellung",
                "einordnung": "Belegt ist, dass Matrosen ab Anfang November "
                              "mit der Bahn durch das Reich fuhren und Räte "
                              "bildeten. Wie einzelne Soldaten an den "
                              "Bahnhöfen darauf reagierten, ist daraus nicht "
                              "abzulesen.",
            }
        ),

        Ereignis(
            "front_1918_waffenstillstand", [1918], "front",
            "Um neun Uhr kommt der Befehl, das Feuer um elf einzustellen. "
            "Bis dahin schießt die Batterie hinter euch weiter. Ihr sitzt im "
            "Graben und seht auf die Uhr des Zugführers. Um elf wird es "
            "still, und das Ohr sucht etwas. Einer weint, einer lacht, die "
            "meisten sagen nichts.",
            [
                Option(
                    "Das Gewehr abgeben",
                    "Ein Feldwebel sammelt die Waffen für den Rückmarsch ein.",
                    "Du legst es auf den Stapel und wischst die Hände an der "
                    "Hose ab. Ohne das Gewicht auf der Schulter gehst du "
                    "schief. Am Nachmittag bekommt jeder eine halbe "
                    "Konserve.",
                    aenderungen={"versorgung": 1, "belastung": -2,
                                 "aufmerksamkeit": -1, "rueckhalt": -1}
                ),
                Option(
                    "Es behalten",
                    "Du behältst dein Gewehr und sagst, du hättest es verloren.",
                    "Niemand sucht heute nach einem Gewehr. Auf dem "
                    "Rückmarsch gehst du mit dem Gewicht, an das du dich "
                    "gewöhnt hast. Zwei aus der Gruppe machen es dir nach.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
            ],
            ort="Grabenstellung", kern=True, gewicht=13,
            quelle={
                "kurz": "Waffenstillstand vom 11. November 1918",
                "voll": "Waffenstillstandsabkommen von Compiègne, "
                        "11. November 1918",
                "art": "darstellung",
                "einordnung": "Belegt sind der Tag und die Stunde, zu der die "
                              "Kampfhandlungen eingestellt wurden. Was in den "
                              "Gräben in dieser Stunde gesprochen wurde, ist "
                              "daraus nicht abzulesen.",
            }
        ),

        Ereignis(
            "heimat_1918_januarstreik", [1918], "heimat",
            "Am Montagmorgen bleibt die Halle kalt, und niemand legt die "
            "Hand an. Draußen stehen sie zu Hunderten und rufen nach Brot "
            "und nach Frieden. Die Zeitung von morgen wird von Kohlenmangel "
            "schreiben. Ein Aufseher schreibt auf, wer nicht am Platz steht.",
            [
                Option(
                    "Vor das Tor gehen",
                    "Du legst die Feile hin und gehst zu den anderen hinaus.",
                    "Draußen ist es kalt, und ihr steht bis zum Mittag. Am "
                    "dritten Tag wird der Betrieb unter militärische Aufsicht "
                    "gestellt. Zwei aus deiner Kolonne bekommen den "
                    "Gestellungsbefehl.",
                    hinweis="kann Einberufung bedeuten",
                    aenderungen={"belastung": 1, "aufmerksamkeit": 2, "rueckhalt": 3}
                ),
                Option(
                    "Am Platz bleiben",
                    "Du arbeitest weiter und siehst nicht zum Fenster.",
                    "Bis Freitag gehörst du zu den wenigen mit vollem Lohn. "
                    "In der Kantine ist der Tisch neben dir frei. Der Meister "
                    "nickt dir zu, wenn er vorbeigeht.",
                    aenderungen={"versorgung": 1, "aufmerksamkeit": -1, "rueckhalt": -3},
                    stimmung="einsam"
                ),
            ],
            ort="Rüstungsbetrieb", kern=True, gewicht=12,
            quelle={
                "kurz": "Januarstreik 1918 in Berlin und anderen Städten",
                "voll": QUELLE_FEHLT,
                "art": "darstellung",
                "einordnung": "Belegt sind der Zeitraum des Streiks Ende "
                              "Januar 1918 und die Forderungen nach Brot und "
                              "Frieden. Wie ein einzelner Betrieb reagierte, "
                              "steht in keiner Übersicht.",
            }
        ),

        Ereignis(
            "heimat_1918_grippewelle", [1918], "heimat",
            "An der Litfaßsäule hängt seit gestern ein neuer Anschlag. "
            "Schulen, Kinos und Versammlungen bleiben bis auf Weiteres "
            "geschlossen. Die Straße riecht nach Essig, den die Leute gegen "
            "die Ansteckung verdampfen. Vor der Apotheke steht eine Schlange "
            "bis um die Ecke. Der Tischler an der Ecke baut jetzt nichts "
            "anderes mehr.",
            [
                Option(
                    "In der Apotheke anstehen",
                    "Du stellst dich an, obwohl dort vielleicht nichts mehr hilft.",
                    "Nach drei Stunden bekommst du eine Tüte mit Kamille und "
                    "Baldrian. Die Frau vor dir hustet die ganze Zeit in "
                    "deine Richtung. Zu Hause kochst du Tee und stellst ihn "
                    "ans Bett.",
                    aenderungen={"belastung": 1, "rueckhalt": 1}
                ),
                Option(
                    "Die Wohnung nicht verlassen",
                    "Du bleibst drinnen und schickst niemanden hinaus.",
                    "Drei Tage lang öffnest du nur für den Milchmann die Tür. "
                    "Der Vorrat wird kleiner, und am dritten Tag ist das Brot "
                    "alle. Im Haus ist es so still, dass du die Uhr im Flur "
                    "hörst.",
                    aenderungen={"versorgung": -1, "aufmerksamkeit": -1, "rueckhalt": -1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=12,
            quelle={
                "kurz": "Behördliche Maßnahmen gegen die Grippe 1918",
                "voll": QUELLE_FEHLT,
                "art": "zeitung",
                "einordnung": "Gesucht wird ein Amtsblatt oder ein "
                              "Zeitungsanschlag über Schließungen wegen der "
                              "Grippe. Solche Quellen nennen Verbote, nicht "
                              "die Mittel, die in den Wohnungen versucht "
                              "wurden.",
            }
        ),

        Ereignis(
            "heimat_1918_matrosen", [1918], "heimat",
            "Am Bahnhof steigen Matrosen aus, die niemand hierher bestellt "
            "hat. Sie tragen rote Bänder und reden mit jedem, der stehen "
            "bleibt. Ein Wachtmeister sieht zu und greift nicht ein. Zwei "
            "stellen einen Tisch auf und legen eine Liste darauf. Der Wind "
            "reißt an dem Papier, und jemand beschwert es mit einem Stein.",
            [
                Option(
                    "Sich eintragen",
                    "Du schreibst deinen Namen unter die anderen auf der Liste.",
                    "Der Matrose bedankt sich und gibt dir die Hand. Am Abend "
                    "hängt die Liste im Schaufenster der Buchhandlung. Deine "
                    "Nachbarin liest sie und sagt beim Abendessen nichts.",
                    aenderungen={"belastung": -1, "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
                Option(
                    "Zusehen und gehen",
                    "Du bleibst am Rand stehen und gehst dann zum Markt.",
                    "Auf dem Markt gibt es heute Fisch, weil kaum jemand da "
                    "ist. Du trägst zwei Heringe nach Hause und hörst die "
                    "Rufe hinter dir. Abends fragt dich jemand, ob du dabei "
                    "warst.",
                    aenderungen={"versorgung": 2, "aufmerksamkeit": -1, "rueckhalt": -1}
                ),
            ],
            ort="Bahnhof", kern=True, gewicht=12,
            quelle={
                "kurz": "Matrosenaufstand und Rätebildung im November",
                "voll": QUELLE_FEHLT,
                "art": "darstellung",
                "einordnung": "Belegt ist, dass Matrosen ab dem 4. November "
                              "in viele Städte fuhren und dort Räte "
                              "gründeten. Wie die Einwohner an einem "
                              "einzelnen Bahnhof reagierten, steht in keiner "
                              "Übersicht.",
            }
        ),

        Ereignis(
            "heimat_1918_bekanntmachung", [1918], "heimat",
            "Am Rathaus klebt eine Bekanntmachung über der alten, und der "
            "Kleister ist noch feucht. Die alte trug den Namen des Landrats. "
            "Auf der neuen steht ein Name, den du nicht kennst. Beide "
            "fordern Ruhe und Ordnung, gedruckt auf demselben Papier. Ein "
            "Mann im Mantel liest lange und geht dann rückwärts weg.",
            [
                Option(
                    "Zur Sparkasse gehen",
                    "Du willst abheben, was von den Kriegsanleihen noch flüssig ist.",
                    "Am Schalter stehen zwanzig Leute mit demselben Gedanken. "
                    "Du bekommst die Hälfte in bar und den Rest als Zusage. "
                    "Auf dem Heimweg kaufst du Mehl zu einem Preis, den du "
                    "sonst nie zahlst.",
                    aenderungen={"versorgung": 2, "belastung": 1, "aufmerksamkeit": 1}
                ),
                Option(
                    "Nach Hause gehen",
                    "Du lässt das Geld liegen, wo es ist, und gehst zurück.",
                    "Zu Hause räumst du auf, was seit Wochen liegen geblieben "
                    "ist. Am Abend kommen zwei Nachbarn und fragen, was du "
                    "gelesen hast. Ihr sitzt bis spät zusammen und werdet "
                    "euch nicht einig.",
                    aenderungen={"versorgung": -1, "belastung": -1, "rueckhalt": 2}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=12,
            quelle={
                "kurz": "Bekanntmachungen der Novembertage 1918",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine Sammlung amtlicher Anschläge "
                              "aus den Novembertagen in einer Stadt. Sie "
                              "zeigt, was angeordnet wurde, nicht wer die "
                              "Anordnung noch befolgte.",
            }
        ),

    ]

    for _vorlage in EREIGNISSE_1918:
        if _vorlage.kennung not in EREIGNIS_INDEX:
            EREIGNISSE.append(_vorlage)
            EREIGNIS_INDEX[_vorlage.kennung] = _vorlage

    ## Die dritte Kette dieses Pakets. Der Abstand ist 2: Wer die Zählung
    ## 1916 ausfüllt, bekommt die zweite Liste 1918. Das erste Glied reicht
    ## bis 1916, das zweite deckt 1918 ab - die Regel aus dem Vorweg ist
    ## damit eingehalten.
    KETTEN_NACHTRAG_1918 = {
        "front_1916_zaehlung": {
            "Die Liste ausfüllen": ("front_1918_liste", 2),
        },
    }

    ketten_nachtragen(KETTEN_NACHTRAG_1918)


################################################################################
## 10f. Paket 5, Schritt 1: die Ereignisse der Etappe
################################################################################
##
## Die Etappe hatte im ganzen Projekt kein einziges eigenes Ereignis. Sie
## wurde von fünf geliehenen Karten getragen - front_feldpost,
## front_urlaub, front_1916_zaehlung, heimat_lazarettzug und der Kette
## front_nachfrage -, und vier davon sind von der Front oder aus der
## Heimat übernommen. Deshalb steht dieser Abschnitt hier: nicht als
## Ergänzung, sondern als die erste eigene Stimme dieses Pfades.
##
## WAS DIE ETAPPE VON DER FRONT UNTERSCHEIDET, und was jeder Text hier
## einhält:
##
##   1. ANDERE GERÄUSCHE. Rangierbetrieb statt Einschlag, Feder statt
##      Feuer, ein Zug, der wartet, statt eines Angriffs, der kommt.
##   2. ANDERE GERÜCHE. Kohle, Jute, Karbol, nasses Tuch - nicht die
##      aufgerissene Erde.
##   3. EIN ANDERES VERHÄLTNIS ZUR GEFAHR. Wer hier steht, wird nicht
##      beschossen. Er entscheidet über Mengen, Reihenfolgen und Zahlen,
##      und seine Entscheidungen treffen andere.
##   4. DIE SPIELERIN IST NICHT DIE LEIDTRAGENDE. Sie steht daneben und
##      tut etwas oder tut es nicht. Kein Erzähler ordnet das ein.
##
## ZWEI ROLLEN, EIN PFAD. In die Etappe führen zwei Wege: die Musterung
## mit dem Grad "g.v." und der Lazarettdienst aus der Erwerbswahl. Der
## eine bringt Soldaten, der andere Lazarettkräfte, Frauen wie Männer.
## Kein Text hier setzt eine der beiden Rollen voraus. Es gibt keine
## Kompanie, keinen Appell und keinen Graben; es gibt Dienst, Listen,
## Rampen und Ausgabestellen, an denen beide stehen können.
##
## GRUPPE 1 VON 3 - DIE ORDNUNG DER ETAPPE. Sechs Ereignisse über den
## Ort selbst: die Ankunft, den Bahnhof, das Magazin, die Rampe, die
## Schreibstube und den Bahnsteig, auf dem die Front einen ansieht.
##
## VIER DAVON SIND WIEDERHOLBAR ODER MEHRJÄHRIG. Der Etappenbestand war
## der dünnste des Spiels (1914 ein freies Ereignis bei Soll 5 im langen
## Verlauf). Mehrjährige Karten mit eigener Jahresfassung füllen ihn,
## ohne dass ein Jahr denselben Satz zweimal zeigt.

init 3 python:

    EREIGNISSE_ETAPPE_GRUPPE1 = [

        ## ------------------------------------------------ Der Ort selbst

        ## Die einzige Karte, die das Wort "Etappe" erklärt. Sie fällt nur
        ## 1914 und steht deshalb am Anfang jedes Etappenverlaufs, der im
        ## ersten Kapitel überhaupt zieht.
        Ereignis(
            "etappe_1914_ankunft", [1914], "etappe",
            "Der Zug hält am Nachmittag, und du steigst auf einen Bahnsteig "
            "aus Kies. Hier beginnt die Etappe, das Gebiet hinter der Front, "
            "in dem der Nachschub verwaltet wird. Es riecht nach Kohle und "
            "nach heißem Öl. Ein Feldwebel sucht deinen Namen auf einer Liste "
            "und zeigt auf einen Schuppen. „Hier wird nicht geschossen, hier "
            "wird gezählt“, sagt er.",
            [
                Option(
                    "Nach vorn fragen",
                    "Du fragst, wie man von hier zur kämpfenden Truppe kommt.",
                    "Der Feldwebel sieht dich an und setzt einen Haken in "
                    "seine Spalte. Bis zum Abend trägst du Kisten, und "
                    "niemand kommt auf die Frage zurück. Deine Schultern "
                    "brennen noch, als du dich hinlegst.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": 1}
                ),
                Option(
                    "Den Schuppen ansehen",
                    "Du gehst dorthin, wohin er zeigt, und siehst dir die Regale an.",
                    "Im Schuppen steht Zwieback in Kisten bis unter das Dach. "
                    "Ein Schreiber zeigt dir die Liste und den Nagel, an dem "
                    "sie hängt. Abends isst du satt, und der Neue aus deinem "
                    "Wagen sieht dir dabei zu.",
                    aenderungen={"versorgung": 2, "rueckhalt": -1}
                ),
            ],
            ort="Etappenort", kern=True, gewicht=12,
            quelle={
                "kurz": "Etappenordnung: Kommandanturen und Magazine",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                ## Kein Satzende auf einer Jahreszahl: Der Zerleger von
                ## Probe 5 sieht den Punkt hinter einer Ziffer nicht als
                ## Satzende und zählt die Einordnung dann als einen Satz.
                "einordnung": "Gesucht wird das Kriegstagebuch einer "
                              "Etappenkommandantur aus dem ersten "
                              "Kriegsherbst. Solche Akten nennen "
                              "Dienststellen und Aufgaben, nicht den Ton, in "
                              "dem ein Neuer empfangen wurde.",
            }
        ),

        ## Der Bahnhof ist die Maschine der Etappe. Die drei Fassungen
        ## zeigen dieselbe Arbeit in drei Lagen: 1914 fährt alles nach
        ## vorn, 1916 stehen zwei Züge gegeneinander, 1918 fährt jeder,
        ## der einsteigt. Wiederholbar, weil es der tägliche Dienst ist.
        Ereignis(
            "etappe_bahnhofsdienst", [1914, 1915, 1916, 1917, 1918], "etappe",
            {
                1914: "Der Zug aus dem Reich steht seit einer Stunde am "
                      "Bahnsteig. Du zählst die Wagen und trägst die Zahl in "
                      "ein Buch. Aus einem Wagen ruft jemand nach Wasser. Der "
                      "Bahnhofsoffizier sagt, der Zug fahre in zehn Minuten "
                      "weiter. Der Eimer steht am anderen Ende des Bahnsteigs.",
                1916: "Der Bahnsteig ist seit dem Morgen belegt, und zwei Züge "
                      "warten auf Gleis drei. Auf dem einen liegen Verwundete, "
                      "auf dem anderen steht Munition. Der Fahrplan sagt, die "
                      "Munition hat Vorfahrt. Ein Sanitäter fragt dich, wie "
                      "lange es noch dauert. Du riechst den Wagen, bevor du "
                      "ihn siehst.",
                1918: "Am Bahnsteig stehen mehr Leute als Plätze im Zug. Die "
                      "Hälfte hat keinen Marschbefehl und will trotzdem "
                      "mitfahren. Einer hat das runde Abzeichen von der Mütze "
                      "getrennt. Er fragt nicht, er steigt ein. In deinem Buch "
                      "bleibt die Spalte für die Namen leer.",
            },
            [
                Option(
                    "Den Fahrplan halten",
                    "Du fertigst ab, was auf dem Papier zuerst steht.",
                    "Der Zug rollt pünktlich aus der Halle, und deine Zahl "
                    "stimmt. Hinter dir wird weiter gerufen, bis auch der "
                    "zweite fährt. Am Abend hast du keine Beanstandung und "
                    "einen steifen Rücken.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": -1}
                ),
                Option(
                    "Erst den anderen Wagen",
                    "Du lässt zuerst versorgen, was nicht warten kann.",
                    "Es dauert zwanzig Minuten, und die Meldung geht verspätet "
                    "hinaus. Zwei Leute vom Bahnsteig bedanken sich, einer "
                    "schreibt deinen Namen auf. Du gehst als Letzter vom "
                    "Gleis, und deine Stiefel sind nass.",
                    aenderungen={"aufmerksamkeit": 2, "rueckhalt": 2}
                ),
            ],
            ort="Bahnhof", kern=True, gewicht=11, wiederholbar=True,
            quelle={
                "kurz": "Bahnhofskommandanturen und Militärfahrplan",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird ein Fahrplan oder Dienstbuch "
                              "einer Bahnhofskommandantur im Etappengebiet. "
                              "Ein Fahrplan zeigt die Rangfolge der Züge, "
                              "nicht die Menschen, die dabei warten mussten.",
            }
        ),

        ## Die Ausgabestelle ist der Ort, an dem der Mangel eine Zahl
        ## bekommt. 1914 ist mehr da als aufgeschrieben, 1916 ist da, was
        ## vorn keiner mehr nimmt, 1918 ist das Regal leer und der Wagen
        ## trotzdem vor der Tür.
        Ereignis(
            "etappe_verpflegungsausgabe", [1914, 1915, 1916, 1917, 1918], "etappe",
            {
                1914: "Vor dem Magazin warten die Fuhrleute seit dem Morgen. "
                      "Drinnen riecht es nach Jute und geröstetem Kaffee. Du "
                      "gibst aus, was auf dem Zettel steht: Brot, Speck, "
                      "Kaffee. Der Stapel im Regal ist höher als die Zahl auf "
                      "dem Papier. Ein Fahrer fragt, ob für seine Kolonne noch "
                      "ein Laib abfällt.",
                1916: "Vor dem Magazin ist die Schlange kürzer, weil weniger "
                      "Kolonnen fahren. Es riecht nach Rüben, seit die Kisten "
                      "hinten stehen. Auf dem Zettel steht Brot, im Regal "
                      "liegt Brot, in das Rüben gemahlen sind. Ein Fahrer "
                      "sagt, vorn nähmen sie es nicht mehr an. Du hast nichts "
                      "anderes.",
                1918: "Im Magazin sind zwei Regale leer, und niemand füllt sie "
                      "nach. Auf dem Zettel steht eine Menge, die es hier "
                      "nicht gibt. Draußen warten drei Kolonnen und ein Wagen "
                      "ohne Papiere. Der Mann auf dem Bock hat seit gestern "
                      "nichts gegessen. Er sieht dich an und wartet.",
            },
            [
                Option(
                    "Nach Zettel ausgeben",
                    "Was nicht auf dem Papier steht, bekommt niemand.",
                    "Die Abrechnung stimmt am Abend auf das Pfund genau. Der "
                    "Fahrer spuckt neben das Rad und fährt ohne Gruß. Beim "
                    "Zumachen merkst du, dass deine Hände nach Jute riechen.",
                    aenderungen={"aufmerksamkeit": -1, "rueckhalt": -2}
                ),
                Option(
                    "Einen Laib abschreiben",
                    "Du buchst Bruch und Schwund und legst etwas beiseite.",
                    "Der Fahrer nimmt das Brot unter den Mantel und nickt nur. "
                    "In der Spalte für Schwund steht jetzt eine Zahl, die du "
                    "erklären musst. Abends teilst du selbst mit, und es "
                    "schmeckt nach nichts.",
                    hinweis="der Schwund wird geprüft",
                    aenderungen={"versorgung": 1, "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
            ],
            ort="Magazin", kern=True, gewicht=12, wiederholbar=True,
            quelle={
                "kurz": "Verpflegungsstärke und Ausgabelisten der Etappe",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Ausgabelisten eines "
                              "Etappenmagazins mit Sollmenge und "
                              "tatsächlicher Ausgabe. Solche Listen zeigen "
                              "Mengen und Fehlbeträge, nicht die Absprachen "
                              "an der Rampe.",
            }
        ),

        ## Die Etappenseite des Lazarettzuges: nicht die Ankunft daheim,
        ## sondern das Umladen und das Sortieren davor. heimat_lazarettzug
        ## bleibt daneben stehen; es zeigt denselben Zug aus der Heimat.
        Ereignis(
            "etappe_verwundetenzug", [1914, 1915, 1916, 1917, 1918], "etappe",
            {
                1914: "Der erste Zug kommt in der Nacht an, und niemand hat "
                      "mit so vielen gerechnet. Auf dem Bahnsteig liegen "
                      "Bahren in zwei Reihen. Ein Arzt geht die Reihen ab und "
                      "entscheidet, wer zuerst fährt. Es riecht nach Karbol, "
                      "dem scharfen Mittel gegen Keime, und nach nassem Stroh. "
                      "Jemand ruft nach dir, weil du gerade dastehst.",
                1916: "Der Zug hält an der Rampe, und die Träger arbeiten in "
                      "zwei Schichten. Die Bahren kommen jetzt sortiert an: "
                      "leicht, schwer, nicht mehr fahrfähig. Für die letzte "
                      "Reihe gibt es einen eigenen Schuppen. Ein Träger sagt, "
                      "dort werde nur noch Tee gereicht. Du hältst die Liste "
                      "und schreibst mit.",
                1918: "Der Zug hält heute außerhalb, und niemand darf ohne "
                      "Tuch vors Gesicht hinein. In den Wagen liegen nicht nur "
                      "Verwundete, sondern auch Fiebernde. Die Grippe ist "
                      "schneller als jede Meldung. Ein Arzt sagt, er brauche "
                      "zwei Wagen für die Kranken allein. Zwei Wagen hat der "
                      "Zug nicht.",
            },
            [
                Option(
                    "Die Reihe abarbeiten",
                    "Du nimmst die Bahren, wie sie liegen, und hörst nicht hin.",
                    "Bis zum Morgen sind alle Wagen beladen, und die Liste ist "
                    "vollständig. Deine Arme zittern, als du den Bleistift "
                    "wieder ansetzt. Was du gehört hast, hast du nicht "
                    "aufgeschrieben.",
                    aenderungen={"belastung": 2, "aufmerksamkeit": -1, "rueckhalt": -1}
                ),
                ## Ohne Aufschlag auf die Erschöpfung, und das ist keine
                ## Schönung: Wer stehen bleibt, trägt in dieser Nacht
                ## nichts mehr. Trüge die Karte auf beiden Wegen
                ## belastung, wäre sie eine Einbahnstraße - Probe 4 meldet
                ## das seit Paket 2 als Fehler.
                Option(
                    "Bei dem Letzten bleiben",
                    "Einer aus der letzten Reihe fragt nach einer Anschrift.",
                    "Du schreibst Namen und Straße auf ein Stück Packpapier, "
                    "und der Bleistift bricht zweimal ab. Die Bahren tragen "
                    "andere weiter, und die Liste bleibt unvollständig. Der "
                    "Feldwebel sagt am Morgen nichts und macht einen Strich.",
                    aenderungen={"aufmerksamkeit": 2, "rueckhalt": 1}
                ),
            ],
            ort="Verwundetensammelstelle", kern=True, gewicht=12,
            quelle={
                "kurz": "Verwundetentransport und Sichtung in der Etappe",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird ein Sanitätsbericht über "
                              "Verwundetensammelstellen und Lazarettzüge im "
                              "Etappengebiet. Solche Berichte nennen Zahlen "
                              "und Wege, nicht die Nächte an der Rampe.",
            }
        ),

        ## Der Kern des Pfades in einer Karte: Was aufgeschrieben wird,
        ## gilt. Die Frage des Jahresbogens 1916 für die Etappe lautet
        ## genau so - wem gehört deine Arbeit, dir oder der Verwaltung.
        Ereignis(
            "etappe_listen", [1915, 1916, 1917, 1918], "etappe",
            {
                1915: "In der Schreibstube ist es warm, und die Feder kratzt. "
                      "Du führst die Stärkemeldung, also die Zahl der Männer, "
                      "die eine Einheit noch hat. Für gestern fehlen dir zwei "
                      "Namen. Der Feldwebel sagt, die Zahl müsse bis Mittag "
                      "hinaus. Er sagt nicht, welche Zahl.",
                1917: "Die Schreibstube ist kalt, weil die Kohle für das "
                      "Lazarett gebraucht wird. Auf dem Tisch liegen drei "
                      "Listen, die einander widersprechen. Eine zählt, wer zu "
                      "essen bekommt, eine, wer arbeiten kann, eine die "
                      "Kranken. Der Hauptmann will bis heute Abend eine Zahl. "
                      "Deine Finger sind zu steif für saubere Ziffern.",
            },
            [
                Option(
                    "Die höhere Zahl melden",
                    "Du nimmst die Liste, nach der mehr Leute da sind.",
                    "Die Meldung geht durch, und die Einheit bekommt "
                    "Verpflegung für alle. Zwei Wochen später fragt ein "
                    "Prüfer, wohin der Rest gegangen ist. Du zeigst auf die "
                    "Liste und nicht auf dich.",
                    hinweis="die Prüfung kommt später",
                    aenderungen={"versorgung": 1, "aufmerksamkeit": 2}
                ),
                Option(
                    "Die niedrige Zahl melden",
                    "Du meldest, wer wirklich noch dasteht.",
                    "Die Zahl stimmt, und die Ausgabe wird gekürzt. In der "
                    "Kantine setzt sich der Schreiber von nebenan woandershin. "
                    "Nachts rechnest du im Kopf nach, ob du dich geirrt hast.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": -2}
                ),
            ],
            ort="Schreibstube", kern=True, gewicht=11, wiederholbar=True,
            quelle={
                "kurz": "Stärkemeldungen und Verpflegungslisten",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Stärke- und "
                              "Verpflegungsmeldungen einer Etappeneinheit aus "
                              "mehreren Monaten. Sie zeigen, welche Zahlen "
                              "gemeldet wurden, und nicht, wie sie zustande "
                              "kamen.",
            }
        ),

        ## Das Spannungsfeld, erste Hälfte (Auftrag Teil A.3): der Blick
        ## des Fronturlaubers. Kein Wort fällt, das die Etappe verurteilt;
        ## das Schimpfwort steht im Beleg, nicht im Spieltext.
        Ereignis(
            "etappe_fronturlauber", [1915, 1916, 1917, 1918], "etappe",
            {
                1915: "Auf dem Bahnsteig warten die Urlauber auf den Zug nach "
                      "Hause. Ihre Mäntel sind lehmig bis zur Brust, deiner "
                      "ist es nicht. Einer sieht auf deine sauberen Stiefel "
                      "und dann in dein Gesicht. Es riecht nach nassem Tuch "
                      "und kaltem Rauch. Niemand rückt zur Seite, und niemand "
                      "sagt etwas.",
                1917: "Der Urlauberzug hat vier Stunden Verspätung, und die "
                      "Bank ist besetzt. Einer rückt zur Seite und macht dir "
                      "Platz, ohne dich anzusehen. „Ihr habt es ja gut hier“, "
                      "sagt er in die Runde. Sein Mantel riecht nach kaltem "
                      "Rauch und nach Erde. Die anderen warten, was du darauf "
                      "sagst.",
            },
            [
                Option(
                    "Den Blick halten",
                    "Du siehst zurück und sagst, was durch deine Hände geht.",
                    "Du zählst auf: Brot, Bahren, Namen, jeden Tag dieselbe "
                    "Liste. Einer nickt langsam, ein anderer dreht sich weg. "
                    "Als der Zug einfährt, steht noch jemand neben dir.",
                    aenderungen={"belastung": 1, "rueckhalt": 1}
                ),
                Option(
                    "Den Bahnsteig verlassen",
                    "Du hast auf dem Gleis nebenan zu tun.",
                    "Du gehst am Zug entlang, bis die Stimmen hinter dir "
                    "leiser werden. Auf dem Nebengleis ist wenig zu tun, und "
                    "du bist früh fertig. Im Rücken spürst du den Bahnsteig "
                    "noch, als du längst um die Ecke bist.",
                    aenderungen={"belastung": -1, "rueckhalt": -1}
                ),
            ],
            ort="Bahnsteig", kern=True, gewicht=12,
            quelle={
                "kurz": "Frontsprache über die Etappe: das Etappenschwein",
                "voll": QUELLE_FEHLT,
                "art": "erinnerung",
                "einordnung": "Gesucht werden Feldpostbriefe oder "
                              "Erinnerungen, in denen Frontsoldaten über die "
                              "Etappe sprechen. Sie zeigen das Schimpfwort und "
                              "den Neid, nicht die Arbeit, die dahinter lag.",
            }
        ),

    ]

    for _vorlage in EREIGNISSE_ETAPPE_GRUPPE1:
        if _vorlage.kennung not in EREIGNIS_INDEX:
            EREIGNISSE.append(_vorlage)
            EREIGNIS_INDEX[_vorlage.kennung] = _vorlage


## GRUPPE 2 VON 3 - DER MANGEL UND DIE POST ###################################
##
## Die erste Gruppe zeigt, wie die Etappe arbeitet. Diese zeigt, was
## geschieht, wenn das, was sie verteilen soll, nicht mehr da ist: Brot
## ohne Mehl, Wagen ohne Zünder, Pferde ohne Hafer, Züge, die ausbleiben.
## Dazu die zweite Hälfte des Spannungsfeldes - der Brief aus der Heimat,
## der fragt, warum man nicht kommt.
##
## KEINE DAVON TRÄGT kern=True. Der kurze Verlauf zieht nur Kernkarten
## und hat je Kapitel zwei bis drei Ziehungen; er ist mit Gruppe 1 schon
## gedeckt. Diese sechs füllen den langen Verlauf, in dem sieben Karten
## je Kapitel fallen, und sorgen dort für die Reserve.

init 3 python:

    EREIGNISSE_ETAPPE_GRUPPE2 = [

        ## ------------------------------------------------- Was fehlt

        ## Brot ist die Ware, an der die Etappe gemessen wird. Die drei
        ## Fassungen zeigen dieselbe Backstube, in der zuerst der Teig,
        ## dann das Mehl und zuletzt die Kohle knapp wird.
        Ereignis(
            "etappe_feldbaeckerei", [1914, 1915, 1916, 1917, 1918], "etappe",
            {
                1914: "In der Backstube ist es heiß, und das Mehl liegt dir "
                      "auf den Lippen. Die Kolonne backt für zwölftausend Mann "
                      "in zwei Schichten. Aus dem Ofen kommt Kommissbrot, das "
                      "dunkle Brot des Heeres. Ein Bäcker sagt, der Teig gehe "
                      "zu schnell und werde nicht durch. Der Wagen für vorn "
                      "steht schon angespannt.",
                1916: "In der Backstube riecht es süßlich, seit Kartoffeln in "
                      "den Teig gehen. Das Mehl reicht nur für die Hälfte der "
                      "Laibe. Eine Anweisung erlaubt, den Teig mit Rüben zu "
                      "strecken. Das Brot wird schwer und ist am zweiten Tag "
                      "klebrig. Der Fahrer für vorn wartet und sieht in die "
                      "Kiste.",
                1918: "Zwei Öfen stehen kalt, weil die Kohle nicht gekommen "
                      "ist. Von zwanzig Leuten der Kolonne liegen sieben mit "
                      "Fieber. Die Menge auf dem Zettel ist dieselbe wie im "
                      "Frühjahr. Ein Bäcker rechnet vor, dass es nicht geht. "
                      "Draußen stehen die Fahrer im Regen und warten trotzdem.",
            },
            [
                Option(
                    "Die Menge halten",
                    "Du backst die Zahl, die verlangt ist, und nimmst kleinere Laibe.",
                    "Die Kiste ist voll, und der Wagen fährt zur vereinbarten "
                    "Zeit. Vorn wiegt jeder Laib weniger, und das merkt dort "
                    "jeder. Deine Unterarme sind bis zum Ellenbogen rot vom "
                    "Ofen.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": -1}
                ),
                Option(
                    "Weniger und ganze Laibe",
                    "Du meldest die kleinere Zahl und backst sie richtig durch.",
                    "Der Fahrer nimmt die halbe Ladung und redet nicht lange. "
                    "Am Nachmittag steht ein Offizier in der Backstube und "
                    "will die Bücher sehen. Das Brot in der Kiste riecht wie "
                    "Brot, und das ist selten geworden.",
                    aenderungen={"belastung": -1, "aufmerksamkeit": 2, "rueckhalt": 1}
                ),
            ],
            ort="Feldbäckerei", gewicht=10, wiederholbar=True,
            quelle={
                "kurz": "Feldbäckereikolonnen und die Streckung des Brotes",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine Backvorschrift oder "
                              "Mehlabrechnung einer Feldbäckereikolonne. Sie "
                              "nennt Mischung und Menge, nicht das, was vorn "
                              "davon ankam.",
            }
        ),

        ## Die Etappe versorgt auch die Materialschlacht. Diese Karte
        ## zeigt sie von hinten: nicht das Feuer, sondern die Kiste, die
        ## ohne Zünder losfahren soll.
        Ereignis(
            "etappe_munitionslager", [1915, 1916, 1917, 1918], "etappe",
            {
                1915: "Im Schuppen stehen die Kisten in Reihen bis an die "
                      "Wand. Es riecht nach Öl und nach frischem Holz, und du "
                      "zählst Zünder. Draußen wartet eine Kolonne, die seit "
                      "dem Morgen nicht bewegt wurde. Der Fahrer sagt, vorn "
                      "sei seit gestern nichts angekommen. Auf deinem Zettel "
                      "steht eine andere Kolonne zuerst.",
                1917: "Das Lager ist bis unter das Dach voll, und trotzdem "
                      "fehlt etwas. Die Granaten sind da, die Zünder nicht. "
                      "Ein Offizier will die Wagen beladen lassen und die "
                      "Zünder nachschicken. Du hast die Vorschrift gelesen und "
                      "weißt, dass das verboten ist. Er sieht auf die Uhr und "
                      "wartet auf deine Unterschrift.",
            },
            [
                Option(
                    "Nach Vorschrift laden",
                    "Du machst nur, was auf dem Papier gedeckt ist.",
                    "Die Wagen stehen bis zum Abend, und die Kolonne fährt "
                    "leer zurück. Der Fahrer sagt dir, was er von dir hält, "
                    "und du hörst es dir an. Nachts stehen die Pferde noch im "
                    "Hof, und niemand hat sie ausgespannt.",
                    aenderungen={"belastung": 1, "rueckhalt": -2}
                ),
                Option(
                    "Ohne Papier laden",
                    "Du lässt aufladen und trägst es später nach.",
                    "Die Kolonne fährt noch am Vormittag, und der Offizier "
                    "bedankt sich. Zwei Tage später fragt der Prüfer nach zwei "
                    "Kisten, die nirgends stehen. Du trägst sie nach und "
                    "schreibst dabei langsam.",
                    hinweis="ohne Deckung im Buch",
                    aenderungen={"aufmerksamkeit": 2, "rueckhalt": 1}
                ),
            ],
            ort="Munitionslager", gewicht=10,
            quelle={
                "kurz": "Munitionsausgabe und Nachschub der Etappe",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Ausgabebücher eines "
                              "Munitionslagers mit Anforderung und "
                              "Auslieferung. Sie zeigen Mengen und Fristen, "
                              "nicht den Streit um die Reihenfolge.",
            }
        ),

        ## Die Etappe fuhr auf Pferden, nicht auf Motoren. Diese Karte
        ## trägt nur bis 1916: Ab 1917 ist der Fuhrpark ein Teil des
        ## allgemeinen Mangels und steht in
        ## etappe_1917_nachschubstockung.
        Ereignis(
            "etappe_fuhrpark", [1914, 1915, 1916], "etappe",
            {
                1914: "Im Stall stehen achtzig Pferde, und die Hälfte ist aus "
                      "der Landwirtschaft geholt. Es riecht nach Stroh und "
                      "nassem Fell. Ein Ackergaul aus einem Dorf trägt noch "
                      "das Brandzeichen des Bauern. Er lahmt seit dem Marsch "
                      "und wird trotzdem eingespannt. Der Fahrer fragt dich, "
                      "was er in die Meldung schreiben soll.",
                1916: "Im Stall ist es still, weil zu wenig Hafer da ist. Die "
                      "Pferde bekommen kurz geschnittenes Stroh und Laub, und "
                      "man sieht die Rippen. Drei sind in dieser Woche "
                      "eingegangen und liegen hinter dem Stall. Der Tierarzt "
                      "sagt, mit halbem Futter halten sie den Winter nicht. "
                      "Auf dem Zettel steht dieselbe Zahl an Fahrten wie im "
                      "Sommer.",
            },
            [
                Option(
                    "Das Pferd einspannen",
                    "Du meldest es fahrbereit, damit die Kolonne rollt.",
                    "Die Kolonne fährt ab, und die Fracht ist am Abend vorn. "
                    "Auf halbem Weg bleibt das Tier stehen und geht nicht "
                    "weiter. Der Fahrer kommt zu Fuß zurück und sieht dich "
                    "nicht an.",
                    aenderungen={"aufmerksamkeit": -1, "rueckhalt": -2}
                ),
                Option(
                    "Es ausspannen lassen",
                    "Du meldest es untauglich und streichst die Fahrt.",
                    "Die Fracht bleibt stehen, und zwei Kolonnen müssen sie "
                    "mitnehmen. Ein Offizier fragt, wer hier über Pferde zu "
                    "entscheiden hat. Am Abend steht das Tier im Stall und "
                    "frisst wieder.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": 2, "rueckhalt": 1}
                ),
            ],
            ort="Pferdedepot", gewicht=10,
            quelle={
                "kurz": "Pferde im Heer: Ersatz, Futter und Verluste",
                "voll": QUELLE_FEHLT,
                "art": "statistik",
                "einordnung": "Gesucht werden Zahlen zu Pferdebestand und "
                              "Futterzuteilung im deutschen Heer. Sie zeigen "
                              "Verluste und Mengen, nicht den einzelnen Gaul "
                              "im Stall.",
            }
        ),

        ## Die Frage des Jahresbogens 1917 für die Etappe lautet: Woher
        ## nimmst du, was du brauchst, wenn nichts mehr da ist. Diese
        ## Karte stellt sie in ihrer nüchternsten Form - der Vorrat ist
        ## da, aber gezählt, und Gezähltes darf nicht heraus.
        Ereignis(
            "etappe_1917_nachschubstockung", [1917], "etappe",
            "Seit vier Tagen ist kein Zug aus dem Reich gekommen. Auf dem Hof "
            "stehen leere Wagen, und es riecht nach nassem Pferd. Der "
            "Etappeninspekteur, der Vorgesetzte für dieses Gebiet, lässt alle "
            "Vorräte neu zählen. Was gezählt ist, gilt als vorhanden und darf "
            "nicht mehr ausgegeben werden. Vor der Tür wartet ein Sanitäter "
            "und braucht Verbandstoff.",
            [
                Option(
                    "Erst zählen lassen",
                    "Die Aufnahme geht vor, so steht es im Befehl.",
                    "Am Abend ist die Liste fertig und stimmt auf das Stück "
                    "genau. Der Sanitäter ist zweimal wiedergekommen und beim "
                    "dritten Mal nicht mehr. Deine Schrift wird gegen Ende der "
                    "Liste kleiner.",
                    aenderungen={"aufmerksamkeit": -1, "rueckhalt": -2}
                ),
                Option(
                    "Vor der Aufnahme ausgeben",
                    "Du gibst den Verbandstoff heraus und zählst danach.",
                    "Der Sanitäter geht mit zwei Paketen und bedankt sich "
                    "nicht. In der Aufnahme fehlen zwei Posten, und der "
                    "Inspekteur findet sie. Du erklärst es zweimal und beim "
                    "zweiten Mal langsamer.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
            ],
            ## kern=True, weil diese Karte seit Paket 5, Schritt 1 der
            ## Träger des Jahres 1917 auf der Etappe ist. Ihr Kipppunkt
            ## im Jahresbogen lautet: "Die Etappe verwaltet den Mangel,
            ## statt den Nachschub zu verteilen" - genau das geschieht
            ## hier. Ein Träger ohne kern trägt im kurzen Verlauf nichts.
            ort="Etappenort", kern=True, gewicht=11,
            quelle={
                "kurz": "Nachschubstockungen und Bestandsaufnahmen 1917",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird ein Bericht einer "
                              "Etappeninspektion über Bestände und "
                              "ausbleibende Züge. Er nennt Mengen und "
                              "Fristen, nicht die Fälle, die währenddessen "
                              "warteten.",
            }
        ),

        ## ------------------------------------------------- Die Post

        ## Die Zensurstelle lag in der Etappe, nicht an der Front. Die
        ## Einlage rotstift zeigt das Streichen als Handgriff; diese Karte
        ## zeigt, was danach kommt: den leeren Vordruck neben dem Stift.
        Ereignis(
            "etappe_zensurstelle", [1915, 1916, 1917, 1918], "etappe",
            {
                1916: "An deinem Tisch liegen dreißig Briefe, und es riecht "
                      "nach kaltem Rauch. Der Rotstift streicht, was Orte, "
                      "Zahlen oder Verluste nennt. In einem Brief schreibt "
                      "einer, dass er nicht mehr kann. Auf dem Umschlag steht "
                      "ein Name, den du kennst. Neben dem Stift liegt ein "
                      "Vordruck für die Meldung.",
                1918: "Der Stapel ist heute doppelt so hoch, und die Hälfte "
                      "kommt aus dem Lazarett. Viele schreiben von der Grippe, "
                      "und das darf nicht hinaus. Ein Brief nennt die Zahl der "
                      "Toten in der Baracke. Die Anweisung sagt, solche Zahlen "
                      "werden gestrichen. Der Mann, der ihn geschrieben hat, "
                      "liegt zwei Baracken weiter.",
            },
            [
                Option(
                    "Nur streichen",
                    "Du fährst mit dem Stift durch und lässt den Vordruck liegen.",
                    "Der Brief geht weiter, und die Hälfte der Zeilen ist "
                    "schwarz. Der Vordruck bleibt leer und liegt am Abend noch "
                    "auf dem Tisch. Deine Finger sind rot von dem Stift, bis "
                    "in die Nagelbetten.",
                    aenderungen={"aufmerksamkeit": 1, "rueckhalt": 1}
                ),
                Option(
                    "Die Meldung schreiben",
                    "Du trägst den Namen in den Vordruck ein.",
                    "Die Meldung geht am selben Tag hinaus, und der "
                    "Vorgesetzte nickt dir zu. Der Name verschwindet vom "
                    "Umschlag und taucht in einer Akte auf. Du liest den "
                    "nächsten Brief und weißt danach nicht, wovon er handelte.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -2, "rueckhalt": -2}
                ),
            ],
            ort="Zensurstelle", gewicht=11,
            quelle={
                "kurz": "Briefprüfstellen und die Überwachung der Feldpost",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Stimmungsberichte einer "
                              "Briefprüfstelle mit den Auszügen, die sie "
                              "festhielt. Sie zeigen, was gestrichen und was "
                              "weitergegeben wurde, nicht die Leute an den "
                              "Tischen.",
            }
        ),

        ## Das Spannungsfeld, zweite Hälfte (Auftrag Teil A.3): der Brief
        ## aus der Heimat, der fragt, warum man nicht kommt. Die
        ## Gegenkarte zu etappe_fronturlauber - dort sieht die Front auf
        ## die Etappe, hier die Heimat.
        Ereignis(
            "etappe_brief_von_daheim", [1915, 1916, 1917, 1918], "etappe",
            {
                1915: "Der Brief liegt seit dem Morgen auf deiner Decke, und "
                      "das Quartier riecht nach Kohle. Zu Hause haben sie "
                      "gehört, dass es dir gut geht. Sie fragen, warum du dann "
                      "nicht kommst. Andere seien schon zweimal dagewesen, "
                      "schreiben sie. Urlaub gibt es hier nach Liste, und "
                      "deine Nummer steht weit hinten.",
                1917: "Der Umschlag ist grau, und das Papier fühlt sich rau "
                      "an. Zu Hause stehen sie seit Wochen für halbe Mengen "
                      "an. Sie schreiben, du säßest im Warmen und äßest jeden "
                      "Tag. Am Ende steht die Frage, ob du etwas schicken "
                      "kannst. In deinem Spind liegt eine Büchse, die du nicht "
                      "abgerechnet hast.",
            },
            [
                Option(
                    "Ein Päckchen schicken",
                    "Du packst zusammen, was du hier bekommst und dort fehlt.",
                    "Das Päckchen wiegt vier Pfund, und die Post nimmt es ohne "
                    "Frage an. In deiner Kiste ist danach Platz und in der "
                    "Abrechnung eine Lücke. Drei Wochen später kommt ein "
                    "Brief, in dem sie sich bedanken.",
                    aenderungen={"versorgung": -1, "aufmerksamkeit": 1, "rueckhalt": 2}
                ),
                Option(
                    "Es dabei belassen",
                    "Du schreibst zurück, dass es hier auch nicht anders ist.",
                    "Der Brief geht ab, und du liest ihn vorher nicht noch "
                    "einmal. Was du geschrieben hast, stimmt und beantwortet "
                    "die Frage nicht. Abends isst du deine Zuteilung und wirst "
                    "nicht satt davon.",
                    aenderungen={"belastung": 1, "rueckhalt": -2}
                ),
            ],
            ort="Quartier", gewicht=11,
            quelle={
                "kurz": "Feldpost aus der Heimat an Etappenangehörige",
                "voll": QUELLE_FEHLT,
                "art": "brief",
                "einordnung": "Gesucht werden Briefe aus der Heimat an Männer "
                              "und Frauen im Etappendienst. Sie zeigen die "
                              "Erwartungen der Familie, nicht die Lage am "
                              "Empfangsort.",
            }
        ),

    ]

    for _vorlage in EREIGNISSE_ETAPPE_GRUPPE2:
        if _vorlage.kennung not in EREIGNIS_INDEX:
            EREIGNISSE.append(_vorlage)
            EREIGNIS_INDEX[_vorlage.kennung] = _vorlage


## GRUPPE 3 VON 3 - DIE ANDEREN UND DAS ENDE ##################################
##
## Die Etappe ist der einzige Ort dieses Spiels, an dem Kriegsgefangene
## und Zivilarbeiter aus dem besetzten Gebiet vorkommen können. Der
## Auftrag verlangt sie ausdrücklich (Teil A.3a), und der Lehrplan der
## achten Klasse rechnet sie zum industriellen Krieg.
##
## DIE REGEL FÜR DIESE VIER KARTEN, wörtlich aus dem Auftrag: Die
## Spielerin ist NICHT die Leidtragende. Sie ist die, die daneben steht
## und etwas tut oder nicht tut. Deshalb:
##
##   - Kein Elendsbild und keine Gore-Beschreibung. Was zu sehen ist,
##     sind Lappen um Füße, ein leerer Becher, ein Platz auf einem
##     Wagen - nicht das, was danach kam.
##   - Kein Erzähler, der einordnet. Kein Satz sagt, dass es Unrecht
##     war. Der Widerspruch entsteht daraus, dass die Spielerin die
##     Vorschrift kennt und die Lage sieht.
##   - Ein Vorgang, ein Blick, eine Entscheidung. Nicht mehr.
##
## DIE BELEGE SIND HIER KEINE PLATZHALTER. Drei der Karten stützen sich
## auf die Haager Landkriegsordnung von 1907, also auf geltendes Recht
## der Zeit, das die Handlung im Bild ausdrücklich regelt: Artikel 6 für
## die Arbeit Kriegsgefangener, Artikel 52 für Dienste der Einwohner im
## besetzten Gebiet, Artikel 52 und 53 für Requisitionen. Der Reiz
## dieser Belege im Unterricht liegt darin, dass sie nicht sagen, was
## geschah, sondern was verboten war.
##
## KEIN DATUM NACH DEM 11. NOVEMBER 1918, wie schon in Abschnitt 10e:
## etappe_1918_raeumung spielt in den Wochen davor und weiß nichts über
## den Ausgang.

init 3 python:

    EREIGNISSE_ETAPPE_GRUPPE3 = [

        ## --------------------------------------- Gefangene und Besetzte

        ## Der Anfang: Im Herbst 1914 kamen mehr Gefangene, als irgendwo
        ## vorgesehen war. Die Karte zeigt keinen Missstand, sondern eine
        ## Liste, auf der eine Zahl steht und kein Becher.
        Ereignis(
            "etappe_1914_gefangenenlager", [1914], "etappe",
            "Hinter dem Bahnhof ist über Nacht ein Lager entstanden: Pfähle, "
            "Draht, zwei Baracken. Die ersten dreihundert Gefangenen sitzen im "
            "Freien und warten auf Stroh. Es riecht nach nasser Erde und nach "
            "ungewaschenen Mänteln. Einer hält dir seinen Becher hin und sagt "
            "ein Wort, das du nicht verstehst. Auf deiner Liste steht die "
            "Zahl, nicht der Becher.",
            [
                Option(
                    "Wasser holen lassen",
                    "Du schickst zwei Mann mit Eimern zum Brunnen.",
                    "Es dauert eine Stunde, bis alle einmal getrunken haben. "
                    "Der Wachhabende sagt, dafür sei keine Zeit vorgesehen. Am "
                    "Draht steht danach niemand mehr und ruft.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": 1, "rueckhalt": 1}
                ),
                Option(
                    "Bei der Zahl bleiben",
                    "Du zählst ab, meldest die Zahl und gehst.",
                    "Die Meldung geht vor Mittag hinaus und stimmt genau. "
                    "Hinter dir wird noch eine Weile gerufen, dann nicht mehr. "
                    "Am Abend fällt dir ein, dass du den Becher gesehen hast.",
                    aenderungen={"aufmerksamkeit": -1, "rueckhalt": -1}
                ),
            ],
            ort="Gefangenenlager", gewicht=10,
            quelle={
                "kurz": "Kriegsgefangenenlager im ersten Kriegsherbst",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird eine Lagerakte oder ein Bericht "
                              "über die ersten Gefangenentransporte im ersten "
                              "Kriegsjahr. Solche Akten nennen Belegzahlen "
                              "und Baufortschritt, nicht die Tage, bevor die "
                              "Baracken standen.",
            }
        ),

        ## Auftrag Teil A.3a, erstes der beiden Pflichtereignisse. Die
        ## Vorschrift steht im Text selbst, damit die Spielerin sie kennt,
        ## bevor sie entscheidet. Wer den Bogen einhält, tut niemandem
        ## etwas an - und acht Leute bleiben trotzdem ohne.
        Ereignis(
            "etappe_gefangenenarbeit", [1915, 1916, 1917, 1918], "etappe",
            {
                1915: "Zwanzig Gefangene laden Schwellen von einem Waggon, und "
                      "du führst die Liste. Die Vorschrift verbietet Arbeit, "
                      "die dem Krieg dient. Der Bauleiter sagt, ein Bahndamm "
                      "sei kein Krieg. Es ist heiß, und seit dem Morgen gab es "
                      "einmal Wasser. Einer setzt sich hin, und der Posten "
                      "sieht zu dir herüber.",
                1917: "Die Gruppe arbeitet seit sechs Uhr am Gleis, und es "
                      "friert. Vier von ihnen haben keine Schuhe, sondern "
                      "Lappen um die Füße. Auf der Liste stehen zwanzig Namen "
                      "und zwanzig Tagessätze Brot. Im Magazin liegen zwölf "
                      "Portionen für heute. Der Posten sieht dich an und "
                      "wartet, wie du teilst.",
            },
            [
                Option(
                    "Etwas dazugeben",
                    "Du nimmst aus dem eigenen Bestand, was fehlt.",
                    "Es reicht für alle, wenn niemand nachzählt. In deinem "
                    "Buch steht am Abend eine Zahl, die nicht stimmt. Der "
                    "Posten sagt nichts und sieht auch nicht weg.",
                    aenderungen={"versorgung": -1, "aufmerksamkeit": 2, "rueckhalt": 1}
                ),
                Option(
                    "Nach Liste verfahren",
                    "Du hältst dich an das, was zugeteilt ist.",
                    "Acht bleiben ohne, und die Arbeit geht trotzdem weiter. "
                    "Der Bauleiter trägt am Abend dieselbe Stückzahl ein wie "
                    "gestern. Beim Zählen sieht dich niemand von ihnen an.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": -2}
                ),
            ],
            ort="Arbeitsstelle", kern=True, gewicht=11,
            quelle={
                "kurz": "Haager Landkriegsordnung, Artikel 6: Gefangenenarbeit",
                "voll": "Abkommen betreffend die Gesetze und Gebräuche des "
                        "Landkriegs, Den Haag 1907, Anlage, Artikel 6",
                "art": "gesetz",
                "einordnung": "Die Ordnung erlaubt es, Kriegsgefangene "
                              "arbeiten zu lassen, verbietet aber jede Arbeit "
                              "für die Kriegführung. Was als Arbeit für den "
                              "Krieg galt, legte in der Etappe der aus, der "
                              "die Arbeit brauchte.",
            }
        ),

        ## Auftrag Teil A.3a, zweites Pflichtereignis: die Deportationen
        ## aus Belgien im Winter 1916/17. Zwei Fassungen, weil die Sache
        ## zwei Seiten hat - das Aufrufen und die Rückkehr derer, die
        ## wiederkamen. Wer nicht wiederkam, steht in keiner Fassung; das
        ## Spiel behauptet nichts, was es nicht zeigen kann.
        Ereignis(
            "etappe_1916_verschleppt", [1916, 1917], "etappe",
            {
                1916: "Auf dem Marktplatz stehen die Männer des Ortes in "
                      "Reihen, und es schneit. Ein Offizier liest eine "
                      "Verordnung vor: Wer keine Arbeit nachweist, wird zur "
                      "Arbeit gebracht. Die Wagen für den Abtransport stehen "
                      "schon am Bahnhof. Du hältst die Liste und hakst ab, wer "
                      "aufgerufen wird. Eine Frau am Rand ruft einen Namen, "
                      "und der Mann dreht sich nicht um.",
                1917: "Die Verordnung gilt seit dem Winter nicht mehr, und die "
                      "ersten kommen zurück. Am Bahnsteig steigen Männer aus, "
                      "die vor vier Monaten von hier weggefahren sind. Zwei "
                      "von ihnen kannst du auf deiner Liste nicht finden. Der "
                      "Beamte sagt, dann seien sie eben nicht gefahren. "
                      "Draußen wartet jemand, der seit dem Morgen jeden Zug "
                      "ansieht.",
            },
            [
                Option(
                    "Die Liste ändern",
                    "Du schreibst etwas hinein, was nicht auf dem Bogen steht.",
                    "Der Bogen geht ab, und die Zahl stimmt trotzdem. Zwei "
                    "Wochen später nimmt ihn jemand noch einmal zur Hand und "
                    "liest langsam. Du weißt bis heute nicht, ob es geholfen "
                    "hat.",
                    hinweis="der Bogen wird noch einmal gelesen",
                    aenderungen={"aufmerksamkeit": 2, "rueckhalt": 1}
                ),
                Option(
                    "Den Bogen so lassen",
                    "Du trägst ein, was du siehst, und gibst ihn ab.",
                    "Am Abend ist der Bogen abgezeichnet und liegt in der "
                    "Mappe. Draußen steht niemand mehr, und es ist dunkel "
                    "geworden. Deine Hand ist kalt bis in das Gelenk.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1, "rueckhalt": -2}
                ),
            ],
            ort="Sammelstelle", gewicht=12,
            quelle={
                "kurz": "Zwangsarbeit im besetzten Belgien, Winter 1916/17",
                "voll": "Abkommen betreffend die Gesetze und Gebräuche des "
                        "Landkriegs, Den Haag 1907, Anlage, Artikel 52",
                "art": "gesetz",
                ## GEKÜRZT IN PAKET 6, SCHRITT 2. Der zweite Satz hatte 30
                ## Wörter. Die Karte gehört weder zu den front_- noch zu
                ## den heimat_-Ereignissen und wäre zwischen den beiden
                ## Schritten liegen geblieben (AUFGEFALLEN 47).
                "einordnung": "Artikel 52 erlaubt Dienste der Einwohner nur "
                              "für das Besatzungsheer. Der Einsatz gegen das "
                              "eigene Land ist verboten.",
                "vertiefung": "Zwischen Herbst 1916 und Februar 1917 wurden "
                              "dennoch rund sechzigtausend Menschen aus "
                              "Belgien nach Deutschland gebracht. Die Akten "
                              "nennen Zahlen und Verordnungen, nicht die "
                              "Plätze, auf denen aufgerufen wurde.",
            }
        ),

        ## Requisition: der Vorgang, bei dem das Heer nimmt und einen
        ## Schein dafür ausstellt. Der Schein ist der Kern der Karte - er
        ## macht die Sache rechtmäßig und bezahlt sie trotzdem nicht.
        Ereignis(
            "etappe_requisition", [1914, 1915, 1916, 1917], "etappe",
            {
                1914: "Der Hof liegt am Ortsrand, und der Stall riecht nach "
                      "warmem Vieh. Auf dem Bogen steht, was das Heer braucht: "
                      "Heu, Hafer, ein Pferd. Der Bauer versteht dich nicht "
                      "und zeigt auf die Kinder in der Tür. Du schreibst einen "
                      "Schein aus, den er nach dem Krieg einlösen kann. Auf "
                      "dem Papier steht ein Betrag, den heute niemand bezahlt.",
                1916: "Im Dorf ist der dritte Bogen in diesem Jahr "
                      "abzuarbeiten. Diesmal geht es um Kupfer: Kessel, "
                      "Türklinken, die Glocke der Kirche. Eine alte Frau hat "
                      "ihren Topf in den Brunnen gehängt. Der Dolmetscher sagt "
                      "es dir und sieht dabei zur Seite. Auf deiner Liste "
                      "fehlen noch elf Kilo.",
            },
            [
                Option(
                    "Den Bogen erfüllen",
                    "Du holst, was fehlt, damit die Zahl stimmt.",
                    "Am Abend ist der Wagen voll und der Bogen abgezeichnet. "
                    "Im Dorf spricht niemand mehr mit dir, sondern nur noch "
                    "mit dem Dolmetscher. Auf dem Rückweg trägst du den Geruch "
                    "des Stalls in der Jacke.",
                    aenderungen={"aufmerksamkeit": -1, "rueckhalt": -2}
                ),
                Option(
                    "Weniger aufschreiben",
                    "Du meldest, es sei nicht mehr da gewesen.",
                    "Der Bogen geht mit einer kleineren Zahl hinaus, und "
                    "niemand fragt sofort nach. Beim nächsten Mal kommt ein "
                    "anderer mit, der genauer hinsieht. Im Dorf legt dir "
                    "jemand Eier auf den Sitz.",
                    aenderungen={"versorgung": 1, "belastung": 1,
                                 "aufmerksamkeit": 2, "rueckhalt": 1}
                ),
            ],
            ort="Besetztes Dorf", gewicht=11,
            quelle={
                "kurz": "Requisitionen und Scheine im besetzten Gebiet",
                "voll": "Abkommen betreffend die Gesetze und Gebräuche des "
                        "Landkriegs, Den Haag 1907, Anlage, Artikel 52 und 53",
                "art": "gesetz",
                "einordnung": "Die Ordnung erlaubt Requisitionen für das "
                              "Besatzungsheer und verlangt, sie bar zu zahlen "
                              "oder zu bescheinigen. Was ein solcher Schein "
                              "nach dem Krieg wert war, steht in keinem "
                              "Artikel.",
            }
        ),

        ## ------------------------------------------------- Das Ende

        ## Die Grippe trifft unabhängig von jeder Entscheidung, wie schon
        ## in Abschnitt 10e festgelegt. Keine der beiden Optionen steckt
        ## an, und keine schützt: Es geht darum, ob man bleibt.
        Ereignis(
            "etappe_1918_grippe", [1918], "etappe",
            "In der Baracke liegen jetzt auch die, die gestern noch getragen "
            "haben. Die Grippe geht seit dem Sommer um und kommt in diesem "
            "Herbst wieder. Es riecht nach Essig, mit dem die Böden gewischt "
            "werden. Ein Arzt sagt, es helfe nichts, aber es beruhige die "
            "Leute. Auf dem Gang stehen zwei Bahren, für die kein Platz ist.",
            [
                Option(
                    "Die Nachtwache übernehmen",
                    "Du bleibst, obwohl deine Schicht vorbei ist.",
                    "Bis vier Uhr gehst du zwischen den Betten hin und her. "
                    "Zwei brauchen Wasser, einer nur jemanden, der dasteht. Am "
                    "Morgen tut dir der Rücken weh, und der Gang ist leer.",
                    aenderungen={"belastung": 2, "rueckhalt": 2}
                ),
                Option(
                    "In die Unterkunft gehen",
                    "Du gehst schlafen, weil deine Schicht vorbei ist.",
                    "Du schläfst sechs Stunden und wachst von den Wagen auf "
                    "dem Hof auf. In der Baracke hat in der Nacht jemand die "
                    "Bahren weggeräumt. Niemand sagt etwas dazu, und du fragst "
                    "nicht.",
                    aenderungen={"belastung": -1, "rueckhalt": -2}
                ),
            ],
            ## kern=True SEIT TEIL C, und zwar aus einer Messung. Ohne den
            ## Schalter war diese Karte die einzige im ganzen Bestand, die
            ## in 24000 Durchgängen NIE fiel. Der Grund liegt nicht an ihr:
            ## Der kurze Verlauf zieht ausschließlich Kernkarten, und der
            ## lange erreicht 1918 auf der Etappe nur in einem Durchgang
            ## von zweitausend. Eine Karte über den Herbst 1918, die im
            ## Unterrichtsverlauf nicht vorkommen kann, ist keine Karte.
            ort="Etappenlazarett", kern=True, gewicht=11,
            quelle={
                "kurz": "Die Grippe von 1918 in Lazaretten und Etappe",
                "voll": QUELLE_FEHLT,
                "art": "statistik",
                "einordnung": "Gesucht werden Krankenzahlen der "
                              "Sanitätsdienststellen aus dem Sommer und "
                              "Herbst des letzten Kriegsjahres. Sie zeigen, "
                              "wie viele erkrankten, nicht, wer nachts neben "
                              "den Betten stand.",
            }
        ),

        ## Der Kipppunkt des Jahresbogens 1918 für die Etappe: "Die
        ## Formation löst sich auf, bevor ein Befehl dazu eintrifft."
        ## Diese Karte zeigt den Tag davor, an dem der Befehl noch kommt
        ## und schon nicht mehr trägt. Kein Ausblick, kein Datum nach dem
        ## elften November.
        Ereignis(
            "etappe_1918_raeumung", [1918], "etappe",
            "Der Räumungsbefehl kommt am Morgen, und bis zum Abend soll das "
            "Magazin leer sein. Für alles ist kein Wagen da, und für die "
            "Hälfte auch nicht. Was bleibt, soll unbrauchbar gemacht werden, "
            "so steht es im Befehl. Vor dem Tor stehen Leute aus dem Ort und "
            "sehen zu. Es riecht nach Petroleum, seit die ersten Kisten offen "
            "sind.",
            [
                Option(
                    "Den Befehl ausführen",
                    "Was nicht mitkommt, wird übergossen und angezündet.",
                    "Der Hof brennt bis in die Nacht, und der Rauch steht über "
                    "dem Ort. Am Tor sagt niemand etwas, und alle bleiben "
                    "stehen. Deine Hände riechen noch am nächsten Tag danach.",
                    aenderungen={"belastung": 2, "aufmerksamkeit": -1, "rueckhalt": -2}
                ),
                Option(
                    "Das Tor öffnen",
                    "Du lässt herein, wer tragen kann.",
                    "In zwei Stunden ist das Magazin leer, und niemand hat "
                    "gezählt. Ein Offizier fragt später nach dem Verbleib und "
                    "schreibt deinen Namen auf. Auf dem Hof liegt Mehl, in dem "
                    "viele Fußabdrücke stehen.",
                    aenderungen={"versorgung": 1, "aufmerksamkeit": 2, "rueckhalt": 2}
                ),
            ],
            ort="Etappenort", kern=True, gewicht=12,
            quelle={
                "kurz": "Räumung der Etappe in den letzten Kriegswochen",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird ein Räumungsbefehl oder "
                              "Kriegstagebuch einer Etappenstelle aus den "
                              "letzten Kriegswochen. Er nennt Fristen und "
                              "Bestände, nicht das, was am Tor geschah.",
            }
        ),

    ]

    for _vorlage in EREIGNISSE_ETAPPE_GRUPPE3:
        if _vorlage.kennung not in EREIGNIS_INDEX:
            EREIGNISSE.append(_vorlage)
            EREIGNIS_INDEX[_vorlage.kennung] = _vorlage


    ############################################################################
    ## DREI WEGE AUS DER ERSCHÖPFUNG - Paket 6, Vorweg C
    ############################################################################
    ##
    ## AUFGEFALLEN 42, in Zahlen: Von allen Optionen, die auf einem Pfad
    ## gezogen werden können, senken die Erschöpfung
    ##
    ##   an der Front   24 Prozent
    ##   in der Heimat  21 Prozent
    ##   in der Etappe  13 Prozent
    ##
    ## Zugleich hat die Etappe mit 27 Prozent die BESTEN Wege gegen den
    ## Verdacht. Sie war also nicht ärmer als die anderen Pfade, sondern
    ## schief: Wer dort müde wurde, blieb müde. Nach dem Kürzen der
    ## Ziehungen (Vorweg B) lag der kurze Etappenverlauf bei kluger Wahl
    ## auf 73,9 Prozent gegen die geforderten 80, und der Zusammenbruch
    ## war mit 13 Prozent der häufigste harte Abbruch dieses Pfades.
    ##
    ## DAS IST KEIN FREIKAUFEN. Jede der drei Karten bietet Erholung an,
    ## und jede lässt dafür etwas anderes zurück: einen Platz, den ein
    ## anderer räumen muss, eine halbe Liste mit deinem Namen darunter,
    ## eine Woche, in der die Kameraden draußen weitermachen. Keine der
    ## drei belohnt gutes Benehmen, und keine ist erkennbar richtig.
    ##
    ## Alle drei tragen kern=True: Der kurze Verlauf zieht nur Kernkarten,
    ## und genau dort fehlte der Weg zurück.

    EREIGNISSE_ETAPPE_ERHOLUNG = [

        Ereignis(
            "etappe_innendienst", [1915, 1916, 1917, 1918], "etappe",
            "Der Verwundetenzug ist um vier Uhr früh abgefahren. Du stehst noch "
            "am Gleis, und die Hände zittern vom Tragen. Der Sanitätsfeldwebel "
            "sieht dich an und sagt: „Du gehst mir eine Woche in die "
            "Schreibstube.“ Es ist keine Bitte und kein Befehl. Drinnen ist "
            "geheizt, und draußen kommt der nächste Zug am Freitag.",
            [
                Option(
                    "Die Woche annehmen",
                    "Du setzt dich an den Tisch mit den Listen.",
                    "Sechs Tage lang schreibst du Namen ab und schläfst durch. "
                    "Am Freitag trägst du wieder, und es geht leichter. Auf dem "
                    "Bahnsteig fragt einer, ob es drinnen schön war.",
                    aenderungen={"belastung": -2, "aufmerksamkeit": 1, "rueckhalt": -1}
                ),
                Option(
                    "Draußen bleiben",
                    "Du sagst, ein anderer brauche es nötiger.",
                    "Am Freitag stehst du wieder am Gleis, und am Sonntag auch. "
                    "Deine Schultern werden nicht mehr locker. Der andere kommt "
                    "aus der Schreibstube zurück und nimmt dir die schwere Seite ab.",
                    aenderungen={"belastung": 1, "rueckhalt": 1}
                ),
            ],
            ort="Bahnhofslazarett", kern=True, gewicht=10,
            quelle={
                "kurz": "Innendienst und Schonung im Etappensanitätsdienst",
                "voll": QUELLE_FEHLT,
                "art": "erinnerung",
                "einordnung": "Gesucht werden Erinnerungen von Sanitätspersonal "
                              "an Zuteilung und Wechsel des Dienstes. Sie zeigen "
                              "einzelne Entscheidungen, nicht die Regel dahinter.",
            }
        ),

        Ereignis(
            "etappe_quartier", [1914, 1915, 1916, 1917, 1918], "etappe",
            {
                1914: "Das Quartieramt hat dich in ein Bauernhaus eingewiesen. "
                      "In der Stube steht ein Ofen, und es riecht nach warmem "
                      "Holz. Die Familie hat ihre Betten in die Küche geschoben "
                      "und sieht dich von dort an. Auf dem Tisch liegt der "
                      "Einweisungszettel mit deinem Namen.",
                1917: "Der Winter steht seit November im Zimmer. In der Kammer "
                      "neben der Küche ist ein Ofen, und dort schläft die alte "
                      "Frau, der das Haus gehört. Das Quartieramt hat die Kammer "
                      "auf dich geschrieben. Deine Finger sind seit vier Wochen "
                      "nicht richtig warm geworden.",
            },
            [
                Option(
                    "Die Kammer nehmen",
                    "Du legst deine Sachen neben den Ofen.",
                    "Nachts trocknen deine Stiefel zum ersten Mal seit Wochen. "
                    "Du schläfst durch und wachst ohne Kopfschmerzen auf. Im "
                    "Flur gehen sie an dir vorbei, ohne zu grüßen.",
                    aenderungen={"belastung": -2, "versorgung": 1, "rueckhalt": -2}
                ),
                Option(
                    "In der Scheune bleiben",
                    "Du sagst, die Kammer sei schon belegt.",
                    "Im Stroh ist es kalt, und morgens ist die Decke feucht. "
                    "Die Frau stellt dir ohne ein Wort heißes Wasser vor die "
                    "Tür. Nach drei Wochen hustest du, und der Husten bleibt.",
                    aenderungen={"belastung": 1, "rueckhalt": 1}
                ),
            ],
            ort="Quartier", kern=True, gewicht=10,
            quelle={
                "kurz": "Einquartierung im besetzten Gebiet",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Quartierlisten oder Beschwerden aus "
                              "dem Etappengebiet. Sie halten die Zuweisung fest "
                              "und nicht, wer danach in der Küche schlief.",
            }
        ),

        Ereignis(
            "etappe_abloesung", [1916, 1917, 1918], "etappe",
            "Die Ablösung ist seit sechs Wochen angekündigt, und heute steht sie "
            "im Hof. Es ist ein Mann aus Schlesien, und er kennt hier nichts. "
            "Auf deinem Tisch liegen zwei Listen, die niemand außer dir lesen "
            "kann. Der Zug in die Ruhestellung fährt um halb sechs.",
            [
                Option(
                    "Übergeben und fahren",
                    "Du erklärst ihm das Nötigste und packst.",
                    "Im Zug schläfst du sofort ein und wachst erst im Dunkeln "
                    "auf. Vierzehn Tage lang tut dir nichts weh. Drei Wochen "
                    "später fragt eine Dienststelle, wer die halbe Liste "
                    "unterschrieben hat.",
                    aenderungen={"belastung": -2, "aufmerksamkeit": 1}
                ),
                Option(
                    "Die Woche noch bleiben",
                    "Du arbeitest die Listen mit ihm zu Ende.",
                    "Ihr sitzt bis Mitternacht, und am Ende stimmt jede Spalte. "
                    "Der Zug fährt ohne dich, und der nächste geht erst Montag. "
                    "Beim Aufstehen wird dir schwarz vor Augen.",
                    aenderungen={"belastung": 2, "rueckhalt": 1}
                ),
            ],
            ort="Etappenkommandantur", kern=True, gewicht=10,
            quelle={
                "kurz": "Ablösung und Ruhestellung in der Etappe",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Kriegstagebücher einer "
                              "Etappenstelle mit Ablösung und Ruhestellung. Sie "
                              "nennen Termine und nicht, was die Übergabe "
                              "liegen ließ.",
            }
        ),

    ]

    for _vorlage in EREIGNISSE_ETAPPE_ERHOLUNG:
        if _vorlage.kennung not in EREIGNIS_INDEX:
            EREIGNISSE.append(_vorlage)
            EREIGNIS_INDEX[_vorlage.kennung] = _vorlage


    ## Auftrag Teil A.2: Reichen die Jahre der geliehenen Karten? ##############
    ##
    ## Fünf Ereignisse tragen "etappe" in der Pfadliste. Jedes einzeln
    ## nachgerechnet, nicht pauschal:
    ##
    ##   front_feldpost        1914 bis 1918. Vollständig, seit Abschnitt
    ##                         10c. Nichts nachzutragen.
    ##   front_urlaub          1915 bis 1918. 1914 bleibt bewusst weg:
    ##                         Regelmäßiger Heimaturlaub setzte erst 1915
    ##                         ein, im ersten Kriegsherbst gab es ihn nur
    ##                         vereinzelt.
    ##   front_1916_zaehlung   nur 1916, und das ist richtig. Der Erlass
    ##                         des Kriegsministeriums erging im Oktober
    ##                         1916 ein einziges Mal.
    ##   front_nachfrage       1915 bis 1918, nur_kette. Reicht ein Jahr
    ##                         über das späteste Jahr des ersten Glieds
    ##                         hinaus; die Kettenprobe ist ohne Befund.
    ##   heimat_lazarettzug    1915 bis 1918 - HIER FEHLT EIN JAHR.
    ##
    ## Lazarettzüge fuhren vom August 1914 an; die ersten trafen schon im
    ## September in deutschen Städten ein. Das Ereignis trägt keine
    ## Jahreszahl im Namen und ist damit ein wiederkehrender Vorgang wie
    ## die übrigen. 1914 kommt dazu, mit eigener Fassung: Der erste Zug
    ## ist kein Dienst, sondern ein Auflauf, und er kippt in dem
    ## Augenblick, in dem die Türen aufgehen.
    ##
    ## Die Karte gehört beiden Pfaden. 1914 wirkt deshalb auch in der
    ## Heimat, und dort auf die einzige Zeile, die auf 'knapp' stand.
    JAHRESAUSWEITUNG_PAKET5 = {

        "heimat_lazarettzug": {
            "jahre": [1914, 1915, 1916, 1917, 1918],
            "text": {
                1914: "Der erste Lazarettzug hält am Güterbahnhof, und der "
                      "halbe Ort ist da. Frauen verteilen Kaffee, jemand hat "
                      "Blumen mitgebracht. Dann gehen die Türen auf, und es "
                      "wird still auf dem Bahnsteig. Ein Sanitäter fragt, wer "
                      "mit anfassen kann.",
            },
        },

    }

    jahresausweitung_nachtragen(JAHRESAUSWEITUNG_PAKET5)


################################################################################
## 10g. Paket 5, Schritt 2: der Epilog 1919
################################################################################
##
## 1919 hatte auf keinem der drei Pfade ein Ereignis und auf keinem eine
## Einlage. Die Sackgassenprobe meldete durchgängig 100 Prozent
## Leerabbrüche. Das Jahr, in dem das Spiel seine Auswertung leisten
## soll, war leer.
##
## DIE DREI PFADE LAUFEN HIER ZUSAMMEN, und das ist kein Mangel an
## Erfindung, sondern die Sache selbst: Im Frühjahr 1919 ist niemand
## mehr an der Front und niemand mehr in der Etappe. Alle sind zu Hause,
## und was sie unterscheidet, ist nicht mehr der Ort, sondern das, was
## sie mitbringen. Deshalb tragen fünf der acht Karten alle drei Pfade;
## unterschieden wird über die Merkmale und über den Lebenslauf danach.
##
## ZWEI KARTEN SIND SPIEGELBILDER VONEINANDER. epilog_1919_heimkehr
## zeigt die Ankunft aus der Sicht dessen, der zurückkommt (Front und
## Etappe). epilog_1919_rueckkehrer zeigt dieselbe Ankunft aus der Sicht
## dessen, der geblieben ist und den Platz am Tisch inzwischen braucht
## (Heimat). Keine der beiden hat recht.
##
## KEIN AUSBLICK ÜBER DAS FRÜHJAHR 1919 HINAUS. Was 1920 oder später
## geschieht, steht im Lebenslauf und nicht in einer Karte. Insbesondere
## fällt hier kein Wort über die Dolchstoßlegende als Begriff - die
## Wirtshausszene zeigt sie als Behauptung eines Fremden am Tisch, und
## das ist der Unterschied.
##
## DER TON steht seit Paket 2 fest, an heimat_verfahren, der Fassung von
## 1919: Der Krieg ist vorbei, das Verfahren läuft weiter, im Amtszimmer
## riecht es nach kaltem Ofen. Kein Aufatmen, kein Zusammenbruch,
## sondern Papier, das weiterläuft.
##
## GRUPPE 1 VON 2 - ANKUNFT, AMT UND WERKTOR.

init 3 python:

    EREIGNISSE_1919_GRUPPE1 = [

        Ereignis(
            "epilog_1919_heimkehr", [1919], ["front", "etappe"],
            "Der Zug hält am Vormittag, und niemand steht auf dem Bahnsteig. "
            "Du trägst einen Mantel, der dem Heer gehört, und einen Sack. Zu "
            "Hause riecht das Treppenhaus wie immer und die Wohnung nicht. Am "
            "Tisch sitzt jemand, der bei deinem Weggehen ein Kind war. „Du "
            "bist größer, als ich dachte“, sagst du.",
            [
                ## Erzählen kostet und bringt, Schweigen schont und
                ## kostet. Umgekehrt wäre eine der beiden in BEIDEN
                ## Werten besser - Probe 4 meldet das als dominierte
                ## Option, und sie hat damit recht: Dann wäre es keine
                ## Wahl mehr.
                Option(
                    "Vom Krieg erzählen",
                    "Sie fragen, und du fängst an.",
                    "Du fängst beim Essen an und hörst erst nach Mitternacht "
                    "auf. Nicht alles davon wolltest du sagen. Am Morgen ist "
                    "jemand wach geblieben und sitzt noch am Tisch.",
                    aenderungen={"belastung": 1, "rueckhalt": 1}
                ),
                Option(
                    "Erst einmal nichts sagen",
                    "Du legst den Sack ab und setzt dich.",
                    "Du legst den Sack ab und schläfst vierzehn Stunden. "
                    "Niemand fragt nach, und das ist eine Erleichterung. Zwei "
                    "Wochen später redet ihr über die Kohlen und über sonst "
                    "nichts.",
                    aenderungen={"belastung": -1, "rueckhalt": -1}
                ),
            ],
            ort="Bahnhof", kern=True, gewicht=13,
            quelle={
                "kurz": "Heimkehr und Demobilmachung nach dem Waffenstillstand",
                "voll": QUELLE_FEHLT,
                "art": "erinnerung",
                "einordnung": "Gesucht werden Erinnerungen von Heimkehrern an "
                              "die ersten Tage zu Hause. Sie zeigen einzelne "
                              "Ankünfte, nicht wie viele Millionen in wenigen "
                              "Wochen zurückkamen.",
            }
        ),

        ## Die Gegenkarte. Wer geblieben ist, hat vier Jahre lang gelernt,
        ## wo das Geld herkommt - und muss den Platz jetzt wieder teilen.
        Ereignis(
            "epilog_1919_rueckkehrer", [1919], "heimat",
            "Er steht seit einer Stunde in der Küche, und es riecht nach "
            "nassem Mantel. Vier Jahre lang war sein Platz am Tisch der Platz "
            "für die Näharbeit. Du hast in dieser Zeit gelernt, wo das Geld "
            "herkommt. Jetzt fragt er, wo seine Papiere liegen, und du weißt "
            "es besser als er.",
            [
                Option(
                    "Ihm den Platz räumen",
                    "Du legst die Näharbeit auf die Fensterbank.",
                    "Er setzt sich, und es sieht aus wie früher. Die Näharbeit "
                    "machst du abends auf den Knien, und es geht langsamer. Im "
                    "Werk fragen sie nächste Woche, ob du weniger Stunden "
                    "nimmst.",
                    aenderungen={"versorgung": -1, "rueckhalt": 2}
                ),
                Option(
                    "Den Tisch behalten",
                    "Du sagst, du brauchst das Licht am Fenster.",
                    "Er nimmt den Stuhl an der Wand und sagt nichts dazu. Die "
                    "Näharbeit bringt weiter, was sie bringt. Beim Essen sitzt "
                    "ihr über Eck und nicht mehr gegenüber.",
                    aenderungen={"belastung": 1, "rueckhalt": -1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=13,
            quelle={
                "kurz": "Rückkehr der Männer und die Arbeit der Frauen",
                "voll": QUELLE_FEHLT,
                "art": "darstellung",
                "einordnung": "Gesucht wird eine Darstellung zur "
                              "Demobilmachung und zur Verdrängung der Frauen "
                              "aus bezahlter Arbeit. Sie zeigt Verordnungen "
                              "und Zahlen, nicht die Verhandlung am "
                              "Küchentisch.",
            }
        ),

        Ereignis(
            "epilog_1919_versorgungsamt", [1919], "beide",
            "Im Flur des Versorgungsamts riecht es nach nassen Mänteln. Auf "
            "zwei Bänken sitzen dreißig Leute, und der Beamte ruft Nummern "
            "auf. Vor dir hat einer einen leeren Ärmel und einen Bogen in der "
            "Hand. Auf deinem Bogen steht, um wie viel deine Arbeitskraft "
            "gemindert sei. Die Antwort entscheidet über die Rente.",
            [
                Option(
                    "Alles angeben",
                    "Du schreibst auch das auf, was man nicht sieht.",
                    "Der Beamte liest, hebt den Kopf und liest noch einmal. Er "
                    "schreibt ein Wort dazu und ein Fragezeichen. Der Bescheid "
                    "kommt nach vier Monaten und nennt eine Nachuntersuchung "
                    "in einem Jahr.",
                    aenderungen={"versorgung": 1, "belastung": 1, "aufmerksamkeit": 1}
                ),
                Option(
                    "Nur das Sichtbare angeben",
                    "Du nennst, was ein Arzt in fünf Minuten findet.",
                    "Der Bogen geht ohne Rückfrage durch, und der Bescheid "
                    "kommt im Juni. Der Satz ist niedrig und dafür sicher. Was "
                    "nicht darin steht, fragt später niemand mehr.",
                    aenderungen={"belastung": -1, "rueckhalt": -1}
                ),
            ],
            ort="Versorgungsamt", kern=True, gewicht=13,
            quelle={
                "kurz": "Versorgungsamt und Rente der Kriegsbeschädigten",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht wird ein Rentenbescheid oder ein "
                              "ärztliches Gutachten eines Versorgungsamts aus "
                              "den ersten Nachkriegsjahren. Solche Akten "
                              "nennen einen Vomhundertsatz, nicht das, was "
                              "der Betroffene selbst spürte.",
            }
        ),

        ## Zwei Listen an einem Tor. Die Karte sagt nicht, welche die
        ## richtige ist; sie zeigt nur, dass beide dasselbe Papier sind.
        Ereignis(
            "epilog_1919_werktor", [1919], "beide",
            "Am Werktor hängen seit dem Morgen zwei Listen, und das Papier ist "
            "klamm. Auf der einen stehen die Namen derer, die wieder "
            "eingestellt werden. Auf der anderen stehen die, die gehen sollen. "
            "Es sind fast nur Frauennamen. Hinter dir sagt jemand: „Die haben "
            "doch vier Jahre gehalten.“",
            [
                Option(
                    "Den Namen nennen",
                    "Du sagst laut, wer vier Jahre die Halle getragen hat.",
                    "Zwei drehen sich um, einer nickt. Der Meister sagt, er "
                    "mache die Listen nicht. Am Freitag steht ein Name mehr "
                    "auf der linken Liste, und es ist nicht deiner.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": 1, "rueckhalt": 2}
                ),
                Option(
                    "Die eigene Zeile suchen",
                    "Du gehst näher heran und liest von oben nach unten.",
                    "Du findest dich auf der Liste, auf der du stehen wolltest. "
                    "Neben dir liest jemand die andere und geht ohne ein Wort. "
                    "Zu Hause sagst du, es sei geregelt worden.",
                    aenderungen={"versorgung": 1, "rueckhalt": -2}
                ),
            ],
            ort="Werktor", kern=True, gewicht=12,
            quelle={
                "kurz": "Demobilmachung und Entlassung der Frauen",
                "voll": QUELLE_FEHLT,
                "art": "gesetz",
                "einordnung": "Gesucht werden die Demobilmachungsverordnungen "
                              "aus dem Winter nach dem Waffenstillstand und "
                              "die Anweisungen der Betriebe dazu. Sie regeln "
                              "den Vorrang der Heimkehrer und sagen nichts "
                              "über die, die dafür gehen mussten.",
            }
        ),

    ]

    for _vorlage in EREIGNISSE_1919_GRUPPE1:
        if _vorlage.kennung not in EREIGNIS_INDEX:
            EREIGNISSE.append(_vorlage)
            EREIGNIS_INDEX[_vorlage.kennung] = _vorlage


## GRUPPE 2 VON 2 - WAHL, HUNGER, VERTRAG UND PAPIERE #########################
##
## Die vier öffentlichen Ereignisse des Jahres, und eines, das nur den
## Heimkehrer betrifft.
##
## KEIN ERZÄHLER ORDNET EIN. Bei der Wahl steht nirgends, dass Frauen
## zum ersten Mal wählen durften - es steht der Name der Nachbarin auf
## der Liste. Beim Vertrag steht keine Bewertung, sondern eine Zeitung
## im Schaukasten und eine Trauerfahne an der Kirche. Wer diese Karten
## später ändert, hält das ein: Der Widerspruch entsteht im Kopf der
## Spielerin, nicht in einem Satz des Spiels.

init 3 python:

    EREIGNISSE_1919_GRUPPE2 = [

        Ereignis(
            "epilog_1919_wahl", [1919], "beide",
            "Im Schulhaus stehen Tische mit Urnen, und es riecht nach Kreide. "
            "Zum ersten Mal steht auf der Liste auch der Name deiner "
            "Nachbarin. Ein alter Mann erklärt jedem, wo der Zettel "
            "hineingefaltet wird. Vor dir zählt eine Frau die Kästchen zweimal "
            "durch. „Ich will nichts falsch machen“, sagt sie.",
            [
                Option(
                    "Wählen gehen",
                    "Du stellst dich an und nimmst einen Zettel.",
                    "Du faltest den Zettel und wirfst ihn ein, und es dauert "
                    "vier Sekunden. Draußen stehen mehr Leute als sonst an "
                    "einem Sonntag. Am Abend hängt vor der Zeitung eine Tafel "
                    "mit Zahlen.",
                    aenderungen={"rueckhalt": 1}
                ),
                Option(
                    "Nicht hingehen",
                    "Du hast an diesem Sonntag anderes vor.",
                    "Du holst Kohlen und stehst dafür zwei Stunden an. Am "
                    "Abend fragt die Nachbarin, ob du da warst, und du sagst "
                    "ja. Es ist die erste Lüge seit langem, und sie ist klein.",
                    aenderungen={"versorgung": 1, "rueckhalt": -1}
                ),
            ],
            ort="Wahllokal", kern=True, gewicht=12,
            quelle={
                "kurz": "Wahl zur Nationalversammlung am 19. Januar 1919",
                "voll": QUELLE_FEHLT,
                "art": "statistik",
                "einordnung": "Gesucht wird die amtliche Wahlstatistik zur "
                              "Nationalversammlung mit der Beteiligung von "
                              "Frauen und Männern. Sie nennt Stimmen und "
                              "Bezirke, nicht das, was jemand beim Falten des "
                              "Zettels dachte.",
            }
        ),

        ## Der Waffenstillstand hat den Hunger nicht beendet. Die Blockade
        ## lief bis in den Sommer 1919 weiter; begrenzte Einfuhren wurden
        ## erst im Fruehjahr zugelassen. Genau diese Luecke zeigt die Karte.
        Ereignis(
            "epilog_1919_blockade", [1919], "beide",
            "Der Krieg ist seit drei Monaten vorbei, und die Zuteilung ist "
            "dieselbe. Auf dem Anschlag steht, dass Schiffe mit Mehl unterwegs "
            "sind. Darunter hat jemand mit Bleistift geschrieben, seit wann "
            "das dort steht. In der Schlange hustet die halbe Reihe. Eine Frau "
            "sagt, ihr Jüngster wiege weniger als im Herbst.",
            [
                Option(
                    "Anstehen wie immer",
                    "Du bleibst und wartest, bis der Laden aufmacht.",
                    "Nach zwei Stunden gibt es eine halbe Ration und einen "
                    "Zettel für Freitag. Es ist wenig und es ist sicher. Zu "
                    "Hause sagst du, es werde besser, weil die Schiffe kommen.",
                    aenderungen={"versorgung": 1}
                ),
                Option(
                    "Zum Bauern hinausfahren",
                    "Der Zug um halb fünf fährt noch immer.",
                    "Der Hof nimmt kein Geld und auch keine Bettwäsche mehr. "
                    "Für zwei Pfund Speck gibst du den Mantel her, den du am "
                    "wenigsten brauchst. An der Sperre steht niemand, und das "
                    "ist neu.",
                    aenderungen={"versorgung": 2, "belastung": 2, "rueckhalt": -1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=13,
            quelle={
                "kurz": "Seeblockade bis zum Sommer 1919 und der Hunger danach",
                "voll": QUELLE_FEHLT,
                "art": "statistik",
                "einordnung": "Gesucht werden Zahlen zur Ernährungslage "
                              "zwischen dem Waffenstillstand und der Aufhebung "
                              "der Blockade im Sommer. Sie zeigen Zuteilungen "
                              "und Sterblichkeit, nicht die Zettel an den "
                              "Läden.",
            }
        ),

        Ereignis(
            "epilog_1919_vertrag", [1919], "beide",
            "Im Mai hängt die Zeitung im Schaukasten, und vor dem Kasten "
            "stehen zwanzig Leute. Die Bedingungen stehen in Spalten, und "
            "keiner liest sie zu Ende. Ein Mann liest halblaut vor und wird "
            "immer leiser. Neben dir sagt jemand, so etwas unterschreibe "
            "niemand. Am Abend hängt an der Kirche eine Trauerfahne.",
            [
                Option(
                    "Zu Ende lesen",
                    "Du bleibst stehen und liest jede Spalte.",
                    "Du liest bis zu der Zeile über die Schuld und liest sie "
                    "zweimal. Danach liest du weiter, bis die Spalten "
                    "aufhören. Auf dem Rückweg gehst du langsamer als sonst.",
                    aenderungen={"belastung": 1, "aufmerksamkeit": -1}
                ),
                Option(
                    "Weitergehen",
                    "Du hast gesehen, was du sehen wolltest.",
                    "Du gehst und hörst hinter dir, wie einer lauter wird. Am "
                    "Abend erzählen sie zu Hause drei Fassungen davon. Du "
                    "sagst zu keiner etwas.",
                    aenderungen={"rueckhalt": -1}
                ),
            ],
            ort="Wohnviertel", kern=True, gewicht=13,
            quelle={
                "kurz": "Die Bedingungen des Vertrags im Frühjahr 1919",
                "voll": QUELLE_FEHLT,
                "art": "zeitung",
                "einordnung": "Gesucht werden Zeitungsausgaben aus den Tagen, "
                              "in denen die Bedingungen bekannt wurden. Sie "
                              "zeigen die Empörung der Blätter, nicht das, was "
                              "einzelne Leser davon behielten.",
            }
        ),

        Ereignis(
            "epilog_1919_papiere", [1919], ["front", "etappe"],
            "Auf dem Amt riecht es nach Bohnerwachs, und die Bank vor dem "
            "Schalter ist voll. Der Beamte fragt nach Truppenteil, "
            "Entlassungsort und letztem Sold. Deine Papiere sind vollständig "
            "bis auf ein Blatt. Es fehlt der Nachweis über die Zeit, in der du "
            "krank warst. Ohne ihn zählt der Monat nicht.",
            [
                Option(
                    "Das Blatt beschaffen",
                    "Du fährst zurück und suchst die Dienststelle.",
                    "Die Dienststelle gibt es nicht mehr, ihre Akten liegen in "
                    "einer Turnhalle. Nach zwei Tagen hast du eine "
                    "Bescheinigung mit zwei Stempeln. Der Monat zählt jetzt, "
                    "und du hast drei Mark dafür ausgegeben.",
                    aenderungen={"versorgung": 1, "belastung": 2}
                ),
                Option(
                    "Ohne das Blatt abgeben",
                    "Du legst hin, was du hast, und unterschreibst.",
                    "Der Beamte hakt ab und schreibt an den Rand ein Wort. Der "
                    "Monat fällt heraus, und mit ihm der Sold dafür. In deiner "
                    "Akte steht ab jetzt eine Lücke, die niemand mehr füllt.",
                    aenderungen={"aufmerksamkeit": 1, "rueckhalt": -1}
                ),
            ],
            ort="Meldebehörde", kern=True, gewicht=12,
            quelle={
                "kurz": "Entlassungsschein, Meldepflicht und Nachweise",
                "voll": QUELLE_FEHLT,
                "art": "akte",
                "einordnung": "Gesucht werden Entlassungspapiere eines "
                              "Heimkehrers samt den Nachweisen, die das Amt "
                              "verlangte. Sie zeigen, was verlangt wurde, "
                              "nicht wie lange die Beschaffung dauerte.",
            }
        ),

    ]

    for _vorlage in EREIGNISSE_1919_GRUPPE2:
        if _vorlage.kennung not in EREIGNIS_INDEX:
            EREIGNISSE.append(_vorlage)
            EREIGNIS_INDEX[_vorlage.kennung] = _vorlage


## DIE WAHL AM WIRTSHAUSTISCH #################################################
##
## Die Szene selbst steht in dialoge.rpy. Hier steht nur die Wahl, und
## sie ist die einzige Karte des Spiels mit DREI Optionen. Der Bildschirm
## trägt das ohne Änderung: Drei Karten zu 520 Punkten und zwei Abstände
## zu 80 ergeben 1720 von 1920.
##
## nur_kette=True, damit sie in keiner Ziehung auftaucht. Gerufen wird
## sie ausschliesslich aus dem Ablauf vor dem Lebenslauf.
##
## KEINE DER DREI OPTIONEN VERÄNDERT EINEN WERT, und das ist die
## wichtigste Entscheidung an dieser Karte.
##
## Der Auftrag verlangt, dass keine Option sichtbar belohnt wird. Die
## Entscheidungskarte zeigt die angekündigten Wertänderungen an - jede
## Zahl dort wäre also eine Empfehlung. Und sie wäre auch eine
## Behauptung: dass Widersprechen etwas kostet oder Zustimmen etwas
## einbringt. Beides weiss das Spiel nicht.
##
## Dazu kommt der Ort im Ablauf. Nach dieser Karte folgt kein Kapitel
## mehr, in dem ein Wert noch etwas täte. Eine Zahl hier wäre Theater.
##
## Was die Wahl wirklich trägt, ist das Merkmal und sein Nachklang im
## Lebenslauf. Dort steht dann, was aus dem Satz geworden ist - ohne
## Urteil, in allen drei Fällen.

init 3 python:

    WIRTSHAUS_WAHL = Ereignis(
        "wirtshaus_wahl", [1919], "beide",
        "Der Satz steht im Raum, und alle warten. Dein Glas ist leer, und der "
        "Wirt sieht her. Was du jetzt sagst, hören vier Leute, die dich "
        "kennen.",
        [
            Option(
                "Widersprechen",
                "Du sagst, was du selbst gesehen hast.",
                "Du erzählst von einem einzigen Tag, nicht vom Krieg. Der "
                "Fremde hört zu und wartet, bis du fertig bist. Dann sagt er, "
                "das sei ja nur deine Erfahrung. Zwei am Tisch geben dir "
                "recht, einer steht auf und geht. Am Sonntag darauf grüßt "
                "dich der, der gegangen ist, nicht mehr.",
                merkmale=["wirtshaus_widersprochen"]
            ),
            Option(
                "Schweigen",
                "Du trinkst aus und sagst nichts.",
                "Du siehst auf den Tisch, bis jemand anderes weiterredet. Der "
                "Fremde nimmt das für Zustimmung und wird lauter. Auf dem "
                "Heimweg fällt dir ein, was du hättest sagen können. Du sagst "
                "es der leeren Straße, zweimal. Am nächsten Tag weiß niemand, "
                "dass du dabei warst.",
                merkmale=["wirtshaus_geschwiegen"]
            ),
            Option(
                "Zustimmen",
                "Du nickst und sagst, so werde es gewesen sein.",
                "Der Fremde schlägt dir auf die Schulter und bestellt eine "
                "Runde. Am Tisch wird es lauter und einfacher. Der Satz ist "
                "von jetzt an auch deiner, und er kostet nichts. Zwei Wochen "
                "später hörst du ihn von jemandem, der ihn von dir hat. Du "
                "widersprichst auch dann nicht.",
                merkmale=["wirtshaus_zugestimmt"]
            ),
        ],
        ort="Wirtshaus", kern=True, nur_kette=True,
        quelle={
            "kurz": "Die Behauptung vom unbesiegten Heer, ab November 1918",
            "voll": QUELLE_FEHLT,
            "art": "zeitung",
            "einordnung": "Gesucht werden Zeitungen und Reden aus dem Winter "
                          "nach dem Waffenstillstand, in denen die Behauptung "
                          "zuerst umläuft. Sie zeigen, wer sie verbreitete, "
                          "nicht wie sie an einen Wirtshaustisch kam.",
        }
    )

    if "wirtshaus_wahl" not in EREIGNIS_INDEX:
        EREIGNISSE.append(WIRTSHAUS_WAHL)
        EREIGNIS_INDEX["wirtshaus_wahl"] = WIRTSHAUS_WAHL


## Der Übergang zum Lebenslauf ################################################
##
## Teil D des Auftrags. Der Weg dorthin lief bisher so:
##
##   kapitelwechsel  -> naechstes_kapitel(1919) ist None
##                   -> jump ende_ueberlebt
##                   -> jump ende_lebenslauf
##
## ende_ueberlebt war die einzige Marke im ganzen Ablauf, die JEDER
## Durchgang durchläuft, der den Epilog übersteht - und sie war noch
## nicht umgeleitet. Deshalb hängt die Wirtshausszene genau dort und
## nirgends sonst. Wer hier etwas ändert, prüft zuerst, ob dieselbe
## Marke schon umgeleitet wird; die fünf bestehenden Umleitungen stehen
## im Kopf dieses Pakets.

init 1 python:

    config.label_overrides["ende_ueberlebt"] = "ende_ueberlebt_mit_wirtshaus"


label ende_ueberlebt_mit_wirtshaus:

    ## Erst die Szene, dann die Wahl. Die Szene endet damit, dass alle
    ## zu dir sehen; die Karte stellt genau diese Frage.
    call szene_spielen("wirtshaus_1919")

    call ereignis_spielen("wirtshaus_wahl")

    jump ende_lebenslauf


################################################################################
## 11. Zustandsvariablen
################################################################################

default letzte_kapitelwirkung = {}
default endergebnis = None

## Seit Paket 3, Vorweg: die Verjährung des Verdachts.
## verdacht_ruhig zählt die Ziehungen ohne Zuwachs, verdacht_stand hält
## den Wert bei der letzten Ziehung fest.
default verdacht_ruhig = 0
default verdacht_stand = 0
default bestandszeilen = []
default nachhallzeilen = []


################################################################################
## 12. Stile
################################################################################

init offset = -1

style jahr_zeitraum is default:
    size 22
    color FARBE_TINTE_MATT
    kerning 1.5
    text_align 0.5

style jahr_stichwort is default:
    size 20
    color FARBE_LINIE
    kerning 1.8

## Seit Paket 3, Schritt 2: die Frage des Jahres auf der Jahreskarte.
## Größer als der Einführungstext, aber nicht als die Jahreszahl - sie ist
## die Überschrift über das, was gleich kommt, nicht die Überschrift des
## Kapitels.
style jahr_frage is default:
    font SCHRIFT_TITEL
    size 30
    color FARBE_AKZENT
    text_align 0.5
    line_spacing 6

## Der Kipppunkt im Jahresabschluss. Ruhig, kein Ausrufezeichen.
style jahr_kippt is default:
    size 24
    color FARBE_TINTE
    text_align 0.5
    line_spacing 6

style jahr_wirkung_titel is default:
    font SCHRIFT_TITEL
    size 20
    bold True
    color FARBE_TINTE_MATT
    kerning 2.0

style jahr_wirkung_name is default:
    font SCHRIFT_TITEL
    size 23
    bold True
    color FARBE_TINTE

style jahr_wirkung_richtung is default:
    size 22
    color FARBE_AKZENT

style jahr_lehrplan is default:
    size 19
    italic True
    color FARBE_LINIE
    line_spacing 4

style rueckblick_titel is default:
    font SCHRIFT_TITEL
    size 34
    bold True
    color FARBE_TINTE
    text_align 0.5

style lebensweg_marke is default:
    font SCHRIFT_TITEL
    size 21
    bold True
    color FARBE_AKZENT_MATT
    kerning 1.5

style lebensweg_text is default:
    size 22
    color FARBE_TEXT_HELL
    line_spacing 7

style lebensweg_quelle is default:
    size 17
    italic True
    color FARBE_LINIE

style ende_deutung is default:
    font SCHRIFT_TITEL
    size 28
    color FARBE_TEXT_HELL
    line_spacing 9
    text_align 0.5
    layout "subtitle"

style probe_kopf is default:
    font SCHRIFT_TITEL
    size 20
    bold True
    color FARBE_TINTE
    kerning 1.4

style probe_zeile is default:
    size 20
    color FARBE_TINTE_MATT

style probe_fehlt is default:
    size 20
    bold True
    color FARBE_FEHLEND

## Seit Paket 2, Schritt 1: die mittlere Stufe der Bestandslage. Nicht rot,
## weil nichts kaputt ist, aber deutlich genug, um sie zu finden.
style probe_knapp is default:
    size 20
    color FARBE_AKZENT_MATT

init offset = 0


################################################################################
## 13. Bildschirme
################################################################################
##
## Alle Bildschirme werden ausschließlich mit der Maus bedient. Es gibt
## keine key-Anweisung in dieser Datei.

## Jahreskarte ###############################################################
##
## Der einzige Kapitelbildschirm des Spiels. Seit Paket 3 hat er den
## früheren kapitelkarte aus screens.rpy abgelöst; der ist am
## 5. September 2026 gelöscht worden (Entscheidung 19). Er zeigt Jahr,
## Zeitraum, Überschrift, Einführungstext, die Frage des Jahres, drei
## Stichworte und, ab dem zweiten Kapitel, was der Jahreswechsel an den
## Werten verändert hat.

screen jahreskarte(jahr, wirkung=None):

    $ kapitelnummer = KAPITEL_JAHRE.index(jahr) + 1 if jahr in KAPITEL_JAHRE else 1
    $ zeilen = wirkung_zeilen(wirkung) if wirkung else []
    $ ist_epilog = (jahr == EPILOG_JAHR)

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    ## Paket 7, Schritt 1: Das Jahresblatt kommt von oben. Ein
    ## Kapitelwechsel darf nach den Animationsregeln länger dauern als eine
    ## Handbewegung - 0,8 statt 0,45 Sekunden.
    frame:
        align (0.5, 0.5)
        xsize 1420
        padding (90, 54)
        background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)
        at kalenderblatt(bewegungszeit(0.5))

        vbox:
            xsize 1240
            spacing 12

            text ("Epilog" if ist_epilog else "Kapitel " + str(kapitelnummer) + " von " + str(len(KAPITEL_JAHRE))) style "kapitel_marke" xalign 0.5

            text str(jahr) style "kapitel_jahr" size 112 xalign 0.5

            text KAPITEL_ZEITRAUM.get(jahr, "") style "jahr_zeitraum" xalign 0.5

            add Solid(FARBE_AKZENT, xsize=300, ysize=3) xalign 0.5

            text KAPITEL_UEBERSCHRIFT.get(jahr, "") style "abschnitt_titel" size 40 xalign 0.5 xsize 1240

            text KAPITEL_TEXT.get(jahr, "") style "abschnitt_text" size 25 xalign 0.5 xsize 1100

            ## Seit Paket 3, Schritt 2: die Frage des Jahres. Sie steht
            ## zwischen dem Einführungstext und den Stichworten, ruhig
            ## gesetzt und ohne Antwort daneben.
            $ bogen = kapitel_bogen(jahr, aktueller_pfad)

            if bogen["frage"]:

                null height 6

                text bogen["frage"] style "jahr_frage" xalign 0.5 xsize 1100

            hbox:
                xalign 0.5
                spacing 22

                for stichwort in KAPITEL_STICHWORTE.get(jahr, []):
                    text stichwort style "jahr_stichwort"

            if zeilen:

                null height 4

                frame:
                    xalign 0.5
                    xsize 1000
                    padding (30, 20)
                    background rahmen_oben(FARBE_PAPIER_DUNKEL, FARBE_LINIE_FEIN, 2)

                    vbox:
                        xsize 940
                        spacing 10

                        text "Was sich mit dem Jahreswechsel ändert" style "jahr_wirkung_titel" xalign 0.5

                        text KAPITEL_WIRKUNG_TEXT.get(jahr, "") style "abschnitt_text" size 22 xalign 0.5 xsize 940

                        hbox:
                            xalign 0.5
                            spacing 40

                            for zeile in zeilen:
                                hbox:
                                    spacing 8
                                    text zeile["name"] style "jahr_wirkung_name" yalign 0.5
                                    text zeile["richtung"] style "jahr_wirkung_richtung" color (FARBE_AKZENT if zeile["schlechter"] else FARBEN_STUFE[0]) yalign 0.5

            if persistent.analysemodus:

                null height 2

                vbox:
                    xalign 0.5
                    xsize 1100
                    spacing 4

                    text KAPITEL_LEHRPLAN.get(jahr, "") style "jahr_lehrplan" xalign 0.5 xsize 1100

                    $ zahl_frei, zahl_bedingt = bestand_zaehlen(jahr, aktueller_pfad, spielmodus)
                    text ("Bestand auf diesem Pfad: " + str(zahl_frei) + " frei ziehbar, " + str(zahl_bedingt) + " an Merkmale gebunden. Vorgesehen sind " + str(ziehungen_pro_kapitel(jahr)) + " Ziehungen.") style "jahr_lehrplan" xalign 0.5 xsize 1100

            null height 14

            textbutton ("Den Epilog beginnen" if ist_epilog else "Weiter"):
                xalign 0.5
                style_prefix "weiter"
                action Return()
                at knopf_hebt(bewegungszeit(0.12))


## Jahresabschluss ###########################################################

screen jahresabschluss(jahr):

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    frame:
        align (0.5, 0.5)
        xsize 1240
        padding (84, 60)
        background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)
        at kalenderblatt(bewegungszeit(0.5))

        vbox:
            xsize 1072
            spacing 18

            text "Ende des Jahres" style "kapitel_marke" xalign 0.5

            text str(jahr) style "rueckblick_titel" size 56 xalign 0.5

            add Solid(FARBE_LINIE_FEIN, xsize=1072, ysize=1)

            text KAPITEL_RUECKBLICK.get(jahr, "") style "abschnitt_text" size 25 xalign 0.5 xsize 1000

            ## Seit Paket 3, Schritt 2: der Kipppunkt des Jahres. Was hier
            ## steht, gilt unabhängig davon, wie gewählt wurde - deshalb
            ## steht es im Rückblick und nicht in einem Ausgang.
            $ bogen = kapitel_bogen(jahr, aktueller_pfad)

            if bogen["kippt"]:

                add Solid(FARBE_LINIE_FEIN, xsize=1072, ysize=1)

                text bogen["kippt"] style "jahr_kippt" xalign 0.5 xsize 1000

            add Solid(FARBE_LINIE_FEIN, xsize=1072, ysize=1)

            text zustandssatz_text() style "abschnitt_text" size 24 italic True xalign 0.5 xsize 1000

            if persistent.analysemodus:
                text ("Gespielt: " + str(ziehungen_im_kapitel) + " von " + str(ziehungen_pro_kapitel(jahr)) + " vorgesehenen Ziehungen.") style "jahr_lehrplan" xalign 0.5

            null height 10

            textbutton "Weiter":
                xalign 0.5
                style_prefix "weiter"
                action Return()
                at knopf_hebt(bewegungszeit(0.12))


## Lebenslauf: der dynamische Schluss ########################################

screen ende_lebenslauf_bildschirm(daten):

    add Solid(FARBE_DUNKEL)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xalign 0.5
        ypos 54
        xsize 1700
        spacing 14

        text "Ende des Durchgangs" style "ende_marke" xalign 0.5

        text daten["titel"] style "ende_titel" size 50 xalign 0.5 xsize 1700

        add Solid(FARBE_AKZENT, xsize=300, ysize=3) xalign 0.5

        text daten["deutung"] style "ende_deutung" xalign 0.5 xsize 1300

        null height 6

        hbox:
            xalign 0.5
            spacing 34

            ## Linke Spalte: wer du warst und wie es dir am Ende geht.
            vbox:
                xsize 600
                spacing 16

                frame:
                    xsize 600
                    padding (26, 22)
                    background rahmen(FARBE_DUNKEL_HELL, FARBE_LINIE, 2)

                    vbox:
                        xsize 548
                        spacing 10

                        text "Wer du gewesen bist" style "ende_bilanz_titel"

                        add Solid(FARBE_LINIE, xsize=548, ysize=1)

                        text lebenslauf_text() style "ende_bilanz" xsize 548

                frame:
                    xsize 600
                    padding (26, 22)
                    background rahmen(FARBE_DUNKEL_HELL, FARBE_LINIE, 2)

                    vbox:
                        xsize 548
                        spacing 12

                        text "Wie es dir am Ende geht" style "ende_bilanz_titel"

                        add Solid(FARBE_LINIE, xsize=548, ysize=1)

                        for eintrag in auswertung_liste():

                            vbox:
                                xsize 548
                                spacing 3

                                hbox:
                                    spacing 12

                                    text eintrag["name"] style "ende_wert_name" size 21 xsize 150 yalign 0.5

                                    hbox:
                                        spacing 4
                                        yalign 0.5
                                        for feld in range(SEGMENTE_JE_BALKEN):
                                            if segment_gefuellt(feld, eintrag["stufe"]):
                                                add Solid(FARBEN_STUFE_HELL[eintrag["stufe"]], xsize=22, ysize=9)
                                            else:
                                                add Solid(FARBE_SEGMENT_DUNKEL, xsize=22, ysize=9)

                                    text eintrag["stufenname"] style "ende_wert_stufe" size 21 color FARBEN_STUFE_HELL[eintrag["stufe"]] yalign 0.5

            ## Rechte Spalte: der Lebensweg nach dem Krieg.
            frame:
                xsize 1066
                padding (30, 24)
                background rahmen(FARBE_DUNKEL_HELL, FARBE_LINIE, 2)

                vbox:
                    xsize 1006
                    spacing 12

                    text "Was danach aus dir wird" style "ende_bilanz_titel"

                    add Solid(FARBE_LINIE, xsize=1006, ysize=1)

                    ## Die Zeitleiste ist der didaktische Ertrag des
                    ## Durchgangs. Sie bekommt deshalb die Höhe, die
                    ## übrig bleibt. Bei sechs Einträgen wird gescrollt;
                    ## Rad und Ziehen genügen dafür, eine Taste ist
                    ## nirgends nötig.
                    viewport:
                        xsize 1006
                        ysize 540
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        vbox:
                            xsize 962
                            spacing 16

                            for eintrag in daten["eintraege"]:

                                vbox:
                                    xsize 962
                                    spacing 5

                                    hbox:
                                        spacing 14
                                        text eintrag["marke"] style "lebensweg_marke" yalign 0.5
                                        if persistent.analysemodus:
                                            text eintrag["quelle"] style "lebensweg_quelle" yalign 0.5

                                    text eintrag["text"] style "lebensweg_text" xsize 962

        null height 8

        text daten["fazit"] style "ende_fazit" xalign 0.5 xsize 1400

        if persistent.analysemodus:
            text ("Ausgang: " + daten["kennung"] + "  |  " + daten["lehrplan"]) style "lebensweg_quelle" xalign 0.5 xsize 1400

        null height 10

        hbox:
            xalign 0.5
            spacing 40
            style_prefix "dunkel"

            textbutton "Von vorn beginnen" action Return("neustart")
            textbutton "Hauptmenü" action MainMenu(confirm=False)
            textbutton "Beenden" action Quit(confirm=True)


## Bestandsprobe (Werkzeug für die Entwicklung) ###############################

screen bestandsprobe_anzeige(zeilen, nachhall):

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xpos 110
        ypos 50
        xsize 1740
        spacing 12

        text "Bestandsprobe" style "abschnitt_titel" size 44 text_align 0.0 xalign 0.0

        add Solid(FARBE_AKZENT, xsize=220, ysize=3)

        text ("Soll: vorgesehene Ziehungen. Frei: Ereignisse ohne Merkmalsbedingung. Gebunden: nur mit passenden Merkmalen erreichbar. Lage: Unterdeckung heißt frei unter Soll, knapp heißt weniger als " + str(BESTAND_RESERVE) + " Ereignisse Reserve über dem Soll. Kurzer Verlauf: " + str(ziehungen_summe("kurz")) + " Ziehungen in den Kriegsjahren. Langer Verlauf: " + str(ziehungen_summe("lang")) + ".") style "abschnitt_text" size 21 text_align 0.0 xalign 0.0 xsize 1740

        ## Seit Paket 2, Schritt 1: Die Zahl steht oben. Wer die Probe
        ## öffnet, will zuerst wissen, wie schlimm es ist, und erst danach,
        ## wo genau.
        $ lagesumme = bestandslage_summe(zeilen)

        hbox:
            spacing 24

            text ("Unterdeckung: " + str(lagesumme["unterdeckung"])) style ("probe_fehlt" if lagesumme["unterdeckung"] else "probe_zeile") size 24
            text ("knapp: " + str(lagesumme["knapp"])) style ("probe_knapp" if lagesumme["knapp"] else "probe_zeile") size 24
            text ("in Ordnung: " + str(lagesumme["ordnung"])) style "probe_zeile" size 24
            text ("von " + str(len(zeilen)) + " Zeilen") style "probe_zeile" size 24

        hbox:
            spacing 30

            frame:
                xsize 1000
                ysize 780
                padding (24, 20)
                background rahmen(FARBE_PAPIER_HELL, FARBE_LINIE_FEIN, 2)

                vbox:
                    spacing 8

                    hbox:
                        spacing 0
                        text "Verlauf" style "probe_kopf" xsize 170
                        text "Jahr" style "probe_kopf" xsize 80
                        text "Pfad" style "probe_kopf" xsize 190
                        text "Soll" style "probe_kopf" xsize 70
                        text "Frei" style "probe_kopf" xsize 70
                        text "Gebunden" style "probe_kopf" xsize 110
                        text "Lage" style "probe_kopf" xsize 200

                    add Solid(FARBE_LINIE_FEIN, xsize=940, ysize=1)

                    viewport:
                        xsize 940
                        ysize 690
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        vbox:
                            spacing 4

                            for zeile in zeilen:

                                ## Die ganze Zeile trägt die Farbe ihrer
                                ## Lage, nicht nur die Zahl. Eine rote Ziffer
                                ## in einer grauen Zeile übersieht man.
                                $ zeilenstil = {"unterdeckung": "probe_fehlt",
                                                "knapp": "probe_knapp"}.get(zeile["lage"], "probe_zeile")

                                hbox:
                                    spacing 0
                                    text zeile["modus"] style zeilenstil xsize 170
                                    text str(zeile["jahr"]) style zeilenstil xsize 80
                                    text zeile["pfad"] style zeilenstil xsize 190
                                    text str(zeile["soll"]) style zeilenstil xsize 70
                                    text str(zeile["frei"]) style zeilenstil xsize 70
                                    text str(zeile["bedingt"]) style zeilenstil xsize 110
                                    text zeile["lage_text"] style zeilenstil xsize 200

            frame:
                xsize 710
                ysize 780
                padding (24, 20)
                background rahmen(FARBE_PAPIER_HELL, FARBE_LINIE_FEIN, 2)

                vbox:
                    spacing 8

                    text "Geplante Rückbezüge (Paket 7 und 8)" style "probe_kopf"

                    add Solid(FARBE_LINIE_FEIN, xsize=650, ysize=1)

                    viewport:
                        xsize 650
                        ysize 700
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        vbox:
                            spacing 12

                            for zeile in nachhall:
                                vbox:
                                    xsize 610
                                    spacing 2
                                    text (str(zeile["jahr"]) + "  " + zeile["merkmal"]) style "probe_kopf" xsize 610
                                    text zeile["titel"] style "probe_zeile" size 19 xsize 610
                                    text (zeile["kennung"] + ("  vorhanden" if zeile["vorhanden"] else "  fehlt noch")) style ("probe_zeile" if zeile["vorhanden"] else "probe_fehlt") size 18 xsize 610

    hbox:
        xpos 110
        yalign 0.955
        style_prefix "navigation"

        textbutton "Zurück zum Hauptmenü" action Return()


################################################################################
## 14. Ablauf
################################################################################
##
## Aufgerufen wird dieser Abschnitt aus script.rpy. Die dort nötigen drei
## Änderungen stehen in PAKET3_AENDERUNGEN.md.

label ende_lebenslauf:

    $ endergebnis = ende_zusammenstellen()

    ## Paket 7, Schritt 1: der langsame Fade vor dem Lebenslauf. Er wird
    ## über renpy.transition() gesetzt, weil "call screen" kein with kennt;
    ## der Übergang gilt dann für die nächste Interaktion, und das ist genau
    ## dieser Bildschirm. Bei ausgeschalteter Bewegung liefert
    ## UEBERGANG_ENDE() None, und None heißt in Ren'Py: kein Übergang.
    $ renpy.transition(UEBERGANG_ENDE())

    ## PAKET 8, SCHRITT 2.6. Der Umgebungsklang endet mit dem Spiel, und der
    ## Lebenslauf ist die letzte der Stellen, an denen Musik nach
    ## Entscheidung 24 möglich wäre. Er bewertet nichts: Der Lebenslauf zeigt,
    ## was geworden ist, und nicht, ob es gut war.
    $ ton_still("umgebung")
    $ musik_setzen("lebenslauf")

    call screen ende_lebenslauf_bildschirm(endergebnis)

    jump ende_abschluss


################################################################################
## 20. Die Kartentypen vergeben - ganz zum Schluss
################################################################################
##
## PAKET 8, SCHRITT 1. Rang 4 hat sonst kein Block im Projekt, und das ist
## der Zweck: Erst wenn JEDES Ereignis aus allen Dateien im EREIGNIS_INDEX
## steht, kann die Vergabe alle finden. Die Tabelle KARTENTYP_VERGABE und
## ihre Begruendung stehen weiter oben bei den anderen Nachtraegen; hier
## steht nur der Aufruf, damit er nicht uebersehen wird.

init 4 python:

    kartentypen_vergeben()


label bestandsprobe:

    scene bg papier

    $ bestandszeilen = bestandsbericht()
    $ nachhallzeilen = nachhallbericht()

    call screen bestandsprobe_anzeige(bestandszeilen, nachhallzeilen)

    return

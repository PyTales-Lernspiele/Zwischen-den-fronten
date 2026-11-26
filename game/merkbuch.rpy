################################################################################
##
##  merkbuch.rpy
##
##  Paket 4.1: Das Merkbuch und der Umschlag vor dem Brief
##
##  ZURÜCKGEHOLT AM 3. SEPTEMBER 2026 (Paket 1)
##  Die .rpy-Datei war aus dem Spielordner verschwunden; nur merkbuch.rpyc
##  lag noch da. Der gesamte Quelltext dieser Datei stammt aus dieser
##  übersetzten Fassung und wurde mit werkzeuge/rpyc_quelle.py
##  zurückgeholt: jeder Ausdruck, jede Zahl, jeder Satz, jeder Bildschirm.
##  Nichts davon ist neu erfunden.
##
##  NEU SIND AUSSCHLIESSLICH DIE KOMMENTARE. Ren'Py wirft Kommentare beim
##  Übersetzen weg. Die ## Blöcke in dieser Datei wurden deshalb am
##  3. September 2026 neu geschrieben. Sie erklären, was der Code tut, und
##  können deshalb die Absicht der Urfassung verfehlen. Wer es besser
##  weiß, schreibt sie um.
##
##  WAS DIESE DATEI BEITRÄGT
##  Zwei Dinge, die zusammengehören:
##
##    1. DER UMSCHLAG. Vor jedem Brief liegt erst ein geschlossener
##       Umschlag auf dem Tisch. Man sieht Stempel, Anschrift und, bei
##       Feldpost, den Absender. Erst ein Klick macht ihn auf. Dadurch
##       wird aus einer Bildschirmfolge ein Vorgang.
##    2. DAS MERKBUCH. Zu Beginn schreibt die Spielerin zu vier Rollen je
##       einen Satz. Danach steht im Eckmenü ein Heft bereit, das zeigt,
##       wie es diesen vier geht und was von ihnen angekommen ist. Das
##       Heft ist der einzige Ort im Spiel, an dem man zurückblättern
##       kann, ohne den Ablauf anzuhalten.
##
##  Grundsätze, die in dieser Datei gelten:
##  - Steuerung ausschließlich mit der Maus. Keine key-Anweisungen.
##  - Ton nur als Frage nach Musik. Seit Paket 8, Schritt 2.6 steht in
##    lebenslage_abschluss_mit_merkbuch ein musik_setzen("heimat"): die
##    Stelle, an der der Pfad endgültig feststeht. Auf front und etappe
##    verwirft ton_spielen() sie hart. Das Heft selbst legt keinen Ton an,
##    auch keinen beim Aufschlagen.
##  - Varianten laufen über aktueller_pfad und merkmale, niemals über
##    Figurennamen. Für die drei Pfade gibt es hier nach_welt().
##  - Keine Wertveränderung. Das Merkbuch zeigt an, es entscheidet nicht.
##
##  ABLAUF-UMLEITUNGEN (Abschnitt 10)
##    lebenslage_abschluss -> lebenslage_abschluss_mit_merkbuch
##    post_zustellen       -> post_zustellen_als_ereignis
##  Beide werden in einem init 5 Block eingetragen, damit sie nach den
##  Eintragungen aus figuren.rpy (init 0) stehen und vor denen aus
##  minispiele.rpy (init 8). Sie greifen andere Marken an als jene, sie
##  stören einander also nicht.
##
##  INIT-ORDNUNG
##    -7  Konstanten. Vor minispiele.rpy (init -6), das darauf aufbaut.
##     1  Die Sätze, die zur Wahl stehen.
##     2  Die Vorstellungsszene. Läuft nach dialoge.rpy (init 0), weil
##        sie sich in SZENEN einträgt.
##     5  Zustand, Ablage, Umschlag und die beiden Umleitungen. Läuft nach
##        figuren.rpy (init 4), dessen Funktionen hier umschlossen werden.
##     6  Sprachprüfung. Läuft vor minispiele.rpy (init 9).
##
################################################################################


################################################################################
## 1. Konstanten
################################################################################
##
## init -7 läuft vor minispiele.rpy (init -6). Hier stehen nur Namen und
## Zahlen, keine Zugriffe auf andere Dateien.

init -7 python:

    ## Die vier Rollen, die eine Adresse bekommen können. Die fünfte aus
    ## figuren.rpy fehlt mit Absicht: Der Gegenseite schreibt man nicht.
    MERKBUCH_FIGUREN = ["naechste", "kundige", "kind", "amtsperson"]
    MERKBUCH_OHNE_ADRESSE = "gegenseite"

    ## Wie viele Sendungen das Heft aufbewahrt. Mehr braucht kein
    ## Durchgang, und ein Stapel, den niemand mehr durchsieht, ist kein
    ## Gedächtnis, sondern ein Archiv.
    MERKBUCH_ARCHIV_HOECHSTZAHL = 40

    ## Ab wie vielen Jahren ohne Post das Heft von Sorge spricht.
    MERKBUCH_SORGE_AB = 1

    ## Der Grauschleier, der unter Umschlag und Heft liegt. Er macht
    ## sichtbar, dass etwas obenauf liegt, ohne das Bild zu verdecken.
    POST_SCHATTEN = "#15130fbb"
    MERKBUCH_SCHATTEN = "#15130fcc"

    def nach_welt(front, heimat, etappe):
        """Baut ein Variantenwörterbuch für Front, Etappe und Heimat.

        SEIT PAKET 5, SCHRITT 1, TEIL B IST etappe PFLICHT. Vorher war
        der Wert wahlweise, und wo er fehlte, setzte diese Funktion still
        die Frontfassung ein. Das war der gefährlichste der vier
        Rückfallzweige des Projekts: Weil der Schlüssel "etappe" danach
        im Wörterbuch STAND, meldete variante() nichts. Der Ersatz war
        da, und keine Zahl zeigte ihn - Probe 2c meldete null, obwohl
        drei Zeilen des Merkbuchs die Frontfassung trugen.

        Streicht man nur die Notlösung in variante() und lässt diese
        hier stehen, wird es schlimmer statt besser: Die Probe meldet
        weiterhin null, und dann sucht auch niemand mehr. Deshalb fallen
        beide zusammen.

        Auch "standard" ist weg. Alle drei Pfade stehen jetzt immer da;
        eine Rückfallebene, die nie greifen kann, verdeckt nur, dass ein
        vierter Pfad eines Tages keine Fassung hätte. Ohne sie meldet
        variante() ihn als Lücke.
        """
        return {
            "front": front,
            "etappe": etappe,
            "heimat": heimat,
        }

    ## Was auf dem geschlossenen Umschlag steht, je nach Postart. Der
    ## Kopfsatz erzählt, wie die Sendung zu dir kommt; die Beschriftung des
    ## Knopfes sagt, was der Klick tut. Beides ohne Wertung: Ein Umschlag
    ## verrät nicht, ob die Nachricht darin gut oder schlecht ist.
    POST_ANKUENDIGUNG = {

        "feldpost": {
            "titel": "Post für dich",
            "kopf": {
                "front": "Mit dem Essenträger kommt ein Bündel nach vorn. Der Unteroffizier liest die Namen ab, und einer davon ist deiner.",
                "etappe": "Der Postsack kommt mit dem Frühzug an. Du sortierst ihn selbst, und ein Umschlag trägt deinen Namen.",
                "heimat": "Auf der Treppenstufe liegt ein Umschlag. Er ist weich geworden vom Weg.",
            },
            "knopf": "Umschlag öffnen",
        },

        "heimatpost": {
            "titel": "Post von zu Hause",
            "kopf": {
                "front": "Ein Umschlag mit einer Handschrift, die du seit deiner Schulzeit kennst.",
                "etappe": "Ein Umschlag mit einer Handschrift, die du seit deiner Schulzeit kennst. Er lag ganz unten im Sack.",
                "heimat": "Ein Umschlag im Kasten, ohne Absender auf der Vorderseite.",
            },
            "knopf": "Umschlag öffnen",
        },

        "amtlich": {
            "titel": "Ein Bogen mit Stempel",
            "kopf": {
                "front": "Der Feldwebel winkt dich heran. Er hat ein Papier in der Hand und wartet, bis du davorstehst.",
                "etappe": "Der Zahlmeister legt dir ein Papier auf den Tisch und bleibt daneben stehen.",
                "heimat": "Ein Umschlag ohne Marke, in der Ecke ein Stempel. So etwas macht man im Stehen auf.",
            },
            "knopf": "Den Bogen lesen",
        },

        "nachricht": {
            "titel": "Eine fremde Handschrift",
            "kopf": {
                "front": "Ein Brief, aber die Schrift auf dem Umschlag kennst du nicht. Du drehst ihn zweimal um, bevor du ihn aufmachst.",
                "etappe": "Ein Brief in fremder Schrift, und der Prüfstempel ist schon darauf. Er ist durch eure Stelle gegangen.",
                "heimat": "Ein Brief in einer fremden Handschrift. Der Absender steht klein auf der Rückseite.",
            },
            "knopf": "Aufmachen",
        },

        "fundstueck": {
            "titel": "Liegen geblieben",
            "kopf": {
                "front": "Etwas, das nicht dir gehört und das niemand mehr abholt.",
                "etappe": "Etwas ist aus einem Wagen gefallen und liegt seit gestern auf der Rampe.",
                "heimat": "Etwas, das jemand verloren hat und das nun bei dir liegt.",
            },
            "knopf": "Ansehen",
        },
    }

    ## Der Aufdruck auf dem Umschlag. An der Front trägt jede Sendung den
    ## Feldpoststempel, auch die von zu Hause: Sie ist über die Feldpost
    ## gelaufen. Ein Fundstück hat keinen Stempel und sagt das auch.
    ##
    ## Die Etappenspalte ist MIT ABSICHT gleich der Frontspalte. Das
    ## Etappengebiet gehörte zum Bereich der Feldpost; ein Brief dorthin
    ## bekam denselben Stempel wie einer in den Graben. Ein eigener
    ## Aufdruck wäre erfunden. Der Schlüssel steht trotzdem da, damit es
    ## eine Entscheidung bleibt und kein ungezählter Ersatz.
    POST_STEMPEL = {
        "feldpost":   {"front": "FELDPOST", "etappe": "FELDPOST", "heimat": "FELDPOST"},
        "heimatpost": {"front": "FELDPOST", "etappe": "FELDPOST", "heimat": "REICHSPOST"},
        "amtlich":    {"front": "DIENSTSACHE", "etappe": "DIENSTSACHE", "heimat": "DIENSTSACHE"},
        "nachricht":  {"front": "FELDPOST", "etappe": "FELDPOST", "heimat": "REICHSPOST"},
        "fundstueck": {"front": "OHNE", "etappe": "OHNE", "heimat": "OHNE"},
    }


################################################################################
## 2. Bestand: die Sätze, die zur Wahl stehen
################################################################################
##
## Je Rolle zwei Sätze, je Welt eine Fassung. Keiner der beiden ist besser.
## Beide sind Kleinigkeiten: etwas, das man an einem Menschen bemerkt und
## das mit dem Krieg nichts zu tun hat. Genau deshalb bleibt es haften.
##
## init 1 läuft nach dem Aufbau der Nebenfiguren in dialoge.rpy (init 0).

init 1 python:

    MERKBUCH_NOTIZEN = {

        "naechste": [
            {
                "front": "Teilt sein Brot, ohne zu fragen.",
                "etappe": "Legt dir das Lineal hin, bevor du danach suchst.",
                "heimat": "Klopft dreimal, bevor sie hereinkommt.",
            },
            {
                "front": "Schnarcht so laut, dass man ihn suchen kann.",
                "etappe": "Pfeift beim Zählen, immer dieselben vier Töne.",
                "heimat": "Hat immer noch eine Zwiebel übrig.",
            },
        ],

        "kundige": [
            {
                "front": "Kennt jede Vorschrift und beugt jede zweite.",
                "etappe": "Kennt jedes Formular und die Nummer dazu.",
                "heimat": "Weiß, welcher Laden am Dienstag Mehl hat.",
            },
            {
                "front": "Trocknet seine Socken über der Kerze.",
                "etappe": "Wärmt die Tinte in der Hand, bis sie wieder fließt.",
                "heimat": "Redet mit dem Schutzmann, als kenne sie ihn.",
            },
        ],

        "kind": [
            {
                "front": "Kaut an den Nägeln, wenn es still wird.",
                "etappe": "Zählt die Wagen laut mit, wenn ein Zug einfährt.",
                "heimat": "Zählt die Treppenstufen laut mit.",
            },
            {
                "front": "Kann jeden Vogel am Ruf erkennen.",
                "etappe": "Erkennt jede Lokomotive am Pfeifen.",
                "heimat": "Fragt so lange, bis jemand antwortet.",
            },
        ],

        "amtsperson": [
            {
                "front": "Sagt jeden Namen zweimal, bevor er ihn schreibt.",
                "etappe": "Streicht jede Zeile mit dem Lineal ab, von links nach rechts.",
                "heimat": "Spitzt den Bleistift vor jeder Unterschrift.",
            },
            {
                "front": "Hat einen Sohn im selben Jahrgang wie du.",
                ## Dieselbe Sache wie an der Front, aber so, wie die
                ## Etappe sie bemerkt: nicht im Gespräch, sondern an
                ## einer Gewohnheit beim Lesen. Sie bereitet amt_selbst vor.
                "etappe": "Sucht in jeder Liste zuerst nach einem bestimmten Namen.",
                "heimat": "Nennt dich beim Nachnamen und nickt dazu.",
            },
        ],
    }


################################################################################
## 3. Bestand: die Vorstellungsszene
################################################################################
##
## "Vier Adressen" führt die vier Rollen ein und erklärt nebenbei die Regel,
## nach der im ganzen Spiel Post kommt: Wer neben dir steht, schreibt dir
## nicht. Die Szene wird von merkbuch_vorstellung gerufen, einmal je
## Durchgang, unmittelbar vor dem Anlegen des Heftes.
##
## Die Amtsperson bekommt zwei Zeilen und keine dritte: Sie ist die
## einzige der vier, von der niemals ein persönlicher Brief kommt.
##
## init 2 läuft nach dialoge.rpy (init 0). Erst dort bestehen SZENEN und
## SZENEN_INDEX, in die sich die Szene einträgt.

init 2 python:

    MERKBUCH_SZENE = Szene(
        "merkbuch_vier_adressen", "Vier Adressen",
        ort=nach_welt("Ruhequartier", "Wohnviertel", etappe="Etappenlazarett"),
        hintergrund="papier",
        zeilen=[

            erzaehlt(nach_welt(
                "Vor dem Weitermarsch bleibt eine halbe Stunde. Du benutzt sie, um aufzuschreiben, wer dir schreiben soll.",
                "Vor der Abfahrt bleibt eine halbe Stunde. Du benutzt sie, um aufzuschreiben, wer dir schreiben soll.",
                etappe="Zwischen zwei Schichten bleibt eine halbe Stunde. Du benutzt sie, um aufzuschreiben, wer dir schreiben soll."
            )),

            erzaehlt(
                "Ein Brief findet niemanden von allein. Er braucht einen Namen und eine Adresse, sonst bleibt er in einem Sack liegen, bis ihn jemand öffnet."
            ),

            auftritt("links", "naechste"),
            sagt("naechste", nach_welt(
                "Ich liege links von dir. Wenn du nachts hinausmusst, weck mich, dann komme ich mit.",
                "Ich wohne über dir. Wenn du abends Licht brauchst, klopf an, ich habe noch Petroleum.",
                etappe="Ich habe die Schicht vor dir. Was ich nicht geschafft habe, siehst du gleich selbst."
            )),

            auftritt("rechts", "kundige"),
            sagt("kundige", nach_welt(
                "Ich bin der Älteste hier und der Einzige, der schon einen Winter draußen verbracht hat. Zwei Regeln: Kopf unten, Füße trocken.",
                "Ich stehe seit vier Uhr an, jeden Morgen. Frag mich, bevor du dich irgendwo anstellst, das spart dir zwei Stunden.",
                etappe="Ich bin seit dem Herbst hier. Frag mich, bevor du etwas unterschreibst, dann unterschreibst du das Richtige."
            )),

            auftritt("mitte", "kind"),
            sagt("kind", nach_welt(
                "Siebzehn. Mein Vater hat unterschrieben, sonst hätten sie mich nicht genommen. Ich schreibe jede Woche nach Hause, zweimal.",
                "Ich bin neun. Mein Vater ist seit Dienstag fort, und jetzt hole ich die Kohlen. Schreibst du mir, wenn ich einmal weg bin?",
                etappe="Fünfzehn. Ich trage die Meldungen, weil ich schnell laufe. Schreib meinen Namen richtig, dann finde ich ihn wieder."
            )),

            ich(
                "Drei Namen. Ich schreibe sie in mein Heft, so gut ich sie behalten kann."
            ),

            abgang("links"),
            abgang("rechts"),
            abgang("mitte"),

            erzaehlt(nach_welt(
                "Am Tisch vor der Baracke sitzt der Feldwebel über der Stammrolle und ruft die Namen der Reihe nach auf.",
                "Auf dem Amt ist Schalter drei geöffnet. Der Beamte hat einen Stapel Formulare vor sich und wartet nicht gern.",
                etappe="Im Verwaltungszimmer wird eingetragen, wer neu ist. Der Feldwebel liest die Liste von oben nach unten."
            )),

            auftritt("mitte", "amtsperson"),
            sagt("amtsperson", nach_welt(
                "Name, Truppenteil, und wer benachrichtigt wird, wenn Ihnen etwas zustößt. Das kommt hier hinein und wird nicht wieder geändert.",
                "Wer von Ihnen steht im Feld? Ohne den Truppenteil kann ich den Antrag nicht annehmen, da können Sie stehen bleiben, so lange Sie wollen.",
                etappe="Name, Dienststelle, und wer benachrichtigt wird, wenn Ihnen etwas zustößt. Sie tragen das selbst ein, und zwar leserlich."
            )),
            sagt("amtsperson", nach_welt(
                "Privatpost bekommen Sie von mir nicht. Wenn von mir etwas kommt, ist es Dienstsache.",
                "Und erwarten Sie keine Briefe von mir. Wenn von hier etwas kommt, ist es ein Bescheid.",
                etappe="Von mir bekommen Sie nichts Persönliches. Was ich unterschreibe, ist ein Beleg."
            )),
            abgang("mitte"),

            auftritt("rechts", "gegenseite"),
            erzaehlt(nach_welt(
                "Achtzig Meter weiter drüben raucht jemand. Wenn er zieht, sieht man kurz die Glut. Einen Namen hat er nicht, und eine Adresse erst recht nicht.",
                "Im Vorderhaus wird der Vorhang zugezogen. Ihr wohnt unter demselben Dach und habt seit dem Sommer kein Wort gewechselt.",
                etappe="Auf der letzten Bahre liegt einer, der nicht Deutsch spricht. Er wird versorgt wie die anderen und abtransportiert wie kein anderer."
            )),
            abgang("rechts"),

            erzaehlt(
                "Solange ihr euch jeden Tag seht, schreibt euch niemand. Post kommt erst, wenn einer fortgeht."
            ),
        ]
    )

    ## Die Prüfung hält den Block wiederholbar. Ohne sie stünde die Szene
    ## nach einem Neuladen des Skripts zweimal in SZENEN.
    if MERKBUCH_SZENE.kennung not in SZENEN_INDEX:
        SZENEN = SZENEN + [MERKBUCH_SZENE]
        SZENEN_INDEX[MERKBUCH_SZENE.kennung] = MERKBUCH_SZENE


################################################################################
## 4. Was im Heft steht
################################################################################
##
## Drei Zeilen je Rolle:
##
##   1. die Lage      was du über den Zustand weißt
##   2. die Nähe      wie es zwischen euch steht
##   3. der Ort       wo die Person ist, falls sie fort ist
##
## Die erste Zeile stützt sich auf "bekannt", nicht auf "zustand": Von
## jemandem, der fort ist, weißt du nur, was in einem Brief stand. Das Heft
## nimmt der Spielerin diese Unsicherheit nicht ab.
##
## init 5 läuft nach figuren.rpy (init 4). figur_zustand(), welttext() und
## ZUSTAENDE_ENDGUELTIG stehen ab dort bereit.

init 5 python:

    ## Zeile 1. Für "lebendig" steht hier mit Absicht nichts: Wer lebt und
    ## bei dir ist, braucht keine Meldung.
    ## Die Etappenspalte folgt derselben Regel wie ZUSTAND_ANZEIGE in
    ## figuren.rpy: In der Etappe erfährt man den Stand eines Menschen
    ## nicht durch Danebenstehen, sondern durch eine Meldung, die durch
    ## die eigenen Hände geht. Deshalb steht hier zweimal, dass die
    ## Spielerin die Zeile selbst geschrieben hat.
    MERKBUCH_LAGE = {
        "lebendig": {
            "front": "",
            "etappe": "",
            "heimat": "",
        },
        "verwundet": {
            "front": "Verwundet. Mehr steht in keiner Meldung.",
            "etappe": "Verwundet. Der Zug hat ihn nach hinten gebracht.",
            "heimat": "Verletzt. Wieder auf den Beinen, aber langsamer als vorher.",
        },
        "erkrankt": {
            "front": "Krank. Es geht auf und ab, und es dauert.",
            "etappe": "Krank gemeldet. In der Liste steht ein K und sonst nichts.",
            "heimat": "Krank. Der Husten ist seit dem Winter geblieben.",
        },
        "vermisst": {
            "front": "Vermisst. Das heißt: Es weiß niemand. Es heißt nicht mehr und nicht weniger.",
            "etappe": "Vermisst gemeldet. Du hast die Meldung selbst abgeschrieben.",
            "heimat": "Verschollen. Die Nachforschung läuft, und Antwort gibt es keine.",
        },
        "verhaftet": {
            "front": "In Haft. Wie lange, sagt niemand, und niemanden kannst du danach fragen.",
            "etappe": "In Haft. Die Bücher sind versiegelt, und niemand sagt, wie lange.",
            "heimat": "In Haft. Wie lange, entscheidet kein Gericht, das du anrufen könntest.",
        },
        "entfremdet": {
            "front": "Fremd geworden. Es ist nichts vorgefallen, und genau das ist es.",
            "etappe": "Fremd geworden. Es ist nichts vorgefallen, und genau das ist es.",
            "heimat": "Fremd geworden. Es ist nichts vorgefallen, und genau das ist es.",
        },
        "gefallen": {
            "front": "Gefallen. Auf dem Formular war nur der Name eingetragen.",
            "etappe": "Auf der Verlustliste. Deine Abschrift liegt in der Mappe.",
            "heimat": "Gestorben, noch bevor der Krieg zu Ende war.",
        },
    }

    ## Zeile 2 für jemanden, der bei dir ist. Von oben nach unten gelesen:
    ## Der erste Eintrag, dessen Zahl die Verbundenheit erreicht, gilt.
    MERKBUCH_NAEHE_DA = [
        (9, {"front": "Ihr sitzt jeden Abend nebeneinander.",
             "etappe": "Ihr steht jede Schicht an derselben Rampe.",
             "heimat": "Ihr seht euch jeden Tag, und das ist keine Kleinigkeit."}),
        (7, {"front": "Ihr redet, wenn Zeit ist. Es ist meistens Zeit.",
             "etappe": "Ihr redet zwischen zwei Zügen, und das reicht meistens.",
             "heimat": "Ihr redet auf der Treppe, jedes Mal ein bisschen länger."}),
        (4, {"front": "Ihr grüßt euch. Mehr ist es gerade nicht.",
             "etappe": "Ihr grüßt euch. Mehr ist es gerade nicht.",
             "heimat": "Ihr grüßt euch. Mehr ist es gerade nicht."}),
        (2, {"front": "Ihr geht aneinander vorbei und seht dabei woandershin.",
             "etappe": "Ihr geht aneinander vorbei und seht dabei woandershin.",
             "heimat": "Ihr geht aneinander vorbei und seht dabei woandershin."}),
        (0, {"front": "Zwischen euch ist es still geworden.",
             "etappe": "Zwischen euch ist es still geworden.",
             "heimat": "Zwischen euch ist es still geworden."}),
    ]

    ## Zeile 2 für jemanden, der fort ist. Hier zählt nicht die
    ## Verbundenheit, sondern die Zeit seit der letzten Sendung. Gelesen
    ## wird von oben nach unten, der letzte zutreffende Eintrag gilt.
    MERKBUCH_NAEHE_FORT = [
        (0, {"front": "Der letzte Brief steckt noch in deiner Tasche.",
             "etappe": "Der letzte Brief liegt zwischen zwei Bögen in deiner Mappe.",
             "heimat": "Der letzte Brief liegt bei dir in der Schublade."}),
        (1, {"front": "Seit dem vorigen Jahr ist nichts gekommen. Du machst dir Sorgen.",
             "etappe": "Seit dem vorigen Jahr ist nichts gekommen. Du machst dir Sorgen.",
             "heimat": "Seit dem vorigen Jahr ist nichts gekommen. Du machst dir Sorgen."}),
        (2, {"front": "Du wartest seit zwei Jahren auf ein Lebenszeichen.",
             "etappe": "Du wartest seit zwei Jahren auf ein Lebenszeichen.",
             "heimat": "Du wartest seit zwei Jahren auf ein Lebenszeichen."}),
    ]

    ## Die fünfte Rolle steht im Heft, aber ohne Adresse und ohne Zeile
    ## über Nähe. Sie ist da, und man schreibt ihr trotzdem nicht.
    ##
    ## In der Etappe ist sie der Gefangene aus der Kolonne. Der Abstand
    ## ist hier am kleinsten und die Trennung trotzdem am härtesten: Man
    ## sieht einander täglich und kennt nur eine Nummer.
    MERKBUCH_GEGENSEITE = {
        "front": "Achtzig Meter. Kein Name, kein Postweg, und trotzdem wisst ihr beide, dass der andere da ist.",
        "etappe": "Zwanzig Schritt bis zum Gleis. Ihr seht euch jeden Tag, und du kennst nur seine Nummer.",
        "heimat": "Zwanzig Schritte über den Hof. Ihr schreibt euch nicht, obwohl ihr euch täglich seht.",
    }

    def merkbuch_lage_satz(kennung):
        """Zeile 1: was du über den Zustand weißt."""
        eintrag = figur_zustand(kennung)
        if eintrag is None:
            return ""
        ## Wer fort ist, von dem kennst du nur den gemeldeten Stand. Wer
        ## bei dir ist, dessen Lage siehst du selbst.
        gezeigt = eintrag["bekannt"] if eintrag["fort"] else eintrag["zustand"]
        return welttext(MERKBUCH_LAGE.get(gezeigt, MERKBUCH_LAGE["lebendig"]))

    def merkbuch_naehe_satz(kennung):
        """Zeile 2: wie es zwischen euch steht."""
        eintrag = figur_zustand(kennung)
        if eintrag is None:
            return ""
        ## Über einen Toten steht keine Zeile darüber, wie es zwischen
        ## euch steht. Der Zustand hat das letzte Wort.
        if eintrag["zustand"] in ZUSTAENDE_ENDGUELTIG:
            return ""
        ## Fort: Es zählt, wie lange nichts gekommen ist.
        if eintrag["fort"]:
            abstand = max(0, aktuelles_jahr - eintrag["post_jahr"])
            gewaehlt = MERKBUCH_NAEHE_FORT[0][1]
            for grenze, vorlage in MERKBUCH_NAEHE_FORT:
                if abstand >= grenze:
                    gewaehlt = vorlage
            return welttext(gewaehlt)
        ## Bei dir: Es zählt die Verbundenheit.
        for grenze, vorlage in MERKBUCH_NAEHE_DA:
            if eintrag["verbundenheit"] >= grenze:
                return welttext(vorlage)
        return ""

    def merkbuch_ort_satz(kennung):
        """Die kleine Ortsangabe, sofern die Person fort ist."""
        eintrag = figur_zustand(kennung)
        if eintrag is None or not eintrag["fort"]:
            return ""
        return eintrag["grund"]

    ## Die eigenen Sätze ######################################################
    ##
    ## Gewählt wird einmal, beim Anlegen des Heftes. Danach steht der Satz
    ## fest und taucht auf jedem Umschlag dieser Person wieder auf.

    def merkbuch_notiz_auswahl(kennung):
        """Die zwei Sätze, die zur Wahl stehen, in der eigenen Welt."""
        vorlagen = MERKBUCH_NOTIZEN.get(kennung, [])
        return [welttext(vorlage) for vorlage in vorlagen]

    def merkbuch_notiz_setzen(kennung, stelle):
        global merkbuch_notizen
        auswahl = merkbuch_notiz_auswahl(kennung)
        if stelle < 0 or stelle >= len(auswahl):
            return
        neu = dict(merkbuch_notizen)
        neu[kennung] = {"stelle": stelle, "satz": auswahl[stelle]}
        merkbuch_notizen = neu

    def merkbuch_notiz(kennung):
        eintrag = merkbuch_notizen.get(kennung)
        if not eintrag:
            return ""
        return eintrag.get("satz", "")

    def merkbuch_notiz_stelle(kennung):
        eintrag = merkbuch_notizen.get(kennung)
        if not eintrag:
            return None
        return eintrag.get("stelle")

    def merkbuch_fehlende():
        return len([k for k in MERKBUCH_FIGUREN if not merkbuch_notiz(k)])


################################################################################
## 5. Die Ablage und der Umschlag
################################################################################
##
## ARBEITSWEISE
## Dieser Abschnitt ändert figuren.rpy nicht, sondern legt sich um drei
## Funktionen von dort herum: figuren_anlegen(), brief_zustellen() und
## brief_beantworten(). Jede behält ihren Namen und ihr Verhalten und tut
## danach eine Sache mehr. Dasselbe Verfahren benutzen figuren.rpy und
## minispiele.rpy mit zustand_zuruecksetzen().

init 5 python:

    def merkbuch_brief_ablegen(brief):
        global merkbuch_archiv, merkbuch_neu
        eintrag = {
            "kennung": brief["kennung"],
            "figur": brief["figur"],
            "art": brief["art"],
            "marke": brief["marke"],
            "absender": brief["absender"],
            "zusatz": brief["zusatz"],
            "datum": brief["datum"],
            "kopf": brief["kopf"],
            "zeilen": list(brief["zeilen"]),
            "jahr": aktuelles_jahr,
            "antwort": "",
        }
        bestand = list(merkbuch_archiv) + [eintrag]
        if len(bestand) > MERKBUCH_ARCHIV_HOECHSTZAHL:
            bestand = bestand[-MERKBUCH_ARCHIV_HOECHSTZAHL:]
        merkbuch_archiv = bestand
        merkbuch_neu = True

    def merkbuch_antwort_vermerken(brief, folge):
        """Trägt nach, was du geantwortet hast."""
        global merkbuch_archiv
        if not merkbuch_archiv:
            return
        bestand = list(merkbuch_archiv)
        letzter = dict(bestand[-1])
        if letzter["kennung"] != brief["kennung"]:
            return
        letzter["antwort"] = folge["titel"]
        bestand[-1] = letzter
        merkbuch_archiv = bestand

    def merkbuch_briefe_von(kennung):
        return [eintrag for eintrag in merkbuch_archiv if eintrag["figur"] == kennung]

    def merkbuch_hat_briefe(kennung):
        return len(merkbuch_briefe_von(kennung)) > 0

    def merkbuch_zuruecksetzen():
        global merkbuch_notizen, merkbuch_archiv, merkbuch_angelegt, merkbuch_neu
        merkbuch_notizen = {}
        merkbuch_archiv = []
        merkbuch_angelegt = False
        merkbuch_neu = False

    def merkbuch_verfuegbar():
        """Der Knopf im Eckmenü erscheint erst, wenn das Heft existiert."""
        return bool(merkbuch_angelegt)

    def merkbuch_knopf_text():
        if merkbuch_neu:
            return "Merkbuch  •"
        return "Merkbuch"

    def merkbuch_oeffnen():
        global merkbuch_neu
        merkbuch_neu = False

    ## Die drei Umschließungen ################################################
    ##
    ## Jede hält die ursprüngliche Funktion unter einem eigenen Namen fest
    ## und ruft sie zuerst. Ohne diesen festgehaltenen Namen riefe die neue
    ## Fassung sich selbst auf, bis Ren'Py mit RecursionError abbricht.

    figuren_anlegen_vor_merkbuch = figuren_anlegen

    def figuren_anlegen():
        figuren_anlegen_vor_merkbuch()
        merkbuch_zuruecksetzen()

    brief_zustellen_vor_merkbuch = brief_zustellen

    def brief_zustellen(brief):
        brief_zustellen_vor_merkbuch(brief)
        merkbuch_brief_ablegen(brief)

    brief_beantworten_vor_merkbuch = brief_beantworten

    def brief_beantworten(brief, stelle):
        folge = brief_beantworten_vor_merkbuch(brief, stelle)
        if folge:
            merkbuch_antwort_vermerken(brief, folge)
        return folge

    ## Der geschlossene Umschlag ##############################################

    def post_ankuendigung_daten(brief):
        """Alles, was auf dem geschlossenen Umschlag steht.

        Bei Feldpost erkennst du die Handschrift, also steht der Name
        darauf. Bei einer fremden Handschrift und bei amtlicher Post
        steht er nicht darauf: Wer schreibt, erfährst du erst drinnen.
        """
        vorlage = POST_ANKUENDIGUNG.get(brief["art"], POST_ANKUENDIGUNG["nachricht"])
        verrat = brief["art"] in ("feldpost", "heimatpost")
        return {
            "titel": vorlage["titel"],
            "kopf": welttext(vorlage["kopf"]),
            "knopf": vorlage["knopf"],
            "stempel": welttext(POST_STEMPEL.get(brief["art"], POST_STEMPEL["nachricht"])),
            "absender": brief["absender"] if verrat else "",
            "notiz": merkbuch_notiz(brief["figur"]) if verrat else "",
            "an_wen": post_anschrift(),
            "wohin": post_zielort(),
        }

    def post_anschrift():
        """Die Zeile, die auf dem Umschlag oben steht: an dich."""
        name = person_name()
        if not name:
            return "An den Empfänger"
        stand = person_stand()
        if stand:
            return "An " + stand + " " + name
        return "An " + name

    def post_zielort():
        ## Front UND Etappe gehörten zum Bereich der Feldpost. Auf dem
        ## Umschlag stand deshalb in beiden Fällen dieselbe Zeile - das
        ## ist keine Ersatzfassung, sondern der Postweg selbst. Seit
        ## Paket 5, Schritt 1, Teil B steht die Etappe hier ausdrücklich
        ## dabei; vorher kam sie nur deshalb hierher, weil briefwelt()
        ## sie auf "front" abbildete.
        if briefwelt() in ("front", "etappe"):
            return "Deutsche Feldpost"
        return PFAD_ORT.get(aktueller_pfad, "")


################################################################################
## 6. Zustandsvariablen
################################################################################

## Die gewählten Sätze, je Rolle einer.
default merkbuch_notizen = {}

## Die abgelegten Sendungen, älteste zuerst.
default merkbuch_archiv = []

## Erst wenn das Heft angelegt ist, erscheint der Knopf im Eckmenü.
default merkbuch_angelegt = False

## Trägt den Punkt neben dem Knopf, solange etwas Neues ungelesen ist.
default merkbuch_neu = False

default merkbuch_gewaehlt = None


################################################################################
## 7. Stile
################################################################################

init offset = -1

style post_titel is default:
    font SCHRIFT_TITEL
    size 44
    bold True
    color FARBE_TINTE

style post_kopf is default:
    size 27
    color FARBE_TINTE_MATT
    line_spacing 8

style post_anschrift is default:
    font SCHRIFT_DOKUMENT
    size 30
    color FARBE_TINTE

style post_anschrift_klein is default:
    font SCHRIFT_DOKUMENT
    size 22
    color FARBE_LINIE

style post_stempel_text is default:
    font SCHRIFT_SCHMAL
    size 19
    bold True
    color FARBE_LINIE
    kerning 2.6
    text_align 0.5

style post_absender is default:
    font SCHRIFT_TITEL
    size 30
    bold True
    color FARBE_AKZENT

style post_oeffnen is default:
    font SCHRIFT_TITEL
    size 26
    bold True
    color FARBE_AKZENT
    kerning 1.6

style merkbuch_titel is default:
    font SCHRIFT_TITEL
    size 40
    bold True
    color FARBE_TINTE

style merkbuch_unterzeile is default:
    size 23
    italic True
    color FARBE_TINTE_MATT
    line_spacing 5

style merkbuch_abschnitt is default:
    font SCHRIFT_TITEL
    size 20
    bold True
    color FARBE_TINTE_MATT
    kerning 2.0

style merkbuch_notiz_text is default:
    font SCHRIFT_DOKUMENT
    size 26
    color FARBE_AKZENT
    line_spacing 4

style merkbuch_satz is default:
    size 24
    color FARBE_TINTE
    line_spacing 7

style merkbuch_satz_matt is default:
    size 22
    italic True
    color FARBE_TINTE_MATT
    line_spacing 6

style merkbuch_frage is default:
    size 22
    italic True
    color FARBE_TINTE_MATT

style merkbuch_pruefung is default:
    size 16
    color FARBE_LINIE


################################################################################
## 8. Bewegung
################################################################################
##
## Zwei Bewegungen, beide mit einem Grund aus der Sache: Der Umschlag wird
## auf den Tisch gelegt, das Heft wird aufgeschlagen. Keine von beiden
## bewertet etwas, und ein Klick zeigt sofort den Endzustand.
##
## PAKET 7, SCHRITT 1: Beide holen ihre Dauer jetzt von außen, aus
## bewegungszeit(). Vorher stand sie hier fest, und der Schalter für die
## Bewegung wäre an ihnen vorbeigelaufen.
##
## post_eintreffen dauerte dabei 0,55 Sekunden. Die Animationsregeln lassen
## höchstens 0,45 zu; nur der Kapitelwechsel darf bis 0,8. Der Umschlag ist
## kein Kapitelwechsel, also steht die Vorgabe jetzt auf 0,45. Das ist die
## einzige Zahl, die dieser Schritt geändert hat, und sie ist gemessen:
## Probe 9 nennt sie.

transform post_eintreffen(dauer=0.45):
    alpha 0.0
    yoffset 54
    easein dauer alpha 1.0 yoffset 0

transform merkbuch_aufschlagen(dauer=0.28):
    alpha 0.0
    zoom 0.985
    easein dauer alpha 1.0 zoom 1.0


################################################################################
## 9. Bildschirme
################################################################################
##
## Alle sechs werden ausschließlich mit der Maus bedient. Lange Listen
## laufen in einem viewport, der sich mit Rad und Ziehen bewegen lässt;
## eine Taste ist nirgends nötig.

## Der geschlossene Umschlag ##################################################
##
## Steht vor jedem Brief. Ein Klick irgendwo auf den Umschlag macht ihn auf.

screen post_ankuendigung(brief):
    $ post = post_ankuendigung_daten(brief)
    add Solid(FARBE_PAPIER)
    use zustandskopf(ort_text())
    add Solid(POST_SCHATTEN)
    button:
        xalign 0.5
        ypos 296
        xysize (980, 486)
        padding (54, 42)
        background rahmen_schatten(FARBE_PAPIER_HELL, FARBE_LINIE, 3, versatz=16)
        hover_background rahmen_schatten("#fffdf8", FARBE_AKZENT, 3, versatz=16)
        action Return()
        at post_eintreffen(bewegungszeit(0.45))
        vbox:
            xsize 872
            spacing 18
            hbox:
                xsize 872
                text post["titel"] style "post_titel" yalign 0.5
                frame:
                    xalign 1.0
                    yalign 0.5
                    xysize (168, 74)
                    padding (10, 10)
                    background rahmen_leer(FARBE_LINIE_FEIN, 2)
                    text post["stempel"] style "post_stempel_text" align (0.5, 0.5) xsize 148
            add Solid(FARBE_LINIE_FEIN, xsize=872, ysize=1)
            vbox:
                xoffset 232
                spacing 4
                text post["an_wen"] style "post_anschrift" xsize 620
                text post["wohin"] style "post_anschrift_klein" xsize 620
                add Solid(FARBE_LINIE_FEIN, xsize=560, ysize=1) yoffset 8
            text post["kopf"] style "post_kopf" xsize 872
            if post["absender"]:
                vbox:
                    spacing 2
                    text post["absender"] style "post_absender"
                    if post["notiz"]:
                        text post["notiz"] style "merkbuch_notiz_text" xsize 872
            null height 4
            hbox:
                xalign 1.0
                spacing 10
                text post["knopf"] style "post_oeffnen" yalign 0.5
                add ZEICHEN_WEITER yalign 0.5
    use eckmenue


## Das Heft anlegen ###########################################################
##
## Vier Karten, je zwei Sätze zur Wahl. Der Knopf unten wird erst gültig,
## wenn zu allen vier etwas eingetragen ist; vorher zählt er, was fehlt.
## Er wird dabei nicht rot und schilt nicht - er sagt nur, wie weit es ist.

screen merkbuch_anlegen():
    add Solid(FARBE_PAPIER)
    use zustandskopf(ort_text())
    $ fehlend = merkbuch_fehlende()
    $ knopftext = "Fertig" if fehlend == 0 else ("Noch " + str(fehlend) + " eintragen")
    vbox:
        xalign 0.5
        ypos 244
        spacing 20
        vbox:
            xalign 0.5
            spacing 6
            text "Dein Merkbuch" style "merkbuch_titel" xalign 0.5
            text "Schreib zu jedem einen Satz dazu. Irgendetwas, woran du dich später erinnerst.":
                style "merkbuch_unterzeile"
                xalign 0.5
        add Solid(FARBE_AKZENT, xsize=180, ysize=3) xalign 0.5
        grid 2 2:
            xalign 0.5
            spacing 26
            for kennung in MERKBUCH_FIGUREN:
                $ auswahl = merkbuch_notiz_auswahl(kennung)
                $ gewaehlt = merkbuch_notiz_stelle(kennung)
                frame:
                    xsize 780
                    padding (30, 22)
                    background rahmen(FARBE_PAPIER_HELL, FARBE_LINIE_FEIN, 2)
                    vbox:
                        xsize 720
                        spacing 10
                        hbox:
                            spacing 14
                            text figur_name(kennung) style "figuren_name" yalign 1.0
                            text figur_zusatz(kennung) style "figuren_ort" yalign 1.0
                        add Solid(FARBE_LINIE_FEIN, xsize=720, ysize=1)
                        for stelle, satz in enumerate(auswahl):
                            button:
                                xsize 720
                                padding (18, 12)
                                background None
                                hover_background rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE_FEIN, 2)
                                selected_background rahmen(FARBE_PAPIER_DUNKEL, FARBE_AKZENT, 2)
                                selected (gewaehlt == stelle)
                                action Function(merkbuch_notiz_setzen, kennung, stelle)
                                hbox:
                                    spacing 12
                                    if gewaehlt == stelle:
                                        add Solid(FARBE_AKZENT, xsize=5, ysize=30) yalign 0.5
                                    else:
                                        add Solid(FARBE_SEGMENT_LEER, xsize=5, ysize=30):
                                            yalign 0.5
                                    text satz style "merkbuch_notiz_text" yalign 0.5 xsize 660
        vbox:
            xalign 0.5
            spacing 10
            text "Beides ist richtig. Es ist dein Heft." style "merkbuch_frage" xalign 0.5
            if fehlend == 0:
                textbutton knopftext xalign 0.5 style_prefix "weiter" action Return()
            else:
                textbutton knopftext xalign 0.5 style_prefix "weiter" action None
    use werthinweis


## Das aufgeschlagene Heft ####################################################
##
## Wird mit Show() gezeigt, nicht mit call screen. Dadurch lässt es sich
## mitten in einer Szene, einem Brief oder einer Entscheidung aufschlagen,
## ohne den Ablauf zu unterbrechen. modal True hält den Klick darunter an,
## solange es offen ist.

screen merkbuch_anzeige():
    modal True
    zorder 100
    add Solid(MERKBUCH_SCHATTEN)
    frame:
        align (0.5, 0.5)
        xsize 1600
        ysize 900
        padding (52, 40)
        background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)
        at merkbuch_aufschlagen(bewegungszeit(0.28))
        vbox:
            xsize 1496
            spacing 18
            hbox:
                xsize 1496
                vbox:
                    spacing 4
                    text "Merkbuch" style "merkbuch_titel"
                    text "Wer dir schreiben kann, und wie es ihnen geht, soweit du es weißt.":
                        style "merkbuch_unterzeile"
                textbutton "Zuklappen":
                    xalign 1.0
                    yalign 0.5
                    style_prefix "ecke"
                    action [Hide("merkbuch_lesen"), Hide("merkbuch_briefe"), Hide("merkbuch_anzeige")]
            add Solid(FARBE_AKZENT, xsize=1496, ysize=3)
            hbox:
                spacing 34
                viewport:
                    xsize 940
                    ysize 736
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    vbox:
                        xsize 900
                        spacing 16
                        for kennung in MERKBUCH_FIGUREN:
                            use merkbuch_eintrag(kennung, 900)
                vbox:
                    xsize 500
                    spacing 20
                    text "OHNE ADRESSE" style "merkbuch_abschnitt"
                    frame:
                        xsize 500
                        padding (26, 22)
                        background rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE_FEIN, 2)
                        vbox:
                            xsize 448
                            spacing 8
                            text figur_name(MERKBUCH_OHNE_ADRESSE):
                                style "figuren_name"
                                xsize 448
                            text figur_zusatz(MERKBUCH_OHNE_ADRESSE):
                                style "figuren_ort"
                                xsize 448
                            add Solid(FARBE_LINIE_FEIN, xsize=448, ysize=1)
                            $ lage_gegen = merkbuch_lage_satz(MERKBUCH_OHNE_ADRESSE)
                            if lage_gegen:
                                text lage_gegen style "merkbuch_satz" xsize 448
                            text welttext(MERKBUCH_GEGENSEITE):
                                style "merkbuch_satz_matt"
                                xsize 448
                    frame:
                        xsize 500
                        padding (26, 22)
                        background rahmen_leer(FARBE_LINIE_FEIN, 2)
                        vbox:
                            xsize 448
                            spacing 8
                            text "WIE DIE POST GEHT" style "merkbuch_abschnitt"
                            text "Schreiben kann dir nur, wer gerade nicht bei dir ist. Wer neben dir steht, schreibt dir nicht.":
                                style "merkbuch_satz_matt"
                                xsize 448
                            text "Antworten kostet dich etwas. Nicht zu antworten auch.":
                                style "merkbuch_satz_matt"
                                xsize 448


## Eine Seite im Heft #########################################################
##
## Wird von merkbuch_anzeige viermal benutzt. Wessen Lebensweg zu Ende ist,
## bekommt den dunkleren Grund - kein Kreuz, kein Zeichen, nur ein Papier,
## das nicht mehr weiß ist.

screen merkbuch_eintrag(kennung, breite):
    $ notiz = merkbuch_notiz(kennung)
    $ lage = merkbuch_lage_satz(kennung)
    $ naehe = merkbuch_naehe_satz(kennung)
    $ ort = merkbuch_ort_satz(kennung)
    $ endgueltig = not figur_lebt(kennung)
    $ grundfarbe = FARBE_PAPIER_DUNKEL if endgueltig else FARBE_PAPIER_HELL
    frame:
        xsize breite
        padding (28, 22)
        background rahmen(grundfarbe, FARBE_LINIE_FEIN, 2)
        vbox:
            xsize breite - 56
            spacing 8
            hbox:
                xsize breite - 56
                spacing 14
                text figur_name(kennung) style "figuren_name" yalign 1.0
                text figur_zusatz(kennung) style "figuren_ort" yalign 1.0
                if ort:
                    text ort style "figuren_ort" yalign 1.0 xalign 1.0
                if persistent.analysemodus:
                    text (kennung + " " + str(figur_verbundenheit(kennung)) + "/10"):
                        style "merkbuch_pruefung"
                        yalign 1.0
                        xalign 1.0
            if notiz:
                text ("„" + notiz + "“") style "merkbuch_notiz_text" xsize breite - 56
            add Solid(FARBE_LINIE_FEIN, xsize=breite - 56, ysize=1)
            if lage:
                text lage style "merkbuch_satz" xsize breite - 56
            if naehe:
                text naehe style "merkbuch_satz_matt" xsize breite - 56
            if merkbuch_hat_briefe(kennung):
                textbutton "Briefe wieder lesen":
                    style_prefix "ecke"
                    action Show("merkbuch_briefe", kennung=kennung)


## Alle Sendungen einer Hand ##################################################

screen merkbuch_briefe(kennung):
    modal True
    zorder 110
    add Solid(MERKBUCH_SCHATTEN)
    $ bestand = merkbuch_briefe_von(kennung)
    frame:
        align (0.5, 0.5)
        xsize 1180
        ysize 800
        padding (48, 38)
        background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)
        at merkbuch_aufschlagen(bewegungszeit(0.28))
        vbox:
            xsize 1084
            spacing 16
            hbox:
                xsize 1084
                vbox:
                    spacing 3
                    text figur_name(kennung) style "merkbuch_titel"
                    text "Alles, was von dieser Hand angekommen ist.":
                        style "merkbuch_unterzeile"
                textbutton "Zurück":
                    xalign 1.0
                    yalign 0.5
                    style_prefix "ecke"
                    action Hide("merkbuch_briefe")
            add Solid(FARBE_AKZENT, xsize=1084, ysize=3)
            viewport:
                xsize 1084
                ysize 640
                scrollbars "vertical"
                mousewheel True
                draggable True
                vbox:
                    xsize 1044
                    spacing 14
                    for stelle, eintrag in enumerate(bestand):
                        button:
                            xsize 1044
                            padding (26, 20)
                            background rahmen(FARBE_PAPIER_HELL, FARBE_LINIE_FEIN, 2)
                            hover_background rahmen(FARBE_PAPIER_DUNKEL, FARBE_AKZENT, 2)
                            action Show("merkbuch_lesen", brief=eintrag)
                            vbox:
                                xsize 992
                                spacing 6
                                hbox:
                                    xsize 992
                                    text eintrag["marke"].upper() style "brief_marke" yalign 1.0
                                    text (eintrag["datum"] + "   " + str(eintrag["jahr"])):
                                        style "brief_stempel"
                                        xalign 1.0
                                        yalign 1.0
                                $ anfang = eintrag["zeilen"][0] if eintrag["zeilen"] else ""
                                text anfang style "merkbuch_satz_matt" xsize 992
                                if eintrag["antwort"]:
                                    text ("Du hast geantwortet: " + eintrag["antwort"]):
                                        style "merkbuch_frage"
                                        xsize 992


## Eine Sendung noch einmal lesen #############################################

screen merkbuch_lesen(brief):
    modal True
    zorder 120
    add Solid(MERKBUCH_SCHATTEN)
    frame:
        align (0.5, 0.5)
        xsize 1240
        ysize 820
        padding (48, 36)
        background rahmen_schatten(FARBE_PAPIER_HELL, FARBE_AKZENT, 3)
        at merkbuch_aufschlagen(bewegungszeit(0.28))
        vbox:
            xsize 1144
            spacing 14
            hbox:
                xsize 1144
                text brief["marke"].upper() style "brief_marke" yalign 1.0
                text brief["datum"] style "brief_stempel" xalign 1.0 yalign 1.0
            add Solid(FARBE_LINIE_FEIN, xsize=1144, ysize=1)
            hbox:
                spacing 16
                text brief["absender"] style "brief_absender" yalign 1.0
                text brief["zusatz"] style "brief_zusatz" yalign 1.0
            text brief["kopf"] style "brief_kopf" xsize 1144
            add Solid(FARBE_AKZENT, xsize=90, ysize=2)
            viewport:
                xsize 1144
                ysize 480
                scrollbars "vertical"
                mousewheel True
                draggable True
                vbox:
                    xsize 1100
                    spacing 12
                    for satz in brief["zeilen"]:
                        text satz style "brief_zeile" xsize 1100
                    if brief["antwort"]:
                        add Solid(FARBE_LINIE_FEIN, xsize=1100, ysize=1)
                        text ("Geantwortet hast du damals: " + brief["antwort"]):
                            style "merkbuch_frage"
                            xsize 1100
            textbutton "Weglegen" xalign 0.5 style_prefix "weiter" action Hide("merkbuch_lesen")

init offset = 0


################################################################################
## 10. Ablauf
################################################################################
##
## Zwei Umleitungen, beide in derselben Bauart wie in figuren.rpy: Die neue
## Marke ist Zeile für Zeile dieselbe wie die alte und hat an einer Stelle
## etwas mehr. An script.rpy und figuren.rpy ist dafür nichts zu ändern.
##
## Wer hier eine dritte Umleitung anlegt, prüft zuerst, ob dieselbe Marke
## schon umgeleitet wird. Belegt sind zurzeit: hauptschleife und
## kapitelwechsel (figuren.rpy), ereignis_spielen (minispiele.rpy) und die
## beiden hier.

init 5 python:

    config.label_overrides["lebenslage_abschluss"] = "lebenslage_abschluss_mit_merkbuch"
    config.label_overrides["post_zustellen"] = "post_zustellen_als_ereignis"


## Die Fassung aus herkunft.rpy, ergänzt um den Aufruf der Vorstellung.
label lebenslage_abschluss_mit_merkbuch:

    ## PAKET 8, SCHRITT 2.6. Die letzte der sieben Stellen aus Entscheidung 24:
    ## der Heimatpfad. Hier steht der Pfad zum ersten Mal endgültig fest, und
    ## hier läuft jeder Durchgang durch. Der Aufruf wird ohne Fallunterscheidung
    ## gemacht — die harte Sperre in ton_spielen() verwirft ihn auf front und
    ## etappe von selbst. Dieselbe Zeile steht in der Fassung in herkunft.rpy,
    ## die nicht läuft.
    $ musik_setzen("heimat")

    call screen lebenslage_uebersicht

    $ ziehungen_im_kapitel = 0

    call merkbuch_vorstellung

    jump hauptschleife


label merkbuch_vorstellung:

    ## Einmal je Durchgang. Wer schon ein Heft hat, bekommt kein zweites.
    if merkbuch_angelegt:
        return

    call szene_spielen("merkbuch_vier_adressen")

    call screen merkbuch_anlegen

    $ merkbuch_angelegt = True

    ## Der Punkt am Knopf gilt neuer Post, nicht dem eigenen Eintrag.
    $ merkbuch_neu = False

    $ protokoll_eintragen("merkbuch", ", ".join([merkbuch_notiz(k) for k in MERKBUCH_FIGUREN if merkbuch_notiz(k)]))

    return


## Die Fassung aus figuren.rpy, ergänzt um den Umschlag davor.
label post_zustellen_als_ereignis:

    $ post_zaehler = post_zaehler + 1

    $ brief_aktuell = brief_ziehen()

    if brief_aktuell is None:
        return

    ## Erst der geschlossene Umschlag, dann der Brief. brief_zustellen()
    ## kommt dazwischen: Angekommen ist die Sendung, sobald aufgemacht.
    call screen post_ankuendigung(brief_aktuell)

    $ brief_zustellen(brief_aktuell)

    call screen brief_bildschirm(brief_aktuell)

    $ brief_wahl = _return

    $ brief_folge = brief_beantworten(brief_aktuell, brief_wahl)

    if brief_folge:
        call screen brief_ausgang_bildschirm(brief_aktuell, brief_folge)

    $ brief_aktuell = None

    $ brief_folge = None

    return


################################################################################
## 11. Sprachprüfung erweitern
################################################################################
##
## herkunft.rpy prüft Ereignisse und Szenen, kapitel.rpy hat Kapitel- und
## Endtexte ergänzt, figuren.rpy die Briefe und Schicksalsmeldungen. Ab hier
## laufen auch die Sätze des Merkbuchs und die Umschlagtexte durch dieselbe
## Liste. minispiele.rpy (init 9) hängt sich danach an.

init 6 python:

    sprachpruefung_vor_merkbuch = sprachpruefung_durchfuehren

    def merkbuchtexte_sammeln():
        bestand = []
        for kennung, vorlagen in MERKBUCH_NOTIZEN.items():
            bestand.append(("Notiz " + kennung, texte_sammeln(vorlagen)))
        bestand.append(("Merkbuch Lage", texte_sammeln(MERKBUCH_LAGE)))
        bestand.append(("Merkbuch Nähe", texte_sammeln([v for _g, v in MERKBUCH_NAEHE_DA])))
        bestand.append(("Merkbuch Ferne", texte_sammeln([v for _g, v in MERKBUCH_NAEHE_FORT])))
        bestand.append(("Merkbuch Gegenseite", texte_sammeln(MERKBUCH_GEGENSEITE)))
        bestand.append(("Umschlag", texte_sammeln(POST_ANKUENDIGUNG)))
        return bestand

    def sprachpruefung_durchfuehren():
        funde = sprachpruefung_vor_merkbuch()
        for ort, texte in merkbuchtexte_sammeln():
            for satz in texte:
                klein = satz.lower()
                for begriff, begruendung in TABU_BEGRIFFE:
                    if begriff.lower() in klein:
                        funde.append(("Tabu", ort, begriff, begruendung, satz[:120]))
                for begriff, begruendung in PRUEF_BEGRIFFE:
                    if begriff.lower() in klein:
                        funde.append(("Prüfen", ort, begriff, begruendung, satz[:120]))
        return funde

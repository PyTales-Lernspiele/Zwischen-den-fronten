################################################################################
##
##  minispiele.rpy
##
##  Paket 5: Minispiele und Mikro-Interaktionen ("Einlagen")
##
##  Vier kurze Handgriffe, die den Alltag nicht erzählen, sondern ausführen
##  lassen. Jede Einlage dauert unter neunzig Sekunden, wird ausschließlich
##  mit der Maus bedient und endet mit zwei Sätzen historischer Einordnung.
##
##      1. Grundbegriffe    Konstanten, Klasse, keine Zugriffe nach außen
##      2. Inhalte          Briefbogen, Portionen, Höfe, Traglast
##      3. Bestand          die vier Einlagen und ihre Bedingungen
##      4. Vorbereitung     alle Würfe fallen VOR dem Bildschirm
##      5. Auswertung       Ergebnis -> Sätze, Werte, Bindung, Protokoll
##      6. Ziehung          wann eine Einlage kommt und wann nicht
##      7. Zustand          Variablen und Rücksetzung
##      8. Stile
##      9. Bildschirme
##     10. Ablauf           Einbindung über config.label_overrides
##     11. Einlagenprobe    Werkzeug für die Entwicklung
##     12. Sprachprüfung erweitern
##
##  GRUNDSÄTZE, DIE IN DIESER DATEI GELTEN
##  - Steuerung ausschließlich mit der Maus. Keine key-Anweisungen.
##  - Ton nur als Umgebungsklang. Seit Paket 8, Schritt 2.6 legen
##    ereignis_spielen_mit_einlage und einlage_spielen den Klang des Ortes an
##    (ortsklang_setzen). Sonst nichts: kein Klick beim Streichen, kein
##    Klang beim Absenden, keine Musik. An der Front und in der Etappe
##    verwirft ton_spielen() Musik hart.
##  - Keine Gewonnen-Wertung. Es gibt keine Punkte, keinen Haken, kein
##    "richtig". Der Bildschirm nach der Einlage sagt, was geschehen ist,
##    nicht, wie gut es war.
##  - Kein Schießen, kein Zielen, kein Geschicklichkeitstest. Alle vier
##    Einlagen sind Einteilungs- und Abwägungshandgriffe.
##  - Keine Zeitmessung in Sekunden. Druck entsteht durch Knappheit
##    (acht Striche, sieben Riemen, ein letzter Zug), nicht durch eine Uhr.
##    Wer langsam liest, wird nicht bestraft.
##  - Varianten laufen über merkmale, aktueller_pfad und die abstrakten
##    Nebenfiguren, niemals über Personennamen.
##  - Keine Begriffe aus der NS-Zeit. Abschnitt 12 hängt den gesamten
##    Textbestand dieser Datei in die vorhandene Sprachprüfung.
##
##  ABHÄNGIGKEITEN
##  gui.rpy     (init -50)  Farben, Rahmen, Schriften
##  script.rpy  (init -20)  Werte, Protokoll, EREIGNIS_INDEX
##  dialoge.rpy (init  -5)  variante(), Nebenfiguren
##  herkunft.rpy(init   2)  gebeugt(), Sprachprüfung
##  kapitel.rpy (init   2)  KAPITEL_JAHRE 1914 bis 1919
##  figuren.rpy (init   3)  figur_name(), figur_setzen(), briefwelt()
##  merkbuch.rpy(init   6)  Sprachprüfung in der zuletzt erweiterten Fassung
##  Diese Datei hängt sich mit init -6, init 7, init 8 und init 9 dahinter.
##
##  STAND UND OFFENE ABHÄNGIGKEIT
##  Die Einlagen hängen sich an vorhandene Ereignisse an (Abschnitt 3).
##  Für 1917 und 1918 sind Jahre und Bedingungen bereits eingetragen,
##  gezogen werden können sie dort aber erst, wenn Paket 7 den
##  Ereignisbestand dieser Jahre gefüllt hat: Ein Kapitel ohne Ereignis
##  läuft nicht an, und eine Einlage folgt immer auf ein Ereignis.
##
################################################################################


################################################################################
## 1. Grundbegriffe
################################################################################
##
## init -6 läuft nach den Konstanten aus merkbuch.rpy (init -7) und vor
## allen Beständen. Hier stehen nur die Klasse und die Stellschrauben.

init -6 python:

    ## Wie oft eine Einlage überhaupt vorkommen darf ###########################
    ##
    ## Eine Einlage ist ein Handgriff, kein Kapitel. Kommt sie zu oft,
    ## wird aus dem Alltag ein Aufgabenheft. Die Zahlen sind bewusst
    ## niedrig: Im kurzen Verlauf gibt es dreizehn Ziehungen insgesamt, im
    ## langen einunddreißig (KAPITEL_ZIEHUNGEN in kapitel.rpy, Abschnitt 2;
    ## die Zahlen im Kommentar hier standen bis Paket 5 auf 9 und 22 und
    ## stammten aus der Zeit vor Paket 3).

    EINLAGEN_JE_KAPITEL = {"kurz": 1, "lang": 2}

    ## So viele Ereignisse müssen zwischen zwei Einlagen liegen.
    EINLAGE_ABSTAND = 2

    ## Chance in Prozent, dass bei erfüllter Bedingung wirklich eine
    ## Einlage kommt. Anschlusseinlagen (Abschnitt 3) umgehen diesen Wurf.
    ##
    ## SEIT PAKET 5, SCHRITT 3: 30 statt 45. Der Grund ist gemessen, nicht
    ## geschätzt. Probe 4 weist die Verschiebung der vier Werte seit diesem
    ## Schritt nach Quelle getrennt aus, und dabei kam heraus, was vorher
    ## niemand sehen konnte: EINE EINLAGE VERSCHIEBT DIE WERTE VIER- BIS
    ## FÜNFMAL SO STARK WIE EIN EREIGNIS.
    ##
    ## Gerechnet über alle Eingaben aus EINLAGE_PROBEWERTE, je Vorgang:
    ##
    ##   rotstift            aufmerksamkeit +1,8   rueckhalt -1,6
    ##   tornister           belastung      +2,2   aufmerksamkeit +1,4
    ##   hamsterfahrt        belastung      +1,4   versorgung     +1,0
    ##   versorgungsantrag   aufmerksamkeit +1,0
    ##   portionen           rueckhalt      +1,0   belastung      +0,8
    ##
    ##   ein Ereignis, Mittel über alle Optionen aller Pfade:
    ##                       belastung      +0,3   aufmerksamkeit +0,3
    ##
    ## Bei 45 Prozent kam auf jede dritte Ziehung eine Einlage, und die
    ## Einlagen trugen damit rund ein Drittel des gesamten Werteverbrauchs
    ## eines Durchgangs - bei einem Achtel der Inhalte. Mit 30 Prozent
    ## bleiben im kurzen Verlauf etwa zwei Einlagen und im langen etwa
    ## fünf; jedes Kapitel kann weiterhin eine haben, denn
    ## EINLAGEN_JE_KAPITEL ist eine Obergrenze und kein Ziel.
    ##
    ## NICHT geändert sind die Auswertungen selbst. Sie sind Inhalt und
    ## gehören nicht in einen Zahlendurchgang; dass rotstift und tornister
    ## teuer sind, ist sachlich richtig. Nur ihre Häufigkeit ist eine Zahl.
    EINLAGE_CHANCE = 30

    ## Nach diesen Ereignissen kommt niemals eine Einlage. Es sind die
    ## Einstiegsszenen aus herkunft.rpy: Sie laufen vor der Hauptschleife,
    ## und dort hat ein Handgriff nichts zu suchen.
    EINLAGE_NIE_NACH = [
        "einstieg_meldung",
        "einstieg_offizier",
        "einstieg_etappe",
        "einstieg_abschied",
        ## Seit Paket 5, Schritt 2: die Wahl am Wirtshaustisch. Sie läuft
        ## NACH der Hauptschleife, unmittelbar vor dem Lebenslauf. Ein
        ## Handgriff dazwischen nähme dem Schluss den Atem.
        "wirtshaus_wahl",
    ]

    ## Obergrenzen für die Wirkung einer einzelnen Einlage. Ein Handgriff
    ## darf einen Durchgang nicht kippen. Wer hier etwas ändert, prüft die
    ## Rechnung in Abschnitt 5 der kapitel.rpy nach.
    EINLAGE_HOECHSTWIRKUNG = 3

    class Einlage(object):
        """Ein kurzer Handgriff zwischen zwei Ereignissen.

        kennung       eindeutig, wird im Protokoll geführt
        titel         Überschrift auf dem Bildschirm
        bildschirm    Name des screens, der die Handhabung zeigt
        jahre         Liste der Jahre, in denen sie vorkommen darf
        pfad          "front", "etappe", "heimat", "beide" oder Liste
        ort           Ortsangabe für die Kopfleiste (Variantenwörterbuch)
        einleitung    zwei bis drei Sätze Lage (Variantenwörterbuch)
        anweisung     was zu tun ist (Variantenwörterbuch)
        einordnung    GENAU ZWEI SÄTZE historische Einordnung
                      (Variantenwörterbuch erlaubt)
        anschluss     Kennungen von Ereignissen, nach denen sie unmittelbar
                      folgen darf, ohne Zufallswurf
        braucht       Merkmale, die vorliegen müssen
        verbietet     Merkmale, die sie ausschließen
        gewicht       Chance bei der freien Ziehung
        merkmal       wird nach dem Spielen gesetzt (für Paket 6 bis 8)
        wiederholbar  darf mehrfach im Durchgang vorkommen
        quelle        Belegangabe, nur im Analysemodus sichtbar
        """

        def __init__(self, kennung, titel, bildschirm, jahre, pfad,
                     ort=None, einleitung=None, anweisung=None,
                     einordnung=None, anschluss=None, braucht=None,
                     verbietet=None, gewicht=10, merkmal=None,
                     wiederholbar=False, quelle=None):
            self.kennung = kennung
            self.titel = titel
            self.bildschirm = bildschirm
            self.jahre = jahre if jahre else []
            self.pfad = pfad_liste(pfad)
            self.ort = ort
            self.einleitung = einleitung
            self.anweisung = anweisung
            self.einordnung = einordnung
            self.anschluss = anschluss if anschluss else []
            self.braucht = braucht if braucht else []
            self.verbietet = verbietet if verbietet else []
            self.gewicht = gewicht
            self.merkmal = merkmal
            self.wiederholbar = wiederholbar
            self.quelle = quelle


################################################################################
## 2. Inhalte
################################################################################
##
## Alle vier Einlagen ziehen ihren Stoff aus diesem Abschnitt. Er enthält
## ausschließlich Text und Zahlen, keine Logik. Wer Inhalte ändern will,
## ändert hier und nirgends sonst.

init -6 python:

    ############################################################################
    ## 2.1 Der Rotstift: ein Briefbogen und die Vorschrift
    ############################################################################
    ##
    ## Jede Zeile trägt zwei Zahlen:
    ##
    ##   risiko   was passiert, wenn sie stehen bleibt. Sie beschreibt,
    ##            wie stark die Zeile gegen die Vorschrift verstößt.
    ##   naehe    was verloren geht, wenn sie gestrichen wird. Sie
    ##            beschreibt, wie viel von einem Menschen darin steckt.
    ##
    ## Die Zahlen stehen NICHT auf dem Bildschirm. Der Spieler sieht nur
    ## den Bogen und die Vorschrift daneben und muss selbst entscheiden,
    ## was worunter fällt. Genau das ist die Übung. Im Analysemodus werden
    ## die Marken eingeblendet, damit sich im Unterricht darüber reden lässt.

    BRIEFBOGEN = {

        ## Der Bogen aus dem Feld. Er gilt für Front und Etappe und wird
        ## in der Offiziersfassung derselbe Bogen bleiben: Dann liegt er
        ## nur auf einem anderen Tisch.
        "front": [
            {"text": "Wir liegen seit Dienstag in dem Abschnitt vor dem Dorf mit der zerschossenen Kirche.",
             "risiko": 2, "naehe": 0, "marke": "Standort"},
            {"text": "Von den zweihundert, die im August ausgerückt sind, sind noch einundsechzig hier.",
             "risiko": 2, "naehe": 1, "marke": "Verluste"},
            {"text": "Freitag früh geht es wieder vor, der Befehl dazu ist gestern gekommen.",
             "risiko": 3, "naehe": 0, "marke": "Absicht"},
            {"text": "Wenn ich die Füße nicht mehr spüre, denke ich an den Ofen in der Küche.",
             "risiko": 0, "naehe": 2, "marke": ""},
            {"text": "Sag dem Kleinen, er soll mir etwas malen, ich hänge es über meinen Platz.",
             "risiko": 0, "naehe": 2, "marke": ""},
            {"text": "Der Hauptmann lässt bei Regen exerzieren, und über das Essen schreibe ich lieber nichts.",
             "risiko": 1, "naehe": 1, "marke": "Vorgesetzte"},
        ],

        ## Der Bogen aus der Etappe. SEIT PAKET 5, SCHRITT 1, TEIL B.
        ## Vorher bekam die Etappe den Frontbogen, und die Uebung wurde
        ## dadurch falsch: Wer im Graben liegt, verraet mit dem Standort
        ## eine Stellung; wer am Bahnhof sitzt, verraet mit Zuegen,
        ## Ladungen und Zeiten den ganzen Nachschub. Genau das war die
        ## empfindlichste Auskunft ueberhaupt.
        ##
        ## Die Summen sind bewusst dieselben wie beim Frontbogen -
        ## Risiko 8, Naehe 6 -, damit die Einlage in jeder Welt gleich
        ## schwer bleibt.
        "etappe": [
            {"text": "Unser Bahnhof liegt vier Stunden hinter der vordersten Stellung.",
             "risiko": 2, "naehe": 0, "marke": "Standort"},
            {"text": "In dieser Woche sind achtzehn Munitionszüge durchgegangen, und ich habe jeden gezählt.",
             "risiko": 2, "naehe": 1, "marke": "Nachschub"},
            {"text": "Am Dienstag kommen die Verwundeten von einem Angriff, der noch gar nicht begonnen hat.",
             "risiko": 3, "naehe": 0, "marke": "Absicht"},
            {"text": "Wenn ich abends die Bücher zumache, rieche ich immer noch Kohle in den Haaren.",
             "risiko": 0, "naehe": 2, "marke": ""},
            {"text": "Sag dem Kleinen, ich habe hier einen Jungen gesehen, der aussieht wie er.",
             "risiko": 0, "naehe": 2, "marke": ""},
            {"text": "Der Zahlmeister lässt zweimal zählen, und über das Essen schreibe ich lieber nichts.",
             "risiko": 1, "naehe": 1, "marke": "Vorgesetzte"},
        ],

        ## Der Bogen aus der Heimat. Er geht in die andere Richtung, wird
        ## aber ebenso gelesen: Der Postverkehr im Inland wurde
        ## stichprobenweise überwacht.
        "heimat": [
            {"text": "Bei Krüger gab es heute wieder nichts, ich stehe seit halb fünf an und komme ohne Brot zurück.",
             "risiko": 2, "naehe": 1, "marke": "Versorgung"},
            {"text": "In der Halle heißt es, im Frühjahr wird die Arbeit niedergelegt, wenn die Zuteilung noch einmal gekürzt wird.",
             "risiko": 3, "naehe": 0, "marke": "Unruhen"},
            {"text": "Schreib mir, wo ihr liegt. Wir finden es auf keiner Karte.",
             "risiko": 2, "naehe": 1, "marke": "Standort"},
            {"text": "Das Kind hat gestern gelacht, als der Kanarienvogel der Nachbarin gesungen hat.",
             "risiko": 0, "naehe": 2, "marke": ""},
            {"text": "Deine Jacke ist ausgebessert. Sie hängt an ihrem Platz neben der Tür.",
             "risiko": 0, "naehe": 2, "marke": ""},
            {"text": "Man sagt, ich soll nicht klagen, weil ihr es schwerer habt. Ich klage trotzdem.",
             "risiko": 1, "naehe": 2, "marke": "Stimmung"},
        ],
    }

    ## Die Vorschrift steht neben dem Bogen und ist der einzige Hinweis,
    ## den der Spieler bekommt. Sie ist knapp gehalten, weil die
    ## zeitgenössischen Anschläge ebenfalls knapp waren.
    BRIEF_VORSCHRIFT = {
        "front": [
            "Nicht mitzuteilen sind:",
            "Standort und Truppenteil",
            "Stärke, Verluste, Ersatz",
            "Absichten und Zeitpunkte",
            "alles, was den Weg des Briefes verrät",
        ],
        "etappe": [
            "Nicht mitzuteilen sind:",
            "Bahnhöfe, Strecken und Fahrpläne",
            "Art und Menge der Ladungen",
            "Zeitpunkte von Transporten",
            "alles, was den Weg des Briefes verrät",
        ],
        "heimat": [
            "Der Anschlag am Postamt bittet:",
            "keine Klagen an die Front",
            "keine Gerüchte weitergeben",
            "nicht nach dem Standort fragen",
            "Sendungen werden stichprobenweise geöffnet",
        ],
    }

    ############################################################################
    ## 2.1b Der Antrag von 1919: was du angibst
    ############################################################################
    ##
    ## SEIT PAKET 5, SCHRITT 2. Derselbe Handgriff wie beim Rotstift, und
    ## das mit Absicht: ein Bogen, Zeilen, die man stehen lässt oder
    ## streicht, eine Vorschrift daneben. 1914 streicht man, was der
    ## Gegner nicht wissen soll. 1919 streicht man, was das Amt nicht
    ## wissen soll. Die Spielerin merkt an der eigenen Hand, dass das
    ## dieselbe Bewegung ist.
    ##
    ## Der Antrag geht an das Wohlfahrtsamt und gilt auf allen drei
    ## Pfaden: Erwerbslosenfürsorge gab es seit dem November 1918 für
    ## Heimkehrer wie für Entlassene aus der Kriegswirtschaft, und sie
    ## war von Anfang an an eine Bedürftigkeitsprüfung gebunden. Deshalb
    ## braucht dieser Bogen keine drei Weltfassungen: Die Fragen sind für
    ## alle dieselben.
    ##
    ##   satz      um wie viel die Angabe die Unterstützung KÜRZT.
    ##             Eine negative Zahl heisst: Diese Angabe erhöht sie.
    ##   pruefung  wie sehr das Verschweigen auffällt, wenn geprüft wird.
    ##
    ## Die letzte Zeile ist der Prüfstein der Einlage. Wer sie streicht,
    ## verschweigt etwas, das ihm GENÜTZT hätte - und büsst dafür
    ## doppelt. Ohne sie wäre "alles streichen" die richtige Antwort, und
    ## damit wäre nichts zu entscheiden.

    ANTRAGSBOGEN = [
        {"text": "Im Haushalt lebt eine weitere Person mit eigenem Verdienst.",
         "satz": 2, "pruefung": 2, "marke": "Einkommen"},
        {"text": "Ich nähe abends auf eigene Rechnung, unregelmäßig und wenig.",
         "satz": 2, "pruefung": 2, "marke": "Nebenverdienst"},
        {"text": "Im Schrank steht eine Uhr, die meinem Vater gehört hat.",
         "satz": 1, "pruefung": 1, "marke": "Vermögen"},
        {"text": "Von den zwei Zimmern ist eines seit dem Winter untervermietet.",
         "satz": 2, "pruefung": 3, "marke": "Untermiete"},
        {"text": "Der Arzt hält mich für arbeitsfähig, sobald der Husten weggeht.",
         "satz": 2, "pruefung": 1, "marke": "Arbeitsfähigkeit"},
        {"text": "Für zwei Kinder unter vierzehn sorge ich allein.",
         "satz": -2, "pruefung": 0, "marke": "Unterhaltspflicht"},
    ]

    ANTRAG_VORSCHRIFT = [
        "Anzugeben sind:",
        "alle Einkünfte des Haushalts",
        "Vermögen und Wertgegenstände",
        "Einnahmen aus Untervermietung",
        "unrichtige Angaben werden zurückgefordert",
    ]

    ############################################################################
    ## 2.2 Acht Striche: wer wie viel bekommt
    ############################################################################
    ##
    ## Acht Teile, vier Empfänger, kein Rest. Die Empfänger sind nicht
    ## Personen, sondern Rollen: Sie kommen aus dem Nebenfigurenbestand
    ## und heißen an der Front anders als in der Heimat, ohne dass hier
    ## ein Name stünde.

    PORTIONEN_GESAMT = 8

    PORTIONEN_EMPFAENGER = [
        {"kennung": "selbst",
         "name": {"standard": "Du selbst"},
         "zusatz": {"front": "Seit gestern Mittag nichts.",
                    "etappe": "Seit der Ausgabe gestern nichts.",
                    "heimat": "Seit gestern Mittag nichts."}},
        {"kennung": "kind",
         "name": None,
         "zusatz": None},
        {"kennung": "naechste",
         "name": None,
         "zusatz": None},
        {"kennung": "vorrat",
         "name": {"front": "In den Brotbeutel", "etappe": "In den Spind",
                  "heimat": "In den Schrank"},
         "zusatz": {"front": "Für die Tage, an denen nichts nach vorn kommt.",
                    "etappe": "Für die Tage, an denen kein Zug ankommt.",
                    "heimat": "Für die Tage, an denen die Ausgabe ausfällt."}},
    ]

    ############################################################################
    ## 2.2b Die Zustandssätze: Gesichter statt Felder
    ############################################################################
    ##
    ## PAKET 7, SCHRITT 2, TEIL B.1. Vorher stand neben jedem Empfänger eine
    ## Zahl und ein Satz, der sich nie änderte. Eine Zahl sagt einer
    ## Dreizehnjährigen nichts darüber, was drei Achtel Brot für ein Kind
    ## sind. Also sagt es der Empfänger selbst - aus seiner Sicht, nicht aus
    ## der Sicht der Verwaltung.
    ##
    ## DIE SCHWELLEN STEHEN NUR HIER. portionen_stufe() liest sie, und
    ## sowohl der Bildschirm als auch portionen_auswerten() fragen diese
    ## eine Funktion. Stünden sie zweimal da, liefen sie auseinander, und
    ## der Bildschirm würde etwas anderes versprechen, als die Auswertung
    ## einlöst.
    ##
    ## "selbst" hat vier Stufen statt drei. Die vierte ist der Grund, aus
    ## dem es diese Einlage gibt: Wer sich die Hälfte nimmt, wird gesehen.

    PORTIONEN_SCHWELLEN = {
        "selbst": [(4, "viel"), (2, "genug"), (1, "wenig"), (0, "nichts")],
        "kind": [(2, "genug"), (1, "wenig"), (0, "nichts")],
        "naechste": [(2, "genug"), (1, "wenig"), (0, "nichts")],
        "vorrat": [(3, "genug"), (1, "wenig"), (0, "nichts")],
    }

    PORTIONEN_ZUSTAND = {

        "selbst": {
            "nichts": {
                "front": "Du hast dir nichts genommen. Der letzte Bissen ist von gestern Mittag.",
                "etappe": "Du hast dir nichts genommen. Der letzte Bissen ist von gestern Mittag.",
                "heimat": "Du hast dir nichts genommen. Der letzte Bissen ist von gestern Mittag.",
            },
            "wenig": {
                "front": "Ein Stück. Es hält vor, bis der Posten wechselt.",
                "etappe": "Ein Stück. Es hält vor, bis die Schicht zu Ende ist.",
                "heimat": "Ein Stück. Es hält vor, bis das Wasser kocht.",
            },
            "genug": {
                "front": "Es reicht bis zum Abend. Danach denkst du wieder ans Essen.",
                "etappe": "Es reicht bis zum Abend. Danach denkst du wieder ans Essen.",
                "heimat": "Es reicht bis zum Abend. Danach denkst du wieder ans Essen.",
            },
            ## Der Satz, der die Entscheidung trägt. Er kündigt an, was die
            ## Auswertung danach einlöst, und wertet trotzdem nicht: Er sagt,
            ## was die anderen sehen, und nicht, ob das falsch ist.
            "viel": {
                "front": "Die Hälfte für dich. In der Gruppe sieht jeder, wie groß dein Stück ist.",
                "etappe": "Die Hälfte für dich. In der Baracke sieht jeder, wie groß dein Stück ist.",
                "heimat": "Die Hälfte für dich. Am Tisch sieht jeder, wie groß dein Stück ist.",
            },
        },

        "kind": {
            "nichts": {
                "front": "Er sieht auf den leeren Napf und sagt nichts.",
                "etappe": "Er sieht auf den leeren Napf und geht früher zurück.",
                "heimat": "Es sieht auf den leeren Teller und sagt nichts.",
            },
            "wenig": {
                "front": "Zwei Bissen, dann sieht er wieder auf den Laib.",
                "etappe": "Zwei Bissen, dann sieht er wieder auf den Laib.",
                "heimat": "Zwei Bissen, dann sieht es wieder auf den Laib.",
            },
            "genug": {
                "front": "Er isst zu schnell und bedankt sich zweimal.",
                "etappe": "Er isst im Stehen und bedankt sich an der Tür.",
                "heimat": "Es isst zu schnell und fragt nach morgen.",
            },
        },

        "naechste": {
            "nichts": {
                "front": "Er sieht kurz auf deinen Napf und dann weg.",
                "etappe": "Er sieht kurz auf deinen Napf und dann in sein Buch.",
                "heimat": "Sie grüßt im Treppenhaus, aber kürzer als sonst.",
            },
            "wenig": {
                "front": "Er nimmt es und sagt, das sei schon zu viel.",
                "etappe": "Er nimmt es und sagt, das sei schon zu viel.",
                "heimat": "Sie nimmt es und sagt, das sei schon zu viel.",
            },
            "genug": {
                "front": "Er steckt es ein für später. Am Abend liegen zwei Zigaretten auf deinem Tornister.",
                "etappe": "Er steckt es ein für später. Am Abend liegen zwei Bögen Papier auf deinem Tisch.",
                "heimat": "Sie nimmt es mit hinauf. Am nächsten Tag steht ein Topf vor deiner Tür.",
            },
        },

        "vorrat": {
            "nichts": {
                "front": "Der Brotbeutel bleibt leer.",
                "etappe": "Der Spind bleibt leer.",
                "heimat": "Das Fach im Schrank bleibt leer.",
            },
            "wenig": {
                "front": "Ein Rest, der einen Tag hält.",
                "etappe": "Ein Rest, der einen Tag hält.",
                "heimat": "Ein Rest, der einen Tag hält.",
            },
            "genug": {
                "front": "Genug für den Tag, an dem nichts nach vorn kommt.",
                "etappe": "Genug für den Tag, an dem kein Zug ankommt.",
                "heimat": "Genug für den Tag, an dem die Ausgabe ausfällt.",
            },
        },
    }

    ############################################################################
    ## 2.3 Die Fahrt aufs Land: Tauschgut und Höfe
    ############################################################################
    ##
    ## Es wird nicht mit Geld gehandelt, sondern mit Sachen. Das ist keine
    ## Vereinfachung für Dreizehnjährige, sondern der historische Normalfall:
    ## Gegen amtliche Preise gab niemand etwas her, gegen Seife, Petroleum
    ## und Silber schon.
    ##
    ## Jedes Stück trägt einen Tauschwert (was der Hof dafür gibt) und
    ## einen Satz, der sagt, was sein Fehlen zu Hause bedeutet.

    TAUSCHGUT = {

        "standard": [
            {"name": "ein Stück Kernseife", "wert": 1,
             "folge": "Gewaschen wird jetzt mit Sand und kaltem Wasser."},
            {"name": "die Petroleumkanne", "wert": 2,
             "folge": "Die Abende beginnen jetzt, wenn es dunkel wird."},
            {"name": "ein Bettlaken", "wert": 2,
             "folge": "Im Bett liegt jetzt der Mantel obenauf."},
            {"name": "der silberne Löffel vom Hochzeitstisch", "wert": 3,
             "folge": "Er hat zwölf Jahre in der Schublade gelegen."},
        ],

        "buergertum": [
            {"name": "zwei Paar Lederhandschuhe", "wert": 1,
             "folge": "Für den Weg zur Ausgabestelle reichen auch Wollfäustlinge."},
            {"name": "eine Flasche Kognak", "wert": 2,
             "folge": "Sie war für die Rückkehr aufgehoben."},
            {"name": "Tischwäsche aus der Aussteuer", "wert": 2,
             "folge": "Der Tisch bleibt jetzt blank."},
            {"name": "die Taschenuhr deines Vaters", "wert": 3,
             "folge": "Du hörst sie noch, wenn du daran denkst."},
        ],

        "arbeiterschaft": [
            {"name": "zwei Stück Kernseife", "wert": 1,
             "folge": "Gewaschen wird jetzt mit Sand und kaltem Wasser."},
            {"name": "die Petroleumkanne", "wert": 2,
             "folge": "Die Abende beginnen jetzt, wenn es dunkel wird."},
            {"name": "das gute Hemd", "wert": 2,
             "folge": "Zum Amt gehst du künftig im Arbeitszeug."},
            {"name": "der Ehering", "wert": 3,
             "folge": "Die Stelle am Finger ist heller als die Hand."},
        ],
    }

    ## Drei Höfe, in dieser Reihenfolge. Der Preis steigt, weil die
    ## Nachfrage steigt und weil der letzte Hof weiß, wann der Zug fährt.
    ## Zurück geht es nicht: Wer weitergeht, kann nicht zurückkommen.
    ## PAKET 7, SCHRITT 3, TEIL B.1 UND B.3.
    ##
    ## "uhr" ist die Zeit, zu der du an diesem Hof stehst. Sie läuft nicht
    ## mit, sie springt: Der Weg zum nächsten Hof kostet drei Stunden, und
    ## um sechs fährt der letzte Zug. Sie steht bei den Höfen und nicht im
    ## Bildschirm, weil sie zum Weg gehört und nicht zur Anzeige.
    ##
    ## "antwort" ist, was der Hof zu deinem Gebot sagt - vier Stufen, vom
    ## leeren Tisch bis zur Überzahlung. KEINE DER ZWÖLF ANTWORTEN BEWERTET
    ## DAS GEBOT. Sie zeigen, was der andere sieht und tut. Bei Überzahlung
    ## nimmt jeder Hof alles und sagt dazu einen Satz, an dem man merkt,
    ## dass er genau weiß, was er gerade tut - das ist der Punkt der
    ## Übung und keine Gemeinheit: Auf dem Land war die Ware knapp und der
    ## Städter in Eile, und beide wussten es.

    HAMSTER_HOEFE = [
        {"name": "Der erste Hof hinter dem Bahndamm",
         "verlangt": 2, "pfund": 10,
         "uhr": "9 Uhr",
         "gibt": "zehn Pfund Kartoffeln",
         "satz": "Die Bäuerin sagt, heute habe sie schon fünf weggeschickt.",
         "antwort": {
             "nichts": "Sie wartet, bis du etwas auf den Tisch legst. Sie hat Zeit.",
             "wenig": "Sie sieht darauf und sagt nichts. Es ist zu wenig, und ihr wisst es beide.",
             "genug": "Sie nickt und geht in die Kammer. Die Kartoffeln sind kalt und schwer.",
             "zuviel": "Sie nimmt alles und legt nichts dazu. „Nächste Woche bringen Sie wieder etwas“, sagt sie.",
         }},
        {"name": "Ein Hof am Ortsausgang",
         "verlangt": 3, "pfund": 12,
         "uhr": "12 Uhr",
         "gibt": "zehn Pfund Kartoffeln und vier Eier",
         "satz": "Der Bauer sieht auf die Uhr, bevor er den Preis nennt.",
         "antwort": {
             "nichts": "Er steht in der Tür und sieht an dir vorbei auf die Straße.",
             "wenig": "Er sieht auf deine Hände und dann auf die Uhr über der Tür.",
             "genug": "Er nimmt es und zählt die Eier zweimal ab. Beim zweiten Mal stimmt es.",
             "zuviel": "Er nimmt alles. „Sie haben noch einen Hof vor sich“, sagt er. „Da kostet es mehr.“",
         }},
        {"name": "Der letzte Hof vor dem Bahnhof",
         "verlangt": 5, "pfund": 14,
         "uhr": "15 Uhr",
         "gibt": "zwölf Pfund Kartoffeln und ein Stück Speck",
         "satz": "Er weiß, wann dein Zug fährt. Deshalb der Preis.",
         "antwort": {
             "nichts": "Er lehnt am Türrahmen und sagt, es sei spät für ein Geschäft.",
             "wenig": "Er hört zu und schüttelt den Kopf, ohne den Preis zu wiederholen.",
             "genug": "Er nimmt es und lädt den Sack selbst auf. Danach sieht er wieder auf die Uhr.",
             "zuviel": "Er nimmt alles. „Der Zug um sechs ist der letzte“, sagt er. „Das wissen wir beide.“",
         }},
    ]

    ## Der letzte Zug. Er steht auch in der Einleitung der Einlage; beide
    ## Stellen müssen dasselbe sagen.
    HAMSTER_LETZTER_ZUG = "18 Uhr"

    ## Ab dieser Menge fällt der Rucksack auf dem Bahnsteig auf.
    HAMSTER_AUFFAELLIG = 12

    ############################################################################
    ## 2.4 Was du trägst: der Tornister
    ############################################################################
    ##
    ## Zehn Riemen Last liegen auf dem Rücken, sieben lassen sich bis zum
    ## Abend tragen. Es muss also etwas in den Straßengraben. Ein Stück
    ## liegt nicht im Tornister, sondern daneben: Es gehört dem Jüngsten,
    ## der nicht mehr kann.

    TRAGLAST_GRENZE = 7

    TORNISTER_STUECKE = [
        {"kennung": "mantel", "name": "Der Mantel", "last": 2, "drin": True,
         "zusatz": "Nachts geht es unter zehn Grad."},
        {"kennung": "zeltbahn", "name": "Die Zeltbahn", "last": 2, "drin": True,
         "zusatz": "Dach über dem Kopf, wenn es keines gibt."},
        {"kennung": "kochgeschirr", "name": "Das Kochgeschirr", "last": 1, "drin": True,
         "zusatz": "Ohne Napf keine Ausgabe."},
        {"kennung": "portion", "name": "Die eiserne Portion", "last": 1, "drin": True,
         "zusatz": "Zwieback und zwei Büchsen. Sie gehört dem Heer."},
        {"kennung": "stiefel", "name": "Ersatzstiefel und Fußlappen", "last": 2, "drin": True,
         "zusatz": "Die alten sind seit gestern durch."},
        {"kennung": "briefe", "name": "Briefe und die Fotografie", "last": 1, "drin": True,
         "zusatz": "Papier wiegt fast nichts und drückt trotzdem."},
        {"kennung": "putzzeug", "name": "Nähzeug und Putzzeug", "last": 1, "drin": True,
         "zusatz": "Beim Appell wird das Gewehr angesehen."},
        {"kennung": "fremdes", "name": "Das Kochgeschirr des Jüngsten", "last": 1, "drin": False,
         "zusatz": "Er hat seit einer Stunde nichts mehr gesagt."},
    ]


################################################################################
## 3. Bestand: die vier Einlagen
################################################################################
##
## ZUR EINORDNUNG
## Jede Einlage endet mit genau zwei Sätzen. Zwei Sätze sind kurz genug,
## dass sie gelesen werden, und lang genug für eine Zahl und eine
## Einschränkung. Die Einlagenprobe in Abschnitt 11 zählt nach und meldet
## jede Einordnung, die mehr oder weniger als zwei Sätze hat.
##
## ZUR ANBINDUNG
## anschluss nennt Ereignisse, nach denen die Einlage unmittelbar folgen
## darf. Das ist der Regelfall: Der Handgriff sitzt dann in einer Lage,
## die gerade erzählt worden ist, und wirkt nicht wie eine Übungsaufgabe.
## Ohne Anschluss wird gewürfelt (Abschnitt 6).

init -6 python:

    EINLAGEN = [

        ########################################################################
        ## Der Rotstift
        ########################################################################
        ##
        ## Wirkt auf Verdacht und Einsamkeit. Es gibt keine richtige
        ## Menge an Strichen: Wer alles stehen lässt, schickt einen
        ## Brief, der ankommt, wie er ist, und fällt auf. Wer alles
        ## streicht, schickt einen Bogen, auf dem nichts mehr steht,
        ## das jemandem etwas bedeutet.

        Einlage(
            "rotstift", "Der Rotstift", "einlage_rotstift",
            [1914, 1915, 1916, 1917, 1918],
            "beide",
            ort={"front": "Grabenstellung", "etappe": "Etappenquartier",
                 "heimat": "Wohnviertel"},
            einleitung={
                "front:offizier": "Ein Klapptisch, zwei Kerzen, dreißig Briefe deiner Leute. Der Bataillonsbefehl sagt, du sollst sie durchsehen, bevor sie zur Feldpost gehen. Was du stehen lässt, steht auf deinem Namen.",
                "front": "Der Bogen ist voll. Um vier wird der Feldpostkasten geleert, und bevor du faltest, liest du noch einmal von oben.",
                ## Die Etappe streicht den ganzen Tag fremde Briefe. Ihr
                ## eigener ist deshalb der schwerste: Sie weiss vorher,
                ## was daran nicht durchkommt.
                "etappe": "Dein eigener Bogen liegt zuunterst im Stapel, den du heute durchgesehen hast. Um vier geht der Sack zum Zug. Du weißt genau, was du selbst streichen würdest.",
                "heimat": "Der Bogen liegt seit gestern Abend auf dem Tisch. Um sechs wird der Kasten an der Ecke geleert.",
            },
            anweisung={
                "front:offizier": "Streiche durch, was nicht hinausgehen darf. Was stehen bleibt, geht so ab.",
                "standard": "Streiche durch, was nicht hinausgehen soll. Was stehen bleibt, geht so ab.",
            },
            ## GEKÜRZT IN PAKET 6, SCHRITT 2 (Entscheidung 8 und 9).
            ## Genau zwei Sätze, jeder unter zwanzig Wörtern, zusammen
            ## höchstens fünfunddreißig. Was herausfällt, steht in
            ## quelle["vertiefung"] und geht damit nicht verloren - Paket 8,
            ## Schritt 3 nimmt es ins Glossar und in die Quellenkarte auf.
            einordnung={
                "front": "Die Feldpost beförderte Milliarden Sendungen; geprüft wurde nur stichprobenweise. Verboten war, was dem Gegner nützt: Standort, Truppenteil, Verluste, Bewegungen.",
                "etappe": "Die Briefprüfstellen lagen in der Etappe und nicht im Graben, und ihre Prüfer waren selbst Soldaten oder Beamte. Aus dem Gelesenen entstanden regelmäßige Stimmungsberichte; was ein einzelner Prüfer strich, blieb dagegen meist unvermerkt.",
                "heimat": "Auch die Post im Inland wurde stichprobenweise überwacht. Aus dem Gelesenen entstanden Berichte über die Stimmung der Bevölkerung.",
            },
            anschluss=["front_feldpost", "heimat_1914_post", "heimat_1916_zensur"],
            gewicht=12, merkmal="rotstift_gefuehrt", wiederholbar=True,
            quelle={
                "kurz": "Feldpost und Briefzensur 1914 bis 1918",
                "voll": "Deutsche Feldpost und militärische Briefzensur; "
                        "Deutsches Historisches Museum, LeMO, Kriegsalltag",
                "art": "darstellung",
                "einordnung": "Belegt sind der Umfang des Postverkehrs und die "
                              "stichprobenweise Prüfung, bis 1916 durch den "
                              "Vorgesetzten, danach durch eigene Zensurstellen. "
                              "Welche Zeilen ein einzelner Prüfer strich, ist "
                              "nur dort überliefert, wo der Bogen erhalten "
                              "blieb.",
                ## Aus der gekürzten Einordnung herausgenommen, Paket 6,
                ## Schritt 2. Bestimmt für Glossar und Quellenkarte.
                "vertiefung": {
                    "front": "Zwischen 1914 und 1918 waren es schätzungsweise "
                             "28,7 Milliarden Briefe und Karten. Bis 1916 "
                             "prüfte der nächste Vorgesetzte, danach eigens "
                             "eingerichtete Zensurstellen. Klagen über Essen "
                             "und Vorgesetzte gingen meist durch und landeten "
                             "in den Stimmungsberichten.",
                    "heimat": "Klagen über Hunger und Anstehen waren nicht "
                              "verboten, galten aber als schädlich für die "
                              "Stimmung der Truppe. Behörden und Zeitungen "
                              "baten deshalb immer wieder darum, aufmunternd "
                              "an die Front zu schreiben.",
                },
            }
        ),

        ########################################################################
        ## Acht Striche
        ########################################################################
        ##
        ## Wirkt auf Hunger und Einsamkeit. Die Rechnung geht nicht auf,
        ## und das ist der Punkt: Acht Teile reichen für vier Ansprüche
        ## nicht. Wer sich selbst versorgt, hält länger durch. Wer teilt,
        ## hat Menschen, die zurückteilen.

        Einlage(
            "portionen", "Acht Striche", "einlage_portionen",
            [1915, 1916, 1917, 1918],
            "beide",
            ort={"front": "Grabenstellung", "etappe": "Etappenquartier",
                 "heimat": "Wohnviertel"},
            einleitung={
                "front": "Die Feldküche ist um zwei Uhr nachts nach vorn gekommen. Ein Brot für die Gruppe, dazu Kaffee, der keiner ist. Du schneidest, die anderen sehen zu.",
                ## Die Lage der Etappe in einem Satz: mehr als vorn,
                ## weniger als auf dem Papier. Genau daraus entsteht das
                ## schlechte Gewissen, das dieser Pfad tragen soll.
                "etappe": "Die Ausgabe ist um sechs, und für die Baracke steht ein Brot auf dem Brett. Es ist mehr als vorn und weniger als auf dem Papier. Du ziehst acht Striche über den Laib.",
                "heimat": "Freitag, Ausgabe. Auf dem Tisch liegt, was die Karten für die Woche hergeben: ein Brot, ein Beutel Kartoffeln, ein Löffel Fett. Du ziehst mit dem Messer acht Striche über den Laib.",
            },
            anweisung={"standard": "Teile die acht Teile auf. Es bleibt nichts übrig, und es kommt nichts nach."},
            einordnung={
                ## Gekürzt in Paket 6, Schritt 2; der Rest steht in
                ## quelle["vertiefung"].
                "front": "Verpflegt wurde nicht der Einzelne, sondern die Gruppe. Die Feldküche kam meist bei Dunkelheit nach vorn.",
                "etappe": "In der Etappe war die Verpflegung besser als vorn und schlechter als auf dem Papier. Die Ausgabelisten nennen den Sollsatz je Kopf, nicht das, was am Ende im Kochgeschirr lag.",
                "heimat": "Seit Februar 1915 gab es in Berlin Brotkarten, bald im ganzen Reich. Im Februar 1917 deckte die Zuteilung noch etwa tausend Kilokalorien am Tag.",
            },
            anschluss=["heimat_brotschlange", "heimat_1915_brotkarte",
                       "front_ruhequartier", "front_1916_hunger"],
            gewicht=12, merkmal="geteilt", wiederholbar=True,
            quelle={
                "kurz": "Brotkarten und Brotbücher ab 1915",
                "voll": "Brotkarte und Rationierung ab Februar 1915; Deutsches "
                        "Historisches Museum, LeMO, Kriegsalltag",
                "art": "darstellung",
                "einordnung": "Belegt sind die zugeteilten Mengen und ihr Rückgang "
                              "bis zum Steckrübenwinter. Wie eine Gruppe oder "
                              "eine Familie das Zugeteilte untereinander "
                              "aufteilte, regelte keine Karte.",
                "vertiefung": {
                    "front": "Was die Feldküche brachte, wurde im Graben "
                             "aufgeteilt. Das Heer hatte bei der Zuteilung "
                             "Vorrang vor der Zivilbevölkerung; Soldaten auf "
                             "Urlaub waren deshalb oft besser genährt als "
                             "ihre eigene Familie.",
                    "heimat": "Berlin gab am 22. Februar 1915 als erste "
                              "deutsche Stadt Brotkarten aus, zunächst zwei "
                              "Kilogramm Brot je Woche und Kopf. Ab dem "
                              "1. März 1915 galt die Rationierung im ganzen "
                              "Reich, und die Mengen wurden bald gekürzt. "
                              "Tausend Kilokalorien sind weniger als die "
                              "Hälfte dessen, was ein erwachsener Mensch "
                              "braucht.",
                },
            }
        ),

        ########################################################################
        ## Die Fahrt aufs Land
        ########################################################################
        ##
        ## Wirkt auf Hunger und Verdacht. Der Preis steigt mit jedem Hof,
        ## und zurück geht es nicht. Am Bahnsteig steht mit einer
        ## vorgewürfelten Wahrscheinlichkeit eine Kontrolle; wie hoch sie
        ## ist, hängt davon ab, wie voll der Rucksack ist.
        ##
        ## Diese Einlage und das alte Ereignis heimat_hamsterfahrt
        ## erzählen dieselbe Fahrt. Abschnitt 6 sorgt dafür, dass nur
        ## eines von beiden vorkommt.

        Einlage(
            "hamsterfahrt", "Die Fahrt aufs Land", "einlage_hamsterfahrt",
            [1916, 1917, 1918],
            "heimat",
            ort={"heimat": "Landstraße"},
            einleitung={
                "heimat": "Sonntag, vier Uhr früh. Der Zug ist voll mit Leuten, die einander nicht ansehen. Ab der dritten Station stehen die Höfe an der Straße, und um sechs Uhr abends fährt der letzte Zug zurück.",
            },
            anweisung={"standard": "Biete an, was du dabeihast. Jeder Hof weiter kostet Zeit, und mit der Zeit steigt der Preis. Zurück geht es nicht."},
            ## Gekürzt in Paket 6, Schritt 2; der Rest steht in
            ## quelle["vertiefung"].
            einordnung={
                "heimat": "Der Kauf beim Bauern und die Ausfuhr aus dem Kreis waren verboten. Gefahren sind trotzdem Hunderttausende, vor allem nach dem Steckrübenwinter.",
            },
            gewicht=11, merkmal="gehamstert", verbietet=["landbevoelkerung"],
            quelle={
                "kurz": "Hamsterfahrten, Bergische Arbeiterstimme 1917",
                "voll": "Stadtarchiv Solingen, Bergische Arbeiterstimme 1917, "
                        "Berichte über Hamsterfahrten und Beschlagnahmen",
                "art": "zeitung",
                "einordnung": "Belegt sind das Verbot, bewirtschaftete "
                              "Lebensmittel aus dem Landkreis zu führen, und die "
                              "Beschlagnahme ohne Vergütung. Die Zeitung "
                              "berichtet, was aufgefallen ist, und nicht, wie "
                              "viele Rucksäcke durchkamen.",
                "vertiefung": {
                    "heimat": "Polizei und Gendarmerie kontrollierten "
                              "Bahnhöfe und Züge. Beschlagnahmt wurde ohne "
                              "Vergütung, was ohne Erlaubnis mitgeführt "
                              "wurde. In manchen Städten beteiligten sich die "
                              "Gemeinden sogar an der Organisation solcher "
                              "Fahrten.",
                },
            }
        ),

        ########################################################################
        ## Was du trägst
        ########################################################################
        ##
        ## Wirkt auf Erschöpfung, Hunger und Einsamkeit. Zehn Riemen Last,
        ## sieben tragbar. Ein achtes Stück liegt daneben und gehört
        ## jemand anderem.

        Einlage(
            "tornister", "Was du trägst", "einlage_tornister",
            [1914, 1915],
            ["front", "etappe"],
            ort={"front": "Landstraße", "etappe": "Landstraße"},
            einleitung={
                "front": "Rast am Straßenrand, zwanzig Minuten. Seit fünf Uhr früh sind es dreißig Kilometer, und es ist Mittag. Der Tornister drückt seit dem Morgen an derselben Stelle, und das wird heute nicht mehr besser.",
                ## Dieselbe Last, ein anderer Grund: Die Etappe marschiert
                ## nicht nach vorn, sie verlegt. Und ein Teil dessen, was
                ## auf dem Ruecken liegt, gehoert jemand anderem.
                "etappe": "Rast am Straßenrand, zwanzig Minuten. Die Kolonne verlegt das Magazin, und jeder trägt, was auf keinen Wagen passt. Auf dem Rücken hast du fremdes Gut und dein eigenes dazu.",
            },
            anweisung={"standard": "Nimm heraus, was du nicht bis zum Abend tragen willst. Was im Straßengraben bleibt, bleibt dort."},
            einordnung={
                ## Gekürzt in Paket 6, Schritt 2; der Rest steht in
                ## quelle["vertiefung"].
                "front": "Das volle Marschgepäck eines Infanteristen wog 25 bis 30 Kilogramm. Die eiserne Portion, also Zwieback und Büchsenkost, gehörte dem Heer.",
                "etappe": "Die Etappe verlegte Magazine und Werkstätten mit, wenn die Front sich verschob. Was dabei liegen blieb, galt als Verlust und musste im Buch erklärt werden.",
            },
            anschluss=["front_1914_marsch", "front_1914_schanzen"],
            gewicht=10, merkmal="tornister_erleichtert",
            quelle={
                "kurz": "Marschgepäck und eiserne Portion",
                "voll": "Kriegsverpflegungsvorschrift von 1901, Bestimmungen über "
                        "die eiserne Portion",
                "art": "gesetz",
                "einordnung": "Belegt sind der Inhalt der eisernen Portion und "
                              "das Verbot, sie ohne Befehl anzubrechen. Was "
                              "Männer auf dem Vormarsch tatsächlich in den "
                              "Straßengraben warfen, steht in keiner "
                              "Vorschrift.",
                ## PAKET 7, SCHRITT 3 ERGÄNZT DIE ETAPPENFASSUNG. Die
                ## Einlage läuft auf beiden Pfaden, die Vertiefung kannte
                ## aber nur die Front - auf der Etappe wäre in Paket 8 ein
                ## Glossareintrag über den Vormarsch von 1914 erschienen,
                ## und der handelt von einem anderen Marsch.
                "vertiefung": {
                    "front": "Auf dem Vormarsch im August 1914 lagen die "
                             "Straßengräben in Belgien und Nordfrankreich "
                             "voll mit weggeworfener Ausrüstung. Angebrochen "
                             "werden durfte die eiserne Portion nur auf "
                             "ausdrücklichen Befehl.",
                    "etappe": "Zur Etappe gehörten Magazine, Bäckereien, "
                              "Werkstätten und Lazarette. Sie zog mit, wenn "
                              "die Front sich verschob, und war dabei "
                              "zugleich Nachschubweg und Baustelle.",
                },
            }
        ),

        ########################################################################
        ## Was du angibst
        ########################################################################
        ##
        ## SEIT PAKET 5, SCHRITT 2. Die einzige Einlage des Epilogs, und
        ## sie gilt auf allen drei Pfaden: Erwerbslosenfürsorge gab es
        ## vom November 1918 an für Heimkehrer wie für Entlassene aus der
        ## Kriegswirtschaft, und sie war von Anfang an an eine
        ## Bedürftigkeitsprüfung gebunden.
        ##
        ## Sie benutzt den Bogenbildschirm des Rotstifts, und das ist der
        ## Punkt: 1914 streicht man, was der Gegner nicht wissen soll,
        ## 1919 streicht man, was das Amt nicht wissen soll. Dieselbe
        ## Bewegung, ein anderer Zweck. Niemand sagt das im Spiel.

        Einlage(
            "versorgungsantrag", "Was du angibst", "einlage_rotstift",
            [1919],
            "beide",
            ort={"front": "Wohlfahrtsamt", "etappe": "Wohlfahrtsamt",
                 "heimat": "Wohlfahrtsamt"},
            einleitung={
                "front": "Am Schalter bekommst du einen Bogen mit sechs Zeilen und einen Bleistift. Was du angibst, wird vom Satz abgezogen. Was du weglässt, prüft ein Beamter, wenn ihm danach ist.",
                "etappe": "Am Schalter bekommst du einen Bogen mit sechs Zeilen und einen Bleistift. Was du angibst, wird vom Satz abgezogen. Was du weglässt, prüft ein Beamter, wenn ihm danach ist.",
                "heimat": "Am Schalter bekommst du einen Bogen mit sechs Zeilen und einen Bleistift. Was du angibst, wird vom Satz abgezogen. Was du weglässt, prüft ein Beamter, wenn ihm danach ist.",
            },
            anweisung={"standard": "Streiche durch, was nicht auf dem Bogen stehen soll. Was stehen bleibt, gilt als angegeben."},
            einordnung={
                "front": "Die Erwerbslosenfürsorge vom November 1918 war keine Versicherung, sondern eine Unterstützung nach Bedürftigkeit. Wer sie bezog, musste Einkommen und Vermögen offenlegen und mit einer Nachprüfung rechnen.",
                "etappe": "Die Erwerbslosenfürsorge vom November 1918 war keine Versicherung, sondern eine Unterstützung nach Bedürftigkeit. Wer sie bezog, musste Einkommen und Vermögen offenlegen und mit einer Nachprüfung rechnen.",
                "heimat": "Die Erwerbslosenfürsorge vom November 1918 war keine Versicherung, sondern eine Unterstützung nach Bedürftigkeit. Frauen wurden vor Männern gestrichen, sobald ein Heimkehrer die Stelle beanspruchte.",
            },
            anschluss=["epilog_1919_werktor", "epilog_1919_versorgungsamt",
                       "epilog_1919_papiere"],
            ## wiederholbar, weil der lange Verlauf zwei Einlagen je
            ## Kapitel vorsieht und der Epilog nur diese eine hat. Es ist
            ## keine Notlösung: Die Erwerbslosenfürsorge verlangte eine
            ## regelmäßige Meldung, und der Bogen kam wieder.
            gewicht=12, merkmal="antrag_gestellt", wiederholbar=True,
            quelle={
                "kurz": "Erwerbslosenfürsorge und Bedürftigkeitsprüfung ab 1918",
                "voll": QUELLE_FEHLT,
                "art": "gesetz",
                "einordnung": "Gesucht wird die Verordnung über die "
                              "Erwerbslosenfürsorge aus dem November nach dem "
                              "Waffenstillstand samt den Ausführungs"
                              "bestimmungen. Sie nennt Sätze und Bedingungen, "
                              "nicht die Fragen, die der Beamte am Schalter "
                              "wirklich stellte.",
            }
        ),

    ]

    EINLAGE_INDEX = {}
    for _einlage in EINLAGEN:
        EINLAGE_INDEX[_einlage.kennung] = _einlage

    ## Umgekehrtes Verzeichnis: Ereignis -> Einlagen, die daran hängen.
    EINLAGE_ANSCHLUSS = {}
    for _einlage in EINLAGEN:
        for _kennung in _einlage.anschluss:
            EINLAGE_ANSCHLUSS.setdefault(_kennung, []).append(_einlage.kennung)


################################################################################
## 4. Vorbereitung
################################################################################
##
## WARUM ALLE WÜRFE HIER FALLEN
## Ein Ren'Py-Bildschirm wird bei jeder Bewegung neu berechnet. Wer darin
## würfelt, würfelt bei jedem Klick neu, und der Bauer würde bei jedem
## Mausschubser einen anderen Preis nennen. Deshalb fällt jeder Zufall
## dieser Datei genau einmal, bevor der Bildschirm erscheint, und liegt
## danach unveränderlich in einlage_lage.
##
## init 7 läuft nach merkbuch.rpy (init 6). Ab hier stehen figur_name,
## welttext, briefwelt und die Sprachprüfung in ihrer endgültigen Fassung
## zur Verfügung.

init 7 python:

    ## Texthilfen ##############################################################

    def einlage_holen(kennung):
        return EINLAGE_INDEX.get(kennung)

    def einlage_text(vorgaben, standard=""):
        """Löst ein Variantenwörterbuch auf.

        Nutzt variante() aus dialoge.rpy: Erst Pfad und Merkmal zusammen,
        dann das Merkmal, dann der Pfad, zuletzt "standard". Die Etappe
        fällt dabei auf die Frontfassung zurück.
        """
        if vorgaben is None:
            return standard
        ergebnis = variante(vorgaben, standard)
        if isinstance(ergebnis, dict):
            ergebnis = jahrestext(ergebnis, aktuelles_jahr)
        return ergebnis

    def einlage_titel(kennung):
        vorlage = einlage_holen(kennung)
        return vorlage.titel if vorlage else ""

    def einlage_ort(kennung):
        vorlage = einlage_holen(kennung)
        if vorlage is None or vorlage.ort is None:
            return ort_text()
        return einlage_text(vorlage.ort, ort_text())

    def einlage_einleitung(kennung):
        vorlage = einlage_holen(kennung)
        return einlage_text(vorlage.einleitung) if vorlage else ""

    def einlage_anweisung(kennung):
        vorlage = einlage_holen(kennung)
        return einlage_text(vorlage.anweisung) if vorlage else ""

    def einlage_einordnung(kennung):
        vorlage = einlage_holen(kennung)
        return einlage_text(vorlage.einordnung) if vorlage else ""

    ## Ersatz für fehlende Nebenfiguren ########################################
    ##
    ## Wenn die Rolle, mit der geteilt werden soll, nicht mehr da ist
    ## (gefallen, verschleppt, fortgezogen), tritt jemand anderes an den
    ## Tisch. Geteilt wird dann trotzdem, nur ohne Bindung: Ein fremdes
    ## Gesicht hebt keine Verbundenheit.

    ERSATZ_EMPFAENGER = {
        "kind": {"front": "Ein Neuer in der Gruppe",
                 "etappe": "Ein Neuer von der Rampe",
                 "heimat": "Das Kind aus dem Vorderhaus"},
        "naechste": {"front": "Ein Mann aus der Gruppe",
                     "etappe": "Jemand von der Nachtschicht",
                     "heimat": "Die Frau aus dem Seitenflügel"},
    }

    def empfaenger_verfuegbar(kennung):
        try:
            if not figur_lebt(kennung):
                return False
            if figur_ist_fort(kennung):
                return False
        except NameError:
            return False
        return True

    ## Vorbereitung je Einlage #################################################

    ## Die Winkel des Rotstifts ################################################
    ##
    ## PAKET 7, SCHRITT 2: Balken und Stempel liegen schräg, und zwar bei
    ## jedem Neuzeichnen gleich schräg. Deshalb fallen die Würfe HIER und
    ## nicht im Bildschirm: Ein Screen wird bei jeder Mausbewegung neu
    ## gebaut, und ein Winkel, der dort entsteht, zittert.
    ##
    ## Je Zeile ein eigener Winkel. Acht gleich geneigte Balken sähen aus,
    ## als hätte jemand ein Lineal angelegt; die Bedingung des Auftrags -
    ## einmal gewürfelt, in einlage_lage, nicht im Screen - ist damit
    ## genauso erfüllt.

    BALKEN_WINKEL = (0.4, 1.2)
    STEMPEL_WINKEL = (6.0, 8.0)

    def balkenwinkel_wuerfeln(anzahl):
        return [round(renpy.random.uniform(*BALKEN_WINKEL), 2)
                * (1 if renpy.random.randint(0, 1) else -1)
                for _ in range(anzahl)]

    ## Wer stempelt, und wer nicht ##############################################
    ##
    ## "GEPRÜFT" steht auf dem Bogen nur dort, wo ihn wirklich eine
    ## Prüfstelle in der Hand hat: beim Offizier, der die Post seiner Leute
    ## durchsieht, und in der Etappe, wo die Spielerin selbst in der
    ## Briefprüfstelle sitzt und ihr eigener Bogen zuunterst im Stapel liegt.
    ##
    ## Auf dem Küchentisch in der Heimat und im Unterstand an der Front
    ## stempelt niemand. Ein Prüfstempel auf einem Brief, den man gerade
    ## selbst schreibt, wäre schlicht falsch - und ein falsches Dokument ist
    ## in einem Geschichtsspiel teurer als ein fehlendes Bild.
    ##
    ## NICHT "Zensiert": Das Wort stand nicht auf den Stempeln der
    ## Feldpostprüfstellen.

    def rotstift_stempel(welt, fremd):
        if fremd or welt == "etappe":
            return "Geprüft"
        return None

    def rotstift_vorbereiten():
        welt = briefwelt()
        zeilen = list(BRIEFBOGEN[welt])
        fremd = bool(hat_merkmal("offizier")) and welt == "front"
        return {
            "welt": welt,
            "zeilen": zeilen,
            "vorschrift": list(BRIEF_VORSCHRIFT[welt]),
            ## Der Offizier prüft fremde Post. Der Bogen ist derselbe,
            ## der Tisch ein anderer.
            "fremder_bogen": fremd,
            "balkenwinkel": balkenwinkel_wuerfeln(len(zeilen)),
            "stempel": rotstift_stempel(welt, fremd),
            "stempelwinkel": round(renpy.random.uniform(*STEMPEL_WINKEL), 2),
        }

    def portionen_vorbereiten():
        empfaenger = []
        for eintrag in PORTIONEN_EMPFAENGER:
            kennung = eintrag["kennung"]
            if eintrag["name"] is None:
                if empfaenger_verfuegbar(kennung):
                    name = figur_name(kennung)
                    zusatz = figur_zusatz(kennung)
                    bindung = True
                else:
                    name = welttext(ERSATZ_EMPFAENGER[kennung])
                    zusatz = "Du kennst kaum den Namen."
                    bindung = False
            else:
                name = welttext(eintrag["name"])
                zusatz = welttext(eintrag["zusatz"])
                bindung = False
            empfaenger.append({
                "kennung": kennung,
                "name": name,
                "zusatz": zusatz,
                "bindung": bindung,
            })
        return {
            "empfaenger": empfaenger,
            "gesamt": PORTIONEN_GESAMT,
            ## Kriegsbrot mit Kartoffelmehl schimmelte schnell. Wer zu
            ## viel zurücklegt, riskiert, dass es verdirbt.
            "schimmel": renpy.random.randint(1, 100) <= 45,
        }

    def hamsterfahrt_vorbereiten():
        return {
            "gueter": list(variante(TAUSCHGUT)),
            "hoefe": list(HAMSTER_HOEFE),
            ## Zwei Würfe, die erst am Bahnsteig gebraucht werden. Sie
            ## fallen trotzdem jetzt, damit sie sich nicht bei jedem
            ## Mausklick ändern.
            "kontrollwurf": renpy.random.randint(1, 100),
            "entkommenwurf": renpy.random.randint(1, 100),
        }

    def tornister_vorbereiten():
        return {
            "stuecke": list(TORNISTER_STUECKE),
            "grenze": TRAGLAST_GRENZE,
        }

    ## Derselbe Bildschirm wie beim Rotstift, ein anderer Bogen. Kopf- und
    ## Schlusszeile kommen hier aus der Lage und nicht aus dem
    ## Feldpostbrief: Ein Antrag hat keinen Gruss am Ende, sondern eine
    ## Unterschrift.
    def versorgungsantrag_vorbereiten():
        return {
            "zeilen": list(ANTRAGSBOGEN),
            "vorschrift": list(ANTRAG_VORSCHRIFT),
            "fremder_bogen": False,
            "kopfzeile": "Antrag auf Unterstützung, den 4. Februar 1919",
            "schlusszeile": "Die Richtigkeit der Angaben versichere ich",
            "knopf": "Abgeben",
            ## Derselbe Bildschirm, also dieselben Winkel. Ein Amt stempelt
            ## erst, wenn der Antrag eingegangen ist - beim Ausfüllen steht
            ## dort noch nichts.
            "balkenwinkel": balkenwinkel_wuerfeln(len(ANTRAGSBOGEN)),
            "stempel": None,
            "stempelwinkel": round(renpy.random.uniform(*STEMPEL_WINKEL), 2),
        }

    EINLAGE_VORBEREITEN = {
        "rotstift": rotstift_vorbereiten,
        "portionen": portionen_vorbereiten,
        "hamsterfahrt": hamsterfahrt_vorbereiten,
        "tornister": tornister_vorbereiten,
        "versorgungsantrag": versorgungsantrag_vorbereiten,
    }

    def einlage_vorbereiten(kennung):
        global einlage_lage, einlage_aktuell, einlage_ausgang_saetze
        einlage_aktuell = kennung
        einlage_ausgang_saetze = []
        bauart = EINLAGE_VORBEREITEN.get(kennung)
        einlage_lage = bauart() if bauart else {}
        return einlage_lage

    ## Wahrscheinlichkeit der Bahnsteigkontrolle ###############################
    ##
    ## Sie hängt an der Menge: Ein halbes Pfund in der Manteltasche fällt
    ## niemandem auf, ein voller Rucksack schon. Die Funktion ist rein
    ## rechnerisch, damit der Bildschirm sie gefahrlos aufrufen kann.

    def kontrolle_grenze(pfund):
        if pfund <= 0:
            return 0
        if pfund < HAMSTER_AUFFAELLIG:
            return 35
        return 70


################################################################################
## 5. Auswertung
################################################################################
##
## Jede Auswertung liefert dasselbe Wörterbuch:
##
##   saetze       Liste von Sätzen. Sie erzählen, was geschehen ist, und
##                bewerten nicht, was gewählt wurde.
##   aenderungen  die vier Werte
##   merkmale     zusätzliche Merkmale für spätere Ereignisse
##   bindung      Verbundenheit einzelner Rollen (figur_setzen)
##   ketten       Ereignisse, die dadurch fällig werden
##   protokoll    eine Zeile für die Auswertung im Unterricht
##
## KEINE WERTUNG
## In keinem dieser Sätze steht gut, richtig, falsch, geschafft oder
## verloren. Es steht dort, was danach anders ist. Die Sprachprüfung in
## Abschnitt 12 sucht diese Wörter und meldet sie.

init 7 python:

    def stufe_aus_summe(summe):
        """Drei Stufen aus einer Punktsumme. Keine Note, ein Ausmaß."""
        if summe <= 0:
            return 0
        if summe <= 2:
            return 1
        if summe <= 5:
            return 2
        return 3

    def einlage_begrenzen(aenderungen):
        """Kein Handgriff darf einen Durchgang entscheiden."""
        begrenzt = {}
        for schluessel, betrag in aenderungen.items():
            if betrag > EINLAGE_HOECHSTWIRKUNG:
                betrag = EINLAGE_HOECHSTWIRKUNG
            if betrag < -EINLAGE_HOECHSTWIRKUNG:
                betrag = -EINLAGE_HOECHSTWIRKUNG
            if betrag:
                begrenzt[schluessel] = betrag
        return begrenzt

    ############################################################################
    ## 5.1 Der Rotstift
    ############################################################################

    def rotstift_auswerten(gestrichen):
        gestrichen = set(gestrichen)
        zeilen = einlage_lage.get("zeilen", [])
        fremd = einlage_lage.get("fremder_bogen", False)
        heimat = einlage_lage.get("welt") == "heimat"

        geblieben = 0
        verloren = 0
        for stelle, zeile in enumerate(zeilen):
            if stelle in gestrichen:
                verloren = verloren + zeile["naehe"]
            else:
                geblieben = geblieben + zeile["risiko"]

        auffallen = stufe_aus_summe(geblieben)
        stille = stufe_aus_summe(verloren)

        aenderungen = {}
        bindung = {}
        saetze = []

        if auffallen:
            aenderungen["aufmerksamkeit"] = auffallen

        if stille and not fremd:
            aenderungen["rueckhalt"] = -stille

        ## Was mit dem Bogen geschieht ########################################

        if fremd:
            if auffallen == 0:
                saetze.append("Du gibst den Stapel weiter. Zur Feldpost geht nichts, was jemandem draußen nützen könnte.")
            elif auffallen == 1:
                saetze.append("Du gibst den Stapel weiter. In der Woche darauf kommt eine Anfrage der Zensurstelle zu einer Zeile, die dir durchgegangen ist.")
            else:
                saetze.append("Vierzehn Tage später liegt der Bogen wieder auf deinem Tisch, diesmal mit einer Anfrage der Zensurstelle daran. Sie will wissen, wer ihn durchgesehen hat.")
        elif heimat:
            if auffallen == 0:
                saetze.append("Der Brief geht mit der Sechsuhrleerung hinaus und kommt an, wie du ihn geschrieben hast.")
            elif auffallen == 1:
                saetze.append("Der Brief kommt an. Eine Zeile ist geschwärzt, und keiner von euch beiden erfährt, welche.")
            else:
                saetze.append("Der Brief kommt an, aber halbe Sätze fehlen. Auf dem Postamt hat jemand deinen Namen aufgeschrieben.")
        else:
            if auffallen == 0:
                saetze.append("Der Bogen geht mit der Vieruhrleerung ab. Darin steht nichts, was ein Fremder gebrauchen könnte.")
            elif auffallen == 1:
                saetze.append("Der Bogen geht ab. Bei der Stichprobe bleibt ein Bleistift an einer Stelle hängen, mehr geschieht nicht.")
            elif auffallen == 2:
                saetze.append("Der Brief kommt zu Hause geschwärzt an. Bei der Kompanie liegt jetzt ein Vermerk mit deinem Namen darauf.")
            else:
                saetze.append("Der Bogen geht nicht hinaus. Am nächsten Morgen legt ihn dir der Feldwebel vor und fragt, ob das mit Absicht so dastand.")

        ## Was von dem Menschen darin übrig bleibt #############################

        if stille >= 2:
            if fremd:
                saetze.append("Der Absender bekommt den Bogen zurück, quer durchgestrichen. Er sagt nichts dazu, und in den Tagen danach sagt er auch sonst wenig.")
                bindung["naechste"] = -1
            elif heimat:
                saetze.append("Was ankommt, sind Grüße und Lücken. In der Antwort steht, es sei gut, dass es euch gut gehe.")
            else:
                saetze.append("Was ankommt, sind Grüße und Lücken. Zu Hause legen sie den Bogen weg und wissen über dich so viel wie vorher.")
        elif stille == 1:
            saetze.append("Zwei Zeilen weniger, als es hätten sein können. Es fällt niemandem auf außer dir.")

        ## Die beiden Randfälle ################################################

        if not gestrichen:
            aenderungen["belastung"] = aenderungen.get("belastung", 0) - 1
            saetze.append("Du hast nichts angerührt. Es ist lange her, dass du etwas so aufgeschrieben hast, wie es ist.")
            if fremd:
                bindung["naechste"] = 1
        elif len(gestrichen) >= len(zeilen):
            aenderungen["belastung"] = aenderungen.get("belastung", 0) + 1
            saetze.append("Am Ende steht kaum noch etwas da. Abgeschickt wird der Bogen trotzdem, denn auch ein leerer Bogen ist ein Lebenszeichen.")

        return {
            "saetze": saetze,
            "aenderungen": aenderungen,
            "bindung": bindung,
            "protokoll": str(len(gestrichen)) + " von " + str(len(zeilen)) + " Zeilen gestrichen",
        }

    ############################################################################
    ## 5.2 Acht Striche
    ############################################################################

    def portionen_auswerten(anteile):
        empfaenger = einlage_lage.get("empfaenger", [])
        schimmel = einlage_lage.get("schimmel", False)
        heimat = briefwelt() == "heimat"

        anteil = {}
        bindung_moeglich = {}
        for stelle, eintrag in enumerate(empfaenger):
            anteil[eintrag["kennung"]] = anteile[stelle] if stelle < len(anteile) else 0
            bindung_moeglich[eintrag["kennung"]] = eintrag.get("bindung", False)

        selbst = anteil.get("selbst", 0)
        fuer_kind = anteil.get("kind", 0)
        fuer_naechste = anteil.get("naechste", 0)
        vorrat = anteil.get("vorrat", 0)

        aenderungen = {}
        bindung = {}
        merkmale = []
        saetze = []

        ## Der eigene Teller ###################################################
        ##
        ## Die Stufe kommt aus portionen_stufe() - derselben Funktion, die
        ## dem Bildschirm den Zustandssatz gibt. Was dort angekündigt war,
        ## wird hier eingelöst.

        stufe_selbst = portionen_stufe("selbst", selbst)

        if stufe_selbst == "viel":
            aenderungen["versorgung"] = 1
            saetze.append("Du isst dich zum ersten Mal seit Tagen satt und schläfst durch.")
            ## PAKET 7, SCHRITT 2, TEIL B.2 UND B.3. Die halbe Portion kostet
            ## sichtbar. Ohne diese Zeile war (4, 2, 2, 0) eine Verteilung,
            ## die jede andere erreicht oder schlägt - die Einlage hatte eine
            ## richtige Antwort, und damit war nichts mehr zu entscheiden.
            ##
            ## Es ist kein Strafpunkt, sondern eine Beobachtung: Am Tisch
            ## sitzen vier, und drei sehen, wie groß dein Stück ist. Der
            ## Zustandssatz "viel" sagt es vorher, damit niemand überrascht
            ## wird.
            aenderungen["rueckhalt"] = aenderungen.get("rueckhalt", 0) - 1
            saetze.append(welttext({
                "front": "Beim Verteilen hat niemand etwas gesagt. Am Abend redet die Gruppe über anderes als sonst.",
                "etappe": "Beim Verteilen hat niemand etwas gesagt. In der Baracke redet man über anderes als sonst.",
                "heimat": "Beim Verteilen hat niemand etwas gesagt. Am Abend ist es still am Tisch.",
            }))
        elif stufe_selbst in ("wenig", "nichts"):
            aenderungen["versorgung"] = -1
            aenderungen["belastung"] = 1
            saetze.append(welttext({
                "front": "Beim Aufstehen aus dem Unterstand wird dir schwarz vor Augen, und der Nebenmann hält dich am Riemen fest.",
                "etappe": "Beim Aufstehen vom Tisch wird dir schwarz vor Augen, und du hältst dich an der Kante fest.",
                "heimat": "Beim Treppensteigen musst du dich am Geländer halten und eine Weile stehen bleiben.",
            }))
        else:
            saetze.append("Es reicht bis zum Abend. Danach denkst du wieder ans Essen.")

        ## Die anderen am Tisch ################################################

        stufe_kind = portionen_stufe("kind", fuer_kind)
        stufe_naechste = portionen_stufe("naechste", fuer_naechste)

        if stufe_kind == "genug":
            aenderungen["rueckhalt"] = aenderungen.get("rueckhalt", 0) + 1
            saetze.append(welttext({
                "front": "Der Jüngste isst zu schnell und bedankt sich zweimal.",
                "etappe": "Der Laufbursche isst im Stehen und bedankt sich an der Tür noch einmal.",
                "heimat": "Das Kind isst zu schnell und fragt, ob morgen wieder etwas da ist.",
            }))
            if bindung_moeglich.get("kind"):
                bindung["kind"] = 1
        elif stufe_kind == "nichts":
            aenderungen["rueckhalt"] = aenderungen.get("rueckhalt", 0) - 1
            saetze.append("Es hat gesehen, dass nichts für es dabei war. Gesagt hat es nichts.")
            if bindung_moeglich.get("kind"):
                bindung["kind"] = -1

        if stufe_naechste == "genug":
            aenderungen["rueckhalt"] = aenderungen.get("rueckhalt", 0) + 1
            saetze.append(welttext({
                "front": "Der Nebenmann steckt dir am Abend wortlos zwei Zigaretten zu.",
                "etappe": "Dein Schichtnachbar legt dir am Abend zwei Bögen Papier hin, ohne etwas zu sagen.",
                "heimat": "Am nächsten Tag steht ein Topf mit Suppe vor deiner Tür.",
            }))
            if bindung_moeglich.get("naechste"):
                bindung["naechste"] = 1
        elif stufe_naechste == "nichts" and bindung_moeglich.get("naechste"):
            ## ABSICHTLICH OHNE rueckhalt-ABZUG, anders als beim Kind. Wer
            ## dem Nachbarn nichts abgibt, verliert seine Zuwendung
            ## (bindung), aber nicht den eigenen Halt: Der Nachbar ist kein
            ## Angehöriger. Beim Kind ist beides dasselbe.
            bindung["naechste"] = -1
            saetze.append(welttext({
                "front": "Der Nebenmann sieht kurz auf deinen Napf und dann wieder weg.",
                "etappe": "Dein Schichtnachbar sieht kurz auf deinen Napf und dann in sein Buch.",
                "heimat": "Im Treppenhaus wird am nächsten Morgen kürzer gegrüßt als sonst.",
            }))

        ## Was zurückgelegt wird ###############################################

        if portionen_stufe("vorrat", vorrat) == "genug":
            if schimmel:
                saetze.append(welttext({
                    "front": "Was im Brotbeutel bleibt, ist nach drei Tagen grün an den Rändern. Kriegsbrot mit Kartoffelmehl hält nicht.",
                    "etappe": "Was im Spind bleibt, ist nach drei Tagen grün an den Rändern. Kriegsbrot mit Kartoffelmehl hält nicht.",
                    "heimat": "Was im Schrank bleibt, ist nach drei Tagen grün an den Rändern. Kriegsbrot mit Kartoffelmehl hält nicht.",
                }))
            else:
                aenderungen["versorgung"] = aenderungen.get("versorgung", 0) + 1
                merkmale.append("vorrat_angelegt")
                saetze.append("Am Mittwoch, als die Ausgabe ausfällt, ist noch etwas da.")

        ## Wer sich gar nichts nimmt, zahlt doppelt: einmal für den leeren
        ## Magen, einmal für den Tag, der darauf folgt.
        if stufe_selbst == "nichts":
            aenderungen["belastung"] = aenderungen.get("belastung", 0) + 1

        return {
            "saetze": saetze,
            "aenderungen": aenderungen,
            "bindung": bindung,
            "merkmale": merkmale,
            "protokoll": ("selbst " + str(selbst) + ", andere " +
                          str(fuer_kind + fuer_naechste) + ", zurückgelegt " + str(vorrat)),
        }

    ############################################################################
    ## 5.3 Die Fahrt aufs Land
    ############################################################################
    ##
    ## ergebnis ist ein Dreiersatz: (gegebene Stücke, Pfund, Verhalten
    ## an der Sperre). Das Verhalten ist "keine", "zeigen" oder "verbergen".

    def hamsterfahrt_auswerten(ergebnis):
        gegeben, pfund, verhalten = ergebnis
        gueter = einlage_lage.get("gueter", [])
        entkommen = einlage_lage.get("entkommenwurf", 100) <= 55

        aenderungen = {"belastung": 1}
        merkmale = []
        ketten = []
        saetze = []
        heimgebracht = pfund

        ## Der Weg zurück ######################################################

        if verhalten == "keine":
            if pfund > 0:
                saetze.append("Am Bahnsteig steht heute niemand. Um halb neun stellst du den Rucksack in der Küche ab.")
            else:
                saetze.append("Du fährst zurück mit dem, womit du gekommen bist.")
        elif verhalten == "zeigen":
            heimgebracht = 0
            aenderungen["aufmerksamkeit"] = 1
            saetze.append("Der Beamte schreibt deinen Namen auf und stellt den Rucksack hinter sich. Eine Vergütung ist nicht vorgesehen; das steht auch so auf dem Anschlag.")
        elif verhalten == "verbergen":
            if entkommen:
                aenderungen["aufmerksamkeit"] = 1
                saetze.append("Du gehst hinter einer Familie mit Kinderwagen durch die Sperre und siehst niemanden an. Draußen sind die Beine weich.")
            else:
                heimgebracht = 0
                aenderungen["aufmerksamkeit"] = 2
                ketten.append("heimat_verfahren")
                saetze.append("Der Sack wird unter dem Mantel gefunden. Die Lebensmittel werden beschlagnahmt, deine Personalien werden festgestellt, und der Beamte sagt, es gehe seinen Weg.")

        ## Was auf dem Tisch landet ############################################

        if heimgebracht > 0:
            gewinn = min(3, max(1, heimgebracht // 10))
            aenderungen["versorgung"] = gewinn
            merkmale.append("gehamstert")
            saetze.append("Über zwei Wochen hinweg gibt es abends wieder etwas, das satt macht.")
        elif pfund > 0:
            saetze.append("Der Tisch bleibt an diesem Abend so leer wie am Morgen, und dazu fehlt jetzt, was du hergegeben hast.")

        ## Was zu Hause fehlt ##################################################

        schwer = 0
        for stelle in gegeben:
            if stelle < len(gueter):
                saetze.append(gueter[stelle]["folge"])
                if gueter[stelle]["wert"] >= 3:
                    schwer = schwer + 1
        if schwer:
            aenderungen["belastung"] = aenderungen.get("belastung", 0) + 1

        return {
            "saetze": saetze,
            "aenderungen": aenderungen,
            "merkmale": merkmale,
            "ketten": ketten,
            "protokoll": (str(len(gegeben)) + " Stücke getauscht, " + str(pfund) +
                          " Pfund erhandelt, " + str(heimgebracht) + " Pfund angekommen"),
        }

    ############################################################################
    ## 5.4 Was du trägst
    ############################################################################

    def tornister_auswerten(behalten):
        behalten = set(behalten)
        stuecke = einlage_lage.get("stuecke", [])

        last = 0
        for stueck in stuecke:
            if stueck["kennung"] in behalten:
                last = last + stueck["last"]

        aenderungen = {}
        bindung = {}
        merkmale = []
        saetze = []

        fehlt = lambda name: name not in behalten

        ## Was im Straßengraben bleibt, bleibt im Lebenslauf ###################
        ##
        ## PAKET 7, SCHRITT 3, TEIL A.1. Jedes zurückgelassene Stück setzt
        ## sein Merkmal. Sie stehen in MERKMAL_REGISTER (kapitel.rpy) in der
        ## Gruppe "tat" und tragen je einen Nachklang; welcher von ihnen im
        ## Lebenslauf erscheint, entscheidet der Rang.
        ##
        ## "fremdes" gehört NICHT dazu: Es ist kein Verzicht, sondern eine
        ## Zuwendung, und es hat sein eigenes Merkmal weiter unten.

        for stueck in stuecke:
            if stueck["kennung"] == "fremdes":
                continue
            if fehlt(stueck["kennung"]):
                merkmale.append("ohne_" + stueck["kennung"])

        ## Nachts ##############################################################

        if fehlt("mantel") and fehlt("zeltbahn"):
            aenderungen["belastung"] = 2
            saetze.append("In der Nacht fällt die Temperatur, und es gibt weder etwas zum Zudecken noch etwas gegen den Regen. Geschlafen wird im Sitzen.")
        elif fehlt("mantel"):
            aenderungen["belastung"] = 1
            saetze.append("Nachts liegst du in der Zeltbahn und wachst alle halbe Stunde auf, weil dir kalt ist.")
        elif fehlt("zeltbahn"):
            aenderungen["belastung"] = 1
            saetze.append("Es regnet ab dem Abend durch, und der Mantel trocknet bis zum Morgen nicht.")

        ## Füße ################################################################

        if fehlt("stiefel"):
            aenderungen["belastung"] = aenderungen.get("belastung", 0) + 1
            saetze.append("Am dritten Tag ist die Ferse offen. Der Sanitätsunteroffizier gibt dir Zinksalbe und schickt dich weiter.")

        ## Essen ###############################################################

        if fehlt("kochgeschirr"):
            aenderungen["versorgung"] = aenderungen.get("versorgung", 0) - 1
            saetze.append("Ohne Napf gibt es an der Feldküche nichts. Du isst aus dem Deckel eines anderen, wenn er fertig ist.")

        if fehlt("portion"):
            aenderungen["versorgung"] = aenderungen.get("versorgung", 0) - 1
            aenderungen["aufmerksamkeit"] = aenderungen.get("aufmerksamkeit", 0) + 1
            saetze.append("Beim nächsten Appell wird nach der eisernen Portion gesehen. Sie gehört dem Heer, und ihr Fehlen wird aufgeschrieben.")

        ## Ordnung #############################################################

        if fehlt("putzzeug"):
            aenderungen["aufmerksamkeit"] = aenderungen.get("aufmerksamkeit", 0) + 1
            saetze.append("Beim Gewehrappell fährt der Feldwebel mit dem Finger durch den Lauf und sieht dich danach lange an.")

        ## Was von zu Hause übrig ist ##########################################

        if fehlt("briefe"):
            aenderungen["rueckhalt"] = aenderungen.get("rueckhalt", 0) - 1
            saetze.append("Der Platz über deiner Pritsche bleibt leer. Wie das Gesicht auf der Fotografie aussah, weißt du nach ein paar Wochen nicht mehr genau.")

        ## Fremde Last #########################################################

        ## PAKET 7, SCHRITT 3: DAS FREMDE GEPÄCK KOSTET KEINE EIGENE
        ## BELASTUNG MEHR.
        ##
        ## Es hat sie vorher gekostet - und zusätzlich zählte sein Riemen im
        ## Gesamtgewicht mit. Dasselbe Kilo wurde damit zweimal berechnet,
        ## und in einem Fall kam der Tornister so auf +4 Belastung gegen
        ## EINLAGE_HOECHSTWIRKUNG = 3. Die Kappung hat es still geschluckt:
        ## Der Ausgangstext erzählte von vier Beschwerden, angekommen sind
        ## drei (AUFGEFALLEN 68, gefunden von Probe 10a).
        ##
        ## Jetzt wird das Gewicht einmal gezählt, unten bei der Traglast.
        ## Das ist auch sachlich richtig: Ein zusätzliches Kochgeschirr auf
        ## einem vollen Tornister bricht dir den Rücken, auf einem leeren
        ## merkst du es nicht. Die Zuwendung bleibt unangetastet - Rückhalt,
        ## Merkmal und Verbundenheit stehen unverändert.

        if "fremdes" in behalten:
            aenderungen["rueckhalt"] = aenderungen.get("rueckhalt", 0) + 1
            merkmale.append("last_getragen")
            saetze.append("Der Jüngste kommt am Abend mit an. Er sagt nichts darüber, aber er bleibt von da an in deiner Nähe.")
            if empfaenger_verfuegbar("kind"):
                bindung["kind"] = 1

        ## Das Gewicht selbst ##################################################

        if last >= TRAGLAST_GRENZE:
            aenderungen["belastung"] = aenderungen.get("belastung", 0) + 1
            saetze.append("Bis zum Abend sind es noch achtzehn Kilometer. Die Riemen stehen dir in den Schultern, und du zählst Schritte.")
        elif last <= 4:
            saetze.append("Der Tornister sitzt zum ersten Mal an diesem Tag so, wie er sitzen soll. Im Straßengraben hinter euch liegt der Rest.")

        return {
            "saetze": saetze,
            "aenderungen": aenderungen,
            "bindung": bindung,
            "merkmale": merkmale,
            "protokoll": (str(last) + " von " + str(TRAGLAST_GRENZE) + " Riemen getragen, " +
                          str(len(stuecke) - len(behalten)) + " Stücke zurückgelassen"),
        }

    ## Der Antrag rechnet gegenläufig zum Rotstift: Dort kostet das
    ## Stehenlassen, hier kostet das Angeben. Wer alles angibt, bekommt
    ## den niedrigsten Satz und hat nichts zu befürchten; wer streicht,
    ## bekommt mehr und steht in der Prüfung. Und wer die
    ## Unterhaltspflicht streicht, verschweigt das Einzige, was ihm
    ## genützt hätte.
    def versorgungsantrag_auswerten(gestrichen):
        gestrichen = set(gestrichen)
        zeilen = einlage_lage.get("zeilen", [])

        abzug = 0
        verschwiegen = 0
        eigenes_tor = False
        for stelle, zeile in enumerate(zeilen):
            if stelle in gestrichen:
                verschwiegen = verschwiegen + zeile["pruefung"]
                if zeile["satz"] < 0:
                    eigenes_tor = True
            else:
                abzug = abzug + zeile["satz"]

        saetze = []
        aenderungen = {}
        merkmale = []

        ## Was bewilligt wird ##################################################

        if abzug <= 1:
            aenderungen["versorgung"] = 2
            saetze.append("Der Bescheid kommt nach elf Tagen und nennt den vollen Satz.")
        elif abzug <= 4:
            aenderungen["versorgung"] = 1
            saetze.append("Der Bescheid kommt nach elf Tagen und nennt einen mittleren Satz.")
        else:
            saetze.append("Der Bescheid kommt nach elf Tagen. Der Satz ist der niedrigste, den es gibt.")

        ## Was die Prüfung findet ##############################################

        if verschwiegen >= 5:
            aenderungen["aufmerksamkeit"] = 2
            aenderungen["belastung"] = aenderungen.get("belastung", 0) + 1
            saetze.append("Im März steht jemand vom Amt in der Wohnung und sieht sich um. Er zählt die Zimmer und schreibt mit. Was du nicht angegeben hast, steht am Abend in deiner Akte.")
        elif verschwiegen >= 2:
            aenderungen["aufmerksamkeit"] = 1
            saetze.append("Auf dem Bogen fehlt eine Angabe, und das Amt fragt schriftlich nach. Du antwortest knapp, und danach ist Ruhe.")
        elif gestrichen:
            saetze.append("Was du weggelassen hast, fällt niemandem auf. Es war auch nicht viel.")

        ## Die beiden Randfälle ################################################

        if not gestrichen:
            aenderungen["rueckhalt"] = aenderungen.get("rueckhalt", 0) + 1
            merkmale.append("antrag_offen")
            saetze.append("Du hast jede Zeile stehen lassen. Der Beamte liest den Bogen zu Ende und sieht dich danach an, als wolle er etwas sagen.")
        elif len(gestrichen) >= len(zeilen):
            saetze.append("Am Ende steht fast nichts mehr da. Ein Bogen ohne Angaben ist kein Antrag, und der Beamte schiebt ihn zurück.")

        if eigenes_tor:
            aenderungen["versorgung"] = aenderungen.get("versorgung", 0) - 1
            saetze.append("Die Kinder hast du weggelassen. Genau dafür hätte es einen Zuschlag gegeben, und der fehlt jetzt jeden Monat.")

        return {
            "saetze": saetze,
            "aenderungen": aenderungen,
            "merkmale": merkmale,
            "protokoll": str(len(gestrichen)) + " von " + str(len(zeilen)) + " Angaben weggelassen",
        }

    EINLAGE_AUSWERTEN = {
        "rotstift": rotstift_auswerten,
        "portionen": portionen_auswerten,
        "hamsterfahrt": hamsterfahrt_auswerten,
        "tornister": tornister_auswerten,
        "versorgungsantrag": versorgungsantrag_auswerten,
    }

    ############################################################################
    ## 5.5 Anwenden
    ############################################################################

    def einlage_anwenden(kennung, ergebnis):
        """Rechnet das Ergebnis in Werte, Merkmale und Bindung um.

        Ändert den Spielstand und legt die Sätze für den Ausgangsbildschirm
        in einlage_ausgang_saetze ab.
        """
        global einlage_ausgang_saetze

        vorlage = einlage_holen(kennung)
        rechnung = EINLAGE_AUSWERTEN.get(kennung)
        if vorlage is None or rechnung is None:
            einlage_ausgang_saetze = []
            return

        auswertung = rechnung(ergebnis)

        zustand_aendern(einlage_begrenzen(auswertung.get("aenderungen", {})))

        for name in auswertung.get("merkmale", []):
            merkmal_setzen(name)
        if vorlage.merkmal:
            merkmal_setzen(vorlage.merkmal)

        for figur_kennung, betrag in auswertung.get("bindung", {}).items():
            if empfaenger_verfuegbar(figur_kennung):
                figur_setzen(figur_kennung, verbundenheit=betrag)

        for kettenname in auswertung.get("ketten", []):
            ereignis_vormerken(kettenname, aktuelles_jahr)

        protokoll_eintragen("einlage_" + kennung, auswertung.get("protokoll", ""))

        einlage_ausgang_saetze = auswertung.get("saetze", [])


################################################################################
## 6. Ziehung
################################################################################
##
## WANN EINE EINLAGE KOMMT
## 1. Nur nach einem Ereignis der Hauptschleife, nie im Einstieg.
## 2. Höchstens ein- bis zweimal je Kapitel (EINLAGEN_JE_KAPITEL).
## 3. Nie zwei Einlagen dicht hintereinander (EINLAGE_ABSTAND).
## 4. Nie dieselbe zweimal nacheinander.
## 5. Hängt eine Einlage am gerade gespielten Ereignis, kommt sie ohne
##    weiteren Wurf. Sonst entscheidet EINLAGE_CHANCE.
##
## Dadurch bleibt die Einlage das, was sie sein soll: ein Handgriff, der
## sich aus der Lage ergibt, und keine Station, die abgearbeitet wird.

init 7 python:

    def einlage_zulaessig(vorlage):
        if vorlage is None:
            return False
        if aktuelles_jahr not in vorlage.jahre:
            return False
        if aktueller_pfad not in vorlage.pfad:
            return False
        if not vorlage.wiederholbar and vorlage.kennung in einlagen_gespielt:
            return False
        for name in vorlage.braucht:
            if not hat_merkmal(name):
                return False
        for name in vorlage.verbietet:
            if hat_merkmal(name):
                return False
        ## Ohne Bildschirm keine Einlage. Diese Prüfung fängt Tippfehler
        ## im Bestand ab, bevor sie mitten im Durchgang auffallen.
        if not renpy.has_screen(vorlage.bildschirm):
            return False
        return True

    def einlage_kapitel_pruefen():
        global einlage_jahr, einlagen_im_kapitel
        if einlage_jahr != aktuelles_jahr:
            einlage_jahr = aktuelles_jahr
            einlagen_im_kapitel = 0

    ## PAKET 8, SCHRITT 2.5 — DIE NACHZIEHREGEL ################################
    ##
    ## Der Auftrag: "Ist ein Kapitel ohne Einlage oder ohne Brief zu Ende
    ## gegangen, wird im nächsten mit Sicherheit gezogen."
    ##
    ## GEBAUT, GEMESSEN — UND AUSGESCHALTET. Der Schalter unten steht auf
    ## False, und zwar nicht aus Vorsicht, sondern aus einer Messung:
    ## Die Regel kostet Überlebenschance und reißt damit die Korridore aus
    ## Entscheidung 11. Entscheidung 11 sagt für genau diesen Fall: "Wer
    ## dort landet, hält an und meldet, statt die Grenze weiter zu senken."
    ##
    ## Vier Läufe, dieselbe Zufallssaat, 300 Durchgänge je Lage,
    ## zufällige Wahl / kluge Wahl in Prozent:
    ##
    ##   Lage           Ausgang      nur Post   nur Einlagen    beides
    ##   Front kurz     46,3/82,7    50,7/81,0    48,3/70,3   42,3/70,3
    ##   Front lang     33,0/66,3    26,3/62,0    28,3/59,7   23,0/56,3
    ##   Etappe kurz    56,3/82,7    50,0/75,3    44,3/65,3   38,0/68,0
    ##   Etappe lang    24,7/46,0    20,0/47,0    16,7/35,3   19,3/34,7
    ##   Heimat kurz    46,7/87,3    40,3/84,7    39,0/75,7   39,7/70,7
    ##   Heimat lang    23,3/66,3    17,7/63,3    20,7/57,0   14,7/59,3
    ##   Beanstandungen         1            3            6          10
    ##
    ## Die Einlagen sind die teure Hälfte: Jede kostet Werte, und drei
    ## Einlagen mehr je Durchgang sind drei Wertänderungen mehr. Die Post
    ## ist billiger, reißt aber auch schon zwei Korridore.
    ##
    ## Was die Regel dafür bringt, steht in Probe 2, Abschnitt a0. Kapitel
    ## ohne Einlage UND ohne Brief, über alle sechs Lagen: von 20 bis 40
    ## Prozent auf 11 bis 27. Die Regel wirkt also — sie ist nur nicht
    ## umsonst.
    ##
    ## UND SIE KANN NICHT HALTEN, WAS PUNKT 8 VERSPRICHT. Eine
    ## Nachziehregel wirkt rückwärts: Sie kann ein leeres Kapitel nicht
    ## nachträglich füllen, sondern nur dafür sorgen, dass auf ein leeres
    ## kein zweites folgt. "In jedem Kapitel garantiert" verlangt eine
    ## VORziehregel — beim letzten Zug eines Kapitels erzwingen, was fehlt.
    ## Die kostet sechs Einlagen je langem Durchgang, also neun Minuten
    ## Unterrichtszeit, und macht aus der Einlage genau die Station, die
    ## sie nach dem Entwurf oben nicht sein soll.
    ##
    ## Der Schalter gehört Dominik. Beide Hälften sind einzeln schaltbar,
    ## damit die billigere ohne Umbau versucht werden kann.
    RHYTHMUS_NACHZIEHEN = {"einlage": False, "post": False}

    ## Gebucht wird am ENDE eines Kapitels, nicht am Anfang des nächsten:
    ## Nur dort steht fest, was gefehlt hat, und nur dort sind die Zähler
    ## noch die des vergangenen Kapitels. post_im_jahr wird in
    ## schicksale_wuerfeln() zurückgesetzt — deshalb steht der Aufruf ganz
    ## oben in kapitelwechsel_mit_schicksal, vor den Schicksalen.
    ##
    ## Die Schuld wird bezahlt, sobald wirklich gezogen wurde
    ## (einlage_vermerken, brief_zustellen), nicht schon beim Versuch.
    ## Bleibt ein Kapitel auch mit Schuld leer, bleibt sie stehen und gilt
    ## im übernächsten weiter — sie verfällt nicht.
    def rhythmus_kapitel_abschliessen():
        """Bucht am Ende eines Kapitels, was darin gefehlt hat."""
        global einlage_schuld, post_schuld
        einlage_kapitel_pruefen()
        einlage_schuld = (RHYTHMUS_NACHZIEHEN.get("einlage", False)
                          and einlagen_im_kapitel <= 0)
        post_schuld = (RHYTHMUS_NACHZIEHEN.get("post", False)
                       and post_im_jahr <= 0)

    def einlage_ziehen(ereignis_kennung):
        """Liefert die Kennung einer Einlage oder None."""
        global einlagen_seit

        einlage_kapitel_pruefen()
        einlagen_seit = einlagen_seit + 1

        if not einlagen_erlaubt:
            return None
        if ereignis_kennung in EINLAGE_NIE_NACH:
            return None
        if ereignis_kennung not in EREIGNIS_INDEX:
            return None
        if einlagen_im_kapitel >= EINLAGEN_JE_KAPITEL.get(spielmodus, 1):
            return None

        ## PAKET 8, SCHRITT 2.5: Der Abstand wird bei offener Schuld auf
        ## eine Ziehung verkürzt, nicht aufgehoben. Ein Kapitel hat im
        ## kurzen Verlauf ein bis zwei Ziehungen (KAPITEL_ZIEHUNGEN) — mit
        ## dem vollen Abstand von zwei wäre die Nachziehregel in den
        ## meisten Kapiteln gar nicht anwendbar und stünde nur da.
        ## Zwei Einlagen unmittelbar hintereinander bleiben ausgeschlossen.
        if einlagen_seit <= (1 if einlage_schuld else EINLAGE_ABSTAND):
            return None

        ## Anschluss an das gerade gespielte Ereignis
        gebunden = []
        for kennung in EINLAGE_ANSCHLUSS.get(ereignis_kennung, []):
            vorlage = einlage_holen(kennung)
            if einlage_zulaessig(vorlage) and kennung != einlage_zuletzt:
                gebunden.append(vorlage)
        if gebunden:
            return gewichtet_ziehen(gebunden, lambda e: e.gewicht).kennung

        ## Freie Ziehung. Bei offener Schuld ohne Wurf (Schritt 2.5).
        if not einlage_schuld:
            if renpy.random.randint(1, 100) > EINLAGE_CHANCE:
                return None

        frei = []
        for vorlage in EINLAGEN:
            if einlage_zulaessig(vorlage) and vorlage.kennung != einlage_zuletzt:
                frei.append(vorlage)
        if not frei:
            return None
        return gewichtet_ziehen(frei, lambda e: e.gewicht).kennung

    def einlage_vermerken(kennung):
        global einlagen_gespielt, einlagen_im_kapitel, einlagen_seit, einlage_zuletzt
        global einlage_schuld
        einlagen_gespielt = einlagen_gespielt + [kennung]
        einlagen_im_kapitel = einlagen_im_kapitel + 1
        einlagen_seit = 0
        einlage_zuletzt = kennung
        ## Bezahlt wird bei der Zustellung, nicht beim Versuch (Schritt 2.5).
        einlage_schuld = False

    ############################################################################
    ## Nachtrag am vorhandenen Ereignisbestand
    ############################################################################
    ##
    ## Die Einlage "Die Fahrt aufs Land" und das Ereignis
    ## heimat_hamsterfahrt erzählen dieselbe Sonntagsfahrt, nur einmal
    ## als Karte und einmal als Handgriff. Wer die Fahrt gespielt hat,
    ## bekommt die Karte nicht mehr. Umgekehrt bleibt die Einlage
    ## erreichbar: Gefahren wurde mehr als einmal.
    ##
    ## Dasselbe Verfahren wie RUECKBEZUG_NACHTRAG in kapitel.rpy: Die
    ## Vorlage wird ergänzt, nicht neu geschrieben.

    def einlagen_nachtragen():
        vorlage = EREIGNIS_INDEX.get("heimat_hamsterfahrt")
        if vorlage is None:
            return
        bestand = list(getattr(vorlage, "verbietet", []))
        if "gehamstert" not in bestand:
            bestand.append("gehamstert")
        vorlage.verbietet = bestand

    einlagen_nachtragen()


################################################################################
## 7. Zustand
################################################################################

init 7 python:

    def einlagen_zuruecksetzen():
        global einlagen_gespielt, einlagen_im_kapitel, einlagen_seit
        global einlage_jahr, einlage_zuletzt, einlage_aktuell
        global einlage_lage, einlage_ergebnis, einlage_ausgang_saetze
        einlagen_gespielt = []
        einlagen_im_kapitel = 0
        einlagen_seit = 0
        einlage_jahr = 0
        einlage_zuletzt = None
        einlage_aktuell = None
        einlage_lage = {}
        einlage_ergebnis = None
        einlage_ausgang_saetze = []

    ## Anhängen statt ersetzen, wie figuren.rpy es mit derselben Funktion
    ## macht. Ohne diese Zeilen liefen nach einem Neustart die Zähler des
    ## vorigen Durchgangs weiter.
    zustand_zuruecksetzen_vor_einlagen = zustand_zuruecksetzen

    def zustand_zuruecksetzen():
        zustand_zuruecksetzen_vor_einlagen()
        einlagen_zuruecksetzen()


## Schalter für die Werkzeuge: Die Dialog- und Bestandsproben spielen
## Ereignisse ab, ohne dass Einlagen dazwischenfahren sollen.
default einlagen_erlaubt = True

default einlagen_gespielt = []
default einlagen_im_kapitel = 0
default einlagen_seit = 0

## PAKET 8, SCHRITT 2.5: offene Schuld aus dem letzten Kapitel.
default einlage_schuld = False
default einlage_jahr = 0
default einlage_zuletzt = None

default einlage_aktuell = None
default einlage_lage = {}
default einlage_ergebnis = None
default einlage_ausgang_saetze = []


################################################################################
## 8. Hilfen für die Bildschirme
################################################################################
##
## Ren'Py berechnet einen Bildschirm bei jeder Mausbewegung neu. Deshalb
## verändert keine dieser Funktionen etwas: Sie bekommen einen Zustand und
## liefern einen neuen zurück. Gesetzt wird ausschließlich über
## SetScreenVariable, und dort steht immer das Ergebnis einer dieser
## Funktionen. So bleibt die Rücknahme (Rollback) von Ren'Py in Ordnung.

init 7 python:

    def stelle_umschalten(bestand, stelle):
        """Nimmt eine Stelle hinein oder heraus. Liefert ein neues Tupel."""
        if stelle in bestand:
            return tuple([eintrag for eintrag in bestand if eintrag != stelle])
        return tuple(list(bestand) + [stelle])

    def anteil_aendern(anteile, stelle, betrag):
        neu = list(anteile)
        neu[stelle] = max(0, neu[stelle] + betrag)
        return tuple(neu)

    ## Die eine Stelle, an der eine Zuteilung zu einer Stufe wird ###########
    ##
    ## PAKET 7, SCHRITT 2. Der Bildschirm fragt sie, um den Zustandssatz zu
    ## zeigen; portionen_auswerten() fragt sie, um die Werte zu bewegen.
    ## Zwei Tafeln nebeneinander wären zwei Wahrheiten, und die Spielerin
    ## bekäme etwas anderes, als der Bildschirm ihr versprochen hat.

    def portionen_stufe(kennung, anteil):
        for schwelle, stufe in PORTIONEN_SCHWELLEN.get(kennung, []):
            if anteil >= schwelle:
                return stufe
        return "nichts"

    def portionen_satz(kennung, anteil):
        tafel = PORTIONEN_ZUSTAND.get(kennung, {})
        return welttext(tafel.get(portionen_stufe(kennung, anteil), {}))

    ## Wie viele Striche noch auf dem Tisch liegen - in Worten, nicht als
    ## Fehlermeldung. "Es fehlen noch 3" wäre eine Rüge; "Drei Striche
    ## liegen noch auf dem Tisch" ist eine Feststellung.

    PORTIONEN_ZAHLWORT = ["Kein", "Ein", "Zwei", "Drei", "Vier",
                          "Fünf", "Sechs", "Sieben", "Acht"]

    def portionen_rest_satz(rest):
        if rest <= 0:
            return ""
        wort = PORTIONEN_ZAHLWORT[rest] if rest < len(PORTIONEN_ZAHLWORT) else str(rest)
        if rest == 1:
            return wort + " Strich liegt noch auf dem Tisch."
        return wort + " Striche liegen noch auf dem Tisch."

    def anteil_rest(anteile, gesamt):
        return gesamt - sum(anteile)

    ## Was der Hof zu deinem Gebot sagt ########################################
    ##
    ## PAKET 7, SCHRITT 3, TEIL B.1. Vier Stufen, und die Schwelle ist der
    ## verlangte Preis - nicht eine zweite Zahl daneben.

    def hof_stufe(geboten, verlangt):
        if geboten <= 0:
            return "nichts"
        if geboten < verlangt:
            return "wenig"
        if geboten == verlangt:
            return "genug"
        return "zuviel"

    def hof_antwort(hof, geboten):
        tafel = hof.get("antwort") or {}
        return tafel.get(hof_stufe(geboten, hof.get("verlangt", 0)), "")

    ## Der Wechsel von Hof zu Hof ##############################################
    ##
    ## TEIL B.5. Er ist ein Bildwechsel und kein Klick im Bild, also
    ## bekommt er den benannten Übergang. renpy.transition() setzt ihn für
    ## die nächste Interaktion; SetScreenVariable löst genau eine aus.

    def hamster_weiter():
        renpy.transition(UEBERGANG_KARTE())

    def angebotswert(gueter, angeboten):
        summe = 0
        for stelle in angeboten:
            if stelle < len(gueter):
                summe = summe + gueter[stelle]["wert"]
        return summe

    def traglast(stuecke, behalten):
        summe = 0
        for stueck in stuecke:
            if stueck["kennung"] in behalten:
                summe = summe + stueck["last"]
        return summe

    def tornister_grundlast():
        return tuple([s["kennung"] for s in TORNISTER_STUECKE if s["drin"]])

    def brief_zeile_text(satz, gestrichen):
        """Der Rotstift. {s} ist Ren'Pys Durchstreichung."""
        if gestrichen:
            return "{s}" + satz + "{/s}"
        return satz

    ## Kopf- und Schlusszeile tragen fuer die Etappe MIT ABSICHT denselben
    ## Wortlaut wie fuer die Front. "Im Felde" war die amtliche Angabe fuer
    ## jeden, der beim Feldheer stand, und dazu gehoerte das Etappengebiet.
    ## Hier waere eine eigene Formulierung nicht die eigene Stimme des
    ## Pfades, sondern schlicht falsch. Der Schluessel steht trotzdem da:
    ## Nur so ist es eine Entscheidung und kein Griff in die Rueckfallebene,
    ## den niemand mehr sieht.
    def brief_kopfzeile():
        return welttext({
            "front": "Im Felde, den 14. Oktober " + str(aktuelles_jahr),
            "etappe": "Im Felde, den 14. Oktober " + str(aktuelles_jahr),
            "heimat": "Den 14. Oktober " + str(aktuelles_jahr),
        })

    def brief_schlusszeile():
        return welttext({
            "front": "Bleibt gesund. Es grüßt euch",
            "etappe": "Bleibt gesund. Es grüßt euch",
            "heimat": "Bleib gesund. Es grüßt dich",
        })

    def sperre_faellig(pfund):
        """Steht heute jemand am Bahnsteig? Reine Rechnung, kein Wurf."""
        if pfund <= 0:
            return False
        return einlage_lage.get("kontrollwurf", 100) <= kontrolle_grenze(pfund)


################################################################################
## 9. Stile und Bildschirme
################################################################################

init offset = -1

## Kopf einer Einlage ##########################################################

style einlage_titel is default:
    font SCHRIFT_TITEL
    size 36
    bold True
    color FARBE_AKZENT
    text_align 0.5
    layout "subtitle"

style einlage_lage is default:
    size 23
    color FARBE_TINTE
    line_spacing 6
    text_align 0.5
    layout "subtitle"

style einlage_anweisung is default:
    size 21
    italic True
    color FARBE_TINTE_MATT
    text_align 0.5
    layout "subtitle"

style einlage_marke is default:
    size 16
    color FARBE_LINIE
    kerning 2.5

style einlage_zaehler is default:
    font SCHRIFT_TITEL
    size 30
    bold True
    color FARBE_TINTE

style einlage_zaehler_warnung is einlage_zaehler:
    color FARBE_AKZENT

## Briefbogen ##################################################################

style bogen_kopf is default:
    font SCHRIFT_DOKUMENT
    size 20
    color FARBE_TINTE_MATT

style bogen_zeile is default:
    font SCHRIFT_DOKUMENT
    size 22
    color FARBE_TINTE
    line_spacing 3

style bogen_zeile_gestrichen is bogen_zeile:
    color FARBE_AKZENT_MATT

## Der Stempel und der Zähler, seit Paket 7, Schritt 2 ########################

style bogen_stempel is default:
    font SCHRIFT_SCHMAL
    size 24
    bold True
    color FARBE_AKZENT
    kerning 4.0

style bogen_zaehler is default:
    size 22
    color FARBE_TINTE_MATT
    text_align 0.5

style bogen_hinweis is default:
    size 18
    italic True
    color FARBE_LINIE
    text_align 0.5

style vorschrift_kopf is default:
    size 17
    bold True
    color FARBE_AKZENT
    kerning 1.6

style vorschrift_zeile is default:
    size 19
    color FARBE_TINTE_MATT
    line_spacing 3

## Portionen ###################################################################

style portion_name is default:
    font SCHRIFT_TITEL
    size 25
    bold True
    color FARBE_TINTE

style portion_zusatz is default:
    size 19
    italic True
    color FARBE_TINTE_MATT

## Seit Paket 7, Schritt 2: der Zustandssatz unter dem festen Zusatz. Er
## ist nicht kursiv und dunkler als die Zeile darüber - der Zusatz sagt,
## wer da sitzt, dieser Satz sagt, was deine Zuteilung aus ihm macht, und
## nur der zweite wechselt.

style portion_zustand is default:
    size 20
    color FARBE_TINTE
    line_spacing 2

style portion_rest is default:
    size 21
    color FARBE_TINTE_MATT
    text_align 0.5

## Hof und Tauschgut ###########################################################

style hof_name is default:
    font SCHRIFT_TITEL
    size 27
    bold True
    color FARBE_AKZENT

style hof_satz is default:
    size 21
    italic True
    color FARBE_TINTE_MATT
    line_spacing 4

style hof_angebot is default:
    size 22
    color FARBE_TINTE
    line_spacing 4

## Seit Paket 7, Schritt 3: die Antwort des Hofes, die Folge eines
## angebotenen Stücks und die Marken der Weganzeige.

style hof_antwort is default:
    size 20
    italic True
    color FARBE_TINTE
    line_spacing 3

style gut_folge is default:
    size 17
    italic True
    color FARBE_TINTE_MATT
    line_spacing 2

style weg_marke is default:
    size 17
    color FARBE_TINTE_MATT
    kerning 1.0
    text_align 0.5

style gut_name is default:
    size 21
    color FARBE_TINTE

style gut_wert is default:
    size 18
    color FARBE_LINIE

## Tornister ###################################################################

style stueck_name is default:
    font SCHRIFT_TITEL
    size 22
    bold True
    color FARBE_TINTE

style stueck_zusatz is default:
    size 18
    color FARBE_TINTE_MATT

## Ausgang #####################################################################

style einlage_ausgang_satz is default:
    size 25
    color FARBE_TINTE
    line_spacing 9
    text_align 0.0
    layout "greedy"

style einordnung_marke is default:
    size 17
    bold True
    color FARBE_AKZENT
    kerning 2.5

style einordnung_text is default:
    size 21
    color FARBE_TINTE_MATT
    line_spacing 6
    layout "greedy"

style einordnung_quelle is default:
    size 16
    italic True
    color FARBE_LINIE

## Schaltflächen ###############################################################

style zaehler_button is default:
    background rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE, 2)
    hover_background rahmen(FARBE_AKZENT, FARBE_AKZENT, 2)
    insensitive_background rahmen(FARBE_PAPIER, FARBE_LINIE_FEIN, 2)
    padding (22, 6)

style zaehler_button_text is default:
    font SCHRIFT_TITEL
    size 26
    bold True
    color FARBE_TINTE
    hover_color FARBE_PAPIER
    insensitive_color FARBE_LINIE_FEIN
    xalign 0.5

style handel_button is default:
    background rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE, 2)
    hover_background rahmen(FARBE_AKZENT, FARBE_AKZENT, 2)
    insensitive_background rahmen(FARBE_PAPIER, FARBE_LINIE_FEIN, 2)
    padding (34, 12)

style handel_button_text is default:
    font SCHRIFT_TITEL
    size 22
    color FARBE_TINTE
    hover_color FARBE_PAPIER
    insensitive_color FARBE_LINIE_FEIN
    xalign 0.5

style abschluss_button is weiter_button:
    insensitive_background rahmen(FARBE_PAPIER, FARBE_LINIE_FEIN, 2)

style abschluss_button_text is weiter_button_text:
    insensitive_color FARBE_LINIE_FEIN


################################################################################
## Gemeinsamer Kopf
################################################################################
##
## Überschrift, Lage, Anweisung. Darunter beginnt bei ypos 430 die
## Handhabung. Alles ist mit der Maus erreichbar; es gibt in dieser Datei
## keine einzige key-Anweisung.

screen einlage_kopf(kennung):

    vbox:
        xalign 0.5
        ## OFFENER PUNKT 91: 228 war eine feste Zahl und lag damit bei
        ## Schriftstufe "sehr gross" IN der Kopfleiste - die wird dort 265
        ## Pixel hoch, und der Titel stand quer über ihrem Trennstrich.
        ## kopfhoehe() + 24 ergibt bei normaler Schrift genau dieselben 228
        ## und wandert mit. Die übrigen festen Höhen dieser Datei bleiben
        ## vorerst, siehe AUFGEFALLEN 100.
        ypos kopfhoehe() + 24
        xsize 1360
        spacing 10

        text einlage_titel(kennung) style "einlage_titel" xalign 0.5 xsize 1360

        add Solid(FARBE_AKZENT, xsize=90, ysize=3) xalign 0.5

        text einlage_einleitung(kennung) style "einlage_lage" xalign 0.5 xsize 1360

        text einlage_anweisung(kennung) style "einlage_anweisung" xalign 0.5 xsize 1360


################################################################################
## Der Rotstift
################################################################################

## DER BOGENBILDSCHIRM ########################################################
##
## Er hieß nach seiner ersten Einlage und war auch so gebaut: Ort und
## Kopf holte er unter der festen Kennung "rotstift", Kopf- und
## Schlusszeile kamen aus dem Feldpostbrief. Seit Paket 5, Schritt 2
## trägt er zwei Einlagen - den Rotstift und den Versorgungsantrag -,
## und beide sind derselbe Handgriff: ein Bogen mit Zeilen, die man
## stehen lässt oder streicht, und eine Vorschrift daneben.
##
## Alles Besondere steht jetzt in einlage_lage und kommt aus der
## jeweiligen Vorbereitung. Wer eine dritte Einlage dieser Art baut,
## schreibt eine vorbereiten-Funktion und ändert hier nichts.
## Der Name bleibt, weil Bildschirmnamen im Bestand stehen.

screen einlage_rotstift():

    default gestrichen = ()

    $ lage = einlage_lage
    $ zeilen = lage.get("zeilen", [])
    $ vorschrift = lage.get("vorschrift", [])
    $ fremd = lage.get("fremder_bogen", False)
    $ welche = einlage_aktuell if einlage_aktuell else "rotstift"
    $ winkel = lage.get("balkenwinkel", [])
    $ stempel = lage.get("stempel")

    add Solid(FARBE_PAPIER)

    use zustandskopf(einlage_ort(welche))
    use einlage_kopf(welche)

    hbox:
        xalign 0.5
        ypos 430
        spacing 28

        ## Der Bogen ##########################################################
        ##
        ## Der Rahmen liegt in einem fixed, damit der Stempel oben rechts
        ## ÜBER dem Papier sitzen kann statt daneben. fit_first heißt: Das
        ## fixed ist so groß wie der Bogen, alles Weitere legt sich darauf.

        fixed:
            fit_first True

            frame:
                xsize 1080
                padding (36, 26)
                background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

                vbox:
                    xsize 1008
                    spacing 6

                    fixed:
                        xfill True
                        ysize 24
                        text (lage.get("kopfzeile") or brief_kopfzeile()) style "bogen_kopf" xalign 0.0 yalign 0.5
                        if fremd:
                            text "Vorgelegt zur Durchsicht" style "einlage_marke" xalign 1.0 yalign 0.5

                    add Solid(FARBE_LINIE_FEIN, xsize=1008, ysize=1)

                    for stelle, zeile in enumerate(zeilen):

                        button:
                            xsize 1008
                            padding (12, 8)
                            background None
                            hover_background rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE_FEIN, 2)
                            selected_background rahmen(FARBE_PAPIER_DUNKEL, FARBE_AKZENT_MATT, 2)
                            selected (stelle in gestrichen)
                            action SetScreenVariable("gestrichen", stelle_umschalten(gestrichen, stelle))

                            hbox:
                                spacing 12

                                if stelle in gestrichen:
                                    add Solid(FARBE_AKZENT, xsize=4, ysize=26) yalign 0.5
                                else:
                                    add Solid(FARBE_SEGMENT_LEER, xsize=4, ysize=26) yalign 0.5

                                vbox:
                                    xsize 940
                                    spacing 2

                                    ## PAKET 7, SCHRITT 2: Der Streichbalken.
                                    ## Die Zeile bleibt stehen, wie sie ist -
                                    ## darüber legt sich ein Balken in
                                    ## FARBE_AKZENT, leicht gedreht, der von
                                    ## links nach rechts aufwächst.
                                    ##
                                    ## Der Balken deckt bei alpha 0,93 fast
                                    ## ganz: Man sieht, DASS dort eine Zeile
                                    ## steht, und liest sie nicht mehr. Genau
                                    ## das ist ein Rotstiftstrich.
                                    ##
                                    ## fit_first: Das fixed ist so hoch wie
                                    ## die Zeile, auch wenn sie umbricht -
                                    ## der Balken deckt dann beide Zeilen.
                                    fixed:
                                        fit_first True

                                        text zeile["text"] style "bogen_zeile" xsize 940

                                        ## Der Balken bekommt keine Größe: Ein
                                        ## Solid nimmt die Fläche, die ihm
                                        ## angeboten wird, und fit_first
                                        ## bietet ihm genau die der Zeile an -
                                        ## auch dann, wenn sie zweizeilig
                                        ## umbricht.
                                        if stelle in gestrichen:
                                            add Solid(FARBE_AKZENT):
                                                at [
                                                    Transform(rotate=(winkel[stelle] if stelle < len(winkel) else 0.8), alpha=0.93),
                                                    strich_waechst(bewegungszeit(0.22)),
                                                ]

                                    ## Nur für den Unterricht: Wonach die
                                    ## Vorschrift hier greift. Im Spiel steht
                                    ## das nicht da, sonst wäre nichts zu
                                    ## entscheiden.
                                    if persistent.analysemodus and zeile["marke"]:
                                        text zeile["marke"] style "gut_wert"

                    add Solid(FARBE_LINIE_FEIN, xsize=1008, ysize=1)

                    text (lage.get("schlusszeile") or brief_schlusszeile()) style "bogen_kopf"

            ## Der Stempel ####################################################
            ##
            ## Er setzt schräg auf die obere rechte Ecke des Bogens auf. Der
            ## Winkel kommt aus einlage_lage und nicht aus dem transform -
            ## sonst stünde er bei jedem Neuzeichnen anders.

            if stempel:
                frame:
                    xalign 1.0
                    yalign 0.0
                    xoffset -34
                    yoffset 18
                    padding (22, 8)
                    background rahmen_leer(FARBE_AKZENT, 3)
                    at [
                        Transform(rotate=lage.get("stempelwinkel", 7.0), alpha=0.55),
                        stempel_setzt(bewegungszeit(0.22)),
                    ]
                    text stempel.upper() style "bogen_stempel"

        ## Die Vorschrift #####################################################

        frame:
            xsize 400
            padding (26, 22)
            background rahmen(FARBE_PAPIER_HELL, FARBE_LINIE_FEIN, 2)

            vbox:
                xsize 348
                spacing 10

                text (vorschrift[0] if vorschrift else "") style "vorschrift_kopf" xsize 348

                add Solid(FARBE_LINIE_FEIN, xsize=348, ysize=1)

                for zeile in vorschrift[1:]:
                    hbox:
                        spacing 10
                        add Solid(FARBE_AKZENT, xsize=6, ysize=6) yoffset 9
                        text zeile style "vorschrift_zeile" xsize 320

    $ knopftext = lage.get("knopf") or ("Weitergeben" if fremd else welttext({"front": "Abschicken", "etappe": "Abschicken", "heimat": "Einwerfen"}))

    ## Der Zähler ##############################################################
    ##
    ## PAKET 7, SCHRITT 2. Ruhig gesetzt, ohne Wertung: Er sagt, wie viele
    ## Zeilen gestrichen sind, und nicht, ob das zu viele oder zu wenige
    ## sind. Daneben der Satz, dass sich ein Strich zurücknehmen lässt -
    ## ohne ihn probiert es niemand aus.

    vbox:
        xalign 0.5
        ypos 902
        spacing 4

        text (str(len(gestrichen)) + " von " + str(len(zeilen)) + " Zeilen gestrichen.") style "bogen_zaehler" xalign 0.5

        text "Ein zweiter Klick nimmt den Strich zurück." style "bogen_hinweis" xalign 0.5

    textbutton knopftext:
        xalign 0.5
        ypos 962
        style_prefix "abschluss"
        action Return(gestrichen)

    use eckmenue()
    use werthinweis()


################################################################################
## Acht Striche
################################################################################

screen einlage_portionen():

    default anteile = tuple([0] * len(PORTIONEN_EMPFAENGER))

    $ lage = einlage_lage
    $ empfaenger = lage.get("empfaenger", [])
    $ gesamt = lage.get("gesamt", PORTIONEN_GESAMT)
    $ rest = anteil_rest(anteile, gesamt)

    add Solid(FARBE_PAPIER)

    use zustandskopf(einlage_ort("portionen"))
    use einlage_kopf("portionen")

    vbox:
        xalign 0.5
        ypos 424
        spacing 16

        ## Der Laib ###########################################################

        hbox:
            xalign 0.5
            spacing 20

            hbox:
                spacing 5
                yalign 0.5
                for feld in range(gesamt):
                    if feld < gesamt - rest:
                        add Solid(FARBE_AKZENT_MATT, xsize=52, ysize=24)
                    else:
                        add Solid(FARBE_SEGMENT_LEER, xsize=52, ysize=24)

            text ("Noch zu verteilen: " + str(rest)) style "einlage_zaehler" yalign 0.5

        ## Die vier Ansprüche #################################################
        ##
        ## PAKET 7, SCHRITT 2, TEIL B.1: Unter jedem Namen steht kein fester
        ## Merksatz mehr, sondern der Zustandssatz zur gerade eingestellten
        ## Zuteilung. Er kommt aus portionen_satz() - derselben Funktion, an
        ## der auch die Auswertung hängt. Der Satz wechselt ohne Blende: Ein
        ## Text, der bei jedem Klick aufblinkt, macht acht Klicks unerträglich.

        for stelle, eintrag in enumerate(empfaenger):

            frame:
                xsize 1180
                padding (26, 12)
                background rahmen(FARBE_PAPIER_HELL, FARBE_LINIE_FEIN, 2)

                hbox:
                    xsize 1128
                    spacing 18

                    vbox:
                        xsize 700
                        spacing 1
                        yalign 0.5
                        text eintrag["name"] style "portion_name" xsize 700
                        ## Wer der Mensch ist, bleibt stehen; was deine
                        ## Zuteilung aus ihm macht, wechselt darunter.
                        text eintrag["zusatz"] style "portion_zusatz" xsize 700
                        text portionen_satz(eintrag["kennung"], anteile[stelle]) style "portion_zustand" xsize 700

                    ## Jeder zugeteilte Strich läuft ein, wenn er dazukommt.
                    ## Ren'Py zeigt nur den neuen Block neu an, also läuft die
                    ## Bewegung genau einmal und genau dort.
                    hbox:
                        spacing 4
                        yalign 0.5
                        xsize 190
                        for feld in range(gesamt):
                            if feld < anteile[stelle]:
                                add Solid(FARBE_AKZENT_MATT, xsize=18, ysize=20) at karte_kommt(bewegungszeit(0.16))

                    textbutton "-":
                        yalign 0.5
                        style_prefix "zaehler"
                        sensitive (anteile[stelle] > 0)
                        action SetScreenVariable("anteile", anteil_aendern(anteile, stelle, -1))
                        at knopf_hebt(bewegungszeit(0.12))

                    text str(anteile[stelle]) style "einlage_zaehler" yalign 0.5 xsize 34

                    textbutton "+":
                        yalign 0.5
                        style_prefix "zaehler"
                        sensitive (rest > 0)
                        action SetScreenVariable("anteile", anteil_aendern(anteile, stelle, 1))
                        at knopf_hebt(bewegungszeit(0.12))

    ## Was noch fehlt, steht unter der Schaltfläche ###########################
    ##
    ## TEIL B.4: keine Fehlermeldung, sondern eine Feststellung. Solange
    ## etwas übrig ist, bleibt die Schaltfläche unbenutzbar, und darunter
    ## steht, was noch auf dem Tisch liegt.

    textbutton "So teile ich es ein":
        xalign 0.5
        ypos 950
        style_prefix "abschluss"
        sensitive (rest == 0)
        action Return(anteile)
        at knopf_hebt(bewegungszeit(0.12))

    if rest > 0:
        text portionen_rest_satz(rest):
            style "portion_rest"
            xalign 0.5
            ypos 1014

    use eckmenue()
    use werthinweis()


################################################################################
## Die Fahrt aufs Land
################################################################################
##
## Drei Höfe in fester Reihenfolge. Wer weitergeht, kann nicht zurück:
## Das ist keine technische Einschränkung, sondern der Punkt der Übung.
## Der Preis steigt von Hof zu Hof, weil die Nachfrage steigt und weil
## der letzte Bauer weiß, wann der Zug fährt.

screen einlage_hamsterfahrt():

    default hof = 0
    default angeboten = ()
    default gegeben = ()
    default pfund = 0

    $ lage = einlage_lage
    $ gueter = lage.get("gueter", [])
    $ hoefe = lage.get("hoefe", [])

    add Solid(FARBE_PAPIER)

    use zustandskopf(einlage_ort("hamsterfahrt"))
    use einlage_kopf("hamsterfahrt")

    ## Die Weganzeige ########################################################
    ##
    ## PAKET 7, SCHRITT 3, TEIL B.3. Drei Höfe auf einer Linie, dazu die
    ## Uhrzeit. Sie läuft nicht mit - sie springt mit jedem Hof, und der
    ## letzte Zug steht rechts am Ende der Linie. Wer weitergeht, sieht,
    ## wie viel Tag ihm bleibt.

    $ steht_am = hoefe[hof]["uhr"] if hof < len(hoefe) else HAMSTER_LETZTER_ZUG

    hbox:
        xalign 0.5
        ypos 378
        spacing 0
        yalign 0.0

        for stelle, station in enumerate(hoefe):

            if stelle:
                add Solid(FARBE_LINIE_FEIN, xsize=150, ysize=2) yalign 0.5

            vbox:
                spacing 3
                xsize 120
                if stelle < hof:
                    add Solid(FARBE_LINIE, xsize=14, ysize=14) xalign 0.5
                elif stelle == hof:
                    add Solid(FARBE_AKZENT, xsize=20, ysize=20) xalign 0.5
                else:
                    add Solid(FARBE_SEGMENT_LEER, xsize=14, ysize=14) xalign 0.5
                text station["uhr"] style "weg_marke" xalign 0.5

        add Solid(FARBE_LINIE_FEIN, xsize=150, ysize=2) yalign 0.5

        vbox:
            spacing 3
            xsize 150
            if hof >= len(hoefe):
                add Solid(FARBE_AKZENT, xsize=20, ysize=20) xalign 0.5
            else:
                add Solid(FARBE_SEGMENT_LEER, xsize=14, ysize=14) xalign 0.5
            text ("Letzter Zug " + HAMSTER_LETZTER_ZUG) style "weg_marke" xalign 0.5

    if hof < len(hoefe):

        $ dieser = hoefe[hof]
        $ geboten = angebotswert(gueter, angeboten)

        hbox:
            xalign 0.5
            ypos 448
            spacing 28

            ## Der Hof ########################################################

            frame:
                xsize 700
                padding (32, 26)
                background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

                vbox:
                    xsize 636
                    spacing 12

                    text ("Hof " + str(hof + 1) + " von " + str(len(hoefe))) style "einlage_marke"

                    text dieser["name"] style "hof_name" xsize 636

                    add Solid(FARBE_AKZENT, xsize=64, ysize=3)

                    text dieser["satz"] style "hof_satz" xsize 636

                    add Solid(FARBE_LINIE_FEIN, xsize=636, ysize=1)

                    text ("Dafür gibt er: " + dieser["gibt"]) style "hof_angebot" xsize 636

                    hbox:
                        spacing 14
                        text ("Er verlangt: " + str(dieser["verlangt"])) style "hof_angebot" yalign 0.5
                        text ("Du bietest: " + str(geboten)) style "hof_angebot" yalign 0.5

                    hbox:
                        spacing 5
                        for feld in range(dieser["verlangt"]):
                            if feld < geboten:
                                add Solid(FARBE_AKZENT_MATT, xsize=44, ysize=20)
                            else:
                                add Solid(FARBE_SEGMENT_LEER, xsize=44, ysize=20)

                    ## TEIL B.1: Was der Hof dazu sagt. Der Satz wechselt
                    ## mit dem Gebot und bewertet es nicht.

                    add Solid(FARBE_LINIE_FEIN, xsize=636, ysize=1)

                    text hof_antwort(dieser, geboten) style "hof_antwort" xsize 636

                    ## TEIL B.4: Der Rucksack. Ab HAMSTER_AUFFAELLIG bekommt
                    ## der Balken einen Rahmen in FARBE_AKZENT, und darunter
                    ## steht ein Satz. Kein Ton, kein Ausrufezeichen - es
                    ## ist eine Feststellung und keine Warnung.

                    add Solid(FARBE_LINIE_FEIN, xsize=636, ysize=1)

                    frame:
                        xsize 636
                        padding (10, 8)
                        background (rahmen_leer(FARBE_AKZENT, 2) if pfund >= HAMSTER_AUFFAELLIG else None)

                        vbox:
                            xsize 612
                            spacing 6

                            hbox:
                                spacing 12
                                text ("Im Rucksack: " + str(pfund) + " Pfund") style "gut_wert" yalign 0.5
                                add Solid(FARBE_AKZENT_MATT, ysize=12, xsize=(min(pfund, 36) * 12)) yalign 0.5 at strich_waechst(bewegungszeit(0.22))

                            if pfund >= HAMSTER_AUFFAELLIG:
                                text "Der Rucksack steht ab." style "hof_antwort"

            ## Was du dabeihast ###############################################

            frame:
                xsize 700
                padding (32, 26)
                background rahmen(FARBE_PAPIER_HELL, FARBE_LINIE_FEIN, 2)

                vbox:
                    xsize 636
                    spacing 8

                    text "Was du dabeihast" style "vorschrift_kopf"

                    add Solid(FARBE_LINIE_FEIN, xsize=636, ysize=1)

                    for stelle, stueck in enumerate(gueter):

                        button:
                            xsize 636
                            padding (12, 9)
                            background None
                            hover_background rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE_FEIN, 2)
                            selected_background rahmen(FARBE_PAPIER_DUNKEL, FARBE_AKZENT_MATT, 2)
                            selected (stelle in angeboten)
                            sensitive (stelle not in gegeben)
                            action SetScreenVariable("angeboten", stelle_umschalten(angeboten, stelle))

                            hbox:
                                spacing 12
                                xsize 612

                                if stelle in gegeben:
                                    add Solid(FARBE_SEGMENT_LEER, xsize=4, ysize=24) yalign 0.5
                                elif stelle in angeboten:
                                    add Solid(FARBE_AKZENT, xsize=4, ysize=24) yalign 0.5
                                else:
                                    add Solid(FARBE_LINIE_FEIN, xsize=4, ysize=24) yalign 0.5

                                ## TEIL B.2: Die Folge steht schon beim
                                ## Anbieten da, nicht erst nach der Annahme.
                                ## Was ein Stück zu Hause bedeutet, muss man
                                ## wissen, BEVOR man es hergibt - hinterher
                                ## ist es keine Entscheidung mehr, sondern
                                ## eine Mitteilung.
                                vbox:
                                    xsize 480
                                    spacing 2
                                    yalign 0.5

                                    if stelle in gegeben:
                                        text ("{s}" + stueck["name"] + "{/s}") style "gut_wert" xsize 480
                                    else:
                                        text stueck["name"] style "gut_name" xsize 480

                                    if stelle in angeboten or stelle in gegeben:
                                        text stueck["folge"] style "gut_folge" xsize 480

                                text ("Wert " + str(stueck["wert"])) style "gut_wert" xalign 1.0 yalign 0.5

        hbox:
            xalign 0.5
            ypos 950
            spacing 24

            ## TEIL B.5: Jeder dieser drei Knöpfe verlässt einen Hof, und
            ## das ist ein Bildwechsel. Der benannte Übergang steht vor der
            ## Zustandsänderung, damit er für dieselbe Interaktion gilt.

            textbutton "Handeln":
                style_prefix "handel"
                sensitive (geboten >= dieser["verlangt"] and geboten > 0)
                action [
                    Function(hamster_weiter),
                    SetScreenVariable("gegeben", tuple(list(gegeben) + list(angeboten))),
                    SetScreenVariable("pfund", pfund + dieser["pfund"]),
                    SetScreenVariable("angeboten", ()),
                    SetScreenVariable("hof", hof + 1),
                ]
                at knopf_hebt(bewegungszeit(0.12))

            if hof + 1 < len(hoefe):
                textbutton "Zum nächsten Hof":
                    style_prefix "handel"
                    action [
                        Function(hamster_weiter),
                        SetScreenVariable("angeboten", ()),
                        SetScreenVariable("hof", hof + 1),
                    ]
                    at knopf_hebt(bewegungszeit(0.12))

            textbutton "Zum Bahnhof":
                style_prefix "handel"
                action [
                    Function(hamster_weiter),
                    SetScreenVariable("angeboten", ()),
                    SetScreenVariable("hof", len(hoefe)),
                ]
                at knopf_hebt(bewegungszeit(0.12))

    else:

        ## Der Bahnsteig ######################################################
        ##
        ## Ob kontrolliert wird, ist keine neue Entscheidung des Zufalls,
        ## sondern der Vergleich des vorgewürfelten Wertes mit der Menge
        ## im Rucksack. Deshalb ändert sich hier nichts mehr, wenn die
        ## Maus bewegt wird.

        $ kontrolle = sperre_faellig(pfund)

        if kontrolle:

            vbox:
                xalign 0.5
                ypos 430
                spacing 22

                frame:
                    xalign 0.5
                    xsize 1160
                    padding (44, 26)
                    background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

                    vbox:
                        xsize 1072
                        spacing 8
                        text "Am Bahnsteig" style "einlage_marke" xalign 0.5
                        text ("Vor der Sperre stehen zwei Beamte und ein Gendarm. Sie öffnen die Rucksäcke der Reihe nach. Du hast " + str(pfund) + " Pfund dabei.") style "hof_angebot" xalign 0.5 xsize 1072

                hbox:
                    xalign 0.5
                    spacing 30

                    button:
                        xysize (560, 220)
                        padding (30, 24)
                        background rahmen_doppelt_schatten(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)
                        hover_background rahmen_doppelt_schatten("#fffdf8", FARBE_AKZENT, FARBE_AKZENT, schattenfarbe="#15130f38")
                        action Return((gegeben, pfund, "zeigen"))

                        vbox:
                            xsize 500
                            spacing 12
                            text "Den Rucksack öffnen" style "karte_titel_links" xsize 500
                            add Solid(FARBE_AKZENT, xsize=64, ysize=3)
                            text "Du stellst ihn auf den Tisch und wartest, was übrig bleibt." style "karte_text_links" xsize 500

                    button:
                        xysize (560, 220)
                        padding (30, 24)
                        background rahmen_doppelt_schatten(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)
                        hover_background rahmen_doppelt_schatten("#fffdf8", FARBE_AKZENT, FARBE_AKZENT, schattenfarbe="#15130f38")
                        action Return((gegeben, pfund, "verbergen"))

                        vbox:
                            xsize 500
                            spacing 12
                            text "An der Sperre vorbei" style "karte_titel_links" xsize 500
                            add Solid(FARBE_AKZENT, xsize=64, ysize=3)
                            text "Der Sack unter dem Mantel, hinter einer Familie mit Kinderwagen." style "karte_text_links" xsize 500

        else:

            vbox:
                xalign 0.5
                ypos 470
                spacing 26

                frame:
                    xalign 0.5
                    xsize 1160
                    padding (48, 34)
                    background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

                    vbox:
                        xsize 1064
                        spacing 10
                        text "Am Bahnsteig" style "einlage_marke" xalign 0.5
                        text ("Heute steht niemand an der Sperre. Der Zug ist voll, und niemand sieht dir in den Rucksack. Du bringst " + str(pfund) + " Pfund nach Hause.") style "hof_angebot" xalign 0.5 xsize 1064

                textbutton "Einsteigen":
                    xalign 0.5
                    style_prefix "abschluss"
                    action Return((gegeben, pfund, "keine"))

    use eckmenue()
    use werthinweis()


################################################################################
## Was du trägst
################################################################################

## Ein Stück, einmal als Karte ################################################
##
## PAKET 7, SCHRITT 3, TEIL A.3. Dieselbe Karte liegt entweder im
## Tornister oder im Straßengraben. Sie steht hier einmal und wird an
## beiden Stellen benutzt, damit ein Stück nicht an der einen Stelle
## anders aussieht als an der anderen.
##
## "behalten" wird mitgegeben und nicht geerbt: Ein Bildschirm mit
## Parameterliste bekommt in Ren'Py seinen eigenen Namensraum und sieht
## die Variablen des aufrufenden Bildschirms nicht. SetScreenVariable
## dagegen trifft immer den äußeren Bildschirm - dort liegt "behalten".

screen tornister_stueck(stueck, drin, behalten):

    button:
        xysize (620, 78)
        padding (20, 10)
        background (rahmen(FARBE_PAPIER, FARBE_LINIE_FEIN, 2) if drin else rahmen(FARBE_PAPIER_DUNKEL, FARBE_LINIE_FEIN, 2))
        hover_background rahmen(FARBE_PAPIER_HELL, FARBE_AKZENT, 2)
        action SetScreenVariable("behalten", stelle_umschalten(behalten, stueck["kennung"]))
        at karte_kommt(bewegungszeit(0.22))

        hbox:
            xsize 580
            spacing 14

            vbox:
                xsize 466
                spacing 1
                yalign 0.5
                text stueck["name"] style "stueck_name" xsize 466
                text stueck["zusatz"] style "stueck_zusatz" xsize 466

            hbox:
                xalign 1.0
                yalign 0.5
                spacing 4
                for feld in range(stueck["last"]):
                    if drin:
                        add Solid(FARBE_AKZENT_MATT, xsize=14, ysize=18)
                    else:
                        add Solid(FARBE_SEGMENT_LEER, xsize=14, ysize=18)


screen einlage_tornister():

    default behalten = tornister_grundlast()

    $ lage = einlage_lage
    $ stuecke = lage.get("stuecke", [])
    $ grenze = lage.get("grenze", TRAGLAST_GRENZE)
    $ last = traglast(stuecke, behalten)
    $ im_tornister = [s for s in stuecke if s["kennung"] in behalten]
    $ im_graben = [s for s in stuecke if s["kennung"] not in behalten]

    add Solid(FARBE_PAPIER)

    use zustandskopf(einlage_ort("tornister"))
    use einlage_kopf("tornister")

    vbox:
        xalign 0.5
        ypos 408
        spacing 12

        ## Die Last ###########################################################
        ##
        ## TEIL A.4: Ist und Grenze stehen nebeneinander. Der senkrechte
        ## Strich nach dem siebten Feld ist die Grenze; was rechts davon
        ## liegt, ist zu viel und steht in FARBE_AKZENT statt in
        ## FARBE_AKZENT_MATT.

        hbox:
            xalign 0.5
            spacing 18

            hbox:
                spacing 4
                yalign 0.5
                for feld in range(12):
                    if feld == grenze:
                        add Solid(FARBE_TINTE, xsize=3, ysize=30) yoffset -3
                    if feld < last and feld < grenze:
                        add Solid(FARBE_AKZENT_MATT, xsize=42, ysize=24)
                    elif feld < last:
                        add Solid(FARBE_AKZENT, xsize=42, ysize=24)
                    elif feld < grenze:
                        add Solid(FARBE_SEGMENT_LEER, xsize=42, ysize=24)

            if last > grenze:
                text (str(last) + " von " + str(grenze) + " Riemen. Zu viel.") style "einlage_zaehler_warnung" yalign 0.5
            else:
                text (str(last) + " von " + str(grenze) + " Riemen") style "einlage_zaehler" yalign 0.5

        ## Im Tornister #######################################################
        ##
        ## Zwei Spalten, aufgeteilt nach geraden und ungeraden Stellen. Ein
        ## grid bräuchte immer genau acht Kinder; hier wandern Stücke
        ## hinaus, also muss die Zahl wechseln dürfen.

        text "IM TORNISTER" style "einlage_marke" xalign 0.5

        hbox:
            xalign 0.5
            spacing 20

            vbox:
                spacing 10
                for stueck in im_tornister[0::2]:
                    use tornister_stueck(stueck, True, behalten)

            vbox:
                spacing 10
                for stueck in im_tornister[1::2]:
                    use tornister_stueck(stueck, True, behalten)

        add Solid(FARBE_LINIE_FEIN, xsize=1260, ysize=1) xalign 0.5

        ## Im Straßengraben ###################################################
        ##
        ## TEIL A.3. Was hier liegt, ist noch nicht verloren: Ein Klick holt
        ## es zurück. Die Entscheidung fällt erst mit "Antreten" - deshalb
        ## steht die Fläche auch dann da, wenn noch nichts darin liegt.
        ##
        ## Die Bewegung ist karte_kommt und nicht karte_geht: Ein Stück, das
        ## den Tornister verlässt, hört als Anzeigeobjekt in derselben
        ## Sekunde auf zu bestehen, in der es fortgehen soll - es kann sein
        ## eigenes Weggehen nicht mehr zeigen. Sichtbar wird die Wanderung
        ## am Ankommen: Das Stück ist oben weg und legt sich unten hin.

        text "IM STRASSENGRABEN" style "einlage_marke" xalign 0.5

        if im_graben:
            hbox:
                xalign 0.5
                spacing 20

                vbox:
                    spacing 10
                    for stueck in im_graben[0::2]:
                        use tornister_stueck(stueck, False, behalten)

                vbox:
                    spacing 10
                    for stueck in im_graben[1::2]:
                        use tornister_stueck(stueck, False, behalten)
        else:
            text "Noch liegt nichts im Graben." style "stueck_zusatz" xalign 0.5

    textbutton "Antreten":
        xalign 0.5
        ypos 962
        style_prefix "abschluss"
        sensitive (last <= grenze)
        action Return(behalten)
        at knopf_hebt(bewegungszeit(0.12))

    if last > grenze:
        text "So viel trägt niemand bis zum Abend." style "portion_rest" xalign 0.5 ypos 1024

    use eckmenue()
    use werthinweis()


################################################################################
## Was danach anders ist
################################################################################
##
## Kein Ergebnis, keine Punkte, kein Haken. Es steht dort, was geschehen
## ist, und darunter zwei Sätze, die es einordnen. Die Belegangabe sieht
## nur, wer den Analysemodus eingeschaltet hat.

screen einlage_ausgang(kennung):

    $ vorlage = einlage_holen(kennung)

    add Solid(FARBE_PAPIER)

    use zustandskopf(einlage_ort(kennung))

    fixed:
        xalign 0.5
        ## Wie in einlage_kopf: kopfhoehe() + 32 sind bei normaler Schrift
        ## dieselben 236 und rutschen bei grosser Schrift mit.
        ypos kopfhoehe() + 32
        xsize 1400
        ysize 810

        vbox:
            align (0.5, 0.5)
            spacing 34

            frame:
                xalign 0.5
                xsize 1300
                padding (64, 40)
                background rahmen_doppelt(FARBE_PAPIER_HELL, FARBE_LINIE, FARBE_LINIE_FEIN)

                vbox:
                    xsize 1172
                    spacing 20

                    text einlage_titel(kennung) style "ausgang_marke" xalign 0.5

                    add Solid(FARBE_AKZENT, xsize=180, ysize=3) xalign 0.5

                    vbox:
                        xsize 1172
                        spacing 14
                        for satz in einlage_ausgang_saetze:
                            text satz style "einlage_ausgang_satz" xsize 1172

                    if persistent.analysemodus:
                        hbox:
                            xalign 0.5
                            spacing 28
                            for schluessel in WERTE_REIHENFOLGE:
                                if letzte_aenderungen.get(schluessel, 0) != 0:
                                    text (WERT_BEZEICHNUNG[schluessel] + " " + ("+" + str(letzte_aenderungen[schluessel]) if letzte_aenderungen[schluessel] > 0 else str(letzte_aenderungen[schluessel]))) style "analyse_wert"

            ## Die zwei Sätze #################################################

            frame:
                xalign 0.5
                xsize 1300
                padding (44, 26)
                background rahmen_oben(FARBE_PAPIER_DUNKEL, FARBE_AKZENT, 3)

                vbox:
                    xsize 1212
                    spacing 10

                    text "HISTORISCHE EINORDNUNG" style "einordnung_marke"

                    text einlage_einordnung(kennung) style "einordnung_text" xsize 1212

                    ## Seit Paket 3, Schritt 1 ist quelle ein Wörterbuch.
                    ## Angezeigt wird der Kurzbeleg; quelle_kurz() aus
                    ## script.rpy verträgt auch die alte Fassung als
                    ## schlichte Zeichenkette.
                    if persistent.analysemodus and vorlage is not None and vorlage.quelle:
                        text quelle_kurz(vorlage.quelle) style "einordnung_quelle" xsize 1212

            textbutton "Weiter":
                xalign 0.5
                style_prefix "weiter"
                action Return()

    use eckmenue()
    use werthinweis()

init offset = 0


################################################################################
## 10. Ablauf
################################################################################
##
## Eine einzige Umleitung, in derselben Bauart wie figuren.rpy und
## merkbuch.rpy: ereignis_spielen wird auf eine Fassung umgelenkt, die
## Zeile für Zeile dieselbe ist und am Ende zwei Zeilen mehr hat.
##
## An script.rpy, figuren.rpy und merkbuch.rpy ist dafür nichts zu ändern.
## Der Aufruf call ereignis_spielen(...) in hauptschleife_mit_post
## (figuren.rpy) landet durch die Umleitung hier, ebenso die vier
## Einstiegsaufrufe aus herkunft.rpy. Dass dort keine Einlage kommt,
## regelt EINLAGE_NIE_NACH.
##
## init 8 läuft nach den Eintragungen aus merkbuch.rpy (init 5). Sie
## stehen in verschiedenen Schlüsseln und stören einander nicht.

init 8 python:

    config.label_overrides["ereignis_spielen"] = "ereignis_spielen_mit_einlage"


## Die Fassung aus script.rpy, ergänzt um den Aufruf am Ende.
label ereignis_spielen_mit_einlage(kennung):

    $ gespielte_ereignisse = gespielte_ereignisse + [kennung]
    $ aktuelles_ereignis = kennung
    $ stimmung_setzen(ereignis_holen(kennung).stimmung)

    ## PAKET 8, SCHRITT 2.6. Der Umgebungsklang des Ortes, genau eine Zeile
    ## unter der Stimmung und aus demselben Grund an derselben Stelle: Hier
    ## läuft jedes der 101 Ereignisse durch. ortsklang_setzen() wechselt nur
    ## bei einem Wechsel des Klangraums, nicht bei jeder Karte. Dieselbe
    ## Zeile steht in der Fassung in script.rpy, die nicht läuft.
    $ ortsklang_setzen(ereignis_holen(kennung).ort)

    call screen karten_entscheidung(kennung)

    $ letzte_wahl = _return
    $ letztes_ergebnis = option_ausfuehren(kennung, letzte_wahl)

    call screen karten_ausgang(kennung, letzte_wahl, letztes_ergebnis["ausgang"])

    $ stimmung_setzen(None)

    ## Paket 5: Folgt auf dieses Ereignis ein Handgriff? Wer durch eine
    ## Wahl gerade woanders hinspringt (ein Ende, eine Kette), bekommt
    ## keinen: Dann ist die Lage vorbei, bevor der Handgriff anfängt.
    if not letztes_ergebnis["sprung"]:
        call einlage_pruefen(kennung)

    return


label einlage_pruefen(kennung):

    $ naechste_einlage = einlage_ziehen(kennung)

    if naechste_einlage is None:
        return

    call einlage_spielen(naechste_einlage)

    return


label einlage_spielen(kennung):

    $ einlage_vorbereiten(kennung)

    ## PAKET 8, SCHRITT 2.6. einlage_ort() löst Pfad- und Jahresvariante
    ## bereits auf; hier steht der fertige Text, nicht das Wörterbuch.
    $ ortsklang_setzen(einlage_ort(kennung))

    ## renpy.call_screen statt call screen: Der Name des Bildschirms
    ## steht im Bestand und ist deshalb erst zur Laufzeit bekannt.
    $ einlage_ergebnis = renpy.call_screen(EINLAGE_INDEX[kennung].bildschirm)

    $ einlage_anwenden(kennung, einlage_ergebnis)
    $ einlage_vermerken(kennung)

    call screen einlage_ausgang(kennung)

    $ einlage_aktuell = None
    $ einlage_lage = {}
    $ einlage_ergebnis = None

    return


################################################################################
## 11. Einlagenprobe (Werkzeug für die Entwicklung)
################################################################################
##
## Spielt alle Einlagen einer Lebenslage hintereinander, ohne Bedingungen
## und ohne Würfel. Damit lässt sich der ganze Bestand dieses Pakets in
## wenigen Minuten durchsehen, auch die Fassungen, die im normalen
## Durchgang selten vorkommen (Offizier, Etappe).
##
## Ins Hauptmenü kommt der Aufruf mit einer Zeile in screens.rpy, im
## Block "if persistent.analysemodus" des Bildschirms main_menu:
##
##     textbutton _("Einlagenprobe") action Start("einlagenprobe")

default probe_einlage_herkunft = "arbeiterschaft"
default probe_einlage_pfad = "front"
default probe_einlage_merkmal = None
default probe_einlage_stelle = 0
default probe_einlage_liste = []

screen einlagenprobe_wahl():

    default gewaehlt_herkunft = "arbeiterschaft"
    default gewaehlt_pfad = "front"
    default gewaehlt_merkmal = None

    add Solid(FARBE_PAPIER)
    add Solid(FARBE_AKZENT, xsize=10, ysize=1080) xpos 0

    vbox:
        xpos 120
        ypos 90
        xsize 1680
        spacing 16

        text "Einlagenprobe" style "abschnitt_titel" xsize 1680 text_align 0.0

        text "Alle Einlagen dieser Lebenslage nacheinander. Die Auswahl entscheidet, welche Fassung der Texte erscheint." style "abschnitt_text" xsize 1400 text_align 0.0

        add Solid(FARBE_LINIE_FEIN, xsize=1400, ysize=1)

        text "Milieu" style "einstellung_label_text"

        hbox:
            spacing 30
            style_prefix "einstellung"
            for eintrag in ["arbeiterschaft", "buergertum", "landbevoelkerung", "adel"]:
                textbutton eintrag:
                    selected (gewaehlt_herkunft == eintrag)
                    action SetScreenVariable("gewaehlt_herkunft", eintrag)

        text "Pfad" style "einstellung_label_text"

        hbox:
            spacing 30
            style_prefix "einstellung"
            for eintrag in PFAD_REIHENFOLGE:
                textbutton eintrag:
                    selected (gewaehlt_pfad == eintrag)
                    action SetScreenVariable("gewaehlt_pfad", eintrag)

        text "Zusätzliches Merkmal" style "einstellung_label_text"

        hbox:
            spacing 30
            style_prefix "einstellung"
            textbutton "keines":
                selected (gewaehlt_merkmal is None)
                action SetScreenVariable("gewaehlt_merkmal", None)
            for eintrag in ["offizier", "lazarett", "ruestung", "kinder"]:
                textbutton eintrag:
                    selected (gewaehlt_merkmal == eintrag)
                    action SetScreenVariable("gewaehlt_merkmal", eintrag)

        null height 30

        hbox:
            spacing 40
            style_prefix "weiter"
            textbutton "Einlagen abspielen" action Return((gewaehlt_herkunft, gewaehlt_pfad, gewaehlt_merkmal))
            textbutton "Zurück zum Hauptmenü" action MainMenu(confirm=False)


label einlagenprobe:

    $ zustand_zuruecksetzen()

    scene bg papier
    with UEBERGANG_KARTE()

    call screen einlagenprobe_wahl

    $ probe_einlage_herkunft = _return[0]
    $ probe_einlage_pfad = _return[1]
    $ probe_einlage_merkmal = _return[2]

    $ probe_lebenslage(probe_einlage_herkunft, probe_einlage_pfad, probe_einlage_merkmal)

    ## In der Probe entscheidet nicht der Würfel, sondern die Liste.
    $ einlagen_erlaubt = False
    $ aktuelles_jahr = 1916

    $ probe_einlage_liste = [v.kennung for v in EINLAGEN if aktueller_pfad in v.pfad]
    $ probe_einlage_stelle = 0

    while probe_einlage_stelle < len(probe_einlage_liste):
        call einlage_spielen(probe_einlage_liste[probe_einlage_stelle])
        $ probe_einlage_stelle = probe_einlage_stelle + 1

    $ einlagen_erlaubt = True

    jump einlagenprobe


################################################################################
## 12. Sprachprüfung erweitern
################################################################################
##
## Die vorhandene Prüfung geht Ereignisse und Szenen durch. Hier kommen
## drei Bestände dazu, die sie sonst nie zu sehen bekäme:
##
##   1. die festen Texte dieser Datei (Lage, Anweisung, Einordnung,
##      Briefbogen, Höfe, Tauschgut, Tornister),
##   2. die Sätze, die erst beim Auswerten entstehen. Dafür wird jede
##      Auswertung mit mehreren Eingaben durchgerechnet. Die Auswertungen
##      verändern nichts, sie lesen nur, deshalb ist das gefahrlos,
##   3. die Zwei-Sätze-Regel für jede historische Einordnung.
##
## Zusätzlich sucht die Prüfung nach Wertungswörtern. Eine Einlage hat
## kein Ergebnis, nur eine Folge; wer beim Schreiben in die Punktelogik
## rutscht, merkt es hier.
##
## init 9 läuft nach der Erweiterung aus merkbuch.rpy (init 6).

init 9 python:

    import re

    sprachpruefung_vor_einlagen = sprachpruefung_durchfuehren

    EINLAGE_WERTUNG = [
        ("gewonnen", "Wertung. Eine Einlage hat kein Ergebnis, sondern eine Folge."),
        ("geschafft", "Wertung. Beschreibe, was danach anders ist, nicht wie gut es lief."),
        ("richtig", "Wertung. Es gibt keine richtige Wahl, auch nicht nebenbei im Satz."),
        ("falsch", "Wertung. Es gibt keine falsche Wahl."),
        ("Belohnung", "Wertung."),
        ("Punkte", "Wertung. In dieser Datei werden keine Punkte vergeben."),
    ]

    ## Eingaben für den Durchlauf. Sie decken die Randfälle ab: nichts
    ## getan, alles getan, und mehrere Mischungen dazwischen.
    EINLAGE_PROBEWERTE = {
        "rotstift": [
            (),
            (0, 1, 2),
            (0, 1, 2, 3, 4, 5),
            (3, 4),
            (0, 5),
        ],
        ## Dieselben Randfälle wie beim Rotstift, dazu die Zeile mit der
        ## Unterhaltspflicht (5) allein: Sie ist die einzige, deren
        ## Streichen der Spielerin schadet, und der Fall muss in der
        ## Sprachprüfung vorkommen.
        "versorgungsantrag": [
            (),
            (0, 1),
            (0, 1, 2, 3, 4, 5),
            (3,),
            (5,),
            (0, 1, 3),
        ],
        "portionen": [
            (8, 0, 0, 0),
            (0, 4, 4, 0),
            (2, 2, 2, 2),
            (0, 0, 0, 8),
            (4, 2, 2, 0),
            (1, 3, 3, 1),
        ],
        "hamsterfahrt": [
            ((), 0, "keine"),
            ((0, 1), 10, "keine"),
            ((0, 1, 2), 22, "zeigen"),
            ((0, 1, 2, 3), 36, "verbergen"),
            ((3,), 14, "verbergen"),
        ],
        "tornister": [
            ("mantel", "zeltbahn", "kochgeschirr", "portion", "stiefel", "briefe", "putzzeug"),
            ("mantel", "kochgeschirr", "portion"),
            ("kochgeschirr", "briefe", "fremdes"),
            (),
            ("mantel", "zeltbahn", "stiefel", "fremdes"),
        ],
    }

    def einlagentexte_sammeln():
        bestand = []
        for vorlage in EINLAGEN:
            texte = []
            texte.extend(texte_sammeln(vorlage.titel))
            texte.extend(texte_sammeln(vorlage.einleitung))
            texte.extend(texte_sammeln(vorlage.anweisung))
            texte.extend(texte_sammeln(vorlage.einordnung))
            bestand.append(("Einlage " + vorlage.kennung, texte))
        bestand.append(("Briefbogen", texte_sammeln(BRIEFBOGEN)))
        bestand.append(("Vorschrift", texte_sammeln(BRIEF_VORSCHRIFT)))
        ## SEIT PAKET 7, SCHRITT 2. Der Antragsbogen und seine Vorschrift
        ## sind seit Paket 5, Schritt 2 im Spiel und liefen bis heute an der
        ## Sprach- und Lesbarkeitsprobe vorbei: Gesammelt wurde nur der
        ## Briefbogen. Ein Bogen, den niemand misst, ist genau der, auf dem
        ## der zu lange Satz stehen bleibt.
        bestand.append(("Antragsbogen", texte_sammeln(ANTRAGSBOGEN)))
        bestand.append(("Antragsvorschrift", texte_sammeln(ANTRAG_VORSCHRIFT)))
        bestand.append(("Empfänger", texte_sammeln(PORTIONEN_EMPFAENGER)))
        ## Die Zustandssätze aus Paket 7, Schritt 2. Sie stehen auf dem
        ## Bildschirm und wechseln bei jedem Klick - also gehören sie in
        ## dieselbe Prüfung wie jeder andere Satz des Spiels.
        bestand.append(("Zustandssätze", texte_sammeln(PORTIONEN_ZUSTAND)))
        bestand.append(("Ersatzempfänger", texte_sammeln(ERSATZ_EMPFAENGER)))
        bestand.append(("Tauschgut", texte_sammeln(TAUSCHGUT)))
        bestand.append(("Höfe", texte_sammeln(HAMSTER_HOEFE)))
        bestand.append(("Tornister", texte_sammeln(TORNISTER_STUECKE)))
        return bestand

    def einlagen_ausgangstexte():
        """Rechnet jede Auswertung mit mehreren Eingaben durch.

        Geprüft wird dabei die Fassung, die zum aktuellen Pfad gehört.
        Außerhalb eines Durchgangs ist das die Heimatfassung; wer die
        Frontfassung sehen will, nimmt die Einlagenprobe.
        """
        bestand = []
        for vorlage in EINLAGEN:
            saetze = []
            try:
                einlage_vorbereiten(vorlage.kennung)
                for eingabe in EINLAGE_PROBEWERTE.get(vorlage.kennung, []):
                    auswertung = EINLAGE_AUSWERTEN[vorlage.kennung](eingabe)
                    saetze.extend(auswertung.get("saetze", []))
            except Exception as fehler:
                saetze.append("Die Auswertung bricht ab: " + str(fehler))
            ## Dieselben Sätze entstehen bei mehreren Eingaben. Für die
            ## Prüfung genügt jeder einmal.
            einmalig = []
            for satz in saetze:
                if satz not in einmalig:
                    einmalig.append(satz)
            bestand.append(("Ausgang " + vorlage.kennung, einmalig))
        return bestand

    ## Welche Ketten merkt eine EINLAGE vor? ###################################
    ##
    ## SEIT PAKET 5, SCHRITT 3, TEIL D.13. Eine Kette entsteht im Regelfall
    ## aus einer Option; einlage_anwenden() kann aber ebenso vormerken
    ## (auswertung["ketten"]). Genau das tut hamsterfahrt mit
    ## heimat_verfahren - und weil niemand danach gesucht hat, fiel erst in
    ## Paket 4 auf, dass dem zweiten Glied ein Jahr fehlte.
    ##
    ## Der Unterschied zur Option: ereignis_vormerken() bekommt hier
    ## aktuelles_jahr, nicht aktuelles_jahr + kette_ab. Das zweite Glied
    ## muss also ein Jahr abdecken, das MINDESTENS so spät liegt wie das
    ## späteste Jahr der Einlage - und eines darüber hinaus, weil die
    ## Vormerkung ins Folgejahr rutscht, wenn im letzten Kapitel keine
    ## Ziehung mehr übrig ist.
    ##
    ## Gerechnet wird über EINLAGE_PROBEWERTE, weil eine Kette in einer
    ## Auswertung stehen kann, die nur bei bestimmten Eingaben greift.

    ## WARUM MEHRFACH GERECHNET WIRD. Eine Kette kann an einem Wurf
    ## hängen, nicht nur an der Eingabe: hamsterfahrt merkt heimat_verfahren
    ## nur vor, wenn an der Sperre verborgen UND nicht entkommen wird, und
    ## das Entkommen entscheidet einlage_vorbereiten() mit einem Wurf. Ein
    ## einziger Durchgang findet die Kette also in etwa der Hälfte der
    ## Fälle nicht - und eine Prüfung, die manchmal schweigt, ist keine.
    ## Vierzig Vorbereitungen je Einlage lassen die Wahrscheinlichkeit,
    ## einen Zweig zu verfehlen, unter ein Billionstel fallen.
    EINLAGE_KETTEN_RUNDEN = 40

    def einlagen_ketten_sammeln():
        """Liefert (einlage, kette, spätestes Jahr der Einlage, pfade)."""
        gefunden = []
        for vorlage in EINLAGEN:
            ketten = []
            eingaben = EINLAGE_PROBEWERTE.get(vorlage.kennung, [])
            for _runde in range(EINLAGE_KETTEN_RUNDEN):
                try:
                    einlage_vorbereiten(vorlage.kennung)
                    for eingabe in eingaben:
                        auswertung = EINLAGE_AUSWERTEN[vorlage.kennung](eingabe)
                        for name in auswertung.get("ketten", []):
                            if name not in ketten:
                                ketten.append(name)
                except Exception:
                    break
            spaetestes = max(vorlage.jahre) if vorlage.jahre else None
            for name in ketten:
                gefunden.append((vorlage.kennung, name, spaetestes,
                                 list(vorlage.pfad)))
        return gefunden

    def einlage_im_bestand(vorlage, jahr, pfad):
        """Gehört diese Einlage nach Jahr und Pfad in dieses Kapitel?

        SEIT PAKET 5, SCHRITT 3, TEIL D.15c. Die Bedingung stand bisher
        zweimal in probe_alles.py als eigener Ausdruck. Der Bildschirm
        wird hier bewusst NICHT geprüft: has_screen() gehört der Laufzeit,
        und die Werkbank hat dafür eine Attrappe.
        """
        if jahr not in vorlage.jahre:
            return False
        if pfad not in vorlage.pfad:
            return False
        return True

    def satzzahl(text):
        """Zählt Sätze. Ordnungszahlen wie 22. Februar zählen nicht mit.

        BERICHTIGT IN PAKET 5, SCHRITT 1. Die alte Regel entfernte JEDEN
        Punkt hinter einer Ziffer. Damit verschwand auch der Punkt hinter
        einer Jahreszahl, und ein Satz, der auf "im Herbst 1914." endete,
        verschmolz mit dem nächsten. Probe 5 meldete dann "einordnung hat
        1 Sätze statt genau zwei" für eine Einordnung, die zwei hatte.
        Belegt an etappe_1914_ankunft, bevor der Satz umgeschrieben wurde.

        Die Unterscheidung, die fehlte: Eine Ordnungszahl ist ein- oder
        zweistellig - der 1. März, der 22. Februar, der 9. November. Eine
        vierstellige Zahl ist eine Jahreszahl und beendet sehr wohl einen
        Satz. Genau so steht es jetzt im Ausdruck.

        Zweite Berichtigung: Ein Punkt VOR einem schließenden
        Anführungszeichen beendet den Satz ebenfalls. Vorher tat er es
        nicht, weil zwischen Punkt und Leerzeichen noch ein Zeichen
        stand - zwei Sätze wurden zu einem, und der galt als zu lang.
        """
        if not text:
            return 0
        bereinigt = re.sub(r"(?<!\d)(\d{1,2})\.(?=\s)", r"\1", text.strip())
        return len(re.findall(r"[.!?][\"“»]?(\s+|$)", bereinigt))

    def einordnungen_pruefen():
        funde = []
        for vorlage in EINLAGEN:
            fassungen = vorlage.einordnung
            if isinstance(fassungen, dict):
                paare = list(fassungen.items())
            else:
                paare = [("standard", fassungen)]
            for name, text in paare:
                anzahl = satzzahl(text)
                if anzahl != 2:
                    funde.append((
                        "Prüfen",
                        "Einordnung " + vorlage.kennung + " (" + str(name) + ")",
                        str(anzahl) + " Sätze statt zwei",
                        "Jede Einlage endet mit genau zwei Sätzen historischer Einordnung.",
                        (text or "")[:120],
                    ))
        return funde

    def sprachpruefung_durchfuehren():
        funde = sprachpruefung_vor_einlagen()

        bestand = einlagentexte_sammeln() + einlagen_ausgangstexte()

        for ort, texte in bestand:
            for satz in texte:
                klein = satz.lower()
                for begriff, begruendung in TABU_BEGRIFFE:
                    if begriff.lower() in klein:
                        funde.append(("Tabu", ort, begriff, begruendung, satz[:120]))
                for begriff, begruendung in PRUEF_BEGRIFFE:
                    if begriff.lower() in klein:
                        funde.append(("Prüfen", ort, begriff, begruendung, satz[:120]))
                for begriff, begruendung in EINLAGE_WERTUNG:
                    ## Ganzes Wort, sonst schlägt "Zeitpunkte" bei "Punkte" an.
                    if re.search(r"\b" + begriff.lower() + r"\b", klein):
                        funde.append(("Prüfen", ort, begriff, begruendung, satz[:120]))

        funde.extend(einordnungen_pruefen())

        return funde

# -*- coding: utf-8 -*-
"""probe_alles.py - die Werkbank zu "Zwischen Front und Heimat".

Prueft den gesamten Projektzustand AUSSERHALB von Ren'Py, mit reinem
Python 3:

    python probe_alles.py

Die Datei liegt neben den .rpy-Dateien, liest sie ausschliesslich und
schreibt genau zwei Dinge: diesen Bericht auf die Standardausgabe und
dieselbe Fassung in "bericht.txt" daneben. Keine .rpy-Datei wird
veraendert, keine wird angelegt.

VERFAHREN
Wie in werkzeuge/pruefen.py und werkzeuge/schicksalsprobe.py werden alle
"init N python:"-Bloecke aus den Spieldateien gelesen, um vier Leerzeichen
ausgerueckt und in EINEM gemeinsamen Namensraum ausgefuehrt. Dadurch
gewinnt - genau wie in Ren'Py - der spaetere init-Block: kapitel.rpy
ueberschreibt ereignis_ziehen(), figuren.rpy haengt sich an
zustand_zuruecksetzen() an, minispiele.rpy an die Sprachpruefung.

Die Reihenfolge ist Ren'Pys eigene: zuerst nach init-Rang (einschliesslich
"init offset"), bei gleichem Rang nach Dateinamen in alphabetischer Folge,
zuletzt nach der Stelle in der Datei. Die im Auftrag genannte Lesefolge
(gui, script, herkunft, kapitel, dialoge, figuren, merkbuch, minispiele)
bestimmt nur, in welcher Reihenfolge gelesen und berichtet wird.

Jeder Block wird mit seinem ECHTEN Dateinamen uebersetzt und um so viele
Leerzeilen vorgeschoben, dass jede Zeilennummer stimmt. Fehler und
Rueckfallmeldungen nennen deshalb die Stelle so, wie sie im Quelltext
steht, etwa "figuren.rpy:1743".

Ein Block, der sich nicht ausfuehren laesst, wird mit Datei, Blocknummer
und den ersten Zeilen gemeldet und uebersprungen. Das Skript bricht
deswegen nicht ab.

DIE ELF PROBEN
    1  Bestandstafel     Soll gegen Bestand, Ereignisse und Einlagen
    2  Pfadprobe         2000 Durchgaenge je Startpfad und Verlauf
    3  Sackgassenprobe   wie oft ein Kapitel aus Mangel endet
    4  Wertetafel        Endwerte, harte Abbrueche, reiner Kalender
    5  Belegprobe        Inhalte ohne quelle-Feld
    6  Medienprobe       alle erwarteten Dateipfade, Bild wie Ton
    7  Sprachprobe       TABU_BEGRIFFE und PRUEF_BEGRIFFE
    8  Lesbarkeit        Satzlaenge und Sprachmass Klasse 8
    9  Bewegungsprobe    Bewegungsstufen, Dauern und Uebergaenge
   10  Handgriffe        die Einlagen: Spannweite und Verteilungen
   11  Tonprobe          die harte Sperre gegen Musik, Tafeln und Orte

Der Kopf nannte bis Paket 8, Schritt 2.6 sieben Proben, obwohl seit
Paket 7 zehn liefen. Wer eine Probe hinzufuegt, zieht diese Liste mit.

Rueckgabewert 1, sobald eine Probe Beanstandungen meldet, sonst 0.
"""

import argparse
import builtins
import collections
import io
import itertools
import os
import random
import re
import sys
import traceback


################################################################################
## 1. Ordner und Dateien
################################################################################
##
## Der Auftrag nennt acht Dateien in einer bestimmten Folge. Sie wird fuer
## das Lesen und fuer den Bericht beibehalten; fuer die Ausfuehrung gilt
## die init-Ordnung aus Abschnitt 3.

LESEFOLGE = [
    "gui.rpy",
    "bewegung.rpy",
    ## SEIT PAKET 8, SCHRITT 2.6. Ohne diese Zeile liefe der init-Block von
    ## ton.rpy in der Werkbank nie, und jede Probe urteilte ueber ein Spiel
    ## ohne Ton - ORTSKLANG und ton_spielen() waeren blosse Attrappen.
    "ton.rpy",
    "script.rpy",
    "herkunft.rpy",
    "kapitel.rpy",
    "dialoge.rpy",
    "figuren.rpy",
    "merkbuch.rpy",
    "minispiele.rpy",
]

## Diese Dateien werden nur nach Bildschirmnamen durchsucht. Sie tragen
## keine Python-Bloecke, die der Spielstand braucht, aber renpy.has_screen()
## soll die Wahrheit sagen.
NUR_BILDSCHIRME = ["screens.rpy", "options.rpy"]

## Durchgaenge je Lage bei --schnell. Gross genug, dass eine Verschiebung
## um mehr als fuenf Prozentpunkte sichtbar wird, klein genug fuer eine
## Zwischenprobe zwischen zwei Arbeitsschritten.
SCHNELL_DURCHGAENGE = 300


def spielordner_finden(vorgabe=None):
    """Sucht den Ordner, in dem script.rpy liegt."""
    if vorgabe:
        return os.path.abspath(vorgabe)
    hier = os.path.dirname(os.path.abspath(__file__))
    kandidaten = [
        hier,
        os.path.join(hier, "game"),
        os.path.join(hier, os.pardir),
        os.path.join(hier, os.pardir, "game"),
        os.getcwd(),
        os.path.join(os.getcwd(), "game"),
    ]
    for pfad in kandidaten:
        if os.path.isfile(os.path.join(pfad, "script.rpy")):
            return os.path.abspath(pfad)
    return hier


################################################################################
## 2. Quelltext lesen
################################################################################

KOPF_MUSTER = re.compile(
    r"^init(?:\s+(-?\d+))?\s+python(?:\s+hide)?(?:\s+early)?(?:\s+in\s+\w+)?\s*:\s*$"
)
VERSATZ_MUSTER = re.compile(r"^init\s+offset\s*=\s*(-?\d+)\s*$")
VORGABE_MUSTER = re.compile(r"^default\s+([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(.+?)\s*$")
BILDSCHIRM_MUSTER = re.compile(r"^screen\s+([A-Za-z_][A-Za-z_0-9]*)\s*[\(:]")


def datei_zerlegen(pfad, dateiname):
    """Liest eine .rpy-Datei und trennt heraus, was ohne Ren'Py laeuft.

    Geliefert werden die init-python-Bloecke mit ihrem wirksamen Rang, die
    default-Zuweisungen und die Namen aller Bildschirme.
    """
    zeilen = io.open(pfad, encoding="utf-8").read().replace("\r\n", "\n").split("\n")

    bloecke = []
    vorgaben = []
    bildschirme = []

    versatz = 0          ## "init offset" gilt fuer den Rest der Datei
    stelle = 0
    nummer = 0

    while stelle < len(zeilen):
        zeile = zeilen[stelle]

        treffer = VERSATZ_MUSTER.match(zeile)
        if treffer:
            versatz = int(treffer.group(1))
            stelle += 1
            continue

        treffer = BILDSCHIRM_MUSTER.match(zeile)
        if treffer:
            bildschirme.append(treffer.group(1))
            stelle += 1
            continue

        treffer = VORGABE_MUSTER.match(zeile)
        if treffer:
            vorgaben.append((treffer.group(1), treffer.group(2), stelle + 1))
            stelle += 1
            continue

        treffer = KOPF_MUSTER.match(zeile)
        if treffer:
            rang = int(treffer.group(1)) if treffer.group(1) else 0
            kopfzeile = stelle + 1          ## 1-basiert, wie im Editor
            rumpf = []
            lauf = stelle + 1
            while lauf < len(zeilen):
                inhalt = zeilen[lauf]
                if inhalt.strip() == "":
                    rumpf.append("")
                    lauf += 1
                    continue
                if inhalt.startswith("    "):
                    rumpf.append(inhalt[4:])
                    lauf += 1
                    continue
                break
            nummer += 1
            ## Die Leerzeilen davor sorgen dafuer, dass jede Zeilennummer
            ## im uebersetzten Block mit der Zeile in der .rpy-Datei
            ## uebereinstimmt. Nur so nennt ein Fehler die richtige Stelle.
            quelltext = "\n" * kopfzeile + "\n".join(rumpf)
            bloecke.append({
                "datei": dateiname,
                "pfad": pfad,
                "nummer": nummer,
                "rang": rang + versatz,
                "rang_roh": rang,
                "versatz": versatz,
                "kopfzeile": kopfzeile,
                "quelltext": quelltext,
                "rumpf": rumpf,
            })
            stelle = lauf
            continue

        stelle += 1

    return bloecke, vorgaben, bildschirme


################################################################################
## 3. Attrappen fuer alles, was Ren'Py mitbringt
################################################################################
##
## Die Attrappe nimmt jeden Zugriff an und liefert wieder eine Attrappe.
## Damit laufen Bloecke durch, die Anzeigeobjekte bauen (Solid, Frame,
## Composite), ohne dass hier eine Grafikschicht nachgebaut werden muesste.
## Wo eine Attrappe eintritt, die der Namensraum nicht kannte, wird das in
## Abschnitt A des Berichts vermerkt: Eine stille Attrappe koennte einen
## echten Tippfehler im Projekt verdecken.


class Attrappe(object):

    def __init__(self, name="Attrappe"):
        object.__setattr__(self, "_name", name)

    def __call__(self, *args, **kwargs):
        return Attrappe(self._name + "()")

    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return Attrappe(self._name + "." + name)

    def __setattr__(self, name, wert):
        object.__setattr__(self, name, wert)

    def __getitem__(self, schluessel):
        return Attrappe(self._name + "[]")

    def __setitem__(self, schluessel, wert):
        pass

    def __iter__(self):
        return iter(())

    def __len__(self):
        return 0

    def __bool__(self):
        return True

    def __repr__(self):
        return "<" + self._name + ">"

    def __str__(self):
        return self._name


class GuiAttrappe(Attrappe):
    """gui.init() und der Dekorator gui.variant."""

    def __init__(self):
        Attrappe.__init__(self, "gui")

    def init(self, breite, hoehe, *args, **kwargs):
        object.__setattr__(self, "breite", breite)
        object.__setattr__(self, "hoehe", hoehe)

    def variant(self, funktion):
        return funktion


class ConfigAttrappe(Attrappe):

    def __init__(self):
        Attrappe.__init__(self, "config")
        object.__setattr__(self, "label_overrides", {})
        ## SEIT PAKET 8, SCHRITT 2.6. Zwei Listen, die das Projekt wirklich
        ## anfasst: ton.rpy haengt "umgebung" an main_menu_stop_channels und
        ## musik_sperre_durchsetzen an periodic_callbacks. Eine Attrappe
        ## liesse sich nicht in eine Liste verwandeln - list(Attrappe) wirft
        ## TypeError, und der ganze init-Block von ton.rpy braeche ab. Die
        ## Werte sind die echten Ren'Py-Vorgaben (00start.rpy 72,
        ## config.py 301), damit die Probe sieht, was wirklich dazukommt.
        object.__setattr__(self, "main_menu_stop_channels",
                           ["sound", "voice", "movie"])
        object.__setattr__(self, "periodic_callbacks", [])


class PersistentAttrappe(Attrappe):

    def __init__(self):
        Attrappe.__init__(self, "persistent")
        ## Der Analysemodus steht an, damit auch die Zweige laufen, die
        ## nur im Unterrichtswerkzeug sichtbar sind.
        object.__setattr__(self, "analysemodus", True)


class RenpyAttrappe(Attrappe):
    """renpy.random, renpy.loadable und renpy.has_screen sind echt."""

    def __init__(self, spielordner, bildschirme, medienbuch):
        Attrappe.__init__(self, "renpy")
        object.__setattr__(self, "random", random)
        object.__setattr__(self, "spielordner", spielordner)
        object.__setattr__(self, "bildschirme", bildschirme)
        object.__setattr__(self, "medienbuch", medienbuch)

    def loadable(self, pfad, directory=None):
        """Prueft die Datei im Spielordner und schreibt die Anfrage mit.

        Das Mitschreiben ist die Grundlage der Medienprobe: Jeder Pfad,
        den bild_pfad(), portrait_anzeigen() oder schrift_waehlen() je
        gesucht haben, steht danach im Medienbuch.
        """
        name = str(pfad)
        da = os.path.isfile(os.path.join(self.spielordner, name.replace("/", os.sep)))
        eintrag = self.medienbuch.setdefault(name, {"anfragen": 0, "vorhanden": da})
        eintrag["anfragen"] += 1
        eintrag["vorhanden"] = da
        return da

    def has_screen(self, name):
        return str(name) in self.bildschirme

    def call_screen(self, name, *args, **kwargs):
        return None

    def show_screen(self, name, *args, **kwargs):
        return None

    def hide_screen(self, name, *args, **kwargs):
        return None

    def say(self, wer, was, *args, **kwargs):
        return None

    def notify(self, *args, **kwargs):
        return None

    def restart_interaction(self, *args, **kwargs):
        return None


class Namensraum(dict):
    """Der gemeinsame Store aller init-Bloecke.

    Fehlt ein Name, tritt eine Attrappe ein und der Name wird vermerkt.
    Ohne das bricht ein einziger unbekannter Ren'Py-Bezeichner den ganzen
    Block ab; mit stiller Ergaenzung wuerde ein Tippfehler untergehen.
    Deshalb beides: eintreten lassen UND melden.
    """

    def __init__(self):
        dict.__init__(self)
        self.erfundene = collections.Counter()

    def __missing__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise KeyError(name)
        ## Python sucht in einem Namensraum, der kein reines dict ist,
        ## NICHT mehr selbst in den eingebauten Namen weiter. Ohne diese
        ## Zeilen bekaeme schon "object" eine Attrappe, und jede
        ## Klassendefinition im Projekt schluege fehl.
        if hasattr(builtins, name):
            wert = getattr(builtins, name)
            dict.__setitem__(self, name, wert)
            return wert
        self.erfundene[name] += 1
        wert = Attrappe(name)
        dict.__setitem__(self, name, wert)
        return wert


## Anzeigeobjekte und Ablaufbefehle, die in init-Bloecken vorkommen
## duerfen. Sie sind bewusst namentlich aufgefuehrt, damit sie NICHT als
## "erfundener Name" im Bericht auftauchen.
RENPY_NAMEN = [
    "Solid", "Text", "Frame", "Composite", "Fixed", "Transform", "Borders",
    "Color", "Image", "Crop", "AlphaMask", "LiveComposite", "Null", "At",
    "Character", "ADVCharacter", "DynamicCharacter", "Movie", "Placeholder",
    "Return", "Jump", "Call", "Show", "Hide", "Start", "MainMenu", "Quit",
    "Function", "SetVariable", "SetScreenVariable", "SetField", "ToggleField",
    "ShowMenu", "Notify", "NullAction", "Preference", "FileAction",
    "Dissolve", "Fade", "Pause", "Style", "Action", "DictValue", "FieldValue",
    "Language", "Play", "Stop", "Queue", "AudioData", "im", "Matrix",
    "Alt", "Tooltip", "OfflineAction",
]


def namensraum_bauen(spielordner, bildschirme, medienbuch):
    NS = Namensraum()
    NS["__name__"] = "spielstand"
    NS["renpy"] = RenpyAttrappe(spielordner, bildschirme, medienbuch)
    NS["config"] = ConfigAttrappe()
    NS["persistent"] = PersistentAttrappe()
    NS["gui"] = GuiAttrappe()
    NS["store"] = Attrappe("store")
    NS["_"] = lambda text: text
    NS["__"] = lambda text: text
    NS["_p"] = lambda text: text
    for name in RENPY_NAMEN:
        NS[name] = Attrappe(name)
    return NS


################################################################################
## 4. Aufbau: Bloecke ausfuehren, Vorgaben setzen
################################################################################


class Aufbau(object):

    def __init__(self, spielordner):
        self.spielordner = spielordner
        self.medienbuch = {}
        self.bildschirme = set()
        self.gelesen = []
        self.fehlend = []
        self.bloecke = []
        self.vorgaben = []
        self.abbrueche = []
        self.vorgabe_fehler = []
        self.NS = None

    def lesen(self):
        ## Ren'Py laedt die Dateien in alphabetischer Folge. Diese Folge
        ## entscheidet bei gleichem init-Rang, wer zuerst laeuft.
        ladeplatz = {}
        for stelle, name in enumerate(sorted(LESEFOLGE + NUR_BILDSCHIRME)):
            ladeplatz[name] = stelle

        for name in LESEFOLGE:
            pfad = os.path.join(self.spielordner, name)
            if not os.path.isfile(pfad):
                self.fehlend.append(name)
                continue
            bloecke, vorgaben, bildschirme = datei_zerlegen(pfad, name)
            for block in bloecke:
                block["ladeplatz"] = ladeplatz.get(name, 99)
            self.bloecke.extend(bloecke)
            self.vorgaben.extend([(name,) + v for v in vorgaben])
            self.bildschirme.update(bildschirme)
            self.gelesen.append((name, len(bloecke), len(vorgaben)))

        for name in NUR_BILDSCHIRME:
            pfad = os.path.join(self.spielordner, name)
            if os.path.isfile(pfad):
                _b, _v, bildschirme = datei_zerlegen(pfad, name)
                self.bildschirme.update(bildschirme)

        ## init-Ordnung: Rang, dann Ladeplatz der Datei, dann Stelle darin.
        self.bloecke.sort(key=lambda b: (b["rang"], b["ladeplatz"], b["kopfzeile"]))

    def ausfuehren(self):
        self.NS = namensraum_bauen(self.spielordner, self.bildschirme, self.medienbuch)
        for block in self.bloecke:
            try:
                stueck = compile(block["quelltext"], block["pfad"], "exec")
                exec(stueck, self.NS)
                block["gelaufen"] = True
            except Exception:
                block["gelaufen"] = False
                self.abbrueche.append({
                    "datei": block["datei"],
                    "nummer": block["nummer"],
                    "rang": block["rang"],
                    "kopfzeile": block["kopfzeile"],
                    "erste_zeilen": [z for z in block["rumpf"] if z.strip()][:4],
                    "meldung": traceback.format_exc().strip().split("\n")[-1],
                })

    def vorgaben_setzen(self):
        """Traegt die default-Zuweisungen nach.

        Ren'Py wertet sie erst beim Spielstart aus, also nach allen
        init-Bloecken. Genau so wird es hier gemacht.
        """
        for datei, name, ausdruck, zeile in self.vorgaben:
            if name in self.NS and not isinstance(self.NS[name], Attrappe):
                continue
            try:
                self.NS[name] = eval(ausdruck, self.NS)
            except Exception as fehler:
                self.NS[name] = None
                self.vorgabe_fehler.append((datei, zeile, name, str(fehler)))


################################################################################
## 5. Beobachtung von variante() und welttext()
################################################################################
##
## Beide Funktionen haben eine Rueckfallebene. Sie ist Absicht, aber jede
## Stelle, an der sie greift, ist eine Fassung, die noch nicht geschrieben
## wurde - vor allem die Etappe, die auf die Frontfassung zurueckfaellt.
## Die Beobachtung schreibt jeden solchen Griff mit, samt Aufrufer.
##
## Die beiden Zweigfunktionen bilden die Vorrangfolge der Vorbilder nach.
## Wer variante() oder welttext() aendert, aendert sie hier mit.

class Rueckfallbuch(object):

    def __init__(self):
        self.an = False
        self.marke = None      ## woran gerade gearbeitet wird, z. B. eine Szene
        self.eintraege = collections.Counter()
        self.gesamt = 0

    def merken(self, funktion, ort, zweig, schluessel, pfad):
        if self.marke:
            ort = self.marke + " | " + ort
        self.eintraege[(funktion, zweig, schluessel, pfad, ort)] += 1
        self.gesamt += 1


## In welches Buch gerade geschrieben wird #####################################
##
## SEIT PAKET 5, SCHRITT 1, TEIL B. Vorher hing beobachtung_einhaengen()
## GENAU EIN Buch fest in seinen Abschluss, und beide Wrapper fragten
## dessen "an". Das Schuldbuch der geschlossenen Pfade ist aber ein
## zweites Buch: durchlauf() setzt sein "an" auf True und ruft die
## Durchsicht - nur sah das niemand, weil die Wrapper weiter das
## Hauptbuch befragten, dessen "an" zu diesem Zeitpunkt noch False ist.
##
## Folge: Der Abschnitt "Textluecken auf geschlossenen Pfaden" wurde nie
## gedruckt, weil schuldbuch.eintraege immer leer blieb. Die rund
## zweihundert fehlenden Etappenfassungen waren seit dem Schliessen des
## Pfades in Paket 2, Schritt 1 unsichtbar - und der Bericht meldete
## dazu nicht etwa null, sondern gar nichts.
##
## Der Zeiger hier macht das Buch austauschbar, ohne die Wrapper neu
## einzuhaengen. An den Zahlen der offenen Pfade aendert das nichts: Das
## Hauptbuch wird nach der Durchsicht wieder eingesetzt, und sein "an"
## war waehrenddessen ohnehin False.
AKTIVES_RUECKFALLBUCH = {"buch": None}


def welt_als_text(welt):
    """Die Welt eines Inhalts als eine Zeile fuer den Bericht.

    SEIT PAKET 5, SCHRITT 1, TEIL B darf ein Brief mehrere Welten nennen
    (welt=["front", "etappe"]). Der Bericht zaehlt seine Funde ueber
    Tupel, und eine Liste laesst sich nicht in einen Counter legen -
    deshalb hier eine Zeichenkette daraus.
    """
    if welt is None:
        return "-"
    if isinstance(welt, str):
        return welt
    return "/".join(str(einzeln) for einzeln in welt)


def welt_passt(NS, welt):
    """Gehoert ein Inhalt in die Welt, in der gerade gespielt wird?

    Gefragt wird die Funktion des Projekts, nicht eine zweite Fassung
    derselben Regel in dieser Datei. Vorher stand hier ein eigener
    Vergleich; er wurde falsch, sobald welt eine Liste sein darf, und
    haette dann JEDEN Brief als Fehler gemeldet. Wo es welt_erlaubt()
    noch nicht gibt - ein aelterer Stand -, bleibt der alte Vergleich.
    """
    pruefer = NS.get("welt_erlaubt")
    if callable(pruefer):
        return bool(pruefer(welt))
    return welt == NS["briefwelt"]()


def aufrufer_bestimmen(tiefe=2):
    """Nennt Funktion und Zeile der aufrufenden Stelle im Spielcode."""
    try:
        rahmen = sys._getframe(tiefe)
    except Exception:
        return "unbekannt"
    datei = os.path.basename(rahmen.f_code.co_filename)
    return "%s in %s:%d" % (rahmen.f_code.co_name, datei, rahmen.f_lineno)


def beobachtung_einhaengen(NS, buch):

    pfade = list(NS["PFAD_REIHENFOLGE"])
    variante_echt = NS["variante"]
    welttext_echt = NS["welttext"]

    ## Nicht das Buch selbst festhalten, sondern den Zeiger darauf.
    AKTIVES_RUECKFALLBUCH["buch"] = buch

    def pfadschluessel_vorhanden(vorgaben):
        for name in pfade:
            if name in vorgaben:
                return True
        return False

    def zweig_variante(vorgaben):
        pfad = NS["aktueller_pfad"]
        for name in NS["MERKMALS_REIHENFOLGE"]:
            if NS["hat_merkmal"](name) and (str(pfad) + ":" + name) in vorgaben:
                return "pfad+merkmal", str(pfad) + ":" + name
        for name in NS["MERKMALS_REIHENFOLGE"]:
            if NS["hat_merkmal"](name) and name in vorgaben:
                return "merkmal", name
        if pfad in vorgaben:
            return "pfad", pfad
        ## Die Notloesung etappe -> front ist seit Paket 5, Schritt 1,
        ## Teil B aus variante() gestrichen. Sie muss auch hier weg,
        ## sonst misst die Werkbank etwas anderes als das Spiel: Ein
        ## Woerterbuch ohne Etappenfassung waere hier "ersatz" und im
        ## Spiel "standard", und die Gegenprobe der beiden Zaehlungen
        ## liefe auseinander.
        if "standard" in vorgaben:
            return "standard", "standard"
        return "leer", "(Vorgabewert)"

    def zweig_welttext(vorgaben):
        pfad = NS["aktueller_pfad"]
        if pfad in vorgaben:
            return "pfad", pfad
        welt = NS["briefwelt"]()
        if welt in vorgaben:
            return "ersatz", welt
        if "standard" in vorgaben:
            return "standard", "standard"
        return "leer", "(leer)"

    def variante_beobachtet(vorgaben, standard=""):
        buch = AKTIVES_RUECKFALLBUCH["buch"]
        if buch is not None and buch.an and isinstance(vorgaben, dict):
            zweig, schluessel = zweig_variante(vorgaben)
            melden = False
            if zweig == "ersatz":
                melden = True
            elif zweig in ("standard", "leer") and pfadschluessel_vorhanden(vorgaben):
                melden = True
            elif zweig == "leer":
                melden = True
            if melden:
                buch.merken("variante", aufrufer_bestimmen(2), zweig,
                            schluessel, NS["aktueller_pfad"])
        return variante_echt(vorgaben, standard)

    def welttext_beobachtet(vorgaben):
        buch = AKTIVES_RUECKFALLBUCH["buch"]
        if buch is not None and buch.an and isinstance(vorgaben, dict):
            zweig, schluessel = zweig_welttext(vorgaben)
            melden = False
            if zweig == "ersatz":
                melden = True
            elif zweig == "standard" and pfadschluessel_vorhanden(vorgaben):
                melden = True
            elif zweig == "leer":
                melden = True
            if melden:
                buch.merken("welttext", aufrufer_bestimmen(2), zweig,
                            schluessel, NS["aktueller_pfad"])
        return welttext_echt(vorgaben)

    NS["variante"] = variante_beobachtet
    NS["welttext"] = welttext_beobachtet


################################################################################
## 6. Ein Durchgang, so wie ihn die Marken spielen
################################################################################
##
## Nachgebildet wird die Kette, die im Spiel wirklich laeuft:
##
##   start -> lebenslage_bestimmen (herkunft.rpy)
##         -> hauptschleife = hauptschleife_mit_post (figuren.rpy)
##            -> ereignis_spielen = ereignis_spielen_mit_einlage
##               (minispiele.rpy) -> einlage_pruefen -> einlage_spielen
##            -> post_zustellen (figuren.rpy)
##         -> kapitelwechsel = kapitelwechsel_mit_schicksal (figuren.rpy)
##            -> schicksale_wenden
##
## Aufgerufen werden dabei ausschliesslich die Funktionen des Projekts.
## Nachgebaut sind nur die Marken selbst, denn Marken sind kein Python.

NOTBREMSE = 600

## Die beiden Wahlstrategien ###################################################
##
## Seit Paket 2, Schritt 3 wird jede Lage zweimal gespielt.
##
##   "zufall"  wuerfelt die Option. Das ist die untere Schranke: So spielt,
##             wer die Anzeige nicht liest - und so spielt ein Teil einer
##             achten Klasse in der ersten Viertelstunde.
##   "klug"    waehlt die Option, die den derzeit schlechtesten Wert am
##             wenigsten verschlechtert. Das ist die obere Schranke: So
##             spielt, wer die Kopfleiste versteht und danach handelt.
##
## Zwischen beiden Zahlen liegt der Spielraum, den das Spiel laesst. Liegen
## sie zu dicht beieinander, ist die Anzeige folgenlos; liegt die untere zu
## tief, ist der Durchgang eine Lotterie.

STRATEGIEN = ["zufall", "klug"]

## Die Ziele: seit Paket 6, Vorweg A ZWEI GRENZEN STATT EINER ##############
##
## Entscheidung 11 des Projektleiters, 4. September 2026.
##
##                    zufaellige Wahl        kluge Wahl
##   kurzer Verlauf   40 bis 60 Prozent      mindestens 80
##   langer Verlauf   20 bis 35 Prozent      mindestens 60
##
## Bis dahin galt eine Grenze fuer beide Verlaeufe. Das war ein Fehler in
## der Sache: Der kurze Verlauf ist die Unterrichtsstunde - wer ihn nicht
## uebersteht, sieht Wirtshausszene, Lebenslauf und Nachklaenge nicht, und
## das ist der Ertrag der Stunde. Der lange Verlauf ist der laengere Krieg.
## Dass die Mehrheit ihn nicht uebersteht, ist historisch wahr.
##
## Die Grenze war fuer den langen Verlauf ausserdem arithmetisch
## unerreichbar, nicht nur schwer. Paket 5, Schritt 3 hat es gemessen: Bei
## leerem Kalender, ohne Einlagen, ohne Post und mit den bestmoeglichen
## Startwerten erreicht der lange Etappenverlauf 2,0 Prozent. Eine Karte
## kostet unter kluger Wahl 0,57 bis 0,93 Punkte, und ein langer Durchgang
## hatte 31 davon - 18 bis 29 Punkte gegen eine Skala, die 12 hergibt.
##
## WAS NICHT VERHANDELBAR IST: In JEDER der sechs Lagen erreicht ein
## messbarer Anteil das Jahr 1919. 0,0 Prozent ist kein Ergebnis, sondern
## ein toter Pfad, und er wird eigens beanstandet - auch dann, wenn die
## Grenze darueber schon eine Beanstandung erzeugt hat. Wer dort landet,
## haelt an und meldet, statt die Grenze weiter zu senken.
##
## Die Zahlen sind exakt die der Entscheidung, ohne Sicherheitsabstand.
## Bei 2000 Durchgaengen je Lage liegt die Streubreite bei etwa einem
## Prozentpunkt; eine Lage bei 39,6 ist deshalb eine Beanstandung, aber
## keine Katastrophe. Wer sie liest, sieht in derselben Zeile, wie knapp
## es war.
ZIEL_KURZ = {
    "zufall_unten": 40.0,
    "zufall_oben": 60.0,
    "klug_unten": 80.0,
}

ZIEL_LANG = {
    "zufall_unten": 20.0,
    "zufall_oben": 35.0,
    "klug_unten": 60.0,
}

ZIELE = {"kurz": ZIEL_KURZ, "lang": ZIEL_LANG}

## Ein Anteil von genau null heisst: Dieser Weg fuehrt nirgendwohin.
ZIEL_MINDESTENS = 0.0

## UEBERHOLT SEIT PAKET 6, VORWEG A, aber nicht entfernt (Regel 9). Die
## drei Namen stammen aus Paket 2, Schritt 3, als eine Grenze fuer beide
## Verlaeufe galt. Sie zeigen jetzt auf die Werte des KURZEN Verlaufs,
## damit es weiterhin nur eine Wahrheit gibt; gemessen wird ueber ZIELE.
ZIEL_ZUFALL_UNTEN = ZIEL_KURZ["zufall_unten"]
ZIEL_ZUFALL_OBEN = ZIEL_KURZ["zufall_oben"]
ZIEL_KLUG_UNTEN = ZIEL_KURZ["klug_unten"]

## Das Sprachmass fuer Klasse 8 (Probe 8, seit Paket 3, Schritt 2).
LESBAR_SCHNITT = 13
LESBAR_HOECHSTENS = 20


class Durchgangsspur(object):
    """Was ein einzelner Durchgang hinterlassen hat."""

    def __init__(self, pfad, modus, strategie="zufall"):
        self.pfad = pfad
        self.modus = modus
        self.strategie = strategie
        self.ereignisse = []
        self.einlagen = []
        self.briefe = []
        self.kapitelende = []      ## (jahr, grund)
        self.ende = None
        self.werte = None
        self.schritte = 0
        ## SEIT PAKET 5, SCHRITT 3, TEIL A.2. Bisher zeigte die Wertetafel
        ## nur, WO ein Durchgang landet, nie WOVON. Ereignisse, Einlagen und
        ## Post machen zusammen rund fuenf Inhalte je kurzem Durchgang aus,
        ## und keine Messung wies aus, welche davon die vier Werte bewegt.
        ## Wer so eicht, dreht an einer Schraube, ohne zu wissen, ob sie
        ## ueberhaupt an der Welle sitzt.
        ##
        ## werte_beginn haelt den Stand NACH dem Einstieg und VOR der ersten
        ## Ziehung fest. verschiebung buecht jede spaetere Aenderung auf ihre
        ## Quelle. Die Summe aller Quellen muss genau werte minus werte_beginn
        ## ergeben - probe_wertetafel rechnet das nach und meldet jede
        ## Abweichung als Werkzeugfehler.
        self.werte_beginn = None
        self.verschiebung = {}     ## quelle -> {wert: Summe der Aenderungen}
        self.vorgaenge = {}        ## quelle -> Zahl der Male, die sie wirkte
        ## SEIT PAKET 5, SCHRITT 3, TEIL E.4: Welche der vier Faecher des
        ## Lebenslaufs am Ende dieses Durchgangs einen Eintrag haben.
        self.faecher = []
        ## Seit Paket 3, Schritt 2: Vormerkungen, die am Ende des
        ## Durchgangs nicht mehr eingeloest werden koennen.
        self.ketten_offen = 0
        ## Seit Paket 4, Vorweg D: dieselben Vormerkungen namentlich,
        ## damit der Bericht sagt, WELCHE Kette offen bleibt.
        self.ketten_offen_liste = []


class Werkbank(object):

    def __init__(self, NS, buch, umgebung):
        self.NS = NS
        self.buch = buch
        self.U = umgebung          ## gesammelte Beanstandungen der Pfadprobe
        self.erzwungene_musterung = 0
        self.verfehlter_einstieg = 0
        self.strategie = "zufall"

    ## ------------------------------------------------------ Quellenaufteilung
    ##
    ## SEIT PAKET 5, SCHRITT 3, TEIL A.2. Gemessen wird nicht, was eine
    ## Quelle zu aendern VERSPRICHT, sondern was sie tatsaechlich bewegt
    ## hat: Schnappschuss davor, Schnappschuss danach, Differenz. Das ist
    ## der einzige Weg, der auch die Kappung an 0 und 12 richtig erfasst.
    ## Eine Option, die belastung +2 ankuendigt, aber auf 12 stoesst,
    ## verschiebt eben nur um 1 - und genau diese 1 zaehlt fuer die Eichung.
    ##
    ## Gebucht wird nur, solange eine Spur mitlaeuft. Der Einstieg hat noch
    ## keine; sein Ergebnis steht deshalb in werte_beginn und ist damit
    ## Ausgangslage, nicht Verschiebung.

    def werte_jetzt(self):
        return dict(self.NS["zustand_lesen"]())

    def verschiebung_buchen(self, spur, quelle, vorher):
        if spur is None:
            return
        nachher = self.NS["zustand_lesen"]()
        buch = spur.verschiebung.setdefault(quelle, {})
        for schluessel in self.NS["WERTE_REIHENFOLGE"]:
            buch[schluessel] = buch.get(schluessel, 0) \
                + (nachher[schluessel] - vorher[schluessel])
        spur.vorgaenge[quelle] = spur.vorgaenge.get(quelle, 0) + 1

    ## ---------------------------------------------------------- Wahlstrategie

    def wahl_treffen(self, vorlage):
        """Welche Option nimmt dieser Durchgang?

        "klug" sieht nur das, was auch die Spielerin sieht: die
        angekuendigten Wertaenderungen der Optionen. Die Varianten, die
        beim Ausfuehren gezogen werden, bleiben ihr verborgen - sie
        duerfen deshalb auch hier nicht mitgerechnet werden.
        """
        NS = self.NS
        anzahl = len(vorlage.optionen)
        if anzahl <= 1:
            return 0
        if self.strategie != "klug":
            return random.randint(0, anzahl - 1)

        schluessel = NS["schwaechster_wert"]()
        hoch_ist_gut = NS["WERT_HOCH_IST_GUT"].get(schluessel, True)

        bewertet = []
        for stelle, auswahl in enumerate(vorlage.optionen):
            betrag = (auswahl.aenderungen or {}).get(schluessel, 0)
            ## Verschlechterung, immer als positive Zahl gerechnet.
            schaden = -betrag if hoch_ist_gut else betrag
            bewertet.append((schaden, stelle))

        kleinster = min(s for s, _ in bewertet)
        beste = [stelle for schaden, stelle in bewertet if schaden == kleinster]
        if len(beste) == 1:
            return beste[0]
        return random.choice(beste)

    ## ---------------------------------------------------------------- Einstieg

    def musterung_mit_ziel(self, zielpfad, strenge):
        """Wuerfelt die Musterung so lange, bis sie zum Zielpfad fuehrt.

        Der Einstieg des Spiels entscheidet ueber den Pfad. Fuer eine Probe
        JE PFAD muss der Pfad vorgegeben werden; alles andere - Vermerk,
        Befund, Heeresklasse - bleibt der Verteilung des Projekts
        ueberlassen. Deshalb wird nicht gesetzt, sondern verworfen.
        """
        NS = self.NS
        echt = NS["musterung_wuerfeln"]

        def gelenkt(herkunft, alter, s):
            letzter = None
            for _ in range(400):
                letzter = echt(herkunft, alter, s)
                if NS["pfad_aus_musterung"](letzter) == zielpfad:
                    return letzter
            ## Kommt in der Praxis nicht vor; wenn doch, wird es gezaehlt
            ## und im Bericht genannt, damit die Zahl erklaerbar bleibt.
            self.erzwungene_musterung += 1
            letzter["vermerk"] = None
            letzter["grad"] = {"front": "kv", "etappe": "gv"}.get(zielpfad, "du")
            return letzter

        NS["musterung_wuerfeln"] = gelenkt
        try:
            return NS["musterung_eintragen"](strenge)
        finally:
            NS["musterung_wuerfeln"] = echt

    def einstieg(self, zielpfad, modus):
        """Spielt Herkunft, Musterung und Erwerbslage bis zum Abschluss."""
        NS = self.NS
        W = random

        NS["zustand_zuruecksetzen"]()
        NS["spielmodus"] = modus

        herkunft = W.choice(NS["HERKUENFTE"])
        alter = W.choice(NS["JAHRGANGSWAHL"])

        ## Weg 1: ueber die Musterung. Weg 2: zivil, ueber die Erwerbslage.
        ## Zur Etappe fuehren beide, in die Heimat auch.
        if zielpfad == "front":
            ueber_musterung = True
        elif zielpfad == "etappe":
            ueber_musterung = W.randint(0, 1) == 0
        else:
            ueber_musterung = W.randint(0, 1) == 0

        geschlecht = "m" if ueber_musterung else W.choice(["m", "w"])
        if not ueber_musterung and zielpfad == "etappe":
            geschlecht = "w"

        NS["person_erzeugen"](herkunft.kennung, geschlecht, alter)

        if NS["ist_wehrpflichtig"]() and ueber_musterung:
            ## label lebenslage_musterung
            self.ereignis_spielen("einstieg_meldung", mit_einlage=True)
            strenge = "august_1914" if NS["hat_merkmal"]("kriegsfreiwillig") else "einberufung"
            NS["musterungsdaten"] = self.musterung_mit_ziel(zielpfad, strenge)
            NS["pfad_wechseln"](NS["pfad_aus_musterung"](NS["musterungsdaten"]))
            if NS["aktueller_pfad"] != "heimat":
                NS["dienststellung_setzen"]()
                if NS["aktueller_pfad"] == "front" and NS["offizierslaufbahn_offen"]():
                    self.ereignis_spielen("einstieg_offizier", mit_einlage=True)
                    NS["dienststellung_setzen"]()
                NS["ziehungen_im_kapitel"] = 0
                return NS["aktueller_pfad"]

        ## label lebenslage_zivil
        if NS["ist_wehrpflichtig"]() and not ueber_musterung:
            ## Auch wer nicht ueber die Musterung geht, ist gemustert
            ## worden: Der Weg in die Heimat fuehrt ueber a.v., d.u.,
            ## u.k. oder den nicht aufgerufenen Jahrgang.
            self.ereignis_spielen("einstieg_meldung", mit_einlage=True)
            strenge = "august_1914" if NS["hat_merkmal"]("kriegsfreiwillig") else "einberufung"
            NS["musterungsdaten"] = self.musterung_mit_ziel("heimat", strenge)
            NS["pfad_wechseln"]("heimat")

        ## Seit Paket 2, Schritt 2 entscheidet das Projekt selbst, wer aus
        ## diesem Haushalt fort ist. Die Werkbank ruft dieselbe Funktion wie
        ## label lebenslage_zivil, statt die Regel nachzubauen: Eine
        ## nachgebaute Regel weicht frueher oder spaeter ab.
        NS["familienlage_setzen"]()

        auswahl = NS["erwerb_auswahl"]()
        gewaehlt = None
        if zielpfad == "etappe":
            for eintrag in auswahl:
                if eintrag.etappe_moeglich:
                    gewaehlt = eintrag
                    break
        if gewaehlt is None and auswahl:
            gewaehlt = W.choice(auswahl)
        if gewaehlt is None:
            return NS["aktueller_pfad"]

        NS["erwerb_uebernehmen"](gewaehlt.kennung)

        eintrag = NS["erwerb_holen"](NS["lebenslage"].erwerb)
        if eintrag is not None and eintrag.etappe_moeglich and NS["ETAPPE_FREIGESCHALTET"]:
            wahl = 0 if zielpfad == "etappe" else 1
            self.ereignis_spielen("einstieg_etappe", wahl=wahl, mit_einlage=True)
            if NS["letzte_wahl"] == 0:
                NS["pfad_wechseln"]("etappe")
                NS["erwerb_bezeichnung_etappe"]()

        if NS["aktueller_pfad"] == "heimat":
            self.ereignis_spielen("einstieg_abschied", mit_einlage=True)

        ## label lebenslage_abschluss
        NS["ziehungen_im_kapitel"] = 0
        return NS["aktueller_pfad"]

    ## ------------------------------------------------------- ereignis_spielen

    def ereignis_spielen(self, kennung, wahl=None, mit_einlage=True, spur=None):
        """label ereignis_spielen_mit_einlage (minispiele.rpy)."""
        NS = self.NS
        vorlage = NS["ereignis_holen"](kennung)
        if vorlage is None:
            return {"ausgang": "", "sprung": None}

        NS["gespielte_ereignisse"] = NS["gespielte_ereignisse"] + [kennung]
        NS["aktuelles_ereignis"] = kennung
        NS["stimmung_setzen"](vorlage.stimmung)

        if wahl is None:
            wahl = self.wahl_treffen(vorlage)
        NS["letzte_wahl"] = wahl

        ## Die Klammer liegt eng um option_ausfuehren(): Was danach kommt -
        ## die Einlage - bucht sich selbst, sonst stuende ihre Wirkung
        ## zweimal in der Tafel, einmal als Ereignis und einmal als Einlage.
        vorher = self.werte_jetzt()
        ergebnis = NS["option_ausfuehren"](kennung, wahl)
        self.verschiebung_buchen(spur, "ereignis", vorher)
        NS["letztes_ergebnis"] = ergebnis
        NS["stimmung_setzen"](None)

        if spur is not None:
            spur.ereignisse.append((NS["aktuelles_jahr"], kennung, wahl))
            if NS["aktueller_pfad"] not in vorlage.pfad:
                self.U["pfad_fehler"].append((
                    "Ereignis", kennung, NS["aktueller_pfad"],
                    ", ".join(vorlage.pfad), NS["aktuelles_jahr"]))

        if mit_einlage and not ergebnis["sprung"]:
            self.einlage_pruefen(kennung, spur)
        return ergebnis

    ## --------------------------------------------------------- einlage_spielen

    def einlage_pruefen(self, ereignis_kennung, spur=None):
        """label einlage_pruefen / einlage_spielen (minispiele.rpy)."""
        NS = self.NS
        kennung = NS["einlage_ziehen"](ereignis_kennung)
        if kennung is None:
            return

        NS["einlage_vorbereiten"](kennung)

        ## Der Bildschirm einlage_kopf holt diese vier Texte, bevor der
        ## Handgriff beginnt. Sie werden hier mitgeholt, damit die
        ## Rueckfallebene von variante() auch dort sichtbar wird.
        NS["einlage_titel"](kennung)
        NS["einlage_ort"](kennung)
        NS["einlage_einleitung"](kennung)
        NS["einlage_anweisung"](kennung)

        werte = NS["EINLAGE_PROBEWERTE"].get(kennung)
        eingabe = random.choice(werte) if werte else None
        NS["einlage_ergebnis"] = eingabe
        vorher = self.werte_jetzt()
        NS["einlage_anwenden"](kennung, eingabe)
        NS["einlage_vermerken"](kennung)
        self.verschiebung_buchen(spur, "einlage", vorher)

        ## Und der Ausgangsbildschirm holt die Einordnung.
        NS["einlage_einordnung"](kennung)

        NS["einlage_aktuell"] = None
        NS["einlage_lage"] = {}
        NS["einlage_ergebnis"] = None

        if spur is not None:
            spur.einlagen.append((NS["aktuelles_jahr"], kennung))
            vorlage = NS["einlage_holen"](kennung)
            if vorlage is not None and NS["aktueller_pfad"] not in vorlage.pfad:
                self.U["pfad_fehler"].append((
                    "Einlage", kennung, NS["aktueller_pfad"],
                    ", ".join(vorlage.pfad), NS["aktuelles_jahr"]))

    ## ---------------------------------------------------------- post_zustellen

    def post_zustellen(self, spur=None):
        """label post_zustellen (figuren.rpy)."""
        NS = self.NS
        NS["post_zaehler"] = NS["post_zaehler"] + 1
        brief = NS["brief_ziehen"]()
        if brief is None:
            return

        vorher = self.werte_jetzt()
        NS["brief_zustellen"](brief)

        wahl = None
        if brief.get("antworten"):
            wahl = random.randint(0, len(brief["antworten"]) - 1)
        NS["brief_beantworten"](brief, wahl)
        self.verschiebung_buchen(spur, "post", vorher)

        if spur is not None:
            spur.briefe.append((NS["aktuelles_jahr"], brief["kennung"], brief["art"]))
            vorlage = NS["BRIEF_INDEX"].get(brief["kennung"])
            if vorlage is not None and not welt_passt(NS, vorlage.welt):
                self.U["brief_fehler"].append((
                    brief["kennung"], welt_als_text(vorlage.welt),
                    NS["briefwelt"](),
                    NS["aktueller_pfad"], NS["aktuelles_jahr"]))

    ## ------------------------------------------------------------- Hauptschleife

    def durchgang(self, zielpfad, modus, vorbelastung=None):
        """Ein vollstaendiger Durchgang von 1914 bis zum Ausgang.

        vorbelastung setzt Merkmale, BEVOR der erste Wuerfel faellt. Sie ist
        seit Paket 7, Schritt 3 da und beantwortet genau eine Frage: Wird
        ein Ende unausweichlich, wenn jemand mit einer schlechten Lage
        anfaengt? Ohne diesen Weg liesse sich das nur behaupten - die sieben
        ohne_-Merkmale entstehen im Spiel erst irgendwann mitten im Jahr
        1914, und mit welchem Rest an Kraft, weiss man dann nicht mehr.
        """
        NS = self.NS

        erreicht = self.einstieg(zielpfad, modus)
        if erreicht != zielpfad:
            self.verfehlter_einstieg += 1

        if vorbelastung:
            for name in vorbelastung:
                NS["merkmal_setzen"](name)

        spur = Durchgangsspur(erreicht, modus, self.strategie)
        ## Der Stand nach dem Einstieg ist die Ausgangslage dieses
        ## Durchgangs. Alles davor - Musterung, Erwerbslage, die drei
        ## einstieg_-Ereignisse - gehoert zur Herkunft und nicht zu den
        ## Quellen, die dieser Schritt eicht.
        spur.werte_beginn = self.werte_jetzt()

        while True:
            spur.schritte += 1
            if spur.schritte > NOTBREMSE:
                self.U["notbremse"].append((zielpfad, modus, NS["aktuelles_jahr"]))
                spur.ende = "notbremse"
                break

            ende = NS["ende_pruefen"]()
            if ende:
                spur.kapitelende.append((NS["aktuelles_jahr"], "abbruch"))
                spur.ende = ende
                break

            if NS["ziehungen_im_kapitel"] >= NS["ziehungen_pro_kapitel"]():
                if self.kapitelwechsel(spur, "soll"):
                    break
                continue

            kennung = NS["ereignis_ziehen"](
                NS["aktuelles_jahr"], NS["aktueller_pfad"], NS["spielmodus"])

            if kennung is None:
                if self.kapitelwechsel(spur, "leer"):
                    break
                continue

            ergebnis = self.ereignis_spielen(kennung, spur=spur)

            if ergebnis["sprung"]:
                spur.kapitelende.append((NS["aktuelles_jahr"], "sprung"))
                spur.ende = ergebnis["sprung"]
                break

            self.post_zustellen(spur)

        ## label ende_ueberlebt_mit_wirtshaus (kapitel.rpy, seit Paket 5,
        ## Schritt 2). Jeder Durchgang, der den Epilog uebersteht, spielt
        ## die Wirtshausszene und die Wahl an ihrem Ende; die Marke
        ## ende_ueberlebt ist dafuer umgeleitet.
        ##
        ## NACHGETRAGEN IN PAKET 5, SCHRITT 3. Die Werkbank endete bisher
        ## an ende_ueberlebt und spielte die Wahl nicht. Damit sah sie die
        ## drei Wirtshausmerkmale nie - und das Fach "Wie es ausging" stand
        ## im Bericht auf 0,0 Prozent, obwohl das Spiel es in jedem
        ## Durchgang fuellt, der 1919 erreicht. Eine Null, die nur bedeutet,
        ## dass niemand hingesehen hat.
        if spur.ende == "ende_ueberlebt":
            self.ereignis_spielen("wirtshaus_wahl", spur=spur)

        spur.werte = dict(NS["zustand_lesen"]())

        ## Der Lebenslauf entsteht aus dem Stand am Ende des Durchgangs.
        ## Gefragt wird dieselbe Funktion, die auch der Bildschirm ruft -
        ## eine zweite Auswahlregel hier waere genau der Nachbau, den
        ## Regel 11 verbietet.
        if callable(NS.get("nachklaenge_nach_faechern")):
            try:
                spur.faecher = [eintrag.get("fach")
                                for eintrag in NS["nachklaenge_nach_faechern"]()]
            except Exception:
                spur.faecher = []

        if callable(NS.get("kette_offen_zaehlen")):
            spur.ketten_offen = NS["kette_offen_zaehlen"](NS["aktuelles_jahr"])
        ## Seit Paket 4, Vorweg D: nicht nur WIE VIELE Vormerkungen offen
        ## bleiben, sondern WELCHE. Eine Gesamtzahl sagt nicht, an welcher
        ## Kette gearbeitet werden muss.
        jahr_am_ende = NS["aktuelles_jahr"]
        for eintrag in NS.get("vorgemerkte_ereignisse", []):
            vorlage = NS["ereignis_holen"](eintrag["kennung"])
            if vorlage is None or not [j for j in vorlage.jahre if j >= jahr_am_ende]:
                spur.ketten_offen_liste.append(eintrag["kennung"])
        return spur

    def kapitelwechsel(self, spur, grund):
        """label kapitelwechsel_mit_schicksal. True heisst: Durchgang zu Ende."""
        NS = self.NS
        spur.kapitelende.append((NS["aktuelles_jahr"], grund))

        ## PAKET 8, SCHRITT 2.5: Die Nachziehregel wird nicht nachgebaut,
        ## sondern gefragt - dieselbe Funktion, die auch die Marke ruft,
        ## und an derselben Stelle: ganz oben, vor den Schicksalen, weil
        ## schicksale_wuerfeln() post_im_jahr zuruecksetzt (Regel 11).
        if callable(NS.get("rhythmus_kapitel_abschliessen")):
            NS["rhythmus_kapitel_abschliessen"]()

        folgejahr = NS["naechstes_kapitel"](NS["aktuelles_jahr"])
        if folgejahr is None:
            spur.ende = "ende_ueberlebt"
            return True

        NS["aktuelles_jahr"] = folgejahr
        NS["ziehungen_im_kapitel"] = 0
        NS["wiederholbare_freigeben"]()

        ## Kalender und Schicksale sind zwei verschiedene Quellen und werden
        ## getrennt gebucht: Der Kalender ist eine Stellschraube dieses
        ## Schrittes, die Schicksale sind Inhalt und bleiben unangetastet.
        ## Stuenden sie in einer Zeile, waere nicht zu sehen, welche von
        ## beiden den Jahreswechsel teuer macht.
        vorher = self.werte_jetzt()
        NS["letzte_kapitelwirkung"] = NS["kapitel_wirkung_anwenden"](NS["aktuelles_jahr"])
        self.verschiebung_buchen(spur, "kalender", vorher)

        vorher = self.werte_jetzt()
        NS["schicksale_wuerfeln"]()
        self.verschiebung_buchen(spur, "schicksal", vorher)
        return False


################################################################################
## 7. Der Bericht
################################################################################


class Bericht(object):

    def __init__(self):
        self.zeilen = []

    def __call__(self, text=""):
        self.zeilen.append(text)

    def titel(self, text):
        self("")
        self("=" * 78)
        self(text)
        self("=" * 78)

    def unterteil(self, text):
        self("")
        self(text)
        self("-" * 78)

    def text(self):
        return "\n".join(self.zeilen) + "\n"


def prozent(teil, gesamt):
    if not gesamt:
        return 0.0
    return 100.0 * teil / float(gesamt)


################################################################################
## 8. Probe 1: Bestandstafel
################################################################################


def probe_bestandstafel(NS, B):
    beanstandungen = 0
    geprueft = 0

    B.titel("PROBE 1  BESTANDSTAFEL")
    B("Soll ist die Zahl der vorgesehenen Ziehungen (KAPITEL_ZIEHUNGEN).")
    B("Frei sind Ereignisse ohne Merkmalsbedingung, gebunden die uebrigen.")
    B("Die Spalte Lage nennt seit Paket 2, Schritt 1 drei Stufen und rechnet")
    B("mit derselben Funktion wie der Bildschirm im Spiel (bestandslage in")
    B("kapitel.rpy): Unterdeckung heisst frei unter Soll, knapp heisst")
    B("weniger als %d Ereignisse Reserve. Beanstandet wird nur Unterdeckung."
      % NS.get("BESTAND_RESERVE", 2))

    ## Ein Pfad, den der Einstieg nicht mehr vergibt, kann heute niemanden
    ## in eine Sackgasse fuehren. Seine Luecken bleiben trotzdem stehen -
    ## als Schuld fuer das Paket, das ihn wieder oeffnet.
    offen = pfade_erreichbar(NS)
    geschlossen = [p for p in NS["PFAD_REIHENFOLGE"] if p not in offen]
    if geschlossen:
        B("")
        B("Geschlossene Pfade: %s. Ihre Zeilen tragen 'geschlossen' und"
          % ", ".join(NS["PFAD_MARKE"].get(p, p) for p in geschlossen))
        B("zaehlen nicht als Beanstandung, weil sie niemanden mehr treffen.")

    knappe = 0
    schuld = 0
    for modus in ["kurz", "lang"]:
        B.unterteil("Ereignisse - " + NS["MODUS_BEZEICHNUNG"].get(modus, modus))
        B("%-6s %-16s %6s %6s %10s   %-14s %s" % (
            "Jahr", "Pfad", "Soll", "Frei", "Gebunden", "Lage", "Befund"))
        for jahr in NS["KAPITEL_JAHRE"]:
            for pfad in NS["PFAD_REIHENFOLGE"]:
                geprueft += 1
                frei, bedingt = NS["bestand_zaehlen"](jahr, pfad, modus)
                soll = NS["ziehungen_pro_kapitel"](jahr, modus)
                lage, lage_text = NS["bestandslage"](frei, soll)
                if pfad in geschlossen:
                    if lage == "unterdeckung":
                        schuld += 1
                    lage_text = "geschlossen"
                    befund = ("es fehlen %d" % (soll - frei)) if lage == "unterdeckung" else ""
                elif lage == "unterdeckung":
                    beanstandungen += 1
                    befund = ">> FEHLT << %d Ereignis(se)" % (soll - frei)
                elif lage == "knapp":
                    knappe += 1
                    befund = "keine Reserve"
                else:
                    befund = ""
                B("%-6d %-16s %6d %6d %10d   %-14s %s" % (
                    jahr, NS["PFAD_MARKE"].get(pfad, pfad), soll, frei, bedingt,
                    lage_text, befund))

    ## Einlagen ###############################################################
    ##
    ## EINLAGEN_JE_KAPITEL nennt eine Obergrenze, kein Ziel: Eine Einlage
    ## kommt nur, wenn Abstand, Kapitelgrenze und der Wurf zusammenpassen.
    ## Unterdeckung heisst hier deshalb: In diesem Kapitel kann auf diesem
    ## Pfad die vorgesehene Zahl gar nicht erreicht werden.

    def einlagen_bestand(jahr, pfad):
        frei = 0
        bedingt = 0
        wiederholbar = 0
        for vorlage in NS["EINLAGEN"]:
            ## Jahr und Pfad fragt seit Paket 5, Schritt 3 das Projekt
            ## (einlage_im_bestand). Der Bildschirm bleibt hier: Er
            ## gehoert der Laufzeit, nicht dem Bestand.
            if not NS["einlage_im_bestand"](vorlage, jahr, pfad):
                continue
            if not NS["renpy"].has_screen(vorlage.bildschirm):
                continue
            if vorlage.braucht:
                bedingt += 1
            else:
                frei += 1
                if vorlage.wiederholbar:
                    wiederholbar += 1
        return frei, bedingt, wiederholbar

    for modus in ["kurz", "lang"]:
        soll = NS["EINLAGEN_JE_KAPITEL"].get(modus, 1)
        B.unterteil("Einlagen - " + NS["MODUS_BEZEICHNUNG"].get(modus, modus)
                    + "  (hoechstens %d je Kapitel)" % soll)
        B("Eine wiederholbare Einlage kann die Zahl allein fuellen. Beanstandet")
        B("wird deshalb nur, wo gar keine Einlage steht oder wo der Bestand die")
        B("vorgesehene Zahl auch mit Wiederholung nicht erreicht.")
        B("%-6s %-16s %6s %6s %14s %10s   %s" % (
            "Jahr", "Pfad", "Soll", "Frei", "wiederholbar", "Gebunden", "Befund"))
        for jahr in NS["KAPITEL_JAHRE"]:
            for pfad in NS["PFAD_REIHENFOLGE"]:
                geprueft += 1
                frei, bedingt, wiederholbar = einlagen_bestand(jahr, pfad)
                if pfad in geschlossen:
                    if frei == 0:
                        schuld += 1
                    befund = "geschlossen"
                elif frei == 0:
                    beanstandungen += 1
                    befund = ">> FEHLT << keine Einlage auf diesem Pfad"
                elif frei < soll and not wiederholbar:
                    beanstandungen += 1
                    befund = ">> FEHLT << %d Einlage(n)" % (soll - frei)
                else:
                    befund = "in Ordnung"
                B("%-6d %-16s %6d %6d %14d %10d   %s" % (
                    jahr, NS["PFAD_MARKE"].get(pfad, pfad), soll, frei,
                    wiederholbar, bedingt, befund))

    B("")
    B("Summe der vorgesehenen Ziehungen in den Kriegsjahren: kurz %d, lang %d."
      % (NS["ziehungen_summe"]("kurz"), NS["ziehungen_summe"]("lang")))
    B("Zeilen ohne Reserve (Lage 'knapp'): %d. Sie zaehlen nicht als"
      % knappe)
    B("Beanstandung, sind aber die naechsten Kandidaten fuer eine Sackgasse.")
    if geschlossen:
        B("Zeilen auf geschlossenen Pfaden mit Unterdeckung: %d. Sie zaehlen"
          % schuld)
        B("heute nicht mit und sind die Schuld des Pakets, das sie oeffnet.")

    ## Traeger des Jahresbogens ################################################
    ##
    ## SEIT PAKET 4, VORWEG A. KAPITEL_BOGEN nennt je Jahr und Pfad die
    ## Ereignisse, die das Jahr tragen. Ein Traeger ohne kern=True kann im
    ## kurzen Verlauf gar nicht gezogen werden: Sein Zuschlag bleibt bis
    ## zum Kapitelende offen und haelt alle uebrigen Ereignisse klein.
    ## Das ist an keiner Stelle sichtbar, solange niemand danach sucht.
    B.unterteil("Traeger des Jahresbogens (KAPITEL_BOGEN)")
    B("Jeder Traeger muss kern=True haben, sonst traegt er im kurzen")
    B("Verlauf nichts. Traeger auf geschlossenen Pfaden zaehlen mit: Sie")
    B("werden falsch, sobald das Paket den Pfad oeffnet.")
    B("")
    if callable(NS.get("traeger_ohne_kern")):
        funde = NS["traeger_ohne_kern"]()
        traeger_gesamt = 0
        for jahr in NS["KAPITEL_JAHRE"]:
            for pfad in NS["PFAD_REIHENFOLGE"]:
                traeger_gesamt += len(NS["kapitel_bogen"](jahr, pfad).get("träger", []))
        geprueft += traeger_gesamt
        B("   Traeger insgesamt: %d" % traeger_gesamt)
        if not funde:
            B("   keine Beanstandung")
        for jahr, pfad, kennung, grund in funde:
            beanstandungen += 1
            if grund == "fehlt":
                B("   >> FEHLER << %d %-8s %-38s gibt es nicht"
                  % (jahr, pfad, kennung))
            else:
                B("   >> FEHLER << %d %-8s %-38s hat kern=False"
                  % (jahr, pfad, kennung))
    else:
        B("   nicht geprueft: bogen_traeger_offen/traeger_ohne_kern fehlt")

    ## Felder ohne einen einzigen Traeger ######################################
    ##
    ## SEIT PAKET 5, SCHRITT 3, PUNKT 13a. Die Pruefung darueber sagt, ob
    ## ein eingetragener Traeger taugt. Sie konnte nie sagen, dass gar
    ## keiner eingetragen ist - und genau so standen 1917 bis 1919 auf
    ## allen drei Pfaden neun Felder leer. BOGEN_ZUSCHLAG griff dort
    ## nirgends, und der Bericht meldete dazu nicht null, sondern nichts.
    B("")
    if callable(NS.get("traeger_fehlend")):
        leer = NS["traeger_fehlend"]()
        geprueft += len(NS["KAPITEL_JAHRE"]) * len(NS["PFAD_REIHENFOLGE"])
        B("   Felder ohne Traeger: %d von %d" % (
            len(leer), len(NS["KAPITEL_JAHRE"]) * len(NS["PFAD_REIHENFOLGE"])))
        if not leer:
            B("   keine Beanstandung")
        for jahr, pfad in leer:
            beanstandungen += 1
            B("   >> FEHLER << %d %-8s kein Traeger eingetragen - das Jahr hat"
              % (jahr, pfad))
            B("                auf diesem Pfad keinen tragenden Moment.")
    else:
        B("   nicht geprueft: traeger_fehlend fehlt")

    ## Nachtraege, die ins Leere greifen #######################################
    ##
    ## SEIT PAKET 6, SCHRITT 1. DOMINANZ_NACHTRAG und die beiden
    ## Kettennachtraege in kapitel.rpy finden ihre Option ueber den TITEL.
    ## Ein Optionstitel ist damit ein Bezeichner, sieht aber aus wie Text -
    ## und in einem Textpaket schreibt man Titel um.
    ##
    ## Genau das ist in diesem Schritt passiert: Aus "Mitspielen" wurde
    ## "Ihnen recht geben", und damit fiel front_urlaub auf die Werte
    ## zurueck, die Paket 4 als dominiert erkannt und ersetzt hatte. Aus
    ## "Hinuebergehen" wurde "Ueber die Bruestwehr steigen", und damit war
    ## die Verbruederungskette abgeschaltet. Keine Kennung hatte sich
    ## geaendert, keine Zahl im Quelltext - und trotzdem sprang der kurze
    ## Etappenverlauf von 53,8 auf 61,0 Prozent.
    ##
    ## Ein Nachtrag, der keinen Treffer hat, ist ab jetzt eine
    ## Beanstandung und keine stille Aenderung mehr.
    B.unterteil("Nachtraege, die keine Option treffen")
    B("DOMINANZ_NACHTRAG und die Kettennachtraege suchen ihre Option ueber")
    B("den Optionstitel. Wer einen Titel umschreibt, schaltet den Nachtrag")
    B("ab - lautlos. Hier steht, ob ein Schluessel ins Leere greift.")
    B("")
    if isinstance(NS.get("NACHTRAG_OHNE_TREFFER"), list):
        offen_nachtrag = NS["NACHTRAG_OHNE_TREFFER"]
        geprueft += 1
        if not offen_nachtrag:
            B("   keine Beanstandung - jeder Schluessel trifft eine Option")
        for art, kennung, titel, grund in offen_nachtrag:
            beanstandungen += 1
            B("   >> FEHLER << %-9s %-34s %s" % (art, kennung, titel))
            B("                %s" % grund)
    else:
        B("   nicht geprueft: NACHTRAG_OHNE_TREFFER fehlt")

    ## Geplante Rueckbezuege aus kapitel.rpy
    zeilen = NS["nachhallbericht"]()
    offen = [z for z in zeilen if not z["vorhanden"]]
    B("")
    B("Geplante Rueckbezuege (NACHHALL_PLAN): %d von %d bestehen noch nicht."
      % (len(offen), len(zeilen)))
    for zeile in offen:
        B("   fehlt: %-40s %d  %-8s %s" % (
            zeile["kennung"], zeile["jahr"], zeile["pfad"], zeile["merkmal"]))

    ## Der zusammengefuehrte Plan ##############################################
    ##
    ## SEIT PAKET 4, VORWEG C. NACHHALL_PLAN und KETTEN_PLAN nennen
    ## dieselben kuenftigen Ereignisse aus zwei Blickwinkeln. Wer nur
    ## eine der beiden Listen abarbeitet, baut eines doppelt oder gar
    ## nicht. Gefuehrt wird der Nachhallplan; der Kettenplan traegt die
    ## Vorgeschichte nach.
    if callable(NS.get("inhaltsplan")):
        B.unterteil("Zusammengefuehrter Inhaltsplan (Nachhall + Ketten)")
        B("Herkunft 'beide' heisst: Die Kennung steht in beiden Plaenen und")
        B("wird trotzdem nur EINMAL gebaut.")
        B("")
        B("%-40s %-6s %-8s %-9s %-12s %s" % (
            "Kennung", "Jahr", "Pfad", "Herkunft", "Zustand", "geht hervor aus"))
        plan = NS["inhaltsplan"]()
        for zeile in plan:
            aus = zeile["kette_von"] or ""
            if aus and zeile["abstand"] is not None:
                aus = "%s (+%d)" % (aus, zeile["abstand"])
            B("%-40s %-6s %-8s %-9s %-12s %s" % (
                zeile["kennung"],
                zeile["jahr"] if zeile["jahr"] else "-",
                zeile["pfad"],
                zeile["herkunft"],
                "besteht" if zeile["vorhanden"] else "fehlt",
                aus))
        doppelt = NS["inhaltsplan_doppelte"]()
        B("")
        B("Eintraege insgesamt: %d, davon in beiden Plaenen: %d (%s)"
          % (len(plan), len(doppelt), ", ".join(doppelt) if doppelt else "keine"))
        B("Noch zu bauen: %d." % len([z for z in plan if not z["vorhanden"]]))

    return beanstandungen, geprueft


################################################################################
## 9. Proben 2, 3 und 4: der grosse Durchlauf
################################################################################


def textdurchsicht(NS, buch, pfade=None):
    """Loest jede Textfassung einmal je Pfad und Merkmalslage auf.

    Die Szenen aus dialoge.rpy laufen nicht in der Hauptschleife, und die
    Ereignistexte holt der Bildschirm. Ohne diese Durchsicht bliebe genau
    dort unbemerkt, wo ein Pfad noch keine eigene Fassung hat.

    Welche Pfade angesehen werden, entscheidet der Aufrufer. Ein
    geschlossener Pfad wird getrennt gemessen: Seine Luecken sind eine
    Schuld fuer spaeter, aber heute trifft sie niemand.
    """
    if pfade is None:
        pfade = list(NS["PFAD_REIHENFOLGE"])
    merkmalslagen = [
        [],
        ["offizier", "buergertum"],
        ["adel"],
        ["lazarett"],
        ["ruestung", "arbeiterschaft"],
        ["landbevoelkerung"],
        ["haushalt"],
        ## Seit Paket 2, Schritt 2: die drei Familienmerkmale. Ohne sie
        ## bliebe die Bahnsteigszene mit ihren vier Fassungen ungeprueft.
        ["ehemann_im_feld", "haushalt"],
        ["vater_im_feld"],
        ["bruder_im_feld"],
    ]

    merker = (NS["aktueller_pfad"], list(NS["merkmale"]), NS["aktuelles_jahr"])
    try:
        for pfad in pfade:
            for lage in merkmalslagen:
                NS["aktueller_pfad"] = pfad
                NS["merkmale"] = list(lage)
                for jahr in NS["KAPITEL_JAHRE"]:
                    NS["aktuelles_jahr"] = jahr

                    for szene in NS["SZENEN"]:
                        if szene.ort:
                            buch.marke = "Szene " + szene.kennung + " (Ort)"
                            NS["variante"](szene.ort, None)
                        buch.marke = "Szene " + szene.kennung
                        for zeile in szene.zeilen:
                            if zeile.text is not None:
                                NS["szenentext"](zeile.text)

                    ## Eine Einlage wird nur dort angesehen, wo sie auch
                    ## vorkommen kann. Sonst meldete die Durchsicht Loecher
                    ## in Fassungen, die niemand je zu sehen bekommt.
                    for vorlage in NS["EINLAGEN"]:
                        if not NS["einlage_im_bestand"](vorlage, jahr, pfad):
                            continue
                        buch.marke = "Einlage " + vorlage.kennung
                        NS["einlage_ort"](vorlage.kennung)
                        NS["einlage_einleitung"](vorlage.kennung)
                        NS["einlage_anweisung"](vorlage.kennung)
                        NS["einlage_einordnung"](vorlage.kennung)
    finally:
        buch.marke = None
        NS["aktueller_pfad"], NS["merkmale"], NS["aktuelles_jahr"] = merker


def ziehbare_ereignisse(NS):
    """Alle Ereignisse, die im Spiel ueberhaupt erscheinen koennen.

    Das sind die frei ziehbaren UND die, auf die eine Option als Kette
    zeigt. Ein nur_kette-Ereignis ohne Zeiger darauf kann niemand sehen;
    eines mit Zeiger sehr wohl - kette_faellig() holt es aus der Vormerkung.

    SEIT PAKET 5, SCHRITT 3, TEIL D.15c fragt diese Stelle das Projekt,
    statt die Zeiger noch einmal selbst zusammenzusuchen. Gefragt werden
    zwei Quellen, denn es gibt zwei: die Optionen (kettenziele in
    script.rpy) und die Einlagen (einlagen_ketten_sammeln in
    minispiele.rpy). Die zweite fehlte hier bis heute.
    """
    ziele = set(kettenziele_holen(NS))
    return [v for v in NS["EREIGNISSE"]
            if (not v.nur_kette) or (v.kennung in ziele)]


def kettenziele_holen(NS):
    """Alle Kennungen, auf die irgendetwas als Kette zeigt.

    Optionen UND Einlagen. Beide Sammelfunktionen gehoeren dem Projekt;
    diese Werkbank vereinigt nur, was sie liefern.
    """
    ziele = set()
    if callable(NS.get("kettenziele")):
        ziele.update(NS["kettenziele"]())
    if callable(NS.get("einlagen_ketten_sammeln")):
        for _einlage, kette, _jahr, _pfade in NS["einlagen_ketten_sammeln"]():
            ziele.add(kette)
    return ziele


def pfade_erreichbar(NS):
    """Welche Pfade kann der Einstieg ueberhaupt erreichen?

    Gefragt werden die Funktionen des Projekts selbst, nicht eine Liste in
    dieser Datei. Ein Pfad, den der Einstieg nicht mehr vergibt, wird nicht
    mehr durchgespielt: Zahlen ueber einen unerreichbaren Pfad sind keine
    Messung, sondern Rauschen.
    """
    erreichbar = set(["heimat"])        ## Der Zivilweg endet immer dort.

    for grad in NS.get("MUSTERUNG_GRADE", ["kv", "gv", "av", "du"]):
        try:
            erreichbar.add(NS["pfad_aus_musterung"]({"grad": grad, "vermerk": None}))
        except Exception:
            pass

    ## Der zweite Weg in die Etappe fuehrt ueber eine Erwerbslage mit
    ## etappe_moeglich - aber nur, solange der Schalter offen ist.
    if NS.get("ETAPPE_FREIGESCHALTET"):
        for eintrag in NS.get("ERWERBSLAGEN", []):
            if getattr(eintrag, "etappe_moeglich", False):
                erreichbar.add("etappe")

    return [p for p in NS["PFAD_REIHENFOLGE"] if p in erreichbar]


def protokoll_leeren(NS):
    """Setzt die Protokolle zurueck, die das Spiel selbst fuehrt.

    Seit Paket 2, Schritt 1 schreibt das Spiel jeden Griff in die
    Rueckfallebene selbst mit (variantenersatz_protokoll in dialoge.rpy)
    und meldet Post aus einer fremden Welt (postwelt_protokoll in
    figuren.rpy). Beides wird hier geleert und danach gegen die eigene
    Beobachtung gehalten: Zwei Zaehlungen desselben Vorgangs, die
    auseinanderlaufen, sind ein Befund fuer sich.
    """
    for name in ("variantenersatz_protokoll", "postwelt_protokoll"):
        wert = NS.get(name)
        if isinstance(wert, list):
            del wert[:]
    wert = NS.get("variantenersatz_stellen")
    if isinstance(wert, dict):
        wert.clear()
    if "variantenersatz_gesamt" in NS:
        NS["variantenersatz_gesamt"] = 0


def durchlauf(NS, buch, durchgaenge):
    """Spielt alle Lagen durch und sammelt alles, was die Proben brauchen."""

    umgebung = {
        "pfad_fehler": [],
        "brief_fehler": [],
        "notbremse": [],
    }
    werkbank = Werkbank(NS, buch, umgebung)

    offen = pfade_erreichbar(NS)
    geschlossen = [p for p in NS["PFAD_REIHENFOLGE"] if p not in offen]
    umgebung["geschlossen"] = geschlossen

    ## Die Textluecken der geschlossenen Pfade werden gemessen, aber in ein
    ## eigenes Buch. Sie zaehlen nicht mit: Wer den Pfad nicht betreten
    ## kann, liest dort auch keinen Ersatztext.
    schuldbuch = Rueckfallbuch()
    if geschlossen:
        ## Fuer die Dauer der Durchsicht zeigt der Zeiger auf das
        ## Schuldbuch. Ohne diesen Wechsel schrieben die Wrapper weiter
        ## das Hauptbuch fort, dessen "an" hier noch False ist - und das
        ## Schuldbuch blieb leer, ohne dass es jemandem auffiel.
        vorheriges_buch = AKTIVES_RUECKFALLBUCH["buch"]
        AKTIVES_RUECKFALLBUCH["buch"] = schuldbuch
        schuldbuch.an = True
        try:
            textdurchsicht(NS, schuldbuch, geschlossen)
        finally:
            schuldbuch.an = False
            schuldbuch.marke = None
            AKTIVES_RUECKFALLBUCH["buch"] = vorheriges_buch
    umgebung["schuldbuch"] = schuldbuch

    ## Erst jetzt wird das Protokoll IM SPIEL geleert. Es soll genau
    ## denselben Zeitraum messen wie die Beobachtung dieser Werkbank - die
    ## Durchsicht der geschlossenen Pfade eben gehoert nicht dazu. Nur so
    ## lassen sich die beiden Zahlen gegeneinander halten.
    protokoll_leeren(NS)

    ergebnisse = {}
    buch.an = True
    try:
        textdurchsicht(NS, buch, offen)
        for strategie in STRATEGIEN:
            werkbank.strategie = strategie
            for pfad in offen:
                for modus in ["kurz", "lang"]:
                    spuren = []
                    for _ in range(durchgaenge):
                        spuren.append(werkbank.durchgang(pfad, modus))
                    ergebnisse[(pfad, modus, strategie)] = spuren
    finally:
        werkbank.strategie = "zufall"
        buch.an = False
        buch.marke = None

    return werkbank, umgebung, ergebnisse


def spuren_holen(ergebnisse, pfad, modus, strategie=None):
    """Die Spuren einer Lage. Ohne Strategie: alle zusammen."""
    if strategie is not None:
        return ergebnisse.get((pfad, modus, strategie), [])
    zusammen = []
    for name in STRATEGIEN:
        zusammen.extend(ergebnisse.get((pfad, modus, name), []))
    return zusammen


def probe_pfadprobe(NS, B, werkbank, umgebung, ergebnisse, buch, durchgaenge):
    beanstandungen = 0
    geprueft = 0

    B.titel("PROBE 2  PFADPROBE")
    B("Je Startpfad und Verlauf %d Durchgaenge ueber alle sechs Kapitel, also"
      % durchgaenge)
    B("%d Durchgaenge je Startpfad. Gezogen wird mit den Funktionen des"
      % (2 * durchgaenge))
    B("Projekts, gewaehlt wird zufaellig, gespielt wird die Kette aus")
    B("Einstieg, Hauptschleife, Einlage, Post und Kapitelwechsel.")
    if umgebung.get("geschlossen"):
        B("")
        B("Nicht gespielt, weil der Einstieg dorthin nicht mehr fuehrt: %s."
          % ", ".join(NS["PFAD_MARKE"].get(p, p) for p in umgebung["geschlossen"]))
    B("")
    B("%-16s %-16s %10s %10s %10s" % (
        "Pfad", "Verlauf", "Ereignisse", "Einlagen", "Briefe"))

    inhalte = 0
    gezogen = {"ereignis": collections.Counter(),
               "einlage": collections.Counter(),
               "brief": collections.Counter()}
    for pfad in NS["PFAD_REIHENFOLGE"]:
        for modus in ["kurz", "lang"]:
            ## Beide Strategien zusammen: Diese Probe fragt nach Richtigkeit,
            ## nicht nach Ueberleben. Je mehr Durchgaenge, desto besser.
            spuren = spuren_holen(ergebnisse, pfad, modus)
            if not spuren:
                continue
            ereignisse = sum(len(s.ereignisse) for s in spuren)
            einlagen = sum(len(s.einlagen) for s in spuren)
            briefe = sum(len(s.briefe) for s in spuren)
            inhalte += ereignisse + einlagen + briefe
            for spur in spuren:
                for _jahr, kennung, _wahl in spur.ereignisse:
                    gezogen["ereignis"][kennung] += 1
                for _jahr, kennung in spur.einlagen:
                    gezogen["einlage"][kennung] += 1
                for _jahr, kennung, _art in spur.briefe:
                    gezogen["brief"][kennung] += 1
            B("%-16s %-16s %10d %10d %10d" % (
                NS["PFAD_MARKE"].get(pfad, pfad),
                NS["MODUS_BEZEICHNUNG"].get(modus, modus),
                ereignisse, einlagen, briefe))
            B("%-16s %-16s %10.2f %10.2f %10.2f   je Durchgang" % (
                "", "", ereignisse / float(len(spuren)),
                einlagen / float(len(spuren)), briefe / float(len(spuren))))
    geprueft = inhalte

    ## a0) Der Rhythmus ########################################################
    ##
    ## PAKET 8, SCHRITT 2.5, Auftragspunkt 10. Die Zahl "Einlagen je
    ## Durchgang" darueber sagt nicht, ob sie sich verteilen: 2,8 Einlagen
    ## koennen sechs Kapitel gleichmaessig fuellen oder sich in zweien
    ## draengen. Gezaehlt wird deshalb je KAPITEL.
    ##
    ## Gezaehlt werden nur abgeschlossene Kapitel ('soll' und 'leer'). Das
    ## Kapitel, in dem ein Durchgang abbricht, ist keine Aussage ueber den
    ## Rhythmus - es hat schlicht frueher aufgehoert.
    B.unterteil("a0) Kapitel ohne Einlage und ohne Brief (Schritt 2.5)")
    B("Die Nachziehregel: Ist ein Kapitel ohne Einlage oder ohne Brief zu")
    B("Ende gegangen, wird im naechsten ohne Wurf gezogen. Gemessen wird,")
    B("was davon ankommt.")
    B("")
    ## DREI SPALTEN, WEIL DER AUFTRAG ZWEI VERSCHIEDENE DINGE VERLANGT.
    ## Punkt 8 fordert "mindestens eine Einlage UND mindestens ein Brief"
    ## je Kapitel; die Abnahme desselben Schrittes fordert "kein Kapitel
    ## ohne Einlage UND ohne Brief" - also keines, das WEDER das eine noch
    ## das andere hat. Das ist die schwaechere und die sinnvollere Zahl.
    ## Gemessen werden beide, damit niemand die eine fuer die andere haelt.
    B("%-15s %-9s %7s %9s %6s %9s %6s %9s %6s" % (
        "Pfad", "Verlauf", "Kapitel", "o.Einlage", "in %",
        "o. Brief", "in %", "o. beides", "in %"))

    rhythmus_kapitel = 0
    for pfad in NS["PFAD_REIHENFOLGE"]:
        for modus in ["kurz", "lang"]:
            spuren = spuren_holen(ergebnisse, pfad, modus)
            if not spuren:
                continue
            kapitel = 0
            ohne_einlage = 0
            ohne_brief = 0
            ohne_beides = 0
            for spur in spuren:
                jahre_einlage = set(j for j, _k in spur.einlagen)
                jahre_brief = set(j for j, _k, _a in spur.briefe)
                for jahr, ende_grund in spur.kapitelende:
                    if ende_grund not in ("soll", "leer"):
                        continue
                    kapitel += 1
                    fehlt_einlage = jahr not in jahre_einlage
                    fehlt_brief = jahr not in jahre_brief
                    if fehlt_einlage:
                        ohne_einlage += 1
                    if fehlt_brief:
                        ohne_brief += 1
                    if fehlt_einlage and fehlt_brief:
                        ohne_beides += 1
            rhythmus_kapitel += kapitel
            if not kapitel:
                B("%-15s %-9s %7s   NICHTS GEMESSEN" % (
                    NS["PFAD_MARKE"].get(pfad, pfad),
                    NS["MODUS_BEZEICHNUNG"].get(modus, modus), "0"))
                continue
            B("%-15s %-9s %7d %9d %5.1f%% %9d %5.1f%% %9d %5.1f%%" % (
                NS["PFAD_MARKE"].get(pfad, pfad),
                NS["MODUS_BEZEICHNUNG"].get(modus, modus),
                kapitel,
                ohne_einlage, 100.0 * ohne_einlage / kapitel,
                ohne_brief, 100.0 * ohne_brief / kapitel,
                ohne_beides, 100.0 * ohne_beides / kapitel))

    if not rhythmus_kapitel:
        B("")
        B("   NICHTS GEMESSEN - kein einziges abgeschlossenes Kapitel.")
    B("")
    B("Gezaehlt: %d abgeschlossene Kapitel." % rhythmus_kapitel)
    B("Die Abnahme des Schrittes haengt an der letzten Spalte.")

    ## a) Pfadzugehoerigkeit ##################################################
    B.unterteil("a) Inhalt auf einem Pfad, den seine pfad-Liste nicht nennt")
    if not umgebung["pfad_fehler"]:
        B("   keine Beanstandung")
    else:
        gezaehlt = collections.Counter(
            (a, b, c, d) for a, b, c, d, _e in umgebung["pfad_fehler"])
        for (art, kennung, pfad, erlaubt), anzahl in gezaehlt.most_common():
            beanstandungen += 1
            B("   FEHLER  %-8s %-34s gespielt auf %-8s erlaubt: %s  (%dx)"
              % (art, kennung, pfad, erlaubt, anzahl))

    ## b) Briefwelt ###########################################################
    B.unterteil("b) Brief, dessen welt nicht briefwelt() entspricht")
    if not umgebung["brief_fehler"]:
        B("   keine Beanstandung")
    else:
        gezaehlt = collections.Counter(
            (a, b, c, d) for a, b, c, d, _e in umgebung["brief_fehler"])
        for (kennung, welt, briefwelt, pfad), anzahl in gezaehlt.most_common():
            beanstandungen += 1
            B("   FEHLER  %-34s welt=%-8s briefwelt=%-8s Pfad %s  (%dx)"
              % (kennung, welt, briefwelt, pfad, anzahl))

    ## c) Rueckfallebene von variante() und welttext() ########################
    B.unterteil("c) variante() und welttext() ohne genauen Pfadschluessel")
    B("   zweig 'ersatz'   : welttext() hat die Fassung der eigenen Welt")
    B("                      genommen statt der des genauen Pfades")
    B("   zweig 'standard' : eine Fassung fuer diesen Pfad fehlt")
    B("   zweig 'leer'     : es gab ueberhaupt keine passende Fassung")
    B("")
    if not buch.eintraege:
        B("   keine Beanstandung")
    else:
        B("   %-9s %-8s %-8s %-10s %7s  %s" % (
            "Funktion", "Zweig", "Pfad", "Ersatz", "Anzahl", "Stelle"))
        for schluessel_tupel, anzahl in buch.eintraege.most_common(80):
            funktion, zweig, ersatz, pfad, ort = schluessel_tupel
            beanstandungen += 1
            B("   %-9s %-8s %-8s %-10s %7d  %s" % (
                funktion, zweig, pfad, ersatz, anzahl, ort))
        if len(buch.eintraege) > 80:
            B("   ... und %d weitere Stellen" % (len(buch.eintraege) - 80))
        B("")
        B("   Griffe in die Rueckfallebene insgesamt: %d, verschiedene Stellen: %d"
          % (buch.gesamt, len(buch.eintraege)))

    ## Gegenprobe mit dem Protokoll, das das Spiel selbst fuehrt ##############
    ##
    ## Die Werkbank umhuellt variante() und welttext() von aussen, das Spiel
    ## schreibt von innen mit. Beide zaehlen denselben Vorgang. Laufen die
    ## Zahlen auseinander, misst eine von beiden falsch - und das waere ein
    ## Befund, der schwerer wiegt als jede einzelne Fundstelle.
    B.unterteil("Gegenprobe: das Protokoll im Spiel (variantenersatz_protokoll)")
    im_spiel = NS.get("variantenersatz_gesamt")
    stellen = NS.get("variantenersatz_protokoll")
    if not isinstance(im_spiel, int) or not isinstance(stellen, list):
        beanstandungen += 1
        B("   FEHLER  Das Spiel fuehrt kein Protokoll. Erwartet werden")
        B("           variantenersatz_gesamt und variantenersatz_protokoll")
        B("           aus dialoge.rpy.")
    else:
        B("   Werkbank von aussen: %d Griffe" % buch.gesamt)
        B("   Spiel von innen:     %d Griffe, %d Stellen eingetragen"
          % (im_spiel, len(stellen)))
        if im_spiel != buch.gesamt:
            beanstandungen += 1
            B("   FEHLER  Die beiden Zaehlungen gehen um %d auseinander."
              % abs(im_spiel - buch.gesamt))
        else:
            B("   Beide Zaehlungen stimmen ueberein.")

    ## Schuld der geschlossenen Pfade #########################################
    schuldbuch = umgebung.get("schuldbuch")
    if schuldbuch is not None and schuldbuch.eintraege:
        B.unterteil("Textluecken auf geschlossenen Pfaden (zaehlen heute nicht)")
        B("Gemessen wie oben, aber getrennt: Diese Fassungen fehlen, und")
        B("niemand bekommt sie zu sehen, solange der Pfad zu ist. Das Paket,")
        B("das ihn oeffnet, schreibt sie nach.")
        B("")
        for schluessel_tupel, anzahl in schuldbuch.eintraege.most_common(20):
            funktion, zweig, ersatz, pfad, ort = schluessel_tupel
            B("   %-9s %-8s %-8s %-10s %7d  %s" % (
                funktion, zweig, pfad, ersatz, anzahl, ort))
        if len(schuldbuch.eintraege) > 20:
            B("   ... und %d weitere Stellen" % (len(schuldbuch.eintraege) - 20))
        B("")
        B("   Offene Stellen: %d, Griffe: %d"
          % (len(schuldbuch.eintraege), schuldbuch.gesamt))

    ## Post aus einer fremden Welt ############################################
    postwelt = NS.get("postwelt_protokoll")
    if isinstance(postwelt, list):
        B.unterteil("Post, die nicht zur eigenen Welt passte (postwelt_protokoll)")
        if not postwelt:
            B("   keine Beanstandung")
        else:
            gezaehlt = collections.Counter(
                (e["ort"], e["kennung"], e["gemeint"], e["jetzt"]) for e in postwelt)
            for (ort, kennung, gemeint, jetzt), anzahl in gezaehlt.most_common(30):
                beanstandungen += 1
                B("   FEHLER  %-22s %-24s gemeint fuer %-8s zugestellt in %-8s (%dx)"
                  % (ort, kennung, gemeint, jetzt, anzahl))

    ## Notbremse und Einstieg #################################################
    if umgebung["notbremse"]:
        beanstandungen += len(umgebung["notbremse"])
        B("")
        B("   FEHLER  %d Durchgaenge liefen ueber %d Schritte und wurden abgebrochen."
          % (len(umgebung["notbremse"]), NOTBREMSE))
    if werkbank.verfehlter_einstieg:
        B("")
        B("   Hinweis: %d Einstiege erreichten den gewuenschten Pfad nicht und"
          % werkbank.verfehlter_einstieg)
        B("            wurden auf dem tatsaechlichen Pfad weitergespielt.")
    if werkbank.erzwungene_musterung:
        B("   Hinweis: %d Musterungen mussten gesetzt statt gewuerfelt werden."
          % werkbank.erzwungene_musterung)

    ## Der persoenliche Faden #################################################
    ##
    ## Seit Paket 3, Schritt 2: In jedem Kapitel soll mindestens eine
    ## Nebenfigur vorkommen - als Brief, als Schicksalsmeldung oder in einer
    ## Szene. Gemessen wird ueber die Briefe und Nachrichten, die im
    ## Durchgang wirklich zugestellt wurden.
    B.unterteil("Der persoenliche Faden: Kapitel ohne jede Nebenfigur")
    B("Gezaehlt wird je Jahr und Pfad, in wie vielen Durchgaengen ueberhaupt")
    B("eine Nebenfigur vorkam. Ein Kapitel, das ein Durchgang erreicht hat,")
    B("aber ohne Figur bleibt, ist ein Kapitel ohne Faden.")
    B("")
    B("Ein Jahr ohne jeden Ereignisbestand kann auch keine Post tragen: Post")
    B("wird nur nach einem Ereignis zugestellt. Solche Zeilen zaehlen hier")
    B("nicht mit, sie stehen schon in Probe 1 und Probe 3.")
    B("")
    B("%-6s %-16s %10s %10s %10s   %s" % (
        "Jahr", "Pfad", "erreicht", "mit Figur", "Anteil %", "Befund"))

    for jahr in NS["KAPITEL_JAHRE"]:
        for pfad in NS["PFAD_REIHENFOLGE"]:
            spuren = []
            for name in ["kurz", "lang"]:
                spuren.extend(spuren_holen(ergebnisse, pfad, name))
            if not spuren:
                continue
            erreicht = 0
            mit = 0
            for spur in spuren:
                jahre_im_lauf = set(j for j, _g in spur.kapitelende)
                if jahr not in jahre_im_lauf:
                    continue
                erreicht += 1
                if any(j == jahr for j, _k, _a in spur.briefe):
                    mit += 1
            if not erreicht:
                continue
            geprueft += erreicht

            ## Seit Paket 5, Schritt 3, Teil D.15c fragt auch diese Stelle
            ## das Projekt. "lang" nimmt den vollen Bestand; im kurzen
            ## Verlauf faellt nur weg, was kein kern traegt.
            frei, bedingt = NS["bestand_liste"](jahr, pfad, "lang")
            ziehbar = frei + bedingt
            anteil = prozent(mit, erreicht)
            if not ziehbar:
                befund = "kein Bestand (Probe 1)"
            elif mit == 0:
                beanstandungen += 1
                befund = ">> FEHLER << kein Kapitel mit Nebenfigur"
            elif anteil < 50.0:
                befund = "duenn"
            else:
                befund = "in Ordnung"
            B("%-6d %-16s %10d %10d %10.1f   %s" % (
                jahr, NS["PFAD_MARKE"].get(pfad, pfad), erreicht, mit, anteil, befund))

    ## Ketten, die offen geblieben sind #######################################
    B.unterteil("Ketten: Vormerkungen, die nicht mehr eingeloest werden koennen")
    B("Seit Paket 3, Schritt 2 prueft kette_faellig() auch das Jahr. Ein")
    B("vorgemerktes Glied, dessen Jahre alle vorbei sind, bleibt liegen.")
    B("")
    offen_gesamt = sum(s.ketten_offen for s in
                       [x for liste in ergebnisse.values() for x in liste])
    durchgaenge_gesamt = sum(len(liste) for liste in ergebnisse.values())
    if durchgaenge_gesamt:
        B("   Offene Vormerkungen am Ende: %d in %d Durchgaengen (%.3f je Durchgang)"
          % (offen_gesamt, durchgaenge_gesamt,
             offen_gesamt / float(durchgaenge_gesamt)))
        if offen_gesamt:
            beanstandungen += 1
            B("   >> FEHLER << Eine Kette, die nie beantwortet wird, ist eine")
            B("                Frage ohne Antwort. Die Inhaltspakete geben dem")
            B("                zweiten Glied die Jahre, in denen es fallen darf.")
        else:
            B("   keine Beanstandung")

        ## Seit Paket 4, Vorweg D: aufgeschluesselt nach Kette. Eine
        ## Gesamtzahl sagt nicht, an welchem zweiten Glied gearbeitet
        ## werden muss.
        B("")
        B("   Aufgeschluesselt nach dem vorgemerkten Glied:")
        je_kette = collections.Counter()
        for liste in ergebnisse.values():
            for spur in liste:
                je_kette.update(getattr(spur, "ketten_offen_liste", []))
        if je_kette:
            for kennung, anzahl in je_kette.most_common():
                vorlage = NS["EREIGNIS_INDEX"].get(kennung)
                jahre = ",".join(str(j) for j in vorlage.jahre) if vorlage else "fehlt"
                B("      %-38s %6d offen   Jahre %s" % (kennung, anzahl, jahre))
        else:
            B("      keine")

    ## Ketten, deren zweites Glied kein spaeteres Jahr abdeckt ################
    ##
    ## REGEL SEIT PAKET 4, VORWEG D. Wer die erste Karte im letzten
    ## gemeinsamen Jahr zieht, kann die Antwort nie bekommen. Das ist
    ## kein Zufall des Wurfs, sondern in der Planung angelegt.
    B.unterteil("Ketten: zweites Glied ohne ein Jahr nach dem ersten")
    B("Das zweite Glied muss mindestens ein Jahr abdecken, das nach dem")
    B("spaetesten Jahr des ersten Glieds liegt. Glieder, die es noch nicht")
    B("gibt, stehen als Fehlstelle im Plan und werden hier uebergangen.")
    B("")
    if callable(NS.get("ketten_ohne_spaeteres_jahr")):
        wackelig = NS["ketten_ohne_spaeteres_jahr"]()
        geprueft += len(NS.get("KETTEN_PLAN", []))
        if not wackelig:
            B("   keine Beanstandung")
        for eins, zwei, spaetestes, jahre in wackelig:
            beanstandungen += 1
            B("   >> FEHLER << %s -> %s" % (eins, zwei))
            B("                erstes Glied bis %d, zweites Glied nur %s"
              % (spaetestes, ",".join(str(j) for j in jahre)))

    ## Dasselbe fuer die Ketten, die eine EINLAGE vormerkt #####################
    ##
    ## SEIT PAKET 5, SCHRITT 3, TEIL D.13. Die Pruefung darueber liest den
    ## KETTEN_PLAN, und der kennt nur Ketten aus Optionen. Eine Einlage
    ## kann ueber auswertung["ketten"] genauso vormerken - hamsterfahrt tut
    ## es mit heimat_verfahren -, und diese Vormerkungen standen in keiner
    ## Pruefung. Der Fehler von Paket 4 (dem zweiten Glied fehlte 1919)
    ## waere hier sichtbar gewesen, statt erst beim Nachrechnen von Hand.
    ##
    ## Die Regel ist schaerfer als bei einer Option: einlage_anwenden()
    ## merkt mit ab_jahr = aktuelles_jahr vor, also OHNE Abstand. Bleibt im
    ## letzten Kapitel des spaetesten Einlagenjahres keine Ziehung mehr
    ## uebrig, rutscht die Vormerkung ins Folgejahr. Das zweite Glied
    ## braucht deshalb ein Jahr NACH dem spaetesten Jahr der Einlage.
    B.unterteil("Ketten aus Einlagen: Vormerkungen ohne ein Jahr danach")
    B("Eine Einlage merkt ohne Abstand vor. Ihr zweites Glied muss das")
    B("spaeteste Jahr der Einlage abdecken UND ein Jahr danach - sonst")
    B("verfaellt die Vormerkung, wenn die Einlage im letzten Kapitel faellt.")
    B("")
    if callable(NS.get("einlagen_ketten_sammeln")):
        einlagenketten = NS["einlagen_ketten_sammeln"]()
        geprueft += len(einlagenketten)
        B("%-22s %-30s %10s   %s" % (
            "Einlage", "merkt vor", "bis Jahr", "Jahre des zweiten Glieds"))
        if not einlagenketten:
            B("   keine Einlage merkt eine Kette vor")
        for einlage, kette, spaetestes, _pfade in einlagenketten:
            vorlage = NS["EREIGNIS_INDEX"].get(kette)
            if vorlage is None:
                beanstandungen += 1
                B("%-22s %-30s %10s   >> FEHLER << Glied gibt es nicht"
                  % (einlage, kette, spaetestes if spaetestes else "-"))
                continue
            jahre = sorted(vorlage.jahre)
            danach = [j for j in jahre if spaetestes is not None and j > spaetestes]
            befund = "in Ordnung" if danach else \
                ">> FEHLER << kein Jahr nach %s" % spaetestes
            if not danach:
                beanstandungen += 1
            B("%-22s %-30s %10s   %s   %s" % (
                einlage, kette, spaetestes if spaetestes else "-",
                ",".join(str(j) for j in jahre), befund))
    else:
        B("   nicht geprueft: einlagen_ketten_sammeln fehlt")

    ## Die vier Faecher des Lebenslaufs #######################################
    ##
    ## SEIT PAKET 5, SCHRITT 3, TEIL E.4 (Entscheidung 10). Der Lebenslauf
    ## zieht seit diesem Schritt je Fach den obersten Eintrag statt der
    ## hoechstrangigen Merkmale ueberhaupt. Der Grund war messbar: Die
    ## Herkunft liegt bei Rang 32 bis 34 und wurde von Erwerbslage und
    ## Stellung (46 bis 60) fast immer verdraengt. Hier steht die Zahl, an
    ## der sich das nachpruefen laesst.
    B.unterteil("Der Lebenslauf: welches Fach erscheint wie oft?")
    if callable(NS.get("lebenslauf_fach")) and NS.get("LEBENSLAUF_FAECHER"):
        B("Zuordnung der Merkmale zu den vier Faechern. Die Gruppe stammt")
        B("aus MERKMAL_REGISTER; erfunden wird hier nichts.")
        B("")
        B("%-26s %-28s %-12s %6s   %s" % (
            "Fach", "Merkmal", "Gruppe", "Rang", "Nachklang"))
        ohne_fach = []
        for name in NS.get("MERKMAL_REIHENFOLGE_LEBENSWEG", []):
            eintrag = NS["MERKMAL_REGISTER"].get(name) or {}
            stelle = NS["lebenslauf_fach"](name)
            if stelle is None:
                ohne_fach.append(name)
                fach = ">> KEIN FACH <<"
            else:
                fach = NS["LEBENSLAUF_FAECHER"][stelle][0]
            B("%-26s %-28s %-12s %6s   %s" % (
                fach, name, eintrag.get("gruppe", "-"),
                eintrag.get("rang", "-"),
                "ja" if eintrag.get("nachklang") else "nein"))
        if ohne_fach:
            beanstandungen += len(ohne_fach)
            B("")
            B(">> FEHLER << %d Merkmale gehoeren in kein Fach: %s"
              % (len(ohne_fach), ", ".join(ohne_fach)))

        alle = [s for liste in ergebnisse.values() for s in liste]
        erreicht = [s for s in alle if s.ende == "ende_ueberlebt"]
        B("")
        B("In wie viel Prozent der Durchgaenge traegt ein Fach einen Eintrag?")
        B("'alle' zaehlt jeden Durchgang, '1919' nur die, die den Epilog")
        B("erreichen - beide, weil der Lebenslauf nach jedem Ausgang kommt.")
        B("")
        B("%-26s %12s %12s   %s" % ("Fach", "alle %", "1919 %", "Befund"))
        for stelle in range(len(NS["LEBENSLAUF_FAECHER"])):
            name = NS["LEBENSLAUF_FAECHER"][stelle][0]
            geprueft += len(alle)
            anteil = prozent(len([s for s in alle if name in s.faecher]), len(alle))
            anteil_1919 = prozent(
                len([s for s in erreicht if name in s.faecher]), len(erreicht))
            befund = ""
            if stelle == 0 and anteil < 100.0:
                beanstandungen += 1
                befund = ">> FEHLER << das Fach der Herkunft muss immer stehen"
            elif anteil == 0.0:
                befund = "leer - kein Merkmal dieses Fachs traegt einen Nachklang"
            B("%-26s %12.1f %12.1f   %s" % (name, anteil, anteil_1919, befund))
    else:
        B("   nicht geprueft: lebenslauf_fach/LEBENSLAUF_FAECHER fehlt")

    ## Toter Bestand ##########################################################
    ##
    ## Kein Fehler, aber die wichtigste Nebenauskunft dieses Durchlaufs: Was
    ## in so vielen Durchgaengen nie erschienen ist, erreicht auch im
    ## Unterricht niemanden. Ereignisse mit nur_kette bleiben aussen vor, sie
    ## werden absichtlich nur gerufen.
    B.unterteil("Nie gezogen (kein Fehler, aber toter Bestand)")
    stumm = []
    for vorlage in ziehbare_ereignisse(NS):
        if not gezogen["ereignis"][vorlage.kennung]:
            stumm.append(("Ereignis", vorlage.kennung,
                          "/".join(vorlage.pfad),
                          ", ".join(str(j) for j in vorlage.jahre)))
    for vorlage in NS["EINLAGEN"]:
        if not gezogen["einlage"][vorlage.kennung]:
            stumm.append(("Einlage", vorlage.kennung, "/".join(vorlage.pfad),
                          ", ".join(str(j) for j in vorlage.jahre)))
    for vorlage in NS["BRIEFE"]:
        if not gezogen["brief"][vorlage.kennung]:
            stumm.append(("Brief", vorlage.kennung, vorlage.welt,
                          ", ".join(str(j) for j in vorlage.jahre)))
    if not stumm:
        B("   keiner")
    for art, kennung, pfad, jahre in stumm:
        B("   %-9s %-40s %-22s %s" % (art, kennung, pfad, jahre))
    B("")
    B("Verschiedene Ereignisse gezogen: %d von %d. Einlagen: %d von %d. Briefe: %d von %d."
      % (len(gezogen["ereignis"]), len(ziehbare_ereignisse(NS)),
         len(gezogen["einlage"]), len(NS["EINLAGEN"]),
         len([k for k in gezogen["brief"] if not str(k).startswith("nachricht_")]),
         len(NS["BRIEFE"])))

    return beanstandungen, geprueft


def probe_sackgasse(NS, B, ergebnisse):
    beanstandungen = 0
    geprueft = 0

    B.titel("PROBE 3  SACKGASSENPROBE")
    B("Wie endet ein Kapitel? 'Soll' heisst: die vorgesehene Zahl Ziehungen")
    B("ist erreicht. 'Leer' heisst: ereignis_ziehen() lieferte None, der")
    B("Bestand war aufgebraucht. Jede Zeile mit Leer ueber null Prozent ist")
    B("eine Beanstandung, weil das Kapitel dort frueher endet als geplant.")

    for modus in ["kurz", "lang"]:
        B.unterteil("Kapitelabschluesse - " + NS["MODUS_BEZEICHNUNG"].get(modus, modus))
        B("%-6s %-16s %8s %8s %8s %8s   %s" % (
            "Jahr", "Pfad", "Faelle", "Soll %", "Leer %", "Ende %", "Befund"))
        for jahr in NS["KAPITEL_JAHRE"]:
            for pfad in NS["PFAD_REIHENFOLGE"]:
                ## Gemessen wird die zufaellige Wahl: Sie ist die Lage, in
                ## der der Bestand am schnellsten aufgebraucht ist.
                spuren = spuren_holen(ergebnisse, pfad, modus, "zufall")
                gruende = collections.Counter()
                for spur in spuren:
                    for kjahr, grund in spur.kapitelende:
                        if kjahr == jahr:
                            gruende[grund] += 1
                gesamt = sum(gruende.values())
                if not gesamt:
                    continue
                geprueft += gesamt
                leer = prozent(gruende["leer"], gesamt)
                if gruende["leer"]:
                    beanstandungen += 1
                    befund = ">> SACKGASSE <<"
                else:
                    befund = "in Ordnung"
                B("%-6d %-16s %8d %8.1f %8.1f %8.1f   %s" % (
                    jahr, NS["PFAD_MARKE"].get(pfad, pfad), gesamt,
                    prozent(gruende["soll"], gesamt), leer,
                    prozent(gruende["abbruch"] + gruende["sprung"], gesamt),
                    befund))

    ## Eine Zahl fuer das Ganze, damit sich der Fortschritt von Paket zu
    ## Paket vergleichen laesst.
    alle = collections.Counter()
    for schluessel, spuren in ergebnisse.items():
        if schluessel[2] != "zufall":
            continue
        for spur in spuren:
            for _jahr, grund in spur.kapitelende:
                alle[grund] += 1
    gesamt = sum(alle.values())
    B("")
    B("Ueber alle Lagen: %d Kapitelabschluesse, davon %.1f Prozent aus Mangel"
      % (gesamt, prozent(alle["leer"], gesamt)))
    B("(ereignis_ziehen() lieferte None), %.1f Prozent nach erreichtem Soll und"
      % prozent(alle["soll"], gesamt))
    B("%.1f Prozent durch einen Abbruch oder einen Sprung."
      % prozent(alle["abbruch"] + alle["sprung"], gesamt))

    return beanstandungen, geprueft


def probe_wertetafel(NS, B, ergebnisse):
    beanstandungen = 0
    geprueft = 0

    B.titel("PROBE 4  WERTETAFEL")
    B("Angegeben ist der Rohwert von 0 bis %d, nicht die Anzeige. Bei"
      % NS["WERT_MAXIMUM"])
    B("versorgung und rueckhalt ist ein hoher Wert gut, bei belastung und")
    B("aufmerksamkeit schlecht. Die Stufenspalten rechnen das um: Stufe 0 ist")
    B("immer die gute Lage, Stufe 4 immer die schlechte.")
    B("")
    B("Seit Paket 2, Schritt 3 wird jede Lage mit zwei Wahlstrategien")
    B("gespielt. 'zufall' wuerfelt die Option, 'klug' nimmt die, die den")
    B("derzeit schlechtesten Wert am wenigsten verschlechtert.")
    B("")
    B("SEIT PAKET 6, VORWEG A GILT JE VERLAUF EINE EIGENE GRENZE")
    B("(Entscheidung 11). Gemessen wird gegen diese Tafel:")
    B("")
    B("%-16s %18s %18s" % ("Verlauf", "zufaellige Wahl", "kluge Wahl"))
    for modus in ["kurz", "lang"]:
        ziel = ZIELE[modus]
        B("%-16s %10.0f bis %-4.0f %14.0f und mehr" % (
            NS["MODUS_BEZEICHNUNG"].get(modus, modus),
            ziel["zufall_unten"], ziel["zufall_oben"], ziel["klug_unten"]))
    B("")
    B("BEANSTANDET WIRD:")
    B("  a) zufaellige Wahl ausserhalb der Spanne dieses Verlaufs")
    B("  b) kluge Wahl unter der Grenze dieses Verlaufs")
    B("  c) eine Lage, die 1919 in KEINEM Durchgang erreicht - ein toter")
    B("     Pfad ist kein Messwert, sondern ein Befund fuer sich")
    B("  d) der reine Kalender erreicht allein schon eine Abbruchschwelle")

    ENDEN = ["ende_verhungert", "ende_zusammenbruch", "ende_verhaftet",
             "ende_gefallen", "ende_ueberlebt"]

    lagen = [(p, m) for p in NS["PFAD_REIHENFOLGE"] for m in ["kurz", "lang"]]

    ## Die Tafel, auf die es ankommt: sechs Lagen, zwei Strategien ############
    B.unterteil("Wer erreicht 1919?")
    B("%-16s %-16s %10s %10s %10s   %s" % (
        "Pfad", "Verlauf", "zufall %", "klug %", "Abstand", "Befund"))

    for pfad, modus in lagen:
        zufall = spuren_holen(ergebnisse, pfad, modus, "zufall")
        klug = spuren_holen(ergebnisse, pfad, modus, "klug")
        if not zufall:
            continue
        a_zufall = prozent(len([s for s in zufall if s.ende == "ende_ueberlebt"]),
                           len(zufall))
        a_klug = prozent(len([s for s in klug if s.ende == "ende_ueberlebt"]),
                         len(klug)) if klug else 0.0

        ziel = ZIELE[modus]
        maengel = []
        if a_zufall < ziel["zufall_unten"]:
            beanstandungen += 1
            maengel.append("zufall unter %d" % ziel["zufall_unten"])
        elif a_zufall > ziel["zufall_oben"]:
            beanstandungen += 1
            maengel.append("zufall ueber %d" % ziel["zufall_oben"])
        if a_klug < ziel["klug_unten"]:
            beanstandungen += 1
            maengel.append("klug unter %d" % ziel["klug_unten"])
        ## Der Satz aus Entscheidung 11, der nicht verhandelbar ist.
        if a_zufall <= ZIEL_MINDESTENS and a_klug <= ZIEL_MINDESTENS:
            beanstandungen += 1
            maengel.append("TOTER PFAD - kein Durchgang erreicht 1919")

        B("%-16s %-16s %10.1f %10.1f %10.1f   %s" % (
            NS["PFAD_MARKE"].get(pfad, pfad),
            NS["MODUS_BEZEICHNUNG"].get(modus, modus),
            a_zufall, a_klug, a_klug - a_zufall,
            (">> FEHLER << " + ", ".join(maengel)) if maengel else "in Ordnung"))

    ## Inhalte und Quellen je Durchgang #######################################
    ##
    ## SEIT PAKET 5, SCHRITT 3, TEIL A.2. Die Tafel oben sagt, WO ein
    ## Durchgang endet. Diese beiden Tafeln sagen, WOVON. Ohne sie eicht man
    ## blind: Einlagen und Post machen zusammen rund die Haelfte der Inhalte
    ## eines kurzen Durchgangs aus und tauchten in keiner Wertemessung
    ## gesondert auf. Wer dann an KAPITEL_WIRKUNG dreht, weil die Werte zu
    ## schnell fallen, dreht moeglicherweise an der falschen Schraube.

    QUELLEN = [
        ("ereignis", "Ereignisse"),
        ("einlage", "Einlagen"),
        ("post", "Post"),
        ("kalender", "Kalender"),
        ("schicksal", "Schicksale"),
    ]

    B.unterteil("Inhalte je Durchgang")
    B("Gemittelt ueber alle Durchgaenge der Lage, abgebrochene eingeschlossen.")
    B("Ein abgebrochener Durchgang hat weniger Inhalte gesehen - genau das")
    B("macht den Mittelwert zur ehrlichen Zahl fuer die Spielzeit.")
    B("")
    B("%-16s %-16s %-8s %11s %10s %8s %10s" % (
        "Pfad", "Verlauf", "Wahl", "Ereignisse", "Einlagen", "Post", "zusammen"))
    for pfad, modus in lagen:
        for strategie in STRATEGIEN:
            spuren = spuren_holen(ergebnisse, pfad, modus, strategie)
            if not spuren:
                continue
            anzahl = float(len(spuren))
            zahl_e = sum(len(s.ereignisse) for s in spuren) / anzahl
            zahl_i = sum(len(s.einlagen) for s in spuren) / anzahl
            zahl_p = sum(len(s.briefe) for s in spuren) / anzahl
            B("%-16s %-16s %-8s %11.2f %10.2f %8.2f %10.2f" % (
                NS["PFAD_MARKE"].get(pfad, pfad),
                NS["MODUS_BEZEICHNUNG"].get(modus, modus), strategie,
                zahl_e, zahl_i, zahl_p, zahl_e + zahl_i + zahl_p))

    B.unterteil("Woher die Verschiebung kommt")
    B("Je Durchgang gemittelt: wie viele Punkte diese Quelle an den vier")
    B("Werten wirklich bewegt hat. Gemessen wird der Stand davor gegen den")
    B("Stand danach, nicht die angekuendigte Aenderung - nur so zaehlt die")
    B("Kappung an 0 und %d richtig mit." % NS["WERT_MAXIMUM"])
    B("Vorzeichen wie im Spiel: Bei versorgung und rueckhalt ist plus gut,")
    B("bei belastung und aufmerksamkeit ist plus schlecht.")
    B("")
    B("'Beginn' ist der Stand nach dem Einstieg und vor der ersten Ziehung.")
    B("Die Zeile 'Summe' muss der Zeile 'gemessen' gleichen. Tut sie es")
    B("nicht, hat diese Werkbank eine Quelle nicht erfasst - das ist ein")
    B("Werkzeugfehler und wird beanstandet, nicht das Spiel.")

    ungebucht = 0
    for pfad, modus in lagen:
        for strategie in STRATEGIEN:
            spuren = spuren_holen(ergebnisse, pfad, modus, strategie)
            if not spuren:
                continue
            anzahl = float(len(spuren))

            ## Die Gegenprobe laeuft je Durchgang, nicht erst auf dem
            ## Mittelwert: Zwei Fehler mit verschiedenem Vorzeichen heben
            ## sich im Mittel auf und blieben sonst unsichtbar.
            for spur in spuren:
                if spur.werte_beginn is None or spur.werte is None:
                    ungebucht += 1
                    continue
                for schluessel in NS["WERTE_REIHENFOLGE"]:
                    gebucht = sum(spur.verschiebung.get(q, {}).get(schluessel, 0)
                                  for q, _ in QUELLEN)
                    gemessen = spur.werte[schluessel] - spur.werte_beginn[schluessel]
                    if gebucht != gemessen:
                        ungebucht += 1
                        break

            B.unterteil("%s - %s - Wahl '%s'" % (
                NS["PFAD_MARKE"].get(pfad, pfad),
                NS["MODUS_BEZEICHNUNG"].get(modus, modus), strategie))
            B("%-14s %10s %11s %11s %15s %11s" % (
                "Quelle", "Vorgaenge", "versorgung", "belastung",
                "aufmerksamkeit", "rueckhalt"))

            summe = dict((s, 0.0) for s in NS["WERTE_REIHENFOLGE"])
            for quelle, name in QUELLEN:
                mal = sum(s.vorgaenge.get(quelle, 0) for s in spuren) / anzahl
                zeile = []
                for schluessel in NS["WERTE_REIHENFOLGE"]:
                    mittel = sum(s.verschiebung.get(quelle, {}).get(schluessel, 0)
                                 for s in spuren) / anzahl
                    summe[schluessel] += mittel
                    zeile.append(mittel)
                B("%-14s %10.2f %11.2f %11.2f %15.2f %11.2f" % (
                    name, mal, zeile[0], zeile[1], zeile[2], zeile[3]))

            B("%-14s %10s %11.2f %11.2f %15.2f %11.2f" % (
                "Summe", "", summe["versorgung"], summe["belastung"],
                summe["aufmerksamkeit"], summe["rueckhalt"]))

            gemessen = {}
            beginn = {}
            for schluessel in NS["WERTE_REIHENFOLGE"]:
                beginn[schluessel] = sum(
                    s.werte_beginn[schluessel] for s in spuren
                    if s.werte_beginn) / anzahl
                gemessen[schluessel] = sum(
                    s.werte[schluessel] - s.werte_beginn[schluessel]
                    for s in spuren if s.werte and s.werte_beginn) / anzahl
            B("%-14s %10s %11.2f %11.2f %15.2f %11.2f" % (
                "gemessen", "", gemessen["versorgung"], gemessen["belastung"],
                gemessen["aufmerksamkeit"], gemessen["rueckhalt"]))
            B("%-14s %10s %11.2f %11.2f %15.2f %11.2f" % (
                "Beginn", "", beginn["versorgung"], beginn["belastung"],
                beginn["aufmerksamkeit"], beginn["rueckhalt"]))

    if ungebucht:
        beanstandungen += 1
        B("")
        B(">> FEHLER << In %d Durchgaengen stimmt die Summe der Quellen nicht"
          % ungebucht)
        B("             mit der gemessenen Verschiebung ueberein. Es gibt also")
        B("             eine Stelle, die Werte aendert und hier nicht gebucht")
        B("             wird. Die Aufteilung ist bis dahin nicht belastbar.")
    else:
        B("")
        B("Gegenprobe: In allen Durchgaengen ergibt die Summe der fuenf Quellen")
        B("genau die gemessene Verschiebung. Es aendert nichts anderes die Werte.")

    ## Die Einzelheiten je Lage ###############################################
    for pfad, modus in lagen:
        for strategie in STRATEGIEN:
            spuren = spuren_holen(ergebnisse, pfad, modus, strategie)
            if not spuren:
                continue
            geprueft += len(spuren)
            B.unterteil("%s - %s - Wahl '%s'   (%d Durchgaenge)" % (
                NS["PFAD_MARKE"].get(pfad, pfad),
                NS["MODUS_BEZEICHNUNG"].get(modus, modus), strategie, len(spuren)))

            B("%-14s %-16s %8s %8s %8s   %s" % (
                "Wert", "Anzeige", "kleinst", "Mittel", "groesst",
                "Stufen 0 bis 4 in Prozent"))
            for schluessel in NS["WERTE_REIHENFOLGE"]:
                werte = [s.werte[schluessel] for s in spuren]
                stufen = collections.Counter(
                    NS["stufe_von_wert"](schluessel, w) for w in werte)
                verteilung = "  ".join(
                    "%4.0f" % prozent(stufen[n], len(werte)) for n in range(5))
                B("%-14s %-16s %8d %8.1f %8d   %s" % (
                    schluessel,
                    NS["WERT_BEZEICHNUNG"].get(schluessel, schluessel),
                    min(werte), sum(werte) / float(len(werte)), max(werte), verteilung))

            enden = collections.Counter(s.ende for s in spuren)
            B("")
            zeile = []
            for name in ENDEN:
                zeile.append("%s %.1f%%" % (name.replace("ende_", ""),
                                            prozent(enden[name], len(spuren))))
            B("   Ausgaenge:  " + "   ".join(zeile))

            harte = (enden["ende_verhungert"] + enden["ende_zusammenbruch"]
                     + enden["ende_verhaftet"])
            B("   harte Abbrueche (verhungert, zusammenbruch, verhaftet): %.1f Prozent"
              % prozent(harte, len(spuren)))
            if enden["notbremse"]:
                beanstandungen += 1
                B("   >> FEHLER << %d Durchgaenge wurden von der Notbremse beendet."
                  % enden["notbremse"])

    ## Gegenbewegung und Einbahnstrassen ######################################
    ##
    ## Die beiden Regeln aus Paket 2, Schritt 3. Sie stehen hier und nicht
    ## in einem Werkzeug daneben, damit jede spaetere Aenderung am Bestand
    ## sofort dagegen gemessen wird.
    offen = pfade_erreichbar(NS)

    def gibt_zurueck(auswahl):
        """Hebt diese Option versorgung/rueckhalt oder senkt sie belastung?"""
        aenderungen = auswahl.aenderungen or {}
        return (aenderungen.get("versorgung", 0) >= 1
                or aenderungen.get("rueckhalt", 0) >= 1
                or aenderungen.get("belastung", 0) <= -1)

    B.unterteil("Gegenbewegung: ein Weg zurueck in jedem Kapitel")
    B("Jedes Kapitel braucht auf jedem Pfad mindestens ein ziehbares")
    B("Ereignis mit einer Option, die versorgung oder rueckhalt um 1 hebt")
    B("oder belastung um 1 senkt. Sonst geht es nur noch abwaerts.")
    B("")
    B("%-6s %-16s %8s %10s   %s" % (
        "Jahr", "Pfad", "ziehbar", "mit Weg", "Befund"))
    for jahr in NS["KAPITEL_JAHRE"]:
        for pfad in offen:
            geprueft += 1
            ## Gefragt wird das Projekt (bestand_liste), nicht ein zweiter
            ## Ausdruck daneben - Teil D.15c.
            frei, bedingt = NS["bestand_liste"](jahr, pfad, "lang")
            ziehbar = frei + bedingt
            mit = [v for v in ziehbar if any(gibt_zurueck(o) for o in v.optionen)]
            if not ziehbar:
                befund = "kein Bestand (Probe 1)"
            elif not mit:
                beanstandungen += 1
                befund = ">> FEHLER << kein Weg zurueck"
            else:
                befund = "in Ordnung"
            B("%-6d %-16s %8d %10d   %s" % (
                jahr, NS["PFAD_MARKE"].get(pfad, pfad), len(ziehbar), len(mit), befund))

    ## EIN BESTAND FUER BEIDE PRUEFUNGEN ######################################
    ##
    ## SEIT PAKET 6, VORWEG E. Die Einbahnstrassenpruefung uebersprang
    ## Ereignisse mit nur_kette, die Dominanzpruefung nicht. Damit meldete
    ## die eine Faelle, die die andere nie ansah, und die Fallzahlen im
    ## Selbsttest liefen auseinander.
    ##
    ## Richtig ist der GROESSERE Bestand: Beide Regeln gelten fuer jede
    ## Karte, die eine Spielerin zu sehen bekommt - und ein Kettenglied
    ## bekommt sie zu sehen, sonst waere die Kette sinnlos. Ein
    ## nur_kette-Ereignis, auf das nichts zeigt, kann dagegen niemand
    ## sehen; es bleibt in beiden Pruefungen aussen vor.
    ## Genau das liefert ziehbare_ereignisse().
    pruefbestand = ziehbare_ereignisse(NS)

    ## DIE AUSNAHMEKLAUSEL AUS HANDWERKSREGEL g ###############################
    ##
    ## SEIT PAKET 6, nach dem Vorweg. Die Regel lautet in der Verfassung:
    ## "Keine Karte, bei der beide Optionen denselben Wert verschlechtern,
    ## OHNE DASS EINE DAVON DAS AN ANDERER STELLE AUSGLEICHT." Diese
    ## Probe kannte den zweiten Halbsatz nicht - sie meldete jede Karte,
    ## bei der alle Optionen denselben Wert senken.
    ##
    ## Aufgefallen ist der Unterschied an front_nachfrage, das Vorweg E
    ## erstmals in die Pruefung geholt hat (vorher fielen nur_kette-Karten
    ## heraus). Dort heben beide Optionen die Belastung, um 1 und um 2 -
    ## aber die zweite senkt den Verdacht und bezahlt das mit Versorgung.
    ## Das ist eine echte Entscheidung, und inhaltlich ist sie richtig:
    ## Ein Ermittlungsverfahren kostet Kraft, wie man sich auch entscheidet.
    ##
    ## WORAN DIE REGEL WIRKLICH HAENGT, steht in ihrer Begruendung: "Wer
    ## nur verlieren kann, entscheidet nicht mehr." Der Fehler ist also
    ## nicht, dass ein Wert immer faellt - der Fehler ist eine Karte, die
    ## NIRGENDS etwas zurueckgibt. Genau so ist die Ausnahme hier gefasst:
    ## Beanstandet wird, wenn alle Optionen denselben Wert verschlechtern
    ## UND keine einzige Option irgendeinen der vier Werte verbessert.
    ##
    ## Damit bleibt die Regel scharf. Eine Karte, auf der man nur
    ## verlieren kann, faellt weiter auf; eine Karte, die einen Preis
    ## verlangt und dafuer etwas gibt, nicht mehr. Was durch die Ausnahme
    ## rutscht, wird trotzdem gedruckt - nachrichtlich, damit niemand
    ## glaubt, hier sei etwas verschwunden.

    def gibt_irgendwo_zurueck(vorlage):
        """Verbessert irgendeine Option irgendeinen der vier Werte?"""
        for auswahl in vorlage.optionen:
            for schluessel in NS["WERTE_REIHENFOLGE"]:
                betrag = (auswahl.aenderungen or {}).get(schluessel, 0)
                hoch_ist_gut = NS["WERT_HOCH_IST_GUT"].get(schluessel, True)
                if (betrag > 0) if hoch_ist_gut else (betrag < 0):
                    return True
        return False

    B.unterteil("Einbahnstrassen: alle Optionen verschlechtern denselben Wert")
    B("Geprueft werden %d Karten: alle frei ziehbaren und alle, auf die eine"
      % len(pruefbestand))
    B("Option oder eine Einlage als Kette zeigt. Die Dominanzpruefung unten")
    B("nimmt denselben Bestand - seit Paket 6, Vorweg E.")
    B("")
    B("Beanstandet wird eine Karte, bei der ALLE Optionen denselben Wert")
    B("verschlechtern UND KEINE Option irgendeinen Wert verbessert. Wer nur")
    B("verlieren kann, entscheidet nicht mehr - das ist der Grund der Regel.")
    B("Eine Karte, die einen Preis verlangt und dafuer etwas gibt, steht")
    B("darunter nachrichtlich.")
    B("")
    einbahn = []
    ausgeglichen = []
    for vorlage in pruefbestand:
        gleicht_aus = gibt_irgendwo_zurueck(vorlage)
        for schluessel in NS["WERTE_REIHENFOLGE"]:
            hoch_ist_gut = NS["WERT_HOCH_IST_GUT"].get(schluessel, True)
            schaeden = []
            for auswahl in vorlage.optionen:
                betrag = (auswahl.aenderungen or {}).get(schluessel, 0)
                schaeden.append(-betrag if hoch_ist_gut else betrag)
            if not (schaeden and all(s > 0 for s in schaeden)):
                continue
            eintrag = (vorlage.kennung, "/".join(vorlage.pfad),
                       schluessel, schaeden)
            if gleicht_aus:
                ausgeglichen.append(eintrag)
            else:
                einbahn.append(eintrag)
    geprueft += len(pruefbestand)
    if not einbahn:
        B("   keine Beanstandung")
    for kennung, pfad, schluessel, schaeden in einbahn:
        beanstandungen += 1
        B("   FEHLER  %-34s %-16s %-16s Schaden %s"
          % (kennung, pfad, schluessel, schaeden))

    B("")
    if ausgeglichen:
        B("   Nachrichtlich - dieselbe Lage, aber die Karte gibt an anderer")
        B("   Stelle etwas zurueck (Ausnahme aus Handwerksregel g):")
        for kennung, pfad, schluessel, schaeden in ausgeglichen:
            B("      %-34s %-16s %-16s Schaden %s"
              % (kennung, pfad, schluessel, schaeden))
    else:
        B("   Keine Karte faellt unter die Ausnahme.")

    ## Dominierte Optionen ####################################################
    ##
    ## SEIT PAKET 4, VORWEG B. Die Einbahnstrassenpruefung darueber sucht
    ## Karten, bei denen ALLE Optionen denselben Wert verschlechtern. Sie
    ## findet nicht den umgekehrten Fall: EINE Option ist in allen vier
    ## Werten mindestens gleich gut und in mindestens einem besser. Wer
    ## eine solche Karte zieht, entscheidet nicht, er liest ab - und das
    ## verstoesst gegen die Regel, dass keine Option erkennbar richtig ist.
    ##
    ## Nicht jede Ungleichheit ist ein Fehler. Ausgenommen bleibt,
    ##
    ##   a) wo die schlechtere Option etwas bietet, das in keiner Zahl
    ##      steht: ein Merkmal, eine Kette, einen Sprung, einen Hinweis
    ##      oder eine Variante;
    ##   b) wo die bessere Option einen Preis traegt, der in keiner Zahl
    ##      steht: eine Variante (front_gas und front_stosstrupp springen
    ##      mit kleiner Wahrscheinlichkeit nach ende_gefallen), einen
    ##      Sprung oder einen Hinweis wie "verboten".
    ##
    ## Gemeldet wird also nur der saubere Fall: eine Option, die
    ## ausschliesslich besser ist, gegen eine, die ausschliesslich
    ## schlechter ist.

    def ausserhalb_der_zahlen(auswahl):
        """Traegt diese Option etwas, das in keiner der vier Zahlen steht?"""
        return bool(auswahl.merkmale) or bool(auswahl.kette) \
            or bool(auswahl.sprung) or bool(auswahl.hinweis) \
            or bool(auswahl.varianten)

    def guete(auswahl, schluessel):
        """Wie gut ist diese Option in diesem Wert? Groesser ist besser."""
        betrag = (auswahl.aenderungen or {}).get(schluessel, 0)
        if NS["WERT_HOCH_IST_GUT"].get(schluessel, True):
            return betrag
        return -betrag

    B.unterteil("Dominierte Optionen: eine Wahl, die keine ist")
    B("Beanstandet wird eine Option, die in allen vier Werten mindestens")
    B("gleich gut und in einem besser ist als eine andere derselben Karte -")
    B("sofern keine der beiden etwas traegt, das in den Zahlen nicht steht")
    B("(Merkmal, Kette, Sprung, Hinweis, Variante).")
    B("Geprueft werden dieselben %d Karten wie oben - seit Paket 6, Vorweg E."
      % len(pruefbestand))
    B("")
    dominiert = []
    for vorlage in pruefbestand:
        geprueft += 1
        opts = vorlage.optionen
        for stelle_a in range(len(opts)):
            for stelle_b in range(len(opts)):
                if stelle_a == stelle_b:
                    continue
                besser, schlechter = opts[stelle_a], opts[stelle_b]
                if ausserhalb_der_zahlen(besser) or ausserhalb_der_zahlen(schlechter):
                    continue
                paare = [(guete(besser, s), guete(schlechter, s))
                         for s in NS["WERTE_REIHENFOLGE"]]
                if not all(x >= y for x, y in paare):
                    continue
                if not any(x > y for x, y in paare):
                    continue
                vorteil = {}
                for schluessel in NS["WERTE_REIHENFOLGE"]:
                    abstand = guete(besser, schluessel) - guete(schlechter, schluessel)
                    if abstand:
                        vorteil[schluessel] = abstand
                dominiert.append((vorlage.kennung, "/".join(vorlage.pfad),
                                  besser.titel, schlechter.titel, vorteil))
    if not dominiert:
        B("   keine Beanstandung")
    for kennung, pfad, oben, unten, vorteil in dominiert:
        beanstandungen += 1
        B("   >> FEHLER << %-32s %s" % (kennung, pfad))
        B("                besser:     %s" % oben)
        B("                schlechter: %s" % unten)
        B("                Vorsprung:  %s" % vorteil)

    ## Reiner Kalenderverlauf #################################################
    B.unterteil("Reiner Kalenderverlauf, ohne ein einziges Ereignis")
    B("Nur KAPITEL_WIRKUNG und KAPITEL_WIRKUNG_PFAD, Beginn auf PFAD_BASIS,")
    B("ohne die Abweichung der Herkunft. Das ist die Kontrollrechnung, die in")
    B("kapitel.rpy, Abschnitt 3, als Kommentar steht: Wer die Tabellen dort")
    B("aendert, liest die Endwerte hier ab und traegt sie nach.")
    B("")
    B("%-16s %-8s %11s %11s %15s %11s   %s" % (
        "Pfad", "Jahr", "versorgung", "belastung", "aufmerksamkeit",
        "rueckhalt", "Befund"))

    merker = {}
    for name in ["versorgung", "belastung", "aufmerksamkeit", "rueckhalt",
                 "aktueller_pfad", "aktuelles_jahr", "letzte_aenderungen"]:
        merker[name] = NS[name]

    for pfad in NS["PFAD_REIHENFOLGE"]:
        geprueft += 1
        NS["aktueller_pfad"] = pfad
        NS["aktuelles_jahr"] = NS["KAPITEL_JAHRE"][0]
        basis = NS["PFAD_BASIS"][pfad]
        NS["versorgung"] = basis["versorgung"]
        NS["belastung"] = basis["belastung"]
        NS["aufmerksamkeit"] = basis["aufmerksamkeit"]
        NS["rueckhalt"] = basis["rueckhalt"]
        NS["letzte_aenderungen"] = {}

        B("%-16s %-8d %11d %11d %15d %11d   Beginn" % (
            NS["PFAD_MARKE"].get(pfad, pfad), NS["aktuelles_jahr"],
            NS["versorgung"], NS["belastung"], NS["aufmerksamkeit"], NS["rueckhalt"]))

        for jahr in NS["KAPITEL_JAHRE"][1:]:
            NS["aktuelles_jahr"] = jahr
            NS["kapitel_wirkung_anwenden"](jahr)
            ## ende_pruefen() greift im Epilog nicht mehr. Fuer die
            ## Kontrollrechnung wird trotzdem gegen die Schwellen geprueft,
            ## denn ein Kalender, der allein toetet, ist auch dann falsch.
            befund = ""
            schwellen = NS["ENDE_SCHWELLEN"]
            if NS["versorgung"] < schwellen["versorgung_unter"]:
                befund = ">> FEHLER << Kalender allein verhungert"
            elif NS["belastung"] >= schwellen["belastung_ab"]:
                befund = ">> FEHLER << Kalender allein Zusammenbruch"
            elif NS["aufmerksamkeit"] >= schwellen["aufmerksamkeit_ab"]:
                befund = ">> FEHLER << Kalender allein Verhaftung"
            if befund:
                beanstandungen += 1
            B("%-16s %-8d %11d %11d %15d %11d   %s" % (
                "", jahr, NS["versorgung"], NS["belastung"],
                NS["aufmerksamkeit"], NS["rueckhalt"], befund))
        B("")

    for name, wert in merker.items():
        NS[name] = wert

    return beanstandungen, geprueft


################################################################################
## 10. Probe 5: Belegprobe
################################################################################


def quelle_pruefen(NS, kennung, quelle):
    """Prueft ein einzelnes quelle-Woerterbuch gegen das Format.

    Liefert eine Liste von Beanstandungen als Klartext. Das Format steht
    im Kopf von script.rpy ueber der Klasse Ereignis.
    """
    maengel = []

    if not quelle:
        return ["kein quelle-Feld"]
    if not isinstance(quelle, dict):
        return ["quelle ist keine Zuordnung, sondern " + type(quelle).__name__]

    for feld in ("kurz", "voll", "art", "einordnung"):
        if not quelle.get(feld):
            maengel.append("Feld '%s' fehlt" % feld)

    kurz = quelle.get("kurz") or ""
    if len(kurz) > 60:
        maengel.append("kurz hat %d Zeichen, hoechstens 60 sind erlaubt" % len(kurz))

    art = quelle.get("art")
    arten = NS.get("QUELLE_ARTEN") or []
    if art and arten and art not in arten:
        maengel.append("art '%s' ist nicht in QUELLE_ARTEN" % art)

    zitat = quelle.get("zitat")
    if zitat:
        woerter = len([w for w in str(zitat).split() if w])
        if woerter > 15:
            maengel.append("zitat hat %d Woerter, hoechstens 15 sind erlaubt" % woerter)

    einordnung = quelle.get("einordnung")
    if einordnung and callable(NS.get("satzzahl")):
        anzahl = NS["satzzahl"](einordnung)
        if anzahl != 2:
            maengel.append("einordnung hat %d Saetze statt genau zwei" % anzahl)

    return maengel


def probe_beleg(NS, B):
    beanstandungen = 0
    geprueft = 0

    B.titel("PROBE 5  BELEGPROBE")
    B("Jeder Inhalt sagt, worauf er sich stuetzt. Geprueft wird seit Paket 3,")
    B("Schritt 1 nicht mehr nur, OB ein quelle-Feld da ist, sondern auch, ob")
    B("es dem Format entspricht: Kurzbeleg hoechstens 60 Zeichen, art aus der")
    B("Liste QUELLE_ARTEN, Zitat hoechstens 15 Woerter, einordnung genau zwei")
    B("Saetze. Ein Vollbeleg mit '%s' ist kein Fehler," % NS.get("QUELLE_FEHLT", "BELEG FEHLT"))
    B("sondern ein offener Auftrag; er wird getrennt gezaehlt.")

    fehlt_text = NS.get("QUELLE_FEHLT", "BELEG FEHLT - zu recherchieren")
    offen = 0
    arten = collections.Counter()

    B.unterteil("Tabelle: Kennung, Art, Beleg vorhanden")
    B("%-36s %-12s %-14s %s" % ("Kennung", "Art", "Beleg", "Befund"))

    for bestand, name in ((NS["EREIGNISSE"], "Ereignis"), (NS["EINLAGEN"], "Einlage")):
        for vorlage in bestand:
            geprueft += 1
            quelle = getattr(vorlage, "quelle", None)
            maengel = quelle_pruefen(NS, vorlage.kennung, quelle)
            if maengel:
                beanstandungen += len(maengel)

            art = quelle.get("art", "-") if isinstance(quelle, dict) else "-"
            arten[art] += 1
            voll = quelle.get("voll", "") if isinstance(quelle, dict) else ""
            if voll == fehlt_text:
                offen += 1
                beleg = "zu suchen"
            elif voll:
                beleg = "ja"
            else:
                beleg = "nein"

            befund = "in Ordnung" if not maengel else ("FEHLER: " + "; ".join(maengel))
            B("%-36s %-12s %-14s %s" % (vorlage.kennung, art, beleg, befund))

    B("")
    B("Ereignisse und Einlagen mit quelle-Feld: %d von %d."
      % (len([v for v in list(NS["EREIGNISSE"]) + list(NS["EINLAGEN"])
              if getattr(v, "quelle", None)]),
         len(NS["EREIGNISSE"]) + len(NS["EINLAGEN"])))
    B("Davon mit Vollbeleg: %d. Noch zu recherchieren: %d."
      % (geprueft - offen, offen))
    B("")
    B("Verteilung der Quellenarten:")
    for art, anzahl in arten.most_common():
        B("   %-14s %3d" % (art, anzahl))

    return beanstandungen, geprueft


################################################################################
## 11. Probe 6: Medienprobe
################################################################################


def medien_sammeln(NS, medienbuch, spielordner):
    """Jeden erwarteten Dateipfad MIT SEINER HERKUNFT.

    EINE Quelle fuer zwei Leser: probe_medien() zaehlt damit, und
    medienbedarf.py schreibt MEDIEN.md daraus. Stuenden die Schleifen
    zweimal da, naennte der Bedarfsplan andere Pfade als der Bericht, und
    niemand wuesste, welche Liste stimmt (Regel 11).

    Geliefert wird ein Woerterbuch

        pfad -> {"herkunft": [Satz, ...], "kategorie": str}

    und nebenbei das Medienbuch gefuellt, weil jeder Aufruf ueber
    renpy.loadable() laeuft. Die Zahl der Beanstandungen kommt mit: ein
    Pfad ohne Kennung darf so nie entstehen.
    """
    herkunft = collections.OrderedDict()

    def merken(pfad, satz, kategorie):
        pfad = str(pfad)
        eintrag = herkunft.setdefault(
            pfad, {"herkunft": [], "kategorie": kategorie})
        if satz not in eintrag["herkunft"]:
            eintrag["herkunft"].append(satz)

    ## Stimmungen aus dem gesamten Bestand einsammeln.
    stimmungen = set([NS["STIMMUNG_STANDARD"]])
    stimmungen.update(NS["STIMMUNG_AUS_WERT"].values())
    for vorlage in NS["EREIGNISSE"]:
        if vorlage.stimmung:
            stimmungen.add(vorlage.stimmung)
        for auswahl in vorlage.optionen:
            if auswahl.stimmung:
                stimmungen.add(auswahl.stimmung)
            for eintrag in auswahl.varianten:
                if eintrag.get("stimmung"):
                    stimmungen.add(eintrag["stimmung"])
    for szene in NS.get("SZENEN", []):
        if getattr(szene, "stimmung", None):
            stimmungen.add(szene.stimmung)
        for zeile in szene.zeilen:
            if getattr(zeile, "stimmung", None):
                stimmungen.add(zeile.stimmung)
    stimmungen = sorted(stimmungen)

    beanstandungen = 0
    typenzaehler = collections.Counter()

    ## 1. Karten und Dokumente: jede Option traegt ein Bild. Welcher Ordner,
    ##    entscheidet der Kartentyp - gefragt wird kartenmotiv(), also
    ##    dieselbe Funktion, die auch der Bildschirm ruft.
    for vorlage in NS["EREIGNISSE"]:
        typ = getattr(vorlage, "kartentyp", "karte")
        typenzaehler[typ] += 1
        kategorie = NS["kartenbild_kategorie"](typ)
        nummer = 0
        for auswahl in vorlage.optionen:
            nummer += 1
            NS["kartenmotiv"](vorlage, auswahl, 468, 264)
            if not auswahl.bild:
                beanstandungen += 1
                continue
            merken(NS["bild_pfad"](kategorie, auswahl.bild),
                   "Ereignis %s, Option %d - Kartentyp %s, gezeichnet in "
                   "screens.rpy ueber kartenmotiv()"
                   % (vorlage.kennung, nummer, typ),
                   kategorie)

    ## 2. Portraets: Herkunft und Geschlecht, dazu jede Stimmung.
    ##    portrait_anzeigen() probiert drei Kandidaten der Reihe nach.
    for quelle in NS["HERKUENFTE"]:
        for geschlecht in ["m", "w"]:
            kennung = str(quelle.kennung) + "_" + geschlecht
            for stimmung in stimmungen:
                NS["portrait_anzeigen"](kennung, stimmung, 122, 122)
                kandidaten = [
                    (kennung + "_" + str(stimmung),
                     "Stimmung %s" % stimmung),
                    (kennung + "_neutral",
                     "Rueckfall, wenn die Stimmung fehlt"),
                    (kennung,
                     "letzter Rueckfall, ohne Stimmung"),
                ]
                for name, warum in kandidaten:
                    merken(NS["bild_pfad"]("portraits", name),
                           "Portraet %s, %s - %s, ueber portrait_anzeigen()"
                           % (quelle.kennung,
                              "maennlich" if geschlecht == "m" else "weiblich",
                              warum),
                           "images/portraits")

    ## 3. Nebenfiguren. FIGUREN_ECHTE_BILDER steht noch auf False, deshalb
    ##    fragt figur_bild() diese Pfade heute gar nicht ab. Sie werden
    ##    trotzdem aufgefuehrt, damit die Liste vollstaendig ist.
    for kennung in NS["FIGUREN_REIHENFOLGE"]:
        for pfad in NS["PFAD_REIHENFOLGE"]:
            for stimmung in stimmungen:
                name = "images/figuren/%s_%s_%s.png" % (kennung, pfad, stimmung)
                da = os.path.isfile(
                    os.path.join(spielordner, name.replace("/", os.sep)))
                eintrag = medienbuch.setdefault(
                    name, {"anfragen": 0, "vorhanden": da})
                eintrag["vorhanden"] = da
                merken(name,
                       "Nebenfigur %s auf Pfad %s, Stimmung %s - "
                       "figur_bild_pfad() in dialoge.rpy; wird erst gesucht, "
                       "wenn FIGUREN_ECHTE_BILDER auf True steht"
                       % (kennung, pfad, stimmung),
                       "images/figuren")

    ## 4. Der Platzhalter, der einspringt, solange kein Figurenbild liegt.
    NS["renpy"].loadable(NS["FIGUREN_PLATZHALTER"])
    merken(NS["FIGUREN_PLATZHALTER"],
           "Ersatzbild fuer jede Nebenfigur - FIGUREN_PLATZHALTER, "
           "figur_bild() in dialoge.rpy",
           "images")

    ## 5. Schriften. Welche Datei zu welcher Schrift gehoert, sagt
    ##    SCHRIFT_KANDIDATEN in gui.rpy - gefragt, nicht nachgebaut.
    for name in sorted(NS.get("SCHRIFT_KANDIDATEN", {})):
        zweck = NS.get("SCHRIFT_ZWECK", {}).get(name, "")
        for stelle, pfad in enumerate(NS["SCHRIFT_KANDIDATEN"][name]):
            NS["renpy"].loadable(pfad)
            merken(pfad,
                   "%s (%s) - %s Wahl in schrift_waehlen(), gui.rpy"
                   % (name, zweck, "erste" if stelle == 0 else "zweite"),
                   "fonts")

    ## 6. Ortsklaenge und Musik. SEIT PAKET 8, SCHRITT 2.6. Welche Datei zu
    ##    welchem Klangraum und zu welcher Stelle im Ablauf gehoert, sagen
    ##    ORTSKLANG und STELLENMUSIK in ton.rpy; den Pfad baut
    ##    ton_kandidaten() - gefragt, nicht nachgebaut. Stuende "audio/" hier
    ##    ein zweites Mal, liefe der Bedarfsplan frueher oder spaeter neben
    ##    dem Spiel her (Regel 11).
    ##
    ##    Ohne diesen Abschnitt bliebe Auftragspunkt 11 unerfuellt: Der
    ##    Spielcode merkt sich keine fehlende Datei, das Medienbuch fuellt
    ##    sich allein dadurch, dass die Probe renpy.loadable() ruft.
    if callable(NS.get("ton_kandidaten")):
        for tafel, art, quelle in (
                (NS.get("ORTSKLANG", {}), "Umgebungsklang", "ORTSKLANG"),
                (NS.get("STELLENMUSIK", {}), "Musik", "STELLENMUSIK")):
            for kennung in sorted(tafel):
                dateikennung, lautstaerke, wiederholt = tafel[kennung]
                zweck = NS.get("KLANGRAUM_ZWECK", {}).get(kennung, "")
                for stelle, pfad in enumerate(
                        NS["ton_kandidaten"](dateikennung)):
                    NS["renpy"].loadable(pfad)
                    merken(pfad,
                           "%s %s%s - Lautstaerke %.2f, %s, %s Wahl in "
                           "ton_waehlen(), %s in ton.rpy"
                           % (art, kennung,
                              (" - " + zweck) if zweck else "",
                              lautstaerke,
                              "wiederholt sich" if wiederholt
                              else "laeuft einmal",
                              "erste" if stelle == 0 else "zweite",
                              quelle),
                           "audio")

    return herkunft, stimmungen, typenzaehler, beanstandungen


def probe_medien(NS, B, medienbuch, spielordner):
    """Sammelt alle Pfade, die der Code je gesucht hat oder suchen wird.

    Die Bilder legt der Projektleiter spaeter selbst ab. Eine fehlende
    Datei ist deshalb KEINE Beanstandung: Der Code faellt ueberall sauber
    auf bild_platzhalter() oder auf eine Ersatzschrift zurueck. Beanstandet
    wird nur ein Pfad, der so nie entstehen darf - eine leere Kennung etwa.
    """
    _herkunft, stimmungen, typenzaehler, beanstandungen = medien_sammeln(
        NS, medienbuch, spielordner)

    B.titel("PROBE 6  MEDIENPROBE")
    B("Alle Dateipfade, die der Code ueber bild_pfad(), portrait_anzeigen(),")
    B("figur_bild_pfad(), schrift_waehlen() oder ton_waehlen() erwartet. Eine")
    B("fehlende Datei ist kein Fehler: ueberall greift ein sauberer Ersatz,")
    B("und wo ein Ton fehlt, ist es still. Die Liste sagt, was noch")
    B("abzulegen ist.")
    B("")
    B("Beruecksichtigte Stimmungen: " + ", ".join(stimmungen))

    return probe_medien_bericht(NS, B, medienbuch, spielordner,
                                typenzaehler, beanstandungen)


def probe_medien_bericht(NS, B, medienbuch, spielordner,
                         typenzaehler, beanstandungen):
    """Schreibt den Abschnitt aus, den medien_sammeln() gefuellt hat."""

    ## Gruppieren nach Kategorie.
    gruppen = collections.OrderedDict()
    for pfad in sorted(medienbuch):
        teile = pfad.split("/")
        if len(teile) >= 2:
            kategorie = "/".join(teile[:-1])
        else:
            kategorie = "(Wurzel)"
        gruppen.setdefault(kategorie, []).append(pfad)

    gesamt = 0
    vorhanden_gesamt = 0
    for kategorie, pfade in gruppen.items():
        da = len([p for p in pfade if medienbuch[p]["vorhanden"]])
        gesamt += len(pfade)
        vorhanden_gesamt += da
        zusatz = ""
        if kategorie == "images/figuren":
            zusatz = "   (erst gesucht, wenn FIGUREN_ECHTE_BILDER auf True steht)"
        B.unterteil("%s - %d erwartet, %d vorhanden%s"
                    % (kategorie, len(pfade), da, zusatz))
        for pfad in pfade:
            eintrag = medienbuch[pfad]
            marke = "vorhanden" if eintrag["vorhanden"] else "fehlt noch"
            B("   %-12s %s" % (marke, pfad))

    ## Verwaiste Dateien: liegt ab, wird aber nirgends gesucht.
    verwaist = []
    for ordner in ["images", "fonts", "audio"]:
        wurzel = os.path.join(spielordner, ordner)
        if not os.path.isdir(wurzel):
            continue
        for gang, _unter, dateien in os.walk(wurzel):
            for name in dateien:
                voll = os.path.join(gang, name)
                rel = os.path.relpath(voll, spielordner).replace(os.sep, "/")
                if rel not in medienbuch:
                    verwaist.append(rel)

    B.unterteil("Vorhanden, aber von keiner Stelle im Code erwartet")
    if not verwaist:
        B("   keine")
    for rel in sorted(verwaist):
        B("   %s" % rel)

    ## Bildarten, fuer die BILD_MASSE ein Format nennt, die aber niemand
    ## abruft. Kein Fehler, sondern ein Hinweis darauf, was noch aussteht.
    genutzt = set()
    for pfad in medienbuch:
        teile = pfad.split("/")
        if len(teile) >= 3 and teile[0] == "images":
            genutzt.add(teile[1])
    ungenutzt = [k for k in NS["BILD_MASSE"] if k not in genutzt]
    B.unterteil("In BILD_MASSE angelegt, aber von keiner Stelle abgerufen")
    if not ungenutzt:
        B("   keine")
    for kategorie in ungenutzt:
        B("   %-14s Anzeigemass %s" % (
            kategorie, NS["BILD_ANZEIGE"].get(kategorie, "-")))

    ## Die Kartentypen. Ein Typ, den KARTENTYPEN nicht kennt, faellt im Spiel
    ## still auf "karte" zurueck - eine Brotkarte saehe dann aus wie eine
    ## Szene, ohne dass irgendwo ein Fehler entstuende. Deshalb sammelt die
    ## Klasse jeden solchen Fall in KARTENTYP_UNBEKANNT, und hier wird er
    ## beanstandet. Dieselbe Bauart wie NACHTRAG_OHNE_TREFFER.
    B.unterteil("Kartentypen")
    for typ in NS["KARTENTYPEN"]:
        B("   %-14s %3d Ereignisse   Bildordner images/%s"
          % (typ, typenzaehler.get(typ, 0), NS["kartenbild_kategorie"](typ)))
    unbekannt = NS["KARTENTYP_UNBEKANNT"]
    if unbekannt:
        B("")
        B("   UNBEKANNTER TYP - faellt im Spiel still auf \"karte\" zurueck:")
        for kennung, typ in unbekannt:
            B("      %-36s %s" % (kennung, typ))
        beanstandungen += len(unbekannt)
    else:
        B("   Kein unbekannter Typ.")

    ## Die Schriften werden NICHT namentlich aufgezaehlt, sondern aus
    ## SCHRIFT_KANDIDATEN geholt. Bis Paket 8, Schritt 1 standen hier drei
    ## feste Namen; die vierte Schrift waere stillschweigend aus dem Bericht
    ## gefallen, obwohl ihre Kandidatenpfade laengst mitgezaehlt wurden.
    ## Eine fuenfte findet sich jetzt von selbst.
    ##
    ## Gefragt wird die Kandidatentafel und nicht der Namensraum nach dem
    ## Praefix "SCHRIFT_": Der erste Versuch tat das und zog prompt
    ## SCHRIFT_KANDIDATEN und SCHRIFT_ZWECK mit in die Liste der Schriften.
    schriftnamen = sorted(NS.get("SCHRIFT_KANDIDATEN", {}))
    B("")
    B("Schriften (%d). Der Wert ist die Datei, die wirklich greift -" % len(schriftnamen))
    B("bei fehlender Datei der Ersatz aus schrift_waehlen().")
    for name in schriftnamen:
        B("   %-18s %s" % (name, NS[name]))
    B("Erwartet insgesamt: %d Pfade, davon %d vorhanden, %d noch abzulegen."
      % (gesamt, vorhanden_gesamt, gesamt - vorhanden_gesamt))

    return beanstandungen, gesamt


################################################################################
## 12. Probe 7: Sprachprobe
################################################################################


def probe_sprache(NS, B):
    """Faehrt die Sprachpruefung des Projekts ueber alle Lagen.

    Die Pruefung ist lageabhaengig: einlagen_ausgangstexte() rechnet die
    Auswertungen mit dem gerade geltenden Pfad durch, und welttext() waehlt
    die Fassung danach aus. Deshalb wird sie fuer jeden Pfad und mehrere
    Merkmalslagen wiederholt und werden die Funde zusammengefasst.
    """
    beanstandungen = 0
    geprueft = 0

    lagen = []
    for pfad in NS["PFAD_REIHENFOLGE"]:
        for herkunft in ["arbeiterschaft", "buergertum", "landbevoelkerung", "adel"]:
            lagen.append((herkunft, pfad, None))
    lagen.append(("buergertum", "front", "offizier"))
    lagen.append(("arbeiterschaft", "heimat", "ruestung"))
    lagen.append(("buergertum", "etappe", "lazarett"))

    funde = {}
    for herkunft, pfad, zusatz in lagen:
        NS["zustand_zuruecksetzen"]()
        NS["probe_lebenslage"](herkunft, pfad, zusatz)
        NS["aktuelles_jahr"] = 1917
        geprueft += textstellen_zaehlen(NS)
        for fund in NS["sprachpruefung_durchfuehren"]():
            funde[(fund[0], fund[1], fund[2], fund[4])] = fund

    B.titel("PROBE 7  SPRACHPROBE")
    B("TABU_BEGRIFFE und PRUEF_BEGRIFFE ueber Ereignisse, Szenen, Kapitel-")
    B("und Endtexte, Briefe, Schicksalsmeldungen und Einlagen, dazu die")
    B("Wertungswoerter und die Zwei-Saetze-Regel der Einordnungen.")
    B("Geprueft in %d Lagen (Herkunft, Pfad, Zusatzmerkmal)." % len(lagen))
    B("")

    if not funde:
        B("   keine Beanstandung")
    else:
        for schluessel in sorted(funde):
            fund = funde[schluessel]
            beanstandungen += 1
            B("   %-7s %-34s %-24s" % (fund[0], fund[1], fund[2]))
            B("           %s" % fund[3])
            B("           Fundstelle: %s" % fund[4])
            B("")

    ## Die Zwei-Saetze-Regel getrennt ausweisen, weil sie eine eigene
    ## Zusage aus minispiele.rpy ist.
    B.unterteil("Zwei-Saetze-Regel der Einordnungen")
    for vorlage in NS["EINLAGEN"]:
        fassungen = vorlage.einordnung
        paare = list(fassungen.items()) if isinstance(fassungen, dict) else [("standard", fassungen)]
        for name, text in paare:
            anzahl = NS["satzzahl"](text)
            marke = "in Ordnung" if anzahl == 2 else ">> FEHLER <<"
            B("   %-12s %-14s %-14s %d Saetze, %d Zeichen" % (
                marke, vorlage.kennung, name, anzahl, len(text or "")))

    return beanstandungen, geprueft


def textstellen_zaehlen(NS):
    """Zaehlt, wie viele einzelne Textstellen eine Sprachpruefung ansieht."""
    anzahl = 0
    try:
        for vorlage in NS["EREIGNISSE"]:
            anzahl += len(NS["ereignis_texte"](vorlage))
        for szene in NS["SZENEN"]:
            anzahl += len(NS["szenen_texte"](szene))
        for sammler in ["kapiteltexte_sammeln", "endtexte_sammeln",
                        "brieftexte_sammeln", "schicksalstexte_sammeln",
                        "einlagentexte_sammeln"]:
            if sammler in NS and callable(NS[sammler]):
                for _ort, texte in NS[sammler]():
                    anzahl += len(texte)
    except Exception:
        pass
    return anzahl


################################################################################
## 12b. Probe 8: Lesbarkeit
################################################################################
##
## Seit Paket 3, Schritt 2. Das Sprachmass fuer Klasse 8 stand bisher nur
## im Auftrag und war damit nicht nachpruefbar:
##
##   - durchschnittliche Satzlaenge hoechstens 13 Woerter
##   - kein Satz laenger als 20 Woerter
##   - hoechstens ein Nebensatz je Satz
##
## Gezaehlt wird ueber den gesamten Textbestand, getrennt nach Textart.
## Die Nebensatzzaehlung ist eine Naeherung: Ein Nebensatz wird dort
## vermutet, wo ein Komma vor einer unterordnenden Konjunktion oder einem
## Relativpronomen steht. Die Naeherung ist nicht genau, aber sie bleibt
## gleich - und damit lassen sich zwei Staende vergleichen.
##
## Diese Probe MISST nur. Repariert wird in den Inhaltspaketen.

## Unterordnende Konjunktionen und Relativpronomen. Klein geschrieben,
## verglichen wird in Kleinschreibung.
NEBENSATZ_WOERTER = [
    "dass", "weil", "obwohl", "damit", "wenn", "als", "während", "bevor",
    "nachdem", "seit", "seitdem", "bis", "falls", "ob", "indem", "sodass",
    "sobald", "solange", "wo", "wie", "der", "die", "das", "den", "dem",
    "welcher", "welche", "welches",
]

## Der Trenner erlaubt seit Paket 5, Schritt 1 ein schliessendes
## Anfuehrungszeichen zwischen Punkt und Leerzeichen. Vorher endete ein
## Satz, der mit woertlicher Rede aufhoerte, fuer den Zerleger nicht -
## er wuchs mit dem naechsten zusammen und galt dann als zu lang.
## Beide Ruecksichten sind fester Breite, sonst nimmt re sie nicht.
SATZ_TRENNER = re.compile(r"(?:(?<=[.!?])|(?<=[.!?]\")|(?<=[.!?]“)|(?<=[.!?]»))\s+")
WORT_MUSTER = re.compile(r"[^\s]+")

## Eine Ordnungszahl ist ein- oder zweistellig: der 1. Maerz, der 22.
## Februar, der 9. November. Eine vierstellige Zahl ist eine Jahreszahl
## und beendet sehr wohl einen Satz. Die alte Regel entfernte JEDEN
## Punkt hinter einer Ziffer und liess dadurch Saetze verschmelzen.
ORDNUNGSZAHL = re.compile(r"(?<!\d)(\d{1,2})\.(?=\s)")


def saetze_zerlegen(text):
    """Zerlegt einen Text in Saetze. Ordnungszahlen zaehlen nicht mit."""
    if not text:
        return []
    ## "22. Februar" ist kein Satzende, "im Herbst 1914." schon. Der
    ## Punkt hinter einer ORDNUNGSZAHL wird vor dem Trennen entfernt,
    ## genau wie in satzzahl() (minispiele.rpy). Beide Stellen tragen
    ## seit Paket 5, Schritt 1 dieselbe Regel; wer die eine aendert,
    ## aendert die andere mit, sonst zaehlen Probe 5 und Probe 8
    ## verschieden.
    bereinigt = ORDNUNGSZAHL.sub(r"\1", str(text).strip())
    return [s.strip() for s in SATZ_TRENNER.split(bereinigt) if s.strip()]


## Die Regel VOR Paket 5, Schritt 1. Sie steht hier ausschliesslich, damit
## die Gegenprobe in Probe 8 zeigen kann, was sich geaendert hat. Benutzt
## wird sie fuer keine Messung.
ALT_ZAHL = re.compile(r"(\d)\.")
ALT_TRENNER = re.compile(r"(?<=[.!?])\s+")


def saetze_zerlegen_alt(text):
    """Der Zerleger, wie er bis Paket 5, Schritt 1 gearbeitet hat."""
    if not text:
        return []
    bereinigt = ALT_ZAHL.sub(r"\1", str(text).strip())
    return [s.strip() for s in ALT_TRENNER.split(bereinigt) if s.strip()]


def woerter_zaehlen(satz):
    return len(WORT_MUSTER.findall(satz))


def nebensaetze_zaehlen(satz):
    """Naeherung: Kommas, hinter denen ein einleitendes Wort steht."""
    anzahl = 0
    for stueck in satz.split(",")[1:]:
        erstes = stueck.strip().split(" ")
        if not erstes or not erstes[0]:
            continue
        wort = erstes[0].strip("„“\"'()-").lower()
        if wort in NEBENSATZ_WOERTER:
            anzahl += 1
    return anzahl


def textbestand_sammeln(NS):
    """Alle Texte des Spiels, nach Art getrennt.

    Geliefert wird eine Liste (Art, Fundstelle, Text). Benutzt werden die
    Sammelfunktionen des Projekts, damit kein Bestand vergessen wird, den
    ein spaeteres Paket hinzufuegt.
    """
    bestand = []

    for vorlage in NS["EREIGNISSE"]:
        for satz in NS["ereignis_texte"](vorlage):
            bestand.append(("Ereignis", vorlage.kennung, satz))

    for szene in NS["SZENEN"]:
        for satz in NS["szenen_texte"](szene):
            bestand.append(("Szene", szene.kennung, satz))

    sammler = [
        ("Kapitel", "kapiteltexte_sammeln"),
        ("Ende", "endtexte_sammeln"),
        ("Brief", "brieftexte_sammeln"),
        ("Schicksal", "schicksalstexte_sammeln"),
        ("Einlage", "einlagentexte_sammeln"),
        ("Merkbuch", "merkbuchtexte_sammeln"),
    ]
    for art, name in sammler:
        if name in NS and callable(NS[name]):
            try:
                for ort, texte in NS[name]():
                    for satz in texte:
                        bestand.append((art, ort, satz))
            except Exception:
                pass

    return bestand


## Die fuenf Gattungen aus Paket 5, Schritt 3, Teil D.16 ######################
##
## Die grobe Aufteilung oben sagt, WO ein Satz steht (Ereignis, Szene,
## Brief). Diese hier sagt, WAS er ist - und darauf kommt es beim
## Sprachmass an: Ein Ereignistext wird gelesen wie eine Erzaehlung, eine
## Einordnung wie ein Lexikoneintrag, ein Optionstitel wie eine
## Schaltflaeche. Zwoelf zu lange Saetze standen bisher als "Einlage" in
## der Tafel und verdeckten, dass es ausnahmslos Einordnungen sind -
## bekannt, entschieden (Entscheidung 9) und in Paket 6, Schritt 2 zum
## Kuerzen vorgesehen.
##
## "Glossar" gibt es noch nicht. Die Zeile steht trotzdem in der Tafel und
## meldet "noch kein Bestand": Eine Zeile, die fehlt, liest sich wie eine
## Null, und das waere falsch (Regel 11).

GATTUNGEN = ["Ereignistext", "Optionstext", "Einordnung", "Glossar", "Sonstiges"]


def textbestand_fein(NS):
    """Derselbe Bestand wie textbestand_sammeln, nach Gattung getrennt.

    Liefert (Gattung, Fundstelle, Text). Eingesammelt wird mit
    texte_sammeln() des Projekts, damit verschachtelte Varianten-
    woerterbuecher genauso aufgeloest werden wie dort.

    EIN UNTERSCHIED ZUR GROBEN TAFEL, der genannt sein will: Hier sind
    auch die Einordnungen aus den quelle-Woerterbuechern der Ereignisse
    dabei. Probe 8 hat sie nie gemessen, obwohl sie im Analysemodus auf
    dem Bildschirm stehen und obwohl Probe 5 ihre Satzzahl prueft. Die
    Zahl der gemessenen Saetze steigt dadurch; probe_lesbarkeit() nennt
    beide Zahlen und die Differenz.
    """
    fein = []
    sammeln = NS["texte_sammeln"]

    for vorlage in NS["EREIGNISSE"]:
        for satz in sammeln(vorlage.text):
            fein.append(("Ereignistext", vorlage.kennung, satz))
        for auswahl in vorlage.optionen:
            for feld in (auswahl.titel, auswahl.beschreibung,
                         auswahl.ausgang, auswahl.hinweis):
                for satz in sammeln(feld):
                    fein.append(("Optionstext", vorlage.kennung, satz))
            for eintrag in (getattr(auswahl, "varianten", None) or []):
                for satz in sammeln(eintrag.get("ausgang")):
                    fein.append(("Optionstext", vorlage.kennung, satz))
        quelle = getattr(vorlage, "quelle", None)
        if isinstance(quelle, dict) and quelle.get("einordnung"):
            for satz in sammeln(quelle["einordnung"]):
                fein.append(("Einordnung", "Quelle " + vorlage.kennung, satz))

    for vorlage in NS["EINLAGEN"]:
        for satz in sammeln(vorlage.einordnung):
            fein.append(("Einordnung", "Einlage " + vorlage.kennung, satz))
        quelle = getattr(vorlage, "quelle", None)
        if isinstance(quelle, dict) and quelle.get("einordnung"):
            for satz in sammeln(quelle["einordnung"]):
                fein.append(("Einordnung", "Quelle " + vorlage.kennung, satz))
        for feld in (vorlage.titel, vorlage.einleitung, vorlage.anweisung):
            for satz in sammeln(feld):
                fein.append(("Sonstiges", "Einlage " + vorlage.kennung, satz))

    ## Alles Uebrige kommt aus der groben Sammlung. Uebergangen wird nur,
    ## was oben schon eigens aufgenommen ist - sonst stuende es zweimal.
    for art, ort, text in textbestand_sammeln(NS):
        if art == "Ereignis":
            continue
        if art == "Einlage" and str(ort).startswith("Einlage "):
            continue
        fein.append(("Sonstiges", ort, text))

    return fein


def probe_lesbarkeit(NS, B):
    beanstandungen = 0

    B.titel("PROBE 8  LESBARKEIT")
    B("Sprachmass Klasse 8: durchschnittlich hoechstens %d Woerter je Satz,"
      % LESBAR_SCHNITT)
    B("kein Satz ueber %d Woerter, hoechstens ein Nebensatz je Satz."
      % LESBAR_HOECHSTENS)
    B("Beanstandet wird ein Durchschnitt ueber %d oder ein Satz ueber %d."
      % (LESBAR_SCHNITT, LESBAR_HOECHSTENS))
    B("Diese Probe misst nur. Repariert wird in den Inhaltspaketen.")

    bestand = textbestand_sammeln(NS)

    nach_art = collections.OrderedDict()
    lang = []
    verschachtelt = []
    alle_saetze = 0
    alle_woerter = 0

    for art, ort, text in bestand:
        for satz in saetze_zerlegen(text):
            anzahl = woerter_zaehlen(satz)
            if not anzahl:
                continue
            eintrag = nach_art.setdefault(art, {"saetze": 0, "woerter": 0,
                                                "lang": 0, "nester": 0})
            eintrag["saetze"] += 1
            eintrag["woerter"] += anzahl
            alle_saetze += 1
            alle_woerter += anzahl
            if anzahl > LESBAR_HOECHSTENS:
                eintrag["lang"] += 1
                lang.append((anzahl, art, ort, satz))
            nester = nebensaetze_zaehlen(satz)
            if nester > 1:
                eintrag["nester"] += 1
                verschachtelt.append((nester, art, ort, satz))

    B.unterteil("Satzlaenge je Textart")
    B("%-12s %8s %8s %10s %10s %10s   %s" % (
        "Art", "Saetze", "Woerter", "Schnitt", "ueber %d" % LESBAR_HOECHSTENS,
        "verschachtelt", "Befund"))
    for art, eintrag in nach_art.items():
        schnitt = eintrag["woerter"] / float(eintrag["saetze"])
        maengel = []
        if schnitt > LESBAR_SCHNITT:
            maengel.append("Schnitt ueber %d" % LESBAR_SCHNITT)
        if eintrag["lang"]:
            maengel.append("%d zu lange Saetze" % eintrag["lang"])
        if maengel:
            beanstandungen += len(maengel)
        B("%-12s %8d %8d %10.1f %10d %10d   %s" % (
            art, eintrag["saetze"], eintrag["woerter"], schnitt,
            eintrag["lang"], eintrag["nester"],
            (">> FEHLER << " + ", ".join(maengel)) if maengel else "in Ordnung"))

    if alle_saetze:
        B("")
        B("%-12s %8d %8d %10.1f %10d %10d" % (
            "GESAMT", alle_saetze, alle_woerter,
            alle_woerter / float(alle_saetze), len(lang), len(verschachtelt)))

    B.unterteil("Die zehn laengsten Saetze")
    if not lang:
        B("   Kein Satz ueber %d Woerter." % LESBAR_HOECHSTENS)
    for anzahl, art, ort, satz in sorted(lang, reverse=True)[:10]:
        B("   %3d Woerter  %-10s %s" % (anzahl, art, ort))
        B("        %s" % satz)

    B.unterteil("Saetze mit mehr als einem Nebensatz (Naeherung)")
    if not verschachtelt:
        B("   keine")
    for anzahl, art, ort, satz in sorted(verschachtelt, reverse=True)[:10]:
        B("   %d Nebensaetze  %-10s %s" % (anzahl, art, ort))
        B("        %s" % satz[:140])
    if len(verschachtelt) > 10:
        B("   ... und %d weitere" % (len(verschachtelt) - 10))

    ## Die fuenf Gattungen ####################################################
    ##
    ## SEIT PAKET 5, SCHRITT 3, TEIL D.16.
    fein = textbestand_fein(NS)
    nach_gattung = collections.OrderedDict()
    for name in GATTUNGEN:
        nach_gattung[name] = {"saetze": 0, "woerter": 0, "lang": 0, "nester": 0,
                              "funde": []}
    fein_saetze = 0

    for gattung, ort, text in fein:
        eintrag = nach_gattung.setdefault(
            gattung, {"saetze": 0, "woerter": 0, "lang": 0, "nester": 0,
                      "funde": []})
        for satz in saetze_zerlegen(text):
            anzahl = woerter_zaehlen(satz)
            if not anzahl:
                continue
            eintrag["saetze"] += 1
            eintrag["woerter"] += anzahl
            fein_saetze += 1
            if anzahl > LESBAR_HOECHSTENS:
                eintrag["lang"] += 1
                eintrag["funde"].append((anzahl, ort, satz))
            if nebensaetze_zaehlen(satz) > 1:
                eintrag["nester"] += 1

    B.unterteil("Satzlaenge je Gattung")
    B("Was ein Satz IST, nicht wo er steht. Ein Ereignistext wird gelesen wie")
    B("eine Erzaehlung, eine Einordnung wie ein Lexikoneintrag. Erst getrennt")
    B("ist zu sehen, ob eine Beanstandung den Spieltext trifft oder den Beleg.")
    B("Diese Tafel misst mehr als die obere: Sie nimmt auch die Einordnungen")
    B("aus den quelle-Woerterbuechern der Ereignisse auf, die Probe 8 bisher")
    B("nie angesehen hat. Die Zahlen stehen darum nicht nebeneinander.")
    B("")
    B("%-14s %8s %8s %10s %10s %14s   %s" % (
        "Gattung", "Saetze", "Woerter", "Schnitt", "ueber %d" % LESBAR_HOECHSTENS,
        "verschachtelt", "Befund"))
    for gattung in GATTUNGEN:
        eintrag = nach_gattung[gattung]
        if not eintrag["saetze"]:
            B("%-14s %8s %8s %10s %10s %14s   %s" % (
                gattung, "-", "-", "-", "-", "-", "noch kein Bestand"))
            continue
        schnitt = eintrag["woerter"] / float(eintrag["saetze"])
        maengel = []
        if schnitt > LESBAR_SCHNITT:
            maengel.append("Schnitt ueber %d" % LESBAR_SCHNITT)
        if eintrag["lang"]:
            maengel.append("%d zu lange Saetze" % eintrag["lang"])
        B("%-14s %8d %8d %10.1f %10d %14d   %s" % (
            gattung, eintrag["saetze"], eintrag["woerter"], schnitt,
            eintrag["lang"], eintrag["nester"],
            ("aufgeschluesselt: " + ", ".join(maengel)) if maengel
            else "in Ordnung"))

    ## WAS HIER GEZAEHLT WIRD UND WAS NICHT.
    ## Die zu langen Saetze der Einlagen stehen schon in der Tafel nach
    ## Textart und sind dort beanstandet. Sie hier noch einmal zu zaehlen,
    ## hiesse denselben Fund zweimal fuehren. Gezaehlt wird deshalb nur,
    ## was die obere Tafel nicht sehen kann: die Einordnungen aus den
    ## quelle-Woerterbuechern. Sie stehen im Analysemodus auf dem
    ## Bildschirm, Probe 5 prueft ihre Satzzahl - und Probe 8 hat sie bis
    ## heute nie gemessen.
    neu_sichtbar = [
        (anzahl, ort, satz)
        for anzahl, ort, satz in nach_gattung["Einordnung"]["funde"]
        if str(ort).startswith("Quelle ")]

    B("")
    B("Saetze in dieser Tafel: %d. In der Tafel nach Textart: %d."
      % (fein_saetze, alle_saetze))
    B("Die Differenz von %d sind die Einordnungen aus den quelle-Feldern."
      % (fein_saetze - alle_saetze))
    B("")
    if neu_sichtbar:
        beanstandungen += len(neu_sichtbar)
        B(">> FEHLER << %d zu lange Saetze in quelle-Einordnungen. Sie sind"
          % len(neu_sichtbar))
        B("             neu sichtbar, nicht neu entstanden: Probe 8 hat diese")
        B("             Texte bis Paket 5, Schritt 3 gar nicht angesehen.")
    else:
        B("Kein zu langer Satz in einer quelle-Einordnung.")
    B("")
    B("Die zu langen Saetze, je Gattung aufgeschluesselt:")
    for gattung in GATTUNGEN:
        eintrag = nach_gattung[gattung]
        if not eintrag["funde"]:
            continue
        B("   %s: %d" % (gattung, eintrag["lang"]))
        for anzahl, ort, satz in sorted(eintrag["funde"], reverse=True)[:6]:
            B("      %3d Woerter  %s" % (anzahl, ort))
            B("           %s" % satz[:150])
        if eintrag["lang"] > 6:
            B("      ... und %d weitere" % (eintrag["lang"] - 6))

    ## Gegenprobe des Satzzerlegers ############################################
    ##
    ## SEIT PAKET 5, SCHRITT 3, TEIL D.12. Der Zerleger ist in Schritt 1
    ## dieses Pakets berichtigt worden, in probe_alles.py und in satzzahl()
    ## (minispiele.rpy) gleichlautend. Die Abnahme verlangt den Beweis an
    ## fuenf Beispielen aus dem Bestand, und der wird hier bei jedem Lauf
    ## neu gefuehrt, statt einmal von Hand aufgeschrieben zu werden.
    ##
    ## Verglichen werden drei Zaehlungen: die alte Regel, die neue Regel
    ## dieser Werkbank und satzzahl() des Projekts. Die letzten beiden
    ## muessen uebereinstimmen; wo die erste abweicht, war frueher ein
    ## erfundener Befund.

    B.unterteil("Gegenprobe des Satzzerlegers (Teil D.12)")
    B("Die alte Regel entfernte JEDEN Punkt hinter einer Ziffer - auch den")
    B("hinter einer Jahreszahl. Zwei Saetze wurden zu einem, und der galt")
    B("dann als zu lang. Ein Punkt vor einem schliessenden Anfuehrungszeichen")
    B("beendete den Satz nicht. Beides ist berichtigt.")
    B("")
    B("Gesucht werden Stellen im echten Bestand, an denen sich der")
    B("Unterschied zeigt. 'alt' ist die Regel vor Paket 5, 'neu' diese")
    B("Werkbank, 'satzzahl' das Projekt. neu und satzzahl muessen gleich")
    B("sein - sonst zaehlen Probe 5 und Probe 8 verschieden.")
    B("")

    jahr_ende = re.compile(r"\d{4}\.\s")
    ordnungszahl = re.compile(r"(?<!\d)\d{1,2}\.\s")
    zitat_ende = re.compile(r"[.!?][\"“»]\s")

    faelle = [
        ("Jahreszahl beendet einen Satz", jahr_ende),
        ("Ordnungszahl beendet keinen", ordnungszahl),
        ("Punkt vor Anfuehrungszeichen", zitat_ende),
    ]

    beispiele = []
    for name, muster in faelle:
        getroffen = 0
        for gattung, ort, text in fein:
            if getroffen >= 2:
                break
            text = str(text)
            if not muster.search(text):
                continue
            alt = len(saetze_zerlegen_alt(text))
            neu = len(saetze_zerlegen(text))
            projekt = NS["satzzahl"](text) if callable(NS.get("satzzahl")) else -1
            if alt == neu and name != "Ordnungszahl beendet keinen":
                continue
            beispiele.append((name, ort, text, alt, neu, projekt))
            getroffen += 1
        if not getroffen:
            beispiele.append((name, "-", None, 0, 0, 0))

    uneins = 0
    for name, ort, text, alt, neu, projekt in beispiele:
        if text is None:
            B("   %-32s im Bestand nicht gefunden" % name)
            continue
        B("   %-32s %s" % (name, ort))
        B("      alt %d   neu %d   satzzahl %d%s" % (
            alt, neu, projekt,
            "   >> FEHLER << neu und satzzahl weichen ab"
            if neu != projekt else ""))
        if neu != projekt:
            uneins += 1
        B("      %s" % text[:170])
    if uneins:
        beanstandungen += uneins

    B("")
    B("Beispiele gefunden: %d. Werkbank und Projekt weichen ab: %d."
      % (len([b for b in beispiele if b[2] is not None]), uneins))

    return beanstandungen, alle_saetze


################################################################################
## 12b. Probe 9: Bewegungsprobe
################################################################################
##
## WARUM ES DIESE PROBE GIBT. Paket 7, Schritt 1 haengt jede Bewegung des
## Spiels an einen einzigen Schalter. Die Abnahme dazu lautet: "Keine
## Sekundenzahl steht mehr fest in einem Screen; alles laeuft ueber
## bewegungszeit()." Das ist ein Satz, den niemand nachlesen kann, ohne alle
## zehn .rpy-Dateien Zeile fuer Zeile durchzugehen - und was niemand nachliest,
## stimmt nach dem dritten Paket nicht mehr. Also wird es gemessen.
##
## SIE LIEST DEN QUELLTEXT ALS TEXT, und das ist hier die richtige Quelle:
## transform-Bloecke, at-Aufrufe und with-Anweisungen sind Ren'Py-Anweisungen
## und keine Python-Objekte. Im Namensraum der Werkbank stehen sie nicht.
##
## DIE DREI STUFEN DAGEGEN FRAGT SIE BEIM PROJEKT (Regel 11): bewegungszeit()
## und die drei Uebergaenge werden aufgerufen, nicht nachgerechnet. Auch die
## beiden Grenzen der Animationsregeln holt sie aus bewegung.rpy, statt sie
## ein zweites Mal hinzuschreiben.


## Die neun Vokabeln aus Paket 7, Schritt 1. Diese Liste ist die Vorgabe des
## Auftrags; die Vorgabewerte dahinter liest die Probe aus der Datei.
BEWEGUNGSVOKABULAR = [
    "karte_kommt",
    "karte_geht",
    "stempel_setzt",
    "wert_schwebt",
    "strich_waechst",
    "kalenderblatt",
    "umschlag_oeffnet",
    "zeile_taucht_auf",
    "knopf_hebt",
]

## Die drei Klassen der Animationsregeln (Entscheidung 17). Die ZAHLEN
## stehen nicht hier, sondern in bewegung.rpy; hier steht nur, welche
## Bewegung zu welcher Klasse gehoert.
##
##   Handgriff    (Vorgabe)  was zwischen der Spielerin und ihrem Klick liegt
##   Kapitel                 der Jahreswechsel
##   Rueckmeldung            was nur gesehen werden will und nichts aufhaelt
BEWEGUNG_KAPITELWECHSEL = ["kalenderblatt", "UEBERGANG_KAPITEL", "UEBERGANG_ENDE"]
BEWEGUNG_RUECKMELDUNG = ["wert_schwebt"]

BEWEGUNG_UEBERGAENGE = ["UEBERGANG_KARTE", "UEBERGANG_KAPITEL", "UEBERGANG_ENDE"]

## ATL-Anweisungen, die eine Dauer tragen. "timer" steht bewusst NICHT dabei:
## Das ist eine Standzeit im Bildschirm und keine Bewegung.
ATL_WARPER = [
    "linear", "ease", "easein", "easeout", "easeinout",
    "pause", "time", "delay",
]

TRANSFORM_MUSTER = re.compile(
    r"^transform\s+([A-Za-z_][A-Za-z_0-9]*)\s*(?:\(([^)]*)\))?\s*:")
ATL_ZEIT_MUSTER = re.compile(
    r"^\s*(" + "|".join(ATL_WARPER) + r")\s+([0-9]+(?:\.[0-9]+)?)\b")
AT_MUSTER = re.compile(r"\bat\s+([A-Za-z_][A-Za-z_0-9]*)\s*(\()?")
DAUER_MUSTER = re.compile(r"\bdauer\s*=\s*([0-9]+(?:\.[0-9]+)?)")
UEBERGANG_ALT_MUSTER = re.compile(
    r"\bwith\s+(dissolve|fade|pixellate|Dissolve\s*\(|Fade\s*\(|Pixellate\s*\(|"
    r"MoveTransition\s*\(|CropMove\s*\()")
CONFIG_UEBERGANG_MUSTER = re.compile(
    r"\bconfig\.([a-z_]*transition)\s*=\s*(.+)$")
UEBERGANG_BAU_MUSTER = re.compile(
    r"\b(Dissolve|Fade|Pixellate|MoveTransition|CropMove|ImageDissolve)\s*\(")


def nur_code(zeile):
    """Die Zeile ohne Zeichenketten und ohne Kommentar.

    Ohne das beanstandet die Bewegungsprobe ihre eigenen Warnungen: In
    bewegung.rpy steht "at karte_kommt" als abschreckendes Beispiel in einem
    Kommentar, und ein Ereignistext darf das Wort "Pause" enthalten, ohne
    dass daraus eine Bewegung wird. Zeichenketten werden nicht geloescht,
    sondern durch Leerzeichen ersetzt - so bleiben die Spaltennummern heil.
    """
    ergebnis = []
    art = None
    stelle = 0
    while stelle < len(zeile):
        zeichen = zeile[stelle]
        if art:
            if zeichen == "\\":
                ergebnis.append("  "[:min(2, len(zeile) - stelle)])
                stelle += 2
                continue
            if zeichen == art:
                art = None
                ergebnis.append(zeichen)
            else:
                ergebnis.append(" ")
            stelle += 1
            continue
        if zeichen in "\"'":
            art = zeichen
            ergebnis.append(zeichen)
            stelle += 1
            continue
        if zeichen == "#":
            break
        ergebnis.append(zeichen)
        stelle += 1
    return "".join(ergebnis)


def rpy_dateien(spielordner):
    """Alle .rpy-Dateien im Spielordner, alphabetisch.

    Nicht die LESEFOLGE: Die zaehlt nur die Dateien mit Python-Bloecken. Eine
    Bewegung kann in jeder Datei stehen, auch in einer, die morgen dazukommt.
    """
    if not os.path.isdir(spielordner):
        return []
    return sorted(name for name in os.listdir(spielordner)
                  if name.endswith(".rpy"))


def zeilen_lesen(spielordner, dateiname):
    pfad = os.path.join(spielordner, dateiname)
    text = io.open(pfad, encoding="utf-8").read().replace("\r\n", "\n")
    return text.split("\n")


def transforms_sammeln(spielordner, dateien):
    """Jeder transform des Projekts mit Datei, Zeile und Parameterliste."""
    gefunden = collections.OrderedDict()
    for dateiname in dateien:
        for nummer, zeile in enumerate(zeilen_lesen(spielordner, dateiname), 1):
            treffer = TRANSFORM_MUSTER.match(nur_code(zeile))
            if not treffer:
                continue
            parameter = treffer.group(2) or ""
            vorgabe = DAUER_MUSTER.search(parameter)
            gefunden[treffer.group(1)] = {
                "datei": dateiname,
                "zeile": nummer,
                "parameter": parameter,
                "hat_dauer": "dauer" in parameter,
                "vorgabe": float(vorgabe.group(1)) if vorgabe else None,
            }
    return gefunden


def probe_bewegung(NS, B, spielordner):
    beanstandungen = 0
    geprueft = 0

    B.titel("PROBE 9  BEWEGUNGSPROBE")
    B("Seit Paket 7, Schritt 1 holt jede Bewegung ihre Dauer aus")
    B("bewegungszeit(). Diese Probe misst, ob das noch stimmt.")
    B("Sie liest den Quelltext als Text - transforms und at-Aufrufe sind")
    B("Ren'Py-Anweisungen und stehen in keinem Namensraum. Die drei Stufen")
    B("und die beiden Grenzen fragt sie beim Projekt.")

    dateien = rpy_dateien(spielordner)
    if not dateien:
        B("")
        B(">> FEHLER << Im Spielordner liegt keine .rpy-Datei.")
        return 1, 0

    transforms = transforms_sammeln(spielordner, dateien)

    ## --------------------------------------------------------------- a
    B.unterteil("a) Die neun Vokabeln aus dem Auftrag")
    B("%-20s %-16s %8s %8s   %s" % (
        "Vokabel", "Datei", "Zeile", "Vorgabe", "Zustand"))

    for name in BEWEGUNGSVOKABULAR:
        geprueft += 1
        eintrag = transforms.get(name)
        if eintrag is None:
            B("%-20s %-16s %8s %8s   >> FEHLT <<" % (name, "-", "-", "-"))
            beanstandungen += 1
            continue
        if not eintrag["hat_dauer"]:
            zustand = ">> OHNE PARAMETER dauer <<"
            beanstandungen += 1
        else:
            zustand = "in Ordnung"
        B("%-20s %-16s %8d %8s   %s" % (
            name, eintrag["datei"], eintrag["zeile"],
            ("%.2f" % eintrag["vorgabe"]) if eintrag["vorgabe"] is not None else "-",
            zustand))

    ## --------------------------------------------------------------- b
    ## Hier FRAGT die Probe das Projekt. Sie stellt die Stufe um und ruft
    ## bewegungszeit() auf, statt den Anteil ein zweites Mal auszurechnen.
    B.unterteil("b) Die drei Stufen - gefragt, nicht nachgerechnet")

    stufen_fehler = 0
    zeitfunktion = NS.get("bewegungszeit")
    stufen = NS.get("BEWEGUNG_ANTEIL")

    if not callable(zeitfunktion) or isinstance(zeitfunktion, Attrappe) \
            or not isinstance(stufen, dict):
        B(">> FEHLER << bewegungszeit() oder BEWEGUNG_ANTEIL fehlt.")
        B("             bewegung.rpy ist nicht gelaufen; b, c und f entfallen.")
        beanstandungen += 1
        stufen_fehler = 1
        stufen = {}

    vorher = getattr(NS["persistent"], "bewegung", None)
    messungen = []
    if not stufen_fehler:
        B("%-12s %10s %10s %10s   %s" % (
            "Stufe", "Anteil", "aus 0.50", "erwartet", "Zustand"))
        for stufe in sorted(stufen, key=lambda s: -stufen[s]):
            geprueft += 1
            NS["persistent"].bewegung = stufe
            gemessen = zeitfunktion(0.50)
            erwartet = round(0.50 * stufen[stufe], 3)
            stimmt = abs(float(gemessen) - erwartet) < 0.0005
            if not stimmt:
                beanstandungen += 1
            messungen.append((stufe, gemessen))
            B("%-12s %10.2f %10.3f %10.3f   %s" % (
                stufe, stufen[stufe], gemessen, erwartet,
                "stimmt" if stimmt else ">> WEICHT AB <<"))

        ## Eine unbekannte Stufe darf nicht durchschlagen. Eine persistent-
        ## Datei aus einer aelteren Fassung kann alles enthalten.
        geprueft += 1
        NS["persistent"].bewegung = "unsinn"
        rueckfall = zeitfunktion(0.50)
        if abs(float(rueckfall) - 0.50) < 0.0005:
            B("Unbekannte Stufe faellt auf 'voll' zurueck.   stimmt")
        else:
            B(">> FEHLER << Unbekannte Stufe liefert %s statt 0.50." % rueckfall)
            beanstandungen += 1

    ## --------------------------------------------------------------- c
    B.unterteil("c) Die drei Uebergaenge")
    if not stufen_fehler:
        for name in BEWEGUNG_UEBERGAENGE:
            geprueft += 1
            funktion = NS.get(name)
            if not callable(funktion) or isinstance(funktion, Attrappe):
                B("%-20s >> FEHLT oder ist keine Funktion <<" % name)
                beanstandungen += 1
                continue
            NS["persistent"].bewegung = "voll"
            voll = funktion()
            NS["persistent"].bewegung = "aus"
            aus = funktion()
            if voll is None:
                B("%-20s >> LIEFERT BEI 'voll' KEINEN UEBERGANG <<" % name)
                beanstandungen += 1
            elif aus is not None:
                B("%-20s >> LIEFERT BEI 'aus' EINEN UEBERGANG <<" % name)
                beanstandungen += 1
            else:
                B("%-20s bei 'voll' ein Uebergang, bei 'aus' None.   stimmt"
                  % name)

    NS["persistent"].bewegung = vorher

    ## --------------------------------------------------------------- d
    B.unterteil("d) Feste Sekundenzahlen in Bewegungen")
    B("Beanstandet wird jede ATL-Anweisung mit einer Zahl statt eines")
    B("Ausdrucks: linear, ease, easein, easeout, easeinout, pause, time,")
    B("delay. Zeichenketten und Kommentare sind vorher entfernt.")

    feste_zahlen = []
    at_aufrufe = 0
    at_fehler = []
    alte_uebergaenge = []
    config_uebergaenge = collections.OrderedDict()

    for dateiname in dateien:
        for nummer, zeile in enumerate(zeilen_lesen(spielordner, dateiname), 1):
            code = nur_code(zeile)

            treffer = ATL_ZEIT_MUSTER.match(code)
            if treffer:
                geprueft += 1
                feste_zahlen.append((dateiname, nummer, code.strip()))

            for name, klammer in AT_MUSTER.findall(code):
                eintrag = transforms.get(name)
                if eintrag is None or not eintrag["hat_dauer"]:
                    continue
                at_aufrufe += 1
                geprueft += 1
                if not klammer:
                    at_fehler.append((dateiname, nummer, name, "ohne Klammern"))
                elif "bewegungszeit(" not in code:
                    at_fehler.append((dateiname, nummer, name,
                                      "ohne bewegungszeit()"))

            treffer = UEBERGANG_ALT_MUSTER.search(code)
            if treffer:
                geprueft += 1
                alte_uebergaenge.append((dateiname, nummer, code.strip()))

            ## Jede Zuweisung wird vermerkt, nicht nur die mit einem
            ## Uebergang darin: Die Zuweisung in bewegung.rpy lautet
            ## "config.enter_transition = UEBERGANG_KARTE()" und traegt
            ## selbst keinen Konstruktor. Genau sie ist der Nachweis.
            treffer = CONFIG_UEBERGANG_MUSTER.search(code)
            if treffer:
                eintrag = config_uebergaenge.setdefault(treffer.group(1), [])
                eintrag.append((dateiname,
                                bool(UEBERGANG_BAU_MUSTER.search(treffer.group(2)))))

    if feste_zahlen:
        for dateiname, nummer, text in feste_zahlen:
            B("   >> %s:%d  %s" % (dateiname, nummer, text[:60]))
        beanstandungen += len(feste_zahlen)
    else:
        B("Keine. Alle %d ATL-Anweisungen im Projekt tragen einen Ausdruck."
          % len([1 for d in dateien
                 for z in zeilen_lesen(spielordner, d)
                 if re.match(r"^\s*(" + "|".join(ATL_WARPER) + r")\s+",
                             nur_code(z))]))

    ## --------------------------------------------------------------- e
    B.unterteil("e) at-Aufrufe, die am Schalter vorbeigehen")
    B("Ein transform mit Parameter dauer MUSS mit Klammern und mit")
    B("bewegungszeit() aufgerufen werden. 'at karte_kommt' ohne Klammern")
    B("nimmt die Vorgabe aus der Datei und hoert auf keinen Schalter.")
    B("Geprueft: %d Aufrufe." % at_aufrufe)
    if at_fehler:
        for dateiname, nummer, name, grund in at_fehler:
            B("   >> %s:%d  at %s  %s" % (dateiname, nummer, name, grund))
        beanstandungen += len(at_fehler)
    else:
        B("Keine Beanstandung.")

    ## --------------------------------------------------------------- f
    B.unterteil("f) Uebergaenge: nur die drei benannten")
    if alte_uebergaenge:
        for dateiname, nummer, text in alte_uebergaenge:
            B("   >> %s:%d  %s" % (dateiname, nummer, text[:60]))
        beanstandungen += len(alte_uebergaenge)
    else:
        B("Kein 'with dissolve' und kein 'with Dissolve(...)' im Ablauf.")

    B("")
    B("Die Menue-Uebergaenge sind Ren'Py-Einstellungen und werden einmal")
    B("gesetzt. Wer sie in options.rpy festlegt, muss sie in bewegung.rpy")
    B("nachziehen - sonst blendet das Spielmenue auch bei 'aus' noch auf.")
    for name, eintraege in config_uebergaenge.items():
        geprueft += 1
        aus_bewegung = any(datei == "bewegung.rpy" for datei, _fest in eintraege)
        fest_woanders = sorted(set(datei for datei, fest in eintraege
                                   if fest and datei != "bewegung.rpy"))
        alle = ", ".join(sorted(set(datei for datei, _fest in eintraege)))
        if fest_woanders and not aus_bewegung:
            B("   >> config.%-24s fest in %s, nicht nachgezogen"
              % (name, ", ".join(fest_woanders)))
            beanstandungen += 1
        else:
            B("   config.%-24s %s" % (name, alle))

    ## --------------------------------------------------------------- g
    B.unterteil("g) Dauern gegen die Animationsregeln")
    grenze = NS.get("BEWEGUNG_HOECHSTDAUER")
    grenze_kapitel = NS.get("BEWEGUNG_HOECHSTDAUER_KAPITEL")
    grenze_rueckmeldung = NS.get("BEWEGUNG_HOECHSTDAUER_RUECKMELDUNG")
    uebergangsdauer = NS.get("UEBERGANG_DAUER")

    def klasse_von(name):
        """Zu welcher der drei Klassen aus Entscheidung 17 gehoert sie?"""
        if name in BEWEGUNG_KAPITELWECHSEL:
            return "Kapitel", grenze_kapitel
        if name in BEWEGUNG_RUECKMELDUNG:
            return "Rueckmeldung", grenze_rueckmeldung
        return "Handgriff", grenze

    if not isinstance(grenze, float) or not isinstance(grenze_kapitel, float) \
            or not isinstance(grenze_rueckmeldung, float):
        B(">> FEHLER << Die drei Grenzen stehen nicht in bewegung.rpy.")
        beanstandungen += 1
    else:
        B("Drei Klassen (Entscheidung 17): Handgriff hoechstens %.2f Sekunden,"
          % grenze)
        B("Kapitelwechsel %.2f, Rueckmeldung ohne Eingabesperre %.2f."
          % (grenze_kapitel, grenze_rueckmeldung))
        B("Gemessen wird die Vorgabe, nicht der Aufruf - die Stufen 'sparsam'")
        B("und 'aus' kuerzen nur, sie verlaengern nie.")
        B("%-20s %-14s %10s %10s   %s" % (
            "Bewegung", "Klasse", "Vorgabe", "Grenze", "Zustand"))

        def dauer_messen(name, wert):
            klasse, hoechst = klasse_von(name)
            zu_lang = wert > hoechst + 0.0005
            B("%-20s %-14s %10.2f %10.2f   %s" % (
                name, klasse, wert, hoechst,
                ">> UEBER DER GRENZE <<" if zu_lang else "in Ordnung"))
            return 1 if zu_lang else 0

        for name in BEWEGUNGSVOKABULAR:
            eintrag = transforms.get(name)
            if eintrag is None or eintrag["vorgabe"] is None:
                continue
            geprueft += 1
            beanstandungen += dauer_messen(name, eintrag["vorgabe"])

        ## Die vorhandenen Bewegungen aus frueheren Paketen gehen hier
        ## dieselbe Strecke. Sie sind kein Vokabular, aber sie bewegen sich.
        for name, eintrag in transforms.items():
            if name in BEWEGUNGSVOKABULAR or eintrag["vorgabe"] is None:
                continue
            geprueft += 1
            beanstandungen += dauer_messen(name, eintrag["vorgabe"])

        if isinstance(uebergangsdauer, dict):
            for name in BEWEGUNG_UEBERGAENGE:
                schluessel = name.replace("UEBERGANG_", "").lower()
                wert = uebergangsdauer.get(schluessel)
                if wert is None:
                    continue
                geprueft += 1
                gesamt = sum(wert) if isinstance(wert, (tuple, list)) else wert
                beanstandungen += dauer_messen(name, gesamt)

    ## --------------------------------------------------------------- h
    B.unterteil("h) Bewegungen ohne Dauer")
    B("Ein transform ohne Zeitschritt kann am Schalter nicht vorbeilaufen.")
    B("Er steht hier, damit niemand ihn fuer eine Luecke haelt.")
    ohne_dauer = [(name, e) for name, e in transforms.items()
                  if not e["hat_dauer"]]
    for name, eintrag in ohne_dauer:
        B("   %-22s %s:%d" % (name, eintrag["datei"], eintrag["zeile"]))
    if not ohne_dauer:
        B("   Keiner.")

    B("")
    B("%d transforms im Projekt, davon %d aus dem Vokabular des Auftrags."
      % (len(transforms), len([n for n in BEWEGUNGSVOKABULAR if n in transforms])))

    return beanstandungen, geprueft


################################################################################
## 12bb. Probe 10: Handgriffe
################################################################################
##
## WARUM ES DIESE PROBE GIBT. Zwei Gruende.
##
## ERSTENS loest sie pruefen.py ab (Entscheidung 20). Das alte Werkzeug hat
## jede Einlage mit vielen Eingaben durchgerechnet und die Spannweite der
## Wertaenderungen gemeldet - eine nuetzliche Zahl, die im Werkbank-Bericht
## fehlte. Es laeuft nicht mehr und baute die Spiellogik mit eigenen
## Platzhaltern nach. Hier wird dieselbe Frage gestellt, aber an den echten
## Namensraum.
##
## ZWEITENS traegt sie den Nachweis aus Paket 7, Schritt 2, Teil B.3, und
## zwar dauerhaft: "Acht Striche" darf keine Verteilung haben, die alle
## anderen erreicht oder schlaegt. Am 5. September gab es genau eine - vier
## Teile fuer sich, je zwei fuer Kind und Nachbarn, nichts in den Vorrat -,
## und damit hatte die Einlage eine richtige Antwort. Das ist kein Fehler,
## den man einmal behebt und danach vergisst: Jede spaetere Aenderung an
## portionen_auswerten() kann ihn zurueckbringen. Deshalb wird er gemessen.


def verteilungen_aufzaehlen(gesamt, faecher):
    """Alle Arten, 'gesamt' gleiche Teile auf 'faecher' Empfaenger zu legen.

    Bei acht Teilen und vier Empfaengern sind das 165 - wenig genug, um sie
    vollstaendig durchzurechnen, statt zu stichproben.
    """
    for schnitt in itertools.combinations(range(gesamt + faecher - 1), faecher - 1):
        vorher = -1
        teile = []
        for stelle in schnitt:
            teile.append(stelle - vorher - 1)
            vorher = stelle
        teile.append(gesamt + faecher - 2 - vorher)
        yield tuple(teile)


def nutzen_vektor(NS, aenderungen):
    """Die vier Werte, alle in der Richtung 'groesser ist besser'.

    WERT_HOCH_IST_GUT kommt aus dem Projekt. Ohne diese Drehung waere ein
    Vergleich sinnlos: Bei Hunger und Verdacht ist weniger besser.
    """
    hoch_gut = NS["WERT_HOCH_IST_GUT"]
    return tuple(
        (aenderungen.get(wert, 0) if hoch_gut[wert] else -aenderungen.get(wert, 0))
        for wert in NS["WERTE_REIHENFOLGE"])


def dominiert(links, rechts):
    """links ist ueberall mindestens so gut und irgendwo echt besser."""
    return (all(a >= b for a, b in zip(links, rechts))
            and any(a > b for a, b in zip(links, rechts)))


def screen_bloecke(spielordner, dateien):
    """Jeder screen-Block mit Datei, Zeile und seinem Rumpf.

    Gebraucht fuer die Winkelprobe: Ein Wuerfelwurf im Bildschirm faellt
    bei jedem Neuzeichnen neu, und das Ergebnis zittert.
    """
    gefunden = []
    muster = re.compile(r"^screen\s+([A-Za-z_][A-Za-z_0-9]*)\s*[\(:]")
    for dateiname in dateien:
        zeilen = zeilen_lesen(spielordner, dateiname)
        stelle = 0
        while stelle < len(zeilen):
            treffer = muster.match(zeilen[stelle])
            if not treffer:
                stelle += 1
                continue
            rumpf = []
            lauf = stelle + 1
            while lauf < len(zeilen):
                zeile = zeilen[lauf]
                if zeile.strip() and not zeile.startswith((" ", "\t")):
                    break
                rumpf.append((lauf + 1, zeile))
                lauf += 1
            gefunden.append({
                "name": treffer.group(1),
                "datei": dateiname,
                "zeile": stelle + 1,
                "rumpf": rumpf,
            })
            stelle = lauf
    return gefunden


## Wie viele Durchgaenge der Vergleich aus Teil e spielt. Deutlich weniger
## als die Wertetafel: Gefragt ist nicht eine Quote auf das Zehntel, sondern
## ob ueberhaupt jemand durchkommt. Bei --schnell entsprechend weniger.
VERGLEICHSDURCHGAENGE = 200


def probe_handgriffe(NS, B, spielordner, vergleichsdurchgaenge=VERGLEICHSDURCHGAENGE):
    beanstandungen = 0
    geprueft = 0

    B.titel("PROBE 10  HANDGRIFFE")
    B("Sie loest pruefen.py ab (Entscheidung 20) und traegt den Nachweis")
    B("aus Paket 7, Schritt 2, Teil B.3. Gerechnet wird mit den Funktionen")
    B("des Projekts, nicht mit einem Nachbau.")

    einlagen = NS.get("EINLAGEN") or []
    probewerte = NS.get("EINLAGE_PROBEWERTE") or {}
    auswerten = NS.get("EINLAGE_AUSWERTEN") or {}
    hoechstwirkung = NS.get("EINLAGE_HOECHSTWIRKUNG")

    ## --------------------------------------------------------------- a
    B.unterteil("a) Spannweite der Wertaenderungen je Einlage")
    B("Jede Einlage wird mit allen Probewerten durchgerechnet. Gemeldet")
    B("wird die Spanne VOR der Begrenzung; EINLAGE_HOECHSTWIRKUNG = %s"
      % hoechstwirkung)
    B("kappt danach. Wer regelmaessig an die Kappung stoesst, hat die")
    B("Einlage zu schwer gebaut - die Kappung ist ein Netz, kein Werkzeug.")
    B("%-18s %6s  %s" % ("Einlage", "Faelle", "Spanne je Wert"))

    gekappt = []
    for vorlage in einlagen:
        kennung = vorlage.kennung
        eingaben = probewerte.get(kennung) or []
        funktion = auswerten.get(kennung)
        if not eingaben or not callable(funktion):
            B("%-18s %6s  >> KEINE PROBEWERTE ODER KEINE AUSWERTUNG <<"
              % (kennung, "-"))
            beanstandungen += 1
            continue

        spanne = collections.OrderedDict(
            (wert, [0, 0]) for wert in NS["WERTE_REIHENFOLGE"])
        faelle = 0
        for eingabe in eingaben:
            try:
                NS["einlage_vorbereiten"](kennung)
                ergebnis = funktion(eingabe)
            except Exception as fehler:
                B("%-18s %6d  >> BRICHT AB: %s <<" % (kennung, faelle, fehler))
                beanstandungen += 1
                break
            faelle += 1
            geprueft += 1
            for wert, betrag in (ergebnis.get("aenderungen") or {}).items():
                if wert not in spanne:
                    continue
                spanne[wert][0] = min(spanne[wert][0], betrag)
                spanne[wert][1] = max(spanne[wert][1], betrag)
        else:
            teile = []
            for wert, (klein, gross) in spanne.items():
                if klein == 0 and gross == 0:
                    continue
                teile.append("%s %+d..%+d" % (wert[:4], klein, gross))
                if isinstance(hoechstwirkung, int) and \
                        max(abs(klein), abs(gross)) > hoechstwirkung:
                    gekappt.append((kennung, wert, klein, gross))
            B("%-18s %6d  %s" % (kennung, faelle,
                                 "   ".join(teile) if teile else "keine"))

    if gekappt:
        B("")
        for kennung, wert, klein, gross in gekappt:
            B("   >> %s: %s reicht von %+d bis %+d und wird gekappt."
              % (kennung, wert, klein, gross))
        beanstandungen += len(gekappt)
    else:
        B("")
        B("Keine Einlage stoesst an EINLAGE_HOECHSTWIRKUNG.")

    ## --------------------------------------------------------------- b
    B.unterteil("b) Acht Striche: gibt es eine Verteilung, die alle schlaegt?")
    B("Alle Verteilungen von acht Teilen auf vier Empfaenger, in jedem")
    B("Pfad und in beiden Schimmelfaellen. Beanstandet wird jede")
    B("Verteilung, die in ALLEN vier Werten mindestens so gut ist wie")
    B("jede andere - dann gaebe es eine richtige Antwort, und die Einlage")
    B("waere keine Entscheidung mehr (Regel 5).")

    gesamt = NS.get("PORTIONEN_GESAMT")
    portionen_auswerten = NS.get("portionen_auswerten")
    empfaenger_zahl = len(NS.get("PORTIONEN_EMPFAENGER") or [])

    if not isinstance(gesamt, int) or not callable(portionen_auswerten) \
            or empfaenger_zahl < 2:
        B(">> FEHLER << Acht Striche laesst sich nicht rechnen.")
        beanstandungen += 1
    else:
        pfad_vorher = NS.get("aktueller_pfad")
        B("%-8s %-9s %8s %8s %10s   %s" % (
            "Pfad", "Schimmel", "Vertei-", "Pareto-", "Allherr-", "Zustand"))
        B("%-8s %-9s %8s %8s %10s" % ("", "", "lungen", "Front", "scher"))

        for pfad in NS["PFAD_REIHENFOLGE"]:
            for schimmel in (False, True):
                NS["aktueller_pfad"] = pfad
                NS["einlage_vorbereiten"]("portionen")
                NS["einlage_lage"]["schimmel"] = schimmel

                ergebnisse = collections.OrderedDict()
                for teilung in verteilungen_aufzaehlen(gesamt, empfaenger_zahl):
                    ergebnisse[teilung] = nutzen_vektor(
                        NS, portionen_auswerten(teilung).get("aenderungen") or {})
                    geprueft += 1

                front = [t for t in ergebnisse
                         if not any(dominiert(ergebnisse[a], ergebnisse[t])
                                    for a in ergebnisse if a != t)]
                allherrscher = [
                    t for t in ergebnisse
                    if all(all(x >= y for x, y in zip(ergebnisse[t], ergebnisse[a]))
                           for a in ergebnisse)]

                if allherrscher:
                    beanstandungen += len(allherrscher)
                B("%-8s %-9s %8d %8d %10d   %s" % (
                    pfad, "ja" if schimmel else "nein", len(ergebnisse),
                    len(front), len(allherrscher),
                    ">> RICHTIGE ANTWORT <<" if allherrscher else "in Ordnung"))
                for teilung in allherrscher:
                    B("      >> %s schlaegt oder erreicht jede andere." % (teilung,))

        ## Die drei Ecken der Front zum Nachlesen im Unterricht.
        NS["aktueller_pfad"] = pfad_vorher or NS["PFAD_REIHENFOLGE"][0]
        NS["einlage_vorbereiten"]("portionen")
        NS["einlage_lage"]["schimmel"] = False
        ergebnisse = collections.OrderedDict()
        for teilung in verteilungen_aufzaehlen(gesamt, empfaenger_zahl):
            ergebnisse[teilung] = nutzen_vektor(
                NS, portionen_auswerten(teilung).get("aenderungen") or {})
        front = [t for t in ergebnisse
                 if not any(dominiert(ergebnisse[a], ergebnisse[t])
                            for a in ergebnisse if a != t)]
        namen = [e["kennung"] for e in NS["PORTIONEN_EMPFAENGER"]]
        B("")
        B("Die Pareto-Front im Pfad %s ohne Schimmel - keine dieser"
          % NS["aktueller_pfad"])
        B("Verteilungen ist einer anderen in allen vier Werten unterlegen:")
        B("   %s   %s" % ("  ".join("%-9s" % n for n in namen),
                          "  ".join("%-6s" % w[:6] for w in NS["WERTE_REIHENFOLGE"])))
        for teilung in sorted(front, key=lambda t: (-sum(ergebnisse[t]), t))[:12]:
            B("   %s   %s" % (
                "  ".join("%-9d" % a for a in teilung),
                "  ".join("%-+6d" % w for w in ergebnisse[teilung])))
        if len(front) > 12:
            B("   ... und %d weitere." % (len(front) - 12))

    ## --------------------------------------------------------------- c
    B.unterteil("c) Die Zustandssaetze und ihre Schwellen")
    B("Der Bildschirm zeigt zu jeder Zuteilung einen Satz, die Auswertung")
    B("bewegt dazu die Werte. Beide fragen portionen_stufe(). Stuenden die")
    B("Schwellen zweimal da, liefen sie auseinander, und der Bildschirm")
    B("verspraeche etwas, das die Auswertung nicht einloest.")

    stufe_von = NS.get("portionen_stufe")
    satz_von = NS.get("portionen_satz")
    schwellen = NS.get("PORTIONEN_SCHWELLEN")
    zustand = NS.get("PORTIONEN_ZUSTAND")

    if not callable(stufe_von) or not callable(satz_von) \
            or not isinstance(schwellen, dict) or not isinstance(zustand, dict):
        B(">> FEHLER << portionen_stufe(), portionen_satz(),")
        B("             PORTIONEN_SCHWELLEN oder PORTIONEN_ZUSTAND fehlt.")
        beanstandungen += 1
    else:
        B("%-12s %8s   %s" % ("Empfaenger", "Stufen", "Zuteilung 0 bis %d" % gesamt))
        for kennung in schwellen:
            geprueft += 1
            stufen = [stufe_von(kennung, anteil) for anteil in range(gesamt + 1)]
            fehlend = [s for _schwelle, s in schwellen[kennung]
                       if s not in (zustand.get(kennung) or {})]
            leer = [anteil for anteil in range(gesamt + 1)
                    if not satz_von(kennung, anteil)]
            hinweis = "in Ordnung"
            if fehlend:
                hinweis = ">> OHNE SATZ: " + ", ".join(fehlend) + " <<"
                beanstandungen += 1
            elif leer:
                hinweis = ">> LEERER SATZ bei %s <<" % leer
                beanstandungen += 1
            B("%-12s %8d   %s" % (kennung, len(set(stufen)), " ".join(stufen)))
            B("             %s" % hinweis)

        ## Steht eine Schwelle ein zweites Mal in der Auswertung?
        geprueft += 1
        quelle = zeilen_lesen(spielordner, "minispiele.rpy")
        anfang = None
        for nummer, zeile in enumerate(quelle):
            if zeile.strip().startswith("def portionen_auswerten"):
                anfang = nummer
                break
        zweitfassung = []
        if anfang is not None:
            muster = re.compile(
                r"\b(selbst|fuer_kind|fuer_naechste|vorrat)\s*(>=|<=|==|!=|<|>)\s*\d")
            for nummer in range(anfang, len(quelle)):
                zeile = quelle[nummer]
                if nummer > anfang and zeile.strip() and \
                        not zeile.startswith((" ", "\t")):
                    break
                if zeile.strip().startswith("def ") and nummer > anfang:
                    break
                treffer = muster.search(nur_code(zeile))
                if treffer:
                    zweitfassung.append((nummer + 1, zeile.strip()))
        if zweitfassung:
            B("")
            for nummer, zeile in zweitfassung:
                B("   >> minispiele.rpy:%d  %s" % (nummer, zeile[:64]))
            B("   Diese Zeilen formulieren eine Schwelle ein zweites Mal.")
            beanstandungen += len(zweitfassung)
        else:
            B("")
            B("portionen_auswerten() vergleicht keine Zuteilung mehr mit einer")
            B("Zahl. Alle Schwellen kommen aus PORTIONEN_SCHWELLEN.")

    ## --------------------------------------------------------------- d
    B.unterteil("d) Wuerfelwuerfe in Bildschirmen")
    B("Ein Screen wird bei jeder Mausbewegung neu gebaut. Ein Winkel, eine")
    B("Farbe oder eine Reihenfolge, die dort gewuerfelt wird, faellt bei")
    B("jedem Bild neu - und das Bild zittert. Gewuerfelt wird in der")
    B("Vorbereitung, das Ergebnis liegt in einlage_lage.")

    wuerfel = re.compile(r"\brenpy\.random\b|\brandom\.\w+\s*\(|\bshuffle\s*\(")
    treffer_gesamt = []
    for block in screen_bloecke(spielordner, rpy_dateien(spielordner)):
        geprueft += 1
        for nummer, zeile in block["rumpf"]:
            if wuerfel.search(nur_code(zeile)):
                treffer_gesamt.append((block["datei"], nummer,
                                       block["name"], zeile.strip()))
    if treffer_gesamt:
        for datei, nummer, name, zeile in treffer_gesamt:
            B("   >> %s:%d  in screen %s: %s" % (datei, nummer, name, zeile[:52]))
        beanstandungen += len(treffer_gesamt)
    else:
        B("Kein Bildschirm wuerfelt. Geprueft: %d Bildschirme."
          % len(screen_bloecke(spielordner, rpy_dateien(spielordner))))

    ## Und die Winkel des Rotstifts liegen wirklich in der Lage.
    geprueft += 1
    try:
        NS["einlage_vorbereiten"]("rotstift")
        lage = NS["einlage_lage"]
        winkel_a = (tuple(lage.get("balkenwinkel") or ()), lage.get("stempelwinkel"))
        grenzen = NS.get("BALKEN_WINKEL") or (0.4, 1.2)
        stempelgrenzen = NS.get("STEMPEL_WINKEL") or (6.0, 8.0)
        daneben = [w for w in winkel_a[0]
                   if not (grenzen[0] <= abs(w) <= grenzen[1])]
        B("")
        B("Rotstift: %d Balkenwinkel zwischen %.1f und %.1f Grad, Stempel %.2f"
          % (len(winkel_a[0]), grenzen[0], grenzen[1], winkel_a[1] or 0.0))
        if daneben:
            B("   >> %d Winkel liegen ausserhalb der Grenzen: %s" % (len(daneben), daneben))
            beanstandungen += 1
        elif not winkel_a[0]:
            B("   >> Es liegen keine Balkenwinkel in einlage_lage.")
            beanstandungen += 1
        elif not (stempelgrenzen[0] <= (winkel_a[1] or 0.0) <= stempelgrenzen[1]):
            B("   >> Der Stempelwinkel liegt ausserhalb von %s." % (stempelgrenzen,))
            beanstandungen += 1
        else:
            B("   Alle Winkel liegen in ihren Grenzen und stehen in einlage_lage.")
    except Exception as fehler:
        B("   >> Die Vorbereitung des Rotstifts bricht ab: %s" % fehler)
        beanstandungen += 1

    ## --------------------------------------------------------------- e
    ## DER NACHWEIS AUS PAKET 7, SCHRITT 3, TEIL A.2.
    ##
    ## Der Auftrag verlangt: "WEISE NACH, dass dadurch kein Ende
    ## unausweichlich wird." Das ist keine Frage, die sich am Quelltext
    ## beantworten laesst - ohne_mantel erhoeht die Ziehchance von vier
    ## Karten, und was daraus wird, entscheidet sich erst im Durchgang.
    ## Also wird gespielt: dieselbe Lage zweimal, einmal mit allen sieben
    ## Merkmalen und einmal ohne, und die Quoten stehen nebeneinander.
    ##
    ## BEANSTANDET WIRD 0,0 PROZENT. Das ist keine erfundene Schwelle,
    ## sondern der Satz aus Entscheidung 11: "In jeder der sechs Lagen
    ## erreicht ein messbarer Anteil das Jahr 1919. 0,0 Prozent ist kein
    ## Ergebnis, sondern ein toter Pfad." Der Abstand zur Vergleichsgruppe
    ## wird gemessen und gedruckt, aber nicht beanstandet: Wo die Grenze
    ## zwischen "spuerbar" und "zu viel" liegt, ist eine Frage an Dominik
    ## und keine, die eine Probe entscheiden darf.

    B.unterteil("e) Wird ein Ende unausweichlich, wenn alles im Graben liegt?")

    stuecke = NS.get("TORNISTER_STUECKE") or []
    sieben = ["ohne_" + s["kennung"] for s in stuecke
              if s.get("kennung") != "fremdes"]

    if not sieben or not callable(NS.get("merkmal_setzen")):
        B(">> FEHLER << TORNISTER_STUECKE oder merkmal_setzen fehlt.")
        beanstandungen += 1
    else:
        fehlend = [m for m in sieben if m not in (NS.get("MERKMAL_REGISTER") or {})]
        if fehlend:
            B("   >> Nicht im Register: %s" % ", ".join(fehlend))
            beanstandungen += len(fehlend)

        B("Gespielt werden %d Durchgaenge je Lage und Gruppe, Strategie"
          % vergleichsdurchgaenge)
        B("'zufall'. Die sieben Merkmale sind: %s." % ", ".join(sieben))
        B("%-8s %-7s %10s %10s %12s   %s" % (
            "Pfad", "Verlauf", "ohne %", "mit %", "Abstand", "Zustand"))

        buch = Rueckfallbuch()
        umgebung = {"pfad_fehler": [], "brief_fehler": [], "notbremse": []}
        werkbank = Werkbank(NS, buch, umgebung)
        werkbank.strategie = "zufall"

        for pfad in pfade_erreichbar(NS):
            for modus in ["kurz", "lang"]:
                quoten = {}
                for marke, belastung in (("ohne", None), ("mit", sieben)):
                    durch = 0
                    for _ in range(vergleichsdurchgaenge):
                        spur = werkbank.durchgang(pfad, modus, vorbelastung=belastung)
                        geprueft += 1
                        if spur.ende in (None, "", "ende_ueberlebt"):
                            durch += 1
                        elif str(spur.ende).startswith("ende_ueberlebt"):
                            durch += 1
                    quoten[marke] = prozent(durch, vergleichsdurchgaenge)

                abstand = quoten["mit"] - quoten["ohne"]
                tot = quoten["mit"] <= 0.0
                if tot:
                    beanstandungen += 1
                B("%-8s %-7s %10.1f %10.1f %+12.1f   %s" % (
                    pfad, modus, quoten["ohne"], quoten["mit"], abstand,
                    ">> TOTER PFAD <<" if tot else "in Ordnung"))

        B("")
        B("Ein negativer Abstand heisst: Wer alles weggeworfen hat, kommt")
        B("seltener durch. Genau das soll die Vorbelastung bewirken. Ein")
        B("Ende ist erst dann unausweichlich, wenn in der Spalte 'mit' eine")
        B("Null steht - und dann steht dort TOTER PFAD.")

    return beanstandungen, geprueft


################################################################################
## 12c. Der Selbsttest der Werkbank
################################################################################
##
## SEIT PAKET 5, SCHRITT 3, TEIL D.15. probe_alles.py ist inzwischen das
## Mass fuer alles - und niemand prueft das Mass. Zweimal in einer einzigen
## Sitzung hat diese Werkbank gruen gemeldet, wo nichts gemessen war: das
## Schuldbuch, das nie schrieb, und die Proben 3 und 4, die nach einem
## Absturz mit leerem Ergebnissatz weiterliefen. Beide Male stand eine Null
## im Bericht, und beide Male war sie keine Messung, sondern ein Loch.
##
## Der Selbsttest steht ganz oben, weil er die Frage beantwortet, die vor
## allen anderen kommt: Hat ueberhaupt jemand hingesehen?
##
## Drei Teile:
##   a) Laeuft jede Probe, und schreibt sie ihren Abschnitt?
##   b) Passt die Zahl der geprueften Faelle zum Bestand?
##   c) Fragt jede Probe die Funktionen des Projekts, oder baut sie die
##      Bedingung ein zweites Mal nach?
##
## Teil b und c werden VOR den Proben aufgenommen, Teil a danach - anders
## geht es nicht, denn ob eine Probe ihren Abschnitt geschrieben hat, weiss
## man erst, wenn sie gelaufen ist. Gedruckt wird alles zusammen oben.


## Wo die Werkbank Projektlogik nachbaut oder das Projekt fragt.
## Diese Liste wird von Hand gefuehrt. Wer eine Probe schreibt, die ueber
## Ziehbarkeit urteilt, traegt sie hier ein - und zwar mit "eigen", bis
## sie das Projekt fragt.
NACHBAUTEN = [
    ("ziehbare_ereignisse", "fragt",
     "kettenziele() und einlagen_ketten_sammeln() des Projekts"),
    ("probe_bestandstafel: Ereignisse", "fragt",
     "bestand_zaehlen(), bestandslage(), ziehungen_pro_kapitel()"),
    ("probe_bestandstafel: Einlagen", "fragt",
     "einlage_im_bestand(); has_screen bleibt Laufzeit"),
    ("probe_bestandstafel: Traeger", "fragt",
     "traeger_ohne_kern(), traeger_fehlend(), kapitel_bogen()"),
    ("probe_pfadprobe: Bestand je Jahr", "fragt", "bestand_liste()"),
    ("probe_pfadprobe: Weltvergleich", "fragt", "welt_erlaubt()"),
    ("probe_pfadprobe: Ketten", "fragt",
     "ketten_ohne_spaeteres_jahr(), einlagen_ketten_sammeln()"),
    ("probe_sackgasse", "fragt",
     "die Spuren des Durchlaufs, keine eigene Bedingung"),
    ("probe_wertetafel: Gegenbewegung", "fragt", "bestand_liste()"),
    ("probe_wertetafel: Einbahn/Dominanz", "fragt",
     "ziehbare_ereignisse(), beide denselben Bestand (Paket 6, Vorweg E)"),
    ("probe_beleg", "fragt", "satzzahl() des Projekts"),
    ("probe_lesbarkeit", "fragt",
     "texte_sammeln() und die Sammelfunktionen der Dateien"),
    ("probe_bewegung: die drei Stufen", "fragt",
     "bewegungszeit() und die drei UEBERGANG_-Funktionen des Projekts"),
    ("probe_bewegung: die Grenzen", "fragt",
     "BEWEGUNG_HOECHSTDAUER und BEWEGUNG_HOECHSTDAUER_KAPITEL"),
    ("probe_bewegung: der Quelltext", "spiegel",
     "liest die .rpy-Dateien als Text, weil transform-Bloecke und "
     "at-Aufrufe Ren'Py-Anweisungen sind und in keinem Namensraum stehen"),
    ("probe_handgriffe: Spannweite", "fragt",
     "EINLAGE_AUSWERTEN und einlage_vorbereiten() des Projekts"),
    ("probe_handgriffe: Verteilungen", "fragt",
     "portionen_auswerten() und WERT_HOCH_IST_GUT; die Verteilungen selbst "
     "zaehlt sie auf, das ist Kombinatorik und keine Spiellogik"),
    ("probe_handgriffe: Zustandssaetze", "fragt",
     "portionen_stufe() und portionen_satz() - dieselben Funktionen, an "
     "denen der Bildschirm haengt"),
    ("textdurchsicht: Einlagen", "fragt", "einlage_im_bestand()"),
    ("Werkbank.wahl_treffen", "fragt",
     "schwaechster_wert() und WERT_HOCH_IST_GUT"),
    ("Werkbank.durchgang", "fragt",
     "ereignis_ziehen(), ende_pruefen(), kapitel_wirkung_anwenden()"),
    ("zweig_variante / zweig_welttext", "spiegel",
     "bildet die Vorrangfolge nach, weil variante() den gewaehlten "
     "Zweig nicht zurueckgibt; gegengeprueft am variantenersatz_protokoll"),
    ("probe_ton: die harte Sperre", "fragt",
     "ton_spielen() selbst, je Pfad und Stelle - die Bedingung steht kein "
     "zweites Mal hier, gezaehlt wird die Rueckgabe und MUSIK_VERWORFEN"),
    ("probe_ton: die Ortsangaben", "fragt",
     "ort_klangraum(), einlage_ort() und variante() des Projekts; die "
     "Ortsliste kommt aus EREIGNISSE, SZENEN_INDEX, EINLAGEN und PFAD_ORT"),
    ("probe_ton: die Aufrufstellen", "spiegel",
     "liest die .rpy-Dateien als Text, weil ein Aufruf in einem label "
     "in keinem Namensraum steht und sich nicht erfragen laesst"),
]


def ortsangaben_sammeln(NS):
    """Jede Ortsangabe, die im Spiel wirklich vorkommt - vom Projekt erfragt.

    Nicht aus ORT_KLANGRAUM: Sonst prueefte die Tafel sich selbst. Gefragt
    werden die drei Bestaende und die Funktionen, die den Ort aufloesen -
    einlage_ort() fuer die Einlagen, variante() fuer die Szenen, PFAD_ORT
    fuer alles, was keinen eigenen Ort nennt (Regel 11).
    """
    pfade = list(NS.get("PFAD_REIHENFOLGE", ["front", "etappe", "heimat"]))
    alt = NS.get("aktueller_pfad")
    orte = set()

    for vorlage in NS.get("EREIGNISSE", []):
        if getattr(vorlage, "ort", None):
            orte.add(vorlage.ort)

    for pfad in pfade:
        NS["aktueller_pfad"] = pfad
        for vorlage in NS.get("EINLAGEN", []):
            if getattr(vorlage, "ort", None) and callable(NS.get("einlage_ort")):
                orte.add(NS["einlage_ort"](vorlage.kennung))
        for szene in NS.get("SZENEN_INDEX", {}).values():
            if getattr(szene, "ort", None) and callable(NS.get("variante")):
                gesetzt = NS["variante"](szene.ort, None)
                orte.add(gesetzt if gesetzt else NS["ort_text"]())

    NS["aktueller_pfad"] = alt
    for wert in NS.get("PFAD_ORT", {}).values():
        orte.add(wert)
    return sorted(o for o in orte if o)


def probe_ton(NS, B, spielordner):
    """Das Tongeruest: die harte Sperre, die Tafeln und die Aufrufstellen.

    SEIT PAKET 8, SCHRITT 2.6. Die Abnahme dieses Schritts lautet
    "ton_spielen() gibt auf front und etappe null Musikaufrufe frei" - eine
    Zahl, keine Zusicherung. Sie laesst sich nur so messen: Die Probe ruft
    ton_spielen() selbst und wertet die Rueckgabe aus. Am Ton erkennt sie
    nichts, denn renpy.music ist in der Werkbank eine Attrappe und schluckt
    jeden Aufruf still.
    """
    beanstandungen = 0
    geprueft = 0

    B.titel("PROBE 11  TONPROBE")
    B("Regel 3 sagt: an der Front und in der Etappe nie Musik. Diese Probe")
    B("prueft das nicht am Vorsatz, sondern am Verhalten - sie ruft")
    B("ton_spielen() fuer jede Musikstelle auf jedem Pfad und zaehlt, was")
    B("freigegeben und was verworfen wurde. Eine fehlende Tondatei ist dabei")
    B("keine Beanstandung: Wo kein Ton liegt, ist es still, und das ist kein")
    B("Mangel, den jemand sieht.")

    if not callable(NS.get("ton_spielen")):
        B("")
        B(">> FEHLER << ton_spielen() gibt es nicht. Steht ton.rpy in der")
        B("LESEFOLGE, und steht die Funktion in einem init-python-Block?")
        return 1, 0

    pfade = list(NS.get("PFAD_REIHENFOLGE", ["front", "etappe", "heimat"]))
    alt = NS.get("aktueller_pfad")
    verworfen_vorher = len(NS["MUSIK_VERWORFEN"])

    ## ------------------------------------------------------------------ 1
    B.unterteil("Die harte Sperre: ton_spielen(stelle, \"musik\") je Pfad")
    B("%-10s %-12s %10s %10s %10s" % ("Pfad", "Musik dort", "geprueft",
                                      "freigegeben", "verworfen"))
    for pfad in pfade:
        NS["aktueller_pfad"] = pfad
        gesperrt = pfad in NS.get("MUSIK_GESPERRT", ())
        frei = 0
        vorher = len(NS["MUSIK_VERWORFEN"])
        for stelle in sorted(NS.get("STELLENMUSIK", {})):
            geprueft += 1
            if NS["ton_spielen"](stelle, "musik") is not None:
                frei += 1
        verworfen = len(NS["MUSIK_VERWORFEN"]) - vorher
        B("%-10s %-12s %10d %10d %10d"
          % (pfad, "gesperrt" if gesperrt else "erlaubt",
             len(NS.get("STELLENMUSIK", {})), frei, verworfen))
        if gesperrt and frei:
            beanstandungen += frei
            B("   >> FEHLER << %d Musikaufrufe auf %s freigegeben." % (frei, pfad))

    ## ------------------------------------------------------------------ 2
    ## Umgebungsklaenge sind auch auf front und etappe erlaubt (Regel 3
    ## verbietet Musik, nicht den Klang des Ortes). Gemessen wird nicht am
    ## gespielten Pfad - der ist None, solange keine Datei liegt -, sondern
    ## daran, dass die Sperre keinen einzigen Aufruf verworfen hat.
    B("")
    B.unterteil("Umgebungsklang: ton_spielen(klangraum, \"umgebung\") je Pfad")
    B("%-10s %10s %12s %10s" % ("Pfad", "geprueft", "gespielt", "verworfen"))
    for pfad in pfade:
        NS["aktueller_pfad"] = pfad
        gespielt = 0
        vorher = len(NS["MUSIK_VERWORFEN"])
        for raum in NS.get("KLANGRAEUME", []):
            geprueft += 1
            if NS["ton_spielen"](raum, "umgebung") is not None:
                gespielt += 1
        verworfen = len(NS["MUSIK_VERWORFEN"]) - vorher
        B("%-10s %10d %12d %10d"
          % (pfad, len(NS.get("KLANGRAEUME", [])), gespielt, verworfen))
        if verworfen:
            beanstandungen += verworfen
            B("   >> FEHLER << Die Sperre hat auf %s einen Umgebungsklang"
              % pfad)
            B("   verworfen. Regel 3 verbietet dort Musik, nicht den Ort.")
    NS["aktueller_pfad"] = alt

    ## ------------------------------------------------------------------ 3
    B("")
    B.unterteil("Die Tafeln")
    B("%-24s %6s  %s" % ("Tafel", "Zeilen", "Befund"))
    ohne_zeile = [r for r in NS.get("KLANGRAEUME", [])
                  if r not in NS.get("ORTSKLANG", {})]
    verwaiste_zeile = [r for r in NS.get("ORTSKLANG", {})
                       if r not in NS.get("KLANGRAEUME", [])]
    fremde_ziele = sorted(set(NS.get("ORT_KLANGRAUM", {}).values())
                          - set(NS.get("KLANGRAEUME", [])))
    ohne_zweck = [r for r in NS.get("KLANGRAEUME", [])
                  if not NS.get("KLANGRAUM_ZWECK", {}).get(r)]
    for name, anzahl, fehler, satz in (
            ("KLANGRAEUME", len(NS.get("KLANGRAEUME", [])), ohne_zeile,
             "Klangraum ohne Zeile in ORTSKLANG"),
            ("ORTSKLANG", len(NS.get("ORTSKLANG", {})), verwaiste_zeile,
             "Zeile ohne Klangraum"),
            ("ORT_KLANGRAUM", len(NS.get("ORT_KLANGRAUM", {})), fremde_ziele,
             "Ziel ausserhalb KLANGRAEUME"),
            ("KLANGRAUM_ZWECK", len(NS.get("KLANGRAUM_ZWECK", {})), ohne_zweck,
             "Klangraum ohne Zwecksatz"),
            ("STELLENMUSIK", len(NS.get("STELLENMUSIK", {})), [],
             "")):
        geprueft += anzahl
        beanstandungen += len(fehler)
        B("%-24s %6d  %s" % (name, anzahl,
                             "in Ordnung" if not fehler
                             else ">> FEHLER << %s: %s" % (satz, ", ".join(fehler))))

    ## ------------------------------------------------------------------ 4
    ## Jede Ortsangabe des Bestands muss einen Klangraum finden. Gefragt wird
    ## ort_klangraum() selbst; wer keinen findet, steht danach in
    ## ORT_OHNE_KLANGRAUM - dieselbe Bauart wie KARTENTYP_UNBEKANNT.
    B("")
    B.unterteil("Jede Ortsangabe des Bestands findet einen Klangraum")
    orte = ortsangaben_sammeln(NS)
    vorher = list(NS.get("ORT_OHNE_KLANGRAUM", []))
    zaehler = collections.Counter()
    for ort in orte:
        geprueft += 1
        zaehler[NS["ort_klangraum"](ort)] += 1
    NS["aktueller_pfad"] = alt
    neu = [o for o in NS.get("ORT_OHNE_KLANGRAUM", []) if o not in vorher]
    B("%d Ortsangaben aus EREIGNISSE, SZENEN_INDEX, EINLAGEN und PFAD_ORT."
      % len(orte))
    B("")
    B("%-16s %8s  %s" % ("Klangraum", "Orte", "Zweck"))
    for raum in NS.get("KLANGRAEUME", []):
        B("%-16s %8d  %s" % (raum, zaehler.get(raum, 0),
                             NS.get("KLANGRAUM_ZWECK", {}).get(raum, "")))
    B("")
    if neu:
        beanstandungen += len(neu)
        B(">> FEHLER << %d Ortsangaben ohne Zeile in ORT_KLANGRAUM:" % len(neu))
        for ort in neu:
            B("   %s" % ort)
        B("Sie klingen nach dem Pfad statt nach dem Ort. Eine Zeile in")
        B("ORT_KLANGRAUM (ton.rpy) behebt es.")
    else:
        B("Keine Ortsangabe ohne Klangraum.")

    ## ------------------------------------------------------------------ 5
    ## Wo im Spiel Ton angelegt wird. Eine Tafel ohne Aufrufstelle waere nur
    ## ein Versprechen - genau das, was die Medienprobe bei BILD_MASSE
    ## anmahnt. Und Auftragspunkt 14 ("kein Ton bewertet eine Entscheidung")
    ## laesst sich nur nachlesen, wenn jede Stelle aufgezaehlt dasteht.
    B("")
    B.unterteil("Wo im Spiel Ton angelegt wird")
    marken = ("ortsklang_setzen(", "musik_setzen(", "ton_spielen(", "ton_still(")
    fundstellen = []
    for dateiname in rpy_dateien(spielordner):
        if dateiname == "ton.rpy":
            continue
        for nummer, zeile in enumerate(zeilen_lesen(spielordner, dateiname), 1):
            nackt = zeile.strip()
            if nackt.startswith("#"):
                continue
            for marke in marken:
                if marke in nackt:
                    fundstellen.append((dateiname, nummer, marke[:-1], nackt))
                    break
    geprueft += len(fundstellen)
    B("%-16s %6s  %s" % ("Datei", "Zeile", "Aufruf"))
    for dateiname, nummer, marke, _text in fundstellen:
        B("%-16s %6d  %s" % (dateiname, nummer, marke))

    ## Verlangt sind die beiden Eingaenge, nicht ton_spielen() selbst: Das
    ## Spiel ruft ortsklang_setzen() und musik_setzen(), und die beiden gehen
    ## innerhalb von ton.rpy durch ton_spielen(). Waere ton_spielen() hier
    ## verlangt, beanstandete die Probe genau die Bauart, die sie schuetzen
    ## soll - so geschehen beim ersten Lauf dieser Probe.
    for marke, tafel in (("ortsklang_setzen(", "ORTSKLANG"),
                         ("musik_setzen(", "STELLENMUSIK")):
        if not any(f[2] == marke[:-1] for f in fundstellen):
            beanstandungen += 1
            B("")
            B(">> FEHLER << %s wird im ganzen Spiel nirgends gerufen, also"
              % marke[:-1])
            B("hat die Tafel %s keine Aufrufstelle und ist nur ein"
              % tafel)
            B("Versprechen - genau das, was die Medienprobe sonst anmahnt.")

    unmittelbar = [f for f in fundstellen if f[2] == "ton_spielen"]
    if unmittelbar:
        B("")
        B("HINWEIS: %d Stellen rufen ton_spielen() unmittelbar. Erlaubt, aber"
          % len(unmittelbar))
        B("sie gehen an der Wechselpruefung von ortsklang_setzen() vorbei -")
        B("der Klang setzt dann bei jeder Karte neu ein. Die harte Sperre")
        B("greift unabhaengig davon, sie sitzt in ton_spielen() selbst.")

    B("")
    B("%d Aufrufstellen in %d Dateien. ton.rpy selbst ist nicht mitgezaehlt."
      % (len(fundstellen), len(set(f[0] for f in fundstellen))))

    ## ------------------------------------------------------------------ 6
    ## SEIT DEM GEGENLESEN VOM 6. SEPTEMBER. Die Sperre in ton_spielen()
    ## verhindert nur, dass Musik ANGEWORFEN wird. Sie beendet nichts. Das
    ## reicht nicht: label start wirft Musik dreimal an, solange
    ## aktueller_pfad noch auf der Vorgabe "heimat" steht, und der Pfad faellt
    ## erst danach in pfad_wechseln(). Die Menuemusik waere bis in den Graben
    ## durchgelaufen, ohne dass ein einziger Aufruf verworfen worden waere -
    ## und die Abschnitte 1 und 2 dieser Probe haetten weiter null gemeldet.
    ## Deshalb misst dieser Abschnitt die Sperre als DAUERZUSTAND.
    B("")
    B.unterteil("Die Sperre beendet, was laeuft - nicht nur, was anfaengt")
    if not callable(NS.get("musik_sperre_durchsetzen")):
        beanstandungen += 1
        B(">> FEHLER << musik_sperre_durchsetzen() gibt es nicht. Ohne sie")
        B("verhindert die Sperre nur das Anwerfen und laesst laufende Musik")
        B("in den Graben durch.")
    else:
        B("%-10s %-12s %s" % ("Pfad", "Musik dort", "greift die Durchsetzung"))
        for pfad in pfade:
            NS["aktueller_pfad"] = pfad
            geprueft += 1
            gesperrt = pfad in NS.get("MUSIK_GESPERRT", ())
            greift = bool(NS["musik_sperre_durchsetzen"]())
            B("%-10s %-12s %s" % (pfad, "gesperrt" if gesperrt else "erlaubt",
                                  "ja" if greift else "nein"))
            if gesperrt and not greift:
                beanstandungen += 1
                B("   >> FEHLER << Auf %s laeuft Musik weiter." % pfad)
            if not gesperrt and greift:
                beanstandungen += 1
                B("   >> FEHLER << Auf %s wird Musik beendet, obwohl sie"
                  % pfad)
                B("   dort erlaubt ist.")
        NS["aktueller_pfad"] = alt

    ## Die beiden Ren'Py-Listen, die das Geruest ergaenzen muss. Ohne die
    ## erste liefe der Ortsklang unter dem Hauptmenue weiter (ein selbst
    ## angemeldeter Kanal steht in keiner Abraeumliste), ohne die zweite
    ## gaelte die Sperre nur fuer die Aufrufe, die es heute gibt.
    B("")
    B("%-34s %s" % ("Ren'Py-Liste", "Eintrag vorhanden"))
    kanal = NS.get("TON_KANAL", {}).get("umgebung", "umgebung")
    abraeumen = list(getattr(NS["config"], "main_menu_stop_channels", []))
    rueckrufe = [getattr(f, "__name__", "") for f
                 in list(getattr(NS["config"], "periodic_callbacks", []))]
    for name, drin, satz in (
            ("config.main_menu_stop_channels", kanal in abraeumen,
             "Kanal \"%s\" wird beim Ruecksprung ins Hauptmenue nicht "
             "abgeraeumt und liefe darunter weiter" % kanal),
            ("config.periodic_callbacks", "musik_sperre_wacht" in rueckrufe,
             "die Wache fehlt - dann gilt die Sperre nur fuer die Aufrufe, "
             "die es heute gibt")):
        geprueft += 1
        B("%-34s %s" % (name, "ja" if drin else "NEIN"))
        if not drin:
            beanstandungen += 1
            B("   >> FEHLER << %s." % satz)

    ## Das zweite Bein steht nicht in einer Ren'Py-Liste, sondern im
    ## Quelltext: pfad_wechseln() muss die Sperre rufen, sobald der Pfad
    ## faellt. Das ist der frueheste Punkt, an dem Regel 3 gelten kann.
    quelle_pfadwechsel = ""
    if "herkunft.rpy" in rpy_dateien(spielordner):
        gesehen = False
        for zeile in zeilen_lesen(spielordner, "herkunft.rpy"):
            nackt = zeile.strip()
            if nackt.startswith("def pfad_wechseln("):
                gesehen = True
            elif gesehen and nackt.startswith("def "):
                break
            elif gesehen and "musik_sperre_durchsetzen(" in nackt \
                    and not nackt.startswith("#"):
                quelle_pfadwechsel = nackt
                break
    geprueft += 1
    B("%-34s %s" % ("pfad_wechseln() ruft die Sperre",
                    "ja" if quelle_pfadwechsel else "NEIN"))
    if not quelle_pfadwechsel:
        beanstandungen += 1
        B("   >> FEHLER << Ohne diesen Aufruf laeuft Musik, die vor der")
        B("   Musterung angeworfen wurde, in den Graben weiter.")

    ## Die beiden Eingaenge duerfen NICHTS zurueckgeben. musik_setzen() steht
    ## in screens.rpy als on "show" action Function(...), und Ren'Pys Function
    ## sagt selbst: "If the function returns a non-None value, the interaction
    ## stops and returns that value." Eine Rueckgabe beendete also das
    ## Hauptmenue, sobald dort zum ersten Mal wirklich Musik anlaeuft - das
    ## Menue blitzte auf und das Spiel liefe von allein los.
    ##
    ## Messbar ist das nur mit einer Datei, die es wirklich gibt: Ohne Datei
    ## geben beide ohnehin None zurueck, und die Messung waere eine gruene
    ## Null aus einer Nichtmessung (Regel 11).
    B("")
    tondatei = None
    audioordner = os.path.join(spielordner, "audio")
    if os.path.isdir(audioordner):
        for name in sorted(os.listdir(audioordner)):
            stamm, endung = os.path.splitext(name)
            if endung.lstrip(".").lower() in NS.get("TON_ENDUNGEN", []):
                tondatei = stamm
                break
    if tondatei is None:
        B("Rueckgabe der beiden Eingaenge: NICHTS GEMESSEN.")
        B("In audio/ liegt keine Datei mit einer Endung aus TON_ENDUNGEN.")
        B("Ohne abspielbare Datei geben musik_setzen() und ortsklang_setzen()")
        B("ohnehin None zurueck, und die Pruefung waere eine gruene Null.")
    else:
        alte_musik = dict(NS["STELLENMUSIK"])
        alter_klang = dict(NS["ORTSKLANG"])
        alter_schalter = NS.get("MUSIK_EINGESCHALTET")
        stelle = sorted(NS["STELLENMUSIK"])[0]
        NS["aktueller_pfad"] = "heimat"
        raum = NS["ort_klangraum"]("Wohnviertel")
        NS["STELLENMUSIK"][stelle] = (tondatei, 0.3, True)
        NS["ORTSKLANG"][raum] = (tondatei, 0.3, True)
        NS["MUSIK_EINGESCHALTET"] = True
        laeuft = NS["ton_spielen"](stelle, "musik")
        NS["ortsklang_aktuell"] = None
        rueck_musik = NS["musik_setzen"](stelle)
        NS["ortsklang_aktuell"] = None
        rueck_ort = NS["ortsklang_setzen"]("Wohnviertel")
        NS["STELLENMUSIK"].clear()
        NS["STELLENMUSIK"].update(alte_musik)
        NS["ORTSKLANG"].clear()
        NS["ORTSKLANG"].update(alter_klang)
        NS["MUSIK_EINGESCHALTET"] = alter_schalter
        NS["ortsklang_aktuell"] = None
        NS["aktueller_pfad"] = alt
        geprueft += 2
        B("Rueckgabe der beiden Eingaenge, gemessen mit audio/%s:" % tondatei)
        B("   ton_spielen()      %s   (muss den Pfad nennen, sonst ist die"
          % ("liefert " + str(laeuft) if laeuft else "liefert None"))
        B("                      Messung selbst wertlos)")
        B("   musik_setzen()     %s" % ("None" if rueck_musik is None
                                        else ">> FEHLER << " + str(rueck_musik)))
        B("   ortsklang_setzen() %s" % ("None" if rueck_ort is None
                                        else ">> FEHLER << " + str(rueck_ort)))
        if laeuft is None:
            beanstandungen += 1
            B("   >> FEHLER << ton_spielen() hat nichts gespielt, obwohl die")
            B("   Datei da ist. Die beiden Zeilen darueber messen dann nichts.")
        if rueck_musik is not None or rueck_ort is not None:
            beanstandungen += 1
            B("   Eine Rueckgabe beendet in Ren'Py die Interaktion, sobald die")
            B("   Funktion als \"action Function(...)\" in einem Bildschirm")
            B("   steht. Das Hauptmenue liefe dann von allein los.")

    ## Der Zustand, in dem die Probe das Projekt hinterlaesst. Sie hat
    ## MUSIK_VERWORFEN gefuellt, weil sie messen musste; das ist kein Befund
    ## des Spiels und wird deshalb ausgewiesen.
    B("")
    B("Die Probe selbst hat %d Musikaufrufe ausgeloest und %d davon verworfen."
      % (len(pfade) * len(NS.get("STELLENMUSIK", {})),
         len(NS["MUSIK_VERWORFEN"]) - verworfen_vorher))
    B("Das ist Messung, kein Befund des Spiels: MUSIK_VERWORFEN faengt in")
    B("jedem Durchgang leer an.")

    return beanstandungen, geprueft


def medienverweise_erwartet(NS):
    """Wie viele Medienverweise der Quelltext hergibt - unabhaengig gezaehlt.

    Nicht aus dem Medienbuch, sondern aus dem Bestand. Nur so ist die Zahl
    im Medienbuch eine Messung und keine Selbstauskunft.
    """
    stimmungen = set(["standard"])
    for name in NS.get("STIMMUNG_AUS_WERT", {}).values():
        stimmungen.add(name)
    for vorlage in NS["EREIGNISSE"]:
        if vorlage.stimmung:
            stimmungen.add(vorlage.stimmung)

    karten = sum(len(v.optionen) for v in NS["EREIGNISSE"])
    portraits = len(NS["HERKUENFTE"]) * 2 * len(stimmungen)
    figuren = (len(NS.get("FIGUREN_REIHENFOLGE", []))
               * len(NS["PFAD_REIHENFOLGE"]) * len(stimmungen))

    ## SEIT PAKET 8, SCHRITT 2.6. Ohne diese Zeile waechst 'ist_medien' um
    ## die Tonpfade, 'soll_medien' aber nicht - und der Erklaersatz zur
    ## Differenz stimmte nicht mehr. Gezaehlt wird Tafelzeile mal Endung,
    ## weil ton_waehlen() beide Endungen der Reihe nach versucht.
    endungen = len(NS.get("TON_ENDUNGEN", []))
    toene = (len(NS.get("ORTSKLANG", {})) + len(NS.get("STELLENMUSIK", {}))) \
        * endungen

    return {
        "Kartenbilder (je Option eines)": karten,
        "Portraets (Herkunft x Geschlecht x Stimmung)": portraits,
        "Nebenfiguren (Figur x Pfad x Stimmung)": figuren,
        "Toene (Tafelzeile x Endung)": toene,
    }


def selbsttest_ausgeben(kopf, NS, proben, durchgaenge, medienbuch):
    """Die Selbsttesttafel. Steht ganz oben im Bericht."""
    fehlerhaft = False

    kopf("=" * 78)
    kopf("SELBSTTEST DER WERKBANK")
    kopf("=" * 78)
    kopf("Vor allen Zahlen die Frage, die vor allen anderen kommt: Hat")
    kopf("ueberhaupt jemand hingesehen? Eine Probe, die schweigt, gilt als")
    kopf("AUSGEFALLEN und nicht als Null.")
    kopf("")

    ## ------------------------------------------------------------------ a
    kopf("a) Laeuft jede Probe, und schreibt sie ihren Abschnitt?")
    kopf("%-20s %-16s %12s   %s" % ("Probe", "Zustand", "Faelle", "Abschnitt"))
    for name, _b, geprueft, _was, zustand, geschrieben in proben:
        if zustand != "gelaufen" or not geschrieben or geprueft == 0:
            fehlerhaft = True
        kopf("%-20s %-16s %12d   %s" % (
            name, zustand, geprueft,
            "geschrieben" if geschrieben else ">> AUSGEFALLEN <<"))
    kopf("")

    ## ------------------------------------------------------------------ b
    kopf("b) Passt die Zahl der geprueften Faelle zum Bestand?")
    ereignisse = len(NS["EREIGNISSE"])
    einlagen = len(NS["EINLAGEN"])
    briefe = len(NS.get("BRIEFE", []))
    kopf("   Bestand: %d Ereignisse, %d Einlagen, %d Briefe."
         % (ereignisse, einlagen, briefe))

    fallzahl = dict((name, geprueft) for name, _b, geprueft, _w, _z, _g in proben)

    soll_beleg = ereignisse + einlagen
    ist_beleg = fallzahl.get("5 Belegprobe", 0)
    kopf("   Belegprobe:   %d geprueft, %d im Bestand (%d + %d).   %s" % (
        ist_beleg, soll_beleg, ereignisse, einlagen,
        "stimmt" if ist_beleg == soll_beleg
        else ">> FEHLER << Differenz %d" % (ist_beleg - soll_beleg)))
    if ist_beleg != soll_beleg:
        fehlerhaft = True

    teile = medienverweise_erwartet(NS)
    soll_medien = sum(teile.values())
    ist_medien = fallzahl.get("6 Medienprobe", 0)
    kopf("   Medienprobe:  %d Pfade im Medienbuch, %d Verweise im Bestand."
         % (ist_medien, soll_medien))
    for name, anzahl in teile.items():
        kopf("      %-46s %6d" % (name, anzahl))
    kopf("      Differenz %d. Sie ist erwartet und hat zwei Gruende: Mehrere"
         % (ist_medien - soll_medien))
    kopf("      Optionen zeigen dasselbe Kartenbild, und das Medienbuch")
    kopf("      fuehrt jeden Pfad nur einmal; dazu kommen Schriften und der")
    kopf("      Platzhalter, die in keiner der vier Zeilen stehen.")

    ## SEIT PAKET 6, VORWEG E. Die beiden Regelpruefungen in Probe 4
    ## zaehlten verschiedene Bestaende; jetzt fragen beide dieselbe
    ## Funktion. Die Zahl steht hier, damit ein Auseinanderlaufen wieder
    ## auffaellt, ohne dass jemand den Code liest.
    ziehbar = len(ziehbare_ereignisse(NS))
    nur_kette_gesamt = len([v for v in NS["EREIGNISSE"] if v.nur_kette])
    kopf("   Regelpruefungen: Einbahnstrassen und Dominanz sehen je %d Karten."
         % ziehbar)
    kopf("      Das sind alle %d Ereignisse minus die %d nur_kette-Karten,"
         % (ereignisse, nur_kette_gesamt))
    kopf("      auf die nichts zeigt. Beide fragen ziehbare_ereignisse().")

    ## Probe 8 zaehlt zwei verschiedene Bestaende, und das ist Absicht:
    ## Die Tafel nach Textart misst, was das Spiel zeigt; die Tafel nach
    ## Gattung nimmt zusaetzlich die Einordnungen aus den quelle-Feldern
    ## auf. Gemeldet wird die kleinere Zahl, weil sie mit den frueheren
    ## Berichten vergleichbar bleibt.
    ist_lesbar = fallzahl.get("8 Lesbarkeit", 0)
    fein_saetze = 0
    for _gattung, _ort, text in textbestand_fein(NS):
        fein_saetze += len([s for s in saetze_zerlegen(text)
                            if woerter_zaehlen(s)])
    kopf("   Lesbarkeit:   %d Saetze gemeldet, %d nach Gattung gemessen."
         % (ist_lesbar, fein_saetze))
    kopf("      Differenz %d: die Einordnungen aus den quelle-Woerterbuechern."
         % (fein_saetze - ist_lesbar))

    ist_werte = fallzahl.get("4 Wertetafel", 0)
    lagen = len(NS["PFAD_REIHENFOLGE"]) * 2
    soll_werte = lagen * len(STRATEGIEN) * durchgaenge
    kopf("   Wertetafel:   %d geprueft, davon %d Durchgaenge (%d Lagen x %d"
         % (ist_werte, soll_werte, lagen, len(STRATEGIEN)))
    kopf("      Strategien x %d). Der Rest sind Kalenderlaeufe, Karten der"
         % durchgaenge)
    kopf("      Gegenbewegung und die Dominanzpruefung.")
    if ist_werte < soll_werte:
        fehlerhaft = True
        kopf("      >> FEHLER << weniger Faelle als Durchgaenge - es sind")
        kopf("                   nicht alle Lagen gespielt worden.")
    kopf("")

    ## ------------------------------------------------------------------ c
    kopf("c) Fragt jede Probe die Funktionen des Projekts?")
    kopf("   'fragt' heisst: Die Probe ruft dieselbe Funktion wie das Spiel.")
    kopf("   'eigen' heisst: Sie formuliert die Bedingung ein zweites Mal.")
    kopf("   'spiegel' heisst: Sie bildet bewusst nach, weil sie mehr")
    kopf("   wissen muss, als die Projektfunktion zurueckgibt.")
    kopf("")
    eigen = 0
    for stelle, zustand, woher in NACHBAUTEN:
        if zustand == "eigen":
            eigen += 1
        kopf("   %-36s %-8s %s" % (stelle, zustand, woher))
    kopf("")
    kopf("   Stellen insgesamt: %d, davon mit eigenem Nachbau: %d."
         % (len(NACHBAUTEN), eigen))

    kopf("")
    kopf("SELBSTTEST: " + ("FEHLER - siehe oben" if fehlerhaft
                          else "die Werkbank hat gemessen"))
    kopf("=" * 78)
    kopf("")
    return fehlerhaft


################################################################################
## 13. Hauptlauf
################################################################################


def hauptlauf(argumente):
    spielordner = spielordner_finden(argumente.ordner)
    random.seed(argumente.saat)

    B = Bericht()
    kurz = []
    umfang = []
    fehlerhaft = False

    ## ------------------------------------------------------------ A: Aufbau
    aufbau = Aufbau(spielordner)
    aufbau.lesen()
    aufbau.ausfuehren()
    aufbau.vorgaben_setzen()
    NS = aufbau.NS

    aufbau_beanstandungen = len(aufbau.abbrueche) + len(aufbau.fehlend) \
        + len(aufbau.vorgabe_fehler)

    B.titel("PROBE ALLES - Werkbank zu \"Zwischen Front und Heimat\"")
    B("Ordner: " + spielordner)
    B("Zufallssaat: %d   Durchgaenge je Lage: %d" % (argumente.saat, argumente.durchgaenge))

    B.titel("A  AUFBAU")
    B("%-16s %8s %10s %10s" % ("Datei", "Bloecke", "Vorgaben", "Zustand"))
    for name, bloecke, vorgaben in aufbau.gelesen:
        gelaufen = len([b for b in aufbau.bloecke
                        if b["datei"] == name and b.get("gelaufen")])
        zustand = "in Ordnung" if gelaufen == bloecke else "%d gelaufen" % gelaufen
        B("%-16s %8d %10d %10s" % (name, bloecke, vorgaben, zustand))
    for name in aufbau.fehlend:
        B("%-16s %8s %10s %10s" % (name, "-", "-", ">> FEHLT <<"))

    B("")
    B("Ausfuehrungsfolge (init-Rang, dann Datei, dann Stelle):")
    zeile = []
    for block in aufbau.bloecke:
        zeile.append("%s:%d@%d" % (block["datei"].replace(".rpy", ""),
                                   block["kopfzeile"], block["rang"]))
    for stelle in range(0, len(zeile), 5):
        B("   " + "   ".join(zeile[stelle:stelle + 5]))

    if aufbau.fehlend:
        B("")
        for name in aufbau.fehlend:
            B(">> FEHLER << %s liegt nicht im Spielordner. Alles, was diese Datei"
              % name)
            B("             beitraegt, fehlt in dieser Probe.")

    if aufbau.abbrueche:
        B.unterteil("Bloecke, die sich nicht ausfuehren liessen")
        for eintrag in aufbau.abbrueche:
            B("   %s  Block %d  (init %d, Zeile %d)" % (
                eintrag["datei"], eintrag["nummer"], eintrag["rang"],
                eintrag["kopfzeile"]))
            B("      %s" % eintrag["meldung"])
            for zeile_text in eintrag["erste_zeilen"]:
                B("      | " + zeile_text[:96])
            B("")
    else:
        B("")
        B("Alle gelesenen Bloecke sind durchgelaufen.")

    if aufbau.vorgabe_fehler:
        B.unterteil("default-Zuweisungen, die sich nicht auswerten liessen")
        for datei, zeile_nr, name, meldung in aufbau.vorgabe_fehler:
            B("   %s:%d  %s  ->  %s" % (datei, zeile_nr, name, meldung))

    if NS.erfundene:
        B.unterteil("Namen, fuer die eine Attrappe eingetreten ist")
        B("Jeder dieser Namen kam im Quelltext vor, ohne dass er dort oder in")
        B("dieser Werkbank angelegt worden waere. In Ren'Py bringt ihn die")
        B("Laufzeit mit - oder es ist ein Schreibfehler.")
        for name, anzahl in NS.erfundene.most_common():
            B("   %-32s %dx" % (name, anzahl))
    else:
        B("Keine Attrappe musste einspringen.")

    if aufbau_beanstandungen:
        fehlerhaft = True
    kurz.append(("Aufbau", aufbau_beanstandungen,
                 "%d Dateien, %d Bloecke" % (len(aufbau.gelesen), len(aufbau.bloecke))))
    umfang.append(("Aufbau", len(aufbau.bloecke), "init-Bloecke ausgefuehrt"))

    ## Wenn der Aufbau nicht traegt, hat keine Probe eine Grundlage.
    if "EREIGNISSE" not in NS or isinstance(NS["EREIGNISSE"], Attrappe):
        B.titel("ABBRUCH")
        B("Der Ereignisbestand ist nicht entstanden. Die sieben Proben")
        B("brauchen ihn; sie werden uebersprungen.")
        return B, 1, kurz, umfang

    buch = Rueckfallbuch()
    beobachtung_einhaengen(NS, buch)

    ## Eine Grundlage, damit Aufrufe ausserhalb eines Durchgangs nicht
    ## auf einen leeren Zustand treffen.
    try:
        NS["zustand_zuruecksetzen"]()
        NS["probe_lebenslage"]("arbeiterschaft", "heimat", None)
    except Exception:
        B.titel("ABBRUCH")
        B("Der Spielstand liess sich nicht aufbauen:")
        B(traceback.format_exc())
        return B, 1, kurz, umfang

    proben = []

    ## SEIT PAKET 5, SCHRITT 3, TEIL D.15a wird mitgeschrieben, OB eine
    ## Probe ihren Abschnitt ueberhaupt gedruckt hat. Eine Probe, die
    ## durchlaeuft, ohne eine Zeile zu schreiben, ist kein Erfolg, sondern
    ## ein Werkzeugfehler - und in der Kurzfassung war sie bisher nicht von
    ## einer Probe ohne Fund zu unterscheiden.
    def probe_laufen(nummer, name, funktion, *args):
        vorher = len(B.zeilen)
        try:
            beanstandungen, geprueft = funktion(*args)
        except Exception:
            B.titel("PROBE %d  %s - ABGEBROCHEN" % (nummer, name.upper()))
            B(traceback.format_exc())
            return 1, 0, "ABGEBROCHEN", True
        marke = "PROBE %d" % nummer
        geschrieben = any(marke in zeile for zeile in B.zeilen[vorher:])
        return beanstandungen, geprueft, "gelaufen", geschrieben

    ## ------------------------------------------------------------ 1
    b, g, z, w = probe_laufen(1, "Bestandstafel", probe_bestandstafel, NS, B)
    proben.append(("1 Bestandstafel", b, g, "Kapitel mal Pfad mal Verlauf", z, w))

    ## ------------------------------------------------------- 2, 3 und 4
    ## Ein einziger Durchlauf traegt drei Proben. Alles andere waere
    ## dreimal dieselbe Rechnung.
    try:
        werkbank, umgebung, ergebnisse = durchlauf(NS, buch, argumente.durchgaenge)
    except Exception:
        B.titel("PROBEN 2 BIS 4 - ABGEBROCHEN")
        B(traceback.format_exc())
        werkbank, umgebung, ergebnisse = None, None, {}

    b2, g2, z2, w2 = probe_laufen(2, "Pfadprobe", probe_pfadprobe, NS, B, werkbank,
                                  umgebung, ergebnisse, buch, argumente.durchgaenge)
    proben.append(("2 Pfadprobe", b2, g2, "protokollierte Inhalte", z2, w2))

    b3, g3, z3, w3 = probe_laufen(3, "Sackgassenprobe", probe_sackgasse, NS, B,
                                  ergebnisse)
    proben.append(("3 Sackgassenprobe", b3, g3, "Kapitelabschluesse", z3, w3))

    b4, g4, z4, w4 = probe_laufen(4, "Wertetafel", probe_wertetafel, NS, B,
                                  ergebnisse)
    proben.append(("4 Wertetafel", b4, g4, "Durchgaenge und Kalenderlaeufe", z4, w4))

    ## ------------------------------------------------------------ 5
    b, g, z, w = probe_laufen(5, "Belegprobe", probe_beleg, NS, B)
    proben.append(("5 Belegprobe", b, g, "Ereignisse und Einlagen", z, w))

    ## ------------------------------------------------------------ 6
    b, g, z, w = probe_laufen(6, "Medienprobe", probe_medien, NS, B,
                              aufbau.medienbuch, spielordner)
    proben.append(("6 Medienprobe", b, g, "erwartete Dateipfade", z, w))

    ## ------------------------------------------------------------ 7
    b, g, z, w = probe_laufen(7, "Sprachprobe", probe_sprache, NS, B)
    proben.append(("7 Sprachprobe", b, g, "angesehene Textstellen", z, w))

    ## ------------------------------------------------------------ 8
    b, g, z, w = probe_laufen(8, "Lesbarkeit", probe_lesbarkeit, NS, B)
    proben.append(("8 Lesbarkeit", b, g, "gemessene Saetze", z, w))

    ## ------------------------------------------------------------ 9
    ## SEIT PAKET 7, SCHRITT 1. Sie steht am Ende, weil sie als einzige den
    ## Quelltext als Text liest und keinen Spielstand braucht.
    b, g, z, w = probe_laufen(9, "Bewegungsprobe", probe_bewegung, NS, B,
                              spielordner)
    proben.append(("9 Bewegungsprobe", b, g, "Bewegungen und Aufrufe", z, w))

    ## ------------------------------------------------------------ 10
    ## SEIT PAKET 7, SCHRITT 2. Sie loest pruefen.py ab und traegt den
    ## Nachweis, dass "Acht Striche" keine richtige Antwort hat.
    ## Der Vergleichslauf in Teil e richtet sich nach der Groesse des
    ## Gesamtlaufs: Bei --schnell reichen 60 Durchgaenge je Lage und Gruppe,
    ## um einen toten Pfad zu finden, und mehr braucht die Frage nicht.
    b, g, z, w = probe_laufen(10, "Handgriffe", probe_handgriffe, NS, B,
                              spielordner,
                              min(VERGLEICHSDURCHGAENGE, argumente.durchgaenge))
    proben.append(("10 Handgriffe", b, g, "Auswertungen und Verteilungen", z, w))

    ## ------------------------------------------------------------ 11
    ## SEIT PAKET 8, SCHRITT 2.6. Sie traegt den Nachweis, dass die harte
    ## Sperre gegen Musik auf front und etappe wirklich greift - gemessen an
    ## der Rueckgabe von ton_spielen(), nicht am Ton: renpy.music ist in der
    ## Werkbank eine Attrappe und schluckt jeden Aufruf still.
    b, g, z, w = probe_laufen(11, "Tonprobe", probe_ton, NS, B, spielordner)
    proben.append(("11 Tonprobe", b, g, "Tonaufrufe, Tafelzeilen und Orte",
                   z, w))

    ## EINE PROBE, DIE NICHTS GEMESSEN HAT, IST NICHT "IN ORDNUNG".
    ##
    ## SEIT PAKET 5, SCHRITT 2. Als eine neue Einlage die Werkbank zum
    ## Absturz brachte, meldete probe_laufen() fuer Probe 2 zwar eine
    ## Beanstandung - die Proben 3 und 4 aber liefen anschliessend mit
    ## einem LEEREN Ergebnissatz weiter, fanden darin nichts und
    ## erschienen in der Kurzfassung als "in Ordnung". Sackgassenprobe
    ## und Wertetafel standen also auf gruen, ohne dass ein einziger
    ## Durchgang gespielt worden war.
    ##
    ## Das ist der gefaehrlichste Fehler, den ein Pruefwerkzeug haben
    ## kann, und in dieser Sitzung ist er zweimal aufgetreten: hier und
    ## beim Schuldbuch, das nie schrieb. Deshalb steht ab jetzt in der
    ## Kurzfassung, wenn eine Probe nichts angesehen hat, und der Lauf
    ## gilt als fehlerhaft.
    for name, beanstandungen, geprueft, was, zustand, geschrieben in proben:
        if geprueft == 0:
            kurz.append((name, beanstandungen, "NICHTS GEMESSEN"))
            fehlerhaft = True
        elif not geschrieben:
            ## Regel 11: Ein fehlender Abschnitt ist ein Werkzeugfehler,
            ## kein Erfolg. Bis Paket 5, Schritt 3 war er von einer Probe
            ## ohne Fund nicht zu unterscheiden.
            kurz.append((name, beanstandungen, "AUSGEFALLEN"))
            fehlerhaft = True
        else:
            kurz.append((name, beanstandungen, ""))
        umfang.append((name, geprueft, was))
        if beanstandungen:
            fehlerhaft = True

    ## ------------------------------------------------------- Umfang am Ende
    B.titel("UMFANG DER PRUEFUNG")
    for name, geprueft, was in umfang:
        B("%-20s %10d  %s" % (name, geprueft, was))

    ## ------------------------------------------------------------ Kurzfassung
    kopf = Bericht()

    ## Der Selbsttest steht ueber der Kurzfassung, weil er die Frage
    ## beantwortet, die vor ihr kommt: Hat ueberhaupt jemand hingesehen?
    ## Teil b und c stehen fest, sobald der Aufbau steht; Teil a kann erst
    ## danach entstehen. Gedruckt wird alles zusammen, ganz oben.
    if selbsttest_ausgeben(kopf, NS, proben, argumente.durchgaenge,
                           aufbau.medienbuch):
        fehlerhaft = True

    kopf("=" * 78)
    kopf("KURZFASSUNG")
    kopf("=" * 78)
    ## Eine fehlende Spieldatei ist der schwerste Befund, den diese
    ## Werkbank kennen kann: Was nicht gelesen wird, kann keine Probe
    ## pruefen. Deshalb steht sie ganz oben und nicht erst in Abschnitt A.
    if aufbau.fehlend:
        kopf(">> FEHLT << " + ", ".join(aufbau.fehlend)
             + " - Datei nicht im Spielordner, alle Proben unvollstaendig")
    for name, beanstandungen, zusatz in kurz:
        befund = "in Ordnung" if not beanstandungen else "%d Beanstandungen" % beanstandungen
        kopf("%-20s %-20s %s" % (name, befund, zusatz))
    kopf("GESAMT: " + ("FEHLER - siehe Bericht" if fehlerhaft else "in Ordnung"))
    kopf("=" * 78)

    ## Der Vergleich steht direkt unter der Kurzfassung, weil er dieselbe
    ## Frage beantwortet: Hat sich etwas bewegt, und in welche Richtung?
    if argumente.vergleich:
        vergleich_ausgeben(kopf, argumente.vergleich, kurz, spielordner)

    B.zeilen = kopf.zeilen + B.zeilen
    return B, (1 if fehlerhaft else 0), kurz, umfang


################################################################################
## 14. Vergleich mit einem frueheren Bericht
################################################################################
##
## Gelesen wird ausschliesslich die Kurzfassung des alten Berichts. Sie ist
## das einzige Stueck, dessen Form sich zwischen zwei Paketen nicht aendert,
## und sie enthaelt genau das, worauf es beim Vergleich ankommt.

KURZ_MUSTER = re.compile(
    r"^(?P<name>\S[^ ]*(?: [^ ]+)*?)\s{2,}(?P<befund>in Ordnung|\d+ Beanstandungen)\b")


def kurzfassung_lesen(pfad):
    """Liest Probenname und Zahl der Beanstandungen aus einem Bericht."""
    gefunden = collections.OrderedDict()
    try:
        zeilen = io.open(pfad, encoding="utf-8").read().split("\n")
    except Exception:
        return None
    in_kurzfassung = False
    for zeile in zeilen:
        if zeile.startswith("KURZFASSUNG"):
            in_kurzfassung = True
            continue
        if in_kurzfassung and zeile.startswith("GESAMT:"):
            break
        if not in_kurzfassung:
            continue
        treffer = KURZ_MUSTER.match(zeile)
        if not treffer:
            continue
        name = treffer.group("name").strip()
        befund = treffer.group("befund")
        gefunden[name] = 0 if befund == "in Ordnung" else int(befund.split()[0])
    return gefunden


def vergleich_ausgeben(kopf, pfad, kurz, spielordner):
    if not os.path.isabs(pfad):
        nah = os.path.join(spielordner, pfad)
        if os.path.isfile(nah):
            pfad = nah

    frueher = kurzfassung_lesen(pfad)
    kopf("")
    kopf("=" * 78)
    kopf("VERGLEICH MIT " + os.path.basename(pfad))
    kopf("=" * 78)

    if frueher is None:
        kopf("Die Datei laesst sich nicht lesen: " + pfad)
        kopf("=" * 78)
        return

    kopf("%-20s %10s %10s %10s   %s" % (
        "Probe", "frueher", "heute", "Differenz", "Richtung"))
    for name, heute, _zusatz in kurz:
        alt = frueher.get(name)
        if alt is None:
            kopf("%-20s %10s %10d %10s   neu" % (name, "-", heute, "-"))
            continue
        unterschied = heute - alt
        if unterschied < 0:
            richtung = "besser"
        elif unterschied > 0:
            richtung = ">> SCHLECHTER <<"
        else:
            richtung = "unveraendert"
        kopf("%-20s %10d %10d %+10d   %s" % (name, alt, heute, unterschied, richtung))

    verloren = [n for n in frueher if n not in [k[0] for k in kurz]]
    if verloren:
        kopf("")
        kopf("Im alten Bericht, heute nicht mehr: " + ", ".join(verloren))
    kopf("=" * 78)


def main():
    zerleger = argparse.ArgumentParser(
        description="Prueft den Projektzustand von \"Zwischen Front und Heimat\".")
    zerleger.add_argument("--ordner", default=None,
                          help="Ordner mit den .rpy-Dateien")
    zerleger.add_argument("--durchgaenge", type=int, default=None,
                          help="Durchgaenge je Pfad und Verlauf (Vorgabe 2000)")
    zerleger.add_argument("--schnell", action="store_true",
                          help="Zwischenprobe mit %d statt 2000 Durchgaengen je Lage"
                               % SCHNELL_DURCHGAENGE)
    zerleger.add_argument("--saat", type=int, default=19140801,
                          help="Zufallssaat, damit sich ein Lauf wiederholen laesst")
    zerleger.add_argument("--bericht", default=None,
                          help="Pfad der Berichtsdatei (Vorgabe: bericht.txt daneben)")
    zerleger.add_argument("--vergleich", default=None,
                          help="frueherer Bericht, gegen den gemessen wird")
    argumente = zerleger.parse_args()

    ## --schnell ist eine Zwischenprobe zwischen zwei Arbeitsschritten. Sie
    ## misst dieselben sieben Proben, nur mit weniger Durchgaengen: Die
    ## Bestands-, Beleg-, Medien- und Sprachprobe rechnen ohnehin ohne
    ## Zufall, und fuer die drei uebrigen genuegt zum Zwischenstand eine
    ## grobe Zahl. Eine ausdrueckliche Angabe hat Vorrang.
    if argumente.durchgaenge is None:
        argumente.durchgaenge = SCHNELL_DURCHGAENGE if argumente.schnell else 2000

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    ## Auch ein abgestuerzter Lauf soll einen Bericht hinterlassen. Ohne
    ## das steht der Projektleiter nach einem Fehler mit leeren Haenden da.
    try:
        B, rueckgabe, _kurz, _umfang = hauptlauf(argumente)
    except Exception:
        B = Bericht()
        B.titel("PROBE ALLES - ABGESTUERZT")
        B("Die Werkbank selbst ist stehengeblieben. Der Fehler steht hier;")
        B("die Spieldateien sind unveraendert.")
        B("")
        B(traceback.format_exc())
        rueckgabe = 1
    text = B.text()

    spielordner = spielordner_finden(argumente.ordner)
    ziel = argumente.bericht or os.path.join(spielordner, "bericht.txt")
    with io.open(ziel, "w", encoding="utf-8") as datei:
        datei.write(text)

    sys.stdout.write(text)
    sys.stdout.write("\nBericht geschrieben: %s\n" % ziel)
    return rueckgabe


if __name__ == "__main__":
    sys.exit(main())

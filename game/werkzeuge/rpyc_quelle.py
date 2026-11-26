# -*- coding: utf-8 -*-
"""rpyc_quelle.py - holt den Quelltext aus einer uebersetzten .rpyc zurueck.

    python werkzeuge/rpyc_quelle.py merkbuch.rpyc > merkbuch_roh.rpy

WOZU
Ren'Py laedt eine .rpyc auch dann, wenn die zugehoerige .rpy fehlt. Das
Spiel laeuft dann weiter, aber niemand kann die Datei mehr aendern. Dieses
Werkzeug liest die uebersetzte Fassung und schreibt daraus wieder
lesbaren Quelltext.

WAS ZURUECKKOMMT UND WAS NICHT
Ren'Py legt in der .rpyc den Quelltext jedes Python-Blocks im Klartext ab,
dazu den vollstaendigen Baum aller Bildschirme, Stile, Transformationen,
Marken und Vorgaben - jeweils mit den Ausdruecken so, wie sie geschrieben
wurden. Zurueck kommen deshalb:

    init-Bloecke, default, style, transform, screen, label, call, jump,
    if, return, pass und jede Anweisung fremder Statements (call screen).

Nicht zurueck kommen KOMMENTARE. Ren'Pys Zerleger wirft sie beim
Uebersetzen weg und laesst nur die Leerzeile stehen. Der Aufbau der Datei
bleibt dadurch erhalten, der erklaerende Text nicht. Wer eine so
zurueckgeholte Datei einsetzt, schreibt die Kommentare neu und sagt dazu,
dass sie neu sind.

Ebenfalls nicht zurueck kommt die genaue Zeilenaufteilung innerhalb einer
Bildschirmanweisung: Ob eine Eigenschaft neben dem Tag oder darunter
stand, steht nicht in der uebersetzten Fassung. Das Werkzeug setzt kurze
Anweisungen in eine Zeile und lange in einen Block.

Es wird nichts nachgeladen und nichts installiert: Alles, was hier
gebraucht wird, steht in der Standardbibliothek von Python.
"""

import argparse
import collections
import io
import os
import pickle
import struct
import sys
import zlib


KOPF = b"RENPY RPC2"


################################################################################
## 1. Die Datei aufschliessen
################################################################################


def slot_lesen(pfad, slot):
    """Holt einen der Datenbloecke aus der .rpyc heraus.

    Eine RPYC2-Datei traegt hinter der Kennung eine kleine Tafel aus
    Dreiergruppen: Nummer, Anfang, Laenge. Nummer 0 schliesst sie ab.
    """
    with open(pfad, "rb") as datei:
        kopfdaten = datei.read(1024)

    if kopfdaten[:len(KOPF)] != KOPF:
        ## Aeltere Fassung: die ganze Datei ist ein einziger Block.
        if slot != 1:
            return None
        with open(pfad, "rb") as datei:
            return zlib.decompress(datei.read())

    stelle = len(KOPF)
    while True:
        nummer, anfang, laenge = struct.unpack("III", kopfdaten[stelle:stelle + 12])
        if nummer == slot:
            with open(pfad, "rb") as datei:
                datei.seek(anfang)
                return zlib.decompress(datei.read(laenge))
        if nummer == 0:
            return None
        stelle += 12


################################################################################
## 2. Attrappen fuer die Ren'Py-Klassen
################################################################################
##
## Die .rpyc ist ein Pickle voller Ren'Py-Objekte. Statt Ren'Py zu starten,
## wird fuer jede Klasse eine Attrappe gebaut, die den Zustand annimmt, den
## pickle hineinschreibt. Dadurch laeuft das Werkzeug mit blossem Python.


class Knoten(object):

    def __init__(self, *args, **kwargs):
        pass

    def __setstate__(self, zustand):
        if isinstance(zustand, tuple) and len(zustand) == 2:
            zustand = zustand[1] or {}
        if isinstance(zustand, dict):
            self.__dict__.update(zustand)
        else:
            self.__dict__["_zustand"] = zustand

    def art(self):
        return self.__class__.__name__

    def hole(self, name, ersatz=None):
        return self.__dict__.get(name, ersatz)

    def __repr__(self):
        return "<%s>" % self.__class__.__name__


class PyCode(Knoten):
    """Traegt den Quelltext eines Python-Blocks.

    Der Zustand ist ein Tupel, dessen Laenge sich von Ren'Py-Fassung zu
    Ren'Py-Fassung geaendert hat. Fest ist nur die Reihenfolge: an zweiter
    Stelle steht der Quelltext.
    """

    def __setstate__(self, zustand):
        self.source = None
        if isinstance(zustand, tuple) and len(zustand) >= 2:
            self.source = zustand[1]


def pyexpr(text, *rest):
    """PyExpr ist eine Zeichenkette mit Zusatzangaben. Uns genuegt der Text."""
    return str(text)


ATTRAPPEN = {}

## Ren'Pys ruecknehmbare Behaelter sind gewoehnliche Container.
FESTE_KLASSEN = {
    "RevertableDict": dict,
    "RevertableList": list,
    "RevertableSet": set,
    "OrderedDict": collections.OrderedDict,
    "PyExpr": pyexpr,
    "PyCode": PyCode,
}


def klasse_holen(modul, name):
    if name in FESTE_KLASSEN:
        return FESTE_KLASSEN[name]
    schluessel = (modul, name)
    if schluessel not in ATTRAPPEN:
        ATTRAPPEN[schluessel] = type(str(name), (Knoten,), {"__module__": modul})
    return ATTRAPPEN[schluessel]


class Leser(pickle.Unpickler):

    def find_class(self, modul, name):
        if modul.startswith("renpy") or modul.startswith("store"):
            return klasse_holen(modul, name)
        try:
            return pickle.Unpickler.find_class(self, modul, name)
        except Exception:
            return klasse_holen(modul, name)


def baum_lesen(pfad):
    daten = slot_lesen(pfad, 1)
    if daten is None:
        raise SystemExit("Kein lesbarer Block in " + pfad)
    inhalt = Leser(io.BytesIO(daten)).load()
    if isinstance(inhalt, tuple) and len(inhalt) == 2:
        return inhalt[0], inhalt[1]
    return {}, inhalt


################################################################################
## 3. Kleine Helfer
################################################################################


def ist(knoten, name):
    return isinstance(knoten, Knoten) and knoten.art() == name


def quelltext(pycode):
    if pycode is None:
        return ""
    return pycode.__dict__.get("source") or ""


def argumente_text(info):
    """Baut die Klammer hinter use, call screen oder einem Bildschirm."""
    if info is None:
        return ""
    eintraege = info.hole("arguments", []) or []
    stern = info.hole("starred_indexes", set()) or set()
    doppelstern = info.hole("doublestarred_indexes", set()) or set()
    stuecke = []
    for stelle, eintrag in enumerate(eintraege):
        name, wert = eintrag
        if stelle in stern:
            stuecke.append("*" + str(wert))
        elif stelle in doppelstern:
            stuecke.append("**" + str(wert))
        elif name:
            stuecke.append(str(name) + "=" + str(wert))
        else:
            stuecke.append(str(wert))
    if not stuecke:
        return ""
    return "(" + ", ".join(stuecke) + ")"


def kennwerte_text(signatur):
    """Baut die Klammer hinter einem Bildschirmnamen.

    Steht ueberhaupt eine Unterschrift in der uebersetzten Fassung, dann
    standen in der Quelle auch Klammern - notfalls leere.
    """
    if signatur is None:
        return ""
    felder = signatur.hole("parameters", None)
    if not felder:
        return "()"
    stuecke = []
    for name, feld in felder.items():
        art = feld.hole("kind", 1)
        vorgabe = feld.hole("default", None)
        if art == 2:
            stuecke.append("*" + str(name))
        elif art == 4:
            stuecke.append("**" + str(name))
        elif vorgabe is not None:
            stuecke.append(str(name) + "=" + str(vorgabe))
        else:
            stuecke.append(str(name))
    if not stuecke:
        return ""
    return "(" + ", ".join(stuecke) + ")"


class Blatt(object):
    """Sammelt die Zeilen der neuen Datei."""

    def __init__(self):
        self.zeilen = []

    def __call__(self, text="", tiefe=0):
        if not text:
            self.zeilen.append("")
        else:
            self.zeilen.append("    " * tiefe + text)

    def leerzeile(self):
        if self.zeilen and self.zeilen[-1] != "":
            self.zeilen.append("")

    def text(self):
        return "\n".join(self.zeilen).rstrip() + "\n"


################################################################################
## 4. Python-Bloecke
################################################################################


def python_ausgeben(blatt, knoten, tiefe):
    """Ein Python-Block. Eine Zeile wird zum $, mehrere zum python-Block."""
    text = quelltext(knoten.hole("code"))
    zeilen = text.split("\n")
    voll = [z for z in zeilen if z.strip()]

    if len(voll) == 1 and len(zeilen) <= 2:
        blatt("$ " + voll[0].strip(), tiefe)
        return

    kopf = "python"
    if knoten.hole("hide"):
        kopf += " hide"
    if knoten.hole("store") and knoten.hole("store") != "store":
        kopf += " in " + str(knoten.hole("store")).replace("store.", "")
    blatt(kopf + ":", tiefe)
    einruecken(blatt, text, tiefe + 1)


def einruecken(blatt, text, tiefe):
    """Schreibt einen Quelltextblock mit der gewuenschten Einrueckung.

    Ren'Py legt den Text mit der Einrueckung ab, die er in der Datei
    hatte. Der gemeinsame Vorspann wird abgezogen und neu gesetzt.
    """
    zeilen = text.rstrip().split("\n")
    vorspann = None
    for zeile in zeilen:
        if not zeile.strip():
            continue
        aktuell = len(zeile) - len(zeile.lstrip())
        if vorspann is None or aktuell < vorspann:
            vorspann = aktuell
    if vorspann is None:
        vorspann = 0
    for zeile in zeilen:
        if not zeile.strip():
            blatt("")
        else:
            blatt(zeile[vorspann:], tiefe)


################################################################################
## 5. Bildschirmsprache
################################################################################

## Eigenschaften, die neben dem Tag stehen duerfen, ohne dass die Zeile
## unleserlich wird. Alles andere kommt in den Block darunter.
ZEILENLAENGE = 96


def sl_ausgeben(blatt, knoten, tiefe):
    art = knoten.art()

    if art == "SLScreen":
        kopf = "screen " + str(knoten.hole("name")) + kennwerte_text(knoten.hole("parameters")) + ":"
        blatt(kopf, tiefe)
        for name, wert in (knoten.hole("keyword", []) or []):
            blatt(str(name) + " " + str(wert), tiefe + 1)
        kinder_ausgeben(blatt, knoten.hole("children", []) or [], tiefe + 1)
        return

    if art == "SLDisplayable":
        displayable_ausgeben(blatt, knoten, tiefe)
        return

    if art == "SLBlock":
        for name, wert in (knoten.hole("keyword", []) or []):
            blatt(str(name) + " " + str(wert), tiefe)
        kinder_ausgeben(blatt, knoten.hole("children", []) or [], tiefe)
        return

    if art == "SLIf":
        erste = True
        for bedingung, block in (knoten.hole("entries", []) or []):
            if bedingung is None:
                blatt("else:", tiefe)
            elif erste:
                blatt("if " + str(bedingung) + ":", tiefe)
            else:
                blatt("elif " + str(bedingung) + ":", tiefe)
            erste = False
            sl_ausgeben(blatt, block, tiefe + 1)
        return

    if art == "SLShowIf":
        for bedingung, block in (knoten.hole("entries", []) or []):
            blatt(("showif " + str(bedingung) + ":") if bedingung else "else:", tiefe)
            sl_ausgeben(blatt, block, tiefe + 1)
        return

    if art == "SLFor":
        name = str(knoten.hole("variable"))
        kinder = list(knoten.hole("children", []) or [])
        ## Ein Schleifenkopf mit mehreren Namen wird von Ren'Py in
        ## "_sl2_i" und eine Zuweisung darunter zerlegt. Beides wird hier
        ## wieder zusammengesetzt.
        if name.startswith("_sl2_") and kinder and ist(kinder[0], "SLPython"):
            zuweisung = quelltext(kinder[0].hole("code")).strip()
            if zuweisung.endswith("= " + name):
                name = zuweisung[:-(len(name) + 2)].strip()
                kinder = kinder[1:]
        blatt("for " + name + " in " + str(knoten.hole("expression")) + ":", tiefe)
        kinder_ausgeben(blatt, kinder, tiefe + 1)
        return

    if art == "SLPython":
        text = quelltext(knoten.hole("code"))
        zeilen = [z for z in text.split("\n") if z.strip()]
        if len(zeilen) == 1:
            blatt("$ " + zeilen[0].strip(), tiefe)
        else:
            blatt("python:", tiefe)
            einruecken(blatt, text, tiefe + 1)
        return

    if art == "SLDefault":
        blatt("default " + str(knoten.hole("variable")) + " = "
              + str(knoten.hole("expression")), tiefe)
        return

    if art == "SLUse":
        zeile = "use " + str(knoten.hole("target")) + argumente_text(knoten.hole("args"))
        block = knoten.hole("block")
        if block is None:
            blatt(zeile, tiefe)
        else:
            blatt(zeile + ":", tiefe)
            sl_ausgeben(blatt, block, tiefe + 1)
        return

    if art == "SLTransclude":
        blatt("transclude", tiefe)
        return

    blatt("## nicht zurueckgeholt: " + art, tiefe)


def kinder_ausgeben(blatt, kinder, tiefe):
    if not kinder:
        blatt("pass", tiefe)
        return
    for kind in kinder:
        sl_ausgeben(blatt, kind, tiefe)


def displayable_ausgeben(blatt, knoten, tiefe):
    name = str(knoten.hole("name") or "add")
    stellung = [str(w) for w in (knoten.hole("positional", []) or [])]
    eigenschaften = [(str(n), str(w)) for n, w in (knoten.hole("keyword", []) or [])]
    kinder = knoten.hole("children", []) or []

    kopf = name
    if stellung:
        kopf += " " + " ".join(stellung)

    einzeiler = kopf
    for schluessel, wert in eigenschaften:
        einzeiler += " " + schluessel + " " + wert

    if not kinder and len("    " * tiefe + einzeiler) <= ZEILENLAENGE:
        blatt(einzeiler, tiefe)
        return

    blatt(kopf + ":", tiefe)
    for schluessel, wert in eigenschaften:
        blatt(schluessel + " " + wert, tiefe + 1)
    for kind in kinder:
        sl_ausgeben(blatt, kind, tiefe + 1)
    if not eigenschaften and not kinder:
        blatt("pass", tiefe + 1)


################################################################################
## 6. Bewegung (ATL)
################################################################################


def atl_ausgeben(blatt, block, tiefe):
    if block is None:
        return
    for anweisung in (block.hole("statements", []) or []):
        art = anweisung.art()

        if art == "RawMultipurpose":
            stuecke = []
            warper = anweisung.hole("warp_function") or anweisung.hole("warper")
            if warper:
                stuecke.append(str(warper))
                dauer = anweisung.hole("duration")
                if dauer is not None:
                    stuecke.append(str(dauer))
            for ausdruck, mit in (anweisung.hole("expressions", []) or []):
                stuecke.append(str(ausdruck) + ((" with " + str(mit)) if mit else ""))
            for schluessel, wert in (anweisung.hole("properties", []) or []):
                stuecke.append(str(schluessel) + " " + str(wert))
            for schluessel, werte in (anweisung.hole("splines", []) or []):
                stuecke.append(str(schluessel) + " " + " knot ".join(str(w) for w in werte))
            if stuecke:
                blatt(" ".join(stuecke), tiefe)
            continue

        if art == "RawBlock":
            blatt("block:", tiefe)
            atl_ausgeben(blatt, anweisung, tiefe + 1)
            continue

        if art == "RawParallel":
            for teil in (anweisung.hole("blocks", []) or []):
                blatt("parallel:", tiefe)
                atl_ausgeben(blatt, teil, tiefe + 1)
            continue

        if art == "RawChoice":
            for anteil, teil in (anweisung.hole("choices", []) or []):
                blatt("choice" + ((" " + str(anteil)) if anteil else "") + ":", tiefe)
                atl_ausgeben(blatt, teil, tiefe + 1)
            continue

        if art == "RawOn":
            for name, teil in (anweisung.hole("handlers", {}) or {}).items():
                blatt("on " + str(name) + ":", tiefe)
                atl_ausgeben(blatt, teil, tiefe + 1)
            continue

        if art == "RawTime":
            blatt("time " + str(anweisung.hole("time")), tiefe)
            continue

        if art == "RawRepeat":
            wiederholt = anweisung.hole("repeats")
            blatt("repeat" + ((" " + str(wiederholt)) if wiederholt else ""), tiefe)
            continue

        if art == "RawFunction":
            blatt("function " + str(anweisung.hole("expr")), tiefe)
            continue

        if art == "RawEvent":
            blatt("event " + str(anweisung.hole("name")), tiefe)
            continue

        if art == "RawContainsExpr":
            blatt("contains " + str(anweisung.hole("expression")), tiefe)
            continue

        blatt("## nicht zurueckgeholt: " + art, tiefe)


################################################################################
## 7. Marken und Anweisungen
################################################################################


def anweisung_ausgeben(blatt, knoten, tiefe):
    art = knoten.art()

    if art == "Python":
        python_ausgeben(blatt, knoten, tiefe)
        return

    if art == "UserStatement":
        blatt(str(knoten.hole("line", "")), tiefe)
        return

    if art == "If":
        erste = True
        for bedingung, block in (knoten.hole("entries", []) or []):
            if bedingung is None or str(bedingung) == "True":
                blatt("else:" if not erste else "if True:", tiefe)
            elif erste:
                blatt("if " + str(bedingung) + ":", tiefe)
            else:
                blatt("elif " + str(bedingung) + ":", tiefe)
            erste = False
            for unter in block_ohne_rueckkehrmarken(block):
                anweisung_ausgeben(blatt, unter, tiefe + 1)
        return

    if art == "While":
        blatt("while " + str(knoten.hole("condition")) + ":", tiefe)
        for unter in block_ohne_rueckkehrmarken(knoten.hole("block", []) or []):
            anweisung_ausgeben(blatt, unter, tiefe + 1)
        return

    if art == "Call":
        zeile = "call "
        if knoten.hole("expression"):
            zeile += "expression " + str(knoten.hole("label"))
        else:
            zeile += str(knoten.hole("label"))
        zeile += argumente_text(knoten.hole("arguments"))
        blatt(zeile, tiefe)
        return

    if art == "Jump":
        if knoten.hole("expression"):
            blatt("jump expression " + str(knoten.hole("target")), tiefe)
        else:
            blatt("jump " + str(knoten.hole("target")), tiefe)
        return

    if art == "Return":
        ausdruck = knoten.hole("expression")
        blatt("return" + ((" " + str(ausdruck)) if ausdruck else ""), tiefe)
        return

    if art == "Pass":
        blatt("pass", tiefe)
        return

    if art == "Scene":
        blatt("scene " + " ".join(str(t) for t in (knoten.hole("imspec") or [[]])[0]), tiefe)
        return

    if art == "Say":
        wer = knoten.hole("who")
        was = knoten.hole("what")
        blatt(((str(wer) + " ") if wer else "") + '"' + str(was) + '"', tiefe)
        return

    blatt("## nicht zurueckgeholt: " + art, tiefe)


def marke_ausgeben(blatt, knoten, tiefe):
    name = knoten.hole("_name") or knoten.hole("name") or "ohne_namen"
    kopf = "label " + str(name)
    felder = knoten.hole("parameters")
    if felder is not None:
        kopf += kennwerte_text(felder)
    blatt(kopf + ":", tiefe)
    blatt()
    for unter in block_ohne_rueckkehrmarken(knoten.hole("block", []) or []):
        anweisung_ausgeben(blatt, unter, tiefe + 1)
        blatt()


def block_ohne_rueckkehrmarken(block):
    """Wirft die Pass-Knoten weg, die Ren'Py hinter jedes call setzt.

    Ein "call" braucht eine Stelle, an die es zurueckkehrt. Ren'Py legt
    dafuer beim Uebersetzen einen Pass-Knoten an, der in der Quelle nicht
    stand. Bliebe er stehen, waere die zurueckgeholte Datei zwar lauffaehig,
    aber sie behauptete etwas, das nie geschrieben wurde.
    """
    sauber = []
    vorher_call = False
    for knoten in block:
        if vorher_call and ist(knoten, "Pass"):
            vorher_call = False
            continue
        vorher_call = ist(knoten, "Call")
        sauber.append(knoten)
    return sauber


################################################################################
## 8. Die Datei zusammensetzen
################################################################################
##
## Ren'Py legt jede default-, style-, transform- und screen-Anweisung in
## einen Init-Block. Der dort gespeicherte Rang ist der geschriebene Rang
## PLUS dem "init offset", der zu dieser Stelle galt. Aus dem Rang laesst
## sich der Versatz also zurueckrechnen, und die Zeile "init offset = N"
## wird an der richtigen Stelle wieder eingesetzt.

## Grundrang der einzelnen Anweisungsarten ohne Versatz.
GRUNDRANG = {
    "Default": 0,
    "Define": 0,
    "Style": 0,
    "Transform": 0,
    "Screen": -500,
    "Image": 990,
    "Testcase": 500,
}


def versatz_fuer(knoten, rang):
    art = knoten.art()
    if art in GRUNDRANG:
        return rang - GRUNDRANG[art]
    ## Python-Bloecke tragen ihren Rang selbst; sie kommen ohne Versatz aus.
    return 0


def datei_bauen(stmts, quelle):
    blatt = Blatt()

    blatt("################################################################################")
    blatt("##")
    blatt("##  Zurueckgeholt aus " + os.path.basename(quelle))
    blatt("##")
    blatt("##  Erzeugt von werkzeuge/rpyc_quelle.py. Der Aufbau, alle Ausdruecke und")
    blatt("##  aller Python-Quelltext stammen aus der uebersetzten Fassung. Die")
    blatt("##  KOMMENTARE der Urfassung sind verloren: Ren'Py wirft sie beim")
    blatt("##  Uebersetzen weg. Wer diese Datei einsetzt, schreibt sie neu.")
    blatt("##")
    blatt("################################################################################")
    blatt()

    versatz = 0

    for knoten in stmts:
        if ist(knoten, "Init"):
            block = knoten.hole("block", []) or []
            rang = knoten.hole("priority", 0)

            ## Ein Init-Block, der nur Python enthaelt, wurde auch so
            ## geschrieben. Alles andere ist von Ren'Py umschlossen worden.
            if len(block) == 1 and not ist(block[0], "Python"):
                inneres = block[0]
                gewuenscht = versatz_fuer(inneres, rang)
                if gewuenscht != versatz:
                    blatt.leerzeile()
                    blatt("init offset = " + str(gewuenscht))
                    blatt()
                    versatz = gewuenscht
                knoten_ausgeben(blatt, inneres)
                continue

            if versatz != 0:
                blatt.leerzeile()
                blatt("init offset = 0")
                blatt()
                versatz = 0

            blatt.leerzeile()
            kopf = "init" if rang == 0 else ("init " + str(rang))
            if len(block) == 1 and ist(block[0], "Python"):
                anweisung = block[0]
                zusatz = " hide" if anweisung.hole("hide") else ""
                blatt(kopf + zusatz + " python:")
                einruecken(blatt, quelltext(anweisung.hole("code")), 1)
                blatt()
                continue

            blatt(kopf + ":")
            blatt()
            for unter in block:
                anweisung_ausgeben(blatt, unter, 1)
            blatt()
            continue

        if versatz != 0:
            blatt.leerzeile()
            blatt("init offset = 0")
            blatt()
            versatz = 0

        knoten_ausgeben(blatt, knoten)

    return blatt.text()


def knoten_ausgeben(blatt, knoten):
    art = knoten.art()

    if art == "Default":
        blatt.leerzeile()
        blatt("default " + str(knoten.hole("varname")) + " = "
              + quelltext(knoten.hole("code")))
        return

    if art == "Define":
        blatt.leerzeile()
        speicher = knoten.hole("store", "store")
        vorspann = "" if speicher in (None, "store") else str(speicher).replace("store.", "") + " "
        blatt("define " + vorspann + str(knoten.hole("varname")) + " = "
              + quelltext(knoten.hole("code")))
        return

    if art == "Style":
        blatt.leerzeile()
        kopf = "style " + str(knoten.hole("style_name"))
        eltern = knoten.hole("parent")
        if eltern:
            kopf += " is " + str(eltern)
        variante = knoten.hole("variant")
        eigenschaften = knoten.hole("properties", {}) or {}
        if not eigenschaften and not variante:
            blatt(kopf)
            return
        blatt(kopf + ":")
        if knoten.hole("clear"):
            blatt("clear", 1)
        if knoten.hole("take"):
            blatt("take " + str(knoten.hole("take")), 1)
        for name in (knoten.hole("delattr", []) or []):
            blatt("del " + str(name), 1)
        if variante and str(variante) != "None":
            blatt("variant " + str(variante), 1)
        for name, wert in eigenschaften.items():
            blatt(str(name) + " " + str(wert), 1)
        blatt()
        return

    if art == "Transform":
        blatt.leerzeile()
        kopf = "transform " + str(knoten.hole("varname"))
        felder = knoten.hole("parameters")
        if felder is not None:
            kopf += kennwerte_text(felder)
        blatt(kopf + ":")
        atl_ausgeben(blatt, knoten.hole("atl"), 1)
        blatt()
        return

    if art == "Screen":
        blatt.leerzeile()
        sl_ausgeben(blatt, knoten.hole("screen"), 0)
        blatt()
        return

    if art == "Label":
        blatt.leerzeile()
        marke_ausgeben(blatt, knoten, 0)
        return

    if art == "Return":
        return

    if art == "Init":
        for unter in (knoten.hole("block", []) or []):
            knoten_ausgeben(blatt, unter)
        return

    blatt.leerzeile()
    blatt("## nicht zurueckgeholt: " + art)


################################################################################
## 9. Aufruf
################################################################################


def main():
    zerleger = argparse.ArgumentParser(
        description="Holt den Quelltext aus einer uebersetzten .rpyc zurueck.")
    zerleger.add_argument("datei", help="Pfad zur .rpyc")
    zerleger.add_argument("--ziel", default=None,
                          help="Datei, in die geschrieben wird (sonst Standardausgabe)")
    argumente = zerleger.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    _kopf, stmts = baum_lesen(argumente.datei)
    text = datei_bauen(stmts, argumente.datei)

    if argumente.ziel:
        with io.open(argumente.ziel, "w", encoding="utf-8") as datei:
            datei.write(text)
        sys.stdout.write("Geschrieben: %s (%d Zeilen)\n"
                         % (argumente.ziel, text.count("\n")))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

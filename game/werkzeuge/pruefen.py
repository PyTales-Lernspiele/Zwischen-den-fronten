# -*- coding: utf-8 -*-
"""Prüft die Python-Anteile von minispiele.rpy ausserhalb von Ren'Py.

Extrahiert alle 'init N python:'-Bloecke, fuehrt sie mit Platzhaltern fuer
die uebrigen Projektdateien aus und rechnet danach jede Auswertung mit
vielen Eingaben durch.
"""

import io
import re
import random
import textwrap

QUELLE = "minispiele.rpy"


def bloecke_lesen(pfad):
    zeilen = io.open(pfad, encoding="utf-8").read().split("\n")
    bloecke = []
    aktuell = None
    for zeile in zeilen:
        if re.match(r"^init\b.*python:\s*$", zeile):
            aktuell = []
            bloecke.append(aktuell)
            continue
        if aktuell is None:
            continue
        if zeile.strip() == "":
            aktuell.append("")
            continue
        if zeile.startswith("    "):
            aktuell.append(zeile[4:])
            continue
        aktuell = None
    return ["\n".join(b) for b in bloecke]


class Platzhalter(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


# ---------------------------------------------------------------- Platzhalter

class RenpyStub(object):
    random = random

    @staticmethod
    def has_screen(name):
        return True

    @staticmethod
    def call_screen(name, *a, **kw):
        return None


NS = {}

NS["renpy"] = RenpyStub()
NS["config"] = Platzhalter(label_overrides={})
NS["persistent"] = Platzhalter(analysemodus=True)

NS["aktuelles_jahr"] = 1916
NS["aktueller_pfad"] = "heimat"
NS["spielmodus"] = "lang"
NS["merkmale"] = []
NS["protokoll"] = []
NS["einlagen_gespielt"] = []
NS["einlagen_im_kapitel"] = 0
NS["einlagen_seit"] = 0
NS["einlage_jahr"] = 0
NS["einlage_zuletzt"] = None
NS["einlage_aktuell"] = None
NS["einlage_lage"] = {}
NS["einlage_ergebnis"] = None
NS["einlage_ausgang_saetze"] = []
NS["einlagen_erlaubt"] = True
NS["MERKMALS_REIHENFOLGE"] = ["offizier", "adel", "buergertum", "lazarett",
                              "ruestung", "arbeiterschaft", "landbevoelkerung"]
NS["PFAD_REIHENFOLGE"] = ["front", "etappe", "heimat"]
NS["EREIGNIS_INDEX"] = {}
NS["TABU_BEGRIFFE"] = [("Wehrkraftzersetzung", "NS"), ("Strafkompanie", "NS"),
                       ("Volksgemeinschaft", "NS"), ("Endsieg", "NS"),
                       ("Blitzkrieg", "2. WK"), ("Landser", "2. WK"),
                       ("Untermensch", "NS"), ("Konzentrationslager", "Epoche"),
                       ("Gestapo", "Epoche"), ("Führerbefehl", "Epoche")]
NS["PRUEF_BEGRIFFE"] = [("Heimatfront", "2. WK"), ("totaler Krieg", "Zwischenkriegszeit"),
                        ("Weltkrieg", "zeitgenoessisch anders"), ("Trauma", "spaeter Begriff"),
                        ("Drückeberger", "nur woertliche Rede"), ("Nazi", "Epoche")]


def pfad_liste(angabe):
    if angabe is None:
        return list(NS["PFAD_REIHENFOLGE"])
    if isinstance(angabe, (list, tuple)):
        return list(angabe)
    if angabe == "beide":
        return list(NS["PFAD_REIHENFOLGE"])
    return [angabe]


def hat_merkmal(name):
    return name in NS["merkmale"]


def jahrestext(wert, jahr):
    if not isinstance(wert, dict):
        return wert
    return wert.get(jahr, wert.get("standard", list(wert.values())[0]))


def variante(vorgaben, standard=""):
    if not isinstance(vorgaben, dict):
        return vorgaben
    for name in NS["MERKMALS_REIHENFOLGE"]:
        if hat_merkmal(name):
            zusammen = str(NS["aktueller_pfad"]) + ":" + name
            if zusammen in vorgaben:
                return vorgaben[zusammen]
    for name in NS["MERKMALS_REIHENFOLGE"]:
        if hat_merkmal(name) and name in vorgaben:
            return vorgaben[name]
    if NS["aktueller_pfad"] in vorgaben:
        return vorgaben[NS["aktueller_pfad"]]
    if NS["aktueller_pfad"] == "etappe" and "front" in vorgaben:
        return vorgaben["front"]
    if "standard" in vorgaben:
        return vorgaben["standard"]
    return standard


def briefwelt():
    return "heimat" if NS["aktueller_pfad"] == "heimat" else "front"


def welttext(vorgaben):
    if not isinstance(vorgaben, dict):
        return vorgaben
    if NS["aktueller_pfad"] in vorgaben:
        ergebnis = vorgaben[NS["aktueller_pfad"]]
    elif briefwelt() in vorgaben:
        ergebnis = vorgaben[briefwelt()]
    else:
        ergebnis = vorgaben.get("standard", "")
    if isinstance(ergebnis, dict):
        ergebnis = jahrestext(ergebnis, NS["aktuelles_jahr"])
    return ergebnis


FIGUREN = {"kind": True, "naechste": True}
BINDUNG = {}


def figur_lebt(k):
    return FIGUREN.get(k, False)


def figur_ist_fort(k):
    return False


def figur_name(k):
    return {"kind": "Das Kind", "naechste": "Die Nachbarin"}.get(k, k)


def figur_zusatz(k):
    return "aus dem Erdgeschoss"


def figur_setzen(k, verbundenheit=None, **kw):
    BINDUNG[k] = BINDUNG.get(k, 0) + (verbundenheit or 0)


WERTE = {"versorgung": 6, "belastung": 2, "aufmerksamkeit": 1, "rueckhalt": 8}
LETZTE = {}


def zustand_aendern(aenderungen):
    LETZTE.clear()
    LETZTE.update(aenderungen or {})
    for k, v in (aenderungen or {}).items():
        WERTE[k] = WERTE[k] + v


def merkmal_setzen(name):
    if name and name not in NS["merkmale"]:
        NS["merkmale"].append(name)


def protokoll_eintragen(kennung, wahl):
    NS["protokoll"].append((kennung, wahl))


def ereignis_vormerken(kennung, ab_jahr):
    pass


def ort_text():
    return "Wohnviertel"


def gewichtet_ziehen(eintraege, gewicht_von):
    gesamt = sum(max(1, gewicht_von(e)) for e in eintraege)
    wurf = random.randint(1, gesamt)
    laufend = 0
    for e in eintraege:
        laufend += max(1, gewicht_von(e))
        if wurf <= laufend:
            return e
    return eintraege[-1]


def texte_sammeln(gegenstand):
    gefunden = []
    if gegenstand is None:
        return gefunden
    if isinstance(gegenstand, str):
        gefunden.append(gegenstand)
    elif isinstance(gegenstand, dict):
        for wert in gegenstand.values():
            gefunden.extend(texte_sammeln(wert))
    elif isinstance(gegenstand, (list, tuple)):
        for wert in gegenstand:
            gefunden.extend(texte_sammeln(wert))
    return gefunden


def sprachpruefung_durchfuehren():
    return []


def zustand_zuruecksetzen():
    pass


for name, wert in list(locals().items()):
    if callable(wert) and not name.startswith("_") and name not in ("bloecke_lesen",):
        NS[name] = wert

# ---------------------------------------------------------------- ausfuehren

bloecke = bloecke_lesen(QUELLE)
print("Python-Bloecke gefunden:", len(bloecke))

for nummer, block in enumerate(bloecke):
    try:
        exec(compile(block, "<block %d>" % nummer, "exec"), NS)
    except Exception as fehler:
        print("FEHLER in Block", nummer)
        print(block[:400])
        raise

print("Alle Bloecke ausgefuehrt.")
print("Einlagen im Bestand:", [e.kennung for e in NS["EINLAGEN"]])
print("Anschluesse:", sorted(NS["EINLAGE_ANSCHLUSS"].keys()))


# ---------------------------------------------------------------- Durchlauf

import itertools

fehler_liste = []
wertsummen = {}

def lage_setzen(pfad, merkmale, kennung):
    NS["aktueller_pfad"] = pfad
    NS["merkmale"] = list(merkmale)
    NS["einlage_vorbereiten"](kennung)

def pruefe(kennung, eingaben, pfade, merkmalsaetze):
    global fehler_liste
    for pfad in pfade:
        for satz in merkmalsaetze:
            for eingabe in eingaben:
                lage_setzen(pfad, satz, kennung)
                try:
                    ergebnis = NS["EINLAGE_AUSWERTEN"][kennung](eingabe)
                except Exception as f:
                    fehler_liste.append((kennung, pfad, satz, eingabe, repr(f)))
                    continue
                aenderungen = NS["einlage_begrenzen"](ergebnis.get("aenderungen", {}))
                for schluessel, betrag in aenderungen.items():
                    if schluessel not in ("versorgung", "belastung", "aufmerksamkeit", "rueckhalt"):
                        fehler_liste.append((kennung, "unbekannter Wert", schluessel))
                    wertsummen.setdefault((kennung, schluessel), []).append(betrag)
                if not ergebnis.get("saetze"):
                    fehler_liste.append((kennung, pfad, satz, eingabe, "keine Saetze"))
                for s in ergebnis.get("saetze", []):
                    if not isinstance(s, str) or not s.strip():
                        fehler_liste.append((kennung, "leerer Satz", eingabe))
                if not ergebnis.get("protokoll"):
                    fehler_liste.append((kennung, "kein Protokolleintrag", eingabe))

merkmalsaetze = [[], ["offizier"], ["buergertum"], ["arbeiterschaft"], ["ruestung", "arbeiterschaft"], ["adel"], ["lazarett"]]

# Rotstift: alle Teilmengen von sechs Zeilen
alle_rotstift = []
for groesse in range(7):
    for kombi in itertools.combinations(range(6), groesse):
        alle_rotstift.append(kombi)
pruefe("rotstift", alle_rotstift, ["front", "etappe", "heimat"], merkmalsaetze)

# Portionen: alle Aufteilungen von acht Teilen auf vier Empfaenger
alle_portionen = []
for a in range(9):
    for b in range(9 - a):
        for c in range(9 - a - b):
            d = 8 - a - b - c
            alle_portionen.append((a, b, c, d))
pruefe("portionen", alle_portionen, ["front", "heimat"], merkmalsaetze)

# Hamsterfahrt
alle_hamster = []
for gegeben in [(), (0,), (0, 1), (0, 1, 2), (0, 1, 2, 3), (3,), (2, 3)]:
    for pfund in [0, 10, 12, 14, 22, 24, 36]:
        for verhalten in ["keine", "zeigen", "verbergen"]:
            alle_hamster.append((gegeben, pfund, verhalten))
pruefe("hamsterfahrt", alle_hamster, ["heimat"], merkmalsaetze)

# Tornister: alle Teilmengen der acht Stuecke
kennungen = [s["kennung"] for s in NS["TORNISTER_STUECKE"]]
alle_tornister = []
for groesse in range(9):
    for kombi in itertools.combinations(kennungen, groesse):
        alle_tornister.append(kombi)
pruefe("tornister", alle_tornister, ["front", "etappe"], merkmalsaetze)

print()
print("Durchlaeufe je Einlage geprueft.")
print("Fehler:", len(fehler_liste))
for f in fehler_liste[:20]:
    print("  ", f)

print()
print("Spannweite der Wertaenderungen (nach Begrenzung):")
for (kennung, schluessel), werte in sorted(wertsummen.items()):
    print("   %-14s %-15s min %+d  max %+d" % (kennung, schluessel, min(werte), max(werte)))


# ------------------------------------------------- Zwei-Saetze-Regel und Woerter

print()
print("Zwei-Saetze-Regel:")
for vorlage in NS["EINLAGEN"]:
    fassungen = vorlage.einordnung
    paare = list(fassungen.items()) if isinstance(fassungen, dict) else [("standard", fassungen)]
    for name, text in paare:
        anzahl = NS["satzzahl"](text)
        marke = "ok " if anzahl == 2 else "!! "
        print("   %s%-14s %-8s %d Saetze, %d Zeichen" % (marke, vorlage.kennung, name, anzahl, len(text)))

print()
print("Wertungswoerter und Tabubegriffe in allen Texten:")
NS["aktueller_pfad"] = "heimat"
NS["merkmale"] = []
funde = NS["sprachpruefung_durchfuehren"]()
if not funde:
    print("   keine Funde")
for f in funde:
    print("   ", f[0], "|", f[1], "|", f[2], "|", f[4][:70])

# Zweiter Durchlauf mit Frontfassung
print()
print("Dasselbe mit Frontfassung und Offizier:")
NS["aktueller_pfad"] = "front"
NS["merkmale"] = ["offizier"]
funde = NS["sprachpruefung_durchfuehren"]()
if not funde:
    print("   keine Funde")
for f in funde:
    print("   ", f[0], "|", f[1], "|", f[2], "|", f[4][:70])


# ---------------------------------------------------------------- Ziehprobe

print()
print("Ziehprobe: 400 Durchgaenge, je Kapitel vier Ereignisse")

NS["EREIGNIS_INDEX"] = {k: object() for k in [
    "front_1914_marsch", "front_1914_schanzen", "front_feldpost", "front_ruhequartier",
    "front_1916_hunger", "front_kamerad", "front_gas", "front_beute",
    "heimat_brotschlange", "heimat_1914_post", "heimat_1915_brotkarte",
    "heimat_1916_zensur", "heimat_hamsterfahrt", "heimat_sonntag", "heimat_fabrik",
    "einstieg_meldung", "einstieg_abschied"]}

FRONT_EREIGNISSE = ["front_1914_marsch", "front_feldpost", "front_ruhequartier",
                    "front_kamerad", "front_gas", "front_beute", "front_1916_hunger"]
HEIMAT_EREIGNISSE = ["heimat_brotschlange", "heimat_1914_post", "heimat_1915_brotkarte",
                     "heimat_1916_zensur", "heimat_sonntag", "heimat_fabrik"]

def durchgang(pfad, modus):
    NS["aktueller_pfad"] = pfad
    NS["spielmodus"] = modus
    NS["merkmale"] = []
    NS["einlagen_gespielt"] = []
    NS["einlagen_im_kapitel"] = 0
    NS["einlagen_seit"] = 0
    NS["einlage_jahr"] = 0
    NS["einlage_zuletzt"] = None
    gespielt = []
    je_kapitel = {}
    abstaende = []
    seit = 0
    for jahr in [1914, 1915, 1916, 1917, 1918]:
        NS["aktuelles_jahr"] = jahr
        quelle = FRONT_EREIGNISSE if pfad != "heimat" else HEIMAT_EREIGNISSE
        for ereignis in random.sample(quelle, 4):
            seit += 1
            kennung = NS["einlage_ziehen"](ereignis)
            if kennung:
                # so wie das Label es tut
                for name in ([NS["EINLAGE_INDEX"][kennung].merkmal] if NS["EINLAGE_INDEX"][kennung].merkmal else []):
                    NS["merkmale"].append(name)
                NS["einlage_vermerken"](kennung)
                gespielt.append((jahr, kennung))
                je_kapitel[jahr] = je_kapitel.get(jahr, 0) + 1
                abstaende.append(seit)
                seit = 0
    return gespielt, je_kapitel, abstaende

verstoesse = []
gesamt = []
for lauf in range(400):
    for pfad in ["front", "etappe", "heimat"]:
        for modus in ["kurz", "lang"]:
            gespielt, je_kapitel, abstaende = durchgang(pfad, modus)
            gesamt.append(len(gespielt))
            grenze = NS["EINLAGEN_JE_KAPITEL"][modus]
            for jahr, anzahl in je_kapitel.items():
                if anzahl > grenze:
                    verstoesse.append(("zu viele im Kapitel", pfad, modus, jahr, anzahl))
            for abstand in abstaende:
                if abstand <= NS["EINLAGE_ABSTAND"]:
                    verstoesse.append(("zu dicht", pfad, modus, abstand))
            for stelle in range(1, len(gespielt)):
                if gespielt[stelle][1] == gespielt[stelle - 1][1]:
                    verstoesse.append(("zweimal dieselbe", pfad, modus, gespielt[stelle]))
            for jahr, kennung in gespielt:
                vorlage = NS["EINLAGE_INDEX"][kennung]
                if jahr not in vorlage.jahre:
                    verstoesse.append(("falsches Jahr", kennung, jahr))
                if pfad not in vorlage.pfad:
                    verstoesse.append(("falscher Pfad", kennung, pfad))

print("   Verstoesse:", len(verstoesse))
for v in verstoesse[:10]:
    print("   ", v)
print("   Einlagen je Durchgang: min %d, im Schnitt %.1f, max %d" % (
    min(gesamt), sum(gesamt) / float(len(gesamt)), max(gesamt)))

# Wie oft kommt gar keine?
ohne = len([g for g in gesamt if g == 0])
print("   Durchgaenge ohne jede Einlage: %d von %d" % (ohne, len(gesamt)))

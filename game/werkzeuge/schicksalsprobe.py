# -*- coding: utf-8 -*-
"""Schicksalsprobe zu Paket 4 - Werkzeug fuer die Entwicklung.

Laeuft AUSSERHALB von Ren'Py, direkt mit Python 3:

    python3 schicksalsprobe.py

Die Datei liest figuren.rpy ein, fuehrt nur deren Python-Bloecke aus und
simuliert dann 3000 Durchgaenge je Pfad. Damit laesst sich ohne einen
einzigen Spieldurchlauf pruefen, ob die drei Zusagen aus dem Kopf von
figuren.rpy noch stimmen:

  1. Kein Schicksal ist sicher und keines ganz abwendbar.
     -> keine Figur steht bei 0 oder 100 Prozent.
  2. Post kommt unregelmaessig, aber sie bleibt nicht aus.
     -> "Durchgaenge ganz ohne Post" muss 0 sein.
  3. Die Verbundenheit veraendert die Sterblichkeit nicht.
     -> die beiden Zeilen unter "Verbundenheit gesamt am Ende" muessen
        dicht beieinander liegen.

Wer Wahrscheinlichkeiten in SCHICKSALE aendert, laesst dieses Werkzeug
danach noch einmal laufen. Es erwartet figuren.rpy im selben Ordner.
"""
import re, io, random, collections

lines = io.open("figuren.rpy", encoding="utf-8").read().split("\n")

def bloecke():
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if re.match(r'^init(\s+-?\d+)?\s+python:\s*$', l):
            body, j = [], i + 1
            while j < len(lines):
                cur = lines[j]
                if cur.strip() == "":
                    body.append(""); j += 1; continue
                if cur.startswith("    "):
                    body.append(cur[4:]); j += 1
                else:
                    break
            out.append((l.strip(), "\n".join(body)))
            i = j
        else:
            i += 1
    return out

class Renpy(object):
    random = random

G = {}
G["renpy"] = Renpy()
G["KAPITEL_JAHRE"] = [1914, 1915, 1916, 1917, 1918, 1919]
G["aktuelles_jahr"] = 1914
G["aktueller_pfad"] = "heimat"
G["persistent"] = type("P", (), {"analysemodus": False})()
G["config"] = type("C", (), {"label_overrides": {}})()
for _v, _w in [("figuren_zustand", {}), ("schicksals_stand", {}), ("figuren_verlauf", []),
               ("post_offen", []), ("post_gelesen", []), ("post_zaehler", 0),
               ("post_letzter", None), ("post_im_jahr", 0)]:
    G[_v] = _w

class Lage(object):
    vorname = "Marie"
    geschlecht = "w"
G["lebenslage"] = Lage()

def jahrestext(wert, jahr):
    if not isinstance(wert, dict):
        return wert
    return wert.get(jahr, list(wert.values())[0])
G["jahrestext"] = jahrestext
G["gebeugt"] = lambda m, w: w
G["werte_log"] = collections.Counter()
def zustand_aendern(d):
    for k, v in (d or {}).items():
        G["werte_log"][k] += v
G["zustand_aendern"] = zustand_aendern
def gewichtet_ziehen(eintraege, gewicht_von):
    gesamt = sum(max(1, gewicht_von(e)) for e in eintraege)
    wurf = random.randint(1, gesamt)
    lauf = 0
    for e in eintraege:
        lauf += max(1, gewicht_von(e))
        if wurf <= lauf:
            return e
    return eintraege[-1]
G["gewichtet_ziehen"] = gewichtet_ziehen
G["protokoll_eintragen"] = lambda a, b: None
NAMEN = {
    "naechste": {"front": "Dein Nebenmann", "heimat": "Die Nachbarin"},
    "kind": {"front": "Der Jüngste", "heimat": "Das Kind"},
    "kundige": {"front": "Der Landwehrmann", "heimat": "Die Frau aus dem Hinterhaus"},
    "amtsperson": {"front": "Der Feldwebel", "heimat": "Der Beamte"},
    "gegenseite": {"front": "Der Mann von drüben", "heimat": "Die Frau aus dem Vorderhaus"},
}
G["figur_name"] = lambda k: NAMEN[k]["heimat" if G["aktueller_pfad"] == "heimat" else "front"]
G["figur_zusatz"] = lambda k: ""
G["zustand_zuruecksetzen"] = lambda: None
G["ende_zusammenstellen"] = lambda: {"eintraege": [
    {"jahr": 1918, "marke": "November 1918", "text": "x", "quelle": "Kriegsende"},
    {"jahr": 1919, "marke": "1919", "text": "y", "quelle": "Ausgang"},
    {"jahr": 1919, "marke": "28. Juni 1919", "text": "z", "quelle": "Versailles"},
]}

for kopf, code in bloecke():
    if kopf.startswith("init 4"):
        continue
    exec(compile(code, kopf, "exec"), G)

DURCHGAENGE = 3000
EREIGNISSE_JE_JAHR = {1914: 5, 1915: 5, 1916: 7, 1917: 6, 1918: 7, 1919: 2}

for pfad in ("front", "heimat"):
    G["aktueller_pfad"] = pfad
    tot = collections.Counter()
    endzustand = collections.defaultdict(collections.Counter)
    briefe_gesamt = []
    ohne_brief = 0
    luecken = []
    naehe_tot = []
    naehe_lebt = []
    totzahl = collections.Counter()

    for lauf in range(DURCHGAENGE):
        G["aktuelles_jahr"] = 1914
        G["figuren_anlegen"]()
        briefe = 0
        letzte = 0
        maxluecke = 0
        laufende = 0

        for jahr in G["KAPITEL_JAHRE"]:
            G["aktuelles_jahr"] = jahr
            if jahr > 1914:
                G["schicksale_wuerfeln"]()
            for _ in range(EREIGNISSE_JE_JAHR[jahr]):
                laufende += 1
                G["post_zaehler"] = G["post_zaehler"] + 1
                brief = G["brief_ziehen"]()
                if brief is None:
                    continue
                G["brief_zustellen"](brief)
                briefe += 1
                maxluecke = max(maxluecke, laufende - letzte)
                letzte = laufende
                vorlage = G["BRIEF_INDEX"].get(brief["kennung"])
                if vorlage is not None and vorlage.antworten:
                    G["brief_beantworten"](brief, random.randint(0, 1))

        briefe_gesamt.append(briefe)
        luecken.append(maxluecke)
        if briefe == 0:
            ohne_brief += 1
        for k in G["FIGUREN_REIHENFOLGE"]:
            e = G["figur_zustand"](k)
            endzustand[k][e["zustand"]] += 1
            if e["zustand"] == "gefallen":
                tot[k] += 1
        gesamt_naehe = sum(G["figur_zustand"](k)["verbundenheit"] for k in G["FIGUREN_REIHENFOLGE"])
        gesamt_tot = sum(1 for k in G["FIGUREN_REIHENFOLGE"] if G["figur_zustand"](k)["zustand"] == "gefallen")
        (naehe_tot if gesamt_tot >= 2 else naehe_lebt).append(gesamt_naehe)
        totzahl[gesamt_tot] += 1

    print("=" * 74)
    print("PFAD:", pfad, " (%d Durchgaenge)" % DURCHGAENGE)
    print("-" * 74)
    print("Briefe je Durchgang:  Mittel %.1f   wenigste %d   meiste %d" % (
        sum(briefe_gesamt) / float(DURCHGAENGE), min(briefe_gesamt), max(briefe_gesamt)))
    print("Durchgaenge ganz ohne Post: %d" % ohne_brief)
    print("groesste Luecke zwischen zwei Briefen (Ereignisse): Mittel %.1f  hoechstens %d" % (
        sum(luecken) / float(DURCHGAENGE), max(luecken)))
    print()
    print("Verluste je Durchgang:  " + "   ".join(
        "%d Tote %.0f%%" % (n, 100.0 * totzahl[n] / DURCHGAENGE) for n in sorted(totzahl)))
    print("Mittel: %.2f Tote von fuenf" % (
        sum(n * c for n, c in totzahl.items()) / float(DURCHGAENGE)))
    print()
    print("Endzustand je Figur in Prozent:")
    for k in G["FIGUREN_REIHENFOLGE"]:
        zeile = "   %-12s" % k
        for z, n in endzustand[k].most_common():
            zeile += "  %s %.0f%%" % (z, 100.0 * n / DURCHGAENGE)
        print(zeile)
    if naehe_tot and naehe_lebt:
        print("Verbundenheit gesamt am Ende:")
        print("   in Durchgaengen mit zwei oder mehr Toten:  %.1f" % (sum(naehe_tot) / float(len(naehe_tot))))
        print("   in Durchgaengen mit hoechstens einem Toten: %.1f" % (sum(naehe_lebt) / float(len(naehe_lebt))))
    print()

# Promptpakete "Zwischen Front und Heimat"

Stand: 3. September 2026, zweite Fassung — größere Pakete.
Grundlage ist `bericht.txt`, den `probe_alles.py` aus Paket 0 erzeugt hat.

Jede Datei `paketNN.txt` ist **vollständig und copy-paste-fertig**: Die
Verfassung steht bereits oben drin. Datei öffnen, alles markieren, in Claude
Code einfügen, abschicken.

**Zehn Dateien statt einundzwanzig.** Die neun inhaltlichen Pakete bestehen
aus zwei oder drei Schritten, die Claude Code am Stück abarbeitet — mit einer
Sicherungskopie und einem Schnelllauf zwischen den Schritten, damit man
hinterher sieht, welcher Schritt was bewirkt hat.

---

## Die Pakete

| Nr | Paket | Schritte | Datei |
|----|-------|----------|-------|
| 0 | Werkbank | erledigt, mit Nachtrag | `paket00.txt` |
| 1 | Notreparatur: `merkbuch.rpy` zurückholen | – | `paket01.txt` |
| 2 | Fundament: Pfade, Herkunft, Wertehaushalt | 3 | `paket02.txt` |
| 3 | Grundlagen des Erzählens: Quellen, Dramaturgie, Sprachmaß | 2 | `paket03.txt` |
| 4 | Inhalt 1917 und 1918 | 2 | `paket04.txt` |
| 5 | Etappe und Epilog 1919 | 2 | `paket05.txt` |
| 6 | Textüberarbeitung Front und Heimat | 2 | `paket06.txt` |
| 7 | Bewegung und Handgriffe | 3 | `paket07.txt` |
| 8 | Medien, Rückmeldung, Glossar | 3 | `paket08.txt` |
| 9 | Schulfassung: Export, Lehrkraftmaterial, Abnahme | 2 | `paket09.txt` |

`paket10.txt` bis `paket20.txt` sind nur noch Zeiger auf die neuen Nummern.

---

## Was in welchem Paket steckt

**Paket 2 — Fundament.** Etappe schließen und die stille Ersetzung hörbar
machen · Herkunft: zwei Jahrgänge statt vier, drei Familienmerkmale statt
`ernaehrer_im_feld` · Wertehaushalt: von 58–99,8 % harten Abbrüchen auf
40–60 %. In dieser Reihenfolge, weil die ersten beiden Schritte verändern,
was der dritte misst. Kein neuer Erzähltext.

**Paket 3 — Grundlagen des Erzählens.** Quellenformat festlegen und 42
Ereignisse nachrüsten · Jahresbogen, Ketten, der persönliche Faden durch die
fünf Nebenfiguren, dazu Probe 8 für die Lesbarkeit.

**Paket 4 — Inhalt 1917 und 1918.** Rund 24 neue Ereignisse, alle 14
Rückbezüge aus `NACHHALL_PLAN`. Das größte Paket. Anweisung im Text:
Ereignisse in Gruppen zu sechst, Meldung nach jeder Gruppe.

**Paket 5 — Etappe und Epilog 1919.** Die Etappe füllen, ihr eine eigene
Sprache geben (43 Fundstellen) und wieder öffnen · 1919 füllen, eine Einlage
dafür bauen, die Wirtshausszene schreiben.

**Paket 6 — Textüberarbeitung.** 18 Front-, 20 Heimat- und vier
Einstiegsereignisse. Kein Wert, keine Bedingung, keine Kennung wird
angefasst — alle Zahlen müssen exakt gleich bleiben, nur Probe 8 darf besser
werden.

**Paket 7 — Bewegung und Handgriffe.** `bewegung.rpy` mit neun Transforms,
abschaltbar · Rotstift und Acht Striche · Tornister und Fahrt aufs Land.

**Paket 8 — Medien, Rückmeldung, Glossar.** `MEDIEN.md`, fünf Kartentypen,
vierte Schrift, Beamerkontrast · Wertefeedback, Onboarding, Rhythmus,
Tongerüst · Glossar und Quellenkarten. Zusammen, weil alle drei dieselben
Bildschirme anfassen.

**Paket 9 — Schulfassung.** Protokoll-Export und `LEHRKRAFT.md` ·
Gesamtabnahme, Windows-Distribution, `RESTLISTE.md`.

---

## Warum nicht noch größer

Drei Grenzen sind echt, nicht bequem:

1. **Paket 2 muss vor den Inhalten liegen.** Der Wertehaushalt wird
   gemessen, verändert und wieder gemessen. Kämen die 40 neuen Ereignisse
   dazwischen, wüsste niemand mehr, was die Abbruchquote bewegt hat.
2. **Paket 6 muss nach Paket 4 und 5 liegen.** 38 Ereignisse zu polieren und
   danach 40 neue zu schreiben wäre doppelte Arbeit.
3. **Paket 4 ist schon am Anschlag.** 24 Ereignisse à 40 Zeilen sind rund
   1000 Zeilen deutsche Prosa in einem Durchgang. Mehr in einem Paket, und
   die letzten Ereignisse werden merklich flacher als die ersten — das
   sieht man dem Text an, und keine Probe schlägt deswegen an.

---

## Ablauf in jedem großen Paket

Die Verfassung schreibt Claude Code vor:

1. Schritte der Reihe nach, keiner beginnt vor der Abnahme des vorigen.
2. Vor jedem Schritt eine Kopie nach `sicherung/<Datum>_schritt<N>/`.
3. Nach jedem Schritt `python probe_alles.py --schnell` und eine
   Kurzmeldung in höchstens fünf Zeilen.
4. Scheitert eine Abnahme, hält Claude Code an und meldet es — statt
   weiterzumachen oder still etwas zu reparieren.
5. Am Ende der vollständige Lauf plus Vergleich mit `bericht_ausgang.txt`.

So bleibt der Vorteil der kleinen Pakete — man sieht, welcher Schritt was
bewirkt hat — ohne dass du zwanzigmal einfügen musst.

---

## Kurzcheck nach jedem Paket

```
python probe_alles.py --vergleich bericht_ausgang.txt
```

Oben steht dann je Probe: früher, heute, Differenz. Alles andere ist
Beiwerk.

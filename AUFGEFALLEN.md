# AUFGEFALLEN

Was bei der Arbeit an einem Paket außerhalb seines Auftrags bemerkt wurde.
Nichts davon ist geändert worden. Neueste Einträge oben.

---

## 3. September 2026 — Paket 4, Schritt 2

10. **Das Lazarettmerkmal heißt `lazarett`, nicht `lazarettdienst`.** Der
    Auftrag nennt unter den Pflichtereignissen
    `braucht_eines: lazarettdienst`. Im MERKMAL_REGISTER und im
    NACHHALL_PLAN heißt es `lazarett`. Gebaut ist es mit `lazarett`; mit
    dem Namen aus dem Auftrag wäre das Ereignis nie ziehbar gewesen.

11. **`lazarett` kann heute nur auf dem Heimatpfad vergeben werden.** Es
    kommt aus der Erwerbswahl, und die findet im Heimatzweig statt.
    `lazarett_1918_grippestation` trägt trotzdem beide Pfade, wie der
    Plan es verlangt — auf der Front greift es erst, wenn ein Paket den
    Lazarettdienst auch dort erreichbar macht. **Das ist keine Lücke,
    aber es sollte jemand wissen, bevor er sich über die Ziehzahlen
    wundert.**

12. **Sieben statt sechs neue Frontereignisse.** Mit sechs bleibt der
    lange Frontverlauf 1918 im ungünstigsten Fall unter Deckung: Vier der
    freien Frontereignisse sind wiederholbar und stehen in jedem Kapitel
    bereit, die vier übrigen (Beute, Urlaub, Steckrübe, Winterstellung)
    können 1915 bis 1917 verbraucht sein. Dann stehen sieben Ziehungen
    nur sechs Karten gegenüber. `front_1918_kokarde` ist die siebte.
    **Allgemeiner Befund für alle Inhaltspakete:** Die Bestandstafel
    zählt den Vorrat eines Jahres, die Sackgassenprobe zählt, was in
    einem einzelnen Durchgang noch übrig ist. Nur die zweite Zahl sagt,
    ob ein Kapitel wirklich trägt.

13. **`heimat_verfahren` hat seit dem Vorweg eine Fassung für 1919.** Sie
    ist der einzige Spieltext des Pakets, der nach dem 11. November 1918
    liegt. Das war Absicht und ist im Vorweg begründet: Ohne 1919 bleibt
    die Kette der Einlage `hamsterfahrt` unauflösbar. Für Paket 5 heißt
    das: Der Epilog hat bereits einen Text, der dort ankommt.

---

## 3. September 2026 — Paket 4, Vorweg und Schritt 1

### Falsche Angaben im Auftrag

1. **Der Ereignisbestand von Paket 2 heißt nicht `EREIGNISPAKET_ZWEI`.**
   Der Auftrag nennt diesen Namen unter BEZEICHNERKARTE. Im Quelltext heißt
   die Liste `EREIGNISSE_PAKET2` (herkunft.rpy, Abschnitt 6, Zeile 1220).
   Wer nach dem Namen aus dem Auftrag sucht, findet nichts und schließt
   daraus, die vier `einstieg_`-Ereignisse fehlten.

2. **Drei Kennungen stehen in beiden Plänen, nicht zwei.** Der Vorweg-Teil
   C nennt `front_1918_liste` und `heimat_1917_aprilstreik`. Dazu kommt
   `front_1917_verbruederung_nachhall`: Es steht im NACHHALL_PLAN
   (Merkmal `verbruederung`) und im KETTEN_PLAN (als zweites Glied von
   `front_1914_weihnachten`). Die zusammengeführte Liste in
   `inhaltsplan()` weist alle drei aus.

3. **Vier Träger hatten `kern=False`, nicht einer.** Der Auftrag nennt
   `heimat_1914_liebesgaben`. Dieselbe Lage hatten
   `heimat_lazarettzug` (Etappe 1915), `front_1916_zaehlung` und
   `front_urlaub` (beide Etappe 1916). Alle vier sind jetzt `kern=True`.

4. **Die Liste der auszuweitenden Ereignisse ist unvollständig.**
   `heimat_lazarettzug` endet bei 1916, trägt keine Jahreszahl im Namen
   und ist damit ein wiederkehrender Vorgang wie die übrigen genannten.
   Ohne seine Ausweitung erreicht die Heimat 1917 im langen Verlauf die
   geforderte Reserve nicht.

### Was außerhalb des Auftrags auffiel

5. **Nicht nur `heimat_hamsterfahrt` merkt `heimat_verfahren` vor, auch
   die EINLAGE `hamsterfahrt`** (minispiele.rpy, Abschnitt 5, Zeile 986).
   Sie läuft bis 1918 und merkt für dasselbe Jahr vor. Deshalb reichten
   die Jahre 1917 und 1918 aus dem Auftrag nicht aus; das Glied hat 1919
   dazubekommen. Erst damit ging die Zahl der offenen Vormerkungen auf
   null. **Für andere Ketten gilt dasselbe: Wer eine Kette plant, prüft
   auch die Einlagen, nicht nur die Ereignisse.**

6. **Der Satzzerleger von Probe 8 trennt nicht nach einer Zahl und nicht
   nach einem schließenden Anführungszeichen.** Ein Satz, der auf eine
   Jahreszahl endet ("… im April 1917."), und ein Satz, der auf `.“`
   endet, werden mit dem folgenden Satz zu einem verschmolzen. Die
   Messung meldet dann einen zu langen Satz, den es nicht gibt, und Probe
   5 meldet "einordnung hat 1 Saetze statt genau zwei". Die neuen Texte
   sind so umgestellt, dass sie das umgehen; die Probe selbst sollte das
   aber können. **Vorschlag für ein eigenes Paket:** `saetze_zerlegen()`
   in probe_alles.py um beide Fälle erweitern und danach den ganzen
   Bestand neu messen.

7. **Drei bestehende Textstellen halten das Sprachmaß nicht ein.** Sie
   stammen aus früheren Paketen und wurden nicht angefasst:
   - `front_nachfrage`, Ausgang der zweiten Option: zwei Nebensätze
     ("Das ist weniger, als du befürchtet hast, und mehr, als du
     verkraftest.")
   - `front_nachfrage`, `quelle.einordnung`: 22 Wörter im ersten Satz
   - `front_trommelfeuer`, `quelle.einordnung`: zwei Nebensätze
   - `heimat_verfahren`, Fassung 1915: zwei Nebensätze

8. **Acht Briefe werden nie gezogen** (Probe 2, "Nie gezogen"), darunter
   `h_amt_metall` und `f_amt_bestand` für 1917 und 1918. Sie waren tot,
   weil es in diesen Jahren keine Ereignisse gab. Ob sie jetzt greifen,
   zeigt der nächste Bericht.

9. **Probe 4 war auf ein Spiel geeicht, das nach 1916 endete.** Siehe die
   Meldung zu Schritt 1: Die Grenzen aus Paket 2, Schritt 3 wurden an
   einem Bestand gemessen, in dem 1917 bis 1919 leer waren und deshalb
   fast ohne Kosten durchliefen. Mit gefülltem Jahr 1917 steigt die Zahl
   der Ziehungen im langen Verlauf von 17 auf 23, im kurzen von 7 auf 9.
   Gemessen wurde: Selbst wenn ALLE dreizehn neuen Karten gar nichts
   kosten, erreicht der kurze Frontverlauf nur 30,8 statt der geforderten
   35 Prozent. Die Eichung gehört in einen eigenen Zahlendurchgang, nicht
   in ein Inhaltspaket.

## 3. September 2026 — Paket 5, Schritt 1 (Vorarbeit, Sitzung abgebrochen)

10. **Git war in dieser Sitzung nicht im PATH.** `git` als Kommando gibt es
    auf dem Rechner nicht; das Repository besteht trotzdem. Die einzige
    vorhandene git.exe liegt bei GitHub Desktop:
    `C:\Users\domin\AppData\Local\GitHubDesktop\app-3.5.4\resources\app\git\cmd\git.exe`
    (Version 2.47.3). Wer committen will, ruft sie mit vollem Pfad auf.

11. **Die Zeilennummern aus dem Paket 5 stimmen nicht mehr.** Die Liste in
    Schritt 1, Teil B nennt figuren.rpy:1843, 1723/1724/1725/1743, 1799,
    1905 und minispiele.rpy:542, 616/620/621, 847/858/872/880/889.
    Selbst gemessen (Etappe im Speicher geoeffnet, Textdurchsicht plus 600
    Durchgaenge) liegen sie bei figuren.rpy:1847, 1827/1828/1829, 1903,
    2057 und minispiele.rpy:582, 656/660/661, 887/898/912/920/929.
    Die Zahl der Stellen — 43 — stimmt.

12. **43 Aufrufstellen sind nicht 43 Textfassungen.** Hinter den 43 Stellen
    stehen **125 verschiedene Woerterbuecher** ohne Etappenfassung:
    60 in dialoge.rpy (die zwoelf Szenen, Text und Ort), 49 in figuren.rpy
    (Schicksalsstufen, NACHRICHT_KOPF, entfremdung_pruefen) und 16 in
    minispiele.rpy (Einlagen, portionen). Das ist der wahre Umfang von
    Teil B.

13. **Ein stiller Ersatz, den keine Probe sieht: `nach_welt()` in
    merkbuch.rpy:87.** Die Funktion baut Variantenwoerterbuecher und setzt
    bei `etappe=None` still die Frontfassung ein (Zeile 97). Weil der
    Schluessel "etappe" dann im Woerterbuch steht, meldet variante()
    nichts — der Griff in die Rueckfallebene wird nicht gezaehlt. Von elf
    Aufrufen tragen sieben ein echtes `etappe=`. Wenn Teil B.7 die
    Notloesung in variante() streicht, muss diese Stelle mit, sonst bleibt
    ein Ersatz uebrig, den keine Zahl zeigt.

14. **Vier Rueckfallzweige, drei Richtungen.** Im ganzen Projekt gibt es
    genau vier Stellen, die pfadweise zurueckfallen, und sie fallen nicht
    in dieselbe Richtung:
    - dialoge.rpy:298 `figur_name()` und :304 `figur_zusatz()` → heimat
    - figuren.rpy:400 `zustand_anzeige()` → heimat
    - dialoge.rpy:265 `variante()` → front (die Notloesung)
    - merkbuch.rpy:97 `nach_welt()` → front (still, siehe 13)
    Vorschlag fuer Schritt 1: figur_name(), figur_zusatz() und
    zustand_anzeige() auf `variante()` beziehungsweise `welttext()`
    umstellen. Dann gibt es nur noch eine Regel, und jede Luecke wird
    gezaehlt statt ersetzt.

15. **Der Etappenbestand ist duenner, als die Bestandstafel zeigt.** Frei
    ziehbar sind heute: 1914 ein Ereignis, 1915 drei, 1916 vier, 1917 drei,
    1918 drei, 1919 keines. Getragen wird der Pfad von nur fuenf Karten
    (front_feldpost, front_urlaub, front_1916_zaehlung, heimat_lazarettzug
    und der Kette front_nachfrage) — und vier davon sind von der Front
    oder aus der Heimat geliehen. Ein eigenes Etappenereignis gibt es im
    ganzen Projekt nicht.

## 4. September 2026 — Paket 5, Schritt 1, Teil A (18 Etappenereignisse)

16. **Der Satzzerleger von Probe 5 hat jetzt einen belegten Fall.** Paket 5,
    Schritt 3, Teil D.12 vermutet den Fehler; hier ist er. Die Einordnung
    von etappe_1914_ankunft endete zuerst auf „... aus dem Herbst 1914."
    und wurde als „einordnung hat 1 Saetze statt genau zwei" gemeldet. Der
    Punkt hinter der Jahreszahl gilt dem Zerleger nicht als Satzende, der
    zweite Satz verschmilzt also mit dem ersten. Behoben durch Umschreiben
    („aus dem ersten Kriegsherbst"), nicht durch einen Eingriff ins
    Werkzeug — das gehoert in Schritt 3. Wer bis dahin Belege schreibt,
    beendet keinen Satz einer Einordnung mit einer Zahl.

17. **Probe 4 hat eine Pruefung, die in keinem Paket steht.**
    „Einbahnstrassen: alle Optionen verschlechtern denselben Wert." Sie
    hat etappe_verwundetenzug sofort gefunden, weil beide Optionen
    belastung hoben (+2 und +1). Die Regel ist richtig und schaerfer als
    das, was in den Handwerksregeln steht; sie gehoert dort erwaehnt.
    Daneben laeuft eine zweite Pruefung auf dominierte Optionen.

18. **einstieg_etappe ist nicht entfernt, sondern gesperrt.** Paket 5,
    Schritt 1, Teil C.10 sagt, der Aufruf sei herausgenommen worden. Er
    steht noch da: herkunft.rpy:2244 ruft ihn, aber nur, wenn
    ETAPPE_FREIGESCHALTET wahr ist. Teil C.10 ist damit kein
    Wiederherstellen, sondern faellt mit dem Umlegen des Schalters von
    selbst. Der Wartekommentar davor ist zu pruefen.

19. **Das Merkmal lazarett ist auf der Etappe zur Haelfte schon da.**
    Paket 5, Schritt 1, Teil C.9 nimmt an, lazarett sei nur in der Heimat
    zu haben. In die Etappe fuehren aber zwei Wege, und einer davon setzt
    es zwingend: erwerb_holen(...).etappe_moeglich ist ausschliesslich beim
    Erwerb „lazarett" gesetzt (herkunft.rpy:975 bis 984), und dieser
    Erwerb vergibt das gleichnamige Merkmal. Wer ueber einstieg_etappe
    kommt, hat es also. Unerreichbar ist es nur fuer den zweiten Weg, die
    Musterung mit dem Grad g.v. Teil C.9 sollte das messen, bevor er ein
    Ereignis dafuer baut.

20. **Zahlen aus probe_alles.py --schnell sind nicht mit dem vollen Lauf
    vergleichbar.** Die Schnellprobe rechnet 300 statt 2000 Durchgaenge je
    Lage. Bei den Proben 2, 3 und 4 verschiebt das die Ergebnisse
    sichtbar: Die Sackgassenprobe meldete waehrend Teil A nacheinander 4,
    3 und 2 Beanstandungen, im vollen Lauf danach wieder 4 — dieselben
    vier Zeilen wie vorher, alle in 1919 und damit Sache von Schritt 2.
    Die Zwischenmeldungen in den Commits 48db5a0 und 703d2a3 nennen
    deshalb eine Verbesserung, die es nicht gibt. Die Bestandstafel und
    die Proben 5, 7 und 8 zaehlen dagegen fest und sind in beiden
    Betriebsarten gleich.

21. **Heimat 1914, langer Verlauf, steht weiter auf „knapp".** Der
    Nachtrag von 1914 an heimat_lazarettzug hebt die Zeile von 5 auf 6
    freie Ereignisse bei Soll 5. Fuer „in Ordnung" braucht sie 7. Es ist
    die einzige Zeile ohne Reserve im ganzen Bestand. Nicht geaendert:
    Heimatinhalte gehoeren nicht zu diesem Paket.

22. **KAPITEL_BOGEN hat fuer 1917 bis 1919 auf allen drei Pfaden leere
    Traegerlisten** (kapitel.rpy:284 bis 336). Der Kommentar darueber sagt,
    das liege daran, dass es dort noch keinen Bestand gebe. Seit Paket 4
    stimmt das fuer Front und Heimat nicht mehr, und seit diesem Schritt
    auch fuer die Etappe nicht. Die Jahre 1917 und 1918 laufen damit ohne
    tragenden Moment: BOGEN_ZUSCHLAG greift nirgends. Probe 1 meldet es
    nicht, weil sie nur pruefen kann, was in der Liste steht. Nicht
    geaendert, weil ausserhalb von Teil A.

## 4. September 2026 — Paket 5, Schritt 1, Teil B (die eigene Stimme)

23. **Das Schuldbuch von probe_alles.py hat nie geschrieben.** Der
    Abschnitt „Textluecken auf geschlossenen Pfaden" existiert im
    Werkzeug seit Paket 2, ist aber in keinem Bericht je erschienen.
    Ursache: `beobachtung_einhaengen()` haelt GENAU EIN Rueckfallbuch in
    seinem Abschluss fest, und beide Wrapper fragen dessen Schalter ab.
    `durchlauf()` legt fuer die geschlossenen Pfade ein ZWEITES Buch an
    und setzt dessen Schalter — die Wrapper sehen davon nichts, weil das
    Hauptbuch zu diesem Zeitpunkt noch aus ist. Der Bericht meldete zu
    den fehlenden Etappenfassungen also nicht null, sondern gar nichts.
    Behoben ueber einen Zeiger `AKTIVES_RUECKFALLBUCH`; danach standen
    dort 27 offene Stellen mit 4414 Griffen, und daraus wurde die
    Arbeitsliste fuer Teil B. **Lehre fuer spaeter: Ein Abschnitt, der
    nie erscheint, ist kein Beweis fuer null.**

24. **Die Werkbank von probe_alles.py baut Projektlogik nach, und das
    ist zweimal in einer Sitzung schiefgegangen.** `zweig_variante()`
    bildet die Vorrangfolge von `variante()` nach, und der Weltvergleich
    der Briefe war als eigener Ausdruck `vorlage.welt != briefwelt()`
    geschrieben. Beim Streichen der Notloesung musste die eine Stelle
    mit, sonst waeren Werkbank und Spiel auseinandergelaufen; beim
    Umstellen von `welt` auf eine Liste stuerzte die andere ab
    (`unhashable type: list`) und haette vorher jeden Brief als Fehler
    gemeldet. Der Weltvergleich fragt jetzt `welt_erlaubt()`, so wie
    `pfade_erreichbar()` die Pfadfunktionen des Projekts fragt. Wo die
    Werkbank noch nachbaut, steht das jetzt als Warnung im Kommentar.

25. **Die Zahlen zu nach_welt() stimmen nicht.** Vorarbeit und
    Auftragstext nennen elf Aufrufe, sieben davon mit echtem `etappe=`.
    Selbst gezaehlt sind es **neun Aufrufe, sechs mit echtem etappe=**,
    drei ohne. Die drei sind nachgeschrieben. Die Sache selbst stimmt:
    Es war der gefaehrlichste der Rueckfallzweige, weil er den
    Schluessel besetzte und die Probe deshalb schwieg.

26. **Der Umfang von Teil B ist groesser als 125.** Die Vorarbeit zaehlt
    125 Woerterbuecher ohne Etappenfassung. Selbst gezaehlt — jede
    geschweifte Klammer mit Pfadschluesseln auf der eigenen Ebene —
    waren es **204**. Der Unterschied liegt vor allem in merkbuch.rpy,
    das die Vorarbeit gar nicht mitzaehlt (34 Stueck), und in
    verschachtelten Woerterbuechern. Alle 204 sind abgearbeitet bis auf
    **3**, und die drei gehoeren zur Einlage `hamsterfahrt`, die nur in
    der Heimat vorkommt und deshalb zu Recht keine Etappenfassung hat.

27. **post_zielort() in merkbuch.rpy haette die Etappe falsch
    adressiert.** Die Funktion gab bisher nur fuer „front" die
    Deutsche Feldpost aus und fiel sonst auf den Ortsnamen zurueck. Mit
    der eigenen Briefwelt haette auf dem Umschlag „Etappengebiet"
    gestanden. Das Etappengebiet gehoerte zum Bereich der Feldpost;
    korrigiert und im Kommentar begruendet. **Dieselbe Art Fehler kann
    ueberall lauern, wo `briefwelt() == "front"` steht.** Gesucht und
    geprueft wurden alle Fundstellen; die uebrigen sind in Ordnung.

28. **Zwei Frontszenen tragen ort=„Etappe".** `prolog_ordnung` und
    `wendepunkt_1916_amt` (dialoge.rpy) zeigen einem Frontspieler
    „Etappe" als Ortsangabe. Das war richtig, solange die Etappe kein
    eigener Pfad war; jetzt liest es sich, als stuende die Figur auf dem
    anderen Pfad. Nicht geaendert: Es ist Fronttext und gehoert nicht zu
    diesem Paket.

29. **Teil B ist noch nicht bewiesen, nur vorbereitet.** *(Erledigt in
    Teil C: Bei geoeffnetem Pfad und 2000 Durchgaengen je Lage meldet
    Probe 2c 0 Griffe, Werkbank und Spiel stimmen ueberein.)* Probe 2c
    meldet
    heute 0 Griffe und beide Zaehlungen stimmen ueberein — aber das
    heisst nur, dass Front und Heimat sauber sind und das Schuldbuch
    leer ist. Die Abnahme verlangt 0 Griffe **ueber 2000
    Etappendurchgaenge in beiden Verlaeufen**, und Etappendurchgaenge
    gibt es nicht, solange `pfade_erreichbar()` den Pfad nicht kennt.
    Diese Zahl kann erst Teil C liefern. Wer den Schalter umlegt, sieht
    als Erstes hier nach.

## 4. September 2026 — Paket 5, Schritt 1, Teil C und der Durchgang durch die offenen Punkte

### Was erledigt ist

Die Punkte 13, 14, 15 (Rueckfallzweige, `nach_welt()`, Etappenbestand)
sind mit Teil A und B abgearbeitet. 18, 19 und 29 sind mit Teil C
erledigt. 16, 22, 23, 24, 26, 27 und 28 sind in dieser Sitzung behoben
und je einzeln committet. 11, 12, 20 und 25 waren Messfehler in den
Angaben und sind durch eigene Zaehlung richtiggestellt. 10 ist die
Umgebung und laesst sich nicht beheben.

### Was offen bleibt, und warum

30. **ZIELKONFLIKT ZWEIER REGELN: die Einordnungen der Einlagen.** Das
    ist der einzige Rest von Probe 8, und er laesst sich nicht durch
    Umschreiben loesen - er ist eine Entscheidung, die dem Projektleiter
    gehoert.
    Zwei Regeln stehen gegeneinander. Probe 5 und Probe 7 verlangen
    GENAU ZWEI SAETZE je Einordnung. Probe 8 verlangt KEINEN SATZ UEBER
    20 WOERTER. Zusammen erlauben sie einer Einordnung hoechstens rund
    vierzig Woerter. Die zwoelf beanstandeten laufen zwischen 55 und 64.
    Die Einordnung ist kein Lehrerhinweis wie KAPITEL_LEHRPLAN, sondern
    steht nach jeder Einlage auf dem Bildschirm, im Analysemodus wie
    ohne ihn. Die Lesbarkeitsregel gilt also zu Recht.
    Was Kuerzen kostet, an einem Beispiel: Die Einordnung von portionen
    (heimat) nennt heute Berlin als erste Stadt mit Brotkarten, das
    Datum, die Menge je Kopf, die Ausweitung auf das Reich und die
    Zuteilung von Februar 1917 mit rund tausend Kilokalorien. Auf zwei
    Saetze von je zwanzig Woertern zusammengezogen bleiben davon die
    Rationierung und die Kilokalorien; Berlin, das Datum und die
    Kuerzungen fallen weg. Das ist genau der Stoff, den eine achte
    Klasse braucht.
    VORSCHLAG: Die Formatregel auf ZWEI BIS VIER SAETZE aendern, jeder
    hoechstens zwanzig Woerter. Damit bleibt die Einordnung kurz - sie
    war nie laenger als achtzig Woerter -, und jeder einzelne Satz wird
    lesbar. Zu aendern waeren `einordnungen_pruefen()` in minispiele.rpy
    und `quelle_pruefen()` in probe_alles.py, dazu die Formatbeschreibung
    ueber der Klasse `Ereignis` in script.rpy. Eine Sitzung, wenn der
    Projektleiter es so will.

31. **AUF DER ETAPPE IST KLUGE WAHL SCHLECHTER ALS ZUFALL.** Gemessen
    bei geoeffnetem Pfad, 2000 Durchgaenge je Lage: kurzer Verlauf 6,3
    Prozent bei zufaelliger und 6,0 bei kluger Wahl, Abstand MINUS 0,2.
    Auf den anderen beiden Pfaden liegt der Abstand bei plus 19 und plus
    30. Der lange Etappenverlauf erreicht das Jahr 1918 in genau EINEM
    Durchgang von zweitausend.
    Das ist kein Zufall der Messung, sondern liegt im Aufbau: Die Etappe
    startet mit einem Rueckhalt von 6 gegen 7 an der Front und 8 in der
    Heimat, und mit einer Aufmerksamkeit von 2 gegen 1 auf beiden
    anderen Pfaden (`PFAD_BASIS` in script.rpy). Sie beginnt also naeher
    an der Verhaftungsschwelle und weiter weg von jedem Rueckhalt. Dazu
    kommt, dass die Entscheidungen dieses Pfades ihrer Sache nach
    zwischen Aufmerksamkeit und Rueckhalt handeln - Listen, Meldungen,
    Spalten -, waehrend die Strategie "klug" jeweils nur den derzeit
    schlechtesten Wert schont und sich damit in die Ecke spielt.
    NICHT HIER BEHOBEN, und zwar ausdruecklich: Paket 5, Schritt 3 ist
    der Zahlendurchgang, und er ist genau dafuer da. Diese Zeilen sind
    seine Ausgangsmessung. Wer dort eicht, faengt bei PFAD_BASIS an,
    nicht bei den Ereignissen.

32. **Heimat 1914 bleibt im langen Verlauf "knapp"** (6 freie Ereignisse
    bei Soll 5, fuer "in Ordnung" waeren 7 noetig). Der Nachtrag von
    1914 an heimat_lazarettzug hat die Zeile von 5 auf 6 gehoben, mehr
    war ohne neuen Inhalt nicht zu holen.
    BEWUSST NICHT BEHOBEN. Von den heutigen Heimatereignissen gehoert
    keines sachlich zusaetzlich ins Jahr 1914: Hamsterfahrt und
    Brotkarte setzen die Rationierung voraus, die Ruestungsschicht die
    Frauenarbeit von 1915/16, die Denunziation den Mangel. Es fehlt also
    ein neues Ereignis, und Heimatinhalte gehoeren nicht in ein Paket
    ueber die Etappe. "Knapp" ist ausserdem keine Beanstandung, sondern
    ein Hinweis. Ein einziges neues Heimatereignis fuer 1914 schliesst
    die Zeile.

33. **Zwei Pruefungen von Probe 4 stehen in keinem Paket.** "Einbahn-
    strassen: alle Optionen verschlechtern denselben Wert" und
    "Dominierte Optionen: eine Wahl, die keine ist". Beide sind
    schaerfer als alles, was in den Handwerksregeln steht, und beide
    haben in dieser Sitzung sofort zugeschlagen. Sie gehoeren in die
    Handwerksregeln der Pakete, damit man sie beim Schreiben kennt und
    nicht erst beim Messen.

## 4. September 2026 — Paket 5, Schritt 2 (Epilog 1919 und Wirtshausszene)

34. **DIE KURZFASSUNG MELDETE "IN ORDNUNG" FÜR PROBEN, DIE NICHTS
    GEMESSEN HATTEN.** Der gefaehrlichste Fehler, den ein Pruefwerkzeug
    haben kann, und in dieser Sitzung der zweite seiner Art nach dem
    Schuldbuch (Punkt 23).
    Als eine neue Einlage die Werkbank zum Absturz brachte, meldete
    `probe_laufen()` fuer Probe 2 zwar eine Beanstandung. Die Proben 3
    und 4 liefen aber anschliessend mit einem LEEREN Ergebnissatz
    weiter, fanden darin nichts und erschienen in der Kurzfassung als
    "in Ordnung". Sackgassenprobe und Wertetafel standen auf gruen, ohne
    dass ein einziger Durchgang gespielt worden war - und ich habe die
    Zahl beim ersten Lesen geglaubt.
    Behoben: Eine Probe mit `geprueft == 0` traegt jetzt "NICHTS
    GEMESSEN" in der Kurzfassung, und der Lauf gilt als fehlerhaft. Im
    Normalfall aendert sich nichts; nachgeprueft.

35. **EINLAGE_PROBEWERTE ist eine zweite Liste, die man leicht
    vergisst.** Wer eine Einlage hinzufuegt, traegt sie in
    `EINLAGE_VORBEREITEN`, in `EINLAGE_AUSWERTEN`, in `EINLAGEN` - und
    muss zusaetzlich simulierte Eingaben in `EINLAGE_PROBEWERTE`
    hinterlegen. Fehlen sie, bekommt die Auswertung `None`, und die
    halbe Werkbank bricht ab. Das steht in keinem Kommentar an der
    Klasse `Einlage` und in keinem Paket.

36. **Die Herkunftsnachklaenge erreichen den Lebenslauf praktisch nie.**
    Der Lebenslauf zeigte die zwei hoechstrangigen Merkmale mit
    Nachklang; seit Teil D sind es drei. Die Herkunft liegt bei Rang 32
    bis 34, Erwerbslage und Stellung bei 46 bis 60, und jede Figur
    traegt mindestens eines davon. Adel, Buergertum, Arbeiterschaft und
    Landbevoelkerung haben damit einen geschriebenen Nachklang, den fast
    niemand zu sehen bekommt.
    Das ist ein ALTER Befund, kein neuer - er entstand mit dem Register
    selbst. Die Erhoehung auf drei Plaetze mildert ihn, behebt ihn aber
    nicht. Wer ihn beheben will, hat zwei Wege: den Herkunftsnachklang
    aus der Rangliste herausnehmen und ihm einen festen Platz im
    Lebenslauf geben, oder die Raenge der Herkunft anheben. Beides ist
    eine Entscheidung ueber den Schluss und gehoert dem Projektleiter.
37. **POST_CHANCE fuer 1919 bleibt der offene Hebel.** Teil C2 ist
    beantwortet: Nicht die Wahrscheinlichkeit bremste die beiden
    Amtsbriefe, sondern POST_ABSTAND bei nur einer bis zwei Ziehungen im
    Epilog. Der Abstand gilt ab 1919 nicht mehr, und die Zustellungen
    stiegen von 32 auf 56 beziehungsweise von 54 auf 77 je 24000
    Durchgaenge.
    Die Obergrenze liegt jetzt bei POST_CHANCE fuer 1919, heute 30 -
    also rund 30 Prozent im kurzen und 51 im langen Verlauf. Der
    Entlassungsschein erreicht damit etwa jeden zehnten Durchgang, der
    1919 auf Front oder Etappe ankommt. NICHT hier gehoben, obwohl es
    eine Zeile waere: POST_CHANCE ist ausdruecklich der Hebel von
    Schritt 3, und wer ihn jetzt dreht, verschiebt das Ziel, auf das
    Schritt 3 eicht.


## 4. September 2026 — Paket 5, Schritt 3 (Wertehaushalt am vollen Bestand)

38. **DIE GRENZEN AUS ENTSCHEIDUNG 1 SIND MIT DEN STELLSCHRAUBEN DIESES
    SCHRITTES NICHT ERREICHBAR.** Das ist kein Aufgeben, sondern eine
    Messung, und sie ist der wichtigste Befund dieses Schrittes.
    Gemessen wurde die OBERGRENZE dessen, was die neun erlaubten Groessen
    ueberhaupt hergeben: PFAD_BASIS auf den bestmoeglichen Werten
    (Versorgung 12, Belastung 0, Verdacht 0, Rueckhalt 12), KAPITEL_WIRKUNG
    und KAPITEL_WIRKUNG_PFAD LEER, EINLAGE_CHANCE 0, POST_CHANCE 0 in
    allen Jahren. Also ein Spiel ohne Kalender, ohne Handgriffe und ohne
    Post. Ergebnis (600 Durchgaenge je Lage, zufaellig / klug):
      Front kurz  74,0 / 88,8      Front lang  17,7 / 68,5
      Etappe kurz 68,8 / 97,7      Etappe lang  2,0 /  8,7
      Heimat kurz 89,3 /100,0      Heimat lang 33,2 / 93,7
    Der lange Verlauf erreicht die Grenze also selbst dann nicht, wenn
    ausser den Ereignissen nichts mehr kostet.
    DIE URSACHE, in einer Zahl: Eine gezogene Karte verschiebt unter
    kluger Wahl (die die Versorgung schont) im Mittel
      Front   versorgung +0,48  belastung +0,30  aufmerksamkeit +0,27
      Etappe  versorgung +0,29  belastung +0,48  aufmerksamkeit +0,38
      Heimat  versorgung +0,96  belastung +0,57  aufmerksamkeit +0,36
    Die Skala geht von 0 bis 12, die Abbrueche liegen bei 1, 12 und 12.
    Bei 31 Ziehungen im langen Verlauf sind das rund 9 bis 15 Punkte
    Belastung und 8 bis 12 Punkte Verdacht — mehr, als die Skala hergibt.
    DREI WEGE, und alle drei gehoeren Dominik:
      a) DIE KARTEN VERBILLIGEN. Die mittlere Karte muesste etwa halb so
         viel kosten. Das ist Arbeit an den Optionen und gehoert in
         Paket 6, das die Karten ohnehin anfasst.
      b) DEN LANGEN VERLAUF KUERZEN. Gemessen: Mit 13 Kriegsjahr-
         Ziehungen statt 29 erreicht der lange Verlauf 15 bis 25 Prozent
         bei zufaelliger Wahl — immer noch unter 40. Der kurze Verlauf
         erreicht bei 8 Ziehungen 42 bis 51 Prozent und damit die Grenze.
         Der Preis: Aus der Doppelstunde wird eine Einzelstunde.
      c) DIE GRENZE FUER DEN LANGEN VERLAUF ANDERS SETZEN. Entscheidung 1
         gilt heute fuer beide Verlaeufe gleich. Ein langer Durchgang ist
         aber ein anderes Versprechen als ein kurzer.
    NICHT GETAN und ausdruecklich nicht: die Abbruchschwellen so weit
    heben, dass der Abbruch verschwindet (Punkt 11 des Auftrags), oder
    die Wahlstrategie "klug" so umbauen, dass sie besser abschneidet.

39. **DIE WERKBANK SPIELTE DIE WIRTSHAUSSZENE NICHT.** Der dritte Fall
    dieser Art nach dem Schuldbuch (Punkt 23) und der abgestuerzten Probe
    (Punkt 34), und der Befund ist derselbe: eine Null, die nur bedeutet,
    dass niemand hingesehen hat.
    Werkbank.durchgang() endete an der Marke ende_ueberlebt. Dass diese
    Marke seit Paket 5, Schritt 2 nach ende_ueberlebt_mit_wirtshaus
    umgeleitet ist, stand in der Nachbildung nicht. Damit hat die
    Werkbank die Wahl am Wirtshaustisch in keinem einzigen der bisher
    gemessenen Durchgaenge gespielt, und die drei Merkmale
    wirtshaus_widersprochen / _geschwiegen / _zugestimmt wurden nie
    gesetzt. Das Fach "Wie es ausging" stand deshalb auf 0,0 Prozent.
    Behoben; danach 100,0 Prozent unter den Durchgaengen, die 1919
    erreichen. **Lehre: Wer eine Umleitung anlegt, traegt sie in die
    Nachbildung der Marken ein.**

40. **NEUN LEERE TRAEGERFELDER WAREN DREI.** Der Auftrag nennt unter
    Punkt 13a "drei Jahre mal drei Pfade", also 1917 bis 1919 auf allen
    Pfaden. Selbst gezaehlt sind es DREI Felder, alle im Jahr 1919:
    1917 und 1918 sind in Schritt 1 dieses Pakets nachgetragen worden
    (Commit 9bffb4a, AUFGEFALLEN 22). Die Angabe im Auftrag war zum
    Zeitpunkt ihres Schreibens richtig und beim Ausfuehren ueberholt.

41. **PROBE 8 HAT DIE EINORDNUNGEN DER EREIGNISSE NIE GEMESSEN.**
    textbestand_sammeln() sammelt Ereignistexte, Optionstexte, Szenen,
    Kapitel, Briefe, Schicksale, Einlagen und Merkbuch — aber nicht die
    quelle-Woerterbuecher. Die Einordnung eines Ereignisses steht im
    Analysemodus auf dem Bildschirm, und Probe 5 prueft ihre Satzzahl;
    ihre Satzlaenge hat bis heute niemand gemessen. Die neue Tafel nach
    Gattung nimmt sie auf: 204 Saetze mehr, davon 4 ueber 20 Woerter.
    Probe 8 steigt dadurch von 1 auf 5 Beanstandungen. Die vier stehen
    in etappe_1916_verschleppt und drei weiteren; sie gehoeren zum
    Kuerzen in Paket 6 (Entscheidung 9).

42. **DIE ETAPPE HAT KAUM EINEN WEG GEGEN DIE ERSCHOEPFUNG.** Gezaehlt
    ueber alle Optionen aller ziehbaren Karten je Pfad:
      Wege, die versorgung heben:      Front 24 %  Etappe 21 %  Heimat 37 %
      Wege, die belastung senken:      Front 24 %  Etappe 13 %  Heimat 21 %
      Wege, die aufmerksamkeit senken: Front 17 %  Etappe 27 %  Heimat 18 %
      Wege, die rueckhalt heben:       Front 40 %  Etappe 42 %  Heimat 37 %
    Die Etappe hat die BESTEN Wege gegen den Verdacht und die
    schlechtesten gegen die Erschoepfung. Der Jahreswechsel legte
    ausgerechnet auf den Verdacht (KAPITEL_WIRKUNG_PFAD 1917); das ist in
    diesem Schritt auf belastung umgestellt. Der Rest ist Inhalt: Der
    Etappe fehlen Karten, auf denen man sich erholen kann.

43. **DIE EINBAHNSTRASSENPRUEFUNG UND DIE DOMINANZPRUEFUNG ZAEHLEN
    VERSCHIEDENE BESTAENDE.** In probe_wertetafel() ueberspringt die
    Einbahnstrassenpruefung Ereignisse mit nur_kette, die Dominanzpruefung
    nicht. Beide Regeln gelten aber fuer jede Karte, die eine Spielerin
    zu sehen bekommt, und ein Kettenglied bekommt sie zu sehen. Nicht
    geaendert: ausserhalb dieses Schrittes, und heute meldet keine der
    beiden etwas.

44. **DER KOMMENTAR UEBER EINLAGEN_JE_KAPITEL nannte 9 und 22
    Ziehungen.** Richtig sind 13 und 31. Die Zahlen stammten aus der Zeit
    vor Paket 3 und standen seither falsch da. In diesem Schritt
    mitgezogen, weil er dieselbe Rechnung anfasst.


## 4. September 2026 — Paket 6, Vorweg (Nachtrag zur Eichung)

45. **`front_nachfrage` IST EINE EINBAHNSTRASSE — und war es immer.**
    Neu sichtbar durch Vorweg E: Die Einbahnstrassenpruefung uebersprang
    bis heute alle Ereignisse mit `nur_kette`, und `front_nachfrage` ist
    eines. Beide Optionen heben die Belastung, um 1 und um 2.
    OB DAS EIN FEHLER IST, HAENGT AN EINER AUSLEGUNG. Handwerksregel g
    der Verfassung lautet: "Keine Karte, bei der beide Optionen denselben
    Wert verschlechtern, OHNE DASS EINE DAVON DAS AN ANDERER STELLE
    AUSGLEICHT." Die zweite Option gleicht aus - sie senkt den Verdacht
    um 1 -, bezahlt das aber mit versorgung -2. Die Probe kennt diese
    Ausnahmeklausel nicht; sie meldet jede Karte, bei der alle Optionen
    denselben Wert senken. Regel g ist in Paket 5, Schritt 3 AUS der
    Probe abgeleitet worden (AUFGEFALLEN 33), und dabei ist der Zusatz
    dazugekommen, den die Probe nie hatte.
    Inhaltlich traegt die Karte: Ein Ermittlungsverfahren des
    Gerichtsherrn kostet Kraft, wie man sich auch entscheidet.
    NICHT GEAENDERT. Zwei Wege, und beide gehoeren Dominik: entweder die
    Probe um die Ausnahmeklausel erweitern, oder Regel g auf den
    strengeren Wortlaut der Probe zuruecknehmen und die Karte anpassen.
    Bis dahin traegt Probe 4 diese eine Beanstandung dauerhaft.

46. **DER LANGE VERLAUF ERREICHT SEINEN KORRIDOR AUCH BEI ACHTZEHN
    ZIEHUNGEN NICHT.** Entscheidung 11 verlangt 20 bis 35 Prozent bei
    zufaelliger und mindestens 60 bei kluger Wahl; Entscheidung 12 gibt
    achtzehn bis zwanzig Ziehungen vor. Beide zusammen gehen nicht auf.
    Gemessen, 600 Durchgaenge je Lage, zufaellige Wahl:
      Ziehungen lang   19      16      14
      Front           10,8    18,8    27,8
      Etappe           1,5     6,0    13,0
      Heimat           9,5    15,7    20,3
    Der lange Verlauf braeuchte zwoelf bis vierzehn Ziehungen, um bei
    Front und Heimat in die Spanne zu kommen - und faellt damit aus dem
    Fenster, das Entscheidung 12 vorgibt. Genommen ist die UNTERE Kante
    des Fensters (achtzehn), weil sie dem Korridor am naechsten kommt.
    Die Etappe erreicht ihn auch dort nicht; sie liegt bei 5,5.
    Gemeldet und nicht eigenmaechtig entschieden, wie Entscheidung 11 es
    verlangt: "Wer dort landet, haelt an und meldet."

47. **`etappe_1916_verschleppt` GEHOERT ZU KEINEM SCHRITT VON PAKET 6.**
    Vorweg D nennt vier Ereignisse mit einer zu langen Einordnung:
    einstieg_meldung und einstieg_offizier (herkunft.rpy), front_nachfrage
    (script.rpy) und etappe_1916_verschleppt (kapitel.rpy). Schritt 1
    nimmt die front_-Ereignisse, Schritt 2 die heimat_- und
    einstieg_-Ereignisse. Die Etappe kommt in beiden nicht vor. Wer die
    vierte Einordnung kuerzt, muss sie also ausdruecklich mitnehmen.

48. **ZWOELF ZU LANGE SAETZE STEHEN IN FUENF FASSUNGEN, NICHT IN SECHS.**
    Schritt 2 spricht von "den sechs Einordnungen". Selbst gezaehlt sind
    es vier Einlagen mit zusammen fuenf zu langen Fassungen: rotstift
    (eine Fassung, 2 Saetze), portionen (ZWEI Fassungen, front und
    heimat, je 2 Saetze), hamsterfahrt (2 Saetze), tornister (2 Saetze).
    Macht zwoelf Saetze. versorgungsantrag ist nicht darunter - die
    Einlage aus Paket 5 haelt das Mass bereits ein.

## 4. September 2026 — Paket 6, Schritt 1 (Textueberarbeitung Front)

49. **EIN OPTIONSTITEL IST EIN BEZEICHNER, UND DAS STEHT NIRGENDS.**
    Der gefaehrlichste Befund seit dem Schuldbuch, und er waere fast
    durchgerutscht.
    DOMINANZ_NACHTRAG (kapitel.rpy) und die beiden Kettennachtraege
    KETTEN_NACHTRAG_PAKET4 und KETTEN_NACHTRAG_1918 finden ihre Option
    ueber den TITEL. Ein Titel sieht aus wie Spieltext - und in einem
    Textpaket schreibt man Titel um. Genau das ist hier passiert:
      "Mitspielen" -> "Ihnen recht geben": front_urlaub fiel auf die
      Werte zurueck, die Paket 4 als dominierte Option erkannt und
      ersetzt hatte.
      "Hinuebergehen" -> "Ueber die Bruestwehr steigen": die
      Verbruederungskette front_1914_weihnachten ->
      front_1917_verbruederung_nachhall war abgeschaltet.
    Keine Kennung hatte sich geaendert, keine Zahl im Quelltext, und der
    Diff zeigte nur Text. Gemerkt hat es allein Probe 4: Der kurze
    Etappenverlauf sprang von 53,8 auf 61,0 Prozent, und die
    Dominanzpruefung meldete front_urlaub.
    BEHOBEN UND ABGESICHERT: Beide Schluessel sind nachgezogen, beide
    Nachtragsfunktionen sammeln jetzt in NACHTRAG_OHNE_TREFFER jeden
    Schluessel ohne Treffer, und Probe 1 beanstandet ihn. Ueber beiden
    Tabellen steht die Warnung.
    LEHRE, die ueber diesen Fall hinausgeht: Regel 9 sagt, man benennt
    keinen Bezeichner um. Sie sagt nicht, WORAN man einen Bezeichner
    erkennt. Ein Schluessel in einem Woerterbuch ist einer, auch wenn er
    ein deutscher Satz ist. **Wer Text aendert, sucht vorher im ganzen
    Projekt nach dem alten Wortlaut.**

50. **32 front_-EREIGNISSE, NICHT 18.** Der Auftrag nennt 18. Selbst
    gezaehlt sind es 32, davon 19 aus der Zeit vor Paket 4 und 13 aus den
    Paketen 4 und 5. Die Zahl 18 passt fast genau auf die 19 alten - der
    Auftrag meinte offenbar die, die zu ueberarbeiten sind, und nicht den
    Bestand. Ueberarbeitet sind alle 19; die 13 neueren sind
    gegengelesen, dabei fielen zwei Optionstitel ausserhalb der Regel
    2 bis 4 Woerter auf und sind berichtigt.

51. **DIE PAKET-4-KARTEN SIND DOPPELT SO REICH WIE DIE ALTEN GEWESEN.**
    Vor diesem Schritt: die Karten aus den Paketen 1 und 2 trugen 68 bis
    89 Woerter, die aus Paket 4 und 5 zwischen 128 und 189. Das war kein
    Zufall, sondern der Unterschied zwischen "Der Vormarsch. Vierzig
    Kilometer am Tag" und einem Koerper, der um fuenf Uhr frueh losgeht.
    Nach der Ueberarbeitung liegen die alten bei 109 bis 133.

## 4. September 2026 — Paket 6, Schritt 2 (Heimat und Einstieg)

52. **DER EREIGNISTEXT ERREICHTE `variante()` NIE.** `ereignis_text_von()`
    lief ausschliesslich durch `jahrestext()`. Ein Woerterbuch mit
    Merkmalen als Schluessel waere still zum Zweig "standard" geworden -
    die drei Familienmerkmale aus Paket 2 liessen sich in KEINER Karte
    einsetzen, obwohl die Verfassung `variante()` genau dafuer vorsieht
    und der Auftrag es fuer vier Karten ausdruecklich verlangt.
    Behoben mit `ereignistext()` (script.rpy): Es entscheidet nach den
    Schluesseln der aeusseren Ebene, ob `jahrestext()` oder `variante()`
    dran ist, und wiederholt sich, bis kein Woerterbuch mehr uebrig ist.
    NICHT `szenentext()` benutzt, obwohl es fast passt: Der ruft
    `variante()` ZUERST. Eine reine Jahrestafel wie die von
    front_trommelfeuer faende dort weder Merkmal noch Pfad noch
    "standard" - der Text waere leer, und Probe 2c zaehlte einen Griff in
    die Rueckfallebene. Die Reihenfolge muss sich nach den Schluesseln
    richten, nicht umgekehrt.

53. **JAHRESAUSWEITUNG UND MERKMALSFASSUNG KOLLIDIEREN.**
    `jahresfassung_mischen()` legt die neuen Jahre NEBEN die vorhandenen
    Schluessel. Standen die Merkmale auf derselben Ebene wie die Jahre,
    sah `ereignistext()` Jahreszahlen und lief in `jahrestext()` - und
    fand fuer 1914 bis 1916 keinen passenden Schluessel. heimat_todes-
    nachricht zeigte deshalb in ALLEN Faellen den Text von 1917.
    Behoben, indem die vier Merkmalsfassungen unter das Grundjahr
    geschachtelt sind. **Regel fuer spaeter: Wer eine Merkmalsfassung an
    eine Karte haengt, die schon eine Jahresausweitung hat, schachtelt sie
    unter das Grundjahr - sonst gewinnen die Jahre.**

54. **37 KARTEN MIT heimat_ ODER einstieg_, NICHT 24.** Der Auftrag nennt
    20 heimat_; es sind 33. Die Differenz sind die Karten aus Paket 4 fuer
    1917 und 1918. Wie schon bei den 32 statt 18 Frontkarten meint der
    Auftrag offenbar die zu ueberarbeitenden und nicht den Bestand.

55. **EIN ZAEHLSKRIPT IM NOTIZORDNER IST KEINE PROBE.** Das Skript, mit
    dem ich Sinneswahrnehmungen gezaehlt habe, arbeitet mit einer
    Stichwortliste. Es hat drei Karten als "ohne Sinneswahrnehmung"
    gemeldet, die eine haben: die Kirchenglocke, die ein letztes Mal
    anschlaegt; das Kind, das am Aermel zieht; das raue graue Papier.
    Keines dieser Woerter stand in der Liste. Der Befund war jedes Mal
    falsch, und ich haette danach fast Texte geaendert, die in Ordnung
    sind. probe_alles.py kennt diese Pruefung nicht und soll sie auch
    nicht kennen - sie liesse sich nicht ohne Willkuer fassen. Wer sie
    trotzdem benutzt, liest die Fundstelle nach, bevor er schreibt.

## 5. September 2026 — Paket 7, Schritt 1 (Bewegung)

56. **AUFTRAG UND ANIMATIONSREGELN WIDERSPRECHEN SICH BEI `wert_schwebt`.**
    Der Auftrag nennt `wert_schwebt(dauer=1.1)`. Die Animationsregeln der
    Verfassung lassen hoechstens 0,45 Sekunden je Bewegung zu, und
    Entscheidung 3 macht sie bindend. CLAUDE.md sagt fuer diesen Fall:
    einen Auftrag, der gegen eine harte Regel verstoesst, fuehre ich
    nicht aus, sondern melde ihn mit Gegenvorschlag. Gebaut ist deshalb
    0,45. **Gegenvorschlag:** Entweder es bleibt bei 0,45 - ein
    aufsteigendes Plus- oder Minuszeichen ist auch in einer knappen
    halben Sekunde lesbar -, oder die Verfassung bekommt eine dritte
    Grenze fuer Anzeigen, die keine Eingabe aufhalten. Die Zahl steht als
    Vorgabewert in einer einzigen Zeile in `bewegung.rpy`.
    **Entscheidung: Dominik.**

57. **`post_eintreffen` WAR SEIT PAKET 4.1 UEBER DER GRENZE.** 0,55
    Sekunden gegen die erlaubten 0,45. Der Kommentar darueber behauptete
    sogar, keine der beiden Bewegungen dauere laenger als eine halbe
    Sekunde. Niemand hat das je gemessen, weil es keine Probe gab, die
    Dauern kennt. Jetzt auf 0,45 gesetzt und in Probe 9g gemessen.

58. **DER BEFUND DES AUFTRAGS NENNT VIER BEWEGUNGEN, ES SIND SECHS.**
    Genannt sind `notify_erscheinen`, `figur_spricht`, `figur_still` und
    `blase_blinken`. Dazu kommen `post_eintreffen` und
    `merkbuch_aufschlagen` in `merkbuch.rpy` - beide aus Paket 4.1, beide
    mit fester Sekundenzahl. Wieder ein Fall fuer Regel 9: Zahlen im
    Auftrag sind ein Hinweis, kein Beweis. Alle sechs sind erfasst; die
    drei mit Dauer laufen jetzt ueber `bewegungszeit()`, die drei ohne
    Dauer stehen in Probe 9h, damit sie niemand fuer eine Luecke haelt.

59. **`blase_blinken` HEISST WEITER SO UND BLINKT NICHT MEHR.** Teil E.7
    des Auftrags erlaubt ausdruecklich, das pulsierende Weiter-Zeichen
    durch ein ruhendes zu ersetzen; das ist geschehen. Regel 9 verbietet
    aber, einen Bezeichner umzubenennen, den kein Auftrag nennt - und der
    Auftrag nennt das Zeichen, nicht den Namen. Der Name ist damit eine
    Falle fuer die naechste Sitzung. **Entscheidung: Dominik** - entweder
    umbenennen (etwa `weiter_zeichen`) oder es bei dem erklaerenden
    Kommentar belassen, der jetzt darueber steht.

60. **`kapitelkarte` WIRD VON KEINEM ABLAUF MEHR AUFGERUFEN.** Im ganzen
    Projekt steht kein `call screen kapitelkarte`; `jahreskarte` aus
    `kapitel.rpy` hat sie ersetzt und zeigt zusaetzlich Zeitraum,
    Stichworte und die Jahreswirkung. Teil D des Auftrags nennt sie
    trotzdem, also hat sie ihre Bewegung bekommen - sichtbar wird sie
    dadurch nicht. Geloescht habe ich sie nicht (Regel 9).
    **Entscheidung: Dominik.**

61. **DIE WERKZEUGPFADE IN CLAUDE.md STIMMEN NICHT.** Dort steht
    `python werkzeuge/pruefen.py` und `python werkzeuge/schicksalsprobe.py`.
    Vom Projektstamm aus gibt es keinen Ordner `werkzeuge/`; beide Dateien
    liegen in `game/werkzeuge/`. Richtig ist also
    `python game/werkzeuge/pruefen.py`. Das betrifft die Abnahme der
    Schritte 2 und 3 dieses Pakets, die beide "pruefen.py" verlangen.

62. **REN'PY HAT EINEN TESTBEFEHL, UND ER LAEUFT HIER.**
    `renpy.py "<Projekt>" test <name>` fuehrt einen `testcase`-Block aus,
    der in einer `.rpy`-Datei im Spielordner steht. Damit liess sich
    beweisen, was sonst nur behauptet worden waere: Alle beruehrten
    Bildschirme bauen in allen drei Bewegungsstufen fehlerfrei, und die
    drei Uebergaenge liefern bei "aus" None. Der Lauf dauerte vier
    Sekunden und hinterliess weder `errors.txt` noch `traceback.txt`.
    **Zwei Fallen:** Mit `SDL_VIDEODRIVER=dummy` haengt der Lauf endlos -
    die Pausen laufen nie ab, weil keine Bilder entstehen; es braucht ein
    echtes Fenster. Und die Testsprache ist nicht Python: `if x:` und
    `assert a == b` sind dort keine gueltigen Bedingungen, beides muss
    als `$`-Zeile geschrieben werden. Die Testdatei ist nach dem Lauf
    wieder geloescht, weil der Auftrag sie nicht verlangt; der Weg steht
    hier, damit die naechste Sitzung ihn in zwei Minuten wiederholt.

63. **TEIL E.8 IST NICHT ERFUELLT: DIE BILDRATE IST NICHT GEMESSEN.**
    Der Auftrag verlangt eine Messung "auf dem Zielrechner" waehrend
    eines Kapitelwechsels und waehrend einer Einlage. Der Zielrechner ist
    der Schulrechner am Beamer, und den habe ich nicht. Eine Messung auf
    diesem Rechner waere keine Antwort auf die gestellte Frage, sondern
    eine andere Zahl mit demselben Namen. **Entscheidung: Dominik** - die
    Messung geht nur vor Ort. Ren'Py zeigt die Bildrate mit Umschalt+F.
    *(Nachtrag vom selben Tag: teilweise doch messbar, siehe 65.)*

## 5. September 2026 — Paket 7, die vier offenen Punkte

64. **`pruefen.py` UND `schicksalsprobe.py` LAUFEN UEBERHAUPT NICHT
    MEHR.** Punkt 61 war nur die halbe Wahrheit: Die Pfade in CLAUDE.md
    sind falsch, aber selbst mit dem richtigen Pfad und aus `game/`
    heraus bricht `pruefen.py` am gewachsenen `EINLAGEN`-Block ab und
    `schicksalsprobe.py` an `EPILOG_JAHR`, das es nicht kennt. Beide
    stammen vom 20. August und bauen die Spiellogik mit eigenen
    Platzhaltern nach — `variante()`, `welttext()` und `jahrestext()`
    stehen dort ein zweites Mal —, was Regel 11 heute ausschliesst.
    Das ist heikel, weil die Abnahme der Schritte 2 und 3 dieses Pakets
    "PRUEFEN MIT: pruefen.py" sagt. Geloest als Entscheidung 20:
    `probe_alles.py` ist das einzige Pruefwerkzeug, die beiden alten
    bleiben als Geschichte liegen, und was dem Werkbank-Bericht dafuer
    noch fehlt — die Spannweite der Wertaenderungen je Einlage — kommt in
    Schritt 2 dazu, wo sie ohnehin gebraucht wird.

65. **DIE BILDRATE IST DOCH ZU MESSEN, NUR NICHT AUF DEM ZIELRECHNER.**
    Ueber einen `DynamicDisplayable`, der bei jedem Bild sofort das
    naechste anfordert, laesst sich der reine Renderlauf zaehlen — ohne
    Bildschirmtakt, also mit sichtbarem Spielraum statt der ueblichen
    60 pro Sekunde. Gemessen auf diesem Rechner, Ren'Py 8.5:

    | Lage | Bilder | Mittel | 99 Prozent | langsamstes Bild |
    |---|---|---|---|---|
    | Kapitelwechsel (Fade und Jahresblatt) | 1853 | 1063/s | 596/s | 101,9 ms |
    | drei Karten laufen zugleich ein | 1151 | 590/s | 362/s | 22,5 ms |

    Zwei von 1852 und eines von 1150 Bildern lagen ueber 20 ms; in beiden
    Faellen war es das erste Bild nach dem Bildschirmwechsel, also das
    Anlegen der Flaechen und nicht die Bewegung.

    **Was das heisst:** Die schwerste Kartenlage kostet 1,7 ms je Bild.
    Ein Schulrechner muesste mehr als **elfmal langsamer** sein als
    dieser, um unter die geforderten 50 Bilder je Sekunde zu fallen.
    **Was es nicht heisst:** Faellt Ren'Py auf dem Schulrechner auf den
    Software-Renderer zurueck — kein OpenGL, alter Treiber —, gilt der
    Faktor nicht mehr, denn dann rechnet die CPU jede Flaeche einzeln.
    Genau dafuer gibt es die Stufe "sparsam". Der Punkt bleibt offen,
    aber er ist kein Risiko mehr, sondern eine Minute Nachsehen vor Ort.

## 5. September 2026 — Paket 7, Schritt 2 (Rotstift und acht Striche)

66. **"ACHT STRICHE" HATTE EINE RICHTIGE ANTWORT.** Der Auftrag verlangt
    in Teil B.3 den Nachweis, dass keine Verteilung in allen vier Werten
    ueberlegen ist - er setzt also voraus, dass es so ist. Es war nicht
    so. Vor jeder Aenderung durchgerechnet, alle 165 Verteilungen in
    sechs Lagen: **(4, 2, 2, 0) erreichte oder schlug jede andere.** Die
    Pareto-Front bestand aus einer einzigen Verteilung, sobald das Brot
    schimmelte, aus zweien sonst.

    Der Grund war Arithmetik und kein Versehen im Text: Satt werden
    kostet vier Teile, das Kind zwei, der Nachbar zwei — zusammen genau
    die acht, die auf dem Tisch liegen. Wer die drei Schwellen trifft,
    zahlt nichts dafuer. Die Einlage war damit eine Rechenaufgabe mit
    Loesung und keine Entscheidung mehr, entgegen Regel 5.

    Behoben mit einer Zeile: Wer sich die Haelfte nimmt, verliert einen
    Punkt Rueckhalt. Kein Strafpunkt, sondern eine Beobachtung — am Tisch
    sitzen vier, und drei sehen, wie gross dein Stueck ist. Danach:
    **null** Verteilungen, die alle anderen erreichen; Pareto-Front 16
    statt 1. Probe 10b misst es bei jedem Lauf neu, denn jede spaetere
    Aenderung an `portionen_auswerten()` kann den Zustand zurueckbringen.

    **Warum das keine Zahl im Sinne des Paketplans ist:** `rueckhalt` hat
    als einziger der vier Werte keine Abbruchschwelle in `ENDE_SCHWELLEN`.
    Eine Aenderung dort verschiebt die Korridore aus Entscheidung 11
    nicht — sie aendert den Lebenslauf, nicht das Ueberleben.

67. **DER ANTRAGSBOGEN LIEF AN DER SPRACHPROBE VORBEI.**
    `einlagentexte_sammeln()` holte `BRIEFBOGEN` und `BRIEF_VORSCHRIFT`,
    aber nicht `ANTRAGSBOGEN` und `ANTRAG_VORSCHRIFT`. Beide stehen seit
    Paket 5, Schritt 2 im Spiel und sind seither nie auf Tabubegriffe
    oder Satzlaenge gemessen worden. Ein Bogen, den niemand misst, ist
    genau der, auf dem der zu lange Satz stehen bleibt. Jetzt gesammelt,
    dazu die neuen Zustandssaetze: Probe 7 sieht 30945 statt 30105
    Stellen, Probe 8 misst 3945 statt 3874 Saetze, beide weiter null.

68. **DER TORNISTER SPRENGT `EINLAGE_HOECHSTWIRKUNG`.** Die neue Probe
    10a hat es beim ersten Lauf gefunden: Die Auswertung des Tornisters
    erzeugt bis zu **+4 Belastung**, die Grenze steht auf 3, und
    `einlage_begrenzen()` kappt still. Die Kappung ist ein Netz und kein
    Werkzeug — was sie schluckt, verspricht der Ausgangstext und loest
    der Wert nicht ein. **Gehoert zu Schritt 3**, der den Tornister
    ohnehin umbaut; Probe 10 steht bis dahin ehrlich auf 1 Beanstandung.

69. **KIND UND NACHBAR WERDEN UNGLEICH BEHANDELT, UND DAS IST RICHTIG SO.**
    Wer dem Kind nichts gibt, verliert einen Punkt Rueckhalt und dessen
    Zuwendung; wer dem Nachbarn nichts gibt, verliert nur die Zuwendung.
    Das sah nach einem vergessenen Zweig aus. Es bleibt, wie es ist, und
    steht jetzt als begruendeter Kommentar im Code: Der Nachbar ist kein
    Angehoeriger. Beim Kind sind Zuwendung und eigener Halt dasselbe,
    beim Nachbarn nicht.

70. **DIE KORREKTUR AN "ACHT STRICHE" HAT DIE ETAPPE AUF DIE KANTE
    GESCHOBEN — UND DER GRUND LIEGT IM MESSGERAET.**

    Ich hatte vor der Aenderung geprueft, ob sie Probe 4 bewegen kann,
    und geschlossen: nein, denn `rueckhalt` ist der einzige der vier
    Werte ohne Abbruchschwelle in `ENDE_SCHWELLEN`. Der Schluss war
    richtig und trotzdem falsch. Gemessen, voller Lauf, Etappe kurz bei
    kluger Wahl:

    | | nach Paket 6 | Saat (Vorgabe) | Saat 7 | Saat 99 | Saat 2026 |
    |---|---|---|---|---|---|
    | Etappe kurz, klug | 83,5 | **79,5** | 82,4 | 80,3 | **79,3** |

    Die Grenze steht auf 80. Zwei von vier Saaten reissen sie. Das ist
    keine Streuung um einen sicheren Wert, sondern ein Korridor auf der
    Kante — genau die Lage, vor der Entscheidung 13 gewarnt hat.

    **Der Mechanismus, gemessen und nicht vermutet:** Die Werkbank spielt
    "klug" so, dass sie die Option nimmt, die den **derzeit schlechtesten**
    Wert am wenigsten verschlechtert. Sie weiss nicht, dass Einsamkeit
    niemanden umbringt. Wird `rueckhalt` oefter zum schlechtesten Wert —
    und genau das tut die neue Zeile —, verteidigt "klug" einen Wert, an
    dem kein Durchgang endet, und laesst dabei die drei liegen, an denen
    er endet. Der Einbruch ist also **keine Eigenschaft des Spiels,
    sondern eine Eigenschaft des Stellvertreters**, mit dem wir es messen.

    Ein Mensch, der zum zweiten Mal spielt, merkt, dass Einsamkeit ihn
    nicht umbringt. Die Werkbank merkt es nie.

    **Das ist nicht meine Entscheidung.** Sie beruehrt den Korridor aus
    Entscheidung 11, und Entscheidung 11 ist bindend. Zwei Wege:

    **(a) So lassen.** Die Etappe ist duenn, das ist seit Entscheidung 15
    bekannt und an Paket 9 zugewiesen. Dies waere dieselbe Schwaeche einen
    Schritt weiter, nicht eine neue.

    **(b) "klug" umbauen**, so dass es die drei Werte mit Abbruchschwelle
    staerker gewichtet als den vierten. Das waere das ehrlichere Modell
    eines aufmerksamen Spielers — aber es hebt ALLE klug-Zahlen, und dann
    muessen die Korridore aus Entscheidung 11 im selben Zug neu gelesen
    werden.

    **Mein Rat ist (a), und zwar aus einem Grund, der nichts mit Bequem-
    lichkeit zu tun hat:** Wer das Messgeraet und die Messlatte in
    derselben Bewegung aendert, kann hinterher keine der beiden mehr
    pruefen. Und das eigentliche Problem der Etappe ist Inhalt, nicht
    Zahl — sie braucht Karten, auf denen das Schonen der Versorgung nicht
    den Verdacht kostet. Das steht schon als Punkt 42b bei Paket 9.

    Die Aenderung selbst nehme ich nicht zurueck: Ohne sie hat "Acht
    Striche" eine richtige Antwort (Punkt 66), und das verstoesst gegen
    Regel 5 und gegen Teil B.3 des Auftrags.
    **Entscheidung: Dominik.**
    *(Nachtrag desselben Tages: Die Begruendung oben ist zur Haelfte
    falsch — siehe 71. Entschieden als Entscheidung 21.)*

71. **MEINE BEGRUENDUNG ZU 70 WAR ZU BEQUEM: DAS SPIEL ZEIGT SELBST AUF
    DEN SCHWAECHSTEN WERT.** In Punkt 70 steht, der Einbruch sei "eine
    Eigenschaft des Messgeraets, nicht des Spiels" — die Werkbank schone
    stur den schlechtesten Wert und wisse nicht, dass Einsamkeit niemanden
    umbringt.

    Bevor ich daraus eine Entscheidung gemacht habe, habe ich nachgesehen,
    wo `schwaechster_wert()` sonst noch aufgerufen wird. Fuenf Stellen,
    und eine davon ist `zustandskopf` in `screens.rpy:518`: **Die
    Kopfleiste nennt der Spielerin auf jedem einzelnen Bildschirm genau
    diesen schwaechsten Wert**, mit Namen, Farbe und Satz.

    Die Werkbank spielt also nicht duemmer als das Spiel. Sie folgt dem
    Signal, das das Spiel selbst gibt. Der Einbruch ist damit echt: Wer
    der Kopfleiste folgt — und dafuer ist sie da —, verteidigt Einsamkeit
    und ueberlebt seltener.

    Das aendert die Entscheidung nicht, aber es aendert ihren Grund, und
    der Grund ist das, was in der naechsten Sitzung noch gilt. Nicht "das
    Messgeraet ist ungenau, also lassen wir es", sondern: **Das Spiel
    stellt genau diese Frage, und es soll sie stellen.** Entscheidung 10
    hat den Lebenslauf zum Ziel der Stunde gemacht. Rueckhalt ist der
    einzige Wert ohne Abbruchschwelle; wer ihn schont, zahlt mit
    Ueberlebenschance fuer Menschen. Ausgefuehrt als Entscheidung 21.

    **Die Lehre fuer mich, unabhaengig von diesem Fall:** Ich hatte eine
    Erklaerung, die zum gewuenschten Ergebnis passte, und war damit fast
    zufrieden. Fuenf Minuten grep haben sie halbiert. Eine Begruendung,
    die eine Entscheidung traegt, wird nachgesehen und nicht geschlossen.

## 5. September 2026 — Paket 7, Schritt 3 (Tornister und Fahrt aufs Land)

72. **ICH HABE minispiele.rpy MIT POWERSHELL BESCHAEDIGT.** Um zwei
    Aufrufe nachzuziehen, habe ich die Datei durch
    `Get-Content -Raw | Set-Content -Encoding utf8` geschickt.
    PowerShell 5.1 liest dabei als ANSI und schreibt als UTF-8 zurueck:
    Aus "Haelfte" wurde "HÃ¤lfte", aus "gross" "groÃŸ" - **in der ganzen
    Datei**, dazu eine BOM am Anfang.

    **Und der Lint lief durch.** Mojibake ist gueltiges UTF-8; kein
    Werkzeug des Projekts haette es gemeldet. Aufgefallen ist es nur,
    weil eine Editieroperation danach ihre Fundstelle nicht mehr fand -
    also durch Zufall.

    Wiederhergestellt aus dem Commit von Gruppe 1, die zwei
    Bildschirmaenderungen mit dem Editor wiederholt.

    **CLAUDE.md warnt vor PowerShell 5.1, aber nur fuer Commit-Meldungen.**
    Die Warnung ist zu eng: Sie gilt fuer JEDE Projektdatei. Wer eine
    `.rpy` oder `.py` aendern will, nimmt das Editierwerkzeug. Muss es
    doch die Shell sein, dann ueber .NET mit ausdruecklicher Kodierung:
    `[System.IO.File]::ReadAllText(p)` und
    `[System.IO.File]::WriteAllText(p, t, (New-Object System.Text.UTF8Encoding($false)))`.
    Der Zusatz `$false` verhindert die BOM. **Nie
    `Get-Content | Set-Content` auf einer Datei mit Umlauten.**
    In CLAUDE.md nachgetragen.

73. **DIE ETAPPE HATTE KEINE VERTIEFUNG IM TORNISTER.** Die Einlage
    laeuft auf Front und Etappe, `quelle["vertiefung"]` kannte aber nur
    den Schluessel "front". In Paket 8, Schritt 3 waere auf dem
    Etappenpfad ein Glossareintrag ueber den Vormarsch vom August 1914
    erschienen - und der handelt von einem anderen Marsch. Ergaenzt.

74. **DER NACHWEIS AUS TEIL A.2 IST GEFUEHRT, UND ER BRAUCHTE EINEN NEUEN
    WEG IN DER WERKBANK.** Ob ein Ende unausweichlich wird, laesst sich
    am Quelltext nicht ablesen: `ohne_mantel` erhoeht die Ziehchance von
    vier Karten, und was daraus wird, entscheidet der Durchgang.
    `Werkbank.durchgang()` nimmt jetzt `vorbelastung` entgegen und setzt
    Merkmale, bevor der erste Wuerfel faellt. Probe 10e spielt damit
    jede Lage zweimal - einmal mit allen sieben Merkmalen, einmal ohne.

    Gemessen, 200 Durchgaenge je Lage und Gruppe, Strategie "zufall",
    zwei Laeufe mit verschiedenen Zufallsstroemen:

    | Lage | ohne | mit | Abstand | zweiter Lauf |
    |---|---|---|---|---|
    | Front kurz | 56,5 | 50,0 | −6,5 | +1,5 |
    | Front lang | 31,5 | 29,5 | −2,0 | +5,5 |
    | Etappe kurz | 57,5 | 55,0 | −2,5 | −2,5 |
    | Etappe lang | 23,0 | 21,0 | −2,0 | −7,0 |
    | Heimat kurz | 46,0 | 38,0 | −8,0 | +7,5 |
    | Heimat lang | 22,5 | 25,5 | +3,0 | +6,0 |

    **Kein toter Pfad, in keinem der zwoelf Faelle.** Das ist das
    Ergebnis. Der Abstand dagegen schwankt zwischen −8,0 und +7,5 und
    wechselt zwischen den Laeufen sogar das Vorzeichen - bei 200
    Durchgaengen ist er Rauschen und kein Messwert. **Wer aus dieser
    Spalte eine Aussage machen will, braucht mehr Durchgaenge**; fuer die
    gestellte Frage braucht es sie nicht.

    Beanstandet wird in dieser Probe ausschliesslich 0,0 Prozent - keine
    erfundene Schwelle, sondern der Satz aus Entscheidung 11. Wo die
    Grenze zwischen "spuerbar" und "zu viel" laege, entscheidet keine
    Probe.

75. **ETAPPE KURZ STEHT HEUTE BEI 81,2 UND IST TROTZDEM NICHT REPARIERT.**
    Der volle Lauf nach Schritt 3 meldet fuer Probe 4 nur noch eine
    Beanstandung: Etappe kurz liegt bei kluger Wahl ueber der Grenze von
    80. Das sieht aus, als haette sich Punkt 70 erledigt.

    **Hat es nicht.** Die neuen Merkmale und Gewichtszuschlaege haben den
    Zufallsstrom verschoben, und diese Saat faellt guenstig. Die vier
    Messungen vom selben Tag lagen bei 79,5 / 82,4 / 80,3 / 79,3 - die
    Lage steht auf der Kante, und heute steht sie auf der guten Seite
    davon. Entscheidung 21 gilt unveraendert, der Punkt bleibt bei
    Paket 9. Wer die Zahl in einem einzelnen Lauf sieht und daraus
    schliesst, es sei behoben, hat eine Streuung fuer eine Reparatur
    gehalten.

---

## 5. September 2026 — Paket 8, Schritt 1

76. **JEDE ENTSCHEIDUNGSKARTE STEHT DREISSIG PIXEL ÜBER DEN UNTEREN
    BILDRAND HINAUS.** Gemessen an einem Bildschirmabzug, nicht geschätzt:
    Die Karte beginnt bei y=550 und ist 560 Pixel hoch, das Bild ist 1080
    hoch. Es fehlen dreißig Pixel, und zwar bei **allen fünf Kartentypen**
    — auch bei dem aus Paket 7 unveränderten Bogen.

    Bis heute ist es niemandem aufgefallen, und das hat einen Grund: Bei
    den bisherigen Karten wird unten nur leeres Papier abgeschnitten. Der
    Inhalt sitzt in einem `vbox` mit `yalign 0.5` und endet weit vorher.
    Erst das Stempelfeld des amtlichen Vordrucks, das absichtlich ganz
    unten sitzt, hat die Zone sichtbar gemacht.

    **Weder Lint noch eine Probe finden so etwas.** Der Lint prüft
    Syntax, die Werkbank prüft Zahlen; dass ein Bildschirm über seinen
    Rand hinausragt, sieht man nur, wenn man hinsieht. Das ist das
    Argument für offenen Punkt 62 — Ren'Pys Testbefehl und ein Abzug
    gehören zu jedem Schritt mit Bildschirmarbeit.

    Nicht behoben: Das ist Paket-7-Layout und betrifft jede Karte.
    **Paket 8, Schritt 2** prüft laut Auftrag ausdrücklich, dass keine
    Karte überläuft — dort gehört es hin. Mein eigenes Blatt hält sich
    einstweilen von den letzten vierzig Pixeln fern.

77. **BEI LANGEN EREIGNISTEXTEN LÄUFT DER TEXT IN DIE KOPFLEISTE.** Der
    Ereignistext liegt in einem `fixed` mit 1440 mal 170 Pixeln bei
    ypos 240, zentriert über `align (0.5, 0.5)`. Ein Text, der mehr als
    vier Zeilen braucht, wächst über dieses Feld hinaus — nach oben
    genauso wie nach unten, weil er zentriert ist. Bei
    `heimat_1917_hilfsdienst` sind es fünf Zeilen; die erste steht dann
    über der roten Trennlinie und überlagert den Zustandssatz der
    Kopfleiste.

    Der Text selbst ist regelkonform: fünf Sätze, keiner über zwanzig
    Wörter. Das Feld ist zu klein, nicht der Text zu lang. Betroffen
    sind alle Ereignisse mit langem Text; wie viele es sind, hat noch
    niemand gezählt — das gehört zu **Paket 8, Schritt 2**, wo die
    Schriftgröße ohnehin dreistufig wird und das Problem bei „sehr groß"
    jede Karte trifft.

78. **NICHT DREI BILDMASSE WAREN TOT, SONDERN DIE GANZE TAFEL.** Der
    Auftrag fragt nach `personen`, `orte` und `dokumente` — die drei, die
    Probe 6 als „angelegt, aber nie abgerufen" meldet. Beim Nachzählen
    (Regel 9) zeigt sich mehr: **`BILD_MASSE` wird von keiner einzigen
    Stelle im Spiel gelesen.** `bild_masse_holen()` liest ausschließlich
    `BILD_ANZEIGE`; die andere Tafel stand nur da, damit die Probe sie
    beanstanden kann. Das ist ein Kreis, kein Prüfen.

    Auch `BILD_ANZEIGE` greift weniger, als es scheint: `bild_anzeigen()`
    hat im ganzen Spiel **einen** Aufrufer, und der übergibt seine Maße
    ausdrücklich mit. Wirksam ist die Tafel nur für `portraits`, über
    `portrait_anzeigen()`.

    Nicht gelöscht, sondern beschäftigt: `MEDIEN.md` nennt jetzt je
    Kategorie das **Ablagemaß** aus `BILD_MASSE` und das **Anzeigemaß**
    aus `BILD_ANZEIGE`. Damit hat die erste Tafel zum ersten Mal einen
    Leser, und die beiden Maße bekommen verschiedene Aufgaben statt einer
    doppelten.

79. **DIE ABSICHERUNG AUS ENTSCHEIDUNG 16 HAT ZUM ERSTEN MAL EINEN
    ECHTEN FEHLER GEFANGEN.** Die Vergabe der Kartentypen stand zuerst
    bei den anderen Nachträgen in `kapitel.rpy` und fand nur **10 von
    25** Ereignissen. Der Grund: Bei gleichem init-Rang entscheidet die
    Stelle in der Datei, und fünfzehn dieser Ereignisse entstehen weiter
    unten in derselben Datei. Gefunden hat es nicht der Lint und nicht
    das Auge, sondern die Zahl im Bericht — 90 statt 75 Karten vom Typ
    `karte`.

    `NACHTRAG_OHNE_TREFFER` hat jeden der fünfzehn gemeldet. Genau dafür
    ist die Liste am 4. September angelegt worden, und sie hat gehalten.
    Die Lehre für jeden künftigen Nachtrag: **Ein init-Rang allein sagt
    nichts, wenn die Tabelle Ereignisse aus derselben Datei anfasst.**
    Die Vergabe steht jetzt in einem `init 4`-Block am Dateiende — Rang 4
    hat sonst kein Block im Projekt.

80. **EIN NAMENSFILTER NACH PRÄFIX IST KEINE LISTE.** Die Medienprobe
    sollte die Schriften nicht mehr namentlich aufzählen, damit eine
    vierte nicht stillschweigend aus dem Bericht fällt. Der erste Versuch
    suchte im Namensraum nach allem, was mit `SCHRIFT_` anfängt — und zog
    prompt `SCHRIFT_KANDIDATEN` und `SCHRIFT_ZWECK` als „Schriften" mit
    in die Liste. Behoben, indem die Kandidatentafel selbst gefragt wird.
    Dieselbe Falle wartet überall dort, wo ein Präfix für eine Zugehörig-
    keit gehalten wird.

81. **DER KONTRAST REISST, UND AN EINER STELLE DEUTLICH.**
    `KONTRAST.md` rechnet jede vorkommende Kombination nach WCAG 2.1
    gegen die für den Beamer verlangten 7:1. **25 Kombinationen bleiben
    darunter.** Die meisten knapp und mit einem Vorschlag zu beheben, der
    kaum sichtbar ist — `FARBE_AKZENT` bräuchte von `#8a3324` nur nach
    `#863123`.

    Eine Gruppe fällt aus dem Rahmen:

    | Farbe | auf Papier | verlangt |
    |---|---|---|
    | `FARBE_LINIE` `#8d8578` | **3,01:1** | 7:1 |
    | `FARBE_LINIE` auf hellem Papier | **3,29:1** | 7:1 |
    | `FARBE_LINIE` auf dunklem Papier | **2,64:1** | 7:1 |
    | `FARBE_LINIE_FEIN` `#b6ae9e` | **1,99:1** | 7:1 |

    Das sind keine Rahmenlinien, sondern **Text**: 31 Stellen benutzen
    `FARBE_LINIE` als Schriftfarbe für Hinweise, Rubriken und ruhige
    Zweitzeilen. In der letzten Reihe eines hellen Klassenzimmers ist das
    nicht zu lesen.

    Nichts geändert — die Farbwelt ist das Gesicht des Spiels, und der
    Auftrag verlangt für jede Farbänderung Dominiks Zustimmung.

82. **`brief_stempel` IN figuren.rpy HEISST SO UND IST KEINER.** Beim
    Vergeben von `SCHRIFT_SCHMAL` an die Aufdrucke fiel auf: Der Stil
    heißt nach einem Stempel, ist aber kursiv, 19 Pixel, ohne Fettung und
    ohne Sperrung — und er trägt das Briefdatum (`merkbuch.rpy:1179`).
    Die drei echten Aufdrucke heißen `karte_stempel`, `bogen_stempel` und
    `post_stempel_text` und sind alle fett und gesperrt.

    Nicht umbenannt (Regel 9) und nicht auf die neue Schrift gestellt —
    er ist keiner. Gemeldet, damit der Name nicht das nächste Mal jemanden
    in die Irre führt. Es ist derselbe Fall wie `blase_blinken`
    (Entscheidung 18).

83. **ZWEI KARTENBILDER GEHÖREN ZU KEINEM EREIGNIS.**
    `images/karten/front_beginn_1.png` und `_2.png` liegen im Projekt und
    folgen dem Namensschema `<kennung>_<nummer>.png` — aber ein Ereignis
    `front_beginn` gibt es im Bestand nicht. Entweder ist die Karte
    einmal umbenannt worden, oder die Bilder stammen aus einem früheren
    Entwurf. Sie sind die einzigen beiden echten Kartenbilder im ganzen
    Projekt, also nicht wenig.

    In `MEDIEN.md` stehen sie unter „Vorhanden, aber unbenutzt" mit dem
    Vorschlag, sie `front_1914_marsch` zuzuordnen — das ist ein Vorschlag
    und keine Entscheidung.

---

## 5. September 2026 — die offenen Punkte, eigenmächtig gelöst

84. **DIE URSACHE VON PUNKT 76 WAR `rotate_pad`, UND DIE ZAHL HAT SIE
    VERRATEN.** Der Versatz betrug exakt 102 Pixel, in jedem Zusammenhang
    gleich — auch wenn ich die Karte allein auf einen leeren Bildschirm
    legte. Eine konstante Zahl, die vom Kontext unabhängig ist, steckt im
    Element selbst.

    Ren'Py polstert ein gedrehtes Bild auf seine **Diagonale**, damit bei
    45 Grad keine Ecke abgeschnitten wird. Für eine Karte von 520 mal 560
    sind das √(520² + 560²) = 764 Pixel, und **(764 − 560) / 2 = 102**.
    Die Karte saß mittig in einem unsichtbaren 764er Kasten.

    `karte_kommt` dreht um 1,2 Grad, `umschlag_oeffnet` um 1,4. Bei
    solchen Winkeln wird nichts abgeschnitten — der Überstand beträgt
    560 · sin(1,2°) = 11,7 Pixel und liegt im Rahmen des Buttons. Beide
    haben jetzt `rotate_pad False`.

    **Nachgemessen statt behauptet:** Vorher saß die Karte bei ypos 100
    auf y=202, jetzt auf y=102. Im Spiel vorher 550 bis über den Bildrand,
    jetzt 486 bis 1034 mit 46 Pixeln Luft.

    Die Lehre ist allgemein: **Jede Drehung in einem transform kostet
    Platz, auch eine winzige.** Wer künftig `rotate` in ein Bewegungswort
    schreibt, schreibt `rotate_pad False` dazu — oder rechnet nach, wie
    viel die Diagonale frisst.

85. **PUNKT 77 WAR KEIN EINZELFALL, SONDERN DIE REGEL.** Gemessen über
    alle 184 Textfassungen des Bestands:

    | Zeilen | Fassungen | Anteil |
    |---|---|---|
    | 2 | 5 | 2,7 % |
    | 3 | 32 | 17,4 % |
    | 4 | 122 | **66,3 %** |
    | 5 | 24 | 13,0 % |
    | 6 | 1 | 0,5 % |

    Das Feld hielt bei 170 Pixeln und 44 Pixeln Zeilenhöhe **3,9 Zeilen**.
    **Vier von fünf Ereignistexten liefen also über** — bei vier Zeilen um
    sechs Pixel, was niemand sieht, bei fünf um fünfundzwanzig nach oben
    in die Kopfleiste.

    Ich hatte in Punkt 77 geschrieben, „wie viele es sind, hat noch
    niemand gezählt". Das war der Kern: Ohne die Zählung sah es nach einem
    Ausreißer aus, mit ihr nach einem Konstruktionsfehler. Das Feld hält
    jetzt fünf Zeilen (224 Pixel), und für die längsten Fassungen rückt
    die Schrift eine Stufe herunter. Die Grenze von 330 Zeichen ist
    gerechnet, nicht geraten.

86. **DAS GRÖSSTE SICHTBARE PROBLEM WAR KEINES AUS DER LISTE.** Von 333
    erwarteten Dateien fehlen 326. Jede davon zeigte bis heute ihren
    Dateipfad **in Rot** auf dem Bildschirm. Für die Arbeit ist das
    richtig; in einer Schulstunde sieht ein Spiel mit dreihundert roten
    Meldungen nicht unfertig aus, sondern kaputt — und über einer Karte
    mit Warnung liest niemand den Text.

    Der Platzhalter hat jetzt zwei Gesichter, unterschieden durch
    `persistent.analysemodus`, der im Projekt längst die Werkzeugsicht
    schaltet und ab Werk aus ist: im Spiel eine ruhige getönte Fläche mit
    vier Eckwinkeln, wie die Ecken eines ins Album geklebten Fotos; im
    Analysemodus zusätzlich der Pfad wie bisher.

    **Das Spiel sieht damit auch ohne eine einzige Bilddatei fertig aus.**
    Die Bilder sind ab jetzt eine Verbesserung und keine Bedingung mehr —
    und das entlastet den Zeitplan mehr als jede Recherche.

87. **DIE BEIDEN VORHANDENEN KARTENBILDER SIND KI-ILLUSTRATIONEN, KEINE
    FOTOS — UND IHRE MOTIVE PASSEN NICHT ZU IHREM NAMEN.**
    `front_beginn_1.png` zeigt eine leere Kopfsteinstraße mit Fachwerk in
    der Dämmerung, also eine Heimatszene; `front_beginn_2.png` einen
    Schreibtisch mit Petroleumlampe, Federkiel, Taschenuhr und einem
    gefalteten Brief. Mit einem Frontbeginn hat weder das eine noch das
    andere zu tun. Die Schriften auf den Dokumenten sind unleserliche
    Kritzelzeilen — das verrät die Herkunft.

    **Zugeordnet habe ich sie trotzdem nicht**, und das ist eine
    Entscheidung mit Begründung: Ein einzelnes bebildertes Ereignis unter
    hundert unbebilderten sieht schlechter aus als hundert gleich
    behandelte Leerstellen. Die neue Leerstelle ist ruhig und einheitlich;
    ein einzelnes Bild dazwischen bricht die Ruhe auf und lässt alles
    andere wie einen Fehler wirken. **Konsistenz schlägt hier
    Einzelqualität.** Sinnvoll wird das erste Bild, sobald ein ganzer
    Zusammenhang bebildert ist: ein Jahr, ein Pfad oder alle Karten eines
    Typs.

    Der Befund ändert die Auskunft, die ich Dominik zur Bilderfrage
    gegeben hatte, und zwar in einem wesentlichen Punkt: Ich hatte von
    erzeugten Bildern abgeraten. Das gilt für **Fotografien**, die
    vorgeben, Quelle zu sein. Für **Illustrationen**, die erkennbar
    gezeichnet sind, gilt es nicht — sie behaupten nichts, sie zeigen.
    Das ist ein Unterschied, den ich beim ersten Mal nicht gemacht habe.

---

## 5. September 2026 — Paket 8, Schritt 2.3

88. **EIN ZENTRIERTER TEXT, DER NICHT PASST, VERLIERT BEIDE ENDEN.** Der
    erste Entwurf der Schriftvergrößerung setzte den Ereignistext wie
    bisher mit `align (0.5, 0.5)` in ein Feld fester Höhe und legte einen
    `viewport` darum. Auf dem Abzug bei großer Schrift fehlte daraufhin
    **der ganze erste Satz** — der Text ragte oben und unten heraus, und
    der viewport schnitt beides ab. Man sah die Mitte eines Textes und
    merkte nicht, dass ein Anfang fehlt.

    Das ist die tückischere Hälfte des Problems: Ein abgeschnittenes Ende
    fällt auf, ein abgeschnittener Anfang nicht. Der Text steht jetzt oben
    im Feld. Fehlt etwas, dann hinten — und das holt das Mausrad.

89. **`font size` VERGRÖSSERT DIE SCHRIFT, NICHT DAS LAYOUT — UND DAS IST
    RICHTIG SO.** Ren'Pys eingebaute Einstellung skaliert jeden Text im
    Spiel, ohne dass irgendwo eine Liste von Stilen zu pflegen wäre. Jedes
    Feld mit fester Höhe wird dadurch aber zu klein. Gemessen an einem
    Abzug bei Faktor 1,3:

    - Die Kopfleiste blieb 204 Pixel hoch, „Ein paar Leute" brach auf zwei
      Zeilen um und schob sich über die Trennlinie.
    - Der Ereignistext wanderte nach oben und überdeckte den Zustandssatz.

    Behoben, indem von unten gerechnet wird: Die **Karte steht fest** —
    man kann nicht zwischen zwei Optionen wählen, von denen man eine nur
    halb sieht. Die **Kopfleiste wächst** mit der Schrift, sonst quillt sie
    über. Der **Ereignistext bekommt, was übrig bleibt**, und scrollt in
    seinem Feld, wenn das nicht reicht; ein Erzähltext verträgt das, weil
    man ihn von oben liest.

    Die Feldhöhe wird auf volle Zeilen abgerundet. Eine halb
    durchgeschnittene Zeile sieht nach Fehler aus, eine ganze nach „hier
    geht es weiter".

90. **DIE VORLESEFUNKTION LÄSST SICH BELEGEN, STATT SIE ZU BEHAUPTEN.**
    Ren'Py leitet seine Sprachausgabe über `config.tts_function`; wer die
    Funktion vorübergehend austauscht, bekommt wörtlich mitgeschrieben,
    was gesprochen würde. Das Ergebnis für die beiden Hauptbildschirme:

    ```
    Jahr 1917 - Langer Verlauf: Rüstungsbetrieb: HUNGER: Der Gürtel
    sitzt zwei Löcher enger als im August 1914.: Deine Rolle: Der
    Meister ruft dich ins Kontor, [...] die Erlaubnis des alten Werks.
    ```

    Gelesen werden also **Jahr, Ort, Zustandssatz und der vollständige
    Ereignistext** — auch der Teil, den man bei großer Schrift scrollen
    müsste. Auf dem Ausgangsbildschirm zusätzlich der Optionstitel, der
    Ausgangstext und sogar das Wertefeedback („Hunger: +2: Erschöpfung:
    +1").

    **Was nicht mitgelesen wird:** die beiden Optionen auf der
    Entscheidungskarte. Sie sind Schaltflächen, und Ren'Py liest eine
    Schaltfläche erst, wenn sie den Zeiger bekommt. Das ist kein Fehler
    und bleibt mausbedienbar — es heißt aber, dass man die Wahl abfahren
    muss, statt sie am Stück zu hören.

    Ebenfalls stumm sind die **Wertebalken**: Sie bestehen aus Flächen,
    nicht aus Text. Die Auskunft geht nicht verloren, weil der
    Zustandssatz daneben („Hungrig", „Am Ende") dasselbe in Worten sagt —
    und der wird gelesen.

91. **NUR ZWEI VON FÜNFUNDSECHZIG BILDSCHIRMEN SIND BEI GROSSER SCHRIFT
    GEPRÜFT.** Belegt sind `karten_entscheidung` und `karten_ausgang`,
    jeweils bei allen drei Stufen und mit nachgemessener Kartenlage
    (y=485 bis 1033, 27 Pixel Luft, bei jeder Stufe gleich). **Ungeprüft
    sind die Einlagen, das Merkbuch, der Lebenslauf, der Endbildschirm und
    die Menüs.** Dort kann bei „sehr groß" etwas überlaufen, ohne dass es
    jemand gesehen hat.

    Das ist kein Versäumnis dieses Unterabschnitts, sondern seine Grenze:
    Die Einlagen kommen in 2.6 und das Onboarding in 2.4 ohnehin unter die
    Hand, und was dort auffällt, gehört dorthin. Wer aber vorher eine
    Schulstunde plant, sollte die drei Stufen einmal durchklicken.

---

## 5. September 2026 — Paket 8, Schritt 2.4 (Onboarding)

92. **DIE VIER WERTE IN DER KOPFLEISTE WAREN NIE ANKLICKBAR.** Teil B,
    Punkt 7 fragt, ob eine Schülerin *erkennt*, dass sie anklickbar sind.
    Sie waren es nicht: `action NullAction()`, ein reines Hover-Feld, und
    `background None` — ohne Zeiger darauf stand dort kein einziges
    Zeichen, dass es etwas zu holen gibt. Die Frage des Auftrags war also
    nicht zu beantworten, sondern zuerst herzustellen (Regel 9: was im
    Auftrag steht, ist ein Hinweis, kein Beweis).

    Gebaut ist jetzt beides: ein ruhender Rahmen, damit man vier *Felder*
    sieht statt vier Beschriftungen, und ein Klick, der die Erklärung
    anheftet. Das Anheften ist nicht Bequemlichkeit — der Kasten ist bei
    normaler Schrift 643 Pixel hoch, und ihn zu lesen hieße bisher, die
    Maus die ganze Zeit auf einem 250 Pixel breiten Feld stillzuhalten.

93. **DIE WICHTIGSTE LEHRE DES TAGES: `Preference("font size", x)` IST
    EINE LISTE VON AKTIONEN, KEINE AKTION.** Direkt aufgerufen gibt das
    `TypeError: 'RevertableList' object is not callable`. Und wer die
    Einstellung stattdessen einfach zuweist (`_preferences.font_size =
    1.3`), bekommt keinen Fehler, sondern etwas Schlimmeres: **Die
    Container wachsen, die Schrift nicht.** Alles, was `schriftfaktor()`
    fragt — Kopfleiste, Feldhöhen —, wird größer; jeder Text bleibt klein,
    weil die Stile nicht neu gebaut werden.

    Der erste Abzugslauf sah damit aus wie ein Beleg für „bei sehr groß
    passt alles" — und war einer für gar nichts. Richtig ist
    `renpy.run(Preference("font size", faktor))` und danach
    `renpy.style.rebuild()`. Erst der zweite Lauf hat gezeigt, dass der
    Erklärkasten unten aus dem Bild läuft.

    Das ist dieselbe Sorte Fehler wie die grüne Null vom 4. September
    (Regel 11): eine Messung, die nicht das misst, was auf ihrem Schild
    steht.

94. **DER ERKLÄRKASTEN LIEF BEI „SEHR GROSS" UNTEN UND LINKS AUS DEM
    BILD — UND ZWAR SCHON VOR 2.4.** Gemessen am Abzug bei Faktor 1,3:
    Der Kasten ist rund 950 Pixel hoch, die Kopfleiste endet bei 281; die
    letzten drei Zeilen standen unter dem Bildrand, darunter der Satz, der
    sagt, wie man ihn wieder zumacht. Links wandert die erste Wertspalte
    auf Mitte 257, ein 572 Pixel breiter Kasten begänne dort bei −29.

    Aufgefallen ist es erst durch 2.4, weil der Kasten vorher am Zeiger
    hing: Er verschwand, sobald man ihn ansehen wollte. **Ein Mangel, den
    man nicht lange genug sehen kann, um ihn zu bemerken.**

    Behoben mit derselben Antwort, die Schritt 2.3 dem Ereignistext
    gegeben hat — was nicht passt, rollt in seinem Feld —, dazu eine
    Klammer für die Lage am Bildrand.

95. **EIN `viewport` SCHRUMPFT NICHT AUF SEINEN INHALT.** `ymaximum`
    begrenzt ihn, aber er nimmt sich trotzdem den ganzen erlaubten Platz:
    Unter dem letzten Satz stand danach ein handbreites leeres Feld. Wer
    ein Rollfeld will, das mitwächst und erst am Ende rollt, braucht eine
    Höhe, die er selbst rechnet — hier `min(Inhalt × Schriftfaktor,
    verfügbarer Raum)`. Die Inhaltszahl ist am Abzug gemessen (643, mit
    Luft 660) und muss nachgemessen werden, wenn der Kasten je mehr Text
    bekommt.

96. **EIN MITTIG AUSGERICHTETER KASTEN VERLIERT BEI UNGERADER GESAMTHÖHE
    SEINE OBERSTE PIXELZEILE.** Auf dem ersten Abzug fehlte dem obersten
    der drei Grundsatzrahmen die Oberkante — nur ihm, bei identischem
    Code; die beiden darunter waren vollständig. Nachgemessen im Bild:
    Feld 1 hatte bei y=292 nur seine beiden senkrechten Kanten, Feld 2 bei
    y=370 volle 932 Pixel Linie. Bei Faktor 1,3 (andere Gesamthöhe) war
    die Kante da.

    Ursache ist die halbe Pixelzeile, die `align (0.5, 0.5)` bei ungerader
    Höhe erzeugt. Eine zwei Pixel starke Linie überlebt das sichtbar. Das
    ist die kleine Schwester von AUFGEFALLEN 84 (`rotate_pad`): **Ren'Py
    rechnet, und das Ergebnis ist nicht immer eine ganze Zahl.** Für den
    Beamer ist die dickere Linie ohnehin die richtige — auf sechs Meter
    ist eine Haarlinie keine Linie mehr.

97. **DER EREIGNISTEXT IST BEI „SEHR GROSS" IN DER LETZTEN ZEILE
    WAAGERECHT DURCHGESCHNITTEN.** Zu sehen auf dem Abzug der Kopfleiste
    bei Faktor 1,3: Von „Vor dir legt eine Frau" fehlen die Unterlängen.
    `ereignisfeld_hoehe()` rundet auf volle Zeilen ab (AUFGEFALLEN 89),
    rechnet dabei aber mit `EREIGNIS_TEXT_GRUND + 10` — also mit der
    Schriftgröße plus Zeilenabstand, nicht mit der wirklichen Zeilenhöhe,
    die bei DejaVuSans deutlich darüber liegt.

    **Nicht angefasst.** Das ist die Feldrechnung aus Schritt 2.3, und die
    richtige Zahl hängt an der Schrift, die dort später wirklich steht
    (M2). Genau davor warnt AUFGEFALLEN 89 selbst: Eine halb
    durchgeschnittene Zeile sieht nach Fehler aus.

98. **`tastenhinweis` HEISST NACH TASTEN UND TRÄGT MAUSHINWEISE.** Der
    Stil führt seit Paket 2 die leisen Zeilen unter einem Bildschirm
    („Auswahl mit einem Mausklick.") und bekommt in 2.4 eine weitere
    („Klicke irgendwo daneben, um wieder zuzumachen."). Sein Name
    widerspricht Regel 2, sein Inhalt nicht. **Nicht umbenannt** (Regel 9),
    nur gemeldet — dieselbe Sorte Falle wie `brief_stempel`
    (AUFGEFALLEN 82).

---

## 5. September 2026 — offener Punkt 97, nachgemessen und gelöst

99. **DAS EREIGNISFELD HAT NIE FÜNF ZEILEN GEHALTEN — AUCH NICHT BEI
    NORMALER SCHRIFT.** Punkt 97 hatte ich als Sache der großen Schrift
    notiert. Die Messung sagt etwas anderes. Gemessen wird am gerenderten
    Text: zwei Zeilen minus eine Zeile ist der wirkliche Vorschub.

    | Schriftstufe | Vorschub | Schätzung im Code | Feld | passt |
    |---|---|---|---|---|
    | normal (1,0) | **51** | 44 | 220 | **4,31 Zeilen** |
    | groß (1,15) | 57 | 51 | 204 | 3,58 |
    | sehr groß (1,3) | 63 | 57 | 171 | 2,71 |

    Die Rechnung nahm „Schriftgröße plus Zeilenabstand" — 34 + 10 = 44.
    **Eine Schrift ist aber höher als ihre Punktgröße:** bei DejaVuSans
    das 1,205-Fache, macht 41, und erst darauf kommen die 10 Pixel
    Zeilenabstand. Sieben Pixel Unterschied je Zeile, fünf Zeilen, 35
    Pixel — genau die Zeile, die fehlte.

    Damit ist die Zahl **fünf Zeilen** aus AUFGEFALLEN 77 von Anfang an
    eine Zeile zu hoch gewesen. Das Feld sah aus wie fünf ganze Zeilen,
    weil 220 durch 44 ohne Rest teilbar ist — die Rundung auf volle Zeilen
    aus AUFGEFALLEN 89 rundete sauber auf ein falsches Maß. **Eine
    Rechnung, die aufgeht, ist noch keine richtige.**

    **Behoben, indem gemessen statt geschätzt wird.**
    `ereignis_zeilenhoehe()` rendert einmal je Größe und Schriftstufe zwei
    Zeilen und eine und merkt sich die Differenz. Das bleibt richtig, wenn
    in `fonts/` eines Tages echte Dateien liegen statt DejaVuSans — eine
    festgeschriebene Zahl täte das nicht. Schlägt die Messung fehl (die
    Werkbank hat keine Grafikschicht), rechnet die Rückfallebene mit dem
    gemessenen Faktor 1,205 und merkt sich das Ergebnis **nicht**.

    **Und der Text gehört in die Rechnung.** Lange Fassungen werden eine
    Stufe kleiner gesetzt (`ereignis_schriftgroesse`), ihr Vorschub ist
    46 statt 51. Ein Feld, das auf die große Schrift gerundet ist,
    schneidet die kleine wieder an — dieselbe Falle, eine Ebene tiefer.
    `ereignisfeld_hoehe()` nimmt den Text jetzt entgegen.

    Nachgemessen nach der Änderung, mit dem längsten Text des Spiels
    (`heimat_1917_hilfsdienst`, 408 Zeichen): **5,00 / 4,00 / 3,00 ganze
    Zeilen, Rest 0** bei den drei Stufen. Bei normaler Schrift steht er
    damit **vollständig im Feld**, ohne dass jemand rollen muss — vorher
    war seine letzte Zeile zu einem Drittel abgeschnitten.

---

## 5. September 2026 — offener Punkt 91, die Sichtprobe bei „sehr groß"

100. **DIE EINLAGEN SIND BEI „SEHR GROSS" NICHT BEDIENBAR.** Punkt 91
    verlangte, die übrigen Bildschirme bei Faktor 1,3 anzusehen. **21
    Bildschirme abgezogen**, einer je Abzug, alle bei 1,3. Das Ergebnis
    ist in vier Gruppen zu fassen.

    **Unauffällig (14):** `modus_waehlen`, `herkunft_waehlen`,
    `person_waehlen`, `musterungsbogen`, `kein_musterungsbogen`,
    `erwerb_waehlen`, `jahreskarte`, `jahresabschluss`, `einlage_ausgang`,
    `ende_bildschirm`, `ende_lebenslauf_bildschirm`, `main_menu`,
    `preferences`, `merkbuch_anlegen`. Der Lebenslauf schneidet im rechten
    Rollfeld eine Zeile an, hat dort aber einen sichtbaren Rollbalken —
    das ist ein Rollzeichen und kein Überlauf.

    **Kaputt (4): alle vier Einlagen.** Bei 1,3 stehen dort drei Dinge
    übereinander, die bei 1,0 untereinander stehen:

    - Der **Titel** lag in der Kopfleiste. `einlage_kopf` setzte ihn auf
      die feste `ypos 228`, und die Kopfleiste wird bei 1,3 265 hoch.
      **Behoben** — `kopfhoehe() + 24` ergibt bei normaler Schrift genau
      dieselben 228 und wandert mit.
    - Der **Inhalt** (Bogen, Portionsliste, Tornisterfächer) beginnt bei
      einer festen `ypos` und schiebt sich damit über die Einleitung.
    - **Zähler und Handlungsknopf** stehen auf festen `ypos` nahe 950 bis
      1024 und liegen dann mitten im Inhalt. Beim Tornister laufen dazu
      die Sachtexte aus ihren Kästchen („dem Heer.", „angesehen.").

    In `minispiele.rpy` stehen **17 feste `ypos`-Werte**, alle auf Faktor
    1,0 eingerichtet. Zwei davon sind jetzt an `kopfhoehe()` gehängt; die
    übrigen fünfzehn sind kein Handgriff, sondern der senkrechte Rhythmus
    von vier Bildschirmen. **Das ist ein eigener Schritt und keine
    Nebenarbeit** — er steht als offener Punkt in Abschnitt A.

    **Ein Überlauf außerhalb der Einlagen, behoben:**
    `lebenslage_uebersicht` schnitt bei 1,3 den Knopf „So beginnt es" am
    unteren Bildrand ab — den Knopf, mit dem es weitergeht. Der Block
    rollt jetzt, mit Balken, der sich versteckt, solange nichts zu rollen
    ist; bei normaler Schrift bleibt alles, wie es war.

    **Nicht geprüft (2):** `szenen_buehne` war im Abzug leer, weil die
    Sichtprobe die Szene nicht weiterschaltet — `szene_schritt()` läuft in
    `renpy.say()` und wartet auf einen Klick, den niemand macht.
    `merkbuch_anzeige` **hängt**: Der Lauf blieb dort dreimal stehen, bei
    weicher wie bei harter Pause, mit voller Prozessorlast, während die
    übrigen 21 Bildschirme in Sekunden durchliefen. Die Figurendaten sind
    dabei vollständig (5 Figuren, alle vier Merkbuchfiguren mit Namen und
    Zustand) — es liegt also nicht an leeren Beständen. **Der Verdacht
    ist ein Bildschirm, der sich selbst neu anstößt**, und den sollte
    jemand vor der Schulstunde ansehen: Ein Bildschirm, der nie zur Ruhe
    kommt, kostet auf dem Schulrechner dauerhaft Rechenzeit.

    Beide stehen als offener Punkt in Abschnitt A.

---

## 5. September 2026 — Paket 8, Schritt 2.5 (Rhythmus)

102. **DIE NACHZIEHREGEL IST GEBAUT, GEMESSEN UND AUSGESCHALTET — SIE
    REISST DIE KORRIDORE AUS ENTSCHEIDUNG 11.** Vier Läufe, dieselbe
    Zufallssaat, 300 Durchgänge je Lage, zufällige Wahl / kluge Wahl:

    | Lage | Ausgang | nur Post | nur Einlagen | beides |
    |---|---|---|---|---|
    | Front kurz | 46,3/82,7 | 50,7/81,0 | 48,3/**70,3** | 42,3/**70,3** |
    | Front lang | 33,0/66,3 | 26,3/62,0 | 28,3/**59,7** | 23,0/**56,3** |
    | Etappe kurz | 56,3/82,7 | 50,0/**75,3** | 44,3/**65,3** | 38,0/**68,0** |
    | Etappe lang | 24,7/**46,0** | 20,0/**47,0** | **16,7**/**35,3** | **19,3**/**34,7** |
    | Heimat kurz | 46,7/87,3 | 40,3/84,7 | 39,0/**75,7** | 39,7/**70,7** |
    | Heimat lang | 23,3/66,3 | **17,7**/63,3 | 20,7/**57,0** | **14,7**/**59,3** |
    | **Beanstandungen** | **1** | **3** | **6** | **10** |

    **Die Einlagen sind die teure Hälfte.** Jede kostet Werte, und drei
    Einlagen mehr je Durchgang sind drei Wertänderungen mehr. Die Post ist
    billiger, reißt aber auch schon zwei Korridore.

    Entscheidung 11 sagt für genau diesen Fall: **„Wer dort landet, hält
    an und meldet, statt die Grenze weiter zu senken."** Ausgleichen darf
    ich es nicht — Entscheidung 13: Ab Paket 6, Schritt 1 fasst kein Paket
    mehr eine Zahl an. Also steht die Regel im Code, vollständig und
    gemessen, und `RHYTHMUS_NACHZIEHEN` steht auf `False`. Beide Hälften
    sind einzeln schaltbar.

103. **WAS DIE REGEL BRINGT, WENN MAN SIE EINSCHALTET.** Neu in Probe 2,
    Abschnitt a0: Kapitel ohne Einlage, ohne Brief und ohne beides, je
    Pfad und Verlauf, über 15 000 bis 17 000 abgeschlossene Kapitel.
    Gezählt werden nur Kapitel, die zu Ende gegangen sind — das Kapitel,
    in dem ein Durchgang abbricht, sagt nichts über den Rhythmus.

    | | ohne Einlage | ohne Brief | ohne beides |
    |---|---|---|---|
    | aus (heute) | 46,6 bis 69,2 % | 40,7 bis 55,5 % | 20,3 bis 40,4 % |
    | eingeschaltet | 37,1 bis 50,1 % | 32,5 bis 40,8 % | 11,1 bis 27,1 % |

    Die Regel wirkt also deutlich — sie halbiert die leeren Kapitel fast.
    Sie ist nur nicht umsonst.

104. **EINE NACHZIEHREGEL KANN NICHT HALTEN, WAS PUNKT 8 VERSPRICHT.**
    Der Auftrag verlangt „in jedem Kapitel mindestens eine Einlage und
    mindestens ein Brief" und nennt als Mittel eine Nachziehregel. Beides
    zusammen geht nicht: Eine Nachziehregel wirkt **rückwärts**. Sie kann
    ein leeres Kapitel nicht nachträglich füllen, sondern nur dafür
    sorgen, dass auf ein leeres kein zweites folgt. Ihre theoretische
    Untergrenze ist damit die Hälfte aller Kapitel; gemessen sind 37 bis
    50 Prozent, also besser als diese Schranke, aber niemals null.

    „In jedem Kapitel garantiert" verlangt eine **Vorziehregel**: beim
    letzten Zug eines Kapitels erzwingen, was fehlt. Die kostet im langen
    Verlauf sechs Einlagen je Durchgang — bei 90 Sekunden je Einlage neun
    Minuten Unterrichtszeit — und macht aus der Einlage genau die Station,
    die sie nach dem Entwurf in `minispiele.rpy` nicht sein soll: „ein
    Handgriff, der sich aus der Lage ergibt, und keine Station, die
    abgearbeitet wird."

    **Die Abnahme desselben Schrittes verlangt übrigens etwas anderes und
    Schwächeres** als Punkt 8: „kein Kapitel im langen Verlauf ohne
    Einlage **und** ohne Brief" — also keines, das weder das eine noch das
    andere hat. Das ist die dritte Spalte in a0, und sie steht
    eingeschaltet bei 11,1 bis 16,6 Prozent im langen Verlauf. Auch das
    ist nicht null.

105. **DIE ZAHLEN IM AUFTRAG SIND ÜBERHOLT** (Regel 9). Punkt 8 nennt
    `EINLAGE_CHANCE 45` — im Code stehen **30**. Er nennt „2,82 Einlagen
    und 2,27 Briefe auf sechs Kapitel" im langen Frontverlauf; gemessen
    sind heute 2,48 und 2,81 bei zufälliger Wahl. Vor allem aber ist der
    lange Verlauf seit Entscheidung 13 auf **dreizehn** Ziehungen gekürzt,
    nicht mehr achtzehn: Ein Kapitel hat nach `KAPITEL_ZIEHUNGEN` **zwei
    bis drei** Ziehungen im langen und **eine bis zwei** im kurzen
    Verlauf. Eine garantierte Einlage je Kapitel hieße damit, dass jede
    zweite bis dritte Ziehung eine Einlage ist.


---

## 6. September 2026 — Paket 8, vor Schritt 2.6

106. **PUNKT 101 WAR EIN FEHLER IM MESSAUFBAU, KEIN SPIELFEHLER — UND
    MEIN ERSTER VERDACHT WAR FALSCH.** Ich hatte vermutet, `welttext()`
    schreibe während der Auswertung des Bildschirms in die
    Store-Variablen `variantenersatz_gesamt` und `variantenersatz_stellen`
    (dialoge.rpy:207 und 232) und stoße damit die Interaktion endlos neu
    an. Am Ren'Py-Quellcode ist das **widerlegt**: `restart_interaction`
    wird an keiner Stelle von einem Schreibzugriff gesetzt, und ein
    Bildschirm wird je Interaktion ohnehin nur einmal ausgewertet
    (`screen.py:645`, geleert in `core.py:2417`). Der Rückfallzweig wird
    beim Merkbuch außerdem nie betreten: `MERKBUCH_LAGE`,
    `MERKBUCH_NAEHE_DA`, `MERKBUCH_NAEHE_FORT` und `MERKBUCH_GEGENSEITE`
    tragen zusammen **16 Wörterbücher, jedes mit allen drei Pfaden**, und
    auch die fünf Nebenfiguren haben front, etappe und heimat.

    Die wahre Ursache ist `modal True` (merkbuch.rpy:972) zusammen mit
    dem `renpy.pause(0.3, hard=True)` des Abzugsrezepts: Ein modaler
    Bildschirm setzt am TIMEEVENT `ev.modal = True` (`layout.py:619`,
    gerufen aus `screen.py:812`), `PauseBehavior` hält daraufhin an
    (`behavior.py:607`), weil `config.modal_blocks_pause` voreingestellt
    True ist (`config.py:1297`) — und setzt dabei `timeout(0)` immer
    wieder neu. Das ist die volle Prozessorlast. Der Gegenbeweis stand die
    ganze Zeit im eigenen Protokoll: `merkbuch_anlegen` ruft dieselben
    Funktionen, ist aber **nicht modal**, und lief nach AUFGEFALLEN 100
    unauffällig durch.

    **Behebung: ein Schlüsselwort im Abzugsrezept**, nicht eine Zeile
    Spielcode — `renpy.pause(0.3, hard=True, modal=False)`. Damit werden
    die vier modalen Bildschirme (`merkbuch_anzeige`, `merkbuch_briefe`,
    `merkbuch_lesen`, `confirm` in screens.rpy:1846) für die Sichtprobe
    zugänglich, die bisher 22 von 25 erfasst hat.

    **Die Lehre ist nicht der Befund, sondern das Verfahren:** Ich hätte
    den Verdacht ohne Gegenprüfung als Ursache gemeldet. Er klang
    schlüssig, er passte auf jede Beobachtung, und er war falsch. Ein
    Verdacht, der zu allen Beobachtungen passt, ist noch keine Ursache.

107. **DIE DATEIGRÖSSEN IN `CLAUDE.md` SIND ÜBERHOLT** (Regel 9). Der
    Abschnitt „Kontext sparen" nennt `figuren.rpy` mit 129 KB,
    `minispiele.rpy` mit 102 KB und `kapitel.rpy` mit 79 KB. Gemessen am
    6. September: **figuren.rpy 172 KB, minispiele.rpy 162 KB und
    kapitel.rpy 351 KB** — letztere ist damit die mit Abstand größte
    Datei des Projekts und im Text als kleinste genannt. Nicht geändert,
    weil `CLAUDE.md` Dominik gehört.

108. **ES GIBT KEINEN BESTAND VON „ORTEN", DEN `ORTSKLANG` ADRESSIEREN
    KÖNNTE.** Der Auftrag (Teil D, Punkt 12) verlangt „je Ort ein
    Umgebungsklang". Im Projekt gibt es dafür keine Kennung: kein `ORTE`,
    kein `schauplatz`, keine `kulisse`, kein Hintergrundbild je Ort. Es
    gibt die Dreiertafel `PFAD_ORT` (script.rpy:228) mit „Westfront",
    „Etappengebiet" und „Deutsches Kaiserreich" als Rückfall je Pfad, und
    ein **freies Textfeld** `ort` an drei Inhaltsklassen — Ereignis
    (script.rpy:433), Szene (dialoge.rpy:154) und Einlage. Freier Text
    taugt nicht als Schlüssel einer Tafel. Die Frage, worüber `ORTSKLANG`
    geschlüsselt wird, ist damit die erste, die Schritt 2.6 beantworten
    muss, und sie ist im Auftrag nicht beantwortet.

109. **DER DOCSTRING VON `Nebenfigur` VERSCHWEIGT DIE ETAPPE.**
    dialoge.rpy:121 beschreibt `namen` als `{"front": ..., "heimat": ...}`,
    obwohl alle fünf Figuren seit Paket 5 drei Pfade tragen. Wer sich
    darauf verlässt, sucht eine Lücke, die es nicht gibt. Nicht geändert,
    weil außerhalb des Auftrags (Regel 9).

110. **`auftrag/erkundung_26.md` IST NEU UND GEHÖRT NICHT ZUM AUFTRAG.**
    168 KB Erkundung mit Datei, Zeile und wörtlichem Zitat, entstanden
    vor der ersten Zeile Code von 2.6. Sie steht im Repository, weil der
    Chat abgebrochen wurde und diese Vorarbeit sonst verloren wäre. Sie
    ist eine Erkundung, **kein Auftrag** — sie ersetzt keine Entscheidung.

---

## 6. September 2026 — Paket 8, Schritt 2.6 (Tongerüst)

111. **ICH HABE EINE FREMDE DATEI VEREINNAHMT, UND DAS WAR FALSCH.**
    `audio/stummer_morgen.mp3` lag seit Beginn im Projekt und wurde von
    keiner Zeile gerufen. Auftragspunkt 15 verlangt eine Entscheidung.
    Ich habe ihren ID3-Kopf gelesen — Titel „Stummer Morgen", ein
    Interpret, `made with suno`, ein eingebettetes Titelbild, 4:03 Länge
    — und daraus geschlossen, sie sei Musik und gehöre in `STELLENMUSIK`,
    Stelle „hauptmenue". Der Befund war richtig, die Schlussfolgerung
    falsch: **Dominik hat gesagt, es sei eine Probedatei.**

    Der Fehler liegt in der Frage, die ich beantwortet habe. Ich habe
    geprüft, *was* die Datei ist, und daraus geschlossen, *dass* sie ins
    Spiel gehört. Die Zeile ist wieder heraus; die Datei wird jetzt nach
    dem zweiten Weg behandelt, den Auftragspunkt 15 ausdrücklich offen
    lässt — sie bleibt liegen und steht in `MEDIEN.md` als unbenutzt,
    genau wie die beiden Kartenbilder aus Punkt 83.

    Die Regel, die daraus folgt und die im Code und in `medienbedarf.py`
    steht: **Eine Tafelzeile darf eine Datei anfordern, die noch fehlt —
    das ist der Bedarfsplan. Sie darf eine vorhandene Datei nicht
    vereinnahmen.**

112. **DIE ERKUNDUNG HAT DIE ORTSANGABEN TRANSLITERIERT UND SICH VERZÄHLT**
    (Regel 9). `auftrag/erkundung_26.md` nennt „50 verschiedene
    Ortszeichenketten" und schreibt sie ohne Umlaute: *Landstrasse*,
    *Strasse*, *Rüstungsbetrieb* teils mit, teils ohne. Selbst gezählt
    sind es **51**, und sie tragen ß und Umlaute: `Straße`, `Landstraße`,
    `Feldbäckerei`, `Meldebehörde`, `Rüstungsbetrieb`, `Güterbahnhof`.
    Hätte ich die Liste abgeschrieben, hätte `ORT_KLANGRAUM` sechs Zeilen
    gehabt, die nie greifen — und niemand hätte es gehört. Eine Erkundung
    ist ein Hinweis, kein Beweis, auch die eigene von gestern.

113. **DIE ORTSANGABEN SIND NICHT NORMIERT, UND DAS BLEIBT SO.** Neben
    `Etappe`, `Etappenort` und `Etappengebiet` stehen vier Lazarette
    (`Lazarett`, `Etappenlazarett`, `Reservelazarett`,
    `Bahnhofslazarett`), zwei Quartiere und `Straße` neben
    `Landstraße`. Für den Klang ist das seit 2.6 folgenlos —
    `ORT_KLANGRAUM` bildet alle 54 auf zehn Klangräume ab, und ein
    unbekannter Text fällt über den Pfad zurück und wird gemeldet. Für
    die **Kopfzeile im Spiel** bleibt es uneinheitlich: Dort steht der
    Rohtext. Nicht geändert, weil Textarbeit an 121 Inhalten außerhalb
    dieses Auftrags liegt.

114. **ES GIBT KEINEN SCHALTER „TON GANZ AUS".** Der
    Einstellungsbildschirm hat zwei Regler, „Musik" und „Geräusche".
    Beide lassen sich auf null ziehen, aber nicht mit einem Klick
    stummschalten, und ein `persistent`-Feld für Ton gibt es nicht — das
    Projekt hat nur `persistent.analysemodus` und `persistent.bewegung`.
    Solange keine Tondatei im Projekt liegt, ist das folgenlos. Sobald
    eine liegt, ist es eine Frage des Klassenraums: Beamer, Lautsprecher,
    eine Doppelstunde neben anderen Räumen. **Das ist eine
    Unterrichtsfrage und gehört Dominik.**

115. **JEDE TAFELZEILE ERWARTET ZWEI DATEIEN, UND ES GENÜGT EINE.**
    `TON_ENDUNGEN` steht auf `["ogg", "mp3"]`, also führt die
    Medienprobe für 17 Tafelzeilen **34** erwartete Pfade — 10
    Klangräume und 7 Musikstellen, jeder zweimal. Das ist dieselbe
    Bauart wie bei den Schriften (`.ttf` und `.otf`, 8 Pfade für 4
    Schriften) und hat denselben Zweck: Eine beschaffte Datei muss nicht
    umgewandelt werden, nur weil die Tafel ein Format vorschreibt.
    **In `MEDIEN.md` sieht es nach doppelt so viel Arbeit aus, wie es
    ist.** Wer eine `.ogg` ablegt, braucht die `.mp3` nicht und
    umgekehrt; `ton_waehlen()` nimmt die erste, die da ist.

116. **DIE HARTE SPERRE WAR KEINE. SIE VERHINDERTE NUR DAS ANWERFEN.**
    Ein Gegenleser hat es gefunden, und es war der schlimmste Fund dieses
    Schritts, weil er genau die Zahl traf, die ich als Abnahme gemeldet
    hatte. `ton_spielen()` prüfte `aktueller_pfad` und verwarf den Aufruf —
    aber es beendete nie, was schon lief. **`label start` wirft Musik
    dreimal an** (Moduswahl, Onboarding, Jahreskarte), und dort steht
    `aktueller_pfad` noch auf der Vorgabe `"heimat"`; der Pfad fällt erst
    danach in `pfad_wechseln()`. Wer die von Entscheidung 24 zugesagte
    „eine Tabellenzeile und eine Datei" für `jahreskarte` eingelöst hätte,
    hätte Musik im Graben gehabt — **und Probe 11 hätte weiter „0 von 7
    freigegeben" gemeldet**, weil sie nur Freigaben zählte und eine
    laufende Spur nicht sehen konnte.

    Behoben mit drei Beinen, jedes im laufenden Spiel gemessen:
    `ton_spielen()` beendet beim Verwerfen; `pfad_wechseln()` ruft die
    Sperre, sobald der Pfad fällt; `musik_sperre_wacht()` hängt in
    `config.periodic_callbacks` und räumt auch das ab, was unter Umgehung
    aller Tonfunktionen angeworfen wurde. Probe 11 misst jetzt die
    Durchsetzung und nicht nur die Freigabe.

    Drei weitere Funde desselben Lesers, alle bestätigt und behoben:
    `on "show" action Function(musik_setzen, ...)` hätte das **Hauptmenü
    von allein starten lassen**, sobald dort zum ersten Mal Musik läuft
    (Ren'Pys `Function` beendet die Interaktion bei jedem Rückgabewert
    außer `None`); ein Wechsel in einen Klangraum ohne Datei ließ den
    **vorigen Ortsklang weiterlaufen**, statt still zu werden; und der
    selbst angemeldete Kanal `umgebung` stand in keiner der Listen, die
    Ren'Py beim Rücksprung ins Hauptmenü abräumt.

    **Die Lehre ist nicht der Befund, sondern die Zahl, die nichts sagte.**
    „Auf front und etappe null Musikaufrufe freigegeben" war wahr und
    zugleich wertlos: Sie maß den Vorgang, nicht den Zustand. Eine Regel,
    die „nie zu hören" verlangt, wird an dem gemessen, **was klingt**, nicht
    an dem, was angefordert wurde.

117. **ZWEI FEHLDIAGNOSEN IN EINER STUNDE, BEIDE AUS DEMSELBEN REFLEX.**
    Erstens: Der Messlauf stürzte mit `RecursionError` ab, und ich habe
    den Dauerrückruf verdächtigt — das Neueste im Bild — und ihn wieder
    ausgebaut. Er war es nicht: Der Absturz kam auch ohne ihn und steckt in
    `renpy.pause()` **unter dem Testrahmen** von `renpy.py … test`. Der
    Rückruf ist wieder drin und läuft sauber.
    Zweitens: „Der alte Ortsklang läuft weiter" war ein Messfehler. Ich
    hatte nach 1,2 Sekunden gemessen, und `TON_AUSBLENDEN` steht auf 1,5 —
    **ich habe in die Ausblendung hineingemessen.** Ein ausblendender Titel
    meldet sich weiter als spielend.

    Beide Male habe ich den Verdacht genommen, der am nächsten lag, statt
    ihn durch Weglassen zu prüfen. Beim ersten Mal hat mich genau dieses
    Weglassen dann widerlegt. **Das Verfahren ist der Fund: erst das
    Gegenexperiment, dann die Ursache.** Dasselbe steht schon in Punkt 106.

118. **`renpy.py … test` VERTRÄGT KEIN `renpy.pause()`.** Ein Testfall mit
    `renpy.pause(1.0, hard=True, modal=False)` bricht mit `RecursionError`
    ab, und die Rekursion entsteht im Fehlerbericht selbst
    (`renpy/test/testreporter.py` → `renpy/error.py`), sodass die
    eigentliche Ursache im `traceback.txt` gar nicht auftaucht. Der Weg aus
    offenem Punkt 62 funktioniert dagegen: ein temporäres
    `label splashscreen`, das misst, ein Ergebnis schreibt und
    `renpy.quit()` ruft — ohne Testsprache, mit dem normalen Spielstart.
    So ist die ganze Tonmessung dieses Schritts entstanden.

119. **PROBE 11 MISST MIT DER PROBEDATEI, DIE IM ORDNER LIEGT.** Der
    Abschnitt, der prüft, ob `musik_setzen()` und `ortsklang_setzen()`
    wirklich `None` zurückgeben, braucht eine abspielbare Datei — ohne sie
    geben beide ohnehin `None` zurück, und die Prüfung wäre eine grüne Null
    aus einer Nichtmessung. Die Probe sucht sich deshalb irgendeine Datei
    aus `audio/` und benutzt sie **nur zum Messen**; in keiner Tafel und in
    keiner Zeile MEDIEN.md steht sie. Heute ist das
    `audio/stummer_morgen.mp3`. **Wird sie gelöscht und liegt keine andere
    Tondatei da, meldet der Abschnitt `NICHTS GEMESSEN`** — richtig nach
    Regel 11, aber es ist gut, den Grund zu kennen.

120. **DAS GEGENLESEN IST UNVOLLSTÄNDIG GEBLIEBEN.** Geplant waren drei
    Blickwinkel — Ren'Py-Laufzeit, die elf harten Regeln, die Werkbank —,
    jeder Fund adversarisch geprüft. **Sechs von sieben Lesern sind an
    einem Sitzungslimit gescheitert.** Durchgekommen ist allein der
    Blickwinkel „die elf harten Regeln"; seine vier Funde habe ich selbst
    am Quelltext und am laufenden Spiel nachgeprüft, alle vier bestätigt
    und behoben. **Ungelesen geblieben sind die Blickwinkel Laufzeit und
    Werkbank.** Das leere Ergebnis des Laufs war kein Freispruch, sondern
    ein Ausfall — und es hätte als Freispruch durchgehen können.

121. **DER NACHTRAG ZUM GEGENLESEN — EIN FUND BELEGT, EINER WIDERLEGT,
    ACHT UNGEPRÜFT.** Die beiden fehlenden Blickwinkel sind
    nachgeholt worden. Wieder sind acht von zwölf Lesern am
    Sitzungslimit gescheitert, diesmal die **Prüfer**. Also: Ein Fund
    ist adversarisch belegt, einer widerlegt, der Rest ist eine
    Behauptung ohne Gegenprobe. **Nichts davon ist behoben** — das
    gehört in die nächste Sitzung.

    **BELEGT, mit Messung in einer Projektkopie** (`probe_alles.py`,
    Abschnitt 6 von Probe 11): Die Meldung „musik_sperre_durchsetzen()
    gibt es nicht" ist **unerreichbar**. Abschnitt 1 ruft
    `ton_spielen()` schon vorher, das ruft die fehlende Funktion, und
    `Namensraum.__missing__` trägt sie dabei als **Attrappe** in `NS`
    ein. Eine Attrappe ist `callable`, ihr Aufruf liefert eine
    Attrappe, und die ist wahr. Der Gegenleser hat die Funktion in
    einer Kopie umbenannt und gemessen: Die Probe meldet dann
    `heimat … ja` und „**FEHLER: Auf heimat wird Musik beendet, obwohl
    sie dort erlaubt ist**" — eine Beanstandung mit der **falschen
    Ursache am falschen Pfad**, während Abschnitt A weiter sagt „Keine
    Attrappe musste einspringen" (er wird vor den Proben gedruckt).
    Wer der Meldung folgt, sucht im Pfad `heimat` statt in der
    fehlenden Funktion.

    **WIDERLEGT:** `ortsangaben_sammeln()` sei blind für
    merkmalsgeschlüsselte Ortstexte. Gemessen: 101 `ort`-Felder sind
    Zeichenketten, 18 Wörterbücher tragen genau `front`/`etappe`/
    `heimat`, kein einziger Merkmalsschlüssel. 54 von 54 gesehen.

    **UNGEPRÜFT, in der Reihenfolge, in der ich sie ernst nehme:**
    (a) **`musik_setzen()` startet Musik, aber nichts beendet sie je.**
    `ton_spielen()` räumt den Musikkanal nur ab, wenn die Sperre
    greift; findet `ton_waehlen()` für die neue Stelle keine Datei,
    kehrt es mit `None` zurück und lässt die alte Spur laufen —
    `ortsklang_setzen()` hat seit Punkt 116 genau dafür eine Zeile,
    `musik_setzen()` nicht. Das einzige `ton_still("musik")` steht in
    `label start`; die vier harten Enden und `ende_lebenslauf` rufen
    nur `ton_still("umgebung")`. **Das ist derselbe Fehler wie Punkt
    116, nur auf dem anderen Kanal, und ich habe ihn beim Beheben
    übersehen.**
    (b) **`TON_AUSBLENDEN` wird beim normalen Wechsel nie benutzt.**
    `renpy.music.play()` ohne `fadeout=` nimmt `config.fadeout_audio`,
    gemessen **0,016 s** — der alte Klang bricht nach 16 ms ab, während
    der neue über 1,5 s einblendet. Der Kommentar darüber sagt das
    Gegenteil zu.
    (c) **Die Sperre fragt für `art="umgebung"` den Pfad gar nicht**,
    und beide Sperrbeine räumen nur den Kanal `music` ab. Wer eine
    Musikdatei in `ORTSKLANG` einträgt, hat sie an der Front.
    (d) Werkbank: zwei Tafelzeilen mit derselben Dateikennung; ein
    leeres `TON_ENDUNGEN`; Abschnitt 1 zählt nur Freigaben.

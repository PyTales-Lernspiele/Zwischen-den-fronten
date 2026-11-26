# Verfassung

Das Dauerhafte: Aufbau, Kopplungen, Bezeichner, Handwerk, Arbeitsweise.
Die **harten Regeln** stehen in `CLAUDE.md` und werden hier nicht
wiederholt. Den **Stand** nennt `STAND.md` — in dieser Datei stehen
absichtlich keine Messwerte, damit sie nicht veralten kann.

## Rolle

Du bist leitender Entwickler und historisch-didaktischer Autor. Das Spiel
läuft im Geschichtsunterricht, in einer Einzel- oder Doppelstunde, auf
Schulrechnern oder über den Beamer.

**Das Ziel:** Am Ende steht ein in sich geschlossenes Spiel. Jeder
Durchgang führt von der Musterung im August 1914 bis zum Lebenslauf nach
1919 — ohne Löcher im Bestand, ohne Sackgassen, mit einer Handlung, die
eine Schülerin danach nacherzählen kann. Die Bedienung ist ruhig und
lebendig zugleich: Karten legen sich auf den Tisch, Stempel setzen schräg
auf, geänderte Werte schweben sichtbar hoch. Nichts davon bewertet die
Entscheidung, alles davon macht sie spürbar.

## Aufbau

Dateien und ihre init-Ordnung. Die Ränge stehen in `bericht.txt`,
Abschnitt A, mit der vollständigen Ausführungsfolge Block für Block.

| Datei | init | Inhalt |
|---|---|---|
| `gui.rpy` | −50, −2 | Farben, Rahmen, Schriften, Bildersatz |
| `bewegung.rpy` | −45, 5 | Bewegungsstufen, `bewegungszeit()`, neun transforms, drei Übergänge |
| `ton.rpy` | −45 | Klangräume, `ORTSKLANG`, `STELLENMUSIK`, `ton_spielen()` mit der harten Musiksperre |
| `script.rpy` | −20, −10, −5, 0 | Werte, `Ereignis`/`Option`, `EREIGNISSE` |
| `dialoge.rpy` | −20, −10, −5, 0 | Szenen, `variante()`, Bühne |
| `kapitel.rpy` | −19, −9, 1, 2, 3 | Kapitel 1914–1919, `MERKMAL_REGISTER`, `KapitelEreignis`, Lebenslauf |
| `herkunft.rpy` | −19, −10, −4, 0, 1, 2 | Lebenslage, Musterung, Erwerb, Sprachprüfung |
| `figuren.rpy` | −8, 0, 1, 3, 4 | fünf Nebenfiguren, `BRIEFE`, `SCHICKSALE`, `briefwelt()` |
| `minispiele.rpy` | −6, 7, 8, 9 | die Einlagen |
| `merkbuch.rpy` | −7, 1, 2, 5, 6 | Merkbuch, Post-Umschlag |
| `screens.rpy` | ohne init | Stile und Bildschirme |

**Spätere init-Blöcke überschreiben frühere. Das ist gewollt und die
Arbeitsweise des Projekts:** nicht in fremden Dateien herumschneiden,
sondern in der eigenen Datei überschreiben. Beispiel: `MODUS_ZIELZAHL`
steht in `script.rpy` (init −20) auf 9/22 und wird von `kapitel.rpy`
(init −19) auf 12/30 überschrieben. Gültig ist 12/30.

Ablauf-Umleitungen laufen über `config.label_overrides`:

```
hauptschleife        -> hauptschleife_mit_post              (figuren.rpy)
kapitelwechsel       -> kapitelwechsel_mit_schicksal        (figuren.rpy)
lebenslage_abschluss -> lebenslage_abschluss_mit_merkbuch   (merkbuch.rpy)
post_zustellen       -> post_zustellen_als_ereignis         (merkbuch.rpy)
ereignis_spielen     -> ereignis_spielen_mit_einlage        (minispiele.rpy)
```

Wer eine Umleitung anlegt, prüft, ob dieselbe Marke schon umgeleitet wird.

## Kopplungen, die man leicht bricht

Sie stehen in keiner Probe. Eine grüne Probe beweist hier nichts.

- **`merkbuch.rpy` braucht sechs Stile aus `figuren.rpy`** —
  `brief_marke`, `brief_stempel`, `brief_absender`, `brief_zusatz`,
  `brief_kopf`, `brief_zeile` — und die Funktion `figur_verbundenheit()`.
  Wer `figuren.rpy` umbaut, sieht sich das Merkbuch danach von Hand an,
  auf allen vier Seiten und allen drei Pfaden.
- **Die Figurennamen kommen nicht aus `nach_welt()`**, sondern aus
  `figur_name()` in `dialoge.rpy` — und die fällt für die Etappe anders
  zurück als alles andere.
- **Eine neue Einlage braucht vier Einträge**, nicht drei: `EINLAGEN`,
  `EINLAGE_VORBEREITEN`, `EINLAGE_AUSWERTEN` **und**
  `EINLAGE_PROBEWERTE`. Fehlt der vierte, bricht die halbe Werkbank ab —
  und zwar so, dass Proben mit leerem Ergebnissatz weiterlaufen und auf
  grün stehen. Siehe Regel 11.
- **`EREIGNISSE` ist nicht der ganze Bestand.** Neben `EREIGNISSE` in
  `script.rpy` gibt es `EREIGNISSE_PAKET2` in `herkunft.rpy`,
  Abschnitt 6 — dort liegen die vier `einstieg_`-Ereignisse. Wer nur
  `script.rpy` durchsucht, findet sie nicht. Jede Zählung, jede Suche und
  jede Nachrüstung muss beide Bestände umfassen.

## Bezeichnerkarte

Benutzen statt neu erfinden.

| Bereich | Bezeichner |
|---|---|
| Textvarianten | `variante()`, `szenentext()` (dialoge), `welttext()` (figuren), `jahrestext()` (script), `gebeugt()` (herkunft), `nach_welt()` (merkbuch) |
| Werte | `zustand_lesen()`, `zustand_aendern()`, `wert_begrenzen()`, `stufe_von_wert()`, `schwaechster_wert()`, `ende_pruefen()` |
| Merkmale | `merkmal_setzen()`, `hat_merkmal()`, `MERKMAL_REGISTER`, `MERKMALS_REIHENFOLGE`, `MERKMAL_REIHENFOLGE_LEBENSWEG` |
| Ziehung | `ereignis_ziehen()`, `ereignis_passt()`, `ereignis_gewicht()`, `gewichtet_ziehen()`, `kette_faellig()`, `bestand_zaehlen()`, `bestandsbericht()`, `nachhallbericht()` |
| Kapitel | `KAPITEL_JAHRE`, `KAPITEL_ZIEHUNGEN`, `KAPITEL_WIRKUNG`, `KAPITEL_WIRKUNG_PFAD`, `KAPITEL_BOGEN`, `MODUS_ZIELZAHL`, `MODUS_UMFANG`, `MODUS_DAUER`, `EPILOG_JAHR` 1919, `KRIEGSJAHRE` |
| Pfade und Post | `PFAD_BASIS`, `POST_CHANCE`, `POST_ABSTAND`, `EINLAGE_CHANCE` |
| Bild und Schrift | `bild_pfad()`, `bild_vorhanden()`, `bild_anzeigen()`, `bild_platzhalter()`, `portrait_anzeigen()`, `schrift_waehlen()`, `BILD_MASSE`, `BILD_ANZEIGE` |
| Rahmen | `rahmen()`, `rahmen_leer()`, `rahmen_doppelt()`, `rahmen_oben()`, `rahmen_schatten()`, `rahmen_doppelt_schatten()` |
| Farben | `FARBE_PAPIER`, `_HELL`, `_DUNKEL`, `FARBE_TINTE`, `_MATT`, `FARBE_LINIE`, `_FEIN`, `FARBE_AKZENT` (#8a3324), `_MATT`, `FARBE_DUNKEL`, `FARBE_BLUT`, `FARBE_FEHLEND`, `FARBEN_STUFE` |
| Schriften | `SCHRIFT_FLIESS`, `SCHRIFT_TITEL`, `SCHRIFT_DOKUMENT` |
| Bewegung | `bewegungszeit()`, `bewegungsstufe()`, `bewegung_waehlen()`, `BEWEGUNG_STUFEN`, `BEWEGUNG_ANTEIL`, `UEBERGANG_KARTE()`, `UEBERGANG_KAPITEL()`, `UEBERGANG_ENDE()` — dazu die neun transforms `karte_kommt`, `karte_geht`, `stempel_setzt`, `wert_schwebt`, `strich_waechst`, `kalenderblatt`, `umschlag_oeffnet`, `zeile_taucht_auf`, `knopf_hebt` |
| Ton | `ton_pfad()`, `ton_kandidaten()`, `ton_waehlen()`, `ton_spielen()`, `ton_still()`, `ort_klangraum()`, `ortsklang_setzen()`, `musik_setzen()`, `KLANGRAEUME`, `KLANGRAUM_ZWECK`, `ORTSKLANG`, `ORT_KLANGRAUM`, `PFAD_KLANGRAUM`, `STELLENMUSIK`, `MUSIK_GESPERRT`, `MUSIK_EINGESCHALTET`, `MUSIK_VERWORFEN`, `ORT_OHNE_KLANGRAUM`, `TON_KANAL`, `TON_ENDUNGEN` |

**Die vier Werte** (0 bis 12): `versorgung` (Hunger), `belastung`
(Erschöpfung), `aufmerksamkeit` (Verdacht), `rueckhalt` (Einsamkeit).
`WERT_HOCH_IST_GUT`: `versorgung` und `rueckhalt` True, die anderen
beiden False.
`ENDE_SCHWELLEN`: `versorgung_unter` 1, `belastung_ab` 12,
`aufmerksamkeit_ab` 11.

**Klassen:**

```
Ereignis(kennung, jahre, pfad, text, optionen, kern, gewicht, braucht,
         verbietet, ort, quelle, stimmung, nur_kette, wiederholbar)
  in kapitel.rpy erweitert zu KapitelEreignis mit braucht_eines,
  gewicht_bonus, knuepft_an

Option(titel, beschreibung, ausgang, hinweis, aenderungen, merkmale,
       varianten, sprung, bild, stimmung, kette, kette_ab)

Einlage(kennung, titel, bildschirm, jahre, pfad, ort, einleitung,
        anweisung, einordnung, anschluss, braucht, verbietet, gewicht,
        merkmal, wiederholbar, quelle)
```

## Handwerksregeln für jeden neuen Text

- **a)** Ein Moment, keine Zusammenfassung. Zeigen statt berichten.
- **b)** `Ereignis.text`: 3 bis 5 Sätze. Der erste verortet den Körper,
  der letzte schärft die Lage.
- **c)** Mindestens eine Sinneswahrnehmung je Ereignis: Geruch, Geräusch,
  Kälte, Gewicht, Geschmack.
- **d)** Mindestens jedes dritte Ereignis enthält wörtliche Rede einer
  namenlosen Figur.
- **e)** `Option.titel`: 2 bis 4 Wörter, ein Verb, keine Wertung.
  `Option.beschreibung`: 1 Satz. `Option.ausgang`: 2 bis 3 Sätze,
  mindestens einer körperlich, wertfrei.
- **f)** `jahrestext`: Die Fassungen für verschiedene Jahre unterscheiden
  sich substanziell, nicht um ein Wort.
- **g) Keine Einbahnstraße.** Keine Karte, bei der beide Optionen
  denselben Wert verschlechtern, ohne dass eine davon das an anderer
  Stelle ausgleicht. Wer nur verlieren kann, entscheidet nicht mehr.
- **h) Keine dominierte Option.** Keine Option, die in allen vier Werten
  gleich gut oder besser ist als die andere und das nirgends bezahlt —
  kein Merkmal, keine Kette, kein Sprung, kein Hinweis gleicht es aus.
  Die Einbahnstraßenprüfung findet das **nicht**; sie sucht nur Karten,
  bei denen beide Optionen denselben Wert senken. Deshalb sind es zwei
  Prüfungen. Beide liegen in `probe_alles.py`, und jedes neue Ereignis
  läuft dagegen, bevor du es meldest.

## Sprachmaß Klasse 8 Oberschule (nachprüfbar)

- Durchschnittliche Satzlänge höchstens 13 Wörter. **Kein Satz länger als
  20 Wörter.**
- Höchstens ein Nebensatz je Satz. Keine Schachtelsätze.
- Keine Substantivketten aus mehr als zwei Wörtern.
- Jedes Fremdwort und jeder historische Fachbegriff wird beim ersten
  Auftreten im selben Satz erklärt. Danach steht er im Glossar.
- Anrede durchgehend „du".
- Aktiv statt Passiv, wo es geht. Amtsdeutsch nur dort, wo ein Amt
  spricht — und dann mit einem erklärenden Satz daneben.
- **Die Einordnung einer Quelle sind genau zwei Sätze:** was die Quelle
  zeigt und was sie nicht zeigt. Jeder unter 20 Wörtern, zusammen
  höchstens 35. Das reicht — „Das Foto entstand 1917 in einer Berliner
  Kriegsküche. Es zeigt die Ausgabe, nicht die Menschen, die leer
  ausgingen." sind 18 Wörter. Was nicht hineinpasst, ist nicht
  überflüssig; es gehört in das Feld `vertiefung` und von dort ins
  Glossar. Siehe Entscheidung 9.

## Animationsregeln

- Bewegung nur mit Ren'Py-Bordmitteln (ATL, Transform, Transitions).
  Keine Bilddateien, keine Fremdbibliotheken.
- Jede Bewegung hat einen Grund aus der Sache: Papier legt sich, ein
  Stempel setzt auf, Tinte trocknet, ein Umschlag geht auf.
- **Drei Klassen von Dauer** (Entscheidung 17). Die Grenze richtet sich
  danach, was die Bewegung der Spielerin schuldet:

  | Klasse | Grenze | Was dazugehört |
  |---|---|---|
  | Handgriff | 0,45 s | Alles, was zwischen ihr und dem nächsten Klick liegt: Karten, Stempel, Striche, Knöpfe. Die Grenze schützt die Hand. |
  | Kapitelwechsel | 0,8 s | Der Jahreswechsel und der Weg in den Lebenslauf. Danach wird ohnehin gelesen. |
  | Rückmeldung | 1,2 s | Was nur gesehen werden will und nichts aufhält — der schwebende Wert. Gesehen werden dauert länger als angeklickt werden. |

  Nichts wackelt dauerhaft, nichts blinkt, nichts pulsiert im
  Hintergrund. Die drei Zahlen stehen in `bewegung.rpy`, damit Probe 9
  sie messen kann statt sie ein zweites Mal zu formulieren.
- Keine Bewegung bewertet eine Entscheidung. Kein Aufleuchten bei
  „richtig", kein Zittern bei „falsch".
- Jede Bewegung ist abschaltbar. Seit Paket 7, Schritt 1 heißt der
  Schalter `persistent.bewegung` mit den drei Stufen `voll`, `sparsam`
  und `aus`; jede Dauer im Projekt kommt aus `bewegungszeit()`. Der
  frühere Arbeitsname `BEWEGUNG_STAERKE` ist nie entstanden.
- Ein Klick unterbricht jede laufende Bewegung sofort und zeigt den
  Endzustand. Niemand wartet auf eine Animation.
- **Keine Sekundenzahl steht in einem Bildschirm.** Ein transform mit
  Parameter `dauer` wird immer mit Klammern und mit `bewegungszeit()`
  aufgerufen — `at karte_kommt` ohne Klammern nimmt die Vorgabe aus der
  Datei und hört auf keinen Schalter. Probe 9 sucht genau danach.

## Ausgabeformat

- Vollständige, einsetzbare Blöcke. Keine Auslassungszeichen, kein
  „… hier unverändert …", keine Pseudo-Diffs.
- Bei Änderungen an bestehenden Dateien: den kompletten betroffenen
  Abschnitt ausgeben und darüberschreiben, ab welcher Zeile oder nach
  welchem Kommentar er einzusetzen ist.
- Kommentare auf Deutsch, im Stil der vorhandenen Dateien:
  Blockkommentare mit `##` und einer **erklärten Absicht**, nicht nur
  einer Beschreibung.

## Arbeitsweise

1. Lies zuerst die betroffenen Dateien und die passenden Abschnitte in
   `bericht.txt`. Ändere nichts, bevor du den Ist-Zustand kennst.
2. **Ein Commit je Schritt** ist die Sicherung. Bei sehr langen Schritten
   ein Commit je Gruppe.
3. Arbeite die Schritte eines Pakets der Reihe nach ab. Fang keinen
   neuen an, bevor der vorige seine Abnahme bestanden hat.
4. Nach jedem Schritt: `probe_alles.py --schnell`, dann eine Kurzmeldung
   in höchstens fünf Zeilen — was geändert wurde, welche Probe sich wie
   bewegt hat, ob die Abnahme erfüllt ist.
5. Scheitert eine Abnahme, hältst du an und meldest es. Du gehst nicht
   weiter, und du reparierst nichts stillschweigend aus einem früheren
   Schritt.
6. Wird ein Schritt sehr lang — viele neue Ereignisse zum Beispiel —,
   teilst du ihn selbst in **Gruppen zu sechst** und meldest nach jeder
   Gruppe. Wer zwölf Ereignisse am Stück schreibt, wird beim zwölften
   nachlässig, und man sieht es dem Text an.
7. Am Ende des Pakets: der vollständige Lauf ohne `--schnell`, dazu
   `--vergleich bericht_ausgang.txt`.
8. Starte das Spiel einmal und sieh in `errors.txt` nach.
9. **Lässt du eine Nebenaufgabe oder einen Arbeitsablauf etwas
   schreiben** — Ereignistexte, eine Tafel, eine Liste —, dann schreibt
   dieser Ablauf sein Ergebnis **selbst in die Datei**, bevor er dir
   Bericht erstattet. Nichts Erarbeitetes lebt nur in einer Antwort. Am
   3. September sind so 18 fertige Etappenereignisse verloren gegangen,
   weil der Ablauf nach der Nutzungsgrenze fertig wurde.

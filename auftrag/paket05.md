<!-- Erzeugt aus bau/. Nicht von Hand ändern - die Änderung
     wäre beim nächsten Bauen weg. Melde stattdessen unter AUFGEFALLEN. -->

# Paket 5 - ETAPPE, EPILOG 1919 UND DIE EICHUNG

> **Vor diesem Paket gelesen:** `STAND.md`, `git log --oneline -10`,
> `auftrag/VERFASSUNG.md`, `auftrag/ENTSCHEIDUNGEN.md`.
> **Nach jedem Schritt:** Commit, `probe_alles.py --schnell`, Kurzmeldung,
> `STAND.md` und `auftrag/OFFENE_PUNKTE.md` nachziehen.

## Überblick

```text
Die beiden letzten Bestandslücken - und danach die Eichung.
Die Schritte 1 und 2 sind erledigt (siehe STAND.md). Die Etappe
ist gefüllt, geöffnet und hat eine eigene Sprache; 1919 hat acht
Ereignisse, eine eigene Einlage und die Wirtshausszene, auf die das ganze
Spiel zuläuft. Der Bestand ist damit vollständig - vier Proben stehen
auf null.
Was Schritt 2 gebaut hat und worauf Schritt 3 aufsetzt: 1919 und
die Wirtshausszene, auf die das ganze Spiel zuläuft. Sie gehören
zusammen, weil die Etappe auch 1919 braucht und weil die Wirtshausszene
für alle drei Pfade zugleich geschrieben werden will.
Schritt 3 ist ein reiner Zahlendurchgang und der Grund, warum er hier
steht und nicht früher: Mit ihm ist der Bestand vollständig - alle sechs
Jahre, alle drei Pfade, alle Einlagen, alle Briefe. Die Grenzen aus
Paket 2, Schritt 3 waren an einem Bestand geeicht, in dem 1917 bis 1919 leer waren;
sie mussten reißen, sobald Inhalt dazukam. Jetzt wird einmal richtig
geeicht, gegen etwas, das sich nicht mehr ändert.
Für die Schritte 1 und 2 gilt wieder: Ereignisse in Gruppen zu sechst,
Meldung nach jeder Gruppe.
```

## Die Schritte

1. DIE ETAPPE FÜLLEN UND WIEDER ÖFFNEN — **erledigt**
2. EPILOG 1919 UND DIE WIRTSHAUSSZENE — **erledigt**
3. WERTEHAUSHALT AM VOLLEN BESTAND — **erledigt**

Jeder Schritt hat seine eigene Abnahme. Die Gesamtabnahme steht unten.

---

## Schritt 1 von 3 - DIE ETAPPE FÜLLEN UND WIEDER ÖFFNEN

> **Erledigt und abgenommen am 4. September 2026.** Lies diesen Schritt als
> Bericht, nicht als Auftrag — die späteren Schritte verweisen
> auf ihn. Schreib nichts davon neu. Was er gebracht hat, steht
> in `STAND.md`.

```text
BEFUND
Die Etappe ist seit Paket 2, Schritt 1 geschlossen. Der Grund, in Zahlen: 1914 ein
freies Ereignis bei Soll 2 bzw. 5, 1915 drei, 1916 vier, 1917 und 1918
keines, 1919 keines. Dazu 126220 Griffe in die Rückfallebene an 43
Stellen, ausnahmslos etappe -> front. Die Etappe hatte nie eine eigene
Stimme; sie hat die der Front geliehen.

VORSICHT MIT figuren.rpy
Dieses Paket fasst figuren.rpy an mehreren Stellen an. Daran hängt das
Merkbuch: es benutzt die Stile brief_marke, brief_stempel, brief_absender,
brief_zusatz, brief_kopf, brief_zeile und die Funktion
figur_verbundenheit(). Keine Probe merkt es, wenn du eine davon
umbenennst oder umbaust. Sieh dir das Merkbuch nach diesem Schritt von
Hand an, auf allen vier Seiten und auf allen drei Pfaden.

Das ist inhaltlich die größte Lücke des Spiels. Zwischen Front und
Heimat lag ein drittes Land: Nachschub, Lazarettzüge, Verpflegungsausgabe,
Listen, Zensurstelle, Gefangenenlager. Wer dort war, galt an der Front als
"Etappenschwein" und in der Heimat als Gedrückter - und war beides nicht.
Dieses Spannungsfeld trägt das Paket.

AUFGABE

TEIL A - INHALT
1. 12 neue Etappen-Ereignisse über die Jahre 1914 bis 1918. Themen:
   Lazarettzug, Verpflegungsausgabe, Fronturlauber auf dem Bahnsteig,
   Listen und Meldungen, Kriegsgefangene bei der Arbeit, Zensurstelle,
   Requisition im besetzten Gebiet, Bahnhofskommandantur.
   Mindestens 4 mit kern=True, jedes mit quelle-Dict, mehrere mit
   mehrjähriger jahre-Liste.
2. Prüfe zusätzlich alle bestehenden Ereignisse mit "etappe" in der
   Pfadliste: Reichen ihre Jahre? Trage nach, wo es sachlich stimmt.
3. Das Spannungsfeld bekommt eigene Ereignisse: einmal aus der Sicht eines
   Fronturlaubers, der einen ansieht, und einmal aus der Sicht eines
   Briefes aus der Heimat, der fragt, warum man nicht kommt.
3a. ZWANGSARBEIT UND GEFANGENE. Die Etappe ist der Ort, an dem das im
   Spiel sichtbar werden kann, und im Lehrplan der 8. Klasse gehört es
   zum industriellen Krieg dazu: Kriegsgefangene bei der Arbeit,
   Zivilarbeiter aus dem besetzten Gebiet, die Deportationen aus Belgien
   im Winter 1916/17. Schreib mindestens zwei Ereignisse dazu.
   Die Regel dabei: Die Spielerin ist nicht die Leidtragende, sie ist die,
   die daneben steht und etwas tut oder nicht tut. Kein Elendsbild, keine
   Gore-Beschreibung, kein Erzähler, der einordnet. Ein Vorgang, ein
   Blick, eine Entscheidung. Beide Ereignisse brauchen ein besonders
   sorgfältiges quelle-Dict.

TEIL B - DIE EIGENE STIMME
4. Trage alle fehlenden Etappen-Textvarianten nach.
   DER UMFANG IST GRÖSSER, ALS DIE ALTE ZAHL SAGT. Die 43 Stellen aus
   Probe 2c waren die AUFRUFE. Die Vorarbeit hat gezählt, was dahinter
   liegt: 125 Variantenwörterbücher ohne Etappenfassung. Plane danach,
   arbeite in Gruppen, committe nach jeder Gruppe - sonst endet die
   Sitzung mitten darin.
   ZÜRST DIE VIER RÜCKFALLZWEIGE VEREINHEITLICHEN. Im ganzen Projekt
   gibt es genau vier Stellen, die pfadweise zurückfallen, und sie fallen
   in drei verschiedene Richtungen:
     dialoge.rpy:265  variante()          -> front (die Notlösung)
     dialoge.rpy:298  figur_name()        -> heimat
     dialoge.rpy:304  figur_zusatz()      -> heimat
     figuren.rpy:400  zustand_anzeige()   -> heimat
     merkbuch.rpy:97  nach_welt()         -> front, und zwar STILL
   nach_welt() ist der gefährlichste Fall: Es baut das Wörterbuch und
   setzt bei etappe=None die Frontfassung als Wert ein. Weil der
   Schlüssel "etappe" dann existiert, meldet variante() nichts - dieser
   Ersatz wird von keiner Zahl gezeigt. Von elf Aufrufen tragen nur sieben
   ein echtes etappe=.
   Stelle figur_name(), figur_zusatz() und zustand_anzeige() auf
   variante() beziehungsweise welttext() um. Danach gibt es eine Regel
   statt drei, und jede Lücke wird gezählt statt ersetzt.
   Erst danach die eigentliche Nacharbeit, die größten Posten zuerst.
   Die alte Liste aus Probe 2c bleibt der Wegweiser: Arbeite sie ab, die
   größten zuerst:
     figuren.rpy:1843  schicksale_wuerfeln
     figuren.rpy:1723/1724/1725/1743  stufe_anwenden
     figuren.rpy:1799  entfremdung_pruefen
     figuren.rpy:1905  brief_aus_nachricht
     minispiele.rpy:542  einlage_text
     minispiele.rpy:616/620/621  portionen_vorbereiten
     minispiele.rpy:847/858/872/880/889  portionen_auswerten
     dialoge.rpy:179  szenentext, elf Szenen (prolog_ankunft,
       prolog_ordnung, prolog_kind, feldpost_1915_regeln,
       feldpost_1915_schweigen, alltag_1915_gegenseite,
       wendepunkt_1916_zaehlen, wendepunkt_1916_amt,
       wendepunkt_1916_bruch, abschluss_kind, abschluss_gegenseite,
       abschluss_bilanz) - jeweils Text und Ort.
   Die Etappenfassung ist nie die Frontfassung mit anderen Wörtern. Sie
   hat andere Geräusche (Rangierbahnhof statt Einschlag), andere Gerüche
   (Karbol und Kohle statt Erde) und ein anderes Verhältnis zur Gefahr.
5. UNEINHEITLICHE RÜCKFALLRICHTUNG - beim Wiederherstellen von
   merkbuch.rpy aufgefallen: figur_name() in dialoge.rpy fällt für die
   Etappe auf die HEIMATfassung zurück, während alle anderen
   Rückfallebenen auf die FRONTfassung fallen. Im Merkbuch stehen diese
   Namen groß auf jeder der vier Seiten, dort fällt es zuerst auf.
   Gib der Etappe eigene Namen und weise nach, dass danach keine Stelle
   mehr in zwei verschiedene Richtungen zurückfällt. Suche dafür im
   ganzen Projekt nach Rückfallzweigen, nicht nur in dialoge.rpy.
6. briefwelt() (figuren.rpy) liefert künftig auch "etappe". Briefe und
   Schicksale dafür absichern: Jeder Brief und jede Schicksalsmeldung
   braucht eine Fassung für die Etappenwelt oder eine begründete
   Zuordnung zu einer der beiden anderen.
7. Die Notlösung in variante() (dialoge.rpy:265, "Notlösung bis
   Paket 5b.2", etappe -> front) wird restlos gestrichen. Fehlende
   Varianten sind ab jetzt echte Fehler, keine stillen Ersetzungen.
   ZUSAMMEN MIT nach_welt() IN merkbuch.rpy:97. Beide gehören zu einer
   Sache. Streichst du nur die eine, bleibt ein Ersatz übrig, den keine
   Zahl zeigt - und die Probe meldet trotzdem null. Das wäre schlechter
   als der heutige Zustand, weil es dann auch niemand mehr sucht.

TEIL C - WIEDER ÖFFNEN
7. ETAPPE_FREIGESCHALTET in herkunft.rpy auf True setzen, Kommentar
   darüber neu schreiben: seit wann offen, womit gefüllt.
8. Prüfe den Weg dorthin: pfad_aus_musterung() bei "gv",
   erwerb_holen(...).etappe_moeglich, einstieg_etappe.
9. lazarett UND DIE ZWEI WEGE IN DIE ETAPPE - BERICHTIGT.
   Die Vorarbeit hat gezeigt, dass meine ursprüngliche Annahme falsch
   war: etappe_moeglich ist ausschließlich beim Erwerb lazarett gesetzt
   (herkunft.rpy:975-984), und dieser Erwerb vergibt das gleichnamige
   Merkmal. Wer über einstieg_etappe in die Etappe kommt, HAT lazarett
   bereits.
   Die Lücke liegt beim ZWEITEN Weg: der Musterung mit g.v. Wer so in die
   Etappe kommt, ist Soldat und hat kein lazarett. Für ihn greift
   lazarett_1918_grippestation nicht.
   Entscheide begründet, ob das so bleiben soll - ein g.v. gemusterter
   Nachschubsoldat ist keine Lazarettkraft, das wäre vertretbar - oder ob
   ein Etappenereignis das Merkmal auch auf diesem Weg vergeben darf.
   Was du in jedem Fall tust: den Sachverhalt als Kommentar bei
   etappe_moeglich festhalten, damit die nächste Suche nicht wieder bei
   null anfängt.
10. einstieg_etappe IST NICHT ENTFERNT, SONDERN GESPERRT
   (herkunft.rpy:2244). Es muss also nichts wiederhergestellt werden - der
   Aufruf fällt mit dem Schalter aus Punkt 8 von selbst zurück. Prüfe
   nur nach der Freischaltung über 2000 Etappendurchgänge, dass es
   tatsächlich wieder gezogen wird, und entferne den Wartekommentar.

ABNAHME DIESES SCHRITTS
  - Bestandstafel: alle Etappenzeilen 1914 bis 1918, beide Verläufe,
    Lage "in Ordnung". (1919 kommt in Schritt 2 dieses Pakets.)
  - Sackgassenprobe Etappe: 0,0 % Leerabbrüche in allen Jahren.
  - Probe 2c: 0 Griffe in die Rückfallebene über 2000 Etappendurchgänge
    in beiden Verläufen. Das ist das harte Kriterium dieses Pakets.
  - Probe 2b: kein Brief in falscher Welt.
  - Probe 4: gemessen und genannt. Geeicht wird in Schritt 3 dieses
    Pakets, nicht hier.

PRÜFEN MIT: probe_alles.py, besonders Probe 2c und die Sackgassenprobe.
```

---

## Schritt 2 von 3 - EPILOG 1919 UND DIE WIRTSHAUSSZENE

> **Erledigt und abgenommen am 4. September 2026.** Lies diesen Schritt als
> Bericht, nicht als Auftrag — die späteren Schritte verweisen
> auf ihn. Schreib nichts davon neu. Was er gebracht hat, steht
> in `STAND.md`.

```text
BEFUND
1919 hat auf keinem Pfad ein Ereignis und auf keinem Pfad eine Einlage.
Soll ist kurz 1, lang 2 je Pfad, dazu eine Einlage je Kapitel. Die
Sackgassenprobe meldet für 1919 durchgängig 100 Prozent Leerabbrüche.
Das Jahr, in dem das Spiel seine Auswertung leisten soll, ist leer.

AUFGABE

TEIL A - ACHT EREIGNISSE FÜR 1919
Themen: Heimkehr und das Haus, das anders geworden ist; Versehrte und die
Frage der Rente; Entlassung der Frauen aus den Werken; die Wahl vom
19. Januar 1919 (erstes Frauenwahlrecht); die fortdauernde Seeblockade und
der Hunger nach dem Waffenstillstand; die Nachricht von den Bedingungen
des Vertrags im Frühjahr.
  - Verteile so, dass jeder Pfad mindestens drei ziehbare Ereignisse hat.
  - KEINE harten Spielabbrüche mehr in 1919. Wer den November 1918
    überstanden hat, erreicht den Lebenslauf. Setze das technisch durch,
    nicht nur inhaltlich, und belege es.
  - Jedes Ereignis mit quelle-Dict.

SCHON DA: EIN TEXT, DER IN 1919 ANKOMMT
heimat_verfahren hat seit Paket 2, Schritt 2 eine Fassung für 1919 - der einzige
Spieltext des Projekts nach dem 11. November. Er entstand, damit die Kette
der Einlage hamsterfahrt überhaupt auflösbar wird. Lies ihn, bevor du
die acht neuen Ereignisse schreibst: Er gibt den Ton vor, in dem 1919
klingt, und du solltest nicht daneben schreiben.

TEIL B - MINDESTENS EINE EINLAGE FÜR 1919
Bisher gibt es für 1919 auf keinem Pfad eine. Baue eine neue Einlage, die
zum Jahr passt und mit den vorhandenen Bordmitteln auskommt - zum Beispiel
das Ausfüllen eines Antrags beim Versorgungsamt, bei dem man entscheidet,
was man angibt und was man weglässt. Format wie die vier bestehenden
Einlagen, mit einordnung aus genau zwei Sätzen und quelle-Dict.

TEIL C - DIE WIRTSHAUSSZENE
Pflichtszene für JEDEN Durchgang, unmittelbar vor dem Lebenslauf.
  Ort und Zeit: Wirtshaustisch, Frühjahr 1919.
  Lage: Ein Fremder am Tisch behauptet, das Heer sei im Felde unbesiegt
  geblieben; schuld seien die in der Heimat gewesen.
  Drei Optionen: Widersprechen. Schweigen. Zustimmen.
Bauregeln:
  - Die Reaktionen der anderen am Tisch variieren nach aktueller_pfad und
    nach den gesammelten Merkmalen. Wer an der Front war, wird anders
    angesehen als wer in der Fabrik war. Wer aktenkundig ist, überlegt
    länger.
  - Das Spiel belehrt nicht. Es gibt keinen Erzähler, der die Behauptung
    richtigstellt, und keine Option, die sichtbar belohnt wird. Der
    Widerspruch entsteht im Kopf der Spielerin, weil sie selbst gesehen
    hat, was in den Jahren davor geschehen ist.
  - Die Wahl setzt ein Merkmal (wirtshaus_widersprochen,
    wirtshaus_geschwiegen, wirtshaus_zugestimmt) mit Eintrag in
    MERKMAL_REGISTER und einem Nachklang im Lebenslauf.
  - Die Szene läuft über das Szenensystem aus dialoge.rpy, mit
    variante() für die Fassungen. Kein neuer Mechanismus.
  - Länge: 12 bis 18 Zeilen bis zur Wahl, danach je Option 4 bis 6.

TEIL C2 - DIE POST VON 1919
Zwei Briefe, e_amt_suche und e_amt_entlassung, waren in der Messung nach
Paket 2, Schritt 3 kein einziges Mal erlaubt. Der Grund ist mechanisch: 1919 wird
kein Ereignis gezogen, und Post kommt nur nach einem Ereignis. Mit den
acht Ereignissen aus Teil A fällt der erste Teil weg.
  - Weise nach, dass beide Briefe jetzt zugestellt werden, und nenne die
    Häufigkeit je 2000 Durchgängen.
  - Prüfe zugleich POST_CHANCE für 1919 (heute 30). Reicht das, damit
    die beiden Amtsbriefe verlässlich ankommen, oder braucht der Epilog
    eine eigene Regel?
  - Die drei anderen Briefe aus der Liste (h_kundige_haft,
    f_naechste_gefangen, f_kundige_haft) hängen an der Post von 1917.
    Prüfe sie hier mit und schließe den Punkt aus Paket 3, Schritt 2 ab.

TEIL D - ÜBERGANG UND NACHKLÄNGE
  - Übergangskarte vom letzten Ereignis 1919 zur Wirtshausszene und von
    dort zum Lebenslauf.
  - Alle Nachklänge 1920 bis 1924 aus MERKMAL_REGISTER müssen im
    Lebenslauf-Bildschirm erreichbar sein. Prüfe, ob es Nachklänge gibt,
    die kein Weg jemals zeigt, und melde sie.

ABNAHME DIESES SCHRITTS
  - Bestandstafel 1919: alle drei Pfade, beide Verläufe, Ereignisse und
    Einlagen ohne FEHLT.
  - Sackgassenprobe 1919: 0,0 % Leerabbrüche.
  - Über 2000 Durchgänge je Lage: jeder Durchgang, der 1919 erreicht,
    sieht die Wirtshausszene. Zahl nennen.
  - Kein harter Abbruch im Jahr 1919.
  - Die drei Wirtshaus-Merkmale erscheinen im Lebenslauf.

PRÜFEN MIT: probe_alles.py, dazu je ein Durchgang von Hand mit jeder der
drei Wirtshaus-Optionen.
```

---

## Schritt 3 von 3 - WERTEHAUSHALT AM VOLLEN BESTAND

> **Erledigt und abgenommen am 4. September 2026.** Lies diesen Schritt als
> Bericht, nicht als Auftrag — die späteren Schritte verweisen
> auf ihn. Schreib nichts davon neu. Was er gebracht hat, steht
> in `STAND.md`.

```text
WARUM ERST JETZT
Paket 2, Schritt 3 hat den Wertehaushalt an einem Bestand geeicht, in dem
1917 bis 1919 leer waren. Vier von fünf Kapiteln endeten dort sofort,
ohne eine einzige Ziehung und fast ohne Kosten. Diese Grenzen waren von
Anfang an eine Zwischenmessung, keine Wahrheit.
Das hat sich beim Füllen von 1917 gezeigt: Die Zahl der Inhalte je kurzem
Durchgang stieg von 6,66 auf 9,17, und die Überlebensquote fiel an der
Front von 47,4 auf 22,5 Prozent. Eine Versuchsreihe hat belegt, dass der
Hebel nicht bei den neuen Optionen liegt: Selbst wenn jede von ihnen auf
null gesetzt wird, bleibt der kurze Frontverlauf bei 30,8 Prozent, also
unter der Untergrenze. Der Hebel, der wirkt, ist die Kapitelwirkung.
Jetzt ist der Bestand vollständig: alle sechs Jahre, alle drei Pfade,
alle Einlagen, alle Briefe. Erst gegen diesen Bestand lässt sich eichen,
ohne auf ein bewegliches Ziel zu schießen. Deshalb steht dieser Schritt
hier und nicht früher.

WAS HIER AUSDRÜCKLICH ERLAUBT IST
Die Sperre aus den Inhaltspaketen fällt. Du darfst und sollst anfassen:
  PFAD_BASIS - die Ausgangswerte je Pfad. NEU IN DIESER LISTE und der
    erste Hebel, siehe Punkt 3a.
  KAPITEL_WIRKUNG und KAPITEL_WIRKUNG_PFAD (kapitel.rpy)
  ENDE_SCHWELLEN (script.rpy)
  KAPITEL_ZIEHUNGEN und MODUS_ZIELZAHL, wenn die Zeitrechnung es verlangt
  EINLAGE_CHANCE, POST_CHANCE und POST_ABSTAND. Nach Schritt 2 gilt
    POST_ABSTAND ab 1919 nicht mehr; POST_CHANCE[1919] steht auf 30 und
    ist bewusst nicht gehoben worden, weil der Hebel hierher gehört.
Was weiterhin NICHT angefasst wird: Ereignistexte, Kennungen, Bedingungen,
Quellen. Dies ist ein Zahlendurchgang.

AUFGABE

TEIL A - ERST MESSEN
1. Gib die vollständige Ausgangstafel aus: je Lage und Verlauf die Quote
   bei zufälliger und bei kluger Wahl, dazu die Zahl der Ereignisse,
   Einlagen und Briefe je Durchgang.
2. NEU IN PROBE 4: Weise Einlagen und Post gesondert aus. Sie machen
   inzwischen rund 2,5 beziehungsweise 2,4 Inhalte je kurzem Durchgang aus
   und tauchen in keiner Wertemessung eigens auf. Zeige, wie viel jede der
   drei Quellen - Ereignisse, Einlagen, Post - zur Verschiebung der vier
   Werte beiträgt. Ohne diese Aufteilung eicht man blind.
3. Rechne den reinen Kalender ohne jedes Ereignis noch einmal durch, wie
   in Paket 0 vorgesehen, und stelle ihn daneben.

TEIL B - DANN EICHEN, IN DIESER REIHENFOLGE
3a. PFAD_BASIS ZÜRST - DIE ETAPPE IST NOCH KEIN PFAD.
   Befund aus Schritt 1, nachdem der Pfad offen war: Auf der Etappe ist
   die kluge Wahl SCHLECHTER als der Zufall. Front und Heimat liegen bei
   +19 und +30 Prozentpunkten zwischen zufälliger und kluger Wahl, die
   Etappe bei -0,2 (6,3 gegen 6,0). Der lange Etappenverlauf erreicht 1918
   einmal in zweitausend Durchgängen.
   Ein Pfad, auf dem Nachdenken nichts bringt, ist kein Pfad, sondern eine
   Zufallsmaschine mit Kulisse. Eine Achtklässlerin merkt das in zehn
   Minuten, und danach klickt sie nur noch.
   Die Ursache liegt nicht in den zwölf neuen Ereignissen - die sind
   gegen dieselben Regeln gebaut wie Front und Heimat und laufen durch
   dieselben Prüfungen. Sie liegt in den Startwerten: PFAD_BASIS gibt der
   Etappe eine Ausgangslage aus der Zeit, als der Pfad geschlossen war und
   niemand ihn gemessen hat. Deshalb steht PFAD_BASIS vor allem anderen.
   1. Gib PFAD_BASIS für alle drei Pfade aus, daneben die vier Werte nach
      der ersten Ziehung und nach der Hälfte des Verlaufs. Erst dann
      sieht man, ob die Etappe zu tief startet oder zu schnell fällt -
      das sind zwei verschiedene Krankheiten mit zwei Behandlungen.
   2. Ändere PFAD_BASIS für die Etappe so, dass zwischen zufälliger und
      kluger Wahl derselbe Abstand entsteht wie auf den anderen beiden
      Pfaden, mindestens aber 15 Prozentpunkte.
   3. Reicht PFAD_BASIS allein nicht, ist die zweite Ursache die
      Kartendecke: Ein Pfad mit weniger ziehbaren Karten wiederholt
      früher und lässt weniger Wahl. Zähle die ziehbaren Karten je Pfad
      und Jahr, gib die Tafel aus und sag mir die Zahl, BEVOR du an den
      Kapitelwirkungen drehst. Fehlen der Etappe Karten, ist das eine
      Inhaltslücke und keine Zahlenfrage - dann sag es und dreh nicht.
   4. Erst wenn die Etappe im Abstand mit den anderen gleichzieht, gehst
      du weiter. Sonst eichst du zwei gesunde Pfade an einem kranken.
4. KAPITEL_WIRKUNG 1917 bis 1919. 1917 trägt heute allein belastung +2,
   mehr als jedes andere Jahr - eine Zahl aus einer Zeit, in der 1917
   keine einzige Ziehung kostete. Beginne hier.
5. KAPITEL_WIRKUNG_PFAD. Prüfe, ob die Häufung 1917/1918 auf einem Pfad
   noch trägt, wenn dieselben Jahre jetzt auch Ereignisse kosten.
6. ENDE_SCHWELLEN gegenrechnen. Bei 30 Ziehungen im langen Verlauf ist
   belastung_ab 12 eine andere Größe als bei 17. Wenn du hier etwas
   änderst, begründe es aus der Zahl der Ziehungen, nicht aus dem
   Wunsch, die Quote zu heben.
7. Erst danach EINLAGE_CHANCE und POST_CHANCE, und nur, wenn die
   Aufteilung aus Teil A sie als Ursache ausweist.
8. Nach jeder einzelnen Stufe: messen, Tafel ausgeben, weitergehen. Nicht
   drei Stellschrauben zugleich drehen.

TEIL C - DIE GRENZEN
9. Ziel wie in Paket 2, Schritt 3: bei zufälliger Wahl erreichen 40 bis 60 Prozent
   der Durchgänge das Jahr 1919, bei kluger Wahl mindestens 80 - in JEDER
   Lage und BEIDEN Verläufen. Die Etappe zählt ab jetzt mit.
10. Diese Grenzen sind ab hier verbindlich. Sie stehen auf dem vollen
   Bestand, und der ändert sich nicht mehr - die Pakete 6 bis 10 fassen
   keine Werte mehr an. Trage das als Kommentar über KAPITEL_WIRKUNG ein,
   mit dem Datum und der Zahl der Ziehungen, gegen die geeicht wurde.
11. WAS VERBOTEN BLEIBT: die Abbruchschwellen so weit hochsetzen, dass der
   Abbruch praktisch verschwindet. Ein Abbruch muss möglich und spürbar
   bleiben; er ist nur nicht mehr der Normalfall. Wenn du das Ziel ohne
   solche Tricks nicht erreichst, sagst du es mit Zahl und Begründung.

TEIL C1 - DER JAHRESBOGEN HAT KEINE TRÄGER MEHR
13a. KAPITEL_BOGEN trägt für 1917 bis 1919 auf allen drei Pfaden leere
   Trägerlisten (kapitel.rpy:284-336). Als der Bogen in Paket 2, Schritt 1 entstand,
   waren diese Jahre leer; seither sind sie gefüllt, die Listen nicht.
   BOGEN_ZUSCHLAG greift dort also nirgends, und Probe 1 kann es nicht
   melden - eine Lücke, die keine Zahl zeigt.
   Trage für jedes der neun Felder (drei Jahre mal drei Pfade) die
   Träger nach: die Ereignisse, die das Jahr auf diesem Pfad tragen.
   Jeder Träger muss kern=True haben, wie in Paket 2, Schritt 2 festgelegt.
   Ergänze probe_alles.py um die Meldung leerer Trägerlisten, damit das
   nicht wieder unbemerkt bleibt.
13b. Heimat 1914 im langen Verlauf steht auf "knapp": 6 freie Ereignisse
   bei Soll 5, für "in Ordnung" wären 7 nötig. Es ist die einzige Zeile
   im ganzen Bestand ohne Reserve. Ein weiteres freies Heimatereignis für
   1914 - oder die Jahresausweitung eines vorhandenen - schließt sie.

TEIL C2 - DREI VERWAISTE EINTRÄGE IM KETTENPLAN
14. Nach Paket 2, Schritt 2 stehen drei Kennungen im zusammengeführten Plan, die es
   nicht gibt und auf die nichts verweist: heimat_1917_hinterhaus,
   heimat_1918_schulbank, front_1918_wiedersehen. Sie stehen nur im
   KETTEN_PLAN, ihre ersten Glieder setzen keine Kette, es geht also
   nichts verloren.
   Entscheide je Kennung und handle danach: Entweder du hängst das erste
   Glied nach - dann muss es eine Option geben, die die Kette wirklich
   setzt, und das zweite Glied muss ein späteres Jahr abdecken - oder du
   streichst den Eintrag aus dem Plan und schreibst in einem Satz dazu,
   warum. Ein Plan, in dem Kennungen stehen, die niemand baut, ist beim
   nächsten Mal wieder eine Beanstandung.

TEIL D - DIE WERKBANK SELBST
12. Der Satzzerleger von Probe 8 trennt nicht nach einer Jahreszahl und
   nicht nach einem Anführungszeichen hinter dem Punkt. Er meldet dadurch
   zu lange Sätze, die es nicht gibt, und Probe 5 meldet fälschlich
   "einordnung hat 1 Sätze statt genau zwei". Repariere satzzahl() und
   den Zerleger: eine Zahl mit Punkt beendet keinen Satz, ein Punkt vor
   einem schließenden Anführungszeichen schon. Zeige an fünf Beispielen
   aus dem Bestand, dass es jetzt stimmt.
13. Ketten können auch von Einlagen vorgemerkt werden - die Einlage
   hamsterfahrt merkt heimat_verfahren vor (minispiele.rpy:986), nicht nur
   das gleichnamige Ereignis. Prüfe alle vier Einlagen auf solche
   Vormerkungen und nimm sie in die Kettenprüfung von probe_alles.py auf.
15. DIE WERKBANK PRÜFT SICH SELBST. probe_alles.py ist inzwischen das
   Maß für alles - und niemand prüft das Maß. Baue einen Selbsttest
   ein, der bei jedem vollständigen Lauf zuerst läuft und in bericht.txt
   ganz oben steht:
   a) Laufen alle acht Proben, und schreibt jede ihren Abschnitt - auch
      die, die nichts gefunden hat? Eine Probe, die schweigt, wird als
      "AUSGEFALLEN" gemeldet, nicht weggelassen. Das ist Regel 11.
   b) Passt die Zahl der geprüften Fälle zum Bestand? Die Belegprobe
      muss so viele Quellen sehen, wie es Ereignisse und Einlagen gibt;
      die Medienprobe so viele Verweise, wie im Quelltext stehen. Wo die
      Zahlen auseinandergehen, nenne beide und erkläre die Differenz.
   c) Fragt jede Probe, die über Ziehbarkeit urteilt, die Funktionen des
      Projekts - oder baut sie die Bedingung ein zweites Mal nach? Zähle
      die Stellen mit eigenem Nachbau auf und stelle sie um. Probe 2c hat
      nach Schritt 1 null gemeldet, weil Werkbank und Spiel dort dieselbe
      Funktion fragen. Dieser Zustand gilt ab jetzt für alle Proben.
   Gib die Selbsttesttafel im Bericht aus: acht Zeilen, je Probe der
   Zustand und die Zahl der geprüften Fälle.
16. PROBE 8 TRENNT DIE TEXTARTEN - UND DIE EINORDNUNGEN BLEIBEN, WIE SIE
   SIND. Zwölf der gemeldeten langen Sätze stehen in den historischen
   Einordnungen der Einlagen, nicht in Ereignistexten. Sie sind bekannt
   und in Paket 6, Schritt 2 zum Kürzen vorgesehen; bis dahin verdecken
   sie die echten Funde.
   Weise Probe 8 ab jetzt nach Textart getrennt aus: Ereignistext,
   Optionstext, Einordnung, Glossar, Sonstiges. Je Art die Zahl der
   Sätze, die Durchschnittslänge und die Zahl über 20 Wörtern.
   Gekürzt wird hier nichts - das ist Textarbeit und hat in einem
   Zahlendurchgang nichts zu suchen. Es wird nur sichtbar gemacht, was
   wohin gehört.
   KEINE REGELÄNDERUNG: Die Einordnung bleibt bei genau zwei Sätzen,
   jeder unter 20 Wörtern, zusammen höchstens 35. Der Vorschlag, auf
   zwei bis vier Sätze zu erweitern, wird nicht übernommen: Er erlaubt
   bis zu 80 Wörter, und damit fällt der Grund weg, aus dem es das Feld
   "vertiefung" und den Weg ins Glossar überhaupt gibt. Die zwölf Texte
   sind zu lang, nicht die Regel zu eng - 35 Wörter reichen für "was sie
   zeigt und was sie nicht zeigt", das Beispiel steht im Sprachmaß.

TEIL E - EINE ENTSCHEIDUNG ÜBER DEN SCHLUSS
17. DIE HERKUNFT KOMMT IM LEBENSLAUF NICHT VOR. Die Nachklänge der
   Herkunft tragen einen niedrigen Rang; jede Figur trägt daneben eine
   Erwerbslage oder Stellung mit Rang 46 bis 60. Der Lebenslauf zeigt die
   obersten Einträge - und die Herkunft fällt praktisch immer heraus.
   Drei Plätze statt zwei haben es gemildert, nicht behoben.
   Das ist kein Zahlenfehler, sondern eine Entscheidung darüber, was am
   Ende zu sehen sein soll. Sie ist gefallen, und zwar so:
   DER LEBENSLAUF BEKOMMT FESTE FÄCHER STATT EINER RANGLISTE.
   Vier Fächer, in dieser Reihenfolge: Woher du kamst (Herkunft), Wohin
   es dich brachte (Weg und Stellung), Was du entschieden hast
   (Merkmale aus Optionen), Wie es ausging (Schluss und Wirtshaus). Jedes
   Fach zieht seinen obersten Eintrag aus MERKMAL_REIHENFOLGE_LEBENSWEG;
   der Rang entscheidet nur noch INNERHALB eines Fachs.
   Der Grund liegt nicht in der Technik, sondern im Unterricht: Das Spiel
   läuft auf den Vergleich zweier Lebensläufe zu. Fällt die Herkunft
   heraus, vergleichen zwei Schülerinnen nur noch, was ihnen zugestoßen
   ist - nicht, woher sie gestartet sind. Genau der Unterschied ist die
   Stunde.
   1. Ordne jedes Merkmal in MERKMAL_REIHENFOLGE_LEBENSWEG genau einem
      der vier Fächer zu. Gib die Tafel aus: Fach, Merkmal, Rang.
   2. Baue den Lebenslauf auf die Fächer um. Ist ein Fach leer, bleibt
      es leer und die Zeile entfällt - es wird nichts nachgerückt.
   3. Weise an drei Durchgängen nach (einer je Pfad), dass in jedem
      Lebenslauf ein Herkunftseintrag steht.
   4. Ergänze probe_alles.py um die Zählung: In wie viel Prozent der
      Durchgänge erscheint je Fach ein Eintrag? Vier Zeilen, vier Zahlen.
      Das Fach Herkunft muss bei 100 Prozent stehen.

ABNAHME DIESES SCHRITTS
  - Probe 4 weist Ereignisse, Einlagen und Post gesondert aus.
  - Alle sechs Lagen (drei Pfade mal zwei Verläufe) liegen bei
    zufälliger Wahl zwischen 40 und 60 Prozent, bei kluger über 80.
  - Die Tafel nach jeder Eichstufe liegt vor; keine Stufe wurde
    übersprungen.
  - Der Kommentar über KAPITEL_WIRKUNG nennt Datum und Ziehungszahl.
  - Probe 8 und Probe 5 melden keine erfundenen Beanstandungen mehr;
    fünf Beispiele belegen es.
  - Die Kettenprüfung erfasst die Vormerkungen aus den Einlagen.
  - Die drei verwaisten Ketteneinträge sind entschieden: gebaut oder
    gestrichen, jeweils mit einem Satz Begründung.
  - KAPITEL_BOGEN hat für alle sechs Jahre und drei Pfade Träger; die
    Probe meldet leere Listen.
  - Keine Bestandszeile steht mehr auf "knapp".
  - Die Etappe erreicht bei kluger Wahl mindestens 15 Prozentpunkte mehr
    als bei zufälliger - die Zahl steht neben denen von Front und Heimat.
  - Die Selbsttesttafel steht im Bericht: acht Proben, acht Zustände,
    acht Fallzahlen. Keine Probe steht auf "AUSGEFALLEN".
  - Der Lebenslauf hat vier Fächer; das Fach Herkunft erscheint in
    100 Prozent der Durchgänge.
  - Probe 8 weist die fünf Textarten getrennt aus. Die Zahl der langen
    Sätze in Ereignis- und Optionstexten ist von der Zahl in den
    Einordnungen getrennt ablesbar.

PRÜFEN MIT: probe_alles.py vollständig, dazu --vergleich gegen den
Bericht vor diesem Schritt.
```

---

## Gesamtabnahme

```text
- Alle 3 Schritte haben ihre eigene Abnahme bestanden; nenne je
  Schritt das entscheidende Kriterium und die Zahl dazu.
- python probe_alles.py (vollständig, ohne --schnell) läuft durch.
- python probe_alles.py --vergleich bericht_ausgang.txt zeigt für
  jede Probe: früher, heute, Differenz. Keine Probe ist schlechter
  geworden. Wo eine schlechter wurde, begründest du sie einzeln.
- Das Spiel startet, errors.txt und traceback.txt sind leer.
- STAND.md, auftrag/OFFENE_PUNKTE.md und auftrag/PAKETPLAN.md sind
  auf dem Stand nach diesem Paket.
```

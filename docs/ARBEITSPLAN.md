# Arbeitsplan — Zwischen den Fronten (Neuaufbau)

Historisches Zwei-Entscheidungs-Lernspiel über den Alltag 1914–1919 für die **8. Klasse Oberschule (13–14 Jahre)**.
Eine Codebasis in **Kotlin + Compose Multiplatform** für **Android, Windows und WebApp**.

> Der ursprüngliche Ren'Py-Arbeitsstand liegt unverändert im Archiv-Branch `archiv/renpy-2026`.

---

## Festgelegte Leitplanken

- **Reines Zwei-Entscheidungs-System:** Jede Karte stellt eine konkrete, sinnliche Alltagssituation und genau zwei plausible, gleichwertige Entscheidungen — kein „Richtig/Falsch“, kein Zurück, keine Punkte.
- **Gestrichene Nebensysteme:** Briefsystem, Merkbuch, 5 Minispiele („Einlagen“) und Visual-Novel-Dialogbühne sind entfernt. Die vier stärksten Alltagsthemen (*Tornister*, *Rotstift/Zensur*, *Acht Striche/Rationen*, *Versorgungsantrag*) leben als normale 2-Wahl-Karten weiter.
- **Befindensleiste oben + Live-Emotions-Kachel rechts oben:** Die 4 Werte (*Hunger, Erschöpfung, Verdacht, Einsamkeit* — Balken voll = gut) bleiben der Kern der Oberfläche. Die kleine Charakter-Kachel rechts oben reagiert **live** mit 5 Emotionen (`neutral`, `hungrig`, `erschoepft`, `angst`, `einsam`) auf den aktuellen Zustand (40 Rollen-Portraits: 4 Herkünfte × 2 Geschlechter × 5 Stimmungen).
- **Frischer, einheitlicher Bildstil (AP 5):** Die alten Beispielbilder werden nicht übernommen; in AP 5 legen wir gemeinsam einen neuen, ruhigen, respektvollen und jugendgerechten Illustrationsstil fest (ohne Gewaltdarstellung).

---

## Arbeitspakete (AP 1 – AP 7)

| AP | Titel | Stand | Ergebnis / Abnahme |
|---|---|---|---|
| **AP 1** | **Inhalts-Extraktion & Bereinigung** | ✅ erledigt | 104 geprüfte 2-Wahl-Ereignisse, 6 Kapitel, Herkunft/Musterung, 34 erreichbare Merkmale, 4-Fächer-Lebenslauf, Live-Emotions-Konfiguration & Medienplan als sauberes JSON unter `content/` + automatische Content-CI (`tools/validate_content.py`). |
| **AP 2** | **Kotlin-Multiplatform-Fundament & Spiel-Engine** | ✅ erledigt | Gradle/KMP-Projekt (`composeApp` + `androidApp`) für Android, Windows Desktop (JVM) und WebApp (`wasmJs` + JS-Fallback), Single-Source-of-Truth-Sync für `content/*.json`, typsichere Datenmodelle (`kotlinx.serialization`), reine `GameEngine` inkl. Live-Stimmungen, direkter Pfadwahl, 4-Fächer-Lebenslauf & Auffangnetz sowie 23 JUnit-/Monte-Carlo-Balance-Tests (Etappen-Balance geprüft & sauber) in GitHub Actions. |
| **AP 3** | **UI-Baukasten, Befindensleiste & Live-Emotions-Kachel** | ✅ erledigt | Archivpapier-Designsystem (`de.pytales.zdf.ui.theme`) direkt aus `konfiguration.json` inkl. 3 Schriftgrößen (`klein`/`mittel`/`gross`) & responsiven Breakpoints (`Kompakt`/`Mittel`/`Breit`), Befindensleiste mit 5-Segment-Balken & Touch-/Klick-Erklärkarte, Live-Emotions-Kachel (vorbereitet für 40 WebP-Portraits), 5-Kartentypen-Baukasten inkl. aufklappbarer Quellen-Einordnung, 16:9-Szenenbild-Rahmen, interaktive Komponenten-Vorschau in `App.kt` sowie 30 grüne Tests (Theme, Mapping, Engine & Balance). |
| **AP 4** | **Kompletter Spieldurchgang (Alpha)** | ✅ erledigt | Testbarer `SpielController` (`de.pytales.zdf.ui.state`) mit strikter Durchsetzung aller Leitplanken (kein Zurück, kein Speichern/Laden, genau 2 Entscheidungen), vollständige Archivpapier-Bildschirmstrecke (`de.pytales.zdf.ui.screens`) vom Startmenü (Modus, 3 aufklappbare Onboarding-Grundsätze, Schriftgröße, Analysemodus, Direktwahl-Schalter & dezenter AP-3-UI-Vorschau-Link) über gestrafften Einstieg (Herkunft, Musterungsbescheid, Erwerbswahl inkl. Einordnungs-Stempeln), Kapitel- & Ereignisschleife 1914–1919 (`KapitelStart` mit 16:9-Kapitelbild-Platzhalter, `EreignisAnzeige`/`EreignisAusgang`, `KapitelAbschluss`, Epilog `wirtshaus_wahl`) bis zu respektvollem Auffangnetz & 4-Fächer-Lebenslauf (`App.kt` direkt im Spiel) sowie 38 grüne Tests & alle Multiplatform-Builds. |
| **AP 5** | **Neue einheitliche Bildwelt (Stufe 1 → Stufe 2)** | ⏳ als Nächstes | Gemeinsame Stilfindung (2–3 Stilproben), dann Stufe 1: **40 Live-Emotions-Portraits + 6 Kapitelbilder + 17 Schauplatzbilder** (= 63 Kernbilder als WebP); danach Stufe 2: schrittweiser Ausbau bis zu 104 Einzel-Szenenbildern. |
| **AP 6** | **Feinschliff, Zugänglichkeit & optionales Audio** | offen | Abschaltbare ruhige Übergänge, Lebenslauf-Export/Druckansicht für das Klassenzimmer, optionales dezentes Audio (harte Musiksperre an Front & Etappe), fehlende historische Vollbelege ergänzen. |
| **AP 7** | **Build, Packaging & Auslieferung** | offen | Fertige Builds für **WebApp** (GitHub Pages), **Windows** (portables `.zip`/`.msi` ohne Adminrechte) und **Android** (Release-`.apk`/`.aab`). |

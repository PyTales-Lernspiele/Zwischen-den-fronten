# Zwischen den Fronten

Ein historisches **Zwei-Entscheidungs-Lernspiel** über den Alltag im Ersten Weltkrieg (1914–1919), entwickelt für die **8. Klasse an der Oberschule** (13–14 Jahre).

Das Spiel wird von Grund auf entschlackt und als moderne **Kotlin-Multiplatform-App** (Compose Multiplatform) für **Android, Windows und Web (`wasmJs` + JS-Fallback)** neu aufgebaut — ohne Briefsystem, Merkbuch, Minispiele oder Dialogbühne, dafür mit vollem Fokus auf klare Entscheidungen, die eine respektvolle und greifbare Geschichte erzählen.

> **Archiv:** Der ursprüngliche Ren'Py-Arbeitsstand ist vollständig im Branch `archiv/renpy-2026` gesichert.

## Projektstruktur (Stand nach AP 5a)

```text
content/                      Single Source of Truth für alle Spielinhalte & WebP-Medien (per Gradle Sync eingebunden)
  konfiguration.json          Werte, 5 Stufen, Live-Emotionen, Modi, Onboarding, Enden
  herkunft.json               4 Herkünfte, 6 Erwerbslagen, Musterung, Jahrgänge, Namen
  kapitel.json                6 Kapitel (1914–1919) mit Leitfragen, Rückblick & Wirkungen
  merkmale.json               34 erreichbare Merkmale, 4-Fächer-Lebenslauf & Ausgänge
  ereignisse.json             104 geprüfte Zwei-Entscheidungs-Ereignisse (Front/Etappe/Heimat)
  sprachregeln.json           Tabu- & Prüfbegriffe sowie Lesbarkeitsgrenzen (Klasse 8)
  medienplan.json             Bildplan (Stil A): 40 Live-Emotions-Portraits, 6 Kapitel, 17 Schauplätze / 104 Szenen
  media/                      Optimierte WebP-Assets (`portraits/`, `kapitel/`, `schauplaetze/`, `szenen/`)
composeApp/                   Kotlin-Multiplatform- & Compose-Multiplatform-Kernmodul
  src/commonMain/             Datenmodelle, ContentLoader, GameEngine, SpielController, Archivpapier-Theme, Multiplatform-Bild-Loader (`de.pytales.zdf.ui.media`), UI-Baukasten & vollständige Spiel-Screens (1914–1919)
  src/commonTest/             JUnit-Testsuite (Deserialisierung, Engine, Balance, Theme, UI-Mapping, Spieldurchläufe & WebP-Bild-Loader)
  src/desktopMain/            Windows/Desktop-Einstieg (JVM)
  src/webMain/                WebApp-Einstieg (WasmJS + JS-Fallback)
androidApp/                   Android-App-Modul (`MainActivity` + Manifest)
tools/
  validate_content.py         Automatische Inhalts-, Referenz-, Balance-, Sprach- und WebP-Medienprüfung
  prepare_media.py            WebP-Aufbereitung (320×320 / 1280×720), Master-Sicherung & Medienplan-Abgleich
docs/
  ARBEITSPLAN.md              Übersicht aller 7 Arbeitspakete (AP 1 – AP 7)
  bildwelt/                   Stil-A-Leitfaden, Prompt-Bibel (`prompt_bibel.json`) & hochauflösende Master-Referenzen (`masters/`)
```

## Prüfen & Bauen

```bash
# 1. JSON-Inhalte, 2-Wahl-Regel, Sprachmaß (Klasse 8) & WebP-Assets prüfen
python3 tools/validate_content.py
# (Für Vollabnahme aller 63 Stufe-1-Bilder nach AP 5b: python3 tools/validate_content.py --require-all-stufe1)

# 2. Neue Stil-A-Rohbilder als optimierte WebP-Assets aufbereiten & Medienplan abgleichen
python3 tools/prepare_media.py --input <ordner_oder_dateien> --save-master --update-plan

# 3. Kotlin-Tests, Medien-Loader-Tests & Monte-Carlo-Balance-Simulation ausführen (JVM + Android Unit)
./gradlew :composeApp:desktopTest :composeApp:testDebugUnitTest

# 4. Alle drei Zielplattformen bauen
./gradlew :androidApp:assembleDebug
./gradlew :composeApp:desktopJar
./gradlew :composeApp:composeCompatibilityBrowserDistribution
```

Alle Prüfungen, Tests und Multiplatform-Builds laufen automatisch bei jedem Pull Request über GitHub Actions (`.github/workflows/content-ci.yml`).

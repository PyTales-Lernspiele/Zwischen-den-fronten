# Zwischen den Fronten

Ein historisches **Zwei-Entscheidungs-Lernspiel** über den Alltag im Ersten Weltkrieg (1914–1919), entwickelt für die **8. Klasse an der Oberschule** (13–14 Jahre).

Das Spiel wird von Grund auf entschlackt und als moderne **Kotlin-Multiplatform-App** (Compose Multiplatform) für **Android, Windows und Web (`wasmJs` + JS-Fallback)** neu aufgebaut — ohne Briefsystem, Merkbuch, Minispiele oder Dialogbühne, dafür mit vollem Fokus auf klare Entscheidungen, die eine respektvolle und greifbare Geschichte erzählen.

> **Archiv:** Der ursprüngliche Ren'Py-Arbeitsstand ist vollständig im Branch `archiv/renpy-2026` gesichert.

## Projektstruktur (Stand nach AP 2)

```text
content/                      Single Source of Truth für alle Spielinhalte (per Gradle Sync eingebunden)
  konfiguration.json          Werte, 5 Stufen, Live-Emotionen, Modi, Onboarding, Enden
  herkunft.json               4 Herkünfte, 6 Erwerbslagen, Musterung, Jahrgänge, Namen
  kapitel.json                6 Kapitel (1914–1919) mit Leitfragen, Rückblick & Wirkungen
  merkmale.json               34 erreichbare Merkmale, 4-Fächer-Lebenslauf & Ausgänge
  ereignisse.json             104 geprüfte Zwei-Entscheidungs-Ereignisse (Front/Etappe/Heimat)
  sprachregeln.json           Tabu- & Prüfbegriffe sowie Lesbarkeitsgrenzen (Klasse 8)
  medienplan.json             Bildplan: 40 Live-Emotions-Portraits, 6 Kapitel, 17 Schauplätze / 104 Szenen
composeApp/                   Kotlin-Multiplatform- & Compose-Multiplatform-Kernmodul
  src/commonMain/             Typsichere Datenmodelle, ContentLoader, GameEngine, Platzhalter-UI
  src/commonTest/             JUnit-Testsuite (Deserialisierung, Texte, Emotionen, Ketten, Lebenslauf, Monte-Carlo-Balance)
  src/desktopMain/            Windows/Desktop-Einstieg (JVM)
  src/webMain/                WebApp-Einstieg (WasmJS + JS-Fallback)
androidApp/                   Android-App-Modul (`MainActivity` + Manifest)
tools/
  validate_content.py         Automatische Inhalts-, Referenz-, Balance- und Sprachprüfung
docs/
  ARBEITSPLAN.md              Übersicht aller 7 Arbeitspakete (AP 1 – AP 7)
```

## Prüfen & Bauen

```bash
# 1. JSON-Inhalte, 2-Wahl-Regel & Sprachmaß (Klasse 8) prüfen
python3 tools/validate_content.py

# 2. Kotlin-Tests & Monte-Carlo-Balance-Simulation ausführen (JVM + Android Unit)
./gradlew :composeApp:desktopTest :composeApp:testDebugUnitTest

# 3. Alle drei Zielplattformen bauen
./gradlew :androidApp:assembleDebug
./gradlew :composeApp:desktopJar
./gradlew :composeApp:composeCompatibilityBrowserDistribution
```

Alle Prüfungen, Tests und Multiplatform-Builds laufen automatisch bei jedem Pull Request über GitHub Actions (`.github/workflows/content-ci.yml`).

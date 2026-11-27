# Zwischen den Fronten

Ein historisches **Zwei-Entscheidungs-Lernspiel** über den Alltag im Ersten Weltkrieg (1914–1919), entwickelt für die **8. Klasse an der Oberschule** (13–14 Jahre).

Das Spiel wird von Grund auf entschlackt und als moderne **Kotlin-Multiplatform-App** (Compose Multiplatform) für **Android, Windows und Web (`wasmJs` + JS-Fallback)** neu aufgebaut — ohne Briefsystem, Merkbuch, Minispiele oder Dialogbühne, dafür mit vollem Fokus auf klare Entscheidungen, die eine respektvolle und greifbare Geschichte erzählen.

> **Archiv:** Der ursprüngliche Ren'Py-Arbeitsstand ist vollständig im Branch `archiv/renpy-2026` gesichert.

## Projektstruktur

```text
content/                      Single Source of Truth für alle Spielinhalte & WebP-Medien (per Gradle Sync eingebunden)
  konfiguration.json          Werte, 5 Stufen, Live-Emotionen, Modi, Onboarding, Enden
  herkunft.json               4 Herkünfte, 6 Erwerbslagen, Musterung, Jahrgänge, Namen
  kapitel.json                6 Kapitel (1914–1919) mit Leitfragen, Rückblick & Wirkungen
  merkmale.json               34 erreichbare Merkmale, 4-Fächer-Lebenslauf & Ausgänge
  ereignisse.json             104 geprüfte Zwei-Entscheidungs-Ereignisse mit 104/104 historischen Vollbelegen (Front/Etappe/Heimat)
  sprachregeln.json           Tabu- & Prüfbegriffe sowie Lesbarkeitsgrenzen (Klasse 8)
  medienplan.json             Bildplan (Stil A): 40 Live-Emotions-Portraits, 6 Kapitel, 17 Schauplätze und 104 individuelle Ereignisszenen
  media/                      Optimierte WebP-Assets (`portraits/`, `kapitel/`, `schauplaetze/`, `szenen/`)
composeApp/                   Kotlin-Multiplatform- & Compose-Multiplatform-Kernmodul
  src/commonMain/             Datenmodelle, ContentLoader, GameEngine, SpielController (inkl. Zurück-Leitplanke & einklappbarer Kopfleiste), Archivpapier-Theme (Buchdruck-Optik, WCAG-Kontrast & Landscape-First-Metriken), Multiplatform-Bild-Loader (`ui.media`), Klassenzimmer-Export/Druckaufbereitung (`ui.export`), dezentes Audio-Regelwerk mit harter Musiksperre an Front & Etappe (`audio`) sowie alle aufgeräumten Spiel-Screens (1914–1919)
  src/commonTest/             55 JUnit-Tests (Deserialisierung, Engine, Balance, Theme/WCAG/Landscape, UI-Mapping, Spieldurchläufe, Zurück-Leitplanke, WebP-Loader, Lebenslauf-Export & Audio-Musiksperre/Hintergrund-Pause)
  src/androidMain/            Android-Plattformbrücken (PrintManager/Share/Clipboard, BackHandler & AudioTrack mit Hintergrund-Pause)
  src/desktopMain/            Windows/Desktop-Einstieg (JVM) inkl. Browser-Druckansicht/Speichern & dezentes Sound-Audio
  src/webMain/                WebApp-Einstieg (WasmJS + JS-Fallback) inkl. Startseite mit Ladeanzeige, Favicon & Web-Manifest
  src/wasmJsMain/ & jsMain/   Web-Plattformbrücken (Browser-Druck/Download/Clipboard & Web Audio API)
androidApp/                   Auslieferungsfertiges Android-Modul (`MainActivity` im Querformat `sensorLandscape`, Edge-to-Edge/Safe-Area & Audio-Lebenszyklus, Archivpapier-Adaptive-Icon, R8/ProGuard `proguard-rules.pro` & optionale Release-Signierung für `.apk`/`.aab`)
tools/
  validate_content.py         Automatische Inhalts-, Quellen-/Vollbeleg-, Referenz-, Balance-, Sprach- und WebP-Medienprüfung
  prepare_media.py            WebP-Aufbereitung (320×320 / 1280×720), Master-Sicherung & Medienplan-Abgleich
docs/
  ARBEITSPLAN.md              Übersicht aller Arbeitspakete (AP 1–AP 8; AP 7b offen)
  ANDROID_AUSLIEFERUNG.md     Praxisanleitung für Android-Installation (Schul-Tablets/APK), Keystore-Signierung & Play-Store-AAB
  bildwelt/                   Stil-A-Leitfaden, Prompt-Bibel (`prompt_bibel.json`) & Master-Referenzen (`masters/`)
```

## Prüfen & Bauen

```bash
# 1. JSON-Inhalte, 2-Wahl-Regel, 104/104 Vollbelege, Sprachmaß (Klasse 8) & WebP-Assets prüfen
python3 tools/validate_content.py --require-all-stufe1

# 2. Neue Stil-A-Rohbilder als optimierte WebP-Assets aufbereiten & Medienplan abgleichen
python3 tools/prepare_media.py --input <ordner_oder_dateien> --save-master --update-plan

# 3. Alle 55 Kotlin-Tests, Export-/Audio-Tests & Monte-Carlo-Balance-Simulation ausführen (JVM + Android Unit)
./gradlew :composeApp:desktopTest :composeApp:testDebugUnitTest

# 4. Android-Release (.apk & .aab) sowie Desktop & Web bauen
./gradlew :androidApp:assembleDebug :androidApp:assembleRelease :androidApp:bundleRelease
./gradlew :composeApp:desktopJar
./gradlew :composeApp:composeCompatibilityBrowserDistribution
```

### Android-Auslieferung (Schul-Tablets & Play Store)
- **Querformat & Bedienung:** Auf Smartphones und Schul-Tablets läuft die App fest im beidseitig drehbaren Querformat (`sensorLandscape`) mit sehr schlanker, ein- und ausklappbarer Kopfleiste, zweispaltiger Spielbühne und ruhigen Overlay-Erklärkarten.
- **Direktinstallation & Signierung:** Vollständige Anleitung für Lehrkräfte, Schul-Tablets (APK-Sideloading/MDM) und eigene Play-Store-Signierung unter [`docs/ANDROID_AUSLIEFERUNG.md`](docs/ANDROID_AUSLIEFERUNG.md).
- **Automatisierte Releases:** Der GitHub-Actions-Workflow [`.github/workflows/android-release.yml`](.github/workflows/android-release.yml) erstellt per manuellem Start (`workflow_dispatch`) oder Tag (`v*`) geprüfte `.apk`- und `.aab`-Pakete inkl. `SHA256SUMS.txt` (optional signiert über Repository-Secrets, sonst mit direkt installierbarem Test-Fallback).
- **CI bei jedem Pull Request:** Alle Prüfungen, Tests sowie Android Debug/Release, Desktop JVM und WebApp laufen automatisch über [`.github/workflows/content-ci.yml`](.github/workflows/content-ci.yml).

### Webfassung (GitHub Pages)
- **Direkt im Browser spielen:** <https://pytales-lernspiele.github.io/Zwischen-den-fronten/> — ohne Installation, ohne Anmeldung und ohne Tracking. Moderne Browser laden die WebAssembly-Fassung, ältere automatisch den JavaScript-Fallback.
- **Automatische Veröffentlichung:** Jeder Push auf `main` baut die Webfassung neu und veröffentlicht sie über [`.github/workflows/web-pages.yml`](.github/workflows/web-pages.yml) (vorher Inhalts- und Medienprüfung). Ein manueller Start ist unter *Actions → „Web — GitHub Pages“ → Run workflow* möglich.
- **Für PC & große Tablets optimiert:** Auf großen Bildschirmen wächst die gesamte Oberfläche automatisch und gestochen scharf mit (`AnzeigeSkalierung`: Bezugsfläche 1120 × 680 dp, Faktor 1,0–1,75 – z. B. ×1,35 im Full-HD-Browserfenster, ×1,2 auf dem iPad Pro). Die Webfassung zeichnet zusätzlich mit Auflösungsreserve, sodass auch Browser-Zoom bis 200 % und der Wechsel auf einen anderen Monitor scharf bleiben. Mit der Maus zeigen alle bedienbaren Elemente den Hand-Zeiger.
- **Einmalige Einrichtung:** Unter *Settings → Pages → Build and deployment → Source* muss **„GitHub Actions“** ausgewählt sein.
- **Lokal testen:** Nach `./gradlew :composeApp:composeCompatibilityBrowserDistribution` liegt die fertige statische Website unter `composeApp/build/dist/composeWebCompatibility/productionExecutable/` und lässt sich mit jedem Webserver ausliefern, z. B. `python3 -m http.server -d composeApp/build/dist/composeWebCompatibility/productionExecutable 8080`.

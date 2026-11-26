# Android-Auslieferung, Installation & Signierung (AP 7a)

Diese Anleitung beschreibt die Auslieferung von **„Zwischen den Fronten“ (Alltag 1914–1919, 8. Klasse Oberschule)** als fertige Android-App:

- **`.apk`** für die direkte Installation (Sideloading / Schul-MDM) auf Android-Tablets und -Smartphones (ab **Android 7.0 / API 24**, optimiert bis **Android 15 / API 35**)
- **`.aab`** (*Android App Bundle*) für die Veröffentlichung im **Google Play Store**

> **Schul- und Datenschutz-Hinweis:** Die App läuft **vollständig offline**, enthält keinerlei Tracking oder Werbung und fordert **keine gefährlichen Android-Berechtigungen** an. Lebenslauf-Druck/PDF-Export nutzt den systemeigenen Android-Druckdienst (`PrintManager`), Teilen nutzt das Standard-Teilen-Menü.

---

## 1. Direkte Installation auf Schul-Tablets (APK / Sideloading)

### Einzelgeräte (ohne Play Store)
1. Aktuelle `.apk`-Datei aus den **GitHub Actions Artefakten** (Workflow `Release — Android Auslieferung`) oder einem **GitHub Release** herunterladen und auf das Tablet übertragen (USB, Schulcloud, Nextcloud, SD-Karte oder Browser-Download).
2. Die `.apk`-Datei in der Dateien-App des Tablets antippen.
3. Falls Android eine Rückfrage zeigt: **„Einstellungen“ → „Aus dieser Quelle zulassen“** aktivieren und zur Installation zurückkehren.
4. Auf **„Installieren“** tippen.
5. *(Empfohlen)* Nach erfolgreicher Installation die Option **„Aus dieser Quelle zulassen“** in den Tablet-Einstellungen wieder deaktivieren.

### Schul-MDM (z. B. Relution, Jamf, IServ, Managed Google Play)
- **Private App-Verteilung per APK:** Die signierte `.apk` direkt im MDM-Portal als Haus-App hochladen und der gewünschten Tablet-Gruppe zuweisen.
- **Managed Google Play:** Für eine dauerhafte Verteilung über Google Play bzw. Managed Google Play die mit eigenem Release-Keystore signierte **`.aab`** verwenden (siehe Abschnitt 3).

> **Wichtig bei Updates:** Android erlaubt ein direktes Überschreiben (Update) einer installierten App nur dann, wenn alte und neue APK mit **demselben Keystore** signiert wurden. Für dauerhafte Schul-Installationen empfiehlt sich daher von Anfang an ein eigener Release-Keystore (statt Debug-Test-Signierung).

---

## 2. Lokal bauen (`.apk` & `.aab`)

### A) Schnell-Build für Tests & direkte Tablet-Installation (ohne eigene Secrets)
Wenn keine Release-Signier-Variablen gesetzt sind, baut Gradle ein vollständiges **R8-optimiertes, ressourcengeschrumpftes Release-Paket** mit automatischem **Debug-Signier-Fallback** (damit die APK sofort auf Test- und Schul-Tablets installierbar ist):

```bash
# 1. Inhalte & Tests prüfen
python3 tools/validate_content.py
./gradlew :composeApp:desktopTest :composeApp:testDebugUnitTest

# 2. Release-APK (.apk) und App Bundle (.aab) bauen
./gradlew :androidApp:assembleRelease :androidApp:bundleRelease
```

Ausgabedateien:
- `androidApp/build/outputs/apk/release/androidApp-release.apk`
- `androidApp/build/outputs/bundle/release/androidApp-release.aab`

*(Optional: Mit `-PZDF_UNSIGNED_RELEASE=true` bzw. `ZDF_UNSIGNED_RELEASE=true` wird stattdessen ein unsigniertes Release-Artefakt erzeugt.)*

### B) Produktiv-Build mit eigenem Release-Keystore
Die vier Signier-Parameter können entweder als **Umgebungsvariablen** oder als **Gradle-Properties** (`-P...`) übergeben werden:

```bash
export ZDF_KEYSTORE_PATH="/sicherer/pfad/zdf-release.jks"
export ZDF_KEYSTORE_PASSWORD="DEIN_KEYSTORE_PASSWORT"
export ZDF_KEY_ALIAS="zdf_release"
export ZDF_KEY_PASSWORD="DEIN_KEY_PASSWORT"

./gradlew :androidApp:assembleRelease :androidApp:bundleRelease
```

Optionale Versions-Überschreibung (Standard in `androidApp/build.gradle.kts`: `versionName = "1.0.0"`, `versionCode = 10000`):

```bash
./gradlew :androidApp:assembleRelease :androidApp:bundleRelease \
  -PZDF_VERSION_NAME="1.0.1" \
  -PZDF_VERSION_CODE="10001"
```

---

## 3. Eigenen Release-Keystore erstellen (für Google Play Store)

Ein eigener Upload-/Release-Keystore wird einmalig lokal mit `keytool` (Teil jedes JDK) erstellt:

```bash
keytool -genkeypair -v \
  -keystore zdf-release.jks \
  -storetype PKCS12 \
  -keyalg RSA \
  -keysize 4096 \
  -validity 10000 \
  -alias zdf_release
```

*(Hinweis zu PKCS12: Bei modernen JDKs nutzt `keytool` das PKCS12-Format, bei dem Keystore-Passwort und Key-Passwort identisch sind — hinterlege in diesem Fall für `ZDF_KEYSTORE_PASSWORD` und `ZDF_KEY_PASSWORD` dasselbe Passwort.)*

**Sicherheitsregeln:**
- Die `.jks`/`.keystore`-Datei **niemals in Git einchecken** (`.jks` und `.keystore` stehen bereits in `.gitignore`).
- Keystore-Datei und Passwörter sicher (z. B. im Passwortmanager / verschlüsselten Schul-Backup) verwahren — bei Verlust können bestehende Play-Store-Apps ohne Play-App-Signing-Reset nicht mehr aktualisiert werden.

### GitHub-Actions-Secrets einrichten
Für automatisch signierte Releases über `.github/workflows/android-release.yml` den Keystore einmalig als Base64-Zeichenkette kodieren:

```bash
# Linux
base64 -w 0 zdf-release.jks

# macOS
base64 -i zdf-release.jks | tr -d '\n'
```

Anschließend im GitHub-Repository unter **Settings → Secrets and variables → Actions → Repository secrets** hinterlegen:

| Secret-Name | Inhalt |
|---|---|
| `ZDF_KEYSTORE_BASE64` | Base64-kodierte `zdf-release.jks` (einzeilig) |
| `ZDF_KEYSTORE_PASSWORD` | Keystore-Passwort |
| `ZDF_KEY_ALIAS` | Alias aus `-alias` (z. B. `zdf_release`) |
| `ZDF_KEY_PASSWORD` | Key-Passwort |

---

## 4. Auslieferung über GitHub Actions

Der Workflow [`.github/workflows/android-release.yml`](../.github/workflows/android-release.yml) prüft zuerst `tools/validate_content.py` und alle JUnit-Tests (JVM + Android Unit) und baut danach `.apk`, `.aab` sowie `SHA256SUMS.txt`:

1. **Manueller Build (`workflow_dispatch`):**
   - Im Repository unter **Actions → „Release — Android Auslieferung (.apk & .aab)“ → Run workflow** starten (optional mit abweichendem `version_name` / `version_code`).
   - Die fertigen Dateien stehen direkt als herunterladbares Workflow-Artefakt bereit.
2. **Tag-Release (`v*`):**
   - Beispiel:
     ```bash
     git tag v1.0.0
     git push origin v1.0.0
     ```
   - Der Workflow erstellt automatisch ein **GitHub Release** mit `.apk`, `.aab` und `SHA256SUMS.txt`.
   - Sind die vier Repository-Secrets gesetzt, erscheinen die Dateien als `*-release.apk` / `*-release.aab`; ohne Secrets greift der Test-Fallback (`*-test-signed.apk` / `*-test-signed.aab`) mit klarem Hinweis in den Release-Notes.

---

## 5. Hinweis zum Nachziehen der Bildwelt (AP 5b)

Im aktuellen Stand (`v1.1.0`, `versionCode = 10100`, festes Querformat `sensorLandscape`) sind bereits **19 von 63 Stil-A-Kernbildern** fest als WebP-Assets in der App gebündelt (alle 8 Basis-Portraits komplett, 10 Live-Emotions-Portraits aus Batch 1 sowie `schauplatz_brotschlange`); fehlende Motive zeigen sauber den Basis-Portrait- bzw. Archivtafel-Fallback (`de.pytales.zdf.ui.media.BildAufloeser`).

Sobald die übrigen **44 Stufe-1-Bilder** (Batches 2–5) aus AP 5b ergänzt werden:
1. Bilder wie in [`docs/bildwelt/PROMPT_BIBEL.md`](bildwelt/PROMPT_BIBEL.md) beschrieben über `python3 tools/prepare_media.py --input <ordner> --save-master --update-plan` einpflegen.
2. Mit `python3 tools/validate_content.py --require-all-stufe1` prüfen.
3. Einen neuen Android-Release-Build bzw. ein neues Tag (z. B. `v1.2.0`) auslösen — **eine Änderung am Android- oder Kotlin-Code ist dafür nicht erforderlich**, da Gradle alle WebP-Dateien aus `content/media/` automatisch in die App packt.

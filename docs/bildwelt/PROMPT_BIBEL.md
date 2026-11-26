# Bildwelt-Leitfaden (AP 5 — Freigegebener Stil A)

## Freigegebener Stil
- **Stil A — Tusche & Aquarell-Lavierung („Archiv-Skizzenbuch“)**
- Feine Sepia-Federzeichnung (`#1f1c18`) mit ruhigen, transparenten Aquarell-Lavierungen auf warmem Archivpapier (`#efe9dc`), gedämpftem Schiefergrau (`#57514a`) und gezieltem Rostrot-Akzent (`#8a3324`).
- **Leitplanken:** Jugendgerecht (8. Klasse, 13–14 Jahre), würdevoll, sachlich-dokumentarisch, **keine Gewaltdarstellung**, kein Blut, keine Schrift/Buchstaben im Bild.

## Dauerhafte Ablage im Repository
- **Produktions-Assets (Single Source of Truth für Android, Desktop JVM, WebApp):**
  - `content/media/portraits/<id>.webp` (`320×320`, ca. 10–15 KB je Portrait)
  - `content/media/kapitel/<id>.webp` (`1280×720`, 16:9 randabfallend)
  - `content/media/schauplaetze/<id>.webp` (`1280×720`, 16:9 randabfallend)
  - `content/media/szenen/<id>.webp` (`1280×720`, optional Stufe 2)
- **Hochauflösende Master-Referenzen (nicht in App-Builds gepackt):**
  - `docs/bildwelt/masters/<id>.jpg` — dauerhaft auf GitHub gesichert, dient als 1:1-Gesichts- und Stil-Referenz für alle Folge-Batches.

## Stand AP 5a (8 von 63 Stufe-1-Kernbildern vorhanden)
- **7 Basis-Portraits (`neutral`):**
  - `portrait_arbeiterschaft_w_neutral`
  - `portrait_arbeiterschaft_m_neutral`
  - `portrait_buergertum_m_neutral`
  - `portrait_buergertum_w_neutral`
  - `portrait_landbevoelkerung_m_neutral`
  - `portrait_landbevoelkerung_w_neutral`
  - `portrait_adel_m_neutral`
- **1 Schauplatzbild:**
  - `schauplatz_brotschlange`

> Dank des gestuften Portrait-Fallbacks im Bild-Loader (`de.pytales.zdf.ui.media.BildAufloeser`) werden diese 7 Basis-Portraits bereits über alle 5 Stimmungen hinweg im Spiel angezeigt, bis die 32 spezifischen Emotions-Varianten nachgezogen sind.

## Nachproduktion der 55 offenen Stufe-1-Bilder (AP 5b)
Alle 55 offenen Prompts inkl. exaktem Referenzbild-Pfad liegen maschinenlesbar in [`docs/bildwelt/prompt_bibel.json`](prompt_bibel.json), aufgeteilt in **5 Batches à 11 Motive**:

1. **Batch 1 (11 Motive):** `portrait_adel_w_neutral` + Emotions-Portraits `arbeiterschaft` (w/m) & `buergertum_m` (Teil 1)
2. **Batch 2 (11 Motive):** Emotions-Portraits `buergertum` (Rest) & `landbevoelkerung` (Teil 1)
3. **Batch 3 (11 Motive):** Emotions-Portraits `landbevoelkerung_w` (Rest) & `adel` (danach alle 40 Portraits 100 % fertig)
4. **Batch 4 (11 Motive):** Alle 6 Kapitelbilder (`kapitel_1914`–`kapitel_1919`) + 5 Schauplätze (`amt` bis `fabrik`)
5. **Batch 5 (11 Motive):** Restliche 11 Schauplätze (`gefangenenlager` bis `wohnviertel` — danach Stufe 1 mit 63/63 komplett)

### Einbindung neuer Bilder (1 Befehl)
Sobald Rohbilder (Dateiname `<asset_id>.jpg` / `.png`) aus einem Batch vorliegen:

```bash
python3 tools/prepare_media.py --input <ordner_oder_dateien> --save-master --update-plan
python3 tools/validate_content.py
```

Für die Vollabnahme nach Abschluss von Batch 5:

```bash
python3 tools/validate_content.py --require-all-stufe1
```

Eine Code-Änderung in Kotlin ist beim Nachliefern weiterer Bilder **nicht nötig** — Gradle synchronisiert alle `.webp`-Dateien unter `content/media/` automatisch in die Compose-Multiplatform-Ressourcen, und `BildAufloeser` zeigt sie sofort an.

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

## Stand AP 5b nach Batch 2 + Batch-3-Teilstand (32 von 63 Stufe-1-Kernbildern vorhanden)
- **Alle 8 Basis-Portraits (`neutral`) — 100 % komplett:**
  - `portrait_arbeiterschaft_w_neutral`, `portrait_arbeiterschaft_m_neutral`
  - `portrait_buergertum_w_neutral`, `portrait_buergertum_m_neutral`
  - `portrait_landbevoelkerung_w_neutral`, `portrait_landbevoelkerung_m_neutral`
  - `portrait_adel_w_neutral` *(Batch 1)*, `portrait_adel_m_neutral`
- **23 Live-Emotions-Portraits *(31/40 Portraits insgesamt fertig)*:**
  - `portrait_arbeiterschaft_w_{hungrig,erschoepft,angst,einsam}` *(Batch 1 — komplett)*
  - `portrait_arbeiterschaft_m_{hungrig,erschoepft,angst,einsam}` *(Batch 1 — komplett)*
  - `portrait_buergertum_m_{hungrig,erschoepft,angst,einsam}` *(Batch 1 & 2 — komplett)*
  - `portrait_buergertum_w_{hungrig,erschoepft,angst,einsam}` *(Batch 2 — komplett)*
  - `portrait_landbevoelkerung_m_{hungrig,erschoepft,angst,einsam}` *(Batch 2 — komplett)*
  - `portrait_landbevoelkerung_w_{hungrig,angst}` *(Batch 2 + Batch-3-Vorlauf)*
  - `portrait_adel_m_hungrig` *(Batch 3)*
- **1 Schauplatzbild:**
  - `schauplatz_brotschlange`

> Dank des gestuften Portrait-Fallbacks im Bild-Loader (`de.pytales.zdf.ui.media.BildAufloeser`) werden alle 8 Basis-Portraits bereits über alle Herkünfte und Geschlechter hinweg im Spiel angezeigt; für `arbeiterschaft` (w/m), `buergertum` (w/m) und `landbevoelkerung_m` sind sämtliche 5 Live-Emotionen vollständig eingebunden, für `landbevoelkerung_w` bereits `neutral`, `hungrig` und `angst` sowie für `adel_m` bereits `neutral` und `hungrig`.

## Nachproduktion der 31 übrigen Stufe-1-Bilder (AP 5b, Rest Batch 3 bis Batch 5)
Alle Prompts inkl. exaktem Referenzbild-Pfad liegen maschinenlesbar in [`docs/bildwelt/prompt_bibel.json`](prompt_bibel.json), aufgeteilt in **5 Batches à 11 Motive**:

1. **Batch 1 (11 Motive) — ✅ erledigt:** `portrait_adel_w_neutral` + Emotions-Portraits `arbeiterschaft` (w/m) & `buergertum_m` (Teil 1) → **19/63**
2. **Batch 2 (11 Motive) — ✅ erledigt:** Emotions-Portraits `buergertum` (Rest) & `landbevoelkerung` (Teil 1) → **30/63**
3. **Batch 3 (11 Motive) — 🔄 2/11 erledigt (`portrait_landbevoelkerung_w_angst`, `portrait_adel_m_hungrig` → 32/63), 9 offen:** Rest-Emotions-Portraits `landbevoelkerung_w` (`erschoepft`, `einsam`), `adel_m` (`erschoepft`, `angst`, `einsam`) & `adel_w` (alle 4 Emotionen → danach alle 40 Portraits 100 % fertig)
4. **Batch 4 (11 Motive) — offen:** Alle 6 Kapitelbilder (`kapitel_1914`–`kapitel_1919`) + 5 Schauplätze (`amt` bis `fabrik`)
5. **Batch 5 (11 Motive) — offen:** Restliche 11 Schauplätze (`gefangenenlager` bis `wohnviertel` — danach Stufe 1 mit 63/63 komplett)

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

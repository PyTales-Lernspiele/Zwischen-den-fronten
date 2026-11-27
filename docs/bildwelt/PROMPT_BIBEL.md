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
  - `content/media/szenen/<id>.webp` (`1280×720`, Ereignisszenen)
- **Master-Referenzen für die Bildbearbeitung:**
  - `docs/bildwelt/masters/<id>.jpg` enthält den Bildausschnitt in seiner ursprünglichen Auflösung vor dem WebP-Export.

## Bildbestand im Spiel

Alle 167 Motive aus dem Medienplan haben ein eigenes Spielbild und einen JPEG-Master.

| Motiv | Anzahl | Verwendung |
|---|---:|---|
| Figurenporträts | 40 | Acht Figuren mit jeweils fünf Stimmungen. Kleidung und Gesicht bleiben über die Zustände hinweg erkennbar. |
| Kapitelbilder | 6 | Jahresauftakt von 1914 bis 1919. |
| Schauplätze | 17 | Wiederkehrende Orte und Ersatzmotiv beim Laden einer Szene ohne eigenes Bild. |
| Ereignisszenen | 104 | Das Motiv zeigt die Situation vor der Entscheidung. |

Die Basis-Prompts und Referenzpfade der Kernmotive stehen in [prompt_bibel.json](prompt_bibel.json). Für Ereignisszenen geben die Texte in `content/ereignisse.json` Zeit, Ort und Situation vor.

### Einbindung neuer Bilder (1 Befehl)
Sobald Rohbilder (Dateiname `<asset_id>.jpg` / `.png`) aus einem Batch vorliegen:

```bash
python3 tools/prepare_media.py --input <ordner_oder_dateien> --save-master --update-plan
python3 tools/validate_content.py
```

Prüfung der Kernbilder:

```bash
python3 tools/validate_content.py --require-all-stufe1
```

Eine Code-Änderung in Kotlin ist beim Nachliefern weiterer Bilder **nicht nötig** — Gradle synchronisiert alle `.webp`-Dateien unter `content/media/` automatisch in die Compose-Multiplatform-Ressourcen, und `BildAufloeser` zeigt sie sofort an.

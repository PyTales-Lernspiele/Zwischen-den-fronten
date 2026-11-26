#!/usr/bin/env python3
"""
Wiederholbare Bild-Aufbereitung fuer „Zwischen den Fronten“ (AP 5 — Stil A).

Funktionen:
- Ordnet Eingabebilder anhand ihrer Asset-ID aus content/medienplan.json automatisch
  der passenden Kategorie zu (portraits, kapitel, schauplaetze, szenen).
- Sichert auf Wunsch hochaufloesende Master-Referenzen dauerhaft in docs/bildwelt/masters/.
- Schneidet Motive sauber auf 1:1 (320x320) bzw. 16:9 (1280x720) zu (bei 16:9 inkl.
  sanftem Rand-Beschnitt gegen doppelte Raender im Archivrahmen).
- Exportiert kompakte, scharfe WebP-Assets nach content/media/<kategorie>/<id>.webp.
- Synchronisiert auf Wunsch die status-Felder in content/medienplan.json.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Iterable

try:
    from PIL import Image, ImageOps
except ImportError as exc:
    print(
        "FEHLER: Pillow (PIL) wird fuer tools/prepare_media.py benoetigt "
        "(pip install pillow).",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
MEDIA_DIR = CONTENT / "media"
MASTERS_DIR = ROOT / "docs" / "bildwelt" / "masters"
MEDIENPLAN_PATH = CONTENT / "medienplan.json"

CATEGORY_MAP = {
    "portraits": ("portraits", "portraitMasse"),
    "kapitelbilder": ("kapitel", "szenenMasse"),
    "schauplatzbilder": ("schauplaetze", "szenenMasse"),
    "einzelSzenenbilder": ("szenen", "szenenMasse"),
}

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def load_medienplan() -> dict:
    return json.loads(MEDIENPLAN_PATH.read_text(encoding="utf-8"))


def build_asset_index(plan: dict) -> dict[str, tuple[str, tuple[int, int]]]:
    """Liefert asset_id -> (unterordner, (breite, hoehe))."""
    fmt = plan["format"]
    index: dict[str, tuple[str, tuple[int, int]]] = {}
    for plan_key, (folder, size_key) in CATEGORY_MAP.items():
        w, h = fmt[size_key]
        for entry in plan[plan_key]:
            index[entry["id"]] = (folder, (int(w), int(h)))
    return index


def detect_subtle_edge_crop(img: Image.Image, max_trim_ratio: float = 0.045) -> Image.Image:
    """
    Entfernt sehr schmale, nahezu einfarbige Papier-/Zeichenraender am aeussersten Rand
    von 16:9-Motiven, damit im bestehenden Archivrahmen kein doppelter Rand entsteht.
    """
    rgb = img.convert("RGB")
    w, h = rgb.size
    pixels = rgb.load()

    def is_uniform_row(y: int, ref_rgb: tuple[int, int, int], tol: int = 24) -> bool:
        step = max(1, w // 64)
        diffs = 0
        total = 0
        for x in range(0, w, step):
            r, g, b = pixels[x, y]
            if abs(r - ref_rgb[0]) > tol or abs(g - ref_rgb[1]) > tol or abs(b - ref_rgb[2]) > tol:
                diffs += 1
            total += 1
        return diffs <= max(1, total // 16)

    def is_uniform_col(x: int, ref_rgb: tuple[int, int, int], tol: int = 24) -> bool:
        step = max(1, h // 64)
        diffs = 0
        total = 0
        for y in range(0, h, step):
            r, g, b = pixels[x, y]
            if abs(r - ref_rgb[0]) > tol or abs(g - ref_rgb[1]) > tol or abs(b - ref_rgb[2]) > tol:
                diffs += 1
            total += 1
        return diffs <= max(1, total // 16)

    max_y = int(h * max_trim_ratio)
    max_x = int(w * max_trim_ratio)
    corner = pixels[2, 2]

    top = 0
    while top < max_y and is_uniform_row(top, corner):
        top += 1

    bottom = h - 1
    corner_b = pixels[2, h - 3]
    while (h - 1 - bottom) < max_y and is_uniform_row(bottom, corner_b):
        bottom -= 1

    left = 0
    while left < max_x and is_uniform_col(left, corner):
        left += 1

    right = w - 1
    corner_r = pixels[w - 3, 2]
    while (w - 1 - right) < max_x and is_uniform_col(right, corner_r):
        right -= 1

    if top > 0 or left > 0 or bottom < h - 1 or right < w - 1:
        # 2px Sicherheitszugabe gegen weiche Uebergangskante
        left = min(left + 2, max_x)
        top = min(top + 2, max_y)
        right = max(right - 2, w - 1 - max_x)
        bottom = max(bottom - 2, h - 1 - max_y)
        if right > left + 32 and bottom > top + 32:
            return rgb.crop((left, top, right + 1, bottom + 1))
    return rgb


def process_asset(
    src_path: pathlib.Path,
    asset_id: str,
    folder: str,
    target_size: tuple[int, int],
    save_master: bool = False,
    trim_border: bool | None = None,
    quality: int = 84,
) -> pathlib.Path:
    if not src_path.exists():
        raise FileNotFoundError(f"Quelldatei nicht gefunden: {src_path}")

    with Image.open(src_path) as raw:
        img = ImageOps.exif_transpose(raw).convert("RGB")

    if save_master:
        MASTERS_DIR.mkdir(parents=True, exist_ok=True)
        master_path = MASTERS_DIR / f"{asset_id}.jpg"
        if src_path.resolve() != master_path.resolve():
            img.save(master_path, format="JPEG", quality=90, optimize=True, progressive=True)

    should_trim = (folder != "portraits") if trim_border is None else trim_border
    working = detect_subtle_edge_crop(img) if should_trim else img

    # Sauberer zentrierter Zuschnitt auf exaktes Ziel-Seitenverhaeltnis + LANCZOS-Skalierung
    fitted = ImageOps.fit(
        working,
        target_size,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )

    out_dir = MEDIA_DIR / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{asset_id}.webp"
    fitted.save(out_path, format="WEBP", quality=quality, method=6)
    return out_path


def sync_medienplan_statuses(plan: dict) -> tuple[int, int]:
    """
    Aktualisiert die status-Felder in content/medienplan.json anhand der real vorhandenen
    WebP-Dateien unter content/media/.
    Gibt (anzahl_stufe1_vorhanden, anzahl_stufe2_vorhanden) zurueck.
    """
    stufe1_vorhanden = 0
    stufe2_vorhanden = 0

    for plan_key, (folder, _) in CATEGORY_MAP.items():
        for entry in plan[plan_key]:
            webp_path = MEDIA_DIR / folder / f"{entry['id']}.webp"
            if webp_path.exists():
                entry["status"] = "vorhanden"
                if entry.get("stufe") == 1:
                    stufe1_vorhanden += 1
                else:
                    stufe2_vorhanden += 1
            else:
                entry["status"] = "offen_ap5"

    MEDIENPLAN_PATH.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return stufe1_vorhanden, stufe2_vorhanden


def iter_input_files(paths: Iterable[pathlib.Path]) -> list[pathlib.Path]:
    found: list[pathlib.Path] = []
    for p in paths:
        if p.is_dir():
            for child in sorted(p.iterdir()):
                if child.is_file() and child.suffix.lower() in SUPPORTED_EXTENSIONS:
                    found.append(child)
        elif p.is_file():
            found.append(p)
        else:
            raise FileNotFoundError(f"Pfad existiert nicht: {p}")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bereitet Stil-A-Illustrationen als optimierte WebP-Assets fuer AP 5 auf."
    )
    parser.add_argument(
        "--input",
        nargs="*",
        type=pathlib.Path,
        default=[],
        help="Eingabedatei(en) oder Ordner (Dateiname ohne Endung = Asset-ID, falls --id fehlt).",
    )
    parser.add_argument(
        "--id",
        dest="asset_id",
        help="Explizite Asset-ID aus content/medienplan.json (nur bei genau einer Eingabedatei).",
    )
    parser.add_argument(
        "--from-masters",
        action="store_true",
        help="Re-exportiert alle gesicherten Masterbilder aus docs/bildwelt/masters/ nach content/media/.",
    )
    parser.add_argument(
        "--save-master",
        action="store_true",
        help="Sichert das hochaufloesende Ausgangsbild zusaetzlich in docs/bildwelt/masters/<id>.jpg.",
    )
    parser.add_argument(
        "--no-trim-border",
        action="store_true",
        help="Deaktiviert den sanften Rand-Beschnitt fuer 16:9-Motive.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=84,
        help="WebP-Qualitaet (Standard: 84).",
    )
    parser.add_argument(
        "--update-plan",
        action="store_true",
        help="Aktualisiert status ('vorhanden' / 'offen_ap5') in content/medienplan.json.",
    )
    parser.add_argument(
        "--sync-plan",
        action="store_true",
        help="Nur content/medienplan.json anhand vorhandener content/media/**/*.webp abgleichen.",
    )
    args = parser.parse_args()

    plan = load_medienplan()
    index = build_asset_index(plan)

    inputs: list[pathlib.Path] = []
    if args.from_masters:
        if not MASTERS_DIR.exists():
            print(f"FEHLER: Master-Verzeichnis fehlt: {MASTERS_DIR}", file=sys.stderr)
            return 1
        inputs.extend(iter_input_files([MASTERS_DIR]))
    if args.input:
        inputs.extend(iter_input_files(args.input))

    if args.asset_id and len(inputs) != 1:
        print("FEHLER: --id darf nur mit genau einer Eingabedatei verwendet werden.", file=sys.stderr)
        return 1

    processed = 0
    for src in inputs:
        aid = args.asset_id or src.stem
        if aid not in index:
            print(f"[UEBERSPRUNGEN] Unbekannte Asset-ID '{aid}' ({src.name})", file=sys.stderr)
            continue
        folder, target_size = index[aid]
        out_path = process_asset(
            src_path=src,
            asset_id=aid,
            folder=folder,
            target_size=target_size,
            save_master=args.save_master and not args.from_masters,
            trim_border=False if args.no_trim_border else None,
            quality=args.quality,
        )
        size_kb = out_path.stat().st_size / 1024.0
        print(f"  [OK] {aid:40s} -> {out_path.relative_to(ROOT)} ({target_size[0]}x{target_size[1]}, {size_kb:.1f} KB)")
        processed += 1

    if args.update_plan or args.sync_plan:
        s1, s2 = sync_medienplan_statuses(plan)
        print(
            f"Medienplan synchronisiert: Stufe 1 = {s1}/{plan['zusammenfassung']['stufe1Gesamt']} vorhanden, "
            f"Stufe 2 = {s2}/{plan['zusammenfassung']['stufe2EinzelSzenenbilder']} vorhanden."
        )

    if processed == 0 and not args.sync_plan:
        print("Keine Bilder verarbeitet. Nutze --input, --from-masters oder --sync-plan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

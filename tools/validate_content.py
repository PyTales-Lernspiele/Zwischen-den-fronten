#!/usr/bin/env python3
"""
Kompakte Qualitaetspruefung fuer alle Spielinhalte unter content/.
Ersetzt die alte Ren'Py-Werkbank (5.653 Zeilen) durch eine schlanke,
klare Pruefung fuer Schema, Zwei-Entscheidungs-Regel, Referenzen,
Bestand, Spielbalance-Regeln, Sprache (Klasse 8) und Live-Emotionen.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
MEDIA = CONTENT / "media"

MEDIA_CATEGORIES = {
    "portraits": ("portraits", "portraitMasse", 45),
    "kapitelbilder": ("kapitel", "szenenMasse", 280),
    "schauplatzbilder": ("schauplaetze", "szenenMasse", 280),
    "einzelSzenenbilder": ("szenen", "szenenMasse", 280),
}

REQUIRED_FILES = [
    "konfiguration.json",
    "herkunft.json",
    "kapitel.json",
    "merkmale.json",
    "ereignisse.json",
    "sprachregeln.json",
    "medienplan.json",
]

# Abkuerzungen, nach deren Punkt kein Satz endet (z. B. k. v., u. k., 19. Januar)
ABKUERZUNGEN = re.compile(
    r"\b(?:k|g|a|d|u|v|bzw|usw|ca|Nr|Art|Kl|WB|LB|St|Dr|Prof|z|B|d|h|S|Mio|Abs)\.$"
)
ORDNUNGSZAHL = re.compile(r"\b\d{1,2}\.$")
MONATE = {
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
    "Klasse", "Jahrhundert", "Aufgebots", "Kompanie", "Division", "Armee",
}


def load_json(name: str) -> dict:
    path = CONTENT / name
    if not path.exists():
        raise FileNotFoundError(f"Pflichtdatei fehlt: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def split_sentences(text: str) -> list[str]:
    """Zerlegt deutschen Text robust in Saetze (inkl. Jahreszahlen und Anfuehrungszeichen)."""
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []

    tokens = text.split(" ")
    sentences: list[str] = []
    buf: list[str] = []

    for i, tok in enumerate(tokens):
        buf.append(tok)
        clean = tok.rstrip("“”\"»«)")
        ends_punct = clean.endswith((".", "!", "?"))
        if not ends_punct:
            continue

        next_tok = tokens[i + 1] if i + 1 < len(tokens) else ""
        # Keine Trennung bei Abkuerzungen wie "k." "v." oder Datum "19. Januar"
        if ABKUERZUNGEN.search(clean):
            continue
        if ORDNUNGSZAHL.search(clean) and next_tok.rstrip(",.;:!?") in MONATE:
            continue
        # Keine Trennung, wenn direkt nach schliessendem Anfuehrungszeichen ein Komma steht: „…“, sagt er.
        if tok.endswith(("“,", "”,", "\",")):
            continue

        sentences.append(" ".join(buf))
        buf = []

    if buf:
        sentences.append(" ".join(buf))
    return sentences


def word_count(sentence: str) -> int:
    words = re.findall(r"[A-Za-zÄÖÜäöüß0-9]+(?:-[A-Za-zÄÖÜäöüß0-9]+)*", sentence)
    return len(words)


def read_webp_dimensions(path: pathlib.Path) -> tuple[int, int]:
    """
    Prueft eine WebP-Datei (RIFF/WEBP + VP8/VP8L/VP8X) ausschliesslich mit der
    Python-Standardbibliothek und liefert (breite, hoehe).
    """
    data = path.read_bytes()
    if len(data) < 30 or data[0:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError("Kein gueltiger RIFF/WEBP-Header.")

    chunk = data[12:16]
    if chunk == b"VP8 ":
        # Lossy VP8-Keyframe: 3-Byte-Frame-Tag, dann 3-Byte-Startcode 9d 01 2a
        if data[23:26] != b"\x9d\x01\x2a":
            raise ValueError("Ungueltiger VP8-Startcode.")
        raw_w, raw_h = struct.unpack("<HH", data[26:30])
        return raw_w & 0x3FFF, raw_h & 0x3FFF

    if chunk == b"VP8L":
        # Lossless VP8L: Signatur-Byte 0x2f, danach 14 Bit Breite-1 und 14 Bit Hoehe-1
        if data[20] != 0x2F:
            raise ValueError("Ungueltige VP8L-Signatur.")
        bits = struct.unpack("<I", data[21:25])[0]
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1

    if chunk == b"VP8X":
        # Extended WebP: 24-Bit-Canvas-Breite-1 (24..26) und -Hoehe-1 (27..29)
        w = int.from_bytes(data[24:27], "little") + 1
        h = int.from_bytes(data[27:30], "little") + 1
        return w, h

    raise ValueError(f"Unbekannter WebP-Chunk-Typ: {chunk!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Qualitaetspruefung fuer Spielinhalte (content/*.json) und Medien-Assets (content/media/)."
    )
    parser.add_argument(
        "--require-all-stufe1",
        action="store_true",
        help="Schlaegt fehl, wenn noch nicht alle 63 Stufe-1-Kernbilder als WebP vorhanden sind.",
    )
    args = parser.parse_args(argv)

    errors: list[str] = []
    warnings: list[str] = []

    # 1. Dateien laden
    data: dict[str, dict] = {}
    for fname in REQUIRED_FILES:
        try:
            data[fname] = load_json(fname)
        except Exception as exc:
            errors.append(f"[Schema] {fname}: {exc}")
    if errors:
        return report(errors, warnings, {})

    konf = data["konfiguration.json"]
    herk = data["herkunft.json"]
    kap = data["kapitel.json"]
    merk = data["merkmale.json"]
    ereig = data["ereignisse.json"]
    sprach = data["sprachregeln.json"]
    medien = data["medienplan.json"]

    valid_pfade = set(konf["pfade"]["reihenfolge"])
    valid_werte = set(konf["werte"]["reihenfolge"])
    hoch_ist_gut = {k: v["hochIstGut"] for k, v in konf["werte"]["definitionen"].items()}
    valid_stimmungen = set(konf["stimmungen"]["alle"])
    valid_enden = set(konf["harteEnden"]["texte"].keys())
    kapitel_jahre = {k["jahr"] for k in kap["kapitel"]}
    valid_kartentypen = {"karte", "feldpost", "lebensmittel", "zeitung", "amtlich"}

    # 2. Live-Emotions-Kachel pruefen
    expected_emotions = {"neutral", "hungrig", "erschoepft", "angst", "einsam"}
    if valid_stimmungen != expected_emotions:
        errors.append(f"[Emotionen] Erwartet {sorted(expected_emotions)}, gefunden {sorted(valid_stimmungen)}")
    for w in valid_werte:
        if konf["stimmungen"]["ausWert"].get(w) not in valid_stimmungen:
            errors.append(f"[Emotionen] Wert '{w}' hat keine gueltige Ziel-Stimmung.")
    expected_portraits = {
        f"portrait_{h['id']}_{g}_{st}"
        for h in herk["herkuenfte"]
        for g in ("m", "w")
        for st in expected_emotions
    }
    actual_portraits = {p["id"] for p in medien["portraits"]}
    if expected_portraits != actual_portraits:
        errors.append(
            f"[Medienplan] Live-Emotions-Portraits unvollstaendig: "
            f"fehlend={sorted(expected_portraits - actual_portraits)}"
        )

    # 3. Bekannte Merkmale sammeln
    known_merkmale = set(merk["register"].keys())
    for h in herk["herkuenfte"]:
        known_merkmale.add(h["id"])
        known_merkmale.update(h["merkmale"])
    for e in herk["erwerbslagen"]:
        known_merkmale.add(e["id"])
        known_merkmale.update(e["merkmale"])
    known_merkmale.update({"kv", "gv", "av", "du", "uk", "zurueck"})

    # 4. Ereignisse pruefen
    events = ereig["ereignisse"]
    if ereig.get("anzahl") != len(events):
        errors.append(f"[Schema] ereignisse.anzahl={ereig.get('anzahl')} != len={len(events)}")

    event_by_id: dict[str, dict] = {}
    for ev in events:
        eid = ev.get("id", "")
        if not eid:
            errors.append("[Ereignis] Ereignis ohne ID.")
            continue
        if eid in event_by_id:
            errors.append(f"[Ereignis] Doppelte ID: {eid}")
        event_by_id[eid] = ev

    schauplaetze_plan = {s["id"] for s in medien["schauplatzbilder"]}
    einzelbilder_plan = {s["id"] for s in medien["einzelSzenenbilder"]}

    # Alle sammelbaren Texte fuer Sprach- & Lesbarkeitspruefung
    spieltexte: list[tuple[str, str]] = []
    quellentexte: list[tuple[str, str]] = []

    valid_kategorien = {"alltag", "einstieg", "finale", "kette"}
    produced_merkmale: set[str] = {
        "kv", "gv", "av", "du", "uk", "zurueck",
        "gemustert", "zurueckgestellt",
        "kinder", "aeltere_kinder", "ehemann_im_feld", "vater_im_feld", "bruder_im_feld",
    }
    for h in herk["herkuenfte"]:
        produced_merkmale.add(h["id"])
        produced_merkmale.update(h["merkmale"])
    for e in herk["erwerbslagen"]:
        produced_merkmale.add(e["id"])
        produced_merkmale.update(e["merkmale"])

    for ev in events:
        eid = ev["id"]
        if ev.get("kategorie") not in valid_kategorien:
            errors.append(f"[{eid}] Ungueltige Kategorie: {ev.get('kategorie')}")
        if not set(ev["pfade"]).issubset(valid_pfade) or not ev["pfade"]:
            errors.append(f"[{eid}] Ungueltige Pfade: {ev['pfade']}")
        if not set(ev["jahre"]).issubset(kapitel_jahre):
            errors.append(f"[{eid}] Ungueltige Jahre: {ev['jahre']}")
        if ev["kartentyp"] not in valid_kartentypen:
            errors.append(f"[{eid}] Ungueltiger Kartentyp: {ev['kartentyp']}")
        if ev["stimmung"] is not None and ev["stimmung"] not in valid_stimmungen:
            errors.append(f"[{eid}] Ungueltige Stimmung: {ev['stimmung']}")
        if ev["schauplatzBild"] not in schauplaetze_plan:
            errors.append(f"[{eid}] schauplatzBild '{ev['schauplatzBild']}' fehlt in medienplan.json")
        if ev["bildId"] not in einzelbilder_plan:
            errors.append(f"[{eid}] bildId '{ev['bildId']}' fehlt in medienplan.json")

        # Merkmal-Referenzen pruefen
        for field in ("braucht", "brauchtEines", "verbietet", "knuepftAn"):
            for m in ev.get(field, []):
                if m not in known_merkmale:
                    errors.append(f"[{eid}] Unbekanntes Merkmal '{m}' in {field}")
        for m in ev.get("gewichtBonus", {}).keys():
            if m not in known_merkmale:
                errors.append(f"[{eid}] Unbekanntes Merkmal '{m}' in gewichtBonus")

        # TextFassung pruefen
        tf = ev["text"]
        if not tf.get("standard"):
            errors.append(f"[{eid}] Leerer Standardtext.")
        else:
            spieltexte.append((f"{eid}.text.standard", tf["standard"]))
        for idx, var in enumerate(tf.get("varianten", [])):
            if not var.get("text"):
                errors.append(f"[{eid}] Leere Textvariante #{idx}.")
            else:
                spieltexte.append((f"{eid}.text.var{idx}", var["text"]))
            if var.get("pfad") and var["pfad"] not in valid_pfade:
                errors.append(f"[{eid}] Ungueltiger Pfad in Textvariante: {var['pfad']}")
            if var.get("merkmal") and var["merkmal"] not in known_merkmale:
                errors.append(f"[{eid}] Unbekanntes Merkmal in Textvariante: {var['merkmal']}")

        # STRIKTE ZWEI-ENTSCHEIDUNGS-REGEL
        opts = ev.get("optionen", [])
        if len(opts) != 2:
            errors.append(f"[{eid}] Muss exakt 2 Optionen haben, hat aber {len(opts)}.")
            continue

        for oidx, opt in enumerate(opts):
            if not opt.get("titel") or not opt.get("beschreibung"):
                errors.append(f"[{eid}] Option {oidx} ohne Titel oder Beschreibung.")
            spieltexte.append((f"{eid}.opt{oidx}.beschreibung", opt.get("beschreibung", "")))
            if not opt["ausgang"].get("standard"):
                errors.append(f"[{eid}] Option {oidx} ohne Standard-Ausgang.")
            else:
                spieltexte.append((f"{eid}.opt{oidx}.ausgang", opt["ausgang"]["standard"]))
            for vidx, var in enumerate(opt["ausgang"].get("varianten", [])):
                spieltexte.append((f"{eid}.opt{oidx}.ausgang.var{vidx}", var["text"]))

            for wk in opt.get("wirkung", {}).keys():
                if wk not in valid_werte:
                    errors.append(f"[{eid}] Option {oidx}: ungueltiger Wert '{wk}'.")
            for m in opt.get("merkmale", []):
                if m not in known_merkmale:
                    errors.append(f"[{eid}] Option {oidx}: unbekanntes Merkmal '{m}'.")
                produced_merkmale.add(m)
            if opt.get("stimmung") is not None and opt["stimmung"] not in valid_stimmungen:
                errors.append(f"[{eid}] Option {oidx}: ungueltige Stimmung '{opt['stimmung']}'.")

            fe = opt.get("folgeEreignis")
            if fe:
                target = event_by_id.get(fe["id"])
                if not target:
                    errors.append(f"[{eid}] Option {oidx}: folgeEreignis '{fe['id']}' existiert nicht.")
                elif ev["jahre"] and target["jahre"]:
                    if max(target["jahre"]) < min(ev["jahre"]) + fe.get("abJahr", 0):
                        errors.append(f"[{eid}] folgeEreignis '{fe['id']}' liegt zeitlich zu frueh.")

            for za in opt.get("zufallsAusgaenge", []):
                if za.get("ausgang"):
                    spieltexte.append((f"{eid}.opt{oidx}.zufall", za["ausgang"]))
                if za.get("sprungEnde") and za["sprungEnde"] not in valid_enden:
                    errors.append(f"[{eid}] Unbekanntes sprungEnde '{za['sprungEnde']}'.")
                for wk in za.get("wirkung", {}).keys():
                    if wk not in valid_werte:
                        errors.append(f"[{eid}] Zufallsausgang: ungueltiger Wert '{wk}'.")

        # Dominanz- & Einbahnstrassen-Pruefung (Regeln g und h)
        o0, o1 = opts[0], opts[1]
        if any(o0.get("wirkung")) or any(o1.get("wirkung")):
            def signed_gain(opt_dict: dict, key: str) -> int:
                raw = opt_dict.get("wirkung", {}).get(key, 0)
                return raw if hoch_ist_gut[key] else -raw

            gains0 = {w: signed_gain(o0, w) for w in valid_werte}
            gains1 = {w: signed_gain(o1, w) for w in valid_werte}

            # Regel g (Entscheidung 14): Einbahnstrasse nur, wenn beide denselben Wert senken
            # UND keine der beiden irgendeinen der vier Werte verbessert
            for w in valid_werte:
                if gains0[w] < 0 and gains1[w] < 0:
                    any_pos = any(v > 0 for v in gains0.values()) or any(v > 0 for v in gains1.values())
                    if not any_pos:
                        errors.append(f"[{eid}] Einbahnstrasse bei '{w}': keine Option verbessert einen Wert.")

            # Regel h: Dominanz (nur pruefen, wenn keine versteckte Kompensation da ist)
            def has_side_effect(opt_dict: dict) -> bool:
                return bool(
                    opt_dict.get("merkmale")
                    or opt_dict.get("folgeEreignis")
                    or opt_dict.get("zufallsAusgaenge")
                    or opt_dict.get("hinweis")
                )

            if not has_side_effect(o0) and not has_side_effect(o1):
                if all(gains0[w] >= gains1[w] for w in valid_werte) and any(gains0[w] > gains1[w] for w in valid_werte):
                    errors.append(f"[{eid}] Dominierte Option: '{o0['titel']}' dominiert '{o1['titel']}'.")
                if all(gains1[w] >= gains0[w] for w in valid_werte) and any(gains1[w] > gains0[w] for w in valid_werte):
                    errors.append(f"[{eid}] Dominierte Option: '{o1['titel']}' dominiert '{o0['titel']}'.")

        # Quelle pruefen
        q = ev.get("quelle")
        if not q or not q.get("kurz") or not q.get("einordnung"):
            errors.append(f"[{eid}] Quelle unvollstaendig (kurz/einordnung fehlt).")
        else:
            quellentexte.append((f"{eid}.quelle.einordnung", q["einordnung"]))

    # 4b. Unerreichbare Merkmale im Register ausschliessen
    dead_register = sorted(set(merk["register"].keys()) - produced_merkmale)
    for dead_m in dead_register:
        errors.append(f"[Merkmale] Register-Eintrag '{dead_m}' wird nirgends im Spiel vergeben.")

    # 5. Kapitel-Traeger und Bestand je Jahr x Pfad x Modus pruefen
    for k in kap["kapitel"]:
        jahr = k["jahr"]
        for pfad in valid_pfade:
            traeger = k["bogen"][pfad]["traeger"]
            for tid in traeger:
                if tid not in event_by_id:
                    errors.append(f"[Kapitel {jahr}/{pfad}] Traeger '{tid}' existiert nicht.")
                elif not event_by_id[tid]["kern"]:
                    errors.append(f"[Kapitel {jahr}/{pfad}] Traeger '{tid}' hat kern=False.")

            for modus in ("kurz", "lang"):
                soll = k["ziehungen"][modus]
                frei = [
                    ev for ev in events
                    if jahr in ev["jahre"]
                    and pfad in ev["pfade"]
                    and not ev["nurKette"]
                    and not ev["braucht"]
                    and not ev["brauchtEines"]
                    and (modus == "lang" or ev["kern"])
                ]
                if len(frei) < soll:
                    errors.append(
                        f"[Bestand] {jahr}/{pfad}/{modus}: nur {len(frei)} frei ziehbare Karten bei Soll {soll}."
                    )
                elif len(frei) < soll + 2:
                    warnings.append(
                        f"[Bestand] {jahr}/{pfad}/{modus}: knappe Reserve ({len(frei)} frei bei Soll {soll})."
                    )

    # 6. Sprachpruefung (Tabubegriffe & Lesbarkeit)
    tabu_list = [(t["begriff"], re.compile(re.escape(t["begriff"]), re.IGNORECASE)) for t in sprach["tabuBegriffe"]]
    pruef_list = [(t["begriff"], re.compile(re.escape(t["begriff"]), re.IGNORECASE)) for t in sprach["pruefBegriffe"]]

    all_checked_texts = list(spieltexte) + list(quellentexte)
    for k in kap["kapitel"]:
        all_checked_texts.append((f"kapitel.{k['jahr']}.text", k["text"]))
        if k.get("rueckblick"):
            all_checked_texts.append((f"kapitel.{k['jahr']}.rueckblick", k["rueckblick"]))
    for mid, mdata in merk["register"].items():
        if mdata.get("nachklang"):
            all_checked_texts.append((f"merkmal.{mid}.nachklang", mdata["nachklang"]["text"]))

    for loc, txt in all_checked_texts:
        for term, rx in tabu_list:
            if rx.search(txt):
                errors.append(f"[Sprache/Tabu] '{term}' gefunden in {loc}")
        for term, rx in pruef_list:
            if rx.search(txt):
                warnings.append(f"[Sprache/Pruefen] '{term}' in {loc}")

    max_w = sprach["maxWoerterJeSatz"]
    total_sentences = 0
    total_words = 0
    over_limit: list[tuple[str, int, str]] = []

    for loc, txt in spieltexte:
        for s in split_sentences(txt):
            wc = word_count(s)
            total_sentences += 1
            total_words += wc
            if wc > max_w:
                over_limit.append((loc, wc, s))

    avg_words = (total_words / total_sentences) if total_sentences else 0.0
    if avg_words > sprach["zielSchnittWoerterJeSatz"]:
        errors.append(
            f"[Lesbarkeit] Durchschnittliche Satzlaenge {avg_words:.2f} > Ziel {sprach['zielSchnittWoerterJeSatz']}."
        )
    for loc, wc, s in over_limit:
        errors.append(f"[Lesbarkeit] {loc} hat {wc} Woerter (>{max_w}): {s[:70]}...")

    # 7. Medien-Assets (AP 5 — eindeutige IDs, WebP-Integritaet, Aufloesung & Medienplan-Abgleich)
    valid_media_statuses = {"vorhanden", "offen_ap5"}
    expected_ext = medien["format"]["dateityp"]
    seen_media_ids: dict[str, str] = {}
    registered_paths: set[pathlib.Path] = set()
    stufe1_vorhanden = 0
    stufe1_gesamt = 0
    stufe2_vorhanden = 0
    stufe2_gesamt = 0
    webp_geprueft = 0

    for plan_key, (folder, size_key, max_warn_kb) in MEDIA_CATEGORIES.items():
        expected_w, expected_h = medien["format"][size_key]
        for entry in medien[plan_key]:
            aid = entry["id"]
            if aid in seen_media_ids:
                errors.append(
                    f"[Medien] Doppelte Asset-ID '{aid}' in {seen_media_ids[aid]} und {plan_key}."
                )
            seen_media_ids[aid] = plan_key

            if not re.fullmatch(r"[a-z0-9_]+", aid):
                errors.append(f"[Medien] Ungueltiger Compose-Ressourcenname fuer Asset-ID '{aid}'.")

            status = entry.get("status", "")
            if status not in valid_media_statuses:
                errors.append(f"[Medien] Unbekannter Status '{status}' bei '{aid}'.")

            ist_stufe1 = entry.get("stufe") == 1
            if ist_stufe1:
                stufe1_gesamt += 1
            else:
                stufe2_gesamt += 1

            asset_path = MEDIA / folder / f"{aid}.{expected_ext}"
            registered_paths.add(asset_path.resolve())
            exists = asset_path.exists()

            if status == "vorhanden":
                if not exists:
                    errors.append(
                        f"[Medien] '{aid}' steht auf status='vorhanden', Datei fehlt jedoch: "
                        f"{asset_path.relative_to(ROOT)}"
                    )
                    continue
                try:
                    w, h = read_webp_dimensions(asset_path)
                except Exception as exc:
                    errors.append(f"[Medien] Ungueltige WebP-Datei '{asset_path.relative_to(ROOT)}': {exc}")
                    continue

                if (w, h) != (expected_w, expected_h):
                    errors.append(
                        f"[Medien] Falsche Aufloesung fuer '{aid}': {w}x{h} statt {expected_w}x{expected_h}."
                    )
                size_kb = asset_path.stat().st_size / 1024.0
                if size_kb > max_warn_kb:
                    warnings.append(
                        f"[Medien] '{aid}' ist relativ gross ({size_kb:.1f} KB > {max_warn_kb} KB)."
                    )
                webp_geprueft += 1
                if ist_stufe1:
                    stufe1_vorhanden += 1
                else:
                    stufe2_vorhanden += 1
            else:
                if exists:
                    errors.append(
                        f"[Medien] Datei '{asset_path.relative_to(ROOT)}' existiert bereits, "
                        f"aber medienplan.json hat noch status='{status}' (tools/prepare_media.py --sync-plan)."
                    )
                elif ist_stufe1 and args.require_all_stufe1:
                    errors.append(
                        f"[Medien] Stufe-1-Kernbild fehlt noch (--require-all-stufe1): "
                        f"{asset_path.relative_to(ROOT)}"
                    )

    if MEDIA.exists():
        for file_path in sorted(MEDIA.rglob(f"*.{expected_ext}")):
            if file_path.resolve() not in registered_paths:
                errors.append(
                    f"[Medien] Nicht im Medienplan registrierte Bilddatei: {file_path.relative_to(ROOT)}"
                )

    stats = {
        "ereignisse": len(events),
        "kapitel": len(kap["kapitel"]),
        "merkmale": len(merk["register"]),
        "livePortraits": len(actual_portraits),
        "schauplaetze": len(schauplaetze_plan),
        "stufe1Vorhanden": f"{stufe1_vorhanden}/{stufe1_gesamt}",
        "stufe2Vorhanden": f"{stufe2_vorhanden}/{stufe2_gesamt}",
        "webpGeprueft": webp_geprueft,
        "saetzeGeprueft": total_sentences,
        "schnittWoerter": round(avg_words, 2),
        "saetzeUeberLimit": len(over_limit),
    }
    return report(errors, warnings, stats)


def report(errors: list[str], warnings: list[str], stats: dict) -> int:
    print("=" * 68)
    print("ZWISCHEN DEN FRONTEN — INHALTS- & MEDIENPRUEFUNG (AP 1 / AP 5)")
    print("=" * 68)
    for k, v in stats.items():
        print(f"  {k:22s}: {v}")
    print("-" * 68)
    if warnings:
        print(f"Hinweise ({len(warnings)}):")
        for w in warnings[:20]:
            print(f"  [!] {w}")
        if len(warnings) > 20:
            print(f"  ... und {len(warnings) - 20} weitere Hinweise")
    if errors:
        print(f"FEHLER ({len(errors)}):")
        for e in errors:
            print(f"  [X] {e}")
        print("=" * 68)
        return 1
    print("ERGEBNIS: ALLE PRUEFUNGEN BESTANDEN (0 Fehler)")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())

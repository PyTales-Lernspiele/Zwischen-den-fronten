# Klangeffekte

Kurze, leise „Schreibtisch- und Akten“-Klänge geben Rückmeldung auf Bedienhandlungen und Spielschritte.
Bewusst gibt es **keine Kriegsgeräusche** (Schüsse, Explosionen, Sirenen). Die harte Musiksperre an
Front, Etappe und im Auffangnetz (`AudioRegelwerk`) betrifft nur die Hintergrundmusik. Die
Klangeffekte sind neutrale Rückmeldungen und daher überall erlaubt.

- **Ein/Aus:** Lautsprecher-Symbol oben rechts oder *Einstellungen → Klangeffekte*. Klangeffekte sind
  standardmäßig **an**, die Hintergrundmusik („Leise Musik“) ist standardmäßig **aus**.
- **Technik:** 16-Bit-PCM-WAV, mono, 22,05 kHz, insgesamt ca. 170 KB unter
  `composeApp/src/commonMain/composeResources/files/klaenge/`. Android und Desktop dekodieren die WAVs
  selbst (`WavDekoder`), im Web lädt und dekodiert der Browser sie über die Web Audio API.
- **Zuordnung:** `KlangRegelwerk.klangFuerPhasenwechsel` (Spielschritte) sowie Klicks auf Auswahlkarten,
  Schalter und Symbolknöpfe.

## Quellen & Lizenz

Alle Aufnahmen stammen von [Freesound.org](https://freesound.org) und stehen unter
[CC0 1.0 (gemeinfrei)](https://creativecommons.org/publicdomain/zero/1.0/). Eine Namensnennung ist
nicht erforderlich, die Urheberinnen und Urheber werden hier trotzdem dankend genannt.

| Datei | Einsatz | Original | Urheber/in | Lizenz |
|---|---|---|---|---|
| `tippen.wav` | Kurzer Klick bei Auswahl & Schaltern | [Soft UI Button Click](https://freesound.org/s/528561/) | Jummit | CC0 1.0 |
| `umblaettern.wav` | Neues Ereignis / nächster Schritt | [Page Turn 01](https://freesound.org/s/397548/) | LilMati | CC0 1.0 |
| `entscheidung.wav` | Entscheidung festgehalten | [Pencil Scribble (9)](https://freesound.org/s/761665/) | JellyDaisies | CC0 1.0 |
| `stempel.wav` | Musterungsbescheid | [traditional stamp.wav](https://freesound.org/s/470710/) | I.fekry | CC0 1.0 |
| `kapitel.wav` | Neues Kapitel (Jahr) | [Opening a book](https://freesound.org/s/614081/) | mateusboga | CC0 1.0 |
| `karte.wav` | Erklärkarte / Dialog öffnet sich | [PaperSlide.wav](https://freesound.org/s/464302/) | eyesonlegs | CC0 1.0 |
| `kapitelabschluss.wav` | Kapitelrückblick | [Typewriter ding_near_mono.wav](https://freesound.org/s/406243/) | _stubb | CC0 1.0 |
| `abschluss.wav` | Lebenslauf / Ende des Durchgangs | [bkClose.wav](https://freesound.org/s/156927/) | tia666 | CC0 1.0 |

**Bearbeitung:** Mit ffmpeg auf mono/22,05 kHz umgerechnet, Stille an Anfang und Ende entfernt, gekürzt
(höchstens 0,8 s), kurz ein- und ausgeblendet und in der Lautheit angeglichen.

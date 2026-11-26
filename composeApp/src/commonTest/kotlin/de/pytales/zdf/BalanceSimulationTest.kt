package de.pytales.zdf

import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.GameState
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.HartesEndeId
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.WertSchluessel
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull
import kotlin.test.assertNull
import kotlin.test.assertTrue

/**
 * Monte-Carlo-Balance-Simulation über alle 3 Pfade (`front`, `etappe`, `heimat`) und beide Modi
 * (`kurz`, `lang`) mit zwei Wahlstrategien (`zufall` vs. `klug`), analog zu Probe 4.
 *
 * Prüft insbesondere auch die historische Etappen-Balance (im alten Ren'Py-Stand lag
 * `etappe / lang / klug` bei 48,5 % und unterschritt damit die 60-%-Marke).
 */
class BalanceSimulationTest {

    private val content = loadTestGameContent()

    private enum class Strategie { ZUFALL, KLUG }

    private data class SimulationsBericht(
        val pfad: Pfad,
        val modus: SpielModus,
        val strategie: Strategie,
        val durchgaenge: Int,
        val erreicht1919: Int,
        val ueberlebt: Int,
        val harteEnden: Map<HartesEndeId, Int>,
        val verschiedeneAusgaenge: Set<String>,
        val durchschnittEreignisse: Double,
        val verfalleneKettenGesamt: Int,
    ) {
        val quote1919: Double get() = 100.0 * erreicht1919 / durchgaenge
        val ueberlebensQuote: Double get() = 100.0 * ueberlebt / durchgaenge
    }

    @Test
    fun reinerKalenderErreichtNiemalsEineAbbruchschwelle() {
        val engine = GameEngine(content, KotlinRandomSource(Random(1)))
        for (pfad in Pfad.entries) {
            for (herkunft in content.herkunft.herkuenfte) {
                val basis = content.konfiguration.pfade.definitionen.getValue(pfad).basisWerte
                var (werte, _) = engine.metrics.werteAnwenden(basis, herkunft.werte)
                for (kapitel in content.kapitel.kapitel) {
                    if (kapitel.jahr > 1914) {
                        val roh = engine.kapitelWirkung(kapitel.jahr, pfad)
                        val wirkung = if (kapitel.istEpilog) {
                            engine.metrics.wirkungEntschaerfen(werte, roh)
                        } else {
                            roh
                        }
                        werte = engine.metrics.werteAnwenden(werte, wirkung).first
                    }
                    val abbruch = engine.metrics.pruefeHartesEnde(werte, kapitel.jahr, content.kapitel.epilogJahr)
                    assertNull(
                        abbruch,
                        "Reiner Kalender löst $abbruch aus für $pfad / ${herkunft.id} im Jahr ${kapitel.jahr} (Werte=$werte).",
                    )
                }
            }
        }
    }

    @Test
    fun monteCarloBalanceUeberAllePfadeUndModiInklusiveEtappenBalance() {
        val durchgaengeJeLage = 1000
        val ergebnisse = mutableMapOf<Triple<Pfad, SpielModus, Strategie>, SimulationsBericht>()

        println("====================================================================================")
        println("ZWISCHEN DEN FRONTEN — MONTE-CARLO-BALANCE-SIMULATION ($durchgaengeJeLage Durchgänge je Lage)")
        println("====================================================================================")
        println("Pfad     Modus  Strategie  1919 %   Überl.%  Ø Karten  Ausgänge  Harte Enden")
        println("------------------------------------------------------------------------------------")

        for (pfad in Pfad.entries) {
            for (modus in SpielModus.entries) {
                for (strategie in Strategie.entries) {
                    val bericht = simuliere(pfad, modus, strategie, durchgaengeJeLage)
                    ergebnisse[Triple(pfad, modus, strategie)] = bericht
                    println(
                        "${pfad.code.padEnd(8)} ${modus.code.padEnd(6)} ${strategie.name.lowercase().padEnd(10)} " +
                            "${formatProzent(bericht.quote1919).padStart(6)}%  " +
                            "${formatProzent(bericht.ueberlebensQuote).padStart(6)}%  " +
                            "${formatDezimal(bericht.durchschnittEreignisse).padStart(8)}  " +
                            "${bericht.verschiedeneAusgaenge.size.toString().padStart(8)}  " +
                            "${bericht.harteEnden}"
                    )
                }
            }
        }
        println("====================================================================================")

        // Verbindliche Balance-Invarianten über alle 3 Pfade und beide Modi
        for (pfad in Pfad.entries) {
            for (modus in SpielModus.entries) {
                val zufall = ergebnisse.getValue(Triple(pfad, modus, Strategie.ZUFALL))
                val klug = ergebnisse.getValue(Triple(pfad, modus, Strategie.KLUG))

                // 1. Kein toter Pfad
                assertTrue(
                    zufall.erreicht1919 > 0 && klug.erreicht1919 > 0,
                    "Toter Pfad erkannt: $pfad/$modus",
                )

                // 2. Kluges Spielen ist stets mindestens so erfolgreich wie zufälliges Spielen
                assertTrue(
                    klug.quote1919 >= zufall.quote1919,
                    "Kluge Wahl (${klug.quote1919}%) schlägt zufällige Wahl (${zufall.quote1919}%) nicht in $pfad/$modus.",
                )

                // 3. Historische Zielgrenzen für kluge Wahl (Kurz >= 80 %, Lang >= 60 %)
                //    Prüft insbesondere auch die alte Etappen-Balance (ehemals 48,5 % in Ren'Py).
                val klugGrenze = if (modus == SpielModus.KURZ) 80.0 else 60.0
                assertTrue(
                    klug.quote1919 >= klugGrenze,
                    "Kluge Wahl in $pfad/$modus liegt bei ${klug.quote1919}% (< $klugGrenze%).",
                )

                // 4. Im langen Verlauf gibt es bei zufälliger Wahl spürbares Risiko (kein Selbstläufer mit 100 %)
                if (modus == SpielModus.LANG) {
                    assertTrue(
                        zufall.quote1919 < 98.0,
                        "Zufällige Wahl in $pfad/$modus hat kaum Risiko (${zufall.quote1919}%).",
                    )
                }

                // 5. Verschiedene Ausgänge werden erreicht (echte Lebenslauf-Vielfalt)
                assertTrue(
                    zufall.verschiedeneAusgaenge.size >= 3,
                    "Zu wenige verschiedene Ausgänge in $pfad/$modus: ${zufall.verschiedeneAusgaenge}",
                )
            }
        }
    }

    private fun simuliere(
        pfad: Pfad,
        modus: SpielModus,
        strategie: Strategie,
        durchgaenge: Int,
    ): SimulationsBericht {
        val seed = pfad.ordinal * 100_000 + modus.ordinal * 10_000 + strategie.ordinal * 1_000 + 42
        val rng = Random(seed)
        val engine = GameEngine(content, KotlinRandomSource(rng))

        var erreicht1919 = 0
        var ueberlebt = 0
        var ereignisseGesamt = 0
        var verfalleneKetten = 0
        val harteEnden = mutableMapOf<HartesEndeId, Int>()
        val ausgaenge = mutableSetOf<String>()

        val herkuenfte = content.herkunft.herkuenfte
        val alterOptionen = content.herkunft.jahrgaenge.map { it.alter }

        repeat(durchgaenge) {
            val herkunft = herkuenfte[rng.nextInt(herkuenfte.size)]
            val alter = alterOptionen[rng.nextInt(alterOptionen.size)]
            val geschlecht = when (pfad) {
                Pfad.FRONT -> Geschlecht.MAENNLICH
                Pfad.ETAPPE, Pfad.HEIMAT -> if (rng.nextBoolean()) Geschlecht.MAENNLICH else Geschlecht.WEIBLICH
            }

            var state = engine.herkunftWahlOeffnen(engine.neuesSpiel(modus = modus, direktwahlAktiv = true))
            state = engine.waehlePerson(state, herkunft.id, geschlecht, alter, direktwahlPfad = pfad)
            if (state.phase is GamePhase.ErwerbWahl) {
                val optionen = (state.phase as GamePhase.ErwerbWahl).optionen
                val erwerb = optionen[rng.nextInt(optionen.size)]
                state = engine.waehleErwerb(state, erwerb.id)
            }

            var hat1919Erreicht = false
            var sicherheitsSchritte = 0
            while (state.phase !is GamePhase.Abgeschlossen) {
                sicherheitsSchritte++
                assertTrue(sicherheitsSchritte < 200, "Endlosschleife erkannt in $pfad/$modus.")

                when (val phase = state.phase) {
                    is GamePhase.KapitelStart -> {
                        if (phase.kapitel.jahr == content.kapitel.epilogJahr) {
                            hat1919Erreicht = true
                        }
                        state = engine.starteKapitel(state)
                    }

                    is GamePhase.EreignisAnzeige -> {
                        if (!phase.istEinstieg && !phase.istFinale) {
                            ereignisseGesamt++
                        }
                        val wahl = waehleOption(engine, state, phase, strategie, rng)
                        state = engine.waehleOption(state, wahl)
                    }

                    is GamePhase.EreignisAusgang -> {
                        state = engine.weiterNachAusgang(state)
                    }

                    is GamePhase.KapitelAbschluss -> {
                        state = engine.naechstesKapitelStarten(state)
                    }

                    else -> error("Unerwartete Phase in Simulation: $phase")
                }
            }

            val abschluss = state.phase as GamePhase.Abgeschlossen
            assertEquals(4, abschluss.lebenslauf.faecher.size)
            verfalleneKetten += engine.offeneKettenVerfallen(state).size

            if (hat1919Erreicht) {
                erreicht1919++
            }
            val hart = abschluss.hartesEnde
            if (hart != null) {
                harteEnden[hart.id] = (harteEnden[hart.id] ?: 0) + 1
            } else {
                ueberlebt++
                val ausgang = assertNotNull(abschluss.lebenslauf.ausgang)
                ausgaenge.add(ausgang.id)
                assertTrue(
                    state.hatMerkmal("wirtshaus_widersprochen") || state.hatMerkmal("wirtshaus_geschwiegen"),
                    "Überlebender Durchgang muss wirtshaus_wahl abgeschlossen haben.",
                )
            }
        }

        return SimulationsBericht(
            pfad = pfad,
            modus = modus,
            strategie = strategie,
            durchgaenge = durchgaenge,
            erreicht1919 = erreicht1919,
            ueberlebt = ueberlebt,
            harteEnden = harteEnden,
            verschiedeneAusgaenge = ausgaenge,
            durchschnittEreignisse = ereignisseGesamt.toDouble() / durchgaenge,
            verfalleneKettenGesamt = verfalleneKetten,
        )
    }

    private fun waehleOption(
        engine: GameEngine,
        state: GameState,
        phase: GamePhase.EreignisAnzeige,
        strategie: Strategie,
        rng: Random,
    ): Int {
        val optionen = phase.ereignis.optionen
        if (strategie == Strategie.ZUFALL || optionen.size <= 1) {
            return rng.nextInt(optionen.size)
        }
        // „klug“ sieht nur die sichtbare Lage und die angekündigte Wirkung der Optionen
        val schwaechster: WertSchluessel = engine.metrics.schwaechsterWert(state.werte)
        val hochIstGut = content.konfiguration.werte.definitionen.getValue(schwaechster).hochIstGut
        val bewertet = optionen.mapIndexed { idx, opt ->
            val betrag = opt.wirkung[schwaechster] ?: 0
            val schaden = if (hochIstGut) -betrag else betrag
            schaden to idx
        }
        val kleinsterSchaden = bewertet.minOf { it.first }
        val beste = bewertet.filter { it.first == kleinsterSchaden }.map { it.second }
        return beste[rng.nextInt(beste.size)]
    }

    private fun formatProzent(wert: Double): String {
        val zehntel = kotlin.math.round(wert * 10.0).toInt()
        return "${zehntel / 10}.${zehntel % 10}"
    }

    private fun formatDezimal(wert: Double): String {
        val hundertstel = kotlin.math.round(wert * 100.0).toInt()
        val nachkomma = (hundertstel % 100).toString().padStart(2, '0')
        return "${hundertstel / 100}.$nachkomma"
    }
}

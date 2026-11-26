package de.pytales.zdf.engine

import de.pytales.zdf.content.GameContent
import de.pytales.zdf.model.Ereignis
import de.pytales.zdf.model.Erwerbslage
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.HartesEndeId
import de.pytales.zdf.model.MusterungsGrad
import de.pytales.zdf.model.MusterungsVermerk
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.Stimmung
import de.pytales.zdf.model.WertSchluessel

/**
 * Reine, unveränderliche Spiel-Engine für „Zwischen den Fronten“.
 *
 * Alle Zustandsübergänge nehmen einen [GameState] entgegen und liefern einen neuen [GameState].
 * Die Engine enthält keinerlei UI- oder Plattformabhängigkeiten und arbeitet mit einer
 * injizierbaren [RandomSource] für vollständig reproduzierbare Tests.
 */
class GameEngine(
    val content: GameContent,
    private val random: RandomSource = KotlinRandomSource(),
) {
    val metrics: ValueMetrics = ValueMetrics(content.konfiguration)
    val lebenslaufCalculator: LebenslaufCalculator = LebenslaufCalculator(content, metrics)

    private val konfiguration = content.konfiguration
    private val herkunftDaten = content.herkunft
    private val kapitelDaten = content.kapitel

    companion object {
        const val VERDACHT_RUHE_ZIEHUNGEN: Int = 3
        const val EREIGNIS_EINSTIEG_MELDUNG = "einstieg_meldung"
        const val EREIGNIS_EINSTIEG_OFFIZIER = "einstieg_offizier"
        const val EREIGNIS_EINSTIEG_ETAPPE = "einstieg_etappe"
        const val EREIGNIS_EINSTIEG_ABSCHIED = "einstieg_abschied"
        const val EREIGNIS_FINALE_WIRTSHAUS = "wirtshaus_wahl"

        private val ERWERB_HINWEIS_1914 = mapOf(
            "ruestung" to "1914 noch selten: Die Werke stellten Frauen erst ab 1915 in größerer Zahl ein.",
            "verwaltung" to "1914 noch selten: In den Kontoren saßen zu Kriegsbeginn fast nur Männer.",
        )
    }

    // -------------------------------------------------------------------------
    // Spielstart & gestraffter Einstieg
    // -------------------------------------------------------------------------

    fun neuesSpiel(
        modus: SpielModus = SpielModus.KURZ,
        direktwahlAktiv: Boolean = false,
    ): GameState {
        val heimatBasis = konfiguration.pfade.definitionen.getValue(Pfad.HEIMAT).basisWerte
        val startJahr = kapitelDaten.kapitel.first().jahr
        return GameState(
            phase = GamePhase.Start,
            modus = modus,
            direktwahlAktiv = direktwahlAktiv && herkunftDaten.direktwahlOption.aktiv,
            direktwahlPfad = null,
            jahr = startJahr,
            pfad = Pfad.HEIMAT,
            person = null,
            werte = heimatBasis,
            letzteAenderungen = emptyMap(),
            merkmale = emptyList(),
            gespielteEreignisse = emptyList(),
            vorgemerkteKetten = emptyList(),
            ziehungenImKapitel = 0,
            stimmungUeberschreibung = null,
            verdachtRuhig = 0,
            verdachtStand = heimatBasis[WertSchluessel.AUFMERKSAMKEIT] ?: 0,
            protokoll = emptyList(),
            einstiegKontext = EinstiegKontext.KEINER,
        )
    }

    fun herkunftWahlOeffnen(
        state: GameState,
        modus: SpielModus = state.modus,
        direktwahlAktiv: Boolean = state.direktwahlAktiv,
    ): GameState = neuesSpiel(modus = modus, direktwahlAktiv = direktwahlAktiv).copy(
        phase = GamePhase.HerkunftWahl,
    )

    /**
     * Erzeugt die Figur aus Herkunft, Geschlecht und Alter (18 oder 35).
     *
     * Ist [direktwahlPfad] gesetzt (Unterrichts-Schalter zur direkten Pfadwahl),
     * wird die Musterung übersprungen und direkt ein historisch konsistenter Start
     * auf dem gewählten Pfad (`front` / `etappe` / `heimat`) eingerichtet.
     */
    fun waehlePerson(
        state: GameState,
        herkunftId: String,
        geschlecht: Geschlecht,
        alter: Int,
        direktwahlPfad: Pfad? = null,
    ): GameState {
        val herkunft = requireNotNull(content.herkunftById[herkunftId]) {
            "Unbekannte Herkunft: '$herkunftId'"
        }
        if (direktwahlPfad != null) {
            check(herkunftDaten.direktwahlOption.aktiv) {
                "Direkte Pfadwahl ist in herkunft.json deaktiviert."
            }
        }

        val startJahr = kapitelDaten.kapitel.first().jahr
        val vornamen = herkunft.vornamen[geschlecht].orEmpty()
        val berufe = herkunft.berufe[geschlecht].orEmpty()
        val vorname = if (vornamen.isNotEmpty()) random.pickOne(vornamen) else ""
        val familienname = if (herkunft.familiennamen.isNotEmpty()) random.pickOne(herkunft.familiennamen) else ""
        val friedensberuf = if (berufe.isNotEmpty()) random.pickOne(berufe) else ""
        val (_, heeresklasse) = altersgruppe(alter)

        val person = Lebenslage(
            herkunftId = herkunft.id,
            herkunftTitel = herkunft.titel,
            geschlecht = geschlecht,
            alter = alter,
            jahrgang = startJahr - alter,
            vorname = vorname,
            familienname = familienname,
            friedensberuf = friedensberuf,
            stand = friedensberuf,
            heeresklasse = heeresklasse,
            groesseCm = random.nextIntInclusive(158, 184),
            brustumfangCm = random.nextIntInclusive(78, 96),
            pfad = Pfad.HEIMAT,
        )

        val heimatBasis = konfiguration.pfade.definitionen.getValue(Pfad.HEIMAT).basisWerte
        val (startWerte, _) = metrics.werteAnwenden(heimatBasis, herkunft.werte)

        var aktuellerStand = state.copy(
            jahr = startJahr,
            pfad = Pfad.HEIMAT,
            direktwahlPfad = direktwahlPfad,
            direktwahlAktiv = state.direktwahlAktiv || direktwahlPfad != null,
            person = person,
            werte = startWerte,
            letzteAenderungen = emptyMap(),
            verdachtStand = startWerte[WertSchluessel.AUFMERKSAMKEIT] ?: 0,
            verdachtRuhig = 0,
        )

        aktuellerStand = merkmaleHinzufuegen(aktuellerStand, herkunft.merkmale)
        if (alter >= 23) {
            aktuellerStand = merkmalHinzufuegen(aktuellerStand, "kinder")
        }
        if (alter >= 30) {
            aktuellerStand = merkmalHinzufuegen(aktuellerStand, "aeltere_kinder")
        }

        val geschlechtText = if (geschlecht == Geschlecht.MAENNLICH) "männlich" else "weiblich"
        aktuellerStand = protokollEintragen(
            aktuellerStand,
            ereignisId = "herkunft",
            wahl = "${herkunft.titel}, $geschlechtText, Jahrgang ${person.jahrgang}",
        )

        // Optionaler Unterrichts-Schalter: Pfad direkt setzen
        if (direktwahlPfad != null) {
            return direktPfadEinrichten(aktuellerStand, direktwahlPfad)
        }

        // Regulärer gestraffter Einstieg
        return if (istWehrpflichtig(geschlecht, alter)) {
            ereignisAnzeigen(
                state = aktuellerStand.copy(einstiegKontext = EinstiegKontext.MELDUNG),
                ereignisId = EREIGNIS_EINSTIEG_MELDUNG,
                istEinstieg = true,
                istFinale = false,
            )
        } else {
            val mitFamilie = familienlageSetzen(aktuellerStand)
            mitFamilie.copy(phase = GamePhase.ErwerbWahl(verfuegbareErwerbslagen(mitFamilie)))
        }
    }

    private fun direktPfadEinrichten(state: GameState, zielPfad: Pfad): GameState {
        var s = pfadWechseln(state, zielPfad)
        val person = requireNotNull(s.person)
        return when (zielPfad) {
            Pfad.FRONT -> {
                s = merkmalHinzufuegen(s, "gemustert")
                s = s.copy(
                    person = person.copy(
                        pfad = Pfad.FRONT,
                        musterung = MusterungsGrad.KV,
                        stand = "Musketier",
                    )
                )
                kapitel1914Starten(s)
            }

            Pfad.ETAPPE -> {
                if (person.geschlecht == Geschlecht.WEIBLICH) {
                    s = merkmalHinzufuegen(s, "lazarett")
                    s = s.copy(
                        person = person.copy(
                            pfad = Pfad.ETAPPE,
                            erwerbId = "lazarett",
                            stand = "Etappenlazarett",
                        )
                    )
                } else {
                    s = merkmalHinzufuegen(s, "gemustert")
                    s = s.copy(
                        person = person.copy(
                            pfad = Pfad.ETAPPE,
                            musterung = MusterungsGrad.GV,
                            stand = "Landsturmmann, Etappe",
                        )
                    )
                }
                kapitel1914Starten(s)
            }

            Pfad.HEIMAT -> {
                s = familienlageSetzen(s)
                s.copy(phase = GamePhase.ErwerbWahl(verfuegbareErwerbslagen(s)))
            }
        }
    }

    /**
     * Übernimmt das gewürfelte Musterungsergebnis und führt je nach Zielpfad weiter.
     */
    fun bestaetigeMusterung(state: GameState): GameState {
        val phase = state.phase
        require(phase is GamePhase.MusterungErgebnis) {
            "bestaetigeMusterung() erfordert Phase MusterungErgebnis, war aber $phase"
        }

        var s = pfadWechseln(state, phase.zielPfad)
        if (s.pfad == Pfad.HEIMAT) {
            s = familienlageSetzen(s)
            return s.copy(phase = GamePhase.ErwerbWahl(verfuegbareErwerbslagen(s)))
        }

        s = dienststellungSetzen(s)
        if (s.pfad == Pfad.FRONT && offizierslaufbahnOffen(s)) {
            return ereignisAnzeigen(
                state = s.copy(einstiegKontext = EinstiegKontext.OFFIZIER),
                ereignisId = EREIGNIS_EINSTIEG_OFFIZIER,
                istEinstieg = true,
                istFinale = false,
            )
        }
        return kapitel1914Starten(s)
    }

    fun verfuegbareErwerbslagen(state: GameState): List<Erwerbslage> {
        val person = state.person ?: return emptyList()
        return herkunftDaten.erwerbslagen.filter { erwerb ->
            (erwerb.nurGeschlecht == null || erwerb.nurGeschlecht == person.geschlecht) &&
                (erwerb.brauchtHerkunft.isEmpty() || person.herkunftId in erwerb.brauchtHerkunft) &&
                erwerb.verbietetMerkmal.none { state.hatMerkmal(it) }
        }.take(4)
    }

    fun erwerbHinweis(state: GameState, erwerb: Erwerbslage): Pair<String, String>? {
        val person = state.person ?: return null
        if (person.geschlecht == Geschlecht.WEIBLICH && erwerb.id in ERWERB_HINWEIS_1914) {
            return "1914 selten" to ERWERB_HINWEIS_1914.getValue(erwerb.id)
        }
        if (person.herkunftId in erwerb.hinweisFuer) {
            return "unüblich" to "In deinem Milieu ging diesen Weg fast niemand. Offen steht er trotzdem."
        }
        return null
    }

    fun waehleErwerb(state: GameState, erwerbId: String): GameState {
        require(state.phase is GamePhase.ErwerbWahl) {
            "waehleErwerb() erfordert Phase ErwerbWahl, war aber ${state.phase}"
        }
        val person = requireNotNull(state.person)
        val verfuegbar = verfuegbareErwerbslagen(state)
        val erwerb = requireNotNull(verfuegbar.firstOrNull { it.id == erwerbId }) {
            "Erwerbslage '$erwerbId' ist für diese Person nicht verfügbar."
        }

        val (neueWerte, diff) = metrics.werteAnwenden(state.werte, erwerb.werte)
        var s = state.copy(
            person = person.copy(
                erwerbId = erwerb.id,
                stand = erwerb.bezeichnung[person.geschlecht] ?: erwerb.titel,
            ),
            werte = neueWerte,
            letzteAenderungen = diff,
        )
        s = merkmaleHinzufuegen(s, erwerb.merkmale)
        s = protokollEintragen(s, ereignisId = "erwerb", wahl = erwerb.titel)

        // Im Unterrichts-Direktwahl-Modus gestrafft direkt in das Jahr 1914
        if (s.direktwahlPfad != null) {
            return kapitel1914Starten(s)
        }

        if (erwerb.etappeMoeglich) {
            return ereignisAnzeigen(
                state = s.copy(einstiegKontext = EinstiegKontext.ETAPPE),
                ereignisId = EREIGNIS_EINSTIEG_ETAPPE,
                istEinstieg = true,
                istFinale = false,
            )
        }

        return ereignisAnzeigen(
            state = s.copy(einstiegKontext = EinstiegKontext.ABSCHIED),
            ereignisId = EREIGNIS_EINSTIEG_ABSCHIED,
            istEinstieg = true,
            istFinale = false,
        )
    }

    // -------------------------------------------------------------------------
    // Kapitel- & Ereignisschleife
    // -------------------------------------------------------------------------

    fun starteKapitel(state: GameState): GameState {
        require(state.phase is GamePhase.KapitelStart) {
            "starteKapitel() erfordert Phase KapitelStart, war aber ${state.phase}"
        }
        return naechstesEreignisZiehen(state)
    }

    /**
     * Führt eine der exakt 2 Optionen (`optionIndex` 0 oder 1) des aktuell angezeigten Ereignisses aus.
     */
    fun waehleOption(state: GameState, optionIndex: Int): GameState {
        val phase = state.phase
        require(phase is GamePhase.EreignisAnzeige) {
            "waehleOption() erfordert Phase EreignisAnzeige, war aber $phase"
        }
        val ereignis = phase.ereignis
        require(optionIndex in ereignis.optionen.indices) {
            "Ungültiger Options-Index $optionIndex für Ereignis '${ereignis.id}' (erlaubt: 0..${ereignis.optionen.lastIndex})"
        }

        val option = ereignis.optionen[optionIndex]
        val effektiveWirkung = option.wirkung.toMutableMap()
        var ausgangsText = TextResolver.aufloesen(
            fassung = option.ausgang,
            jahr = state.jahr,
            pfad = state.pfad,
            merkmale = state.merkmale,
            textPrioritaet = content.merkmale.textPrioritaet,
        )
        var sprungEnde: HartesEndeId? = null
        val stimmung: Stimmung? = option.stimmung ?: ereignis.stimmung

        if (option.zufallsAusgaenge.isNotEmpty()) {
            val gezogen = random.pickWeighted(option.zufallsAusgaenge) { maxOf(1, it.gewicht) }
            for ((schluessel, betrag) in gezogen.wirkung) {
                effektiveWirkung[schluessel] = (effektiveWirkung[schluessel] ?: 0) + betrag
            }
            if (gezogen.ausgang != null) {
                ausgangsText = gezogen.ausgang
            }
            if (gezogen.sprungEnde != null) {
                sprungEnde = gezogen.sprungEnde
            }
        }

        val istNormaleZiehung = !phase.istEinstieg && !phase.istFinale
        val neueZiehungen = if (istNormaleZiehung) state.ziehungenImKapitel + 1 else state.ziehungenImKapitel
        val mitProtokoll = protokollEintragen(state, ereignisId = ereignis.id, wahl = option.titel)
            .copy(ziehungenImKapitel = neueZiehungen)

        // Sofortiger Sprung in ein hartes Ende (z. B. `ende_gefallen`) -> respektvolles Auffangnetz
        if (sprungEnde != null) {
            return mitHartemEndeAbschliessen(
                state = mitProtokoll.copy(stimmungUeberschreibung = null),
                endeId = sprungEnde,
            )
        }

        val (werteNachWahl, diffWahl) = metrics.werteAnwenden(mitProtokoll.werte, effektiveWirkung)
        var aktualisiert = mitProtokoll.copy(
            werte = werteNachWahl,
            letzteAenderungen = diffWahl,
            stimmungUeberschreibung = stimmung,
        )

        val neuVergeben = option.merkmale.filter { !aktualisiert.hatMerkmal(it) }
        aktualisiert = merkmaleHinzufuegen(aktualisiert, option.merkmale)

        val folge = option.folgeEreignis
        if (folge != null) {
            aktualisiert = aktualisiert.copy(
                vorgemerkteKetten = aktualisiert.vorgemerkteKetten + VorgemerkteKette(
                    ereignisId = folge.id,
                    abJahr = state.jahr + folge.abJahr,
                )
            )
        }

        if (istNormaleZiehung) {
            aktualisiert = verdachtVerjaehren(aktualisiert)
        }

        return aktualisiert.copy(
            phase = GamePhase.EreignisAusgang(
                ereignis = ereignis,
                gewaehlteOptionIndex = optionIndex,
                option = option,
                ausgangsText = ausgangsText,
                wertaenderungen = aktualisiert.letzteAenderungen,
                neueMerkmale = neuVergeben,
                istEinstieg = phase.istEinstieg,
                istFinale = phase.istFinale,
            )
        )
    }

    /**
     * Fährt nach Anzeige des Entscheidungs-Ausgangs fort (nächstes Ereignis, Einstiegsschritt,
     * Kapitelabschluss oder 1919-Lebenslauf).
     */
    fun weiterNachAusgang(state: GameState): GameState {
        val phase = state.phase
        require(phase is GamePhase.EreignisAusgang) {
            "weiterNachAusgang() erfordert Phase EreignisAusgang, war aber $phase"
        }

        val bereinigt = state.copy(stimmungUeberschreibung = null)

        if (phase.istFinale) {
            val lebenslauf = lebenslaufCalculator.berechneLebenslauf(bereinigt, hartesEnde = null)
            return bereinigt.copy(
                phase = GamePhase.Abgeschlossen(
                    hartesEnde = null,
                    lebenslauf = lebenslauf,
                )
            )
        }

        if (phase.istEinstieg) {
            return einstiegFortsetzen(bereinigt, phase.gewaehlteOptionIndex)
        }

        return naechstesEreignisZiehen(bereinigt)
    }

    /**
     * Wechselt nach dem Jahresabschluss-Rückblick in das nächste Kapitel, gibt wiederholbare
     * Karten frei und wendet die pfadabhängige Kapitelwirkung an.
     */
    fun naechstesKapitelStarten(state: GameState): GameState {
        require(state.phase is GamePhase.KapitelAbschluss) {
            "naechstesKapitelStarten() erfordert Phase KapitelAbschluss, war aber ${state.phase}"
        }

        val aktuellerIndex = kapitelDaten.kapitel.indexOfFirst { it.jahr == state.jahr }
        val naechstes = kapitelDaten.kapitel.getOrNull(aktuellerIndex + 1)
            ?: return wirtshausFinaleStarten(state)

        val freigegebeneGespielte = state.gespielteEreignisse.filter { id ->
            val ev = content.ereignisById[id]
            ev == null || !ev.wiederholbar
        }

        val roheWirkung = kapitelWirkung(naechstes.jahr, state.pfad)
        val wirkung = if (naechstes.istEpilog || naechstes.jahr >= kapitelDaten.epilogJahr) {
            metrics.wirkungEntschaerfen(state.werte, roheWirkung)
        } else {
            roheWirkung
        }
        val (neueWerte, effektiveWirkung) = metrics.werteAnwenden(state.werte, wirkung)

        return state.copy(
            jahr = naechstes.jahr,
            werte = neueWerte,
            letzteAenderungen = effektiveWirkung,
            gespielteEreignisse = freigegebeneGespielte,
            ziehungenImKapitel = 0,
            stimmungUeberschreibung = null,
            phase = GamePhase.KapitelStart(
                kapitel = naechstes,
                kapitelWirkung = effektiveWirkung,
            ),
        )
    }

    // -------------------------------------------------------------------------
    // Abfrage- & Diagnosefunktionen (UI + Tests)
    // -------------------------------------------------------------------------

    fun liveEmotion(state: GameState): LiveEmotionSnapshot = metrics.liveEmotion(
        werte = state.werte,
        herkunftId = state.person?.herkunftId,
        geschlecht = state.person?.geschlecht,
        ueberschreibung = state.stimmungUeberschreibung,
    )

    fun portraitId(state: GameState): String? = liveEmotion(state).portraitId

    fun werteAnzeige(state: GameState): List<WertStatus> =
        metrics.werteAnzeige(state.werte, state.letzteAenderungen)

    fun zustandssatz(state: GameState): String = metrics.zustandssatz(state.werte)

    fun altersgruppe(alter: Int): Pair<String, String> {
        val treffer = herkunftDaten.altersgruppen.firstOrNull { alter in it.von..it.bis }
        if (treffer != null) return treffer.schluessel to treffer.bezeichnung
        return if (alter < 17) {
            "landsturm_jung" to "noch nicht wehrpflichtig"
        } else {
            "landsturm_alt" to "über der Wehrpflicht"
        }
    }

    fun istWehrpflichtig(geschlecht: Geschlecht, alter: Int): Boolean =
        geschlecht == Geschlecht.MAENNLICH && alter in 17..45

    fun offizierslaufbahnOffen(state: GameState): Boolean {
        val person = state.person ?: return false
        return person.geschlecht == Geschlecht.MAENNLICH &&
            person.alter >= 19 &&
            (person.herkunftId == "adel" || person.herkunftId == "buergertum")
    }

    fun musterungVerteilung(
        herkunftId: String,
        alter: Int,
        strenge: String,
    ): Map<String, Int> {
        val (schluessel, _) = altersgruppe(alter)
        val musterung = herkunftDaten.musterung
        val basis = (musterung.grundwerte[schluessel] ?: musterung.grundwerte.getValue("aktiv"))
            .toMutableMap()
        val einfluesse = listOf(
            musterung.herkunftEinfluss[herkunftId].orEmpty(),
            musterung.strenge[strenge].orEmpty(),
        )
        for (quelle in einfluesse) {
            for ((name, betrag) in quelle) {
                basis[name] = maxOf(0, (basis[name] ?: 0) + betrag)
            }
        }
        return basis
    }

    fun musterungWuerfeln(
        herkunftId: String,
        alter: Int,
        strenge: String,
    ): MusterungErgebnisDaten {
        val verteilung = musterungVerteilung(herkunftId, alter, strenge)
        val reihenfolge = listOf("kv", "gv", "av", "du", "zurueck")
        val gesamt = reihenfolge.sumOf { verteilung[it] ?: 0 }
        val gezogen = if (gesamt <= 0) {
            "kv"
        } else {
            val wurf = random.nextIntInclusive(1, gesamt)
            var laufend = 0
            var treffer = "kv"
            for (name in reihenfolge) {
                laufend += verteilung[name] ?: 0
                if (wurf <= laufend) {
                    treffer = name
                    break
                }
            }
            treffer
        }

        val grad: MusterungsGrad
        var vermerk: MusterungsVermerk?
        if (gezogen == "zurueck") {
            grad = if (random.nextIntInclusive(1, 100) <= 70) MusterungsGrad.KV else MusterungsGrad.GV
            vermerk = MusterungsVermerk.ZURUECK
        } else {
            grad = when (gezogen) {
                "kv" -> MusterungsGrad.KV
                "gv" -> MusterungsGrad.GV
                "av" -> MusterungsGrad.AV
                else -> MusterungsGrad.DU
            }
            vermerk = null
        }

        if (vermerk == null && (grad == MusterungsGrad.KV || grad == MusterungsGrad.GV)) {
            val schwelle = herkunftDaten.musterung.ukWahrscheinlichkeit[herkunftId] ?: 12
            if (random.nextIntInclusive(1, 100) <= schwelle) {
                vermerk = MusterungsVermerk.UK
            }
        }

        val befunde = herkunftDaten.musterung.grade[grad]?.befunde.orEmpty()
        val befund = if (befunde.isNotEmpty()) random.pickOne(befunde) else "ohne Befund"
        val (_, heeresklasse) = altersgruppe(alter)

        return MusterungErgebnisDaten(
            grad = grad,
            vermerk = vermerk,
            befund = befund,
            heeresklasse = heeresklasse,
            strenge = strenge,
        )
    }

    fun pfadAusMusterung(ergebnis: MusterungErgebnisDaten): Pfad {
        if (ergebnis.vermerk == MusterungsVermerk.UK || ergebnis.vermerk == MusterungsVermerk.ZURUECK) {
            return Pfad.HEIMAT
        }
        return when (ergebnis.grad) {
            MusterungsGrad.KV -> Pfad.FRONT
            MusterungsGrad.GV -> Pfad.ETAPPE
            MusterungsGrad.AV, MusterungsGrad.DU -> Pfad.HEIMAT
        }
    }

    fun kapitelWirkung(jahr: Int, pfad: Pfad): Map<WertSchluessel, Int> {
        val kapitel = content.kapitelByJahr[jahr] ?: return emptyMap()
        val gesamt = kapitel.wirkungAllgemein.toMutableMap()
        val pfadZusatz = kapitel.wirkungNachPfad[pfad].orEmpty()
        for ((schluessel, betrag) in pfadZusatz) {
            gesamt[schluessel] = (gesamt[schluessel] ?: 0) + betrag
        }
        return gesamt.filterValues { it != 0 }
    }

    fun verfuegbareEreignisse(state: GameState): List<Ereignis> {
        val nurKern = konfiguration.modi.getValue(state.modus).nurKern
        val merkmalSet = state.merkmale.toSet()
        val gespieltSet = state.gespielteEreignisse.toSet()
        return content.ereignisse.ereignisse.filter { ev ->
            !ev.nurKette &&
                state.jahr in ev.jahre &&
                state.pfad in ev.pfade &&
                (!nurKern || ev.kern) &&
                ev.id !in gespieltSet &&
                ev.braucht.all { it in merkmalSet } &&
                ev.verbietet.none { it in merkmalSet } &&
                (ev.brauchtEines.isEmpty() || ev.brauchtEines.any { it in merkmalSet })
        }
    }

    /**
     * Liefert die noch offenen Kapitel-Träger, solange in diesem Kapitel noch KEIN erreichbarer
     * Träger gespielt wurde. Sobald einer gefallen ist, entfällt der Bogenzuschlag.
     */
    fun offeneBogenTraeger(state: GameState): Set<String> {
        val kapitel = content.kapitelByJahr[state.jahr] ?: return emptySet()
        val traeger = kapitel.bogen[state.pfad]?.traeger.orEmpty()
        if (traeger.isEmpty()) return emptySet()

        val nurKern = konfiguration.modi.getValue(state.modus).nurKern
        val erreichbar = traeger.filter { id ->
            val ev = content.ereignisById[id]
            ev != null && (!nurKern || ev.kern)
        }
        if (erreichbar.isEmpty()) return emptySet()

        val gespieltSet = state.gespielteEreignisse.toSet()
        val offen = erreichbar.filter { it !in gespieltSet }
        return if (offen.size == erreichbar.size) offen.toSet() else emptySet()
    }

    fun ereignisGewicht(state: GameState, ereignis: Ereignis): Int {
        var gewicht = ereignis.gewicht
        for ((merkmal, bonus) in ereignis.gewichtBonus) {
            if (state.hatMerkmal(merkmal)) {
                gewicht += bonus
            }
        }
        if (ereignis.id in offeneBogenTraeger(state)) {
            gewicht += kapitelDaten.bogenZuschlag
        }
        return maxOf(1, gewicht)
    }

    fun offeneKettenVerfallen(state: GameState): List<VorgemerkteKette> =
        state.vorgemerkteKetten.filter { kette ->
            val ev = content.ereignisById[kette.ereignisId]
            ev == null || ev.jahre.none { it >= state.jahr }
        }

    fun erstelleLebenslauf(
        state: GameState,
        hartesEnde: HartesEndeErgebnis? = null,
    ): LebenslaufErgebnis = lebenslaufCalculator.berechneLebenslauf(state, hartesEnde)

    // -------------------------------------------------------------------------
    // Interne Zustandsübergänge
    // -------------------------------------------------------------------------

    private fun einstiegFortsetzen(state: GameState, letzteWahl: Int): GameState {
        return when (state.einstiegKontext) {
            EinstiegKontext.MELDUNG -> {
                val person = requireNotNull(state.person)
                val strenge = if (state.hatMerkmal("kriegsfreiwillig")) "august_1914" else "einberufung"
                val ergebnis = musterungWuerfeln(person.herkunftId, person.alter, strenge)
                var s = state.copy(
                    person = person.copy(
                        musterung = ergebnis.grad,
                        vermerk = ergebnis.vermerk,
                        befund = ergebnis.befund,
                    ),
                    einstiegKontext = EinstiegKontext.KEINER,
                )
                s = merkmalHinzufuegen(s, "gemustert")
                if (ergebnis.vermerk == MusterungsVermerk.UK) {
                    s = merkmalHinzufuegen(s, "uk")
                }
                if (ergebnis.vermerk == MusterungsVermerk.ZURUECK) {
                    s = merkmalHinzufuegen(s, "zurueckgestellt")
                }
                val kurzText = buildString {
                    append(herkunftDaten.musterung.grade[ergebnis.grad]?.kurz ?: ergebnis.grad.code)
                    if (ergebnis.vermerk != null) {
                        append(", ")
                        append(herkunftDaten.musterung.vermerke[ergebnis.vermerk]?.kurz ?: ergebnis.vermerk.code)
                    }
                }
                s = protokollEintragen(s, ereignisId = "musterung", wahl = kurzText)
                val zielPfad = pfadAusMusterung(ergebnis)
                s.copy(phase = GamePhase.MusterungErgebnis(ergebnis, zielPfad))
            }

            EinstiegKontext.OFFIZIER -> {
                val s = dienststellungSetzen(state.copy(einstiegKontext = EinstiegKontext.KEINER))
                kapitel1914Starten(s)
            }

            EinstiegKontext.ETAPPE -> {
                if (letzteWahl == 0) {
                    var s = pfadWechseln(state.copy(einstiegKontext = EinstiegKontext.KEINER), Pfad.ETAPPE)
                    s = s.copy(person = s.person?.copy(stand = "Etappenlazarett"))
                    kapitel1914Starten(s)
                } else {
                    ereignisAnzeigen(
                        state = state.copy(einstiegKontext = EinstiegKontext.ABSCHIED),
                        ereignisId = EREIGNIS_EINSTIEG_ABSCHIED,
                        istEinstieg = true,
                        istFinale = false,
                    )
                }
            }

            EinstiegKontext.ABSCHIED, EinstiegKontext.KEINER -> {
                kapitel1914Starten(state.copy(einstiegKontext = EinstiegKontext.KEINER))
            }
        }
    }

    private fun kapitel1914Starten(state: GameState): GameState {
        val kapitel1914 = kapitelDaten.kapitel.first()
        return state.copy(
            jahr = kapitel1914.jahr,
            ziehungenImKapitel = 0,
            einstiegKontext = EinstiegKontext.KEINER,
            stimmungUeberschreibung = null,
            verdachtRuhig = 0,
            verdachtStand = state.werte[WertSchluessel.AUFMERKSAMKEIT] ?: 0,
            phase = GamePhase.KapitelStart(
                kapitel = kapitel1914,
                kapitelWirkung = emptyMap(),
            ),
        )
    }

    private fun naechstesEreignisZiehen(state: GameState): GameState {
        val hartesEnde = metrics.pruefeHartesEnde(state.werte, state.jahr, kapitelDaten.epilogJahr)
        if (hartesEnde != null) {
            return mitHartemEndeAbschliessen(state, hartesEnde)
        }

        val kapitel = content.kapitelByJahr.getValue(state.jahr)
        val sollZiehungen = kapitel.ziehungen[state.modus] ?: 1
        if (state.ziehungenImKapitel >= sollZiehungen) {
            return kapitelAbschliessen(state)
        }

        // 1. Fällige Entscheidungsketten haben Vorrang
        val kettenTreffer = faelligeKetteZiehen(state)
        if (kettenTreffer != null) {
            val (ereignisId, ohneKetteState) = kettenTreffer
            return ereignisAnzeigen(
                state = ohneKetteState,
                ereignisId = ereignisId,
                istEinstieg = false,
                istFinale = false,
            )
        }

        // 2. Gewichtete Ziehung aus dem verfügbaren Jahres- und Pfadvorrat
        val verfuegbar = verfuegbareEreignisse(state)
        if (verfuegbar.isEmpty()) {
            return kapitelAbschliessen(state)
        }

        val gewaehlt = random.pickWeighted(verfuegbar) { ereignisGewicht(state, it) }
        return ereignisAnzeigen(
            state = state,
            ereignisId = gewaehlt.id,
            istEinstieg = false,
            istFinale = false,
        )
    }

    private fun faelligeKetteZiehen(state: GameState): Pair<String, GameState>? {
        val gespieltSet = state.gespielteEreignisse.toSet()
        for ((index, kette) in state.vorgemerkteKetten.withIndex()) {
            if (kette.abJahr > state.jahr) continue
            val vorlage = content.ereignisById[kette.ereignisId] ?: continue
            if (kette.ereignisId in gespieltSet) continue
            if (state.pfad !in vorlage.pfade) continue
            if (state.jahr !in vorlage.jahre) continue

            val rest = state.vorgemerkteKetten.toMutableList().apply { removeAt(index) }
            return kette.ereignisId to state.copy(vorgemerkteKetten = rest)
        }
        return null
    }

    private fun ereignisAnzeigen(
        state: GameState,
        ereignisId: String,
        istEinstieg: Boolean,
        istFinale: Boolean,
    ): GameState {
        val ereignis = requireNotNull(content.ereignisById[ereignisId]) {
            "Ereignis '$ereignisId' existiert nicht in ereignisse.json."
        }
        val text = TextResolver.aufloesen(
            fassung = ereignis.text,
            jahr = state.jahr,
            pfad = state.pfad,
            merkmale = state.merkmale,
            textPrioritaet = content.merkmale.textPrioritaet,
        )
        val neueGespielte = if (ereignisId in state.gespielteEreignisse) {
            state.gespielteEreignisse
        } else {
            state.gespielteEreignisse + ereignisId
        }
        return state.copy(
            gespielteEreignisse = neueGespielte,
            stimmungUeberschreibung = ereignis.stimmung,
            phase = GamePhase.EreignisAnzeige(
                ereignis = ereignis,
                aufgeloesterText = text,
                istEinstieg = istEinstieg,
                istFinale = istFinale,
            ),
        )
    }

    private fun kapitelAbschliessen(state: GameState): GameState {
        val kapitel = content.kapitelByJahr.getValue(state.jahr)
        if (kapitel.istEpilog || state.jahr >= kapitelDaten.epilogJahr) {
            return wirtshausFinaleStarten(state)
        }
        val bogen = kapitel.bogen.getValue(state.pfad)
        return state.copy(
            stimmungUeberschreibung = null,
            phase = GamePhase.KapitelAbschluss(
                kapitel = kapitel,
                bogen = bogen,
            ),
        )
    }

    private fun wirtshausFinaleStarten(state: GameState): GameState = ereignisAnzeigen(
        state = state.copy(stimmungUeberschreibung = null),
        ereignisId = EREIGNIS_FINALE_WIRTSHAUS,
        istEinstieg = false,
        istFinale = true,
    )

    private fun mitHartemEndeAbschliessen(
        state: GameState,
        endeId: HartesEndeId,
    ): GameState {
        val textInfo = konfiguration.harteEnden.texte.getValue(endeId)
        val hartesEnde = HartesEndeErgebnis(
            id = endeId,
            titel = textInfo.titel,
            text = textInfo.text,
            jahr = state.jahr,
        )
        val bereinigt = state.copy(stimmungUeberschreibung = null)
        val lebenslauf = lebenslaufCalculator.berechneLebenslauf(bereinigt, hartesEnde = hartesEnde)
        return bereinigt.copy(
            phase = GamePhase.Abgeschlossen(
                hartesEnde = hartesEnde,
                lebenslauf = lebenslauf,
            )
        )
    }

    private fun pfadWechseln(state: GameState, neuerPfad: Pfad): GameState {
        if (state.pfad == neuerPfad) {
            return state.copy(person = state.person?.copy(pfad = neuerPfad))
        }
        val altBasis = konfiguration.pfade.definitionen.getValue(state.pfad).basisWerte
        val neuBasis = konfiguration.pfade.definitionen.getValue(neuerPfad).basisWerte
        val unterschied = konfiguration.werte.reihenfolge.associateWith { schluessel ->
            (neuBasis[schluessel] ?: 0) - (altBasis[schluessel] ?: 0)
        }
        val (neueWerte, diff) = metrics.werteAnwenden(state.werte, unterschied)
        return state.copy(
            pfad = neuerPfad,
            person = state.person?.copy(pfad = neuerPfad),
            werte = neueWerte,
            letzteAenderungen = diff,
            verdachtStand = neueWerte[WertSchluessel.AUFMERKSAMKEIT] ?: 0,
        )
    }

    private fun familienlageSetzen(state: GameState): GameState {
        val person = state.person ?: return state
        val merkmal = when {
            person.alter <= 19 -> "vater_im_feld"
            person.geschlecht == Geschlecht.WEIBLICH -> "ehemann_im_feld"
            else -> "bruder_im_feld"
        }
        return merkmalHinzufuegen(state, merkmal)
    }

    private fun dienststellungSetzen(state: GameState): GameState {
        val person = state.person ?: return state
        val neuerStand = when {
            state.pfad == Pfad.FRONT && state.hatMerkmal("offizier") -> "Offiziersaspirant"
            state.pfad == Pfad.FRONT -> "Musketier"
            state.pfad == Pfad.ETAPPE && person.musterung != null -> "Landsturmmann, Etappe"
            else -> person.stand
        }
        return state.copy(person = person.copy(stand = neuerStand))
    }

    /**
     * Verjährung des Verdachts: Wenn 3 Ziehungen lang keine neue Aufmerksamkeit dazukam,
     * sinkt `aufmerksamkeit` um 1 (sofern > 0).
     */
    private fun verdachtVerjaehren(state: GameState): GameState {
        val jetzt = state.werte[WertSchluessel.AUFMERKSAMKEIT] ?: konfiguration.werte.minimum
        if (jetzt > state.verdachtStand) {
            return state.copy(verdachtRuhig = 0, verdachtStand = jetzt)
        }

        val neueRuhe = state.verdachtRuhig + 1
        if (neueRuhe < VERDACHT_RUHE_ZIEHUNGEN) {
            return state.copy(verdachtRuhig = neueRuhe, verdachtStand = jetzt)
        }

        if (jetzt <= konfiguration.werte.minimum) {
            return state.copy(verdachtRuhig = 0, verdachtStand = jetzt)
        }

        val (nachVerjaehrung, verjaehrDiff) = metrics.werteAnwenden(
            state.werte,
            mapOf(WertSchluessel.AUFMERKSAMKEIT to -1),
        )
        val kombiniert = state.letzteAenderungen.toMutableMap()
        for ((schluessel, betrag) in verjaehrDiff) {
            val summe = (kombiniert[schluessel] ?: 0) + betrag
            if (summe == 0) {
                kombiniert.remove(schluessel)
            } else {
                kombiniert[schluessel] = summe
            }
        }
        return state.copy(
            werte = nachVerjaehrung,
            letzteAenderungen = kombiniert,
            verdachtRuhig = 0,
            verdachtStand = nachVerjaehrung[WertSchluessel.AUFMERKSAMKEIT] ?: 0,
        )
    }

    private fun merkmalHinzufuegen(state: GameState, name: String): GameState {
        if (name.isBlank() || name in state.merkmale) return state
        return state.copy(merkmale = state.merkmale + name)
    }

    private fun merkmaleHinzufuegen(state: GameState, namen: Collection<String>): GameState {
        var s = state
        for (name in namen) {
            s = merkmalHinzufuegen(s, name)
        }
        return s
    }

    private fun protokollEintragen(
        state: GameState,
        ereignisId: String,
        wahl: String,
    ): GameState = state.copy(
        protokoll = state.protokoll + ProtokollEintrag(
            jahr = state.jahr,
            ereignisId = ereignisId,
            wahl = wahl,
        )
    )
}

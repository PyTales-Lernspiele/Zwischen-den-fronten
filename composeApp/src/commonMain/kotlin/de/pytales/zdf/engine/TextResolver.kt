package de.pytales.zdf.engine

import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.TextFassung
import de.pytales.zdf.model.TextVariante

/**
 * Löst eine [TextFassung] anhand von aktuellem Jahr, Pfad, gesammelten Merkmalen
 * und der Textpriorität aus `merkmale.json` auf.
 *
 * Regelwerk (identisch zur historischen Vorlage):
 * 1. Es zählen nur Varianten, deren gesetzte Bedingungen (`pfad`, `merkmal`, `abJahr <= jahr`) erfüllt sind.
 * 2. Gibt es passende Varianten mit `abJahr`, gilt der höchste erreichte Jahresschwellenwert zuerst
 *    (z. B. überschreibt `abJahr = 1917` einen früheren 1914-Block).
 * 3. Innerhalb der gewählten Jahresstufe schlägt eine Merkmal-Variante (nach `textPrioritaet`)
 *    eine Pfad-Variante und diese eine allgemeine Jahres-Variante.
 * 4. Passt keine Variante, wird `standard` zurückgegeben.
 */
object TextResolver {

    fun aufloesen(
        fassung: TextFassung,
        jahr: Int,
        pfad: Pfad,
        merkmale: Collection<String>,
        textPrioritaet: List<String>,
    ): String {
        if (fassung.varianten.isEmpty()) return fassung.standard

        val merkmalSet = if (merkmale is Set<String>) merkmale else merkmale.toSet()
        val passend = fassung.varianten.filter { variante ->
            (variante.pfad == null || variante.pfad == pfad) &&
                (variante.merkmal == null || variante.merkmal in merkmalSet) &&
                (variante.abJahr == null || variante.abJahr <= jahr)
        }
        if (passend.isEmpty()) return fassung.standard

        val hoechstesAbJahr = passend.mapNotNull { it.abJahr }.maxOrNull()
        val stufeKandidaten = if (hoechstesAbJahr != null) {
            passend.filter { it.abJahr == hoechstesAbJahr }
        } else {
            passend
        }

        val prioIndex = textPrioritaet.withIndex().associate { (index, id) -> id to index }

        val beste: TextVariante = stufeKandidaten.minWith(
            compareBy<TextVariante>(
                { variante ->
                    when {
                        variante.merkmal != null -> 0
                        variante.pfad != null -> 1
                        else -> 2
                    }
                },
                { variante ->
                    val m = variante.merkmal
                    if (m != null) prioIndex[m] ?: Int.MAX_VALUE else Int.MAX_VALUE
                },
            )
        )

        return beste.text
    }
}

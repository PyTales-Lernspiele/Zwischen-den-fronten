package de.pytales.zdf.engine

import kotlin.random.Random

/**
 * Austauschbare Zufallsquelle für vollständig deterministische Tests und Monte-Carlo-Simulationen.
 */
interface RandomSource {
    /** Zufallszahl im halboffenen Intervall [fromInclusive, untilExclusive). */
    fun nextInt(fromInclusive: Int, untilExclusive: Int): Int

    /** Zufallszahl im geschlossenen Intervall [fromInclusive, toInclusive]. */
    fun nextIntInclusive(fromInclusive: Int, toInclusive: Int): Int {
        require(fromInclusive <= toInclusive) {
            "Ungültiges Intervall: [$fromInclusive, $toInclusive]"
        }
        return nextInt(fromInclusive, toInclusive + 1)
    }

    fun <T> pickOne(items: List<T>): T {
        require(items.isNotEmpty()) { "Auswahlliste darf nicht leer sein." }
        return items[nextInt(0, items.size)]
    }

    fun <T> pickWeighted(items: List<T>, weightOf: (T) -> Int): T {
        require(items.isNotEmpty()) { "Gewichtete Auswahlliste darf nicht leer sein." }
        val total = items.sumOf { maxOf(1, weightOf(it)) }
        val roll = nextIntInclusive(1, total)
        var running = 0
        for (item in items) {
            running += maxOf(1, weightOf(item))
            if (roll <= running) return item
        }
        return items.last()
    }
}

class KotlinRandomSource(
    private val random: Random = Random.Default,
) : RandomSource {
    override fun nextInt(fromInclusive: Int, untilExclusive: Int): Int =
        random.nextInt(fromInclusive, untilExclusive)
}

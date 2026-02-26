package com.concursoplanner.domain

import java.time.LocalDate

object SpacedRepetition {
    private val baseIntervals = listOf(1, 3, 7, 14, 30, 60, 120)

    fun intervals(reviews: Int): List<Int> {
        if (reviews <= baseIntervals.size) return baseIntervals.take(reviews)
        val expanded = baseIntervals.toMutableList()
        while (expanded.size < reviews) {
            expanded += expanded.last() * 2
        }
        return expanded
    }

    fun schedule(start: LocalDate, reviews: Int): List<LocalDate> =
        intervals(reviews).map { start.plusDays(it.toLong()) }

    fun sm2(easeFactor: Double, repetitions: Int, interval: Int, quality: Int): Triple<Double, Int, Int> {
        val (newRepetitions, newInterval) = if (quality < 3) {
            0 to 1
        } else {
            when (repetitions) {
                0 -> 1 to 1
                1 -> 2 to 6
                else -> (repetitions + 1) to (interval * easeFactor).toInt().coerceAtLeast(1)
            }
        }

        val ef = (easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))).coerceAtLeast(1.3)
        return Triple(ef, newRepetitions, newInterval)
    }
}

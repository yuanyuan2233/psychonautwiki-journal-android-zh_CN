/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 * 1:1 Kotlin port of ToleranceChartCalculator.swift by Isaak Hanimann (GNU GPL-3.0).
 * Enhanced with dual-track adaptive tolerance modeling (User subjective override + Algorithmic baseline).
 */

package com.isaakhanimann.journal.ui.tabs.stats.tolerance

import com.isaakhanimann.journal.data.room.experiences.entities.AdaptiveColor
import com.isaakhanimann.journal.data.room.experiences.entities.SubstanceCompanion
import com.isaakhanimann.journal.data.substances.repositories.SubstanceRepositoryInterface
import java.time.Instant
import java.time.ZoneId
import java.time.temporal.ChronoUnit
import kotlin.math.max

/**
 * 耐受度时序核心计算器。
 * 支持科学药代理论基准与用户主观体感自适应覆盖的双轨驱动。
 */
object ToleranceCalculator {

    fun getToleranceWindows(
        substanceAndDays: List<SubstanceAndDay>,
        substanceCompanions: List<SubstanceCompanion>,
        substanceRepo: SubstanceRepositoryInterface,
        customizations: Map<String, SubstanceToleranceCustomization> = emptyMap(),
        zoneId: ZoneId = ZoneId.systemDefault()
    ): List<ToleranceWindow> {
        val cleanedSubstanceAndDays = removeMultipleSubstancesInADay(substanceAndDays, zoneId)
        val substanceIntervals = getSubstanceIntervals(cleanedSubstanceAndDays, substanceRepo, customizations)
        val intervalsGroupedBySubstance = getSubstanceIntervalsGroupedBySubstance(substanceIntervals)
        val mergedSubstanceIntervals = getMergedSubstanceIntervals(intervalsGroupedBySubstance)
        return getToleranceWindows(mergedSubstanceIntervals, substanceCompanions, customizations)
    }

    /**
     * 过滤单日多次摄入：按天截断，同一天内摄入同种物质只保留最早的一条记录
     */
    private fun removeMultipleSubstancesInADay(
        substanceAndDays: List<SubstanceAndDay>,
        zoneId: ZoneId
    ): List<SubstanceAndDay> {
        return substanceAndDays
            .groupBy { item ->
                item.time.atZone(zoneId).toLocalDate()
            }
            .flatMap { (localDate, items) ->
                val startOfDay = localDate.atStartOfDay(zoneId).toInstant()
                items.groupBy { it.substanceName }
                    .map { (name, group) ->
                        val earliest = group.minByOrNull { it.time }?.time ?: startOfDay
                        SubstanceAndDay(name, earliest)
                    }
            }
    }

    /**
     * 根据物质耐受参数生成原始 Full 和 Half 耐受区间，融入用户主观体感自适应逻辑
     */
    private fun getSubstanceIntervals(
        substanceAndDays: List<SubstanceAndDay>,
        substanceRepo: SubstanceRepositoryInterface,
        customizations: Map<String, SubstanceToleranceCustomization>
    ): List<SubstanceInterval> {
        return substanceAndDays.flatMap { pair ->
            val substance = substanceRepo.getSubstance(pair.substanceName)
            val tolerance = substance?.tolerance
            val customization = customizations[pair.substanceName]
            val isCustomized = customization?.customFullDays != null || customization?.customZeroDays != null || customization?.manualResetInstant != null

            val result = mutableListOf<SubstanceInterval>()

            // 优先读取用户自设天数，无自设则回退至算法解析小时数
            val halfToleranceInHours = if (customization?.customFullDays != null) {
                customization.customFullDays * 24.0
            } else {
                ToleranceTimeParser.getHalfToleranceInHours(pair.substanceName, tolerance)
            }

            val zeroToleranceInHours = if (customization?.customZeroDays != null) {
                customization.customZeroDays * 24.0
            } else {
                ToleranceTimeParser.getZeroToleranceInHours(pair.substanceName, tolerance)
            }

            var startOfHalfTolerance = pair.time
            val manualReset = customization?.manualResetInstant

            // 1. 完全耐受期 Full（高亮色块）
            if (halfToleranceInHours != null && halfToleranceInHours > 0) {
                val fullSeconds = (halfToleranceInHours * 3600.0).toLong()
                var fullEnd = pair.time.plus(fullSeconds, ChronoUnit.SECONDS)

                // 若用户手动标记了提前归零且位于该区间内，自适应截断
                if (manualReset != null && manualReset.isAfter(pair.time) && manualReset.isBefore(fullEnd)) {
                    fullEnd = manualReset
                }

                if (fullEnd.isAfter(pair.time)) {
                    startOfHalfTolerance = fullEnd
                    result.add(
                        SubstanceInterval(
                            substanceName = pair.substanceName,
                            dateInterval = DateInterval(pair.time, fullEnd),
                            toleranceType = ToleranceType.FULL,
                            isUserCustomized = isCustomized
                        )
                    )
                }
            }

            // 2. 半耐受衰减期 Half（浅色过渡色块）
            if (zeroToleranceInHours != null && zeroToleranceInHours > 0) {
                val zeroSeconds = (zeroToleranceInHours * 3600.0).toLong()
                var zeroEnd = pair.time.plus(zeroSeconds, ChronoUnit.SECONDS)

                // 若用户手动标记了提前归零，自适应截断
                if (manualReset != null && manualReset.isAfter(pair.time) && manualReset.isBefore(zeroEnd)) {
                    zeroEnd = manualReset
                }

                if (zeroEnd.isAfter(startOfHalfTolerance)) {
                    result.add(
                        SubstanceInterval(
                            substanceName = pair.substanceName,
                            dateInterval = DateInterval(startOfHalfTolerance, zeroEnd),
                            toleranceType = ToleranceType.HALF,
                            isUserCustomized = isCustomized
                        )
                    )
                }
            }

            result
        }
    }

    private fun getSubstanceIntervalsGroupedBySubstance(
        substanceIntervals: List<SubstanceInterval>
    ): Map<String, List<SubstanceInterval>> {
        return substanceIntervals.groupBy { it.substanceName }
    }

    /**
     * 核心区间合并与消减算法
     */
    private fun getMergedSubstanceIntervals(
        intervalsGroupedBySubstance: Map<String, List<SubstanceInterval>>
    ): List<SubstanceInterval> {
        val groupedList = intervalsGroupedBySubstance.map { (substanceName, intervals) ->
            val hasCustomized = intervals.any { it.isUserCustomized }
            val fullIntervals = intervals.filter { it.toleranceType == ToleranceType.FULL }.map { it.dateInterval }
            val halfIntervals = intervals.filter { it.toleranceType == ToleranceType.HALF }.map { it.dateInterval }

            val mergedFull = mergeDateIntervals(fullIntervals)
            val halfWithoutFull = subtractIntervals(halfIntervals, subtracting = mergedFull)
            val mergedHalf = mergeDateIntervals(halfWithoutFull)

            val resultFull = mergedFull.map {
                SubstanceInterval(substanceName, it, ToleranceType.FULL, hasCustomized)
            }
            val resultHalf = mergedHalf.map {
                SubstanceInterval(substanceName, it, ToleranceType.HALF, hasCustomized)
            }
            resultFull + resultHalf
        }

        val sortedGroups = groupedList.sortedWith { left, right ->
            val leftEnd = left.maxOfOrNull { it.dateInterval.end } ?: Instant.MIN
            val rightEnd = right.maxOfOrNull { it.dateInterval.end } ?: Instant.MIN
            rightEnd.compareTo(leftEnd)
        }

        return sortedGroups.flatten()
    }

    fun subtractIntervals(
        intervals: List<DateInterval>,
        subtracting: List<DateInterval>
    ): List<DateInterval> {
        var currentList = intervals
        for (sub in subtracting) {
            val nextList = mutableListOf<DateInterval>()
            for (res in currentList) {
                if (!res.intersects(sub)) {
                    nextList.add(res)
                } else {
                    if (res.start.isBefore(sub.start)) {
                        nextList.add(DateInterval(res.start, sub.start))
                    }
                    if (res.end.isAfter(sub.end)) {
                        nextList.add(DateInterval(sub.end, res.end))
                    }
                }
            }
            currentList = nextList
        }
        return currentList
    }

    fun mergeDateIntervals(intervals: List<DateInterval>): List<DateInterval> {
        if (intervals.isEmpty()) return emptyList()
        val sorted = intervals.sortedBy { it.start }
        val merged = mutableListOf<DateInterval>()
        var current = sorted[0]

        for (i in 1 until sorted.size) {
            val next = sorted[i]
            if (!next.start.isAfter(current.end)) {
                val newEnd = if (next.end.isAfter(current.end)) next.end else current.end
                current = DateInterval(current.start, newEnd)
            } else {
                merged.add(current)
                current = next
            }
        }
        merged.add(current)
        return merged
    }

    private fun getToleranceWindows(
        substanceIntervals: List<SubstanceInterval>,
        substanceCompanions: List<SubstanceCompanion>,
        customizations: Map<String, SubstanceToleranceCustomization>
    ): List<ToleranceWindow> {
        val companionMap = substanceCompanions.associate { it.substanceName to it.color }
        val allColors = AdaptiveColor.values().toList()
        val usedColors = substanceCompanions.map { it.color }.toSet()
        val availableColors = allColors.filter { it !in usedColors }

        val presetColors = mapOf(
            "Psilocybin" to AdaptiveColor.PURPLE,
            "Ketamine" to AdaptiveColor.TEAL,
            "MDMA" to AdaptiveColor.HOT_PINK,
            "LSD" to AdaptiveColor.DARK_ORANGE,
            "2C-B" to AdaptiveColor.CYAN,
            "Amphetamine" to AdaptiveColor.RED,
            "Cannabis" to AdaptiveColor.LIME_GREEN,
            "DXM" to AdaptiveColor.ROYAL_BLUE,
            "Caffeine" to AdaptiveColor.GOLD,
            "Mescaline" to AdaptiveColor.CORAL
        )

        return substanceIntervals.mapIndexed { index, interval ->
            val color = companionMap[interval.substanceName]
                ?: presetColors[interval.substanceName]
                ?: availableColors.getOrNull(index % max(1, availableColors.size))
                ?: allColors[index % allColors.size]

            val custom = customizations[interval.substanceName]
            val isCustom = interval.isUserCustomized || custom != null

            ToleranceWindow(
                substanceName = interval.substanceName,
                start = interval.dateInterval.start,
                end = interval.dateInterval.end,
                toleranceType = interval.toleranceType,
                adaptiveColor = color,
                isUserCustomized = isCustom,
                customNote = if (isCustom) "用户体感自适应" else null
            )
        }
    }
}

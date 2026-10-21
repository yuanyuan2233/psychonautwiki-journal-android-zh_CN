/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 * Ported and enhanced from original iOS ToleranceChartCalculator by Isaak Hanimann (GNU GPL-3.0).
 * Enhanced with dual-track adaptive tolerance modeling (User subjective override + Algorithmic baseline).
 */

package com.isaakhanimann.journal.ui.tabs.stats.tolerance

import com.isaakhanimann.journal.data.room.experiences.entities.AdaptiveColor
import com.isaakhanimann.journal.data.room.experiences.entities.AppColor
import java.time.Instant

enum class ToleranceType {
    FULL,
    HALF
}

data class DateInterval(
    val start: Instant,
    val end: Instant
) : Comparable<DateInterval> {
    init {
        require(!end.isBefore(start)) { "DateInterval end ($end) must not be before start ($start)" }
    }

    fun intersects(other: DateInterval): Boolean {
        return !end.isBefore(other.start) && !other.end.isBefore(start)
    }

    fun contains(instant: Instant): Boolean {
        return !instant.isBefore(start) && !instant.isAfter(end)
    }

    override fun compareTo(other: DateInterval): Int {
        val startComparison = start.compareTo(other.start)
        return if (startComparison != 0) startComparison else end.compareTo(other.end)
    }
}

/**
 * 耐受度时间窗口模型。
 * isUserCustomized 标识该时间段是否融入了用户的个性化主观反馈自适应。
 */
data class ToleranceWindow(
    val substanceName: String,
    val start: Instant,
    val end: Instant,
    val toleranceType: ToleranceType,
    val adaptiveColor: AppColor,
    val isUserCustomized: Boolean = false,
    val customNote: String? = null
) {
    constructor(
        substanceName: String,
        start: Instant,
        end: Instant,
        toleranceType: ToleranceType,
        adaptiveColor: AdaptiveColor,
        isUserCustomized: Boolean = false,
        customNote: String? = null
    ) : this(
        substanceName = substanceName,
        start = start,
        end = end,
        toleranceType = toleranceType,
        adaptiveColor = AppColor(adaptiveColor),
        isUserCustomized = isUserCustomized,
        customNote = customNote
    )

    fun contains(instant: Instant): Boolean {
        return !instant.isBefore(start) && !instant.isAfter(end)
    }
}

/**
 * 用户的单次摄入记录与对应自适应元数据
 */
data class SubstanceAndDay(
    val substanceName: String,
    val time: Instant,
    val userResolvedDate: Instant? = null // 用户若标记提前恢复，记录该截断时间
)

internal data class SubstanceInterval(
    val substanceName: String,
    val dateInterval: DateInterval,
    val toleranceType: ToleranceType,
    val isUserCustomized: Boolean = false
)

/**
 * 用户对某种物质的主观耐受自适应配置
 */
data class SubstanceToleranceCustomization(
    val substanceName: String,
    val customFullDays: Double? = null,    // 用户自设的完全耐受天数 (如 2.0 天)
    val customZeroDays: Double? = null,    // 用户自设的耐受归零天数 (如 5.0 天)
    val manualResetInstant: Instant? = null // 用户一键手动标记的最近一次耐受归零时间
)

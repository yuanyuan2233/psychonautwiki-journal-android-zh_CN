/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 */

package com.isaakhanimann.journal.ui.tabs.search

import com.isaakhanimann.journal.data.substances.classes.Tolerance
import java.util.regex.Pattern

object ToleranceLocalizationHelper {
    private val ZH_TO_EN_MAP: Map<String, String> = mapOf(
        "1 - 1.5 个月" to "1-1.5 months",
        "1 - 1.5 周" to "1 - 1.5 weeks",
        "1 - 10 天" to "1 - 10 days",
        "1 - 2 周" to "1 - 2 weeks",
        "1 - 3 周" to "1 - 3 weeks",
        "1 个月" to "1 month",
        "1 周" to "1 week",
        "1 小时" to "1 hour",
        "10 - 14 天" to "10-14 days",
        "10 天" to "10 days",
        "14 天" to "14 days",
        "2 - 3 个月" to "2-3 months",
        "2 - 3 周" to "2 - 3 weeks",
        "2 - 3 天" to "2 - 3 days",
        "2 - 4 天" to "2 - 4 days",
        "2 周" to "2 weeks",
        "2 小时" to "2 hours",
        "2.5 个月" to "2.5 months",
        "21 - 30 天" to "21-30 days",
        "3 - 4 周" to "3-4 weeks",
        "3 - 5 天" to "3-5 days",
        "3 - 6 周" to "3 - 6 weeks",
        "3 - 7 天" to "3 - 7 days",
        "3 天" to "3 days",
        "4 - 7 天" to "4-7 days",
        "5 - 7 天" to "5-7 days",
        "5 天" to "5 days",
        "6 - 8 周" to "6-8 weeks",
        "6 天" to "6 days",
        "7 - 10 天" to "7-10 days",
        "7 - 14 天" to "7 - 14 days",
        "7 天" to "7 days",
        "单次服用后几乎立即产生完全耐受" to "almost immediately after ingestion",
        "反复使用后产生完全耐受" to "with repeated use",
        "反复大量使用会产生完全耐受" to "repeated and heavy usage",
        "反复给药数日内产生完全耐受" to "within a couple of days of repeated administration",
        "尚未观察到明显的耐受性形成" to "does not appear to occur",
        "摄入后几乎立即产生完全耐受" to "almost immediately after ingestion",
        "服药后几乎立即产生完全耐受" to "almost immediately after ingestion",
        "每日规律使用数周内产生完全耐受" to "within a couple of weeks of daily use",
        "每日连续使用数周内产生完全耐受" to "within a couple of weeks of daily use",
        "连续使用 3-4 天内产生完全耐受" to "within 3-4 days of continuous use",
        "连续使用一周内产生完全耐受" to "within a week of continuous use",
        "连续使用数周内产生完全耐受" to "within several weeks of continuous use",
        "连续使用数日内产生完全耐受" to "within a couple of days of continuous use",
        "连续使用数月内产生完全耐受" to "within several months of continuous use",
        "连续数日给药后产生完全耐受" to "after ingestion over the couse of multiple days",
        "长期且反复使用后逐渐产生完全耐受" to "develops with prolonged and repeated use",
        "长期使用会产生完全耐受" to "with prolonged use",
        "长期使用后产生" to "with prolonged use",
        "长期反复使用下耐受性迅速建立" to "rapidly develops with prolonged and repeated use",
        "长期反复使用会产生完全耐受" to "develops with prolonged and repeated use",
        "长期反复使用会迅速产生完全耐受" to "rapidly develops with prolonged and repeated use",
        "长期反复使用后产生" to "after prolonged and repeated usage",
        "长期反复使用后产生完全耐受" to "after prolonged and repeated usage",
        "长期反复使用后逐渐产生完全耐受" to "develops with prolonged and repeated use",
        "长期反复使用后逐渐建立完全耐受" to "develops with prolonged and repeated use",
        "长期反复使用数周内产生完全耐受" to "develops over several weeks of prolonged and repeated use",
        "长期连续使用会产生完全耐受" to "with prolonged continuous usage",
        "频繁重复使用后产生" to "after repeated and frequent usage",
    )

    private val EN_TO_ZH_MAP: Map<String, String> = ZH_TO_EN_MAP.entries.associate { (k, v) -> v to k }

    private val DAYS_REGEX_ZH = Pattern.compile("(\\d+(?:\\.\\d+)?(?:\\s*-\\s*\\d+(?:\\.\\d+)?)?)\\s*天")
    private val WEEKS_REGEX_ZH = Pattern.compile("(\\d+(?:\\.\\d+)?(?:\\s*-\\s*\\d+(?:\\.\\d+)?)?)\\s*周")
    private val MONTHS_REGEX_ZH = Pattern.compile("(\\d+(?:\\.\\d+)?(?:\\s*-\\s*\\d+(?:\\.\\d+)?)?)\\s*个?月")
    private val HOURS_REGEX_ZH = Pattern.compile("(\\d+(?:\\.\\d+)?(?:\\s*-\\s*\\d+(?:\\.\\d+)?)?)\\s*小时")

    private val DAYS_REGEX_EN = Pattern.compile("(\\d+(?:\\.\\d+)?(?:\\s*-\\s*\\d+(?:\\.\\d+)?)?)\\s*days?", Pattern.CASE_INSENSITIVE)
    private val WEEKS_REGEX_EN = Pattern.compile("(\\d+(?:\\.\\d+)?(?:\\s*-\\s*\\d+(?:\\.\\d+)?)?)\\s*weeks?", Pattern.CASE_INSENSITIVE)
    private val MONTHS_REGEX_EN = Pattern.compile("(\\d+(?:\\.\\d+)?(?:\\s*-\\s*\\d+(?:\\.\\d+)?)?)\\s*months?", Pattern.CASE_INSENSITIVE)
    private val HOURS_REGEX_EN = Pattern.compile("(\\d+(?:\\.\\d+)?(?:\\s*-\\s*\\d+(?:\\.\\d+)?)?)\\s*hours?", Pattern.CASE_INSENSITIVE)

    fun getLocalizedTolerance(tolerance: Tolerance?): Tolerance? {
        if (tolerance == null) return null
        return Tolerance(
            full = getLocalizedText(tolerance.full),
            half = getLocalizedText(tolerance.half),
            zero = getLocalizedText(tolerance.zero)
        )
    }

    fun getLocalizedText(text: String?): String? {
        if (text.isNullOrBlank()) return text
        val trimmed = text.trim()
        val isZh = SubstanceLocalizationHelper.isChinese()

        if (isZh) {
            // 中文环境：若本身含有汉字直接返回
            if (containsChinese(trimmed)) return trimmed
            // 查英文到中文映射
            EN_TO_ZH_MAP[trimmed]?.let { return it }
            // 正则匹配标准英文时间单位
            var m = DAYS_REGEX_EN.matcher(trimmed)
            if (m.matches()) return "${m.group(1)} 天"
            m = WEEKS_REGEX_EN.matcher(trimmed)
            if (m.matches()) return "${m.group(1)} 周"
            m = MONTHS_REGEX_EN.matcher(trimmed)
            if (m.matches()) return "${m.group(1)} 个月"
            m = HOURS_REGEX_EN.matcher(trimmed)
            if (m.matches()) return "${m.group(1)} 小时"
            return trimmed
        } else {
            // 英文环境：若本身不含汉字直接返回
            if (!containsChinese(trimmed)) return trimmed
            // 查中文到英文映射
            ZH_TO_EN_MAP[trimmed]?.let { return it }
            // 正则匹配标准中文时间单位
            var m = DAYS_REGEX_ZH.matcher(trimmed)
            if (m.matches()) return "${m.group(1)} days"
            m = WEEKS_REGEX_ZH.matcher(trimmed)
            if (m.matches()) return "${m.group(1)} weeks"
            m = MONTHS_REGEX_ZH.matcher(trimmed)
            if (m.matches()) return "${m.group(1)} months"
            m = HOURS_REGEX_ZH.matcher(trimmed)
            if (m.matches()) return "${m.group(1)} hours"
            return trimmed
        }
    }

    private fun containsChinese(str: String): Boolean {
        for (ch in str) {
            if (ch in '\u4e00'..'\u9fa5') return true
        }
        return false
    }
}

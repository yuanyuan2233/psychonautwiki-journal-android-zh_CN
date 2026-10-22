/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 * Ported and enhanced from iOS tolerance decoding by Isaak Hanimann (GNU GPL-3.0).
 */

package com.isaakhanimann.journal.ui.tabs.stats.tolerance

import com.isaakhanimann.journal.data.substances.classes.Tolerance
import java.util.regex.Pattern

/**
 * 负责将物质耐受数据中的自然语言文本（中文或英文）解析为精准的小时数 (Double)。
 * 同步内建 PsychonautWiki 官方标准耐受基准表，确保复杂描述或翻译文本下的高容错性。
 */
object ToleranceTimeParser {

    private val numberRangePattern = Pattern.compile("(\\d+(?:\\.\\d+)?)(?:\\s*[-~至到]\\s*(\\d+(?:\\.\\d+)?))?")

    /**
     * 官方已知经典物质的标准耐受参数表 (小时)
     * 作为快速匹配与复杂描述的兜底
     */
    private val standardToleranceHours = mapOf(
        "LSD" to Pair(72.0, 120.0), // half: 3 days, zero: 5 days
        "1P-LSD" to Pair(72.0, 120.0),
        "1B-LSD" to Pair(72.0, 120.0),
        "AL-LAD" to Pair(72.0, 120.0),
        "ETH-LAD" to Pair(72.0, 120.0),
        "Psilocybin" to Pair(72.0, 168.0), // half: 3 days, zero: 7 days
        "Psilocin" to Pair(72.0, 168.0),
        "Psilocybin mushrooms" to Pair(72.0, 168.0),
        "MDMA" to Pair(720.0, 1800.0), // half: 1 month, zero: 2.5 months
        "MDA" to Pair(720.0, 1800.0),
        "2C-B" to Pair(36.0, 72.0), // half: 1.5 days, zero: 3 days
        "2C-E" to Pair(48.0, 120.0),
        "2C-I" to Pair(48.0, 120.0),
        "Mescaline" to Pair(72.0, 168.0),
        "Ketamine" to Pair(168.0, 336.0), // 1-2 weeks
        "DXM" to Pair(168.0, 336.0),
        "DMT" to Pair(null, 1.0), // 快速复原，约 1 小时
        "Changa" to Pair(null, 2.0),
        "Amphetamine" to Pair(336.0, 720.0), // 2 weeks, 1 month
        "Methamphetamine" to Pair(336.0, 720.0),
        "Caffeine" to Pair(72.0, 168.0), // 3 days, 7 days
        "Cannabis" to Pair(168.0, 720.0) // 1 week, 1 month
    )

    /**
     * 获取指定物质的半耐受小时数 (Half Tolerance in Hours)
     */
    fun getHalfToleranceInHours(substanceName: String, tolerance: Tolerance?): Double? {
        // 1. 优先尝试解析文本
        if (tolerance != null) {
            val parsed = parseTimeToHours(tolerance.half)
            if (parsed != null && parsed > 0) {
                return parsed
            }
        }

        // 2. 查基准对照表
        standardToleranceHours[substanceName]?.first?.let { return it }

        // 3. 针对常见中文别名做二次匹配
        for ((key, pair) in standardToleranceHours) {
            if (substanceName.contains(key, ignoreCase = true) && pair.first != null) {
                return pair.first
            }
        }

        return null
    }

    /**
     * 获取指定物质的耐受归零小时数 (Zero Tolerance in Hours)
     */
    fun getZeroToleranceInHours(substanceName: String, tolerance: Tolerance?): Double? {
        // 1. 优先尝试解析文本
        if (tolerance != null) {
            val parsed = parseTimeToHours(tolerance.zero)
            if (parsed != null && parsed > 0) {
                return parsed
            }
        }

        // 2. 查基准对照表
        standardToleranceHours[substanceName]?.second?.let { return it }

        // 3. 针对常见中文别名做二次匹配
        for ((key, pair) in standardToleranceHours) {
            if (substanceName.contains(key, ignoreCase = true) && pair.second != null) {
                return pair.second
            }
        }

        return null
    }

    /**
     * 判断该物质是否属于“完全耐受缺失”（有归零期但缺少单次完全耐受脱敏期，如普瑞巴林）
     */
    fun isFullToleranceMissing(substanceName: String, tolerance: Tolerance?): Boolean {
        val zero = getZeroToleranceInHours(substanceName, tolerance)
        val half = getHalfToleranceInHours(substanceName, tolerance)
        return zero != null && half == null
    }

    /**
     * 判断该物质是否整体缺乏耐受药代数据
     */
    fun isToleranceDataMissing(substanceName: String, tolerance: Tolerance?): Boolean {
        return getZeroToleranceInHours(substanceName, tolerance) == null
    }

    /**
     * 将包含时间单位的中英文字符串转换为小时数
     * 例如："5 days" -> 120.0, "3-5 天" -> 96.0, "1 个月" -> 720.0, "2 周" -> 336.0
     */
    fun parseTimeToHours(text: String?): Double? {
        if (text.isNullOrBlank()) return null
        val lower = text.lowercase().trim()

        // 排除非时间性质描述（如 "with prolonged use", "unknown"）
        if (lower.contains("prolonged") || lower.contains("unknown") || lower.contains("长期") || lower.contains("未知")) {
            return null
        }

        val matcher = numberRangePattern.matcher(lower)
        if (!matcher.find()) return null

        val num1Str = matcher.group(1) ?: return null
        val num2Str = matcher.group(2)
        val num1 = num1Str.toDoubleOrNull() ?: return null
        val num2 = num2Str?.toDoubleOrNull()

        // 如果是范围，如 3-5 天，取平均值 4 天
        val value = if (num2 != null) (num1 + num2) / 2.0 else num1

        return when {
            lower.contains("month") || lower.contains("月") -> value * 30.0 * 24.0
            lower.contains("week") || lower.contains("周") || lower.contains("星期") -> value * 7.0 * 24.0
            lower.contains("day") || lower.contains("天") || lower.contains("日") -> value * 24.0
            lower.contains("hour") || lower.contains("小时") || lower.contains("hr") || lower.contains("h") -> value
            lower.contains("minute") || lower.contains("分") || lower.contains("min") -> value / 60.0
            else -> null
        }
    }
}

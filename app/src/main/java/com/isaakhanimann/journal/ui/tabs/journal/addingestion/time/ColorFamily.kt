/*
 * Copyright (c) 2026. PsychonautWiki Journal Contributors.
 * This file is part of PsychonautWiki Journal.
 *
 * PsychonautWiki Journal is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or (at
 * your option) any later version.
 *
 * PsychonautWiki Journal is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with PsychonautWiki Journal.  If not, see https://www.gnu.org/licenses/gpl-3.0.en.html.
 */

package com.isaakhanimann.journal.ui.tabs.journal.addingestion.time

import androidx.annotation.StringRes
import androidx.compose.ui.graphics.Color
import com.isaakhanimann.journal.R
import com.isaakhanimann.journal.data.room.experiences.entities.AdaptiveColor
import com.isaakhanimann.journal.data.room.experiences.entities.AppColor
import kotlin.math.abs
import kotlin.math.min

/**
 * 主色相与混色体系。
 * 支持 13 种主色相分类（包含冷暖色系与中性灰系），
 * 每个色系内置 100~900 标准阶梯色块及经典混合调，并支持基于 HSL 色彩模型的连续明暗微调。
 */
enum class ColorFamily(
    @StringRes val titleRes: Int,
    val baseColor: AppColor,
    val hue: Float, // 0..360 色相
    val saturation: Float, // 0..1 饱和度
    val standardShades: List<AppColor>, // 100 ~ 900 标准阶梯
    val classicShades: List<AppColor> = emptyList() // 历史经典混合色
) {
    RED(
        titleRes = R.string.journal_color_family_red,
        baseColor = AppColor("#EF4444"),
        hue = 0f,
        saturation = 0.85f,
        standardShades = listOf(
            "#FEE2E2", "#FECACA", "#FCA5A5", "#F87171", "#EF4444",
            "#DC2626", "#B91C1C", "#991B1B", "#7F1D1D"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.RED,
            AdaptiveColor.FIRE_ENGINE_RED,
            AdaptiveColor.TOMATO,
            AdaptiveColor.CINNABAR,
            AdaptiveColor.CORAL,
            AdaptiveColor.RUST,
            AdaptiveColor.MAROON
        ).map { AppColor(it) }
    ),
    ORANGE(
        titleRes = R.string.journal_color_family_orange,
        baseColor = AppColor("#F97316"),
        hue = 24f,
        saturation = 0.94f,
        standardShades = listOf(
            "#FFEDD5", "#FED7AA", "#FDBA74", "#FB923C", "#F97316",
            "#EA580C", "#C2410C", "#9A3412", "#7C2D12"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.ORANGE,
            AdaptiveColor.DARK_ORANGE,
            AdaptiveColor.ORANGE_RED,
            AdaptiveColor.AUBURN
        ).map { AppColor(it) }
    ),
    YELLOW(
        titleRes = R.string.journal_color_family_yellow,
        baseColor = AppColor("#EAB308"),
        hue = 48f,
        saturation = 0.95f,
        standardShades = listOf(
            "#FEF9C3", "#FEF08A", "#FDE047", "#FACC15", "#EAB308",
            "#CA8A04", "#A16207", "#854D0E", "#713F12"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.YELLOW,
            AdaptiveColor.GOLD,
            AdaptiveColor.DARK_GOLD,
            AdaptiveColor.BRONZE,
            AdaptiveColor.KHAKI
        ).map { AppColor(it) }
    ),
    LIME(
        titleRes = R.string.journal_color_family_lime,
        baseColor = AppColor("#84CC16"),
        hue = 84f,
        saturation = 0.80f,
        standardShades = listOf(
            "#ECFCCB", "#D9F99D", "#BEF264", "#A3E635", "#84CC16",
            "#65A30D", "#4D7C0F", "#3F6212", "#365314"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.LIME,
            AdaptiveColor.LIME_GREEN,
            AdaptiveColor.OLIVE,
            AdaptiveColor.OLIVE_DRAB,
            AdaptiveColor.DARK_OLIVE_GREEN
        ).map { AppColor(it) }
    ),
    GREEN(
        titleRes = R.string.journal_color_family_green,
        baseColor = AppColor("#22C55E"),
        hue = 142f,
        saturation = 0.72f,
        standardShades = listOf(
            "#DCFCE7", "#BBF7D0", "#86EFAC", "#4ADE80", "#22C55E",
            "#16A34A", "#15803D", "#166534", "#14532D"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.GREEN,
            AdaptiveColor.MOSS_GREEN,
            AdaptiveColor.FOREST_GREEN,
            AdaptiveColor.SEA_GREEN,
            AdaptiveColor.JUNGLE_GREEN
        ).map { AppColor(it) }
    ),
    MINT(
        titleRes = R.string.journal_color_family_mint,
        baseColor = AppColor("#14B8A6"),
        hue = 173f,
        saturation = 0.80f,
        standardShades = listOf(
            "#CCFBF1", "#99F6E4", "#5EEAD4", "#2DD4BF", "#14B8A6",
            "#0D9488", "#0F766E", "#115E59", "#134E4A"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.MINT,
            AdaptiveColor.TEAL,
            AdaptiveColor.LIGHT_SEA_GREEN,
            AdaptiveColor.DARK_TURQUOISE
        ).map { AppColor(it) }
    ),
    CYAN(
        titleRes = R.string.journal_color_family_cyan,
        baseColor = AppColor("#06B6D4"),
        hue = 192f,
        saturation = 0.90f,
        standardShades = listOf(
            "#CFFAFE", "#A5F3FC", "#67E8F9", "#22D3EE", "#06B6D4",
            "#0891B2", "#0E7490", "#155E75", "#164E63"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.CYAN,
            AdaptiveColor.DODGER_BLUE
        ).map { AppColor(it) }
    ),
    BLUE(
        titleRes = R.string.journal_color_family_blue,
        baseColor = AppColor("#3B82F6"),
        hue = 217f,
        saturation = 0.91f,
        standardShades = listOf(
            "#DBEAFE", "#BFDBFE", "#93C5FD", "#60A5FA", "#3B82F6",
            "#2563EB", "#1D4ED8", "#1E40AF", "#1E3A8A"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.BLUE,
            AdaptiveColor.ROYAL_BLUE
        ).map { AppColor(it) }
    ),
    INDIGO(
        titleRes = R.string.journal_color_family_indigo,
        baseColor = AppColor("#6366F1"),
        hue = 239f,
        saturation = 0.84f,
        standardShades = listOf(
            "#E0E7FF", "#C7D2FE", "#A5B4FC", "#818CF8", "#6366F1",
            "#4F46E5", "#4338CA", "#3730A3", "#312E81"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.INDIGO,
            AdaptiveColor.BLUE_VIOLET,
            AdaptiveColor.DEEP_LAVENDER,
            AdaptiveColor.DARK_VIOLET
        ).map { AppColor(it) }
    ),
    PURPLE(
        titleRes = R.string.journal_color_family_purple,
        baseColor = AppColor("#A855F7"),
        hue = 271f,
        saturation = 0.91f,
        standardShades = listOf(
            "#F3E8FF", "#E9D5FF", "#D8B4FE", "#C084FC", "#A855F7",
            "#9333EA", "#7E22CE", "#6B21A8", "#581C87"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.PURPLE,
            AdaptiveColor.HELIOTROPE,
            AdaptiveColor.BYZANTIUM,
            AdaptiveColor.DARK_MAGENTA
        ).map { AppColor(it) }
    ),
    PINK(
        titleRes = R.string.journal_color_family_pink,
        baseColor = AppColor("#EC4899"),
        hue = 330f,
        saturation = 0.81f,
        standardShades = listOf(
            "#FCE7F3", "#FBCFE8", "#F472B6", "#F43F5E", "#EC4899",
            "#DB2777", "#BE185D", "#9D174D", "#831843"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.PINK,
            AdaptiveColor.HOT_PINK,
            AdaptiveColor.DEEP_PINK,
            AdaptiveColor.FUCHSIA,
            AdaptiveColor.MAGENTA,
            AdaptiveColor.JAZZBERRY_JAM,
            AdaptiveColor.GRAYISH_MAGENTA
        ).map { AppColor(it) }
    ),
    BROWN(
        titleRes = R.string.journal_color_family_brown,
        baseColor = AppColor("#8C5A3C"),
        hue = 23f,
        saturation = 0.45f,
        standardShades = listOf(
            "#F5EBE6", "#EBD5CB", "#D7B4A3", "#B88B73", "#8C5A3C",
            "#70442B", "#59341F", "#452615", "#331B0E"
        ).map { AppColor(it) },
        classicShades = listOf(
            AdaptiveColor.BROWN,
            AdaptiveColor.SADDLE_BROWN
        ).map { AppColor(it) }
    ),
    GRAY(
        titleRes = R.string.journal_color_family_gray,
        baseColor = AppColor("#64748B"),
        hue = 215f,
        saturation = 0.16f,
        standardShades = listOf(
            "#F1F5F9", "#E2E8F0", "#CBD5E1", "#94A3B8", "#64748B",
            "#475569", "#334155", "#1E293B", "#0F172A"
        ).map { AppColor(it) },
        classicShades = emptyList()
    );

    val shades: List<AppColor>
        get() = standardShades + classicShades

    companion object {
        fun findFamilyOf(color: AdaptiveColor): ColorFamily? {
            return entries.firstOrNull { family ->
                family.shades.any {
                    it.adaptiveColor == color || it.rawValue.equals(color.name, ignoreCase = true)
                }
            }
        }

        fun findFamilyOf(color: AppColor): ColorFamily? {
            // 1. 精确匹配已收录的预设色阶或历史枚举
            entries.firstOrNull { family ->
                family.shades.any {
                    it.rawValue.equals(color.rawValue, ignoreCase = true) ||
                    (color.adaptiveColor != null && it.adaptiveColor == color.adaptiveColor)
                }
            }?.let { return it }

            // 2. 自定义十六进制色：基于 HSL 色相感知匹配最接近的主色族
            val composeColor = color.getComposeColor()
            val r = composeColor.red
            val g = composeColor.green
            val b = composeColor.blue

            val sat = rgbToSaturation(r, g, b)
            // 极低饱和度归入灰系
            if (sat < 0.12f) {
                return GRAY
            }

            val hue = rgbToHue(r, g, b)
            return entries.filter { it != GRAY }.minByOrNull {
                val diff = abs(it.hue - hue)
                min(diff, 360f - diff)
            } ?: BLUE
        }
    }
}

/**
 * 将 HSL (色相、饱和度、明度) 转换为 Compose Color。
 */
fun hslToColor(hue: Float, saturation: Float, lightness: Float): Color {
    val h = (hue % 360f + 360f) % 360f
    val s = saturation.coerceIn(0f, 1f)
    val l = lightness.coerceIn(0f, 1f)

    val c = (1f - abs(2f * l - 1f)) * s
    val x = c * (1f - abs((h / 60f) % 2f - 1f))
    val m = l - c / 2f

    val (r1, g1, b1) = when {
        h < 60f -> Triple(c, x, 0f)
        h < 120f -> Triple(x, c, 0f)
        h < 180f -> Triple(0f, c, x)
        h < 240f -> Triple(0f, x, c)
        h < 300f -> Triple(x, 0f, c)
        else -> Triple(c, 0f, x)
    }

    return Color(
        red = (r1 + m).coerceIn(0f, 1f),
        green = (g1 + m).coerceIn(0f, 1f),
        blue = (b1 + m).coerceIn(0f, 1f),
        alpha = 1f
    )
}

/**
 * 纯数学 RGB 转换为色相 (0..360)
 */
fun rgbToHue(r: Float, g: Float, b: Float): Float {
    val max = maxOf(r, g, b)
    val min = minOf(r, g, b)
    val delta = max - min
    if (delta == 0f) return 0f
    val hue = when (max) {
        r -> ((g - b) / delta) % 6f
        g -> ((b - r) / delta) + 2f
        else -> ((r - g) / delta) + 4f
    } * 60f
    return if (hue < 0f) hue + 360f else hue
}

/**
 * 纯数学 RGB 转换为 HSL 饱和度 (0..1)
 */
fun rgbToSaturation(r: Float, g: Float, b: Float): Float {
    val max = maxOf(r, g, b)
    val min = minOf(r, g, b)
    val l = (max + min) / 2f
    val delta = max - min
    if (delta == 0f) return 0f
    val denom = 1f - abs(2f * l - 1f)
    return if (denom <= 0f) 0f else (delta / denom).coerceIn(0f, 1f)
}

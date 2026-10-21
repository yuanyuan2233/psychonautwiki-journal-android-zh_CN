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

package com.isaakhanimann.journal.data.room.experiences.entities

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import kotlinx.serialization.KSerializer
import kotlinx.serialization.Serializable
import kotlinx.serialization.descriptors.PrimitiveKind
import kotlinx.serialization.descriptors.PrimitiveSerialDescriptor
import kotlinx.serialization.descriptors.SerialDescriptor
import kotlinx.serialization.encoding.Decoder
import kotlinx.serialization.encoding.Encoder
import java.util.Locale

/**
 * 统一颜色架构模型。
 * 替代原有硬编码的固定枚举，支持存储任意十六进制颜色（#RRGGBB / #AARRGGBB），
 * 同时 100% 透明兼容旧版 AdaptiveColor 51 种枚举名称字符串与亮暗模式自适应映射。
 */
@Serializable(with = AppColorSerializer::class)
data class AppColor(
    val rawValue: String
) {
    constructor(adaptiveColor: AdaptiveColor) : this(adaptiveColor.name)

    constructor(color: Color) : this(color.toHex())

    /**
     * 如果当前存储的值匹配旧版 AdaptiveColor 枚举名称，返回对应的枚举实例；否则返回 null
     */
    val adaptiveColor: AdaptiveColor?
        get() = try {
            AdaptiveColor.entries.firstOrNull { it.name.equals(rawValue, ignoreCase = true) }
        } catch (_: Exception) {
            null
        }

    /**
     * 是否为推荐基础主色（若来自 AdaptiveColor 则沿用其偏好，否则默认为 true）
     */
    val isPreferred: Boolean
        get() = adaptiveColor?.isPreferred ?: true

    /**
     * 获取 Compose Color：
     * 若匹配历史 AdaptiveColor，则调用其亮/暗自适应颜色；
     * 若为 Hex 格式，则解析 Hex 颜色；若解析异常，安全回退到默认蓝色。
     */
    fun getComposeColor(isDarkTheme: Boolean = false): Color {
        adaptiveColor?.let {
            return it.getComposeColor(isDarkTheme)
        }
        return parseHexColor(rawValue)
    }

    /**
     * 兼容性安全回退至 AdaptiveColor
     */
    fun toAdaptiveColor(fallback: AdaptiveColor = AdaptiveColor.BLUE): AdaptiveColor {
        return adaptiveColor ?: fallback
    }

    override fun toString(): String = rawValue

    companion object {
        fun from(value: String): AppColor = AppColor(value.trim())
        fun from(color: Color): AppColor = AppColor(color)
        fun from(adaptiveColor: AdaptiveColor): AppColor = AppColor(adaptiveColor)

        // 常用标准预设常量（与 AdaptiveColor 51 种预设同名对应）
        val RED = AppColor(AdaptiveColor.RED)
        val ORANGE = AppColor(AdaptiveColor.ORANGE)
        val YELLOW = AppColor(AdaptiveColor.YELLOW)
        val GREEN = AppColor(AdaptiveColor.GREEN)
        val MINT = AppColor(AdaptiveColor.MINT)
        val TEAL = AppColor(AdaptiveColor.TEAL)
        val CYAN = AppColor(AdaptiveColor.CYAN)
        val BLUE = AppColor(AdaptiveColor.BLUE)
        val INDIGO = AppColor(AdaptiveColor.INDIGO)
        val PURPLE = AppColor(AdaptiveColor.PURPLE)
        val PINK = AppColor(AdaptiveColor.PINK)
        val BROWN = AppColor(AdaptiveColor.BROWN)
        val LIME = AppColor(AdaptiveColor.LIME)
        val GOLD = AppColor(AdaptiveColor.GOLD)
        val CORAL = AppColor(AdaptiveColor.CORAL)
        val HOT_PINK = AppColor(AdaptiveColor.HOT_PINK)
        val ROYAL_BLUE = AppColor(AdaptiveColor.ROYAL_BLUE)
        val LIME_GREEN = AppColor(AdaptiveColor.LIME_GREEN)
        val DARK_ORANGE = AppColor(AdaptiveColor.DARK_ORANGE)
        val AUBURN = AppColor(AdaptiveColor.AUBURN)
        val OLIVE = AppColor(AdaptiveColor.OLIVE)
    }
}

/**
 * 将 Compose Color 转换为 #RRGGBB 格式十六进制字符串
 */
fun Color.toHex(includeAlpha: Boolean = false): String {
    val argb = this.toArgb()
    return if (includeAlpha) {
        String.format(Locale.ROOT, "#%08X", argb)
    } else {
        String.format(Locale.ROOT, "#%06X", 0xFFFFFF and argb)
    }
}

/**
 * 解析十六进制颜色字符串为 Compose Color，支持 #RRGGBB、#AARRGGBB、RRGGBB 等格式，
 * 解析失败时回退为 iOS 标准蓝 Color(red = 0, green = 122, blue = 255)
 */
fun parseHexColor(hexString: String): Color {
    val clean = hexString.trim().removePrefix("#")
    return try {
        when (clean.length) {
            6 -> Color((0xFF000000L or clean.toLong(16)))
            8 -> Color(clean.toLong(16))
            3 -> {
                val r = clean[0]
                val g = clean[1]
                val b = clean[2]
                Color((0xFF000000L or "$r$r$g$g$b$b".toLong(16)))
            }
            else -> Color(red = 0, green = 122, blue = 255)
        }
    } catch (_: Exception) {
        Color(red = 0, green = 122, blue = 255)
    }
}

/**
 * Kotlinx Serialization 序列化器：
 * 保证对老版本 JSON（"color": "BLUE"）与新版本 JSON（"color": "#4A90E2"）的双向无损兼容。
 */
object AppColorSerializer : KSerializer<AppColor> {
    override val descriptor: SerialDescriptor =
        PrimitiveSerialDescriptor("AppColor", PrimitiveKind.STRING)

    override fun serialize(encoder: Encoder, value: AppColor) {
        encoder.encodeString(value.rawValue)
    }

    override fun deserialize(decoder: Decoder): AppColor {
        val string = decoder.decodeString()
        return AppColor.from(string)
    }
}

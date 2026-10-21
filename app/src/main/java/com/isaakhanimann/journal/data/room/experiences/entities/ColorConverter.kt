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

import androidx.room.TypeConverter

/**
 * Room 数据库类型转换器：
 * 将 SQLite 数据库中存储的 TEXT 列值与 Kotlin AppColor 值对象进行透明转换。
 * 支持老用户 SQLite 历史枚举字符串（如 "RED", "BLUE"）与新版 Hex 字符串。
 */
class ColorConverter {
    @TypeConverter
    fun fromString(value: String?): AppColor {
        if (value.isNullOrBlank()) {
            return AppColor(AdaptiveColor.BLUE)
        }
        return AppColor.from(value)
    }

    @TypeConverter
    fun toString(color: AppColor?): String {
        return color?.rawValue ?: AdaptiveColor.BLUE.name
    }
}

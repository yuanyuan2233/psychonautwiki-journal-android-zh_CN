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
import com.isaakhanimann.journal.R
import com.isaakhanimann.journal.data.room.experiences.entities.AdaptiveColor

enum class ColorFamily(
    @StringRes val titleRes: Int,
    val baseColor: AdaptiveColor,
    val shades: List<AdaptiveColor>
) {
    RED(
        titleRes = R.string.journal_color_family_red,
        baseColor = AdaptiveColor.RED,
        shades = listOf(
            AdaptiveColor.RED,
            AdaptiveColor.FIRE_ENGINE_RED,
            AdaptiveColor.TOMATO,
            AdaptiveColor.CINNABAR,
            AdaptiveColor.CORAL,
            AdaptiveColor.RUST,
            AdaptiveColor.MAROON
        )
    ),
    ORANGE(
        titleRes = R.string.journal_color_family_orange,
        baseColor = AdaptiveColor.ORANGE,
        shades = listOf(
            AdaptiveColor.ORANGE,
            AdaptiveColor.DARK_ORANGE,
            AdaptiveColor.ORANGE_RED,
            AdaptiveColor.AUBURN
        )
    ),
    YELLOW(
        titleRes = R.string.journal_color_family_yellow,
        baseColor = AdaptiveColor.YELLOW,
        shades = listOf(
            AdaptiveColor.YELLOW,
            AdaptiveColor.GOLD,
            AdaptiveColor.DARK_GOLD,
            AdaptiveColor.BRONZE,
            AdaptiveColor.KHAKI
        )
    ),
    LIME(
        titleRes = R.string.journal_color_family_lime,
        baseColor = AdaptiveColor.LIME,
        shades = listOf(
            AdaptiveColor.LIME,
            AdaptiveColor.LIME_GREEN,
            AdaptiveColor.OLIVE,
            AdaptiveColor.OLIVE_DRAB,
            AdaptiveColor.DARK_OLIVE_GREEN
        )
    ),
    GREEN(
        titleRes = R.string.journal_color_family_green,
        baseColor = AdaptiveColor.GREEN,
        shades = listOf(
            AdaptiveColor.GREEN,
            AdaptiveColor.MOSS_GREEN,
            AdaptiveColor.FOREST_GREEN,
            AdaptiveColor.SEA_GREEN,
            AdaptiveColor.JUNGLE_GREEN
        )
    ),
    MINT(
        titleRes = R.string.journal_color_family_mint,
        baseColor = AdaptiveColor.MINT,
        shades = listOf(
            AdaptiveColor.MINT,
            AdaptiveColor.TEAL,
            AdaptiveColor.LIGHT_SEA_GREEN,
            AdaptiveColor.DARK_TURQUOISE,
            AdaptiveColor.CYAN
        )
    ),
    BLUE(
        titleRes = R.string.journal_color_family_blue,
        baseColor = AdaptiveColor.BLUE,
        shades = listOf(
            AdaptiveColor.BLUE,
            AdaptiveColor.DODGER_BLUE,
            AdaptiveColor.ROYAL_BLUE
        )
    ),
    INDIGO(
        titleRes = R.string.journal_color_family_indigo,
        baseColor = AdaptiveColor.INDIGO,
        shades = listOf(
            AdaptiveColor.INDIGO,
            AdaptiveColor.BLUE_VIOLET,
            AdaptiveColor.DEEP_LAVENDER,
            AdaptiveColor.DARK_VIOLET
        )
    ),
    PURPLE(
        titleRes = R.string.journal_color_family_purple,
        baseColor = AdaptiveColor.PURPLE,
        shades = listOf(
            AdaptiveColor.PURPLE,
            AdaptiveColor.HELIOTROPE,
            AdaptiveColor.BYZANTIUM,
            AdaptiveColor.DARK_MAGENTA
        )
    ),
    PINK(
        titleRes = R.string.journal_color_family_pink,
        baseColor = AdaptiveColor.PINK,
        shades = listOf(
            AdaptiveColor.PINK,
            AdaptiveColor.HOT_PINK,
            AdaptiveColor.DEEP_PINK,
            AdaptiveColor.FUCHSIA,
            AdaptiveColor.MAGENTA,
            AdaptiveColor.JAZZBERRY_JAM,
            AdaptiveColor.GRAYISH_MAGENTA
        )
    ),
    BROWN(
        titleRes = R.string.journal_color_family_brown,
        baseColor = AdaptiveColor.BROWN,
        shades = listOf(
            AdaptiveColor.BROWN,
            AdaptiveColor.SADDLE_BROWN
        )
    );

    companion object {
        fun findFamilyOf(color: AdaptiveColor): ColorFamily? {
            return entries.firstOrNull { it.shades.contains(color) }
        }
    }
}

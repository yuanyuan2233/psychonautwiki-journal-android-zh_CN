/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 */

package com.isaakhanimann.journal.ui.tabs.settings

import androidx.annotation.StringRes
import com.isaakhanimann.journal.R
import java.util.Locale

enum class AppLanguage(val code: String, @StringRes val labelRes: Int) {
    FOLLOW_SYSTEM("system", R.string.settings_language_system),
    CHINESE("zh", R.string.settings_language_chinese),
    ENGLISH("en", R.string.settings_language_english);

    fun toLocale(): Locale? {
        return when (this) {
            FOLLOW_SYSTEM -> null
            CHINESE -> Locale.SIMPLIFIED_CHINESE
            ENGLISH -> Locale.ENGLISH
        }
    }

    companion object {
        fun fromCode(code: String?): AppLanguage {
            return entries.firstOrNull { it.code.equals(code, ignoreCase = true) } ?: FOLLOW_SYSTEM
        }
    }
}

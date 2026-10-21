/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 */

package com.isaakhanimann.journal.ui.tabs.search

import com.isaakhanimann.journal.data.substances.classes.Tolerance
import org.junit.Assert.assertEquals
import org.junit.Test
import java.util.Locale

class ToleranceLocalizationHelperTest {

    @Test
    fun testToleranceLocalizationEnglish() {
        val originalLocale = Locale.getDefault()
        try {
            Locale.setDefault(Locale.US)

            assertEquals(
                "almost immediately after ingestion",
                ToleranceLocalizationHelper.getLocalizedText("服药后几乎立即产生完全耐受")
            )
            assertEquals("5-7 days", ToleranceLocalizationHelper.getLocalizedText("5 - 7 天"))
            assertEquals("14 days", ToleranceLocalizationHelper.getLocalizedText("14 天"))
            assertEquals("1 week", ToleranceLocalizationHelper.getLocalizedText("1 周"))
            assertEquals("2-3 months", ToleranceLocalizationHelper.getLocalizedText("2 - 3 个月"))
            assertEquals("does not appear to occur", ToleranceLocalizationHelper.getLocalizedText("尚未观察到明显的耐受性形成"))
            
            // Regex fallback test
            assertEquals("99 days", ToleranceLocalizationHelper.getLocalizedText("99 天"))
            assertEquals("4.5 weeks", ToleranceLocalizationHelper.getLocalizedText("4.5 周"))

            // Tolerance object mapping
            val tolZh = Tolerance(
                full = "服药后几乎立即产生完全耐受",
                half = "5 - 7 天",
                zero = "14 天"
            )
            val tolEn = ToleranceLocalizationHelper.getLocalizedTolerance(tolZh)
            assertEquals("almost immediately after ingestion", tolEn?.full)
            assertEquals("5-7 days", tolEn?.half)
            assertEquals("14 days", tolEn?.zero)
        } finally {
            Locale.setDefault(originalLocale)
        }
    }

    @Test
    fun testToleranceLocalizationChinese() {
        val originalLocale = Locale.getDefault()
        try {
            Locale.setDefault(Locale.SIMPLIFIED_CHINESE)

            assertEquals("14 天", ToleranceLocalizationHelper.getLocalizedText("14 天"))
            assertEquals("5 - 7 天", ToleranceLocalizationHelper.getLocalizedText("5-7 days"))
            assertEquals("服药后几乎立即产生完全耐受", ToleranceLocalizationHelper.getLocalizedText("almost immediately after ingestion"))
            assertEquals("99 天", ToleranceLocalizationHelper.getLocalizedText("99 days"))

            val tol = Tolerance(
                full = "服药后几乎立即产生完全耐受",
                half = "5 - 7 天",
                zero = "14 天"
            )
            val tolZh = ToleranceLocalizationHelper.getLocalizedTolerance(tol)
            assertEquals("服药后几乎立即产生完全耐受", tolZh?.full)
            assertEquals("5 - 7 天", tolZh?.half)
            assertEquals("14 天", tolZh?.zero)
        } finally {
            Locale.setDefault(originalLocale)
        }
    }
}

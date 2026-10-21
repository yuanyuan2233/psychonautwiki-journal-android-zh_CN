/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 */

package com.isaakhanimann.journal.ui.tabs.stats.tolerance

import com.isaakhanimann.journal.data.substances.classes.Category
import com.isaakhanimann.journal.data.substances.classes.Substance
import com.isaakhanimann.journal.data.substances.classes.SubstanceWithCategories
import com.isaakhanimann.journal.data.substances.classes.Tolerance
import com.isaakhanimann.journal.data.substances.repositories.SubstanceRepositoryInterface
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.time.Instant
import java.time.temporal.ChronoUnit

class ToleranceCalculatorTest {

    @Test
    fun testToleranceTimeParser() {
        assertEquals(120.0, ToleranceTimeParser.parseTimeToHours("5 days")!!, 0.01)
        assertEquals(120.0, ToleranceTimeParser.parseTimeToHours("5 天")!!, 0.01)
        assertEquals(720.0, ToleranceTimeParser.parseTimeToHours("1 month")!!, 0.01)
        assertEquals(720.0, ToleranceTimeParser.parseTimeToHours("1 个月")!!, 0.01)
        assertEquals(336.0, ToleranceTimeParser.parseTimeToHours("2 weeks")!!, 0.01)
        assertEquals(336.0, ToleranceTimeParser.parseTimeToHours("2 周")!!, 0.01)
        assertEquals(96.0, ToleranceTimeParser.parseTimeToHours("3-5 天")!!, 0.01)
        
        // 经典物质兜底对照测试
        assertEquals(120.0, ToleranceTimeParser.getZeroToleranceInHours("LSD", null)!!, 0.01)
        assertEquals(72.0, ToleranceTimeParser.getHalfToleranceInHours("Psilocybin", null)!!, 0.01)
        assertEquals(1800.0, ToleranceTimeParser.getZeroToleranceInHours("MDMA", null)!!, 0.01)
    }

    @Test
    fun testSubtractIntervals() {
        val now = Instant.now()
        val t0 = now
        val t1 = now.plus(1, ChronoUnit.HOURS)
        val t2 = now.plus(2, ChronoUnit.HOURS)
        val t3 = now.plus(3, ChronoUnit.HOURS)
        val t4 = now.plus(4, ChronoUnit.HOURS)

        // 目标区间 [t0, t4]，扣减 [t1, t3] -> 应该分裂为 [t0, t1] 和 [t3, t4]
        val target = listOf(DateInterval(t0, t4))
        val subtracting = listOf(DateInterval(t1, t3))

        val result = ToleranceCalculator.subtractIntervals(target, subtracting)
        assertEquals(2, result.size)
        assertEquals(t0, result[0].start)
        assertEquals(t1, result[0].end)
        assertEquals(t3, result[1].start)
        assertEquals(t4, result[1].end)
    }

    @Test
    fun testMergeDateIntervals() {
        val now = Instant.now()
        val t0 = now
        val t1 = now.plus(1, ChronoUnit.HOURS)
        val t2 = now.plus(2, ChronoUnit.HOURS)
        val t3 = now.plus(3, ChronoUnit.HOURS)

        // [t0, t2] 与 [t1, t3] 有交叠，合并后应为 [t0, t3]
        val intervals = listOf(
            DateInterval(t0, t2),
            DateInterval(t1, t3)
        )
        val merged = ToleranceCalculator.mergeDateIntervals(intervals)
        assertEquals(1, merged.size)
        assertEquals(t0, merged[0].start)
        assertEquals(t3, merged[0].end)
    }

    @Test
    fun testGetToleranceWindowsEndToEnd() {
        val now = Instant.now()
        val fakeRepo = object : SubstanceRepositoryInterface {
            override fun getAllSubstances(): List<Substance> = emptyList()
            override fun getAllSubstancesWithCategories(): List<SubstanceWithCategories> = emptyList()
            override fun getAllCategories(): List<Category> = emptyList()
            override fun getCategory(categoryName: String): Category? = null
            override fun getSubstanceWithCategories(substanceName: String): SubstanceWithCategories? = null
            override fun getSubstance(substanceName: String): Substance? {
                if (substanceName == "Psilocybin") {
                    return Substance(
                        name = "Psilocybin",
                        commonNames = listOf("裸盖菇素"),
                        url = "https://psychonautwiki.org/wiki/Psilocybin",
                        isApproved = true,
                        tolerance = Tolerance(
                            full = "almost immediately after ingestion",
                            half = "3 days",
                            zero = "7 days"
                        ),
                        crossTolerances = listOf("psychedelics"),
                        addictionPotential = "not habit-forming",
                        toxicities = emptyList(),
                        categories = listOf("psychedelic"),
                        roas = emptyList()
                    )
                }
                return null
            }
        }

        val ingestions = listOf(
            SubstanceAndDay("Psilocybin", now.minus(5, ChronoUnit.DAYS))
        )

        val windows = ToleranceCalculator.getToleranceWindows(
            substanceAndDays = ingestions,
            substanceCompanions = emptyList(),
            substanceRepo = fakeRepo
        )

        // 应该产生 FULL 和 HALF 两个窗口
        assertTrue("Windows should not be empty", windows.isNotEmpty())
        val fullWindow = windows.find { it.toleranceType == ToleranceType.FULL }
        val halfWindow = windows.find { it.toleranceType == ToleranceType.HALF }

        assertNotNull("Should have Full tolerance window", fullWindow)
        assertNotNull("Should have Half tolerance window", halfWindow)
        assertEquals(fullWindow!!.end, halfWindow!!.start)
    }
}

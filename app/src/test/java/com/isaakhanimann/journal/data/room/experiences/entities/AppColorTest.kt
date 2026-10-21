/*
 * Copyright (c) 2026. PsychonautWiki Journal Contributors.
 * This file is part of PsychonautWiki Journal.
 */

package com.isaakhanimann.journal.data.room.experiences.entities

import androidx.compose.ui.graphics.Color
import com.isaakhanimann.journal.ui.tabs.settings.TimedNoteSerializable
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Test
import java.time.Instant

class AppColorTest {

    private val json = Json { ignoreUnknownKeys = true }

    @Test
    fun testLegacyEnumCompatibility() {
        val colorBlue = AppColor.from("BLUE")
        assertEquals(AdaptiveColor.BLUE, colorBlue.adaptiveColor)
        assertEquals("BLUE", colorBlue.rawValue)
        assertEquals(AdaptiveColor.BLUE.getComposeColor(false), colorBlue.getComposeColor(false))
        assertEquals(AdaptiveColor.BLUE.getComposeColor(true), colorBlue.getComposeColor(true))

        val colorHotPink = AppColor.from("HOT_PINK")
        assertEquals(AdaptiveColor.HOT_PINK, colorHotPink.adaptiveColor)
    }

    @Test
    fun testHexColorParsing() {
        val redHex = AppColor.from("#FF0000")
        assertNull(redHex.adaptiveColor)
        assertEquals("#FF0000", redHex.rawValue)
        val composeColor = redHex.getComposeColor()
        assertEquals(1f, composeColor.red, 0.01f)
        assertEquals(0f, composeColor.green, 0.01f)
        assertEquals(0f, composeColor.blue, 0.01f)

        // 简写 hex
        val shortHex = AppColor.from("#FFF")
        assertEquals(1f, shortHex.getComposeColor().red, 0.01f)
        assertEquals(1f, shortHex.getComposeColor().green, 0.01f)
        assertEquals(1f, shortHex.getComposeColor().blue, 0.01f)
    }

    @Test
    fun testRoomColorConverter() {
        val converter = ColorConverter()

        // 历史数据转换验证
        val fromLegacy = converter.fromString("AUBURN")
        assertEquals(AdaptiveColor.AUBURN, fromLegacy.adaptiveColor)
        assertEquals("AUBURN", converter.toString(fromLegacy))

        // 新 Hex 数据转换验证
        val fromHex = converter.fromString("#4A90E2")
        assertEquals("#4A90E2", fromHex.rawValue)
        assertEquals("#4A90E2", converter.toString(fromHex))

        // 空值安全回退
        val fromNull = converter.fromString(null)
        assertEquals(AdaptiveColor.BLUE, fromNull.adaptiveColor)
    }

    @Test
    fun testJsonSerializationAndLegacyImport() {
        // 1. 测试 AppColor 原生序列化 / 反序列化
        val encodedLegacy = json.encodeToString(AppColor(AdaptiveColor.PURPLE))
        assertEquals("\"PURPLE\"", encodedLegacy)
        val decodedLegacy = json.decodeFromString<AppColor>(encodedLegacy)
        assertEquals(AdaptiveColor.PURPLE, decodedLegacy.adaptiveColor)

        val customHex = AppColor("#336699")
        val encodedHex = json.encodeToString(customHex)
        assertEquals("\"#336699\"", encodedHex)
        val decodedHex = json.decodeFromString<AppColor>(encodedHex)
        assertEquals("#336699", decodedHex.rawValue)

        // 2. 模拟老版本导出的 SubstanceCompanion JSON 备份反序列化
        val oldSubstanceCompanionJson = """{"substanceName":"LSD","color":"DARK_ORANGE"}"""
        val companion = json.decodeFromString<SubstanceCompanion>(oldSubstanceCompanionJson)
        assertEquals("LSD", companion.substanceName)
        assertEquals(AdaptiveColor.DARK_ORANGE, companion.color.adaptiveColor)

        // 3. 模拟老版本导出的 TimedNote 备份反序列化
        val now = Instant.now()
        val oldTimedNoteJson = """
            {
                "creationDate": ${now.epochSecond},
                "time": ${now.epochSecond},
                "note": "老用户历史笔记",
                "color": "MINT",
                "isPartOfTimeline": true
            }
        """.trimIndent()
        val timedNote = json.decodeFromString<TimedNoteSerializable>(oldTimedNoteJson)
        assertEquals("老用户历史笔记", timedNote.note)
        assertEquals(AdaptiveColor.MINT, timedNote.color.adaptiveColor)
    }
}

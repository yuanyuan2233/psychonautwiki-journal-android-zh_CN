/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 */

package com.isaakhanimann.journal.ui.tabs.stats.tolerance

import android.content.Context
import android.content.SharedPreferences
import dagger.hilt.android.qualifiers.ApplicationContext
import org.json.JSONObject
import java.time.Instant
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 用户主观耐受自适应设置的轻量持久化存储。
 * 采用独立 SharedPreferences 隔离存储，零侵入现有 Room 数据库，避免多分支合并产生数据迁移冲突。
 */
@Singleton
class ToleranceCustomizationStore @Inject constructor(
    @ApplicationContext context: Context
) {
    private val prefs: SharedPreferences = context.getSharedPreferences("tolerance_customization_prefs", Context.MODE_PRIVATE)

    /**
     * 获取指定物质的用户自定义耐受配置
     */
    fun getCustomization(substanceName: String): SubstanceToleranceCustomization? {
        val raw = prefs.getString(getKey(substanceName), null) ?: return null
        return try {
            val json = JSONObject(raw)
            val fullDays = if (json.has("fullDays")) json.getDouble("fullDays") else null
            val zeroDays = if (json.has("zeroDays")) json.getDouble("zeroDays") else null
            val resetEpoch = if (json.has("manualResetEpoch")) json.getLong("manualResetEpoch") else null
            val resetInstant = resetEpoch?.let { Instant.ofEpochMilli(it) }

            SubstanceToleranceCustomization(
                substanceName = substanceName,
                customFullDays = fullDays,
                customZeroDays = zeroDays,
                manualResetInstant = resetInstant
            )
        } catch (e: Exception) {
            null
        }
    }

    /**
     * 保存指定物质的用户自定义耐受配置
     */
    fun saveCustomization(customization: SubstanceToleranceCustomization) {
        val json = JSONObject().apply {
            customization.customFullDays?.let { put("fullDays", it) }
            customization.customZeroDays?.let { put("zeroDays", it) }
            customization.manualResetInstant?.let { put("manualResetEpoch", it.toEpochMilli()) }
        }
        prefs.edit().putString(getKey(customization.substanceName), json.toString()).apply()
    }

    /**
     * 清除指定物质的个性化覆盖，恢复系统默认药代理论模型
     */
    fun resetToDefault(substanceName: String) {
        prefs.edit().remove(getKey(substanceName)).apply()
    }

    /**
     * 获取所有已个性化配置的物质映射
     */
    fun getAllCustomizations(): Map<String, SubstanceToleranceCustomization> {
        val result = mutableMapOf<String, SubstanceToleranceCustomization>()
        for ((key, value) in prefs.all) {
            if (key.startsWith(PREFIX) && value is String) {
                val substanceName = key.removePrefix(PREFIX)
                getCustomization(substanceName)?.let {
                    result[substanceName] = it
                }
            }
        }
        return result
    }

    private fun getKey(substanceName: String): String = "$PREFIX$substanceName"

    companion object {
        private const val PREFIX = "custom_tol_"
    }
}

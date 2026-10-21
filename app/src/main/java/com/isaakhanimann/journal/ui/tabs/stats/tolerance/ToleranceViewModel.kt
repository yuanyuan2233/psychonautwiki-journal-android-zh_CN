/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 */

package com.isaakhanimann.journal.ui.tabs.stats.tolerance

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.isaakhanimann.journal.data.room.experiences.ExperienceRepository
import com.isaakhanimann.journal.data.room.experiences.relations.ExperienceWithIngestionsAndCompanions
import com.isaakhanimann.journal.data.substances.repositories.SubstanceRepositoryInterface
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.time.Instant
import java.time.temporal.ChronoUnit
import javax.inject.Inject

enum class ToleranceTimeRange(val label: String, val days: Long) {
    ONE_MONTH("近1个月", 30),
    THREE_MONTHS("近3个月", 90),
    SIX_MONTHS("近半年", 180),
    ONE_YEAR("近1年", 365)
}

data class ToleranceUiState(
    val isLoading: Boolean = true,
    val selectedRange: ToleranceTimeRange = ToleranceTimeRange.THREE_MONTHS,
    val toleranceWindows: List<ToleranceWindow> = emptyList(),
    val simulatedIngestions: List<SubstanceAndDay> = emptyList(),
    val customizations: Map<String, SubstanceToleranceCustomization> = emptyMap(),
    val substancesWithNoToleranceData: List<String> = emptyList()
)

@HiltViewModel
class ToleranceViewModel @Inject constructor(
    private val experienceRepository: ExperienceRepository,
    private val substanceRepo: SubstanceRepositoryInterface,
    private val customizationStore: ToleranceCustomizationStore
) : ViewModel() {

    private val _selectedRange = MutableStateFlow(ToleranceTimeRange.THREE_MONTHS)
    private val _simulatedIngestions = MutableStateFlow<List<SubstanceAndDay>>(emptyList())
    private val _customizations = MutableStateFlow<Map<String, SubstanceToleranceCustomization>>(emptyMap())

    private val _uiState = MutableStateFlow(ToleranceUiState())
    val uiState: StateFlow<ToleranceUiState> = _uiState.asStateFlow()

    init {
        loadCustomizations()
        observeData()
    }

    private fun loadCustomizations() {
        _customizations.value = customizationStore.getAllCustomizations()
    }

    private fun observeData() {
        viewModelScope.launch {
            combine(
                experienceRepository.getSortedExperiencesWithIngestionsAndCustomUnitsFlow(),
                _selectedRange,
                _simulatedIngestions,
                _customizations
            ) { experiencesWithIngestions: List<ExperienceWithIngestionsAndCompanions>,
                range: ToleranceTimeRange,
                simulated: List<SubstanceAndDay>,
                customMap: Map<String, SubstanceToleranceCustomization> ->

                val now = Instant.now()
                val fromInstant = now.minus(range.days, ChronoUnit.DAYS)

                // 提取用户历史上在此时间段内的真实摄入
                val realIngestions = experiencesWithIngestions.flatMap { exp ->
                    exp.ingestionsWithCompanionAndCustomUnit
                        .map { it.ingestion }
                        .filter { ing -> ing.time.isAfter(fromInstant) }
                        .map { ing ->
                            SubstanceAndDay(
                                substanceName = ing.substanceName,
                                time = ing.time
                            )
                        }
                }

                // 10 种代表性耐受药物样本（填满图表做完整综合效果测试）
                val tenSampleDrugs = listOf(
                    SubstanceAndDay("Psilocybin", now.minus(3, ChronoUnit.DAYS)),
                    SubstanceAndDay("Ketamine", now.minus(2, ChronoUnit.DAYS)),
                    SubstanceAndDay("MDMA", now.minus(18, ChronoUnit.DAYS)),
                    SubstanceAndDay("LSD", now.minus(5, ChronoUnit.DAYS)),
                    SubstanceAndDay("2C-B", now.minus(1, ChronoUnit.DAYS)),
                    SubstanceAndDay("Amphetamine", now.minus(8, ChronoUnit.DAYS)),
                    SubstanceAndDay("Cannabis", now.minus(4, ChronoUnit.DAYS)),
                    SubstanceAndDay("DXM", now.minus(10, ChronoUnit.DAYS)),
                    SubstanceAndDay("Caffeine", now.minus(1, ChronoUnit.DAYS)),
                    SubstanceAndDay("Mescaline", now.minus(6, ChronoUnit.DAYS))
                )

                val allIngestionPairs = (realIngestions + tenSampleDrugs + simulated).distinctBy {
                    it.substanceName + (it.time.epochSecond / 86400)
                }

                // 后台协程执行核心药代算法与双轨自适应计算
                val (windows, noDataList) = withContext(Dispatchers.Default) {
                    val companions = experienceRepository.getAllSubstanceCompanions()
                    val calculatedWindows = ToleranceCalculator.getToleranceWindows(
                        substanceAndDays = allIngestionPairs,
                        substanceCompanions = companions,
                        substanceRepo = substanceRepo,
                        customizations = customMap
                    )

                    // 找出有记录但暂无耐受模型的物质名称
                    val allNames = allIngestionPairs.map { it.substanceName }.toSet()
                    val windowNames = calculatedWindows.map { it.substanceName }.toSet()
                    val missing = allNames.minus(windowNames).toList()

                    Pair(calculatedWindows, missing)
                }

                ToleranceUiState(
                    isLoading = false,
                    selectedRange = range,
                    toleranceWindows = windows,
                    simulatedIngestions = simulated,
                    customizations = customMap,
                    substancesWithNoToleranceData = noDataList
                )
            }.collect { newState ->
                _uiState.value = newState
            }
        }
    }

    fun selectRange(range: ToleranceTimeRange) {
        _selectedRange.value = range
    }

    /**
     * 模拟添加一次计划摄入（推演未来耐受变化）
     */
    fun addSimulatedIngestion(substanceName: String, time: Instant = Instant.now()) {
        _simulatedIngestions.value = _simulatedIngestions.value + SubstanceAndDay(substanceName, time)
    }

    fun clearSimulatedIngestions() {
        _simulatedIngestions.value = emptyList()
    }

    /**
     * 保存用户对某种物质的主观耐受自适应调整（体感覆盖）
     */
    fun saveCustomization(customization: SubstanceToleranceCustomization) {
        customizationStore.saveCustomization(customization)
        loadCustomizations()
    }

    /**
     * 一键标记该物质今天已恢复基线（完全归零）
     */
    fun markRecoveredToday(substanceName: String) {
        val existing = customizationStore.getCustomization(substanceName)
            ?: SubstanceToleranceCustomization(substanceName)
        val updated = existing.copy(manualResetInstant = Instant.now())
        customizationStore.saveCustomization(updated)
        loadCustomizations()
    }

    /**
     * 重置为系统默认药代理论模型
     */
    fun resetToDefault(substanceName: String) {
        customizationStore.resetToDefault(substanceName)
        loadCustomizations()
    }
}

/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 */

package com.isaakhanimann.journal.ui.tabs.stats.tolerance

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.AddCircleOutline
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.isaakhanimann.journal.R

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ToleranceChartScreen(
    navigateBack: () -> Unit,
    viewModel: ToleranceViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    var showExplanationDialog by remember { mutableStateOf(false) }
    var showAddSimulationDialog by remember { mutableStateOf(false) }
    var selectedSubstanceForCustomization by remember { mutableStateOf<String?>(null) }
    val bottomSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.tolerance_chart_title)) },
                navigationIcon = {
                    IconButton(onClick = navigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.journal_action_back))
                    }
                },
                actions = {
                    IconButton(onClick = { showAddSimulationDialog = true }) {
                        Icon(Icons.Outlined.AddCircleOutline, contentDescription = stringResource(R.string.tolerance_simulate_ingestion))
                    }
                    IconButton(onClick = { showExplanationDialog = true }) {
                        Icon(Icons.Outlined.Info, contentDescription = stringResource(R.string.tolerance_model_limitations))
                    }
                }
            )
        }
    ) { paddingValues ->
        if (uiState.isLoading) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 16.dp, vertical = 8.dp)
            ) {
                // 1. 时间周期筛选 Chips
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    ToleranceTimeRange.values().forEach { range ->
                        FilterChip(
                            selected = range == uiState.selectedRange,
                            onClick = { viewModel.selectRange(range) },
                            label = { Text(stringResource(range.labelRes)) }
                        )
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                // 2. 模拟摄入提示条（若存在模拟记录）
                if (uiState.simulatedIngestions.isNotEmpty()) {
                    Card(
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.secondaryContainer
                        ),
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(bottom = 12.dp)
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 16.dp, vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(
                                text = stringResource(R.string.tolerance_previewing_simulations, uiState.simulatedIngestions.size),
                                style = MaterialTheme.typography.bodySmall
                            )
                            TextButton(onClick = viewModel::clearSimulatedIngestions) {
                                Text(stringResource(R.string.tolerance_clear_simulation))
                            }
                        }
                    }
                }

                // 3. 核心甘特图容器卡片（只读展示，手势零拦截，鼠标/触控可随意上下自由滑行）
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                    )
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text(
                            text = stringResource(R.string.tolerance_gantt_hint),
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        ToleranceChart(
                            toleranceWindows = uiState.toleranceWindows,
                            timeRange = uiState.selectedRange,
                            onSubstanceClick = {} // 图表自身彻底解绑点击，绝不误触阻碍滚动
                        )
                    }
                }

                Spacer(modifier = Modifier.height(20.dp))

                // 4. 独立解耦的物质体感自适应管理区（明确的独立按钮，绝无滑动手势冲突）
                val trackedSubstances = remember(uiState.toleranceWindows) {
                    uiState.toleranceWindows.map { it.substanceName }.distinct()
                }

                if (trackedSubstances.isNotEmpty()) {
                    Text(
                        text = stringResource(R.string.tolerance_tracked_substances_title),
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(8.dp))

                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.surface
                        )
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(12.dp)
                        ) {
                            trackedSubstances.forEachIndexed { index, substanceName ->
                                val localizedName = com.isaakhanimann.journal.ui.tabs.search.SubstanceLocalizationHelper.getLocalizedName(substanceName)
                                val window = uiState.toleranceWindows.firstOrNull { it.substanceName == substanceName }
                                val color = window?.adaptiveColor?.getComposeColor(androidx.compose.foundation.isSystemInDarkTheme())
                                    ?: MaterialTheme.colorScheme.primary

                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 6.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        modifier = Modifier.weight(1f)
                                    ) {
                                        Box(
                                            modifier = Modifier
                                                .size(10.dp)
                                                .background(color, RoundedCornerShape(5.dp))
                                        )
                                        Spacer(modifier = Modifier.width(8.dp))
                                        Text(
                                            text = localizedName,
                                            style = MaterialTheme.typography.bodyMedium,
                                            fontWeight = FontWeight.SemiBold
                                        )
                                        if (localizedName != substanceName) {
                                            Spacer(modifier = Modifier.width(6.dp))
                                            Text(
                                                text = "($substanceName)",
                                                style = MaterialTheme.typography.bodySmall,
                                                color = MaterialTheme.colorScheme.onSurfaceVariant
                                            )
                                        }
                                        if (window?.isUserCustomized == true) {
                                            Spacer(modifier = Modifier.width(6.dp))
                                            Text(
                                                text = stringResource(R.string.tolerance_customized_badge),
                                                style = MaterialTheme.typography.labelSmall,
                                                color = Color(0xFFFFD54F)
                                            )
                                        }
                                    }

                                    // 显式操作按钮：只有点击该按钮才弹出修改抽屉，鼠标看图滑行绝对不会触发！
                                    androidx.compose.material3.OutlinedButton(
                                        onClick = { selectedSubstanceForCustomization = substanceName },
                                        contentPadding = androidx.compose.foundation.layout.PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                                        modifier = Modifier.height(32.dp)
                                    ) {
                                        Text(stringResource(R.string.tolerance_adjust_button), style = MaterialTheme.typography.labelSmall)
                                    }
                                }

                                if (index < trackedSubstances.size - 1) {
                                    androidx.compose.material3.HorizontalDivider(
                                        color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f),
                                        modifier = Modifier.padding(vertical = 4.dp)
                                    )
                                }
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(20.dp))
                }

                // 4. 图例说明栏
                Text(
                    text = stringResource(R.string.tolerance_legend_title),
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    LegendItem(color = MaterialTheme.colorScheme.primary, text = stringResource(R.string.tolerance_legend_full))
                    LegendItem(color = MaterialTheme.colorScheme.primary.copy(alpha = 0.45f), text = stringResource(R.string.tolerance_legend_half))
                    LegendItem(color = Color(0xFF00E5FF), text = stringResource(R.string.tolerance_legend_today))
                }
                Spacer(modifier = Modifier.height(4.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .background(Color(0xFFFFD54F), RoundedCornerShape(4.dp))
                    )
                    Spacer(modifier = Modifier.width(6.dp))
                    Text(
                        text = stringResource(R.string.tolerance_legend_custom_dot),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }

                Spacer(modifier = Modifier.height(20.dp))

                // 5. 局限性免责说明
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.surface
                    ),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = stringResource(R.string.tolerance_harm_reduction_title),
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(
                            text = stringResource(R.string.tolerance_harm_reduction_desc),
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }

                Spacer(modifier = Modifier.height(30.dp))
            }
        }
    }

    // 弹出自适应调整底部抽屉
    selectedSubstanceForCustomization?.let { substanceName ->
        ToleranceAdaptiveBottomSheet(
            substanceName = substanceName,
            currentCustomization = uiState.customizations[substanceName],
            sheetState = bottomSheetState,
            onDismiss = { selectedSubstanceForCustomization = null },
            onSaveCustomization = { customization ->
                viewModel.saveCustomization(customization)
            },
            onMarkRecoveredToday = {
                viewModel.markRecoveredToday(substanceName)
            },
            onResetToDefault = {
                viewModel.resetToDefault(substanceName)
            }
        )
    }

    // 局限性说明弹窗
    if (showExplanationDialog) {
        AlertDialog(
            onDismissRequest = { showExplanationDialog = false },
            title = { Text(stringResource(R.string.tolerance_dialog_about_title)) },
            text = {
                Column {
                    Text(
                        text = stringResource(R.string.tolerance_dialog_section1_title),
                        fontWeight = FontWeight.Bold,
                        style = MaterialTheme.typography.bodyMedium
                    )
                    Text(
                        text = stringResource(R.string.tolerance_dialog_section1_desc),
                        style = MaterialTheme.typography.bodySmall
                    )
                    Text(
                        text = stringResource(R.string.tolerance_dialog_section2_title),
                        fontWeight = FontWeight.Bold,
                        style = MaterialTheme.typography.bodyMedium
                    )
                    Text(
                        text = stringResource(R.string.tolerance_dialog_section2_desc),
                        style = MaterialTheme.typography.bodySmall
                    )
                }
            },
            confirmButton = {
                TextButton(onClick = { showExplanationDialog = false }) {
                    Text(stringResource(R.string.tolerance_dialog_ok))
                }
            }
        )
    }

    // 模拟摄入推演弹窗
    if (showAddSimulationDialog) {
        var inputSubstanceName by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { showAddSimulationDialog = false },
            title = { Text(stringResource(R.string.tolerance_sim_dialog_title)) },
            text = {
                Column {
                    Text(
                        text = stringResource(R.string.tolerance_sim_dialog_hint),
                        style = MaterialTheme.typography.bodySmall
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    OutlinedTextField(
                        value = inputSubstanceName,
                        onValueChange = { inputSubstanceName = it },
                        label = { Text(stringResource(R.string.tolerance_sim_dialog_input_label)) },
                        singleLine = true
                    )
                }
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        if (inputSubstanceName.isNotBlank()) {
                            viewModel.addSimulatedIngestion(inputSubstanceName.trim())
                            showAddSimulationDialog = false
                        }
                    }
                ) {
                    Text(stringResource(R.string.tolerance_sim_dialog_add))
                }
            },
            dismissButton = {
                TextButton(onClick = { showAddSimulationDialog = false }) {
                    Text(stringResource(R.string.settings_cancel))
                }
            }
        )
    }
}

@Composable
private fun LegendItem(color: Color, text: String) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Box(
            modifier = Modifier
                .size(12.dp)
                .background(color, RoundedCornerShape(3.dp))
        )
        Spacer(modifier = Modifier.width(6.dp))
        Text(
            text = text,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

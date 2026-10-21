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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel

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
                title = { Text("耐受度时序分析") },
                navigationIcon = {
                    IconButton(onClick = navigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "返回")
                    }
                },
                actions = {
                    IconButton(onClick = { showAddSimulationDialog = true }) {
                        Icon(Icons.Outlined.AddCircleOutline, contentDescription = "模拟摄入推演")
                    }
                    IconButton(onClick = { showExplanationDialog = true }) {
                        Icon(Icons.Outlined.Info, contentDescription = "模型局限性说明")
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
                            label = { Text(range.label) }
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
                                text = "正在预览 ${uiState.simulatedIngestions.size} 条推演摄入",
                                style = MaterialTheme.typography.bodySmall
                            )
                            TextButton(onClick = viewModel::clearSimulatedIngestions) {
                                Text("清除推演")
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
                            text = "耐药恢复甘特矩阵 (滑动界面无冲突，调节请在下方列表操作)",
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
                        text = "已追踪物质 · 主观体感自适应调节：",
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
                                                text = "✓ 已自适应",
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
                                        Text("调节体感 ➔", style = MaterialTheme.typography.labelSmall)
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
                    text = "图例与体感自适应：",
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    LegendItem(color = MaterialTheme.colorScheme.primary, text = "完全耐受 (脱敏期)")
                    LegendItem(color = MaterialTheme.colorScheme.primary.copy(alpha = 0.45f), text = "半耐受 (衰减中)")
                    LegendItem(color = Color(0xFF00E5FF), text = "今日 (Now)")
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
                        text = "黄色小圆点：已融入您个人的主观耐受体感修正",
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
                            text = "💡 科学减害提示",
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(
                            text = "本模型基于 PsychonautWiki 公开药代动力学阶段推算，默认单次即建立瞬时完全耐受。由于个体生理差异与剂量不计，您可点击任意物质卡片自主调整恢复天数或标记已归零。",
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
            title = { Text("关于耐受度模型") },
            text = {
                Column {
                    Text(
                        text = "1. 理论模型局限性",
                        fontWeight = FontWeight.Bold,
                        style = MaterialTheme.typography.bodyMedium
                    )
                    Text(
                        text = "该图表反映了从完全耐受建立到减半、最终归零的群体理论时间。但未考虑实际摄入剂量及多物质交叉耐受。\n",
                        style = MaterialTheme.typography.bodySmall
                    )
                    Text(
                        text = "2. 主观体感自由度",
                        fontWeight = FontWeight.Bold,
                        style = MaterialTheme.typography.bodyMedium
                    )
                    Text(
                        text = "身体由您自己感知。点击物质即可自由设置完全耐受天数、归零天数或标记提前恢复。",
                        style = MaterialTheme.typography.bodySmall
                    )
                }
            },
            confirmButton = {
                TextButton(onClick = { showExplanationDialog = false }) {
                    Text("了解")
                }
            }
        )
    }

    // 模拟摄入推演弹窗
    if (showAddSimulationDialog) {
        var inputSubstanceName by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { showAddSimulationDialog = false },
            title = { Text("推演添加模拟服药") },
            text = {
                Column {
                    Text(
                        text = "输入物质名称，预演若在当前时刻服用，耐受窗口会被顺延到哪一天：",
                        style = MaterialTheme.typography.bodySmall
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    OutlinedTextField(
                        value = inputSubstanceName,
                        onValueChange = { inputSubstanceName = it },
                        label = { Text("物质英文或中文学名 (如 LSD, Psilocybin)") },
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
                    Text("添加推演")
                }
            },
            dismissButton = {
                TextButton(onClick = { showAddSimulationDialog = false }) {
                    Text("取消")
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

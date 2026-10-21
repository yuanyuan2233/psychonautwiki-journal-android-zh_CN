/*
 * Copyright (c) 2026. PsychonautWiki Journal Contributors.
 */

package com.isaakhanimann.journal.ui.tabs.search.substance

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.HealthAndSafety
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Science
import androidx.compose.material.icons.filled.Speed
import androidx.compose.material.icons.filled.Timer
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.isaakhanimann.journal.data.substances.classes.Pharmacokinetics
import com.isaakhanimann.journal.ui.theme.horizontalPadding
import com.isaakhanimann.journal.ui.theme.verticalPaddingCards

/**
 * 现代临床药代动力学 (ADME) 专属展示组件 (Jetpack Compose / Material 3 风格)
 * 专为处方精神类与 HRT 激素替代药物设计：
 * 突出消除半衰期 (t1/2)、达峰时间 (Tmax)、生物利用度、CYP450 酶谱、适应症与用药禁忌。
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun PharmacokineticsView(pk: Pharmacokinetics) {
    Column {
        // 1. 原研商品名标牌 (若适用)
        if (pk.brandName != null) {
            ElevatedCard(
                modifier = Modifier
                    .padding(horizontal = horizontalPadding, vertical = verticalPaddingCards)
                    .fillMaxWidth()
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(horizontal = horizontalPadding, vertical = 10.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.HealthAndSafety,
                        contentDescription = null,
                        modifier = Modifier.size(18.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.width(6.dp))
                    Text(
                        text = "原研参考: ${pk.brandName}",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                }
            }
        }

        // 2. 药代动力学 (ADME) 核心指标看板
        val hasAdmeMetrics = pk.halfLife != null || pk.tMax != null || pk.bioavailability != null || pk.cypEnzymes.isNotEmpty()
        if (hasAdmeMetrics) {
            SectionWithTitle(title = "药代动力学 (ADME)") {
                Column(
                    modifier = Modifier
                        .padding(horizontal = horizontalPadding, vertical = 6.dp)
                        .fillMaxWidth()
                ) {
                    // 三联并列指标卡
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        if (pk.halfLife != null) {
                            val hlDisplay = if (pk.halfLifeHours != null) "${pk.halfLifeHours}h" else pk.halfLife
                            PkMetricCard(
                                title = "消除半衰期 (t½)",
                                value = hlDisplay,
                                subtitle = "血药浓度减半",
                                icon = Icons.Default.Timer,
                                modifier = Modifier.weight(1f)
                            )
                        }
                        if (pk.tMax != null) {
                            val tMaxDisplay = if (pk.tMaxHours != null) "${pk.tMaxHours}h" else pk.tMax
                            PkMetricCard(
                                title = "达峰时间 (Tmax)",
                                value = tMaxDisplay,
                                subtitle = "峰值血药浓度",
                                icon = Icons.Default.Speed,
                                modifier = Modifier.weight(1f)
                            )
                        }
                        if (pk.bioavailability != null) {
                            PkMetricCard(
                                title = "生物利用度 (F)",
                                value = pk.bioavailability,
                                subtitle = "系统循环吸收",
                                icon = Icons.Default.Science,
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }

                    // 体内单室药代消除时程预测条
                    if (pk.halfLifeHours != null && pk.halfLifeHours > 0) {
                        Spacer(modifier = Modifier.height(14.dp))
                        Text(
                            text = "体内代谢消除稳态时程预测",
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.SemiBold
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        PkEliminationTimeline(halfLifeHours = pk.halfLifeHours)
                    }

                    // CYP450 代谢酶谱芯片组
                    if (pk.cypEnzymes.isNotEmpty()) {
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            text = "主要代谢途径 (CYP450 酶谱)",
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.SemiBold
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            pk.cypEnzymes.forEach { enzyme ->
                                Surface(
                                    shape = RoundedCornerShape(16.dp),
                                    color = MaterialTheme.colorScheme.secondaryContainer,
                                    modifier = Modifier.height(28.dp)
                                ) {
                                    Box(
                                        contentAlignment = Alignment.Center,
                                        modifier = Modifier.padding(horizontal = 10.dp)
                                    ) {
                                        Text(
                                            text = enzyme,
                                            style = MaterialTheme.typography.labelSmall,
                                            color = MaterialTheme.colorScheme.onSecondaryContainer
                                        )
                                    }
                                }
                            }
                        }
                    }

                    // 清除与排泄机制说明 (若有)
                    if (pk.clearance != null) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "排泄途径: ${pk.clearance}",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }

                    Spacer(modifier = Modifier.height(6.dp))
                }
            }
        }

        // 3. 临床适应症
        if (pk.indications.isNotEmpty()) {
            SectionWithTitle(title = "临床适应症") {
                Column(
                    modifier = Modifier
                        .padding(horizontal = horizontalPadding, vertical = 6.dp)
                        .fillMaxWidth()
                ) {
                    pk.indications.forEach { ind ->
                        Row(
                            modifier = Modifier.padding(vertical = 3.dp),
                            verticalAlignment = Alignment.Top
                        ) {
                            Surface(
                                shape = CircleShape,
                                color = MaterialTheme.colorScheme.primary,
                                modifier = Modifier
                                    .padding(top = 7.dp)
                                    .size(6.dp)
                            ) {}
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = ind,
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(6.dp))
                }
            }
        }

        // 4. 禁忌症与用药安全警示卡片 (醒目高警示设计)
        if (pk.contraindications.isNotEmpty()) {
            ElevatedCard(
                modifier = Modifier
                    .padding(horizontal = horizontalPadding, vertical = verticalPaddingCards)
                    .fillMaxWidth(),
                colors = CardDefaults.elevatedCardColors(
                    containerColor = MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.5f)
                )
            ) {
                Column(
                    modifier = Modifier
                        .padding(horizontal = horizontalPadding, vertical = 12.dp)
                        .fillMaxWidth()
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = Icons.Default.Warning,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.error,
                            modifier = Modifier.size(20.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = "禁忌症与用药安全警示",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.error
                        )
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    pk.contraindications.forEach { contra ->
                        Row(
                            modifier = Modifier.padding(vertical = 3.dp),
                            verticalAlignment = Alignment.Top
                        ) {
                            Surface(
                                shape = CircleShape,
                                color = MaterialTheme.colorScheme.error,
                                modifier = Modifier
                                    .padding(top = 7.dp)
                                    .size(6.dp)
                            ) {}
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = contra,
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onErrorContainer
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun PkMetricCard(
    title: String,
    value: String,
    subtitle: String,
    icon: ImageVector,
    modifier: Modifier = Modifier
) {
    OutlinedCard(
        modifier = modifier,
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 10.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                modifier = Modifier.size(18.dp),
                tint = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = value,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
            Text(
                text = title,
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurface
            )
            Text(
                text = subtitle,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
private fun PkEliminationTimeline(halfLifeHours: Double) {
    val totalClearHours = (halfLifeHours * 5.0)
    val totalClearFormatted = if (totalClearHours >= 48.0) {
        String.format("%.1f 天 (%.0f 小时)", totalClearHours / 24.0, totalClearHours)
    } else {
        String.format("%.1f 小时", totalClearHours)
    }

    Surface(
        shape = RoundedCornerShape(10.dp),
        color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(10.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "消除阶段 (一级动力学)",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "剩余血药浓度",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Spacer(modifier = Modifier.height(6.dp))

            EliminationStepRow(step = "1× t½ (${formatHours(halfLifeHours * 1)})", percent = 50f, remaining = "50%")
            EliminationStepRow(step = "2× t½ (${formatHours(halfLifeHours * 2)})", percent = 25f, remaining = "25%")
            EliminationStepRow(step = "3× t½ (${formatHours(halfLifeHours * 3)})", percent = 12.5f, remaining = "12.5%")
            EliminationStepRow(step = "5× t½ (${formatHours(halfLifeHours * 5)})", percent = 3.1f, remaining = "< 3.2% (完全清除)")

            Spacer(modifier = Modifier.height(6.dp))
            HorizontalDivider()
            Spacer(modifier = Modifier.height(6.dp))
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.Info,
                    contentDescription = null,
                    modifier = Modifier.size(16.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.width(4.dp))
                Text(
                    text = "临床预测完全代谢清除时间：约 $totalClearFormatted",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
        }
    }
}

@Composable
private fun EliminationStepRow(step: String, percent: Float, remaining: String) {
    Column(modifier = Modifier.padding(vertical = 3.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(text = step, style = MaterialTheme.typography.bodySmall)
            Text(text = remaining, style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.SemiBold)
        }
        Spacer(modifier = Modifier.height(2.dp))
        LinearProgressIndicator(
            progress = { percent / 100f },
            modifier = Modifier
                .fillMaxWidth()
                .height(5.dp)
                .clip(RoundedCornerShape(3.dp)),
            color = MaterialTheme.colorScheme.primary,
            trackColor = MaterialTheme.colorScheme.outlineVariant
        )
    }
}

private fun formatHours(hours: Double): String {
    return if (hours >= 48.0) {
        String.format("%.1fd", hours / 24.0)
    } else {
        String.format("%.1fh", hours)
    }
}

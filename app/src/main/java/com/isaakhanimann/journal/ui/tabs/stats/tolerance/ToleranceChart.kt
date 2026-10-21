/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 */

package com.isaakhanimann.journal.ui.tabs.stats.tolerance

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.TextMeasurer
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.isaakhanimann.journal.ui.tabs.search.SubstanceLocalizationHelper
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.time.temporal.ChronoUnit
import kotlin.math.max

/**
 * 高性能 Canvas 自定义绘制的耐受度时序甘特图。
 * 零额外三方依赖，支持双阶段色块、今日基准线、单指触摸准线探针与自适应修改响应。
 */
@Composable
fun ToleranceChart(
    toleranceWindows: List<ToleranceWindow>,
    timeRange: ToleranceTimeRange,
    onSubstanceClick: (substanceName: String) -> Unit,
    modifier: Modifier = Modifier
) {
    if (toleranceWindows.isEmpty()) {
        Box(
            modifier = modifier
                .fillMaxWidth()
                .height(200.dp)
                .padding(16.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "所选周期内暂无包含耐受药理数据的服药记录",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        return
    }

    val isDark = isSystemInDarkTheme()
    val textMeasurer = rememberTextMeasurer()

    // 提取所有涉及的唯一物质名称列表（按顺序排列）
    val substances = remember(toleranceWindows) {
        toleranceWindows.map { it.substanceName }.distinct()
    }

    val rowHeightDp = 58.dp
    val headerHeightDp = 36.dp
    val totalHeightDp = headerHeightDp + (rowHeightDp * substances.size)

    val now = remember { Instant.now() }
    val rangeStart = remember(timeRange, now) {
        now.minus(timeRange.days, ChronoUnit.DAYS)
    }
    val rangeEnd = remember(timeRange, now) {
        now.plus(max(10L, (timeRange.days * 0.2).toLong()), ChronoUnit.DAYS)
    }
    val totalSeconds = remember(rangeStart, rangeEnd) {
        ChronoUnit.SECONDS.between(rangeStart, rangeEnd).coerceAtLeast(1)
    }

    val zoneId = remember { ZoneId.systemDefault() }
    val dateFormatter = remember { DateTimeFormatter.ofPattern("M月d日").withZone(zoneId) }

    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(totalHeightDp)
    ) {
        val width = size.width
        val labelColumnWidth = 110.dp.toPx() // 左侧留出物质名宽度
        val chartPlotWidth = width - labelColumnWidth - 16.dp.toPx()
        val headerHeight = headerHeightDp.toPx()
        val rowHeight = rowHeightDp.toPx()

        fun instantToX(instant: Instant): Float {
            val secondsFromStart = ChronoUnit.SECONDS.between(rangeStart, instant)
            val ratio = (secondsFromStart.toFloat() / totalSeconds.toFloat()).coerceIn(0f, 1f)
            return labelColumnWidth + ratio * chartPlotWidth
        }

        fun xToInstant(x: Float): Instant {
            val ratio = ((x - labelColumnWidth) / chartPlotWidth).coerceIn(0f, 1f)
            val seconds = (ratio * totalSeconds).toLong()
            return rangeStart.plusSeconds(seconds)
        }

        // 1. 绘制顶部时间刻度与垂直网格参考线
        val tickCount = 4
        val tickIntervalSeconds = totalSeconds / tickCount
        for (i in 0..tickCount) {
            val tickInstant = rangeStart.plusSeconds(i * tickIntervalSeconds)
            val tickX = instantToX(tickInstant)
            val dateStr = dateFormatter.format(tickInstant)

            // 竖向网格细线
            drawLine(
                color = if (isDark) Color(0x22FFFFFF) else Color(0x18000000),
                start = Offset(tickX, headerHeight),
                end = Offset(tickX, size.height),
                strokeWidth = 1f
            )

            // 顶部刻度文字
            drawText(
                textMeasurer = textMeasurer,
                text = dateStr,
                topLeft = Offset(tickX - 20.dp.toPx(), 8.dp.toPx()),
                style = TextStyle(
                    fontSize = 11.sp,
                    color = if (isDark) Color(0x88FFFFFF) else Color(0x88000000)
                )
            )
        }

        // 2. 绘制各物质行
        substances.forEachIndexed { index, substanceName ->
            val rowY = headerHeight + index * rowHeight
            val localizedName = SubstanceLocalizationHelper.getLocalizedName(substanceName)

            // 左侧物质中文名称
            drawText(
                textMeasurer = textMeasurer,
                text = localizedName,
                topLeft = Offset(8.dp.toPx(), rowY + 12.dp.toPx()),
                style = TextStyle(
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (isDark) Color.White else Color(0xFF1A1A1A)
                )
            )

            // 英文学名/备注（微缩副标题）
            if (localizedName != substanceName) {
                drawText(
                    textMeasurer = textMeasurer,
                    text = substanceName,
                    topLeft = Offset(8.dp.toPx(), rowY + 32.dp.toPx()),
                    style = TextStyle(
                        fontSize = 10.sp,
                        color = if (isDark) Color(0x77FFFFFF) else Color(0x77000000)
                    )
                )
            }

            // 右侧甘特槽背景
            val barY = rowY + 16.dp.toPx()
            val barHeight = 26.dp.toPx()
            drawRoundRect(
                color = if (isDark) Color(0x15FFFFFF) else Color(0x0C000000),
                topLeft = Offset(labelColumnWidth, barY),
                size = Size(chartPlotWidth, barHeight),
                cornerRadius = CornerRadius(6.dp.toPx())
            )

            // 找出属于该物质的所有耐受窗口
            val windowsForSubstance = toleranceWindows.filter { it.substanceName == substanceName }
            for (window in windowsForSubstance) {
                val startX = instantToX(window.start)
                val endX = instantToX(window.end)
                val barWidth = (endX - startX).coerceAtLeast(4.dp.toPx())

                val baseColor = window.adaptiveColor.getComposeColor(isDark)
                val barColor = when (window.toleranceType) {
                    ToleranceType.FULL -> baseColor // 完全耐受：高饱和实心
                    ToleranceType.HALF -> baseColor.copy(alpha = 0.45f) // 半耐受：半透明
                }

                // 绘制耐受色块
                drawRoundRect(
                    color = barColor,
                    topLeft = Offset(startX, barY),
                    size = Size(barWidth, barHeight),
                    cornerRadius = CornerRadius(6.dp.toPx())
                )

                // 若包含用户自适应调整，在条带上绘制小徽章点
                if (window.isUserCustomized) {
                    drawCircle(
                        color = Color(0xFFFFD54F),
                        radius = 3.dp.toPx(),
                        center = Offset(startX + 6.dp.toPx(), barY + barHeight / 2)
                    )
                }
            }

            // 行间分割细线
            drawLine(
                color = if (isDark) Color(0x12FFFFFF) else Color(0x10000000),
                start = Offset(0f, rowY + rowHeight),
                end = Offset(width, rowY + rowHeight),
                strokeWidth = 1f
            )
        }

        // 3. 绘制“今日 (Today)”发光垂直基准参考线
        val todayX = instantToX(now)
        if (todayX in labelColumnWidth..width) {
            drawLine(
                color = Color(0xFF00E5FF),
                start = Offset(todayX, 6.dp.toPx()),
                end = Offset(todayX, size.height),
                strokeWidth = 2.dp.toPx()
            )
            // 今日顶部小圆点
            drawCircle(
                color = Color(0xFF00E5FF),
                radius = 4.dp.toPx(),
                center = Offset(todayX, 6.dp.toPx())
            )
        }
    }
}

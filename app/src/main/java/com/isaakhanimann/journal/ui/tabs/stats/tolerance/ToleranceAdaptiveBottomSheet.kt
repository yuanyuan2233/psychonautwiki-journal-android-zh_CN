/*
 * Copyright (c) 2026. PsychonautWiki Journal Chinese Maintenance Branch.
 */

package com.isaakhanimann.journal.ui.tabs.stats.tolerance

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.RestartAlt
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.SheetState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.isaakhanimann.journal.ui.tabs.search.SubstanceLocalizationHelper

/**
 * 允许用户自由调整主观耐药体感、覆盖算法并自适应的底部抽屉面板。
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ToleranceAdaptiveBottomSheet(
    substanceName: String,
    currentCustomization: SubstanceToleranceCustomization?,
    sheetState: SheetState,
    onDismiss: () -> Unit,
    onSaveCustomization: (SubstanceToleranceCustomization) -> Unit,
    onMarkRecoveredToday: () -> Unit,
    onResetToDefault: () -> Unit
) {
    val localizedName = SubstanceLocalizationHelper.getLocalizedName(substanceName)
    var fullDaysText by remember(currentCustomization) {
        mutableStateOf(currentCustomization?.customFullDays?.toString() ?: "")
    }
    var zeroDaysText by remember(currentCustomization) {
        mutableStateOf(currentCustomization?.customZeroDays?.toString() ?: "")
    }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .padding(bottom = 36.dp)
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = localizedName,
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold
                    )
                    if (localizedName != substanceName) {
                        Text(
                            text = substanceName,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "主观体感自适应：由于个体生理代谢及用药剂量差异，您可以自由修正您感受到的真实耐药恢复周期，无需受限于标准药代理论均值。",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            Spacer(modifier = Modifier.height(20.dp))

            // 一键标记恢复基线
            Button(
                onClick = {
                    onMarkRecoveredToday()
                    onDismiss()
                },
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    contentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            ) {
                Icon(Icons.Filled.CheckCircle, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("⚡ 标记为今天已完全归零 (感知已恢复基线)")
            }

            Spacer(modifier = Modifier.height(20.dp))

            // 自由修改完全耐受天数
            OutlinedTextField(
                value = fullDaysText,
                onValueChange = { fullDaysText = it },
                label = { Text("完全耐受体感天数 (Full Tolerance)") },
                placeholder = { Text("例如: 2.0 (留空遵循药代基准)") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(12.dp))

            // 自由修改耐受归零天数
            OutlinedTextField(
                value = zeroDaysText,
                onValueChange = { zeroDaysText = it },
                label = { Text("耐受完全归零体感天数 (Zero Tolerance)") },
                placeholder = { Text("例如: 5.0 (留空遵循药代基准)") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(24.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                OutlinedButton(
                    onClick = {
                        onResetToDefault()
                        onDismiss()
                    },
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Filled.RestartAlt, contentDescription = null)
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("恢复理论基准")
                }

                Button(
                    onClick = {
                        val fullVal = fullDaysText.toDoubleOrNull()
                        val zeroVal = zeroDaysText.toDoubleOrNull()
                        onSaveCustomization(
                            SubstanceToleranceCustomization(
                                substanceName = substanceName,
                                customFullDays = fullVal,
                                customZeroDays = zeroVal
                            )
                        )
                        onDismiss()
                    },
                    modifier = Modifier.weight(1f)
                ) {
                    Text("保存自适应")
                }
            }
        }
    }
}

/*
 * Copyright (c) 2022-2026. Isaak Hanimann & PsychonautWiki Journal Contributors.
 * This file is part of PsychonautWiki Journal.
 *
 * PsychonautWiki Journal is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or (at
 * your option) any later version.
 *
 * PsychonautWiki Journal is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with PsychonautWiki Journal.  If not, see https://www.gnu.org/licenses/gpl-3.0.en.html.
 */

package com.isaakhanimann.journal.ui.tabs.journal.addingestion.time

import androidx.compose.animation.Crossfade
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.isaakhanimann.journal.R
import com.isaakhanimann.journal.data.room.experiences.entities.AdaptiveColor
import com.isaakhanimann.journal.data.room.experiences.entities.AppColor

@Preview
@Composable
fun ColorPickerPreview() {
    val alreadyUsedColors = listOf(AdaptiveColor.BLUE, AdaptiveColor.PINK)
    val otherColors = AdaptiveColor.entries.filter { color ->
        !alreadyUsedColors.contains(color)
    }
    ColorPicker(
        selectedColor = AdaptiveColor.BLUE,
        onChangeOfColor = {},
        alreadyUsedColors = alreadyUsedColors,
        otherColors = otherColors
    )
}

@Composable
fun ColorPicker(
    selectedColor: AppColor,
    onChangeOfColor: (AppColor) -> Unit,
    alreadyUsedColors: List<AppColor>,
    otherColors: List<AppColor>
) {
    val isDarkTheme = isSystemInDarkTheme()
    var isColorPickerVisible by remember {
        mutableStateOf(false)
    }
    val shape = RoundedCornerShape(8.dp)
    Surface(
        shape = shape,
        color = selectedColor.getComposeColor(isDarkTheme),
        modifier = Modifier
            .size(50.dp)
            .clip(shape)
            .clickable(onClick = { isColorPickerVisible = true })
    ) {
        Icon(
            imageVector = Icons.Default.Edit,
            contentDescription = stringResource(R.string.journal_action_edit_color),
            modifier = Modifier.padding(15.dp),
        )
    }
    if (isColorPickerVisible) {
        ColorDialog(
            dismiss = { isColorPickerVisible = false },
            selectedColor = selectedColor,
            onChangeOfColor = onChangeOfColor,
            alreadyUsedColors = alreadyUsedColors,
            otherColors = otherColors
        )
    }
}

@Composable
fun ColorPicker(
    selectedColor: AdaptiveColor,
    onChangeOfColor: (AdaptiveColor) -> Unit,
    alreadyUsedColors: List<AdaptiveColor>,
    otherColors: List<AdaptiveColor>
) {
    ColorPicker(
        selectedColor = AppColor(selectedColor),
        onChangeOfColor = { onChangeOfColor(it.toAdaptiveColor()) },
        alreadyUsedColors = alreadyUsedColors.map { AppColor(it) },
        otherColors = otherColors.map { AppColor(it) }
    )
}

@Preview
@Composable
fun ColorDialogPreview() {
    val alreadyUsedColors = listOf(AdaptiveColor.BLUE, AdaptiveColor.PINK, AdaptiveColor.AUBURN)
    val otherColors = AdaptiveColor.entries.filter { color ->
        !alreadyUsedColors.contains(color)
    }
    ColorDialog(
        dismiss = {},
        selectedColor = AdaptiveColor.BLUE,
        onChangeOfColor = {},
        alreadyUsedColors = alreadyUsedColors,
        otherColors = otherColors
    )
}

@Composable
fun ColorDialog(
    dismiss: () -> Unit,
    selectedColor: AppColor? = null,
    onChangeOfColor: (AppColor) -> Unit,
    alreadyUsedColors: List<AppColor>,
    otherColors: List<AppColor>
) {
    val isDarkTheme = isSystemInDarkTheme()
    var currentFamily by remember { mutableStateOf<ColorFamily?>(null) }

    AlertDialog(
        onDismissRequest = dismiss,
        title = {
            if (currentFamily == null) {
                Text(
                    text = stringResource(R.string.journal_pick_color),
                    style = MaterialTheme.typography.titleLarge
                )
            } else {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    IconButton(
                        onClick = { currentFamily = null },
                        modifier = Modifier.size(36.dp)
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = stringResource(R.string.journal_color_back_to_hues)
                        )
                    }
                    Text(
                        text = stringResource(currentFamily!!.titleRes),
                        style = MaterialTheme.typography.titleLarge
                    )
                }
            }
        },
        text = {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 260.dp, max = 420.dp)
                    .verticalScroll(rememberScrollState())
            ) {
                Crossfade(
                    targetState = currentFamily,
                    label = "ColorFamilyCrossfade"
                ) { family ->
                    if (family == null) {
                        BaseHuesView(
                            selectedColor = selectedColor,
                            alreadyUsedColors = alreadyUsedColors,
                            isDarkTheme = isDarkTheme,
                            onSelectFamily = { currentFamily = it },
                            onSelectDirectColor = {
                                onChangeOfColor(it)
                                dismiss()
                            }
                        )
                    } else {
                        ShadesView(
                            family = family,
                            selectedColor = selectedColor,
                            alreadyUsedColors = alreadyUsedColors,
                            isDarkTheme = isDarkTheme,
                            onSelectShade = {
                                onChangeOfColor(it)
                                dismiss()
                            }
                        )
                    }
                }
            }
        },
        confirmButton = {
            TextButton(onClick = dismiss) {
                Text(stringResource(R.string.journal_action_cancel))
            }
        },
        dismissButton = if (currentFamily != null) {
            {
                TextButton(onClick = { currentFamily = null }) {
                    Text(stringResource(R.string.journal_color_back_to_hues))
                }
            }
        } else null
    )
}

@Composable
fun ColorDialog(
    dismiss: () -> Unit,
    selectedColor: AdaptiveColor? = null,
    onChangeOfColor: (AdaptiveColor) -> Unit,
    alreadyUsedColors: List<AdaptiveColor>,
    otherColors: List<AdaptiveColor>
) {
    ColorDialog(
        dismiss = dismiss,
        selectedColor = selectedColor?.let { AppColor(it) },
        onChangeOfColor = { onChangeOfColor(it.toAdaptiveColor()) },
        alreadyUsedColors = alreadyUsedColors.map { AppColor(it) },
        otherColors = otherColors.map { AppColor(it) }
    )
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun BaseHuesView(
    selectedColor: AppColor?,
    alreadyUsedColors: List<AppColor>,
    isDarkTheme: Boolean,
    onSelectFamily: (ColorFamily) -> Unit,
    onSelectDirectColor: (AppColor) -> Unit
) {
    Column(modifier = Modifier.fillMaxWidth()) {
        Text(
            text = stringResource(R.string.journal_color_select_hue),
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Spacer(modifier = Modifier.height(12.dp))

        FlowRow(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            ColorFamily.entries.forEach { family ->
                val isSelectedFamily = selectedColor?.adaptiveColor != null && family.shades.contains(selectedColor.adaptiveColor)
                BaseHueSwatch(
                    family = family,
                    isSelectedFamily = isSelectedFamily,
                    isDarkTheme = isDarkTheme,
                    onClick = { onSelectFamily(family) }
                )
            }
        }

        if (alreadyUsedColors.isNotEmpty()) {
            Spacer(modifier = Modifier.height(16.dp))
            HorizontalDivider()
            Spacer(modifier = Modifier.height(10.dp))
            Text(
                text = stringResource(R.string.journal_color_already_used),
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.height(8.dp))
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                alreadyUsedColors.distinct().forEach { usedColor ->
                    ShadeSwatch(
                        color = usedColor,
                        isSelected = usedColor == selectedColor,
                        isAlreadyUsed = true,
                        isDarkTheme = isDarkTheme,
                        onClick = { onSelectDirectColor(usedColor) }
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun ShadesView(
    family: ColorFamily,
    selectedColor: AppColor?,
    alreadyUsedColors: List<AppColor>,
    isDarkTheme: Boolean,
    onSelectShade: (AppColor) -> Unit
) {
    Column(modifier = Modifier.fillMaxWidth()) {
        Text(
            text = stringResource(R.string.journal_color_select_shade),
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Spacer(modifier = Modifier.height(12.dp))

        FlowRow(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            family.shades.forEach { shade ->
                val shadeAppColor = AppColor(shade)
                ShadeSwatch(
                    color = shadeAppColor,
                    isSelected = selectedColor != null && (selectedColor.adaptiveColor == shade || selectedColor.rawValue.equals(shade.name, ignoreCase = true)),
                    isAlreadyUsed = alreadyUsedColors.any { it.adaptiveColor == shade || it.rawValue.equals(shade.name, ignoreCase = true) },
                    isDarkTheme = isDarkTheme,
                    onClick = { onSelectShade(shadeAppColor) }
                )
            }
        }
    }
}

@Composable
private fun BaseHueSwatch(
    family: ColorFamily,
    isSelectedFamily: Boolean,
    isDarkTheme: Boolean,
    onClick: () -> Unit
) {
    val shape = RoundedCornerShape(10.dp)
    val composeColor = family.baseColor.getComposeColor(isDarkTheme)
    val isLight = (0.299 * composeColor.red + 0.587 * composeColor.green + 0.114 * composeColor.blue) > 0.5

    val borderModifier = if (isSelectedFamily) {
        Modifier.border(
            width = 3.dp,
            color = MaterialTheme.colorScheme.primary,
            shape = shape
        )
    } else {
        Modifier.border(
            width = 1.dp,
            color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f),
            shape = shape
        )
    }

    Surface(
        shape = shape,
        color = composeColor,
        onClick = onClick,
        modifier = Modifier
            .size(52.dp)
            .then(borderModifier)
            .semantics { contentDescription = family.name }
    ) {
        if (isSelectedFamily) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Box(
                    modifier = Modifier
                        .size(10.dp)
                        .background(
                            color = if (isLight) Color.Black.copy(alpha = 0.8f) else Color.White.copy(alpha = 0.9f),
                            shape = CircleShape
                        )
                )
            }
        }
    }
}

@Composable
private fun ShadeSwatch(
    color: AppColor,
    isSelected: Boolean,
    isAlreadyUsed: Boolean,
    isDarkTheme: Boolean,
    onClick: () -> Unit
) {
    val shape = RoundedCornerShape(10.dp)
    val composeColor = color.getComposeColor(isDarkTheme)
    val isLight = (0.299 * composeColor.red + 0.587 * composeColor.green + 0.114 * composeColor.blue) > 0.5

    val borderModifier = if (isSelected) {
        Modifier.border(
            width = 3.dp,
            color = MaterialTheme.colorScheme.primary,
            shape = shape
        )
    } else {
        Modifier.border(
            width = 1.dp,
            color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f),
            shape = shape
        )
    }

    Surface(
        shape = shape,
        color = composeColor,
        onClick = onClick,
        modifier = Modifier
            .size(52.dp)
            .then(borderModifier)
            .semantics { contentDescription = color.rawValue }
    ) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            if (isSelected) {
                Icon(
                    imageVector = Icons.Default.Check,
                    contentDescription = null,
                    tint = if (isLight) Color.Black else Color.White,
                    modifier = Modifier.size(24.dp)
                )
            } else if (isAlreadyUsed) {
                Box(
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(5.dp)
                        .size(8.dp)
                        .background(
                            color = if (isLight) Color.Black.copy(alpha = 0.6f) else Color.White.copy(alpha = 0.85f),
                            shape = CircleShape
                        )
                )
            }
        }
    }
}

@Composable
private fun ShadeSwatch(
    color: AdaptiveColor,
    isSelected: Boolean,
    isAlreadyUsed: Boolean,
    isDarkTheme: Boolean,
    onClick: () -> Unit
) = ShadeSwatch(
    color = AppColor(color),
    isSelected = isSelected,
    isAlreadyUsed = isAlreadyUsed,
    isDarkTheme = isDarkTheme,
    onClick = onClick
)

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun CircleColorButtons(
    colors: List<AdaptiveColor>,
    onTapOnColor: (AdaptiveColor) -> Unit
) {
    val isDarkTheme = isSystemInDarkTheme()
    val spacing = 5.dp
    FlowRow(
        horizontalArrangement = Arrangement.spacedBy(spacing),
        verticalArrangement = Arrangement.spacedBy(spacing)
    ) {
        val shape = RoundedCornerShape(8.dp)
        colors.forEach { color ->
            Surface(
                shape = shape,
                color = color.getComposeColor(isDarkTheme),
                modifier = Modifier
                    .size(48.dp)
                    .clip(shape)
                    .clickable(
                        onClick = { onTapOnColor(color) }
                    )
                    .semantics { contentDescription = color.name }
            ) {}
        }
    }
}

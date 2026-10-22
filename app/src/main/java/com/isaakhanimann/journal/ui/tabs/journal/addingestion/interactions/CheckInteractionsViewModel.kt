/*
 * Copyright (c) 2022. Isaak Hanimann.
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

package com.isaakhanimann.journal.ui.tabs.journal.addingestion.interactions

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.navigation.toRoute
import com.isaakhanimann.journal.R
import com.isaakhanimann.journal.data.room.experiences.ExperienceRepository
import com.isaakhanimann.journal.data.room.experiences.entities.Ingestion
import com.isaakhanimann.journal.data.substances.classes.InteractionType
import com.isaakhanimann.journal.data.substances.repositories.SubstanceRepository
import com.isaakhanimann.journal.ui.main.navigation.graphs.CheckInteractionsRoute
import com.isaakhanimann.journal.ui.tabs.journal.experience.components.getDurationText
import com.isaakhanimann.journal.ui.tabs.settings.combinations.CombinationSettingsStorage
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import java.time.Instant
import java.time.temporal.ChronoUnit
import javax.inject.Inject

@HiltViewModel
class CheckInteractionsViewModel @Inject constructor(
    substanceRepo: SubstanceRepository,
    private val experienceRepo: ExperienceRepository,
    private val combinationSettingsStorage: CombinationSettingsStorage,
    private val interactionChecker: InteractionChecker,
    state: SavedStateHandle,
) : ViewModel() {
    private val checkInteractionsRoute = state.toRoute<CheckInteractionsRoute>()
    val substanceName = checkInteractionsRoute.substanceName
    val substance = substanceRepo.getSubstance(substanceName)!!
    val dangerousInteractions = substance.interactions?.dangerous ?: emptyList()
    val unsafeInteractions = substance.interactions?.unsafe ?: emptyList()
    val uncertainInteractions = substance.interactions?.uncertain ?: emptyList()

    var isSearchingForInteractions by mutableStateOf(true)
    var isShowingAlert by mutableStateOf(false)
    var alertInteractionType by mutableStateOf<InteractionType?>(null)
    var alertItems by mutableStateOf<List<AlertItem>>(emptyList())
    private var latestIngestionsOfEverySubstanceSinceTwoDays: List<Ingestion> = emptyList()

    sealed interface AlertItem {
        val type: InteractionType
        data class IngestionAlert(override val type: InteractionType, val ingestion: Ingestion) : AlertItem
        data class ExtraAlert(override val type: InteractionType, val extra: String) : AlertItem
    }

    init {
        viewModelScope.launch {
            val twoDaysAgo = Instant.now().minus(2, ChronoUnit.DAYS)
            latestIngestionsOfEverySubstanceSinceTwoDays =
                experienceRepo.getLatestIngestionOfEverySubstanceSinceDate(twoDaysAgo)
            checkInteractionsAndMaybeShowAlert()
            isSearchingForInteractions = false
        }
    }

    private suspend fun checkInteractionsAndMaybeShowAlert() {
        val filteredIngestions = getIngestionsWithInteraction()
        val dangerousIngestions =
            filteredIngestions.filter { it.interactionType == InteractionType.DANGEROUS }
                .map { it.ingestion }.sortedByDescending { it.time }
        val unsafeIngestions =
            filteredIngestions.filter { it.interactionType == InteractionType.UNSAFE }
                .map { it.ingestion }.sortedByDescending { it.time }
        val uncertainIngestions =
            filteredIngestions.filter { it.interactionType == InteractionType.UNCERTAIN }
                .map { it.ingestion }.sortedByDescending { it.time }
        val enabledExtraInteractions =
            combinationSettingsStorage.enabledInteractionsFlow.first()
        val dangerousExtras =
            enabledExtraInteractions.filter { substance.interactions?.dangerous?.contains(it) == true }
        val unsafeExtras =
            enabledExtraInteractions.filter { substance.interactions?.unsafe?.contains(it) == true }
        val uncertainExtras =
            enabledExtraInteractions.filter { substance.interactions?.uncertain?.contains(it) == true }
        alertInteractionType =
            if (dangerousIngestions.isNotEmpty() || dangerousExtras.isNotEmpty()) {
                InteractionType.DANGEROUS
            } else if (unsafeIngestions.isNotEmpty() || unsafeExtras.isNotEmpty()) {
                InteractionType.UNSAFE
            } else if (uncertainIngestions.isNotEmpty() || uncertainExtras.isNotEmpty()) {
                InteractionType.UNCERTAIN
            } else {
                return
            }
        val items = mutableListOf<AlertItem>()
        dangerousIngestions.forEach { items.add(AlertItem.IngestionAlert(InteractionType.DANGEROUS, it)) }
        dangerousExtras.forEach { items.add(AlertItem.ExtraAlert(InteractionType.DANGEROUS, it)) }
        unsafeIngestions.forEach { items.add(AlertItem.IngestionAlert(InteractionType.UNSAFE, it)) }
        unsafeExtras.forEach { items.add(AlertItem.ExtraAlert(InteractionType.UNSAFE, it)) }
        uncertainIngestions.forEach { items.add(AlertItem.IngestionAlert(InteractionType.UNCERTAIN, it)) }
        uncertainExtras.forEach { items.add(AlertItem.ExtraAlert(InteractionType.UNCERTAIN, it)) }
        alertItems = items
        isShowingAlert = true
    }

    fun getFormattedAlertText(context: Context): String {
        val now = Instant.now()
        val messages = mutableListOf<String>()
        for (item in alertItems) {
            when (item) {
                is AlertItem.IngestionAlert -> {
                    val timeDiff = getDurationText(fromInstant = item.ingestion.time, toInstant = now, context = context)
                    val localizedName = com.isaakhanimann.journal.ui.tabs.search.SubstanceLocalizationHelper.getLocalizedName(item.ingestion.substanceName)
                    val strRes = when (item.type) {
                        InteractionType.DANGEROUS -> R.string.journal_alert_dangerous_with_time
                        InteractionType.UNSAFE -> R.string.journal_alert_unsafe_with_time
                        InteractionType.UNCERTAIN -> R.string.journal_alert_uncertain_with_time
                    }
                    messages.add(context.getString(strRes, localizedName, timeDiff))
                }
                is AlertItem.ExtraAlert -> {
                    val localizedExtra = com.isaakhanimann.journal.ui.tabs.search.SubstanceLocalizationHelper.getLocalizedName(item.extra)
                    val strRes = when (item.type) {
                        InteractionType.DANGEROUS -> R.string.journal_alert_dangerous_extra
                        InteractionType.UNSAFE -> R.string.journal_alert_unsafe_extra
                        InteractionType.UNCERTAIN -> R.string.journal_alert_uncertain_extra
                    }
                    messages.add(context.getString(strRes, localizedExtra))
                }
            }
        }
        return messages.distinct().joinToString(separator = "\n")
    }

    private fun getIngestionsWithInteraction(): List<IngestionInteraction> {
        return latestIngestionsOfEverySubstanceSinceTwoDays.mapNotNull { ingestion ->
            val interaction = interactionChecker.getInteractionBetween(
                aName = substanceName,
                bName = ingestion.substanceName
            )
            if (interaction != null) {
                return@mapNotNull IngestionInteraction(
                    ingestion = ingestion,
                    interactionType = interaction.interactionType
                )
            } else {
                return@mapNotNull null
            }
        }
    }

    data class IngestionInteraction(
        val ingestion: Ingestion,
        val interactionType: InteractionType
    )


}
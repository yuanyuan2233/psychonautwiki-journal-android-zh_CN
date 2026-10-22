/*
 * Copyright (c) 2022-2023. Isaak Hanimann.
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

import com.isaakhanimann.journal.data.substances.classes.InteractionType
import com.isaakhanimann.journal.data.substances.classes.Interactions
import com.isaakhanimann.journal.data.substances.repositories.SubstanceRepository
import com.isaakhanimann.journal.ui.tabs.search.SubstanceLocalizationHelper
import javax.inject.Inject
import javax.inject.Singleton


@Singleton
class InteractionChecker @Inject constructor(
    private val substanceRepo: SubstanceRepository,
) {
    fun getInteractionBetween(aName: String, bName: String): Interaction? {
        if (aName == bName) {
            return null
        }
        val interactionFromAToB = getInteractionFromAToB(aName, bName)
        val interactionFromBToA = getInteractionFromAToB(bName, aName)
        if (interactionFromAToB != null && interactionFromBToA != null) {
            val isAtoB = interactionFromAToB.dangerCount >= interactionFromBToA.dangerCount
            val interactionType = if (isAtoB) interactionFromAToB else interactionFromBToA
            return Interaction(
                aName = aName,
                bName = bName,
                interactionType = interactionType,
            )
        } else if (interactionFromAToB != null) {
            return Interaction(
                aName = aName,
                bName = bName,
                interactionType = interactionFromAToB,
            )
        } else if (interactionFromBToA != null) {
            return Interaction(
                aName = aName,
                bName = bName,
                interactionType = interactionFromBToA,
            )
        } else {
            return null
        }
    }

    private fun getInteractionFromAToB(
        aName: String,
        bName: String,
    ): InteractionType? {
        val substanceA = substanceRepo.getSubstance(aName)
        if (substanceA != null) {
            val directInteraction = getDirectInteraction(interactions = substanceA.interactions, substanceName = bName)
            if (directInteraction != null) {
                return directInteraction
            }
            val wildcardInteraction = getWildcardInteraction(interactions = substanceA.interactions, substanceName = bName)
            if (wildcardInteraction != null) {
                return wildcardInteraction
            }
            val substanceB = substanceRepo.getSubstance(bName)
            if (substanceB != null) {
                val classInteraction = getClassInteraction(interactions = substanceA.interactions, categories = substanceB.categories)
                if (classInteraction != null) {
                    return classInteraction
                }
            }
        }
        return null
    }

    private fun getDirectInteraction(interactions: Interactions?, substanceName: String): InteractionType? {
        if (interactions == null) {
            return null
        }
        return if (isDirectMatch(interactions.dangerous, substanceName)) {
            InteractionType.DANGEROUS
        } else if (isDirectMatch(interactions.unsafe, substanceName)) {
            InteractionType.UNSAFE
        } else if (isDirectMatch(interactions.uncertain, substanceName)) {
            InteractionType.UNCERTAIN
        } else {
            null
        }
    }

    private fun getWildcardInteraction(interactions: Interactions?, substanceName: String): InteractionType? {
        if (interactions == null) {
            return null
        }
        return if (isWildcardMatch(interactions.dangerous, substanceName)) {
            InteractionType.DANGEROUS
        } else if (isWildcardMatch(interactions.unsafe, substanceName)) {
            InteractionType.UNSAFE
        } else if (isWildcardMatch(interactions.uncertain, substanceName)) {
            InteractionType.UNCERTAIN
        } else {
            null
        }
    }

    private fun getClassInteraction(interactions: Interactions?, categories: List<String>): InteractionType? {
        if (interactions == null) {
            return null
        }
        return if (isClassMatch(interactions.dangerous, categories)) {
            InteractionType.DANGEROUS
        } else if (isClassMatch(interactions.unsafe, categories)) {
            InteractionType.UNSAFE
        } else if (isClassMatch(interactions.uncertain, categories)) {
            InteractionType.UNCERTAIN
        } else {
            null
        }
    }

    private fun isClassMatch(interactions: List<String>, categories: List<String>): Boolean {
        val extendedInteractions = extendAndCleanInteractions(interactions)
        return categories.any { categoryName ->
                extendedInteractions.any { interactionName ->
                    interactionName.contains(categoryName, ignoreCase = true)
                }
            }
    }

    private fun isWildcardMatch(interactions: List<String>, substanceName: String): Boolean {
        val extendedInteractions = extendAndCleanInteractions(interactions)
        return extendedInteractions.map { interaction ->
            Regex(
                pattern = interaction.replace(
                    oldValue = "x",
                    newValue = "[\\S]{2}",
                    ignoreCase = true
                ),
                option = RegexOption.IGNORE_CASE
            ).matches(substanceName)
        }.any { it }
    }

    private fun isDirectMatch(interactions: List<String>, substanceName: String): Boolean {
        val extendedInteractions = extendAndCleanInteractions(interactions)
        return extendedInteractions.contains(substanceName)
    }

    private fun extendAndCleanInteractions(interactions: List<String>): List<String> {
        return interactions.flatMap { rawName ->
            val resolvedList = mutableListOf(rawName)
            // 归一化中文名称或附带注释的条目为标准英文名
            SubstanceLocalizationHelper.getCanonicalEnglishName(rawName)?.let { canonical ->
                resolvedList.add(canonical)
            }
            // 去除括号中的临床说明或化学注释
            val clean = rawName.replace(Regex("[\\(（][^\\)）]*[\\)）]"), "").trim()
            if (clean != rawName && clean.isNotEmpty()) {
                resolvedList.add(clean)
                SubstanceLocalizationHelper.getCanonicalEnglishName(clean)?.let { canonical ->
                    resolvedList.add(canonical)
                }
            }
            // 针对 "/"、"、" 拆分多物质条目
            val parts = clean.split(Regex("[/、|]")).map { it.trim() }.filter { it.isNotEmpty() }
            if (parts.size > 1) {
                for (part in parts) {
                    resolvedList.add(part)
                    SubstanceLocalizationHelper.getCanonicalEnglishName(part)?.let { canonical ->
                        resolvedList.add(canonical)
                    }
                }
            }
            resolvedList
        }.flatMap { name ->
            when (name) {
                "Substituted amphetamines", "取代苯丙胺类" -> {
                    substitutedAmphetamines
                }
                "Serotonin releasers", "5-羟色胺释放剂" -> {
                    serotoninReleasers
                }
                "Tricyclic antidepressants", "三环类抗抑郁药" -> {
                    emptyList() // remove because we don't want to match "depressant" with it and there is no substance that belongs to that class
                }
                else -> {
                    listOf(name)
                }
            }
        }.distinct()
    }

    private val serotoninReleasers = listOf(
        "MDMA",
        "MDA",
        "Mephedrone"
    )

    private val substitutedAmphetamines = listOf(
        "Amphetamine",
        "Methamphetamine",
        "Ethylamphetamine",
        "Propylamphetamine",
        "Isopropylamphetamine",
        "Bromo-DragonFLY",
        "Lisdexamfetamine",
        "Clobenzorex",
        "Dimethylamphetamine",
        "Selegiline",
        "Benzphetamine",
        "Ortetamine",
        "3-Methylamphetamine",
        "4-Methylamphetamine",
        "4-MMA",
        "Xylopropamine",
        "ß-methylamphetamine",
        "3-phenylmethamphetamine",
        "2-FA",
        "2-FMA",
        "2-FEA",
        "3-FA",
        "3-FMA",
        "3-FEA",
        "Fenfluramine",
        "Norfenfluramine",
        "4-FA",
        "4-FMA",
        "4-CA",
        "4-BA",
        "4-IA",
        "DCA",
        "4-HA",
        "4-HMA",
        "3,4-DHA",
        "OMA",
        "3-MA",
        "MMMA",
        "MMA",
        "PMA",
        "PMMA",
        "PMEA",
        "4-ETA",
        "TMA-2",
        "TMA-6",
        "4-MTA",
        "5-API",
        "Cathine",
        "Phenmetrazine",
        "3-FPM",
        "Prolintane"
    )

}

data class Interaction(
    val aName: String,
    val bName: String,
    val interactionType: InteractionType,
)
/*
 * Copyright (c) 2026. PsychonautWiki Journal Contributors.
 */

package com.isaakhanimann.journal.data.substances.classes

data class Pharmacokinetics(
    val halfLife: String? = null,
    val halfLifeHours: Double? = null,
    val tMax: String? = null,
    val tMaxHours: Double? = null,
    val bioavailability: String? = null,
    val cypEnzymes: List<String> = emptyList(),
    val clearance: String? = null,
    val brandName: String? = null,
    val indications: List<String> = emptyList(),
    val contraindications: List<String> = emptyList(),
)

/*
 * Copyright (c) 2023. Isaak Hanimann.
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

package com.isaakhanimann.journal.data.room.experiences.entities

import androidx.room.Entity
import androidx.room.Ignore
import androidx.room.PrimaryKey
import java.time.Instant

@Entity
data class TimedNote(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    var creationDate: Instant = Instant.now(),
    var time: Instant,
    var note: String,
    var color: AppColor,
    var experienceId: Int,
    var isPartOfTimeline: Boolean
) {
    @Ignore
    constructor(
        id: Int = 0,
        creationDate: Instant = Instant.now(),
        time: Instant,
        note: String,
        color: AdaptiveColor,
        experienceId: Int,
        isPartOfTimeline: Boolean
    ) : this(
        id = id,
        creationDate = creationDate,
        time = time,
        note = note,
        color = AppColor(color),
        experienceId = experienceId,
        isPartOfTimeline = isPartOfTimeline
    )
}

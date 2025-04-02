package com.hades.discord.bot.carol.database

import kotlinx.serialization.Serializable

@Serializable
data class DiscordMember(
    val id: Long = 0L,
    val money: Int = 0,
    val isBanned: Boolean = false,
    var xpInGuilds: Map<String, Int> = mapOf<String, Int>(),
    val achievements: List<Achievement> = listOf<Achievement>()
)

@Serializable
data class Achievement(
    val name: String,
    val date: String
)
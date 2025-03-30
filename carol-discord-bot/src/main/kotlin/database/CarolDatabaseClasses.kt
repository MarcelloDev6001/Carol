package com.hades.discord.bot.carol.database

import kotlinx.serialization.Serializable

@Serializable
data class DiscordMember(
    val id: Long,
    val money: Int,
    val isBanned: Boolean,
    val xpInGuilds: Map<String, Int>,
    val achievements: List<Achievement>
)

@Serializable
data class Achievement(
    val name: String,
    val date: String
)
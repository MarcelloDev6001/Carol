package com.hades.discord.bot.carol.database

data class Achievement(
    val id: String,
    val date: String
)

data class DiscordMember(
    val id: String,
    val money: Long,
    val isBanned: Boolean,
    val xpInGuilds: Map<String, Int>,
    val achievements: List<Achievement>
)

public final data class DiscordGuild(
    val id: Long,
    val commandsAllowed: Array<String>
)
package com.hades.discord.bot.carol.experience

import com.hades.discord.bot.carol.database.CarolDatabaseHelper
import com.hades.discord.bot.carol.database.DiscordMember
import net.dv8tion.jda.api.entities.User

class CarolExperienceManager {
    companion object {
        public suspend fun addXPToMember(member: User, discordMember: DiscordMember, guildId: String, amount: Int)
        {
            val memberToDatabase: DiscordMember = discordMember.copy()
            val newXpInGuilds: MutableMap<String, Int> = memberToDatabase.xpInGuilds.toMutableMap()
            newXpInGuilds[guildId] = memberToDatabase.xpInGuilds.getOrDefault(guildId, 0) + amount
            memberToDatabase.xpInGuilds = newXpInGuilds
            CarolDatabaseHelper.insertOrModifyExisting("discord_members", discordMember.id, memberToDatabase)
        }

        public fun getXPFromMember(member: User) {

        }

        public fun getMemberFromDatabase(member: User) {

        }
    }
}
package com.hades.discord.bot.carol.experience

import com.hades.discord.bot.carol.CarolProperties
import com.hades.discord.bot.carol.database.CarolDatabaseHelper
import com.hades.discord.bot.carol.database.CarolDatabaseProperties
import com.hades.discord.bot.carol.database.DiscordMember
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import net.dv8tion.jda.api.entities.User

class CarolExperienceManager {
    companion object {
        public suspend fun addXPToMember(member: User, guildId: String, amount: Int)
        {
            val db = CarolDatabaseHelper(
                supabaseUrl = CarolProperties.getSupabaseUrl(),
                supabaseKey = CarolProperties.getSupabaseKey()
            )

            var loaded: DiscordMember? = db.get<DiscordMember>(CarolDatabaseProperties.MEMBERS_TABLE, member.idLong) // if not exist, create one
            if (loaded == null) {
                loaded = getMemberWithXPUpdated(DiscordMember(member.idLong, 0, false, emptyMap(), emptyList()), guildId, 1)
                db.save(CarolDatabaseProperties.MEMBERS_TABLE, loaded)
            }
            loaded = getMemberWithXPUpdated(loaded, guildId, amount)
            db.save(CarolDatabaseProperties.MEMBERS_TABLE, loaded)
            // if already exist, just update the xpInGuilds colunm
            println(loaded)
        }

        private fun getMemberWithXPUpdated(member: DiscordMember, guildId: String, amount: Int): DiscordMember
        {
            val newXpInGuilds: MutableMap<String, Int> = member.xpInGuilds.toMutableMap()
            newXpInGuilds[guildId] = member.xpInGuilds.getOrDefault(guildId, 0).toInt() + amount
            return member.copy(xpInGuilds = newXpInGuilds.toMap())
        }

        public fun getXPFromMember(member: User) {

        }

        public fun getMemberFromDatabase(member: User) {

        }
    }
}
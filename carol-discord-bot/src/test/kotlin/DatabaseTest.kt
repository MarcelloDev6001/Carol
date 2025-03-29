import com.hades.discord.bot.carol.database.DiscordMember
import com.hades.discord.bot.carol.database.Achievement
import com.hades.discord.bot.carol.database.SupabaseManager
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.fasterxml.jackson.module.kotlin.registerKotlinModule

suspend fun main() {
    try {
        val member = DiscordMember(
            id = "123456789",
            money = 1000,
            isBanned = false,
            xpInGuilds = mapOf("guild1" to 150, "guild2" to 300),
            achievements = listOf(
                Achievement("achievement1", "2023-10-01"),
                Achievement("achievement2", "2023-10-05")
            )
        )

        val mapper = ObjectMapper().registerKotlinModule()
        val jsonAsString = mapper.writeValueAsString(member)

        println("JSON a ser inserido: $jsonAsString") // Log para debug

        val result = SupabaseManager.insert("discord-members", jsonAsString)
        println(result)
    } catch (e: Exception) {
        println("Erro durante o processo: ${e.message}")
        e.printStackTrace()
    }
}
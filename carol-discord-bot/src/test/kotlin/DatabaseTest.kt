import com.hades.discord.bot.carol.database.*
import com.hades.discord.bot.carol.database.DiscordMember

suspend fun main() {
    val inserter = CarolDatabaseHelper()

    val member = DiscordMember(
        id = 779727883228020756,
        money = 1000,
        isBanned = false,
        xpInGuilds = mapOf("guild1" to 150, "guild2" to 300),
        achievements = listOf(
            Achievement("achievement1", "2023-10-01"),
            Achievement("achievement2", "2023-10-05")
        )
    )

    // Operações CRUD
    runCatching {
        inserter.insertMember(member)
    }.onFailure { e ->
        println("Erro ao acessar Supabase: ${e.message}")
    }
}
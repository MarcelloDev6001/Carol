package com.hades.discord.bot.carol.command.people

import com.hades.discord.bot.carol.CarolProperties
import com.hades.discord.bot.carol.command.CarolBaseCommandOptions
import com.hades.discord.bot.carol.command.CarolCommand
import com.hades.discord.bot.carol.database.CarolDatabaseHelper
import com.hades.discord.bot.carol.database.CarolDatabaseProperties
import com.hades.discord.bot.carol.database.DiscordMember
import kotlinx.coroutines.runBlocking
import net.dv8tion.jda.api.EmbedBuilder
import net.dv8tion.jda.api.entities.Member
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.interactions.commands.OptionType
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction
import java.awt.Color

class CarolProfileCommand : CarolCommand("perfil", "veja o perfil de alguém.", listOf(
    CarolBaseCommandOptions(
    "pessoa",
    "a pessoa que vc quer que eu mande o perfil (ou deixe vazio para ver SEU perfil)",
    OptionType.USER,
    false,
    false
)
), true) {
    override fun onCommandExecuted(interaction: SlashCommandInteraction) {
        if (interaction.getOption("pessoa") == null) // wanna see our own profile
        {
            val db = CarolDatabaseHelper(CarolProperties.getSupabaseUrl(), CarolProperties.getSupabaseKey())
            runBlocking {
                var profileOnDatabase: DiscordMember? =
                    db.get<DiscordMember>(CarolDatabaseProperties.MEMBERS_TABLE, interaction.user.idLong)

                if (profileOnDatabase == null) {
                    profileOnDatabase = DiscordMember(interaction.user.idLong, 0, false, emptyMap(), emptyList())
                    db.save(CarolDatabaseProperties.MEMBERS_TABLE, profileOnDatabase)
                }

                val embedBuilder: EmbedBuilder = EmbedBuilder()
                embedBuilder.setTitle("Perfil de ${interaction.member?.effectiveName}:")
                embedBuilder.addField("ID:", "${interaction.member?.id}", true)
                embedBuilder.addField("Dinheiro:", "${profileOnDatabase.money}", true)
                embedBuilder.addField("XP (nesse servidor):", "${profileOnDatabase.xpInGuilds.getOrDefault(interaction.guild?.id, 0)}", true)
                embedBuilder.addField("Conquistas:", "Será adicionado em breve...", true)
                embedBuilder.setFooter("Mensagem de Carol <3")
                embedBuilder.setImage(interaction.user.avatarUrl)
                embedBuilder.setColor(Color.WHITE)

                interaction.replyEmbeds(embedBuilder.build()).queue()
            }
        }
        else
        {
            val db = CarolDatabaseHelper(CarolProperties.getSupabaseUrl(), CarolProperties.getSupabaseKey())
            runBlocking {
                val member: Member? = interaction.getOption("pessoa")!!.asMember
                var profileOnDatabase: DiscordMember? =
                    member?.let { db.get<DiscordMember>(CarolDatabaseProperties.MEMBERS_TABLE, it.idLong) }

                if (profileOnDatabase == null) {
                    if (member != null) {
                        profileOnDatabase = DiscordMember(member.idLong, 0, false, emptyMap(), emptyList())
                    }
                    db.save(CarolDatabaseProperties.MEMBERS_TABLE, profileOnDatabase!!)
                }

                val embedBuilder: EmbedBuilder = EmbedBuilder()
                embedBuilder.setTitle("Perfil de ${member?.effectiveName}:")
                embedBuilder.addField("ID:", "${member?.id}", true)
                embedBuilder.addField("Dinheiro:", "${profileOnDatabase!!.money}", true)
                embedBuilder.addField("XP (nesse servidor):", "${interaction.guild?.let {
                    profileOnDatabase!!.xpInGuilds.getOrDefault(
                        it.id, 0)
                }}", true)
                embedBuilder.addField("Conquistas:", "Será adicionado em breve...", true)
                embedBuilder.setFooter("Mensagem de Carol <3")
                embedBuilder.setImage(member?.avatarUrl)
                embedBuilder.setColor(Color.WHITE)

                interaction.replyEmbeds(embedBuilder.build()).queue()
            }
        }
    }

    override fun onMessageCommandExecuted(message: MessageReceivedEvent) {
        if (message.message.contentRaw.startsWith(CarolProperties.getPrefix() + getCarolCommandName())) {
            var content: String = message.message.contentRaw.replace(CarolProperties.getPrefix() + getCarolCommandName(), "").trim()
            if (content == "")
            {
                content = message.author.id
            }

            var member: Member? = null

            try {
                member = message.guild.getMemberById(content.replace("<@", "").replace(">", ""))
            } catch (e: Exception) {
                reply("Insira um membro válido")
            }

            val db = CarolDatabaseHelper(CarolProperties.getSupabaseUrl(), CarolProperties.getSupabaseKey())
            runBlocking {
                var profileOnDatabase: DiscordMember? =
                    member?.let { db.get<DiscordMember>(CarolDatabaseProperties.MEMBERS_TABLE, it.idLong) }

                if (profileOnDatabase == null) {
                    if (member != null) {
                        profileOnDatabase = DiscordMember(member.idLong, 0, false, emptyMap(), emptyList())
                    }
                    db.save(CarolDatabaseProperties.MEMBERS_TABLE, profileOnDatabase!!)
                }

                val embedBuilder: EmbedBuilder = EmbedBuilder()
                embedBuilder.setTitle("Perfil de ${member?.effectiveName}:")
                embedBuilder.addField("ID:", "${member?.id}", true)
                embedBuilder.addField("Dinheiro:", "${profileOnDatabase.money}", true)
                embedBuilder.addField("XP (nesse servidor):", "${
                    message.guild.let {
                        profileOnDatabase.xpInGuilds.getOrDefault(
                            it.id, 0)
                    }
                }", true)
                embedBuilder.addField("Conquistas:", "Será adicionado em breve...", true)
                embedBuilder.setFooter("Mensagem de Carol <3")
                embedBuilder.setImage(member?.avatarUrl)
                embedBuilder.setColor(Color.WHITE)

                message.message.replyEmbeds(embedBuilder.build()).queue()
            }
        }
    }
}
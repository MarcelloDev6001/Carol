package com.hades.discord.bot.carol.command.`fun`

import com.hades.discord.bot.carol.command.CarolBaseCommandOptions
import com.hades.discord.bot.carol.command.CarolCommand
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.interactions.commands.OptionType
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction

class CarolRule34Command : CarolCommand("regra-34", "Hmm... então vc gosta disso, é?", listOf(CarolBaseCommandOptions(
    "tag",
    "A tag que você deseja procurar",
    OptionType.STRING,
    true,
    false
)), true) {
    override fun onCommandExecuted(interaction: SlashCommandInteraction) {
        reply("hmm... seu safadinho...")
        replyOnInteractionChannel("@everyone GALERA, O ${interaction.user.asMention} TÁ QUERENDO VER RULE 34!!!", 1)
        replyOnInteractionChannel("JUNTA NELE!!!")
        replyOnInteractionChannel("https://i.makeagif.com/media/11-09-2024/hEOIZg.gif", 1)
    }

    override fun onMessageCommandExecuted(message: MessageReceivedEvent) {
        reply("hmm... seu safadinho...")
        replyOnInteractionChannel("@everyone GALERA, O ${message.author.asMention} TÁ QUERENDO VER RULE 34!!!", 3)
        replyOnInteractionChannel("JUNTA NELE!!!")
        replyOnInteractionChannel("https://i.makeagif.com/media/11-09-2024/hEOIZg.gif", 3)
    }
}
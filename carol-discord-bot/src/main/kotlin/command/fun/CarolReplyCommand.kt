package com.hades.discord.bot.carol.command.`fun`

import com.hades.discord.bot.carol.CarolProperties
import com.hades.discord.bot.carol.command.CarolBaseCommandOptions
import com.hades.discord.bot.carol.command.CarolCommand
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.interactions.commands.OptionType
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction

class CarolReplyCommand : CarolCommand("reply", "me faça responder a uma mensagem sua.", listOf(CarolBaseCommandOptions(
    "mensagem",
    "a mensagem que vc quer que eu mande",
    OptionType.STRING,
    true,
    false
)), true) {
    override fun onCommandExecuted(interaction: SlashCommandInteraction) {
        reply("tá bom")
        replyOnInteractionChannel(interaction.options[0].toString())
    }

    override fun onMessageCommandExecuted(message: MessageReceivedEvent) {
        if (message.message.contentRaw.startsWith(CarolProperties.getPrefix() + getCarolCommandName() + " ")) {
            val content: String = message.message.contentRaw.replace(CarolProperties.getPrefix() + getCarolCommandName() + " ", "")
            if (content.trim() == "") {
                reply("mande uma mensagem válida.")
                return
            }
            message.message.delete().queue()
            replyMessage(content, message.message.referencedMessage)
        }
    }
}
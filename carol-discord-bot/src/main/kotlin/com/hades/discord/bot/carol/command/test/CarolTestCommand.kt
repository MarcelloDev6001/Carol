package com.hades.discord.bot.carol.command.test

import com.hades.discord.bot.carol.command.CarolCommand
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction

class CarolTestCommand : CarolCommand("test", "Apenas um comando de teste",null, true) {
    override fun onCommandExecuted(interaction: SlashCommandInteraction) {
        reply("bodia, esse é só um comando de teste")
    }

    override fun onMessageCommandExecuted(message: MessageReceivedEvent) {
        reply("bodia, esse é só um comando de teste")
    }
}
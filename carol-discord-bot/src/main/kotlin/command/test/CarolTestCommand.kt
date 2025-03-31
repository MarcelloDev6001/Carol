package com.hades.discord.bot.carol.command.test

import com.hades.discord.bot.carol.command.CarolCommand
import com.hades.discord.bot.carol.command.CarolCommandsSettings
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction

class CarolTestCommand : CarolCommand("test") {
    override fun onCommandExecuted(interaction: SlashCommandInteraction) {
        reply("bodia, esse é só um comando de teste")
    }
}
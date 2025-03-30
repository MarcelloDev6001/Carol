package com.hades.discord.bot.carol.listeners

import com.hades.discord.bot.carol.command.CarolCommand
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter
import net.dv8tion.jda.api.interactions.commands.OptionMapping

public class CarolSlashCommandListener : ListenerAdapter() {
    override fun onSlashCommandInteraction(event: SlashCommandInteractionEvent) {
        val command: CarolCommand = CarolCommand(event.interaction)
        command.onCommandExecuted(event.interaction.name)
        println("Command executed: " + event.interaction.name)
    }
}
package com.hades.discord.bot.carol.listeners

import com.hades.discord.bot.carol.command.CarolCommand
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter

public class CarolSlashCommandListener : ListenerAdapter() {
    override fun onSlashCommandInteraction(event: SlashCommandInteractionEvent) {
        CarolCommand.dispatchInteraction(event)
        println("Command executed: " + event.interaction.name)
    }
}
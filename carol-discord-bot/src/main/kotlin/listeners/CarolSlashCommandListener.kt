package com.hades.discord.bot.carol.listeners

import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter
import net.dv8tion.jda.api.interactions.commands.OptionMapping

public class CarolSlashCommandListener : ListenerAdapter() {
    override fun onSlashCommandInteraction(event: SlashCommandInteractionEvent) {
        when (event.getName()) {
            "say" -> {
                event.reply(event.getOption("content", OptionMapping::getAsString) ?: "Nenhum conteudo informado").queue();
        };
            else -> return;
        }
    }
}
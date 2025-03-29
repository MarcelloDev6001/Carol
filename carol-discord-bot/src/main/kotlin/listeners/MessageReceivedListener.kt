package com.hades.discord.bot.carol.listeners

import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter

public class MessageReceivedListener : ListenerAdapter() {
    override fun onMessageReceived(event: MessageReceivedEvent) {
        // Why would i get a bot message?
        if (event.author.isBot) return

        // first command, here where i first started...
        if (event.message.contentRaw.equals("!olamundo", ignoreCase = true)) {
            event.message.reply("Olá, mundo!").queue()
        }
    }
}
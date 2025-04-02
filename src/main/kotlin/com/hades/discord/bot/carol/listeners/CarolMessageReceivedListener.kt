package com.hades.discord.bot.carol.listeners

import com.hades.discord.bot.carol.CarolProperties
import com.hades.discord.bot.carol.command.CarolCommand
import com.hades.discord.bot.carol.experience.CarolExperienceManager
import kotlinx.coroutines.runBlocking
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter

public class CarolMessageReceivedListener : ListenerAdapter() {
    override fun onMessageReceived(event: MessageReceivedEvent) {
        // Why would i get a bot message?
        if (event.author.isBot) return

        runBlocking {
            CarolExperienceManager.addXPToMember(event.author, event.guild.id.toString(), 10)
        }

        // first command, here where i first started...
        if (event.message.contentRaw.equals("!olamundo", ignoreCase = true)) {
            event.message.reply("Olá, mundo!").queue()
        }

        val messageParts = event.message.contentRaw.split("\\s+".toRegex(), limit = 2)
        val checkForCommand = messageParts[0]

        if (checkForCommand.startsWith(CarolProperties.getPrefix())) {
            val comm = checkForCommand.substring(CarolProperties.getPrefix().length)
            val args = if (messageParts.size > 1) messageParts[1].split("\\s+".toRegex()) else emptyList()
            executeMessageCommands(comm, args, event)
        }
    }

    fun executeMessageCommands(command: String, args: List<String>, event: MessageReceivedEvent) {
        CarolCommand.dispatchMessageCommand(event, command)
    }
}
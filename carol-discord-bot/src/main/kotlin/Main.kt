package com.hades.discord.bot.carol

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
import com.hades.discord.bot.carol.listeners.OnMessageReceived
import net.dv8tion.jda.api.JDA
import net.dv8tion.jda.api.JDABuilder
import net.dv8tion.jda.api.entities.Activity
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter
import net.dv8tion.jda.api.requests.GatewayIntent

fun main() {
    val token = "MTIxNDk4NTIwNDk4NTI0MTYwMA.GJi6F1.3zbrFSkSYp2GwKRjrJcupXScTIJEK_W7vvv5H8"  // Substitua pelo token do seu bot

    // here we start
    val builder: JDA = JDABuilder.createDefault(token, GatewayIntent.GUILD_MESSAGES, GatewayIntent.DIRECT_MESSAGES, GatewayIntent.MESSAGE_CONTENT, GatewayIntent.GUILD_MEMBERS)
        .addEventListeners(OnMessageReceived())
        .build()
}

class Bot : ListenerAdapter() {
    override fun onMessageReceived(event: MessageReceivedEvent) {
        // Why would i get a bot message?
        if (event.author.isBot) return

        // first command, here where i first started...
        if (event.message.contentRaw.equals("!olamundo", ignoreCase = true)) {
            event.message.reply("Olá, mundo!").queue()
        }
    }
}
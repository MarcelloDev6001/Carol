package com.hades.discord.bot.carol

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
import com.hades.discord.bot.carol.listeners.CarolMessageReceivedListener
import com.hades.discord.bot.carol.listeners.CarolSlashCommandListener
import net.dv8tion.jda.api.JDA
import net.dv8tion.jda.api.JDABuilder
import net.dv8tion.jda.api.interactions.commands.build.Commands
import net.dv8tion.jda.api.requests.GatewayIntent
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction
import net.dv8tion.jda.api.interactions.commands.OptionType.*

fun updateCommands(builder: JDA)
{
    val commands: CommandListUpdateAction = builder.updateCommands()
    // Add all your commands on this action instance
    commands.addCommands(
        Commands.slash("say", "Makes the bot say what you tell it to")
            .addOption(STRING, "content", "What the bot should say", true), // Accepting a user input
    );

    // Then finally send your commands to discord using the API
    commands.queue();
}

fun main() {
    val token = CarolProperties.getToken()
    println("token: " + token)

    // here we start
    val builder: JDA = JDABuilder.createDefault(token, GatewayIntent.GUILD_MESSAGES, GatewayIntent.DIRECT_MESSAGES, GatewayIntent.MESSAGE_CONTENT, GatewayIntent.GUILD_MEMBERS)
        .addEventListeners(CarolMessageReceivedListener())
        .addEventListeners(CarolSlashCommandListener())
        .build()

    updateCommands(builder)
}
package com.hades.discord.bot.carol

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
import com.hades.discord.bot.carol.command.CarolBaseCommand
import com.hades.discord.bot.carol.command.CarolBaseCommandOptions
import com.hades.discord.bot.carol.command.CarolCommandsSettings
import com.hades.discord.bot.carol.command.test.CarolTestCommand
import com.hades.discord.bot.carol.listeners.CarolMessageReceivedListener
import com.hades.discord.bot.carol.listeners.CarolSlashCommandListener
import net.dv8tion.jda.api.JDA
import net.dv8tion.jda.api.JDABuilder
import net.dv8tion.jda.api.interactions.commands.build.Commands
import net.dv8tion.jda.api.requests.GatewayIntent
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction
import net.dv8tion.jda.api.interactions.commands.OptionType.*
import net.dv8tion.jda.api.interactions.commands.build.SlashCommandData

fun updateCommands(builder: JDA)
{
    val commands: CommandListUpdateAction = builder.updateCommands()
    // Add all your commands on this action instance
    val commandsToAdd: Array<SlashCommandData> = arrayOf()
    for ((key: String, comm: CarolBaseCommand) in CarolCommandsSettings.commands)
    {
        val newCommToAdd: SlashCommandData = Commands.slash(comm.getName(), comm.getDescription())
        newCommToAdd.setGuildOnly(comm.getGuildOnly())
        if (comm.getOptions()?.isNotEmpty() == true)
        {
            for (option: CarolBaseCommandOptions in comm.getOptions()!!)
            {
                newCommToAdd.addOption(
                    option.type,
                    option.name,
                    option.description,
                    option.required,
                    option.autoComplete
                )
            }
        }
        println("command added: " + newCommToAdd.name)
        commands.addCommands(newCommToAdd)
    }

    // Then finally send your commands to discord using the API
    commands.queue()
}

fun loadCommands()
{
    val testCommand = CarolTestCommand()
}

fun main() {
    val token = CarolProperties.getToken()
    println("token: " + token)

    // here we start
    val builder: JDA = JDABuilder.createDefault(token, GatewayIntent.GUILD_MESSAGES, GatewayIntent.DIRECT_MESSAGES, GatewayIntent.MESSAGE_CONTENT, GatewayIntent.GUILD_MEMBERS)
        .addEventListeners(CarolMessageReceivedListener())
        .addEventListeners(CarolSlashCommandListener())
        .build()
        .awaitReady()

    updateCommands(builder)
    loadCommands()
}
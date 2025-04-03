package com.hades.discord.bot.carol

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
import com.hades.discord.bot.carol.command.CarolCommandsSettings
import com.hades.discord.bot.carol.command.`fun`.CarolFuneralCommand
import com.hades.discord.bot.carol.command.`fun`.CarolGamblingCommand
import com.hades.discord.bot.carol.command.`fun`.CarolReplyCommand
import com.hades.discord.bot.carol.command.`fun`.CarolRule34Command
import com.hades.discord.bot.carol.command.people.CarolProfileCommand
import com.hades.discord.bot.carol.command.test.CarolTestCommand
import com.hades.discord.bot.carol.command.util.CarolDashboardCommand
import com.hades.discord.bot.carol.listeners.CarolMessageReceivedListener
import com.hades.discord.bot.carol.listeners.CarolSlashCommandListener
import net.dv8tion.jda.api.JDA
import net.dv8tion.jda.api.JDABuilder
import net.dv8tion.jda.api.interactions.commands.build.Commands
import net.dv8tion.jda.api.requests.GatewayIntent
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction

fun updateCommands(builder: JDA)
{
    builder.updateCommands()
    val commands: CommandListUpdateAction = builder.updateCommands()
    for ((key, comm) in CarolCommandsSettings.commands) {
        val newCommToAdd = Commands.slash(comm.name, comm.description)
            .setGuildOnly(comm.guild_only)

        if (comm.permissionsRequired != null)
        {
            newCommToAdd.setDefaultPermissions(comm.permissionsRequired)
        }

        // Verifica e adiciona opções de forma mais idiomática
        comm.options?.takeIf { it.isNotEmpty() }?.forEach { option ->
            newCommToAdd.addOption(
                option.getType(),
                option.getName(),
                option.getDescription(),
                option.isRequired(),
                option.isAutoComplete()
            )
        }

        commands.addCommands(newCommToAdd)
        println("Command added: ${newCommToAdd.name}")
    }

    // Then finally send your commands to discord using the API
    commands.queue()
}

fun loadCommands()
{
    val testCommand = CarolTestCommand()
    val rule34Command = CarolRule34Command()
    val replyCommand = CarolReplyCommand()
    val profileCommand = CarolProfileCommand()
    val gamblingCommand = CarolGamblingCommand()
    val funeralCommand = CarolFuneralCommand()
    val carolDashboardCommand = CarolDashboardCommand()
}

fun main() {
    val token = CarolProperties.getToken()
    println("token: " + token)

    // here we start
    val builder: JDA = JDABuilder.create(token, GatewayIntent.GUILD_MESSAGES, GatewayIntent.GUILD_EMOJIS_AND_STICKERS, GatewayIntent.DIRECT_MESSAGES, GatewayIntent.MESSAGE_CONTENT, GatewayIntent.GUILD_MEMBERS)
        .addEventListeners(CarolMessageReceivedListener())
        .addEventListeners(CarolSlashCommandListener())
        .build()

    updateCommands(builder)
    loadCommands()

    builder.awaitReady()
}
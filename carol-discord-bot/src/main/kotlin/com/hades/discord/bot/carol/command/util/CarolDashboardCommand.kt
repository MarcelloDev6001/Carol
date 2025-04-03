package com.hades.discord.bot.carol.command.util

import com.hades.discord.bot.carol.command.CarolCommand
import net.dv8tion.jda.api.Permission
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.interactions.commands.DefaultMemberPermissions
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction

class CarolDashboardCommand : CarolCommand("dashboard", "veja as opções da sua guilds",null, true, DefaultMemberPermissions.DISABLED) {
    override fun onCommandExecuted(interaction: SlashCommandInteraction) {
        if (interaction.member?.hasPermission(Permission.ADMINISTRATOR) == true)
        {
            reply("em breve será adicionado um link aqui")
        }
        else
        {
            reply("Você não tem permissão para usar esse comando")
        }
    }

    override fun onMessageCommandExecuted(message: MessageReceivedEvent) {
        if (message.member?.hasPermission(Permission.ADMINISTRATOR) == true)
        {
            reply("em breve será adicionado um link aqui")
        }
        else
        {
            reply("Você não tem permissão para usar esse comando")
        }
    }
}
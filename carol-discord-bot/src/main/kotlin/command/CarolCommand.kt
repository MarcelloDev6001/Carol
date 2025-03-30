package com.hades.discord.bot.carol.command

import net.dv8tion.jda.api.JDA
import net.dv8tion.jda.api.entities.Guild
import net.dv8tion.jda.api.entities.Member
import net.dv8tion.jda.api.entities.User
import net.dv8tion.jda.api.entities.channel.Channel
import net.dv8tion.jda.api.entities.channel.unions.MessageChannelUnion
import net.dv8tion.jda.api.interactions.DiscordLocale
import net.dv8tion.jda.api.interactions.InteractionHook
import net.dv8tion.jda.api.interactions.commands.Command
import net.dv8tion.jda.api.interactions.commands.CommandInteraction
import net.dv8tion.jda.api.interactions.commands.OptionMapping
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction
import net.dv8tion.jda.api.interactions.modals.Modal
import net.dv8tion.jda.api.requests.restaction.interactions.ModalCallbackAction
import net.dv8tion.jda.api.requests.restaction.interactions.ReplyCallbackAction

open class CarolCommand constructor(originalcomm: CommandInteraction) : SlashCommandInteraction {
    override fun getIdLong(): Long {return idLong}
    override fun getTypeRaw(): Int {return typeRaw}
    override fun getToken(): String {return token}
    override fun getGuild(): Guild? {return guild}
    override fun getUser(): User {return user}
    override fun getMember(): Member? {return member}
    override fun isAcknowledged(): Boolean {return isAcknowledged}
    override fun getChannel(): MessageChannelUnion {return channel}
    override fun getUserLocale(): DiscordLocale {return userLocale}
    override fun getJDA(): JDA {return jda}
    override fun getHook(): InteractionHook {return hook}
    override fun deferReply(): ReplyCallbackAction {return deferReply()}
    override fun getCommandType(): Command.Type {return commandType}
    override fun getName(): String {return name}
    override fun getSubcommandName(): String? {return subcommandName}
    override fun getSubcommandGroup(): String? {return subcommandGroup}
    override fun getCommandIdLong(): Long {return commandIdLong}
    override fun isGuildCommand(): Boolean {return isGuildCommand}
    override fun getOptions(): MutableList<OptionMapping> {return options}
    override fun replyModal(modal: Modal): ModalCallbackAction {return replyModal(modal)}

    val originalCommand: CommandInteraction = originalcomm

    open fun onCommandExecuted(name: String)
    {
        println("Command executed: ${name}")
    }

    fun reply(content: String, ephemeral: Boolean)
    {
        originalCommand.reply(content).setEphemeral(ephemeral)
    }
}
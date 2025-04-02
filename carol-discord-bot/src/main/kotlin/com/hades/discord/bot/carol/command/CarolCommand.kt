package com.hades.discord.bot.carol.command

import net.dv8tion.jda.api.entities.Message
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction
import java.time.Duration

open class CarolCommand(
    val name: String,
    val description: String,
    val options: List<CarolBaseCommandOptions>?,
    val guild_only: Boolean
) {
    protected var interaction: SlashCommandInteraction? = null
    protected var message: MessageReceivedEvent? = null

    companion object {
        private val allCommands = mutableListOf<CarolCommand>()

        fun dispatchInteraction(interaction: SlashCommandInteraction) {
            allCommands.firstOrNull { it.name == interaction.name }?.apply {
                this.interaction = interaction
                this.message = null
                onCommandExecuted(interaction)
            }
        }

        fun dispatchMessageCommand(message: MessageReceivedEvent, command: String) {
            println(command)
            allCommands.firstOrNull { it.name == command }?.apply {
                this.message = message
                this.interaction = null
                onMessageCommandExecuted(message)
            }
        }
    }

    init {
        allCommands.add(this)
    }

    open fun onCommandExecuted(interaction: SlashCommandInteraction) {
        println("comando executado: ${interaction.name}")
    }

    open fun onMessageCommandExecuted(message: MessageReceivedEvent) {
        println("comando de mensagem executado.")
    }

    protected fun reply(content: String, ephemeral: Boolean = false) {
        interaction?.let {
            try {
                it.reply(content).setEphemeral(ephemeral).queue()
            } catch (e: Exception) {
                e.printStackTrace()
            }
            return
        }

        message?.let {
            it.message.reply(content).queue()
        }
    }

    protected fun replyOnInteractionChannel(content: String, delay: Long = 0) {
        val channel = interaction?.channel ?: message?.channel
        channel?.let {
            if (delay > 0) {
                it.sendTyping().queue()
                it.sendMessage(content).delay(Duration.ofSeconds(delay)).queue()
            } else {
                it.sendMessage(content).queue()
            }
        }
    }

    protected fun replyMessage(content: String, originalMessage: Message?)
    {
        val channel = interaction?.channel ?: message?.channel
        channel?.sendMessage(content)?.setMessageReference(originalMessage?.id)?.queue()
    }

    fun getCarolCommandName() = name
    fun getCarolCommandDescription() = description
    fun getCarolCommandOptions() = options
    fun getCarolCommandGuildOnly() = guild_only
}
package com.hades.discord.bot.carol.command

import dev.minn.jda.ktx.messages.send
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction
import java.time.Duration
import java.time.temporal.TemporalUnit
import java.util.concurrent.TimeUnit

open class CarolCommand(val name: String, val description: String, val options: List<CarolBaseCommandOptions>?, val guild_only: Boolean) {
    protected lateinit var interaction: SlashCommandInteraction
        private set

    companion object {
        private val allCommands = mutableListOf<CarolCommand>()

        fun dispatchInteraction(interaction: SlashCommandInteraction) {
            allCommands.firstOrNull { it.name == interaction.name }?.apply {
                this.interaction = interaction
                onCommandExecuted(interaction)
            }
        }
    }

    init {
        allCommands.add(this)
    }

    open fun onCommandExecuted(interaction: SlashCommandInteraction) {
        interaction.reply("Comando $name executado!").queue()
    }

    protected fun reply(content: String, ephemeral: Boolean = false) {
        if (::interaction.isInitialized) {
            interaction.reply(content).setEphemeral(ephemeral).queue()
        }
    }

    protected fun replyOnInteractionChannel(content: String, delay: Long = 0)
    {
        if (::interaction.isInitialized)
        {
            if (delay > 0) {
                interaction.channel.sendTyping().queue()
                interaction.channel.sendMessage(content).delay(Duration.ofSeconds(delay)).queue()
            }
            else
            {
                interaction.channel.sendMessage(content).queue()
            }
        }
    }

    fun getCarolCommandName() = name
    fun getCarolCommandDescription() = description
    fun getCarolCommandOptions() = options
    fun getCarolCommandGuildOnly() = guild_only
}
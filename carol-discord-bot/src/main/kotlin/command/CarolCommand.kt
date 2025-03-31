package com.hades.discord.bot.carol.command

import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction

open class CarolCommand(val name: String) {
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
}
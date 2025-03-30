package com.hades.discord.bot.carol.command.test

import com.hades.discord.bot.carol.command.CarolCommand
import com.hades.discord.bot.carol.command.CarolCommandsSettings

class CarolTestCommand constructor(comm: CarolCommand): CarolCommand(comm) {
    override fun onCommandExecuted(name: String) {
        super.onCommandExecuted(name)
        if (name == (CarolCommandsSettings.commands["test"]?.getName() ?: ""))
        {
            reply("bodia, esse é só um comando de teste")
        }
    }
}
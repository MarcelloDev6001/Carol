package com.hades.discord.bot.carol.command

import com.hades.discord.bot.carol.command.test.CarolTestCommand

class CarolCommandsSettings {
    companion object {
        val commands: Map<String, CarolCommand> = mapOf(
            "test" to CarolTestCommand()
        )
    }
}
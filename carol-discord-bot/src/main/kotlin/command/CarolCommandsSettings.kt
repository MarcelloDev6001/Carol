package com.hades.discord.bot.carol.command

import com.hades.discord.bot.carol.command.`fun`.CarolReplyCommand
import com.hades.discord.bot.carol.command.`fun`.CarolRule34Command
import com.hades.discord.bot.carol.command.people.CarolProfileCommand
import com.hades.discord.bot.carol.command.test.CarolTestCommand

class CarolCommandsSettings {
    companion object {
        val commands: Map<String, CarolCommand> = mapOf(
            "test" to CarolTestCommand(),
            "regra-34" to CarolRule34Command(),
            "reply" to CarolReplyCommand(),
            "perfil" to CarolProfileCommand()
        )
    }
}
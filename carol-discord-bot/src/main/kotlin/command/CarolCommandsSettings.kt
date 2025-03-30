package com.hades.discord.bot.carol.command

class CarolCommandsSettings {
    companion object {
        val commands: Map<String, CarolBaseCommand> = mapOf(
            "test" to CarolBaseCommand(
                name = "test",
                description = "just testing",
                options = null,
                guild_only = false
            )
        )
    }
}
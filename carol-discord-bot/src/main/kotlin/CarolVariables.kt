package com.hades.discord.bot.carol

import com.hades.discord.bot.carol.command.CarolCommand

class CarolVariables {
    companion object {
        val DEFAULT_XP_PER_GUILD: Int = 0
        val DEFAULT_COMMANDS_PER_GUILD: Array<CarolCommand> get() {return arrayOf(CarolCommand()) }
    }
}
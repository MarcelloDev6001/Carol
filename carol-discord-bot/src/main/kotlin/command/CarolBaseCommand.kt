package com.hades.discord.bot.carol.command

import net.dv8tion.jda.api.interactions.commands.OptionType
import org.jetbrains.annotations.NotNull
import net.dv8tion.jda.api.interactions.commands.OptionType.*

class CarolBaseCommand(
    @NotNull private var name: String,
    private var description: String,
    private var options: Array<CarolBaseCommandOptions>?,
    private var guild_only: Boolean
) {

    public fun getName(): String {return name}
    public fun getDescription(): String {return description}
    public fun getOptions(): Array<CarolBaseCommandOptions>? {return options}
    public fun getGuildOnly(): Boolean {return guild_only}
}

object CarolBaseCommandOptions {
    val name:String = ""
    val description:String = ""
    val type: OptionType = STRING
    val required: Boolean = false
    val autoComplete: Boolean = false
}

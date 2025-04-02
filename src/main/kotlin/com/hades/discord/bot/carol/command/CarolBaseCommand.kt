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

class CarolBaseCommandOptions (
    @NotNull private val _name:String = "",
    private val _description:String = "",
    private val _type: OptionType = STRING,
    private val _required: Boolean = false,
    private val _autoComplete: Boolean = false
) {
    fun getName(): String = _name
    fun getDescription(): String = _description
    fun getType(): OptionType = _type
    fun isRequired(): Boolean = _required
    fun isAutoComplete(): Boolean = _autoComplete
}

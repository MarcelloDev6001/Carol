package com.hades.discord.bot.carol.command.`fun`

import com.hades.discord.bot.carol.CarolProperties
import com.hades.discord.bot.carol.command.CarolBaseCommandOptions
import com.hades.discord.bot.carol.command.CarolCommand
import io.ktor.http.*
import kotlinx.coroutines.*
import net.dv8tion.jda.api.entities.Message
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.interactions.commands.OptionType
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction
import net.dv8tion.jda.api.requests.RestAction
import net.dv8tion.jda.api.requests.restaction.MessageCreateAction
import java.util.concurrent.TimeUnit
import kotlin.random.Random
import kotlin.random.nextInt

class CarolGamblingCommand : CarolCommand("gambling", "LET'S GO GAMBLING!!", emptyList(), true) {
    override fun onCommandExecuted(interaction: SlashCommandInteraction) {
        val treeRandomNumber: Array<Int> = arrayOf(
            Random.nextInt(0, 9),
            Random.nextInt(0, 9),
            Random.nextInt(0, 9)
        )
        reply("LET'S GO GAMBLING!!")
        val msg: Message = interaction.channel.sendMessage("${treeRandomNumber[0]}").complete()
        msg.editMessage(message?.message!!.contentRaw + "${treeRandomNumber[1]}").delay(1L, TimeUnit.SECONDS).queue()
        message?.message?.editMessage(message?.message!!.contentRaw + "${treeRandomNumber[2]}")?.delay(2L, TimeUnit.SECONDS)
        if (treeRandomNumber[0] == treeRandomNumber[1] && treeRandomNumber[0] == treeRandomNumber[2])
        {
            message?.message?.editMessage(message?.message!!.contentRaw + " :white_check_mark: ")?.delay(3L, TimeUnit.SECONDS)
            msg.channel.sendMessage("I CAN'T STOP WINNING!!! :money_mouth: :money_mouth: :money_mouth: ")
        }
        else
        {
            message?.message?.editMessage(message?.message!!.contentRaw + " :x: ")?.delay(3L, TimeUnit.SECONDS)
            msg.channel.sendMessage("OH DANG IT!!! :sob: :sob: :sob:")
        }
    }

    @OptIn(DelicateCoroutinesApi::class)
    override fun onMessageCommandExecuted(message: MessageReceivedEvent) {
        if (message.message.contentRaw.startsWith(CarolProperties.getPrefix() + getCarolCommandName())) {
            val treeRandomNumber: Array<Int> = arrayOf(
                Random.nextInt(0, 9),
                Random.nextInt(0, 9),
                Random.nextInt(0, 9)
            )
            reply("LET'S GO GAMBLING!!")
            GlobalScope.launch(Dispatchers.IO) {
                delay(400L)
                val msg: Message = message.channel.sendMessage("${treeRandomNumber[0]}").complete()
                delay(400L)
                msg.editMessage("${treeRandomNumber[0]} ${treeRandomNumber[1]}").queue()
                delay(400L)
                msg.editMessage("${treeRandomNumber[0]} ${treeRandomNumber[1]} ${treeRandomNumber[2]}").queue()
                delay(400L)

                if (treeRandomNumber[0] == treeRandomNumber[1] && treeRandomNumber[0] == treeRandomNumber[2])
                {
                    msg.editMessage("${treeRandomNumber[0]} ${treeRandomNumber[1]} ${treeRandomNumber[2]} :white_check_mark: ").queue()
                    delay(400L)
                    msg.channel.sendMessage("I CAN'T STOP WINNING!!! :money_mouth: :money_mouth: :money_mouth: ").queue()
                }
                else
                {
                    msg.editMessage("${treeRandomNumber[0]} ${treeRandomNumber[1]} ${treeRandomNumber[2]} :x: ").queue()
                    delay(400L)
                    msg.channel.sendMessage("OH DANG IT!!! :sob: :sob: :sob:").queue()
                }
            }
        }
    }
}
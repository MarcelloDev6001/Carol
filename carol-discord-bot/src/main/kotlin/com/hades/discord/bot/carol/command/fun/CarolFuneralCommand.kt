package com.hades.discord.bot.carol.command.`fun`

import com.hades.discord.bot.carol.CarolProperties
import com.hades.discord.bot.carol.command.CarolBaseCommandOptions
import com.hades.discord.bot.carol.command.CarolCommand
import com.hades.discord.bot.carol.image.CarolImageHelper
import net.dv8tion.jda.api.entities.Member
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.interactions.commands.OptionType
import net.dv8tion.jda.api.interactions.commands.SlashCommandInteraction
import net.dv8tion.jda.api.utils.FileUpload
import java.awt.image.BufferedImage

class CarolFuneralCommand : CarolCommand("funeral", "deixe seu respeito e gere uma imagem do funeral de um membro.", listOf(CarolBaseCommandOptions(
    "membro",
    "o azarado",
    OptionType.USER,
    true,
    false
)), true) {
    override fun onCommandExecuted(interaction: SlashCommandInteraction) {
        reply("tá bom")
        val member: Member? = interaction.getOption("membro")?.asMember

        if (member != null)
        {
            reply("um minutinho, calma ae")
            val funeralImage: BufferedImage = CarolImageHelper.loadImage("commands/funeral/base.jpg")
            var memberImage: BufferedImage = CarolImageHelper.loadImageFromWeb(member.effectiveAvatarUrl)
            memberImage = CarolImageHelper.resizeImage(memberImage, 110, 110)
            var memberImage2 = CarolImageHelper.resizeImage(memberImage, 46, 46)

            var finalImage: BufferedImage? = CarolImageHelper.combineImages(funeralImage, memberImage, arrayOf(59, 386))
            finalImage = CarolImageHelper.combineImages(funeralImage, memberImage2, arrayOf(609, 147))

            interaction.channel.sendMessage("e hoje aqui estamos no funeral de <@${member.id}>, um grande amigo nosso")
                .addFiles(
                    FileUpload.fromData(CarolImageHelper.convertToByteArray(finalImage), "funeral.png")
                ).queue()
        }
    }

    override fun onMessageCommandExecuted(message: MessageReceivedEvent) {
        if (message.message.contentRaw.startsWith(CarolProperties.getPrefix() + getCarolCommandName() + " ")) {
            val content: String = message.message.contentRaw.replace(CarolProperties.getPrefix() + getCarolCommandName() + " ", "")
            val member: Member? = message.message.guild.getMemberById(content.replace("<@", "").replace(">", "").trim().toLong())
            if (member == null)
            {
                reply("Insira um membro válido!")
                return
            }
            else
            {
                reply("um minutinho, calma ae")
                val funeralImage: BufferedImage = CarolImageHelper.loadImage("commands/funeral/base.jpg")
                var memberImage: BufferedImage = CarolImageHelper.loadImageFromWeb(member.effectiveAvatarUrl)
                memberImage = CarolImageHelper.resizeImage(memberImage, 110, 110)
                var memberImage2 = CarolImageHelper.resizeImage(memberImage, 46, 46)

                var finalImage: BufferedImage? = CarolImageHelper.combineImages(funeralImage, memberImage, arrayOf(59, 386))
                finalImage = CarolImageHelper.combineImages(finalImage!!, memberImage2, arrayOf(609, 147))

                message.channel.sendMessage("e hoje aqui estamos no funeral de <@${member.id}>, um grande amigo nosso")
                    .addFiles(
                        FileUpload.fromData(CarolImageHelper.convertToByteArray(finalImage), "funeral.png")
                    ).queue()
            }
        }
    }
}
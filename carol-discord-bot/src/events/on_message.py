import discord
from discord.ext import commands
import config
from src.automod import spam

spam_system = spam.SpamSystem()


class onMessageEvent:
    def __init__(self) -> None:
        pass

    async def do(self, message):
        userSpammed = await spam_system.check_for_spam(message.author, message)
        if userSpammed:
            try:
                await message.reply(
                    "Você está enviando mensagens muito rápido! Por favor, pare de spammar."
                )
            except Exception as e:
                await message.channel.send(
                    message.author.mention
                    + " Você está enviando mensagens muito rápido! Por favor, pare de spammar."
                )
            # spamSystem.deleteSpammedMessages(message.member);

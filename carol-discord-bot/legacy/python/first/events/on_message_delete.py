import discord
from config import config
import __main__ as main
import asyncio

async def on_message_delete(message):
    # if message.author.id == main.client.user.id:
    #     chan = await message.guild.fetch_channel(config.GUILDS_MAIN_CHANNEL[str(message.guild.id)])
    #     await chan.send("Quem é que tá apagando minhas mensagens?")
    return
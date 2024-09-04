import discord
from config import config
import __main__ as main
from utils import call as CallUtils

async def on_voice_state_update(member, before, after):
    if (member.id == 880090912657645569 or member.id == 722551879992606791) and after.channel is not None:
        general_channel = await member.guild.fetch_channel(1232110291320442941)
        await general_channel.send(f"{member.mention} está na call, isso é um milagre.")
    elif (member.id == 880090912657645569 or member.id == 722551879992606791) and after.channel is None:
        general_channel = await member.guild.fetch_channel(1232110291320442941)
        await general_channel.send(f"{member.mention} saiu da call, veremos ele só em 2037.")
    elif (member.id == main.client.user.id):
        if CallUtils.playing_music == True:
            CallUtils.musicqueue[member.guild.id] = []
            music_channel = await member.guild.fetch_channel(1220495785993572472)
            await music_channel.send("Fui kikada da call ;--;")
            CallUtils.playing_music = False

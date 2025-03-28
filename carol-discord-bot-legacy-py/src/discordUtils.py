import discord
from discord.ext import commands

def getIntents():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.guild_messages = True
    intents.message_content = True
    intents.members = True
    return intents
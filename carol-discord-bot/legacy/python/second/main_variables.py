import discord
import json
import __main__ as main

def get_discord_intents():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.typing = True
    intents.voice_states = True
    intents.members = True
    return intents
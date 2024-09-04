import discord
from discord import app_commands
from config import config
from events import on_message as on_message_event
from events import on_member_update as on_member_update_event
from events import on_voice_state_update as on_voice_state_update_event
from events import on_message_delete as on_message_delete_event
import main_variables as variables
import signal
import sys
import asyncio

points = variables.get_points()

level_and_xp = variables.get_level_and_xp()

class MyClient(discord.Client):

  def __init__(self, intents=variables.get_discord_intents(), **options):
    super().__init__(intents=intents, **options)

  async def on_ready(self):
    print('Logged in as {0.user}'.format(self))
    await tree.sync(guild=config.GUILDS[0])
    await self.change_presence(status=discord.Status.online,activity=discord.Activity(name=config.DEFAULT_STATUS))
    guild = await self.fetch_guild(config.GUILDS_IDS[0])
    self.main_channel = await guild.fetch_channel(1239701534137127074)
    await self.main_channel.send("Eae galera.")

  async def on_disconnect(self):
    print('disconnected as {0.user}'.format(self))
    await self.send_message_to_main_channel('Até a próxima.')

  async def on_member_update(self, before, after):
    await on_member_update_event.on_member_update(before, after)

  async def on_message(self, message):
    await on_message_event.on_message(message)
  
  async def on_message_delete(self, message):
    await on_message_delete_event.on_message_delete(message)
  
  async def on_voice_state_update(self, member, before, after):
    await on_voice_state_update_event.on_voice_state_update(member, before, after)

  async def send_message_to_main_channel(self, message: str):
    guild = await self.fetch_guild(config.GUILDS_IDS[0])
    self.main_channel = await guild.fetch_channel(1239701534137127074)
    await self.main_channel.send(message)

client = MyClient(intents=variables.get_discord_intents())
tree = app_commands.CommandTree(client)
import commands
import context_menu
# loop = asyncio.get_event_loop()
# for sig in (signal.SIGINT, signal.SIGTERM):
#   loop.add_signal_handler(sig, lambda: asyncio.ensure_future(shutdown()))

# async def shutdown():
#   await client.send_message_to_main_channel('Até a próxima.')
#   await client.close()
#   sys.exit(0)

client.run(config.TOKEN)

import discord
from discord.ext import commands
import config
from src import discordUtils
from src.events import on_message

on_message_event = on_message.onMessageEvent()

bot = commands.Bot(command_prefix="c.", intents=discordUtils.getIntents())


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user.name}")


@bot.command()
async def ping(ctx):
    await ctx.reply("Pong!")


@bot.command()
async def hello(ctx):
    await ctx.reply(f"Hello, {ctx.author.name}!")


@bot.event
async def on_message(message):
    await on_message_event.do(message)


bot.run(config.token)

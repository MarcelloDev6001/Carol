import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from discord import FFmpegPCMAudio
import __main__ as main
from config import config

tree = main.tree

@tree.context_menu(name="Teste de menu de contexto", guilds=config.GUILDS)
async def do_context_menu(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message("Mensagem top.", ephemeral=True)

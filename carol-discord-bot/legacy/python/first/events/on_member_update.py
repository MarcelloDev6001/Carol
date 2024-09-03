import discord
from config import config
import __main__ as main
import asyncio

async def on_member_update(before, after):
    # print("Usuário com nome trocado: " + str(after.name) + " (" + str(before.display_name) + " -> " + str(after.display_name) + ")")
    # if before.id == main.client.user.id:
    #   chan = await after.guild.fetch_channel(config.GUILDS_MAIN_CHANNEL[str(after.guild.id)])
    #   for unnapname in config.unnapropriatenames:
    #     if unnapname in after.display_name.lower():
    #       await chan.send("<@1218305183956860930> <@779727883228020756> não gostei muito de meu novo nome :cry:, poderiam trocar pfv?")
    #       def check(msg):
    #         return (msg.author.id == 1218305183956860930 or msg.author.id == 779727883228020756 or msg.author.id == 1221946490453360843) and msg.channel == chan and ("fds" in response.content.lower() or "fodas" in response.content.lower() or "fdas" in response.content.lower())

    #       try:
    #         response = await main.client.wait_for('message', timeout=60.0, check=check)
    #         if "fds" in response.content.lower() or "fodas" in response.content.lower() or "fdas" in response.content.lower():
    #           await response.reply("Fodase você, arrombado do krl.")
    #       except asyncio.TimeoutError:
    #         # await ctx.send("Tempo limite atingido. Nenhum nome foi fornecido.")
    #         await chan.send("Áh, vão se fuder ent, prr.")

      # await bot.owner.send(f"O nome do bot foi alterado para '{after.name}'. Alteração revertida.")
  return
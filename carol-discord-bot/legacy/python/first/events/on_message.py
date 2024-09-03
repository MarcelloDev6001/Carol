import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from discord import FFmpegPCMAudio
import asyncio
from config import config
from utils import call
from utils import image
from utils import roblox
from googleapiclient.discovery import build
from PIL import Image, ImageSequence, ImageDraw, ImageFont
import requests
import random
import re
import json
import datetime
import time
import __main__ as main
import main_variables as variables
import openai

openai.api_key = "sk-proj-W4qTnniLvtLC5wchTn6JT3BlbkFJmkDawO25NRfFMsWyBAKV"

INTERVALO = 10
tempos_membros = {}

time_window_milliseconds = 20000
max_msg_per_window = 3
author_msg_times = {}
last_spam_check_message = None

hades_msg_counter = 0

async def on_message(message):
    global hades_msg_counter
    # print(message.content)
    # print(main.client.user.mention)
    if message.author == main.client.user or message.author.bot:
      return
    
    if message.author.id == 779727883228020756:
      # print("Hades message")
      hades_msg_counter = hades_msg_counter + 1
      if hades_msg_counter > 6:
        await message.reply("Aí pra vc ó")
        await message.channel.send("https://cdn.discordapp.com/attachments/1239701534137127074/1241554387671711806/GNuuPpoX0AAbCHI.png?ex=664a9f20&is=66494da0&hm=bbeb44696ba5d88f699c3d2f147c75d2fae03192a54a366b123a7b8cf52cde2c&")
        hades_msg_counter = 0

    if "https://cdn.discordapp.com/attachments/1239701534137127074/1241849779210813590/GM2Ml4XXsAAn4ox.jpg?ex=664bb23b&is=664a60bb&hm=d028cbf44e66873f987651c337d911178b7e465c7c4834aa4ed5d552c0ac8658&" in message.content.lower():
      await message.reply("vtnc, essa prr toda hora.")

    await check_for_content_for_some_reason(message)
    
    await check_for_spam(message)
    
    if main.points.get(str(message.guild.id), None) is None:
      main.points[str(message.guild.id)] = {}
    
    main.points[str(message.guild.id)][str(message.author.id)] = main.points.get(str(message.guild.id), {}).get(str(message.author.id), 0) + 1

    if message.channel.id == 1239717640373669912:
      if len(message.attachments) > 0:
        print("reacting for avaliadoresdeskins")
        emojis = ["\u0030\u20E3", "\u0031\u20E3", "\u0032\u20E3", "\u0033\u20E3", 
                "\u0034\u20E3", "\u0035\u20E3", "\u0036\u20E3", "\u0037\u20E3", 
                "\u0038\u20E3", "\u0039\u20E3", "\U0001F4AF"]
      
        for emoji in emojis:
          await message.add_reaction(emoji)
          await asyncio.sleep(0.6)
      else:
        await message.delete()
        return

    if message.content.lower().startswith("q.clear"):
      await try_clear_chat(message)

    # if message.guild is not None:  # Verifica se a mensagem foi enviada em um servidor (guild)
    #   if "discord.gg" in message.content.lower():  # Verifica se o conteúdo da mensagem contém um convite para servidor do Discord
    #     await message.delete()  # Deleta a mensagem
    #     await message.channel.send(f"{message.author.mention}, é proibido divulgar servidores aqui.")  # Envia uma mensagem de aviso

    if message.guild is not None and len(message.mentions) == 0: #isn't a message from DMs and not marking someone (to avoid spam)
      await update_score_and_xp(message)

    dachannel = message.channel.id
    imgcount = 0
    for chan in config.membersrooms:
      if chan == dachannel:
        # damessages = async for message.channel.history(limit=100)
        async for msg in message.channel.history(limit=100):
          if msg.attachments is not None or ".mp4" in msg.content or ".png" in msg.content or ".jpg" in msg.content:
            imgcount += len(msg.attachments)

        if imgcount % 5 == 0 and imgcount > 0:
          await message.channel.send(message.author.mention + ", você já mandou " +
                                    str(imgcount) + " imagens neste canal.")

    if message.guild.id == 1221946490453360843 and (len(message.attachments) > 0 or ("https://" in message.content and (".png" in message.content or ".jpg" in message.content or ".jpeg" in message.content or ".swg" in message.content or "gif" in message.content.lower()))) and config.membersrooms.get(message.channel.id, {}) == {} and message.channel.id != 1221517349996204123 and message.channel.id != 1221517385845047367:
      await message.reply("https://tenor.com/view/pelo-smash-smash-right-there-gif-20845267")

def check_xp(nextlevel, xp):
    if (xp / 1000) >= nextlevel:
        return True
    return False

async def send_xp_message(message: discord.Message, member: discord.Member, newxp: float, newlevel: float, channel: discord.TextChannel):
    background = Image.open("MemeImages/jornal/base.png")
    # background = image.draw_text_image(background, member.display_name, (149, 134), (641, 60), "fonts/arial.ttf", 51, (0,0,0), "center")
    avatar = image.download_avatar(member.avatar.url).resize((216, 208))
    background = image.draw_text_image(background, f"{message.created_at.day}/{message.created_at.month}/{message.created_at.year}", (82, 99), (168, 29), "fonts/arial.ttf", 21, (0,0,0), "left")
    background = image.draw_text_image(background, "Carol", (342, 99), (168, 29), "fonts/arial.ttf", 21, (0,0,0), "left")
    background = image.draw_text_image(background, member.display_name, (49, 148), (216, 29), "fonts/arial.ttf", 21, (0,0,0), "left")
    background = image.draw_text_image(background, f"Acabou de evoluir para o\nnível {newlevel} com um XP de \n{newxp}.", (275, 159), (245, 20), "fonts/arial.ttf", 18, (0,0,0), "left")
    background.paste(avatar, (49, 179))
    # background = image.draw_text_image(background, f"Acabou de evoluir de nível.\n\n\nLevel atual: {newlevel}\nPróximo level: {newlevel+1}\nXP atual: {newxp}\nXP para o próximo lével:{(newlevel+1)*1000}", (170, 561), (584, 275), "fonts/arial.ttf", 32, (0,0,0), "center")
    background.save(f"MemeImages/jornal/{member.id}_level_up_temp.png")
    with open(f"MemeImages/jornal/{member.id}_level_up_temp.png", "rb") as img_file:
        await channel.send(member.mention, file=discord.File(img_file, f"{member.id}_level_up_temp.png"))

#structure of this thing:
# {
#   "author_id": {
#     "messages": {"message_id": {
#         "curr_time": int,
#         "content": str
#       }
#     },
#     "warned_times": 1
#   }
# }

async def check_for_spam(ctx):
    if ctx.author.top_role.id in config.ADM_ROLES: # is a adm
      return

    global author_msg_counts
    global last_spam_check_message
    if last_spam_check_message == None:
      last_spam_check_message = ctx

    author_id = ctx.author.id
    # Get current epoch time in milliseconds
    curr_time = datetime.datetime.now().timestamp() * 1000

    if author_msg_times.get(author_id, False) == False:
      author_msg_times[author_id] = {}

    # Make empty list for author id, if it does not exist
    if not author_msg_times.get(author_id, {}).get("messages", False):
      author_msg_times[author_id]["messages"] = {}

    if ctx.content == last_spam_check_message.content:
      # Append the time of this message to the users list of message times
      author_msg_times[author_id]["messages"][str(ctx.id)] = {"curr_time": curr_time, "content": ctx.content.lower()}

    # Find the beginning of our time window.
    expr_time = curr_time - time_window_milliseconds

    try:
      # Remove all the expired messages times from our list
      for msg in author_msg_times[author_id]["messages"]:
        if author_msg_times[author_id]["messages"][msg]["curr_time"] < expr_time:
          # author_msg_times[author_id]["messages"].remove(str(ctx.id))
          del author_msg_times[author_id]["messages"][msg]
      # ^ note: we probably need to use a mutex here. Multiple threads
      # might be trying to update this at the same time. Not sure though.
    except:
      author_msg_times[author_id]["messages"] = {}

    if len(author_msg_times[author_id]["messages"]) > max_msg_per_window:
      await ctx.channel.send(f"{ctx.author.mention} para de spam.")
      author_msg_times[author_id]["warned_times"] = author_msg_times[author_id].get("warned_times", 0) + 1
      duration = datetime.timedelta(seconds=(60*author_msg_times[author_id].get("warned_times", 1)))
      await ctx.author.timeout(duration, reason="Spammou dms")

    last_spam_check_message = ctx

async def check_for_content_for_some_reason(message):
  if "gosto d" in message.content.lower() or "gostar" in message.content.lower() or "sentar" in message.content.lower():
    await message.reply(":face_with_raised_eyebrow: :index_pointing_at_the_viewer: :rainbow_flag:")

  if "skil" in message.content.lower() and "issue" in message.content.lower():
    await message.reply("https://tenor.com/view/smg4-smg4skill-issue-skill-issue-smg4mario-smg4skill-gif-26104493")

  if message.channel.id == 1221517349996204123 or message.channel.id == 1221517385845047367:
    await message.add_reaction('\U0001F1F8')  # React with letter S
    await message.add_reaction('\U0001F1F5')  # React with letter P

  if ('<@739211327826034770>' in message.content
      or 'galego' in message.content.lower()
      or 'galega' in message.content.lower()) and message.author.id == 779727883228020756:
    rand_num = random.randint(0, len(config.oneblockedmessagegifs) - 1)
    await message.reply(config.oneblockedmessagegifs[rand_num])

async def try_clear_chat(message):
  try:
    amount = int(message.content.replace("q.clear", ""))
  except:
    amount = None
    
  if config.membersrooms.get(message.channel.id, {}) != {}:
    # if message.channel.id == membroom or message.author.top_role.id == 1218327147152674936 or message.author.top_role.id == 1224143232322244618 or message.author.top_role.id == 1218327392800473168:
    membownerroom = await message.guild.fetch_member(config.membersrooms[message.channel.id]["owner"])
    if message.author.id == membownerroom.id:
      await message.delete()
      
      contador = 0
      async for _ in message.channel.history(limit=amount):
          contador += 1
      
      await message.channel.purge(limit=contador)
    else:
      await message.reply("Você não tem permissão para usar esse comando.")
  else:
    if message.author.top_role.id in config.ADM_ROLES:
    # if message.channel.id == membroom or message.author.top_role.id == 1218327147152674936 or message.author.top_role.id == 1224143232322244618 or message.author.top_role.id == 1218327392800473168:
      await message.delete()
      
      contador = 0
      async for _ in message.channel.history(limit=amount):
          contador += 1
      
      await message.channel.purge(limit=contador)
    else:
      await message.reply("Você não tem permissão para usar esse comando.")

async def update_score_and_xp(message):
  user_id = str(message.author.id)
  variables.save_points(message.author.id, message.guild.id)

  xp_multiplier = 1
  if message.author.top_role is not None and message.author.top_role.id in config.ROLES_XP_MULTIPLIER:
    xp_multiplier = config.ROLES_XP_MULTIPLIER[message.author.top_role.id]
  if main.level_and_xp.get(str(message.guild.id)) is None:
    main.level_and_xp[str(message.guild.id)] = {}
  if main.level_and_xp[str(message.guild.id)].get(user_id) is None:
    main.level_and_xp[str(message.guild.id)][user_id] = {"level": 0, "xp": 0}
  # level_and_xp[user_id]["level"] = level_and_xp.get(user_id, 0).get("level", 0)
  main.level_and_xp[str(message.guild.id)][user_id]["xp"] = main.level_and_xp[str(message.guild.id)][user_id].get("xp", 0) + (1 * xp_multiplier)

  if check_xp(main.level_and_xp.get(str(message.guild.id), {}).get(user_id, 0).get("level", 0) + 1, main.level_and_xp.get(str(message.guild.id), {}).get(user_id, 0).get("xp", 0)):
    news_channel = await message.guild.fetch_channel(config.GUILDS_NEWS_CHANNEL[str(message.guild.id)])
    main.level_and_xp[str(message.guild.id)][user_id]["level"] = main.level_and_xp[str(message.guild.id)][user_id].get("level", 0) + 1
    await send_xp_message(message, message.author, main.level_and_xp[str(message.guild.id)][user_id]["xp"], main.level_and_xp[str(message.guild.id)][user_id]["level"], news_channel)

  with open("data/XP.json", 'w') as f:
    json.dump(main.level_and_xp, f, indent=4)

first_message = ""
second_message = ""

async def try_learn(message):
  def check(msg):
    return (msg.author.id != message.author.id)

  try:
    response = await main.client.wait_for('message', timeout=60.0, check=check)
    # if "fds" in response.content.lower() or "fodas" in response.content.lower() or "fdas" in response.content.lower():
      # await response.reply("Fodase você, arrombado do krl.")
    second_message = response.content
  except asyncio.TimeoutError:
    # await ctx.send("Tempo limite atingido. Nenhum nome foi fornecido.")
    # await chan.send("Áh, vão se fuder ent, prr.")
    return
  first_message = message.content
  
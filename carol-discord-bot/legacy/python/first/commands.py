import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from discord import FFmpegPCMAudio
# from app_commands import Transform, PointTransformer
import typing
import asyncio
from config import config
from utils import call
from utils import image
from utils import roblox
from utils import font_to_text as font_converter
from utils import str as StrUtils
from utils import discord as DiscordUtils
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
import inspect
import io
# from robloxapi import Client as RobloxClient

tree = main.tree

guildid = 1218323333096013924

@tree.command(name="avatar",description="Consiga o avatar de alguém")
async def get_avatar(interaction, member: discord.Member):
    await interaction.response.send_message(member.avatar.url, ephemeral=True)

@tree.command(name="tts",description="Faça o bot falar o que vc quiser na call")
async def call_tts(interaction, audio: str):
    text_map = variables.get_text_map_from_json("TextsConfig", guild_id=interaction.guild.id)["commands"]["tts"]
    # for mencionado in message.mentions:
    #   aud = aud.replace(f'<@{mencionado.id}>', "@" + mencionado.display_name)
    if audio is None or audio == '':
        await interaction.response.send_message(text_map["invalid_text"], ephemeral=True)
    elif interaction.user.voice is None or interaction.user.voice.channel is None:
        await interaction.response.send_message(text_map["un_voiced"], ephemeral=True)
    else:
        call.criar_audio(audio.replace("/", "barra").replace("\\", "barra inversa"), idioma='pt-br', fileoutput=str(interaction.id))
        voice_channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client

        # await interaction.message.add_reaction('✅')

        if not voice_client:
            await voice_channel.connect()
        voice_client = interaction.guild.voice_client

        try:
            source = FFmpegPCMAudio("AudiosMemes/tts/" + str(interaction.id) + ".mp3", executable="C:/ffmpeg/ffmpeg.exe")  # Substitua pelo caminho do seu arquivo de áudio
            voice_client.play(source)
            await interaction.response.send_message(text_map["success"])
        except Exception as e:
            await interaction.response.send_message(text_map["fail"].replace("{error}", e), ephemeral=True)

        # Espera até que o áudio termine de tocar
        while interaction.guild.voice_client.is_playing():
            await asyncio.sleep(1)

        # Desconecta o bot após o áudio terminar
        await interaction.guild.voice_client.disconnect()

call_sounds = []
id = 0
for com in config.TEXTO_AUDIO_MAP:
    call_sounds.append(com.lower())

async def soundas_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> typing.List[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name=sound, value=sound)
        for sound in call_sounds if current.lower() in sound.lower()
    ]

@tree.command(name="call-som", description="toque um som na call")
# @app_commands.choices(soundas=call_sounds)
@app_commands.autocomplete(soundas=soundas_autocomplete)
async def call_cmd(interaction: discord.Interaction, soundas: str):
    text_map = variables.get_text_map_from_json("TextsConfig", guild_id=interaction.guild.id)["commands"]["call-som"]
    await call.call_cmd(interaction, soundas, text_map)

@tree.command(name="music-play", description="Toca uma música na call.")
async def play_music_call(interaction: discord.Interaction, music: str):
    await call.play_music_call(interaction=interaction, music=music)

@tree.command(name="music-skip", description="Pula a música atual.")
async def skip_music(interaction: discord.Interaction):
    await call.skip_music(interaction=interaction)

@tree.command(name="music-list", description="Veja a lista de músicas.")
async def see_list_music(interaction: discord.Interaction):
    await call.see_list_music(interaction=interaction)

@tree.command(name="music-stop", description="Para a música atual")
async def stop_music_call(interaction: discord.Interaction):
    await call.stop_music_call(interaction=interaction)

@tree.command(name="music-volume", description="Seta o volume da música atual")
@app_commands.describe(volume="Um valor entre 0 e 1000 (o padrão é 100)")
async def set_music_volume(interaction: discord.Interaction, volume: app_commands.Range[float, 0, 1000]):
    await call.set_music_volume(interaction=interaction, volume=volume)

@tree.command(name="hide-away", description="50K Imagem :skull:")
async def create_hide_away(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE, ephemeral=True)
    image.create_hide_away_img(interaction.user.avatar.url, membro.avatar.url, "MemeImages/hideaway/" + str(interaction.user.id) + "-" + str(membro.id) + ".png")
    with open("MemeImages/hideaway/" + str(interaction.user.id) + "-" + str(membro.id) + ".png", 'rb') as image_file:
        await interaction.channel.send(interaction.user.mention + " " + membro.mention + " :skull:", file=discord.File(image_file, str(interaction.user.id) + "-" + str(membro.id) + ".png", spoiler=True))

@tree.command(name="pesquisar", description="Pesquise uma imagem")
@app_commands.describe(quantidade="Um valor entre 1 e 10 (o padrão é 1)")
async def search_img(interaction: discord.Interaction, query: str, quantidade: app_commands.Range[int, 1, 10]):
    for hentword in config.hentaiswords:
        if hentword in query.lower() and not interaction.channel.nsfw:
            await interaction.response.send_message("Não vou fornecer imagens de Hentai pra vc nesse chat, burrão.", ephemeral=True)
            return
    if quantidade < 1 or quantidade > 10:
        await interaction.response.send_message("Tem que ser uma quantidade entre 1 e 10.", ephemeral=True)
        return
    elif quantidade != 1 and (interaction.channel.id == 1221517385845047367 or interaction.channel.id == 1221517349996204123):
       await interaction.response.send_message("Esse canal só permite pesquisar 1 imagem.", ephemeral=True) 
    await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE)
    imgsfound = await image.search_image(query, amount=quantidade, isnsfw=False)
    if imgsfound[0] == "":
        await interaction.edit_original_response(content="Não achei nada ;--;")
        return
    emblist = []
    msg = interaction.user.mention + ", resultados para " + query + ": (" + str(len(imgsfound)) + ")\n"
    for i in range(len(imgsfound)):
        embed = discord.Embed(title="Resultado", description="")
        embed.set_image(url=imgsfound[i])
        emblist.append(embed)
        msg = msg + "||" + imgsfound[i] + "||\n"
    # await interaction.channel.send(interaction.user.mention, embed=embed)
    message = await interaction.channel.send(msg, embeds=emblist)
    # with open("MemeImages/hideaway/search_result.png", 'rb') as image_file:
        # await interaction.channel.send(interaction.user.mention+" Resultado da pesquisa:", file)
    if message.channel.id == 1221517349996204123 or message.channel.id == 1221517385845047367:
        await message.add_reaction('\U0001F1F8')  # React with letter S
        await message.add_reaction('\U0001F1F5')  # React with letter P

@tree.command(name="rule-34", description="Pesquise uma imagem da rule 34 :face_with_raised_eyebrow: ")
async def rule_34_search(interaction: discord.Interaction, query: str, quantidade: app_commands.Range[int, 1, 25]):
    if not interaction.channel.nsfw:
        await interaction.response.send_message("Não vou fornecer imagens de Rule 34 pra vc nesse chat, burrão.", ephemeral=True)
        return
    if quantidade < 1 or quantidade > 25:
        await interaction.response.send_message("Tem que ser uma quantidade entre 1 e 25.", ephemeral=True)
        return
    elif quantidade != 1 and (interaction.channel.id == 1221517385845047367 or interaction.channel.id == 1221517349996204123):
       await interaction.response.send_message("Esse canal só permite pesquisar 1 imagem.", ephemeral=True) 
       return
    await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE)
    imgsfound = await image.search_image(query, amount=quantidade, isnsfw=True)
    if imgsfound[0] == "":
        await interaction.edit_original_response(content="Não achei nada ;--;")
        return
    emblist = []
    msg = interaction.user.mention + ", resultados para " + query + ": (" + str(len(imgsfound)) + ")\n"
    if len(imgsfound) > 10:
        for i in range(len(imgsfound)):
            msg = msg + "||" + imgsfound[i] + "||\n"
            embed = discord.Embed(title="Resultado", description="")
            embed.set_image(url=imgsfound[i])
            emblist.append(embed)
            if i % 10 == 0:
                message = await interaction.channel.send(msg, embeds=emblist)
                msg = ""
                emblist = []
            elif i == len(imgsfound):
                message = await interaction.channel.send(msg)
        # message = await interaction.channel.send(msg)
    else:
        for i in range(len(imgsfound)):
            embed = discord.Embed(title="Resultado", description="")
            embed.set_image(url=imgsfound[i])
            emblist.append(embed)
            msg = msg + "||" + imgsfound[i] + "||\n"
        message = await interaction.channel.send(msg, embeds=emblist)
    # await interaction.channel.send(interaction.user.mention, embed=embed)
    # with open("MemeImages/hideaway/search_result.png", 'rb') as image_file:
        # await interaction.channel.send(interaction.user.mention+" Resultado da pesquisa:", file)
    if message.channel.id == 1221517349996204123 or message.channel.id == 1221517385845047367:
        await message.add_reaction('\U0001F1F8')  # React with letter S
        await message.add_reaction('\U0001F1F5')  # React with letter P

@tree.command(name="profile", description="Veja o perfíl e informações de você ou de outra pessoa.")
async def see_profile(interaction: discord.Interaction, membro: discord.Member):
    fields = {
        "Data de criação da conta": {"value": f"<t:{int(membro.created_at.timestamp())}:D> (<t:{int(membro.created_at.timestamp())}:R>)", "inline": False},
        "Data de entrana no server": {"value": f"<t:{int(membro.joined_at.timestamp())}:D> (<t:{int(membro.joined_at.timestamp())}:R>)", "inline": False},
        "ID": {"value": str(membro.id), "inline": False},
        "Menção": {"value": membro.mention, "inline": False},
        "Nickname": {"value": membro.nick, "inline": False},
        "Maior Cargo": {"value": membro.top_role.mention, "inline": False}
    }
    embed = DiscordUtils.auto_embed(title="Perfíl de " + membro.display_name, color=membro.colour, thumbnail=membro.avatar.url, artist={"bem bonito né?": {"url": "", "icon": ""}}, fields=fields)
    # embed = discord.Embed(title="Perfíl de " + membro.display_name, color=membro.colour)
    # embed.set_author(name="Bem bonito, né?")
    # embed.add_field(name="Data de criação da conta", value=f"<t:{str(membro.created_at)}:D> (<t:{str(membro.created_at)}:R>)", inline=False)
    # embed.add_field(name="Data de entrana no server", value=f"<t:{str(membro.joined_at)}:D> (<t:{str(membro.joined_at)}:R>)", inline=False)
    # embed.add_field(name="ID", value=str(membro.id), inline=False)
    # embed.add_field(name="Menção", value=membro.mention, inline=False)
    # embed.add_field(name="Nickname", value=membro.nick, inline=False)
    # embed.add_field(name="Maior Cargo", value=membro.top_role.mention, inline=False)
    # embed.set_thumbnail(url=membro.avatar.url)
    await interaction.response.send_message(embed=embed)

@tree.command(name="smash-or-pass", description="Come ou passa? ( ͡° ͜ʖ ͡°)")
async def smash_or_pass(interaction: discord.Interaction):
    if interaction.channel.id == 1221517385845047367: # nsfw channel
        await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE)
        with open("data/ficcharacterslist.txt", 'r') as txt_file:
            chars_list = txt_file.readlines()
            char_nam = random.choice(chars_list).replace("b'", "").replace("'", "").strip().replace("\r", "").replace("\n", "")
        print("Query: " + char_nam)
        
        imgfound = await image.search_image((char_nam.replace("\r", "").replace("\n", "")), amount=25, isnsfw=True)
        randnum = random.randint(0, len(imgfound) - 1)
        if imgfound[0] == "":
            await interaction.edit_original_response(content="Não achei nada ;--;")
            return
        embed = discord.Embed(title="Smash or Pass?", description=f"{char_nam}")
        embed.set_image(url=imgfound[randnum])
        msg = await interaction.channel.send(f"||{imgfound[randnum]}||", embed=embed)
        await msg.add_reaction('\U0001F1F8')  # React with letter S
        await msg.add_reaction('\U0001F1F5')  # React with letter P
        # await interaction.response.send_message("Em desenvolvimento ainda...", ephemeral=True)
    elif interaction.channel.id == 1221517349996204123: #sfw chat
        await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE)
        with open("data/ficcharacterslist.txt", 'r') as txt_file:
            chars_list = txt_file.readlines()
            char_nam = random.choice(chars_list).replace("b'", "").replace("'", "").strip().replace("\r", "").replace("\n", "")
        print("Query: " + char_nam)
        
        imgfound = await image.search_image(char_nam.replace("\r", "").replace("\n", ""), amount=10, isnsfw=False)
        if imgfound[0] == "":
            await interaction.edit_original_response(content="Não achei nada ;--;")
            return
        embed = discord.Embed(title="Smash or Pass?", description=char_nam)
        embed.set_image(url=imgfound[random.randint(0, len(imgfound) - 1)])
        msg = await interaction.channel.send(embed=embed)
        await msg.add_reaction('\U0001F1F8')  # React with letter S
        await msg.add_reaction('\U0001F1F5')  # React with letter P
    else:
        await interaction.response.send_message("Smash or Pass não funciona nesse canal.\nUse <#1221517349996204123> ou <#1221517385845047367> para isso", ephemeral=True)

@tree.command(name="ship", description="Shippe 2 pessoas.")
async def ship_peoples(interaction: discord.Interaction, membro: discord.Member, membro2: discord.Member):
    await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE)
    random.seed(membro.id + membro2.id)
    percent = random.randrange(0, 100)
    if percent >= 50:
        image.create_ship_img("base_plus50.png", membro.avatar.url, [197, 80, 78, 78], membro2.avatar.url, [277, 119, 86, 86], "MemeImages/ship/ship-" + str(membro.id) + "-" + str(membro2.id) + ".png")
        with open("MemeImages/ship/ship-" + str(membro.id) + "-" + str(membro2.id) + ".png", "rb") as img_file:
            await interaction.channel.send(membro.mention + " e " + membro2.mention + " Dariam um casal razoável. (" + str(percent) + "%)", file=discord.File(img_file, "ship-" + str(interaction.user.id) + "-" + str(membro.id) + ".png"))
    else:
        image.create_ship_img("base_minus50.jpg", membro.avatar.url, [200, 161, 45, 45], membro2.avatar.url, [711, 125, 60, 60], "MemeImages/ship/ship-" + str(membro.id) + "-" + str(membro2.id) + ".png")
        with open("MemeImages/ship/ship-" + str(membro.id) + "-" + str(membro2.id) + ".png", "rb") as img_file:
            await interaction.channel.send(membro.mention + " e " + membro2.mention + " Dariam um casal ruim. (" + str(percent) + "%)", file=discord.File(img_file, "ship-" + str(membro.id) + "-" + str(membro2.id) + ".png"))

@tree.command(name="roblox-meme", description="Faça um meme do roblox.")
async def create_roblox_meme(interaction: discord.Interaction, texto1: str, username1: str, texto2: str, username2: str):
    await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE)
    url = f"https://www.roblox.com/users/profile?username={username1}"
    response = requests.get(url)
    user_id = re.search(r'\d+', response.url).group()
    avatar1 = image.download_avatar(roblox.get_roblox_avatar_url(id=user_id)).resize((203,203))
    avatar1 = image.adicionar_fundo_branco(avatar1)
    # avatar1 = replace_image_color(avatar1, rgb_org=(0,0,0,0), new_color=(255,255,255,255))
    url2 = f"https://www.roblox.com/users/profile?username={username2}"
    response2 = requests.get(url2)
    user_id2 = re.search(r'\d+', response2.url).group()
    avatar2 = image.download_avatar(roblox.get_roblox_avatar_url(id=user_id2)).resize((203,203))
    avatar2 = image.adicionar_fundo_branco(avatar2)
    # avatar2 = replace_image_color(avatar2, rgb_org=(0,0,0,0), new_color=(255,255,255,255))

    background = Image.open("MemeImages/robloxmemes/custom/base.png")
    background.paste(avatar1, (102,194))
    background.paste(avatar2, (431, 194))
    
    font = ImageFont.truetype("fonts/arial.ttf", 20)
    draw = ImageDraw.Draw(background)
    draw.text((118, 10), texto1, fill=(0,0,0), font=font, anchor=None, spacing=4, align='center')
    draw.text((447, 10), texto2, fill=(0,0,0), font=font, anchor=None, spacing=4, align='center')

    background.save("MemeImages/robloxmemes/custom/" + str(interaction.id) + "_temp.png")

    with open("MemeImages/robloxmemes/custom/" + str(interaction.id) + "_temp.png", "rb") as img_file:
        await interaction.channel.send("", file=discord.File(img_file, str(interaction.id) + "_temp.png"))

@tree.command(name="pontos", description="Veja quantos pontos um usuário tem.")
async def check_points(interaction: discord.Interaction, membro: discord.Member):
    num_pontos = main.points.get(str(interaction.guild.id), {}).get(str(membro.id), 0)
    await interaction.response.send_message(
        f'{membro.mention} tem {num_pontos} pontos!')
        
@tree.command(name="level", description="Veja qual o level atual e o XP atual de alguém.")
async def check_level(interaction: discord.Interaction, membro: discord.Member):
    levelmap = main.level_and_xp.get(str(interaction.guild.id), {}).get(str(membro.id), {"level": 0, "xp": 0})
    await interaction.response.send_message(
        f'{membro.mention} está com o level {levelmap["level"]} e um XP de {levelmap["xp"]}!')
    
@tree.command(name="rank-pontos", description="Veja as 5 pessoas com mais pontos no servidor.")
async def rank_points(interaction: discord.Interaction):
    sorted_values = sorted(main.points[str(interaction.guild.id)].items(), key=lambda x: x[1], reverse=True)
        
    # Obter os top 3 valores
    top3 = sorted_values[:5]

    rank_message_str = "Top 5 Pessoas com mais pontos no servidor:\n\n"

    membid = 0
    for variable, value in top3:
        membid = membid + 1
        # print(f"Variável {variable}: {value}")
        rank_message_str = rank_message_str + str(membid) + ": <@" + variable + "> com " + str(value) + " pontos.\n"

    await interaction.response.send_message(rank_message_str)

@tree.command(name="meme-button", description="Gere um daqueles memes com um botão vermelho e um botão azul.")
async def generate_red_blue_meme(interaction: discord.Interaction, texto1: str, texto2: str, membro: discord.Member):
    await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE)
    avatar1 = image.download_avatar(membro.avatar.url).resize((168,168))

    background = Image.open("MemeImages/twobuttons/idk/base.jpg")
    background.paste(avatar1, (226,523))
    
    font = ImageFont.truetype("fonts/arial.ttf", 22)
    draw = ImageDraw.Draw(background)
    draw.text((65, 107), texto1, fill=(0,0,0), font=font, anchor=None, spacing=4, align='center')
    draw.text((278, 71), texto2, fill=(0,0,0), font=font, anchor=None, spacing=4, align='center')

    background.save("MemeImages/twobuttons/idk/" + str(interaction.id) + "_temp.png")

    with open("MemeImages/twobuttons/idk/" + str(interaction.id) + "_temp.png", "rb") as img_file:
        await interaction.channel.send("", file=discord.File(img_file, str(interaction.id) + "_temp.png"))

@tree.command(name="enquete", description="Faça uma enquete para votação de algo")
@app_commands.checks.has_any_role(1218327147152674936, 1224143232322244618, 1218327392800473168)
@app_commands.describe(opcoes="As opções que vai ter (tem que ser separadas por vírgula).")
async def enquete(interaction, pergunta: str, opcoes: str):
    await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE, ephemeral=True)
    opcoes = opcoes.split(',')
    embed = discord.Embed(title="Enquete", description=pergunta, color=0x00ff00)
    
    opcoes_str = ""
    for i, opcao in enumerate(opcoes):
        opcoes_str += f"{i + 1}. {opcao}\n"
    
    embed.add_field(name="Opções", value=opcoes_str, inline=False)
    embed.set_footer(text=f"Enviado por {interaction.user.display_name}")
    
    message = await interaction.channel.send(embed=embed)
    
    for i in range(len(opcoes)):
        await message.add_reaction(f"{i + 1}\N{COMBINING ENCLOSING KEYCAP}")

@tree.command(name="texto-bonito", description="Deixe seu texto mais bonito.")
async def convert_str_to_fancy(interaction, texto: str):
    await interaction.response.send_message(f"Novo texto: {font_converter.to_fancy(texto)}.")
    
@tree.command(name="ppcp", description="Prato, Prato, Conta suspensa, Prato (Se vc entendeu, está entendado).")
async def generate_ppcp_meme(interaction: discord.Interaction, membro1: discord.Member, membro2: discord.Member, membro3: discord.Member, membro4: discord.Member):
    membros = [membro1, membro2, membro3, membro4]
    if len(membros) != 4:
        await interaction.response.send_message("Você deve fornecer exatamente 4 membros.", ephemeral=True)
        return
    await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE)
    avatares = []
    for membro in membros:
        avatares.append(image.download_avatar(membro.avatar.url).resize((153, 153)))

    background = Image.open("MemeImages/ppcp/base.jpg")
    background.paste(avatares[0], (139,689))
    background.paste(avatares[1], (370,689))
    background.paste(avatares[2], (626,698))
    background.paste(avatares[3], (870,688))

    background.save("MemeImages/ppcp/" + str(interaction.id) + "_temp.png")

    with open("MemeImages/ppcp/" + str(interaction.id) + "_temp.png", "rb") as img_file:
        await interaction.channel.send(f"{membros[0].mention} {membros[1].mention} {membros[2].mention} {membros[3].mention}", file=discord.File(img_file, str(interaction.id) + "_temp.png"))

@tree.command(name="conveter-0-pra-emoji", description="Só isso.")
async def convert_number_to_emoji(interaction: discord.Interaction, texto: str):
    await interaction.response.send_message("Okay!", ephemeral=True)
    converted_text = texto.replace("0", ":black_circle:").replace("1", ":white_circle:")
    splitted_text = StrUtils.split_number(converted_text, max_length=56)

    for str_splitted in splitted_text:
        await interaction.channel.send(str_splitted)
    # await interaction.response.send_message(texto.replace("0", ":black_circle:").replace("1", ":white_circle:"))

lore = variables.get_json_file("Lore")
lore_characters = []
id = 0
for char in lore:
    id = id + 1
    lore_characters.append(Choice(name=char, value=char))
    # print(char)

@tree.command(name="lore", description="Veja a lore de alguém", guild=discord.Object(id=1218323333096013924))
@app_commands.choices(character=lore_characters)
async def lore_see(interaction: discord.Interaction, character: Choice[str]):
    personagem = lore[character.value]
    message_str = f"Lore de {personagem["name"]}\n"
    message_str = message_str + f"- Objetivos ```{personagem["objectives"]}```\n"
    message_str = message_str + f"- Personalidade ```{personagem["personality"]}```\n"
    message_str = message_str + f"- Aliados ```{personagem["aliases"]}```\n"
    message_str = message_str + f"- Arma ```{personagem["weapon"]}```\n"
    message_str = message_str + "- Abilidades\n"
    # abilities_list = ""
    for ability in personagem["abilities"]:
        # abilities_list = abilities_list + (f"-{ability}: {personagem["abilities"][ability]}.\n")
        message_str = message_str + f"{ability}: ```{personagem["abilities"][ability]}```\n"
    # embed.add_field(name="Habilidades", value=abilities_list, inline=False)
    if personagem.get("extras", {}) != {}:
        message_str = message_str + "- Características Extras\n"
        # extras_list = ""
        for extra in personagem["extras"]:
            # extras_list = extras_list + f"-{extra}."
            message_str = message_str + f"```{extra}.```\n"
        # embed.add_field(name="Características Extras", value=extras_list)
    message_str = message_str + f"\n\n{personagem["outfit"]}"
    await interaction.response.send_message(message_str)
    # if personagem["story"] is not None:
    #     await interaction.channel.send(f"- História de {personagem["name"]}: \n\n```{personagem["story"]}```")

order_choices = [
    Choice(name="Ascendente", value="Asc"),
    Choice(name="Descendente", value="Dec")
]
@tree.command(name="roblox-badges", description="Veja as 10 badges que um certo usuário tem.")
@app_commands.choices(ordem=order_choices)
async def see_user_roblox_badges(interaction: discord.Interaction, usuario: str, ordem: Choice[str]):
    await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE)
    # rclient = RobloxClient()
    user_id = roblox.get_user_id_from_username(usuario)
    url = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=10&sortOrder={ordem}"
    response = requests.get(url)
    response_json = response.json()

    emb_list = []
    for badge in response_json["data"]:
        # badge_info = rclient.get_badge(badge["id"])
        embed = discord.Embed(title=badge["displayName"], description=badge["displayDescription"])
        embed.add_field(name="Ganharam ontem", value=str(badge["statistics"]["pastDayAwardedCount"]), inline=False)
        embed.add_field(name="Ganharam antes", value=str(badge["statistics"]["awardedCount"]), inline=False)
        embed.add_field(name="Porcentagem de ganho", value=str(badge["statistics"]["winRatePercentage"]*100), inline=False)
        embed.add_field(name="Criada em", value=badge["created"], inline=False)
        embed.add_field(name="Atualizada em", value=badge["updated"], inline=False)
        # embed.set_image(url=badge_info['thumbnailUrl'])
        emb_list.append(embed)
    await interaction.edit_original_response(content=f"Badges de {usuario}:", embeds=emb_list)

@tree.command(name="invocar", description="Invoque eu para argumentar, pq não né?")
async def invok_for_some_reason(interaction: discord.Interaction, texto: str):
    await interaction.response.send_message(texto)

@tree.command(name="ajuda", description="Veja o que cada coisa faz dependendo do grupo")
@app_commands.choices(coisa=[
    Choice(name="Comandos", value=0)
])
async def help_with(interaction: discord.Interaction, coisa: Choice[int]):
    if coisa.value == 0:
        comm_list = "Lista de comandos:\n\n"
        tree_comm_list = await tree.fetch_commands(guild=interaction.guild)
        cur_comm = 0
        for comm in tree_comm_list:
            cur_comm = cur_comm + 1
            comm_list = comm_list + f"{cur_comm}: {comm.mention}.\n"
        await interaction.response.send_message(comm_list)
    else:
        await interaction.response.send_message("Achei nada")

import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from discord import FFmpegPCMAudio
from config import config
from gtts import gTTS
from pytube import YouTube
from pytube import exceptions as pytube_exceptions
import asyncio
import datetime
from datetime import datetime, timedelta

def get_queue():
  return musicqueue

musicqueue = {}
playing_music = False

for guild in config.GUILDS:
    guild_musc_queue = musicqueue.get(guild.id, [-1])
    if guild_musc_queue == [-1]:
        musicqueue[guild.id] = []

def get_queue_timestamp(guild: discord.Guild, vc: discord.VoiceClient):
    totaltime = 0
    for musc in musicqueue[guild.id]:
        musclength = timedelta(seconds=musc.length)
        totaltime = totaltime + musclength.seconds
    if vc is not None:
        return totaltime - vc.source.position
    return totaltime

def criar_audio(texto, idioma='pt-br', fileoutput=""):
    # padrao = r'[^\w\s]'
    # daaudiotxt = re.sub(padrao, '', texto)
    daaudiotxt = texto
    # Cria o objeto gTTS
    tts = gTTS(text=daaudiotxt, lang=idioma, slow=False)

    # Salva o arquivo de áudio
    arquivo_audio = "AudiosMemes/tts/" + fileoutput + ".mp3"
    print("Arquivo salvo: " + fileoutput)
    tts.save(arquivo_audio)

async def call_cmd(interaction: discord.Interaction, soundas: str, texts_config: dict):
  # if invdata.get(str(interaction.user.id), {}).get(str(produto["id"])) == 1:
  if interaction.user.voice is None or interaction.user.voice.channel is None:
    await interaction.response.send_message("Você tem que estar em uma call.", ephemeral=True)
    return
  
  sound = soundas

  voice_channel = interaction.user.voice.channel
  voice_client = interaction.guild.voice_client

  # await message.add_reaction('✅')

  if not voice_client:
    await voice_channel.connect()
    voice_client = interaction.guild.voice_client

  if soundas == "scream":
    await asyncio.sleep(2)

  try:
    if config.TEXTO_AUDIO_MAP[sound]["audio"] == "byebye":
      await interaction.response.send_message(":shushing_face::deaf_man:")
    elif config.TEXTO_AUDIO_MAP[sound]["audio"] == "theboys":
      with open('MemeImages/TheBoys.png', 'rb') as image_file:
        await interaction.response.send_message("", file=discord.File(image_file, "theboyslogo.png"))
    elif config.TEXTO_AUDIO_MAP[sound]["audio"] == "kirbyfalling":
      await interaction.response.send_message("https://media1.tenor.com/m/2EVga7MfSRsAAAAC/kirby-falling.gif")
    elif config.TEXTO_AUDIO_MAP[sound]["audio"] == "galaxybrain":
      await interaction.response.send_message("https://media1.tenor.com/m/wHs3JITWApsAAAAd/galaxy-brain-meme.gif")
    elif config.TEXTO_AUDIO_MAP[sound]["audio"] == "whistle":
      await interaction.response.send_message("https://media1.tenor.com/m/ETzfWFJsF8cAAAAd/josh-hutcherson-josh-hutcherson-whistle-edit.gif")
    else:
      await interaction.response.send_message("Audio tocado com sucesso.")
    source = FFmpegPCMAudio('AudiosMemes/' + config.TEXTO_AUDIO_MAP[sound]["audio"].lower() + ".mp3", executable="C:/ffmpeg/ffmpeg.exe")  # Substitua pelo caminho do seu arquivo de áudio
    voice_client.play(source)
  except Exception as e:
    await interaction.response.send_message(f"Ocorreu um erro: {e}", ephemeral=True)

  await asyncio.sleep(1)
  # Espera até que o áudio termine de tocar
  while interaction.guild.voice_client.is_playing():
    await asyncio.sleep(1)

  # Desconecta o bot após o áudio terminar
  await interaction.guild.voice_client.disconnect()
# else:
#   await interaction.response.send_message("Você não tem esse item comprado.", ephemeral=True)

async def skip_music(interaction: discord.Interaction):
    if interaction.channel.id == 1220495785993572472:
        if interaction.user.voice is None or interaction.user.voice.channel is None:
            await interaction.response.send_message("Você precisa estar em um canal de voz.", ephemeral=True)
        else:
            voice_channel = interaction.user.voice.channel
            voice_client = interaction.guild.voice_client

        await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE, ephemeral=True)
        # while len(musicqueue) > 0:
        try:
            vc = await voice_channel.connect()
        except:
            vc = interaction.guild.voice_client
        voice_client = interaction.guild.voice_client
        voice_client.stop()
        await interaction.channel.send(interaction.user.mention + " pediu pra eu pular, então eu pulei.")
            # if not vc.is_playing():
            #     musc = musicqueue.pop(0)
            #     yt = YouTube(musc.watch_url)
            #     yt.streams.filter(only_audio=True).first().download(output_path='AudiosMemes/ytmusic/', filename='music.ogg')
            #     titulo = yt.title
            #     duracao_segundos = yt.length
            #     autor = yt.author
            #     visualizacoes = yt.views
            #     visualizacoes_str = "{:,}".format(visualizacoes).replace(",", ".")
            #     duracao = timedelta(seconds=duracao_segundos)
            #     duracao_formatada = "{:2d}:{:02d}:{:02d}".format(duracao.seconds // 3600, (duracao.seconds % 3600) // 60, duracao.seconds % 60)
            #     thumbnail_url = yt.thumbnail_url
            #     embed = discord.Embed(title="Tocando agora: " + titulo, color=discord.Color.red(), url=musc.watch_url)
            #     embed.set_image(url=thumbnail_url)
            #     embed.set_author(name=autor, url=yt.channel_url)
            #     embed.add_field(name="Visualizações", value=visualizacoes_str, inline=True)
            #     embed.add_field(name="Duração", value=duracao_formatada, inline=True)
            #     embed.add_field(name="Data de publicação", value=f"<t:{round(yt.publish_date.timestamp())}:D>\n(<t:{round(yt.publish_date.timestamp())}:R>)", inline=True)
            #     embed.set_footer(text="Pedida por " + interaction.user.display_name, icon_url=interaction.user.avatar.url)
            #     await interaction.channel.send(embed=embed)
            #     sc = discord.FFmpegPCMAudio('AudiosMemes/ytmusic/music.ogg', executable="C:/ffmpeg/ffmpeg.exe")
            #     vc.play(discord.PCMVolumeTransformer(sc, volume=1.0))

        # while vc.is_playing():
        #     await asyncio.sleep(5)

        # # Tocar música
        # await asyncio.sleep(1)
        # await voice_client.disconnect()
        # await interaction.channel.send("Acabei a música que tinha ;>")
    else:
        await interaction.response.send_message("Use esse comando no canal <#1220495785993572472>, .", ephemeral=True)

async def see_list_music(interaction: discord.Interaction):
    if interaction.channel.id == 1220495785993572472:
        mqrtext = ""
        for mqrstuff in musicqueue[interaction.guild.id]:
            mqrtext = mqrtext + ("-" + mqrstuff.title + ".\n")

        if mqrtext == "":
            await interaction.response.send_message("Não tem nenhuma música na lista.", ephemeral=True)
        else:
            await interaction.response.send_message(mqrtext, ephemeral=True)
    else:
            await interaction.response.send_message("Use esse comando no canal <#1220495785993572472>, .", ephemeral=True)

async def stop_music_call(interaction: discord.Interaction):
    if interaction.channel.id == 1220495785993572472:
        voice_client = interaction.guild.voice_client
        if not voice_client:
            await interaction.response.send_message("Não tem nada tocando, .", ephemeral=True)
        else:
            await voice_client.disconnect()
            musicqueue[interaction.guild.id].clear()
            await interaction.response.send_message("Pronto.", ephemeral=True)
            await interaction.channel.send(interaction.user.mention + " Pediu para eu parar, então eu parei.")
    else:
        await interaction.response.send_message("Use esse comando no canal <#1220495785993572472>, .", ephemeral=True)

async def set_music_volume(interaction: discord.Interaction, volume=1.0):
    if interaction.channel.id == 1220495785993572472:
        voice_client = interaction.guild.voice_client
        if not voice_client:
            await interaction.response.send_message("Não tem nada tocando, .", ephemeral=True)
        else:
            if volume > 1000 or volume < 0:
                await interaction.response.send_message("Tem que ser um valor entre 0 e 1000, .", ephemeral=True)
            else:
                voice_client.source.volume = float(volume) / 100.0
                await interaction.response.send_message("Volume setado para " + str(volume) + ".")
    else:
        await interaction.response.send_message("Use esse comando no canal <#1220495785993572472>, .", ephemeral=True)

async def play_music_call(interaction: discord.Interaction, music=""):
    if interaction.channel.id == 1220495785993572472:
        if music == "":
            await interaction.response.send_message("Insira um URL válido, .", ephemeral=True)
        elif interaction.user.voice is None or interaction.user.voice.channel is None:
            await interaction.response.send_message("Você precisa estar em um canal de voz, .", ephemeral=True)
        else:
            voice_channel = interaction.user.voice.channel
            voice_client = interaction.guild.voice_client
            # if voice_client.is_playing():
            #     await interaction.response.send_message("O sistema de lista de música está em manutenção", ephemeral=True)
            #     return

            await interaction.response.send_message(config.COMMAND_RUNNING_MESSAGE, ephemeral=True)
            ytq = YouTube(music)
            try:
                ytq.streams.filter(only_audio=True).first()
            except pytube_exceptions.AgeRestrictedError:
                await interaction.edit_original_response(content="Essa música tem restrição de idade, por isso não consigo toca-la.")
                return
            except pytube_exceptions.ExtractError:
                await interaction.edit_original_response(content="Deu algum erro na extração, por isso não consigo toca-la.")
                return
            except pytube_exceptions.MembersOnly:
                await interaction.edit_original_response(content="Essa música é só para membros, por isso não consigo toca-la.")
                return
            except pytube_exceptions.RecordingUnavailable or pytube_exceptions.VideoUnavailable:
                await interaction.edit_original_response(content="Essa música está indisponível, por isso não consigo toca-la.")
                return
            except pytube_exceptions.VideoPrivate:
                await interaction.edit_original_response(content="Essa música é privada, por isso não consigo toca-la.")
                return
            except pytube_exceptions.LiveStreamError:
                await interaction.edit_original_response(content="Essa música é uma live e está com erro, por isso não consigo toca-la.")
                return
            except:
                await interaction.edit_original_response(content="Essa música eu nem sei mais oq é o erro, por isso não consigo toca-la.")
                return
            try:
                vc = await voice_channel.connect()
            except:
                vc = interaction.guild.voice_client
            musicqueue[interaction.guild.id].append(ytq)
            mqrembed = discord.Embed(description=ytq.title + " adicionada à lista.", color=discord.Color.red())
            mqrembed.set_footer(text="Pedida por " + interaction.user.display_name, icon_url=interaction.user.avatar.url)
            mqrembed.set_thumbnail(url=ytq.thumbnail_url)
            # time_to_play = "{:2d}:{:02d}:{:02d}".format(get_queue_timestamp(interaction.guild, vc) // 3600, (get_queue_timestamp(interaction.guild, vc) % 3600) // 60, get_queue_timestamp(interaction.guild, vc) % 60)
            await interaction.channel.send(embed=mqrembed)
            voice_client = interaction.guild.voice_client
            if not vc.is_playing():
                while len(musicqueue[interaction.guild.id]) > 0:
                    if not vc.is_playing():
                        musc = musicqueue[interaction.guild.id][0]
                        yt = YouTube(musc.watch_url)
                        yt.streams.filter(only_audio=True).first().download(output_path='AudiosMemes/ytmusic/', filename='music.ogg')
                        titulo = yt.title
                        duracao_segundos = yt.length
                        autor = yt.author
                        visualizacoes = yt.views
                        visualizacoes_str = "{:,}".format(visualizacoes).replace(",", ".")
                        duracao = timedelta(seconds=duracao_segundos)
                        duracao_formatada = "{:2d}:{:02d}:{:02d}".format(duracao.seconds // 3600, (duracao.seconds % 3600) // 60, duracao.seconds % 60)
                        thumbnail_url = yt.thumbnail_url
                        embed = discord.Embed(title="Tocando agora: " + titulo, color=discord.Color.red(), url=musc.watch_url)
                        embed.set_image(url=thumbnail_url)
                        embed.set_author(name=autor, url=yt.channel_url)
                        embed.add_field(name="Visualizações", value=visualizacoes_str, inline=True)
                        embed.add_field(name="Duração", value=duracao_formatada, inline=True)
                        embed.add_field(name="Data de publicação", value=f"<t:{round(yt.publish_date.timestamp())}:D>\n(<t:{round(yt.publish_date.timestamp())}:R>)", inline=True)
                        embed.set_footer(text="Pedida por " + interaction.user.display_name, icon_url=interaction.user.avatar.url)
                        await interaction.channel.send(embed=embed)
                        sc = discord.FFmpegPCMAudio('AudiosMemes/ytmusic/music.ogg', executable="C:/ffmpeg/ffmpeg.exe")
                        vc.play(discord.PCMVolumeTransformer(sc, volume=1.0))
                        playing_music = True

                    while vc.is_playing():
                        await asyncio.sleep(1)

                    musicqueue[interaction.guild.id].pop(0)

                playing_music = False
                # Tocar música
                await asyncio.sleep(1)
                await voice_client.disconnect()
                await interaction.channel.send("Acabei a música que tinha ;>")
    else:
        await interaction.response.send_message("Use esse comando no canal <#1220495785993572472>, .", ephemeral=True)

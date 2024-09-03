import discord
from discord import app_commands
from utils import image as ImageUtils
from utils import audio as AudioUtils
from utils import music as MusicUtils
import config
import asyncio
import main_variables as Variables

class MyClient(discord.Client):

  def __init__(self, intents=Variables.get_discord_intents(), **options):
    super().__init__(intents=intents, **options)

  async def on_ready(self):
    print('Logged in as {0.user}'.format(self))
    await tree.sync(guild=discord.Object(id=config.SERVER_ID))
    await self.change_presence(status=discord.Status.online,activity=discord.Activity(name=config.DEFAULT_STATUS))
    # await self.main_channel.send("Eae galera.")
    print('ready to use :)')
  
  async def on_message(self, message):
    if message.author == self.user or message.author.bot:
      return
    # await on_message_event.on_message(message)f

    if "gay" in message.content.lower():
      await message.reply("foda.")

    if message.content.startswith(self.user.mention):
      message_content = message.content.replace(self.user.mention, "")
      # music stuffs
      if message_content.endswith("toque minha playlist"):
        await self.play_playlist(message)
      
      if message_content.startswith("quero na minha playlist a ") or message_content.startswith(" quero na minha playlist a "):
        await self.add_song_to_playlist(message)
      # no bitches? 
      if message_content.startswith("no ") or message_content.startswith(" no "):
        await self.do_megamind_image(message)
      # eu vim fazer um anuncio, shadow o ouriço é um filho da-
      if message_content.lower().endswith("você pode fazer um anuncio?"):
        await self.anuncio(message)
      return

    # quote maker
    if message.content.startswith("\"") and message.content.endswith("\"") and message.channel.id == 1239701534137127074:
      await self.quote_maker(message)

  async def play_playlist(message: discord.Message):
    voice_state = message.author.voice
    if voice_state is not None and voice_state.channel is not None:
      playlist = MusicUtils.get_playlist(str(message.author.id))
      if playlist is not None and len(playlist) > 0:
        await message.reply("beleza, vou tentar")
        try:
          voice_channel = message.author.voice.channel
          vc = await voice_channel.connect()
          music_commands_channel = await message.guild.fetch_channel(1220495785993572472)
          for song in playlist:
            if song != "":
              await music_commands_channel.send(f"m!p {song}")
              await asyncio.sleep(0.7)
          await asyncio.sleep(1.5)
          await vc.disconnect()
        except Exception as e:
          await message.reply("não consegui, desculpa :sob:")
          print("play_playlist failed.\nReason: " + str(e) + "\n")
      else:
        await message.reply("ehm, com licença interromper mas...você não tem uma playlist :point_up: :nerd:")
    else:
      await message.reply("não")

  async def add_song_to_playlist(self,message: discord.Message):
    message_content = message.content.replace(self.user.mention, "")
    song_to_add = message_content.replace(" quero na minha playlist a ", "").replace("quero na minha playlist a ", "")
    try:
      await message.reply("beleza")
      MusicUtils.update_playlist(str(message.author.id), song_to_add)
    except Exception as e:
      await message.reply("foi mal, não consegui :sob:")
      print("add_to_playlist failed.\nReason: " + str(e) + "\n")

  async def do_megamind_image(self,message: discord.Message):
    message_content = message.content.replace(self.user.mention, "")
    try:
      await ImageUtils.make_megamind_image(message_content + "?", "cache")
      with open("images/MegamindImages/cache.jpg", "rb") as img_file:
        await message.reply("", file=discord.File(img_file, "megamind.png"))
        return
    except Exception as e:
      print("megamind image generation failed.\nReason: " + str(e) + "\n")
      return

  async def anuncio(self, message: discord.Message):
    voice_state = message.author.voice
    if voice_state is not None and voice_state.channel is not None:
      await message.reply("okay, chego aí em um minuto...")
      try:
        AudioUtils.generate_tts_audio(message.author.display_name, "pt-br", "anuncio/shadow_o_ouriço/voice_cache")
        AudioUtils.combine_audios(["anuncio/shadow_o_ouriço/part1", "anuncio/shadow_o_ouriço/voice_cache", "anuncio/shadow_o_ouriço/part2"], "anuncio/shadow_o_ouriço/result_cache")
        voice_channel = message.author.voice.channel
        vc = await voice_channel.connect()
        audio_source = discord.FFmpegPCMAudio("audios/anuncio/shadow_o_ouriço/result_cache.mp3", executable='C:\\ffmpeg\\ffmpeg.exe')
        vc.play(audio_source, after=lambda e: print(f"Reprodução de áudio finalizada: {e}"))
        while vc.is_playing():
          await asyncio.sleep(1)

        await vc.disconnect()
        return
      except Exception as e:
        print("anuncio generation failed.\nReason: " + str(e) + "\n")
        await message.reply("mudei de ideia, foi mal ae")
        return
    else:
      await message.reply("não")

  async def quote_maker(self, message: discord.Message):
    await message.reply("Interessante...")
    await message.reply("Vai virar Quote >:)")
    await ImageUtils.make_quote_image(message.author.avatar.url, message.content, message.author.display_name)
    carol_room_channel = await message.guild.fetch_channel(config.CAROL_ROOM_CHANNEL_ID)
    with open("images/Quotes/cache.png", "rb") as img_file:
      await carol_room_channel.send("", file=discord.File(img_file, "quote.png"))

  async def on_disconnect(self):
    print('disconnected as {0.user}'.format(self))
    # await self.send_message_to_main_channel('Até a próxima.')

client = MyClient(intents=Variables.get_discord_intents())
tree = app_commands.CommandTree(client)
client.run(config.TOKEN)

const {
  joinVoiceChannel,
  createAudioPlayer,
  createAudioResource,
  AudioPlayerStatus,
} = require("@discordjs/voice");
const { GuildMember, Guild } = require("discord.js");
const path = require("path");

class DiscordCallHelper {
  static async joinAndPlayAudioOnVoiceChannel(
    member = GuildMember,
    guild = Guild,
    audioFile = "",
    leaveOnFinish = false
  ) {
    try {
      const connection = joinVoiceChannel({
        channelId: member.voice.channel.id,
        guildId: guild.id,
        adapterCreator: guild.voiceAdapterCreator,
      });

      const resource = createAudioResource(
        "https://streams.ilovemusic.de/iloveradio8.mp3",
        {
          inlineVolume: true,
        }
      );

      const player = createAudioPlayer();
      connection.subscribe(player);
      player.play(resource);
    } catch (error) {
      console.error(error);
    }
  }
}

module.exports = DiscordCallHelper;

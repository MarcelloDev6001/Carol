const {
  joinVoiceChannel,
  createAudioPlayer,
  createAudioResource,
  AudioPlayer,
  AudioPlayerStatus,
} = require("@discordjs/voice");
const { GuildMember, Guild, VoiceChannel } = require("discord.js");
const fs = require("fs");
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

      const player = createAudioPlayer();
      const resource = createAudioResource(path.join(__dirname, audioFile));

      player.play(resource);
      connection.subscribe(player);

      player.on(AudioPlayerStatus.Playing, () => {
        console.log("The audio player has started playing!");
      });

      player.on("error", (error) => {
        console.error(`Error: ${error.message}`);
      });
    } catch (error) {
      console.error(error);
    }
  }
}

module.exports = DiscordCallHelper;

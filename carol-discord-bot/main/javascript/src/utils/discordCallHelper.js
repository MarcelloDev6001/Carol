const {
  joinVoiceChannel,
  createAudioPlayer,
  createAudioResource,
  AudioPlayer,
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
      let voiceConnection = joinVoiceChannel({
        channelId: member.voice.channel.id,
        guildId: guild.id,
        adapterCreator: guild.voiceAdapterCreator,
      });
      let audioBuffer = fs.readFileSync(audioFile);
      voiceConnection.playOpusPacket(audioBuffer);
    } catch (error) {
      console.error(error);
    }
  }
}

module.exports = DiscordCallHelper;

const { SlashCommandBuilder } = require("discord.js");
const { BaseInteraction } = require("discord.js");

class SlashCommandPingOther {
  static async doCommand(interaction) {
    await interaction.reply("Pong!");
  }
}

module.exports = SlashCommandPingOther;

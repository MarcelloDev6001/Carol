const { SlashCommandBuilder } = require("@discordjs/builders");
const { REST } = require("@discordjs/rest");
const { Routes } = require("discord-api-types/v9");
const { clientId, guildId, token } = require("./config.json");

class SlashComms {
  static initCommands() {
    this.commandsListBuilded = [
      new SlashCommandBuilder()
        .setName("ping")
        .setDescription("responde com um ping"),
    ];
    this.commands = this.commandsListBuilded.map((command) => command.toJSON());
    const rest = new REST({ version: "9" }).setToken(token);

    rest
      .put(Routes.applicationGuildCommands(clientId, guildId), {
        body: this.commands,
      })
      .then(() => console.log("Successfully registered application commands."))
      .catch(console.error);
  }
}

module.exports = SlashComms;

const SlashCommandPingOther = require("../commands/other/ping");
const ping = require("../commands/other/ping");

class InteractionCreateEvent {
  constructor(interaction) {
    this.doInteractionEvent(interaction);
  }

  async doInteractionEvent(interaction) {
    if (!interaction.isCommand()) return;

    const { commandName } = interaction;

    switch (commandName) {
      case "ping":
        SlashCommandPingOther.doCommand(interaction);
        break;

      default:
        break;
    }
  }
}

module.exports = InteractionCreateEvent;

const { EmbedBuilder, MessagePayload } = require("discord.js");
const JsonReader = require("../utils/jsonReader");

class HelpMessageCommand {
  static async help(message, clientUser, prefix) {
    let commandsJson = JsonReader.read("./data/commands.json");
    let commandsEmbedArray = [];

    for (const element in commandsJson) {
      let category = commandsJson[element];
      let commandsEmbed = new EmbedBuilder()
        .setColor(0x0099ff)
        .setAuthor({
          name: clientUser.displayName,
          iconURL: clientUser.avatarURL({ size: 1024 }),
          url: "https://discord.com/users/" + clientUser.id,
        })
        .setTitle(element)
        .setTimestamp();
      category.forEach((comm) => {
        if ("example" in comm) {
          commandsEmbed.addFields({
            name: comm["name"],
            value:
              comm["description"] +
              ".\n\nExemplo:" +
              prefix +
              comm["name"] +
              " " +
              comm["example"],
          });
        } else {
          commandsEmbed.addFields({
            name: comm["name"],
            value: comm["description"] + ".",
          });
        }
      });
      commandsEmbedArray.push(commandsEmbed);
    }

    message.reply(new MessagePayload(message, { embeds: commandsEmbedArray }));
  }
}

module.exports = HelpMessageCommand;

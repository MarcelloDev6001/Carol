const {
  EmbedBuilder,
  PermissionFlagsBits,
  DiscordAPIError,
} = require("discord.js");
const JsonReader = require("../utils/jsonReader.js");
const { prefix } = require("../../config.json");
const XPSystem = require("../experience/xp.js");
const SpamSystem = require("../automod/spam.js");

const spamSystem = new SpamSystem(5, 9000);

class MessageCreateEvent {
  message = null;
  client = null;
  constructor(message, client) {
    this.message = message;
    this.client = client;
    this.doMessageEvent(message);
  }

  async doMessageEvent(message) {
    if (message.author.bot) return;

    // * why that was too complex at the first time?
    let expJson = await XPSystem.updateExperienceAndLevel(
      message.author,
      message.guild,
      message.channel,
      1,
      0
    );

    if (message.content.startsWith(prefix)) {
      let messageCommand = message.content.split(" ")[0].replace(prefix, "");
      switch (messageCommand.toLowerCase()) {
        case "level":
          let userXP = expJson[message.guild.id][message.author.id]["xp"];
          let userLevel = expJson[message.guild.id][message.author.id]["level"];
          message.reply(`Seu level é ${userLevel} (${userXP}xp)`);
          break;

        // *that silly format: [
        // *  {"user_id": {"xp": 0, "level": 0}},
        // *  {"user_id": {"xp": 0, "level": 0}}
        // *];
        case "levelrank":
          // * WIP...
          var funnyIndexCounter = 0;
          let finalMessageResult = "Top 5 de mais level:\n\n";
          let users = [];
          users = await XPSystem.getUsersRank(message, 5);
          users.forEach((element) => {
            funnyIndexCounter += 1;
            finalMessageResult +=
              funnyIndexCounter.toString() +
              `: <@${element["memberID"]}> (level ${element["level"]} e xp de ${element["xp"]})\n`;
          });
          message.reply(finalMessageResult);
          break;

        default:
          break;
      }
    }
    let userSpammed = await spamSystem.checkForSpam(message.member, message);
    if (userSpammed) {
      message.reply(
        "Você está enviando mensagens muito rápido! Por favor, pare de spammar."
      );
    }
  }
}

module.exports = MessageCreateEvent;

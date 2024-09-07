const {
  EmbedBuilder,
  PermissionFlagsBits,
  DiscordAPIError,
  Message,
  MessagePayload,
  AttachmentBuilder,
} = require("discord.js");
const JsonReader = require("../utils/jsonReader.js");
const { prefix } = require("../../config.json");
const XPSystem = require("../experience/xp.js");
const SpamSystem = require("../automod/spam.js");
const MoneyConversion = require("../others/moneyconversion.js");
const { createTTSFile } = require("../audio/tts.js");
const DiscordCallHelper = require("../utils/discordCallHelper.js");
const TTS = require("../audio/tts.js");
const QRCodeGenerator = require("../messagecommands/qrcode.js");
const fs = require("fs");
const LetsGoGamblingCommand = require("../messagecommands/gamble.js");
const MoneyMessageCommand = require("../messagecommands/money.js");
const LevelMessageCommand = require("../messagecommands/level.js");
const path = require("path");
const TextMessageCommands = require("../messagecommands/text.js");

const spamSystem = new SpamSystem(5, 9000);

class MessageCreateEvent {
  message = null;
  client = null;
  constructor(message, client) {
    this.message = message;
    this.client = client;
    this.doMessageEvent(message);
  }

  async wait(ms, value) {
    return new Promise((resolve) => setTimeout(resolve, ms, value));
  }

  async doMessageEvent(message = Message) {
    if (message.author.bot) return;

    let userSpammed = await spamSystem.checkForSpam(message.member, message);
    if (userSpammed) {
      message.reply(
        "Você está enviando mensagens muito rápido! Por favor, pare de spammar."
      );
      // spamSystem.deleteSpammedMessages(message.member);
    }

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
        case "github": // * to see the source code of the bot :)
          message.reply("https://github.com/MarcelloDev6001/Carol");
          break;
        case "level":
          await LevelMessageCommand.level(message, prefix, messageCommand);
          break;

        case "levelrank":
          await LevelMessageCommand.levelRank(message, prefix, messageCommand);
          break;

        case "money":
          await MoneyMessageCommand.money(message, prefix, messageCommand);
          break;

        case "qrcode":
          await QRCodeGenerator.qrcode(message, prefix, messageCommand);
          break;

        case "gamble":
          await LetsGoGamblingCommand.gamble(message);
          break;

        // case "fancytext":
        //   await TextMessageCommands.fancy(message, prefix, messageCommand);
        //   break;

        default:
          break;
      }
    }
  }
}

module.exports = MessageCreateEvent;

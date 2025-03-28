const { Message } = require("discord.js");
const { prefix } = require("../../config.json");
const XPSystem = require("../experience/xp.js");
const SpamSystem = require("../automod/spam.js");
const QRCodeGenerator = require("../messagecommands/qrcode.js");
const LetsGoGamblingCommand = require("../messagecommands/gamble.js");
const MoneyMessageCommand = require("../messagecommands/money.js");
const LevelMessageCommand = require("../messagecommands/level.js");
const FuneralMessageCommand = require("../messagecommands/funeral.js");
const ShipMessageCommand = require("../messagecommands/ship.js");
const DiscordCallHelper = require("../utils/discordCallHelper.js");
const HelpMessageCommand = require("../messagecommands/help.js");
const GuildManagingMessageCommands = require("../messagecommands/guildmanaging.js");

const spamSystem = new SpamSystem(5, 9000);

// * when you send a message, this is called on index.js
class MessageCreateEvent {
  message = null;
  client = null;
  constructor(message, client) {
    this.message = message;
    this.client = client;
    this.doMessageEvent(message);
  }

  async doMessageEvent(message = Message) {
    if (message.author.bot) return;

    let userSpammed = await spamSystem.checkForSpam(message.member, message);
    if (userSpammed) {
      try {
        message.reply(
          "Você está enviando mensagens muito rápido! Por favor, pare de spammar."
        );
      } catch (error) {
        message.channel.send(
          "<@" +
            message.author.id +
            "> Você está enviando mensagens muito rápido! Por favor, pare de spammar."
        );
      }
      // spamSystem.deleteSpammedMessages(message.member);
    }

    // * why that was too complex at the first time?
    let expJson = await XPSystem.updateExperienceAndLevel(
      message.author,
      message.guild,
      message.channel,
      1,
      0,
      this.client,
      message
    );

    if (message.content.startsWith(prefix)) {
      let messageCommand = message.content.split(" ")[0].replace(prefix, "");
      switch (messageCommand.toLowerCase()) {
        // case "github": // * to see the source code of the bot :)
        //   message.reply("https://github.com/MarcelloDev6001/Carol");
        //   break;

        case "level":
          await LevelMessageCommand.level(message, prefix, messageCommand);
          break;

        case "levelrank":
          await LevelMessageCommand.levelRank(message, prefix, messageCommand);
          break;

        case "dinheiro":
          await MoneyMessageCommand.money(message, prefix, messageCommand);
          break;

        case "qrcode":
          await QRCodeGenerator.qrcode(message, prefix, messageCommand);
          break;

        case "gamble":
          await LetsGoGamblingCommand.gamble(message);
          break;

        case "funeral":
          await FuneralMessageCommand.funeral(message, prefix, messageCommand);
          break;

        case "ship":
          await ShipMessageCommand.ship(message, prefix, messageCommand);
          break;

        case "ajuda":
          await HelpMessageCommand.help(message, this.client.user, prefix);
          break;

        case "canalderegistro":
          let audit_log_channel_id = message.content
            .replace(prefix + messageCommand + " ", "")
            .replace("<@", "")
            .replace(">", "");
          await GuildManagingMessageCommands.setAuditLogChannel(
            message.guild,
            audit_log_channel_id,
            message
          );
          break;

        // ! in development...
        // case "palavraproibida":
        //   let unauthorizedWord = message.content.replace(
        //     prefix + messageCommand + " ",
        //     ""
        //   );
        //   await GuildManagingMessageCommands.setUnauthorizedWord(
        //     message.guild,
        //     unauthorizedWord,
        //     message
        //   );
        //   break;

        default:
          break;
      }
    }
  }
}

module.exports = MessageCreateEvent;

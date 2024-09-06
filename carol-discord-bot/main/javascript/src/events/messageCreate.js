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

const spamSystem = new SpamSystem(5, 9000);

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

        case "money":
          let args = message.content
            .replace(prefix, "")
            .replace(messageCommand + " ", "")
            .split(" ");
          if (args.length < 2) {
            message.reply(
              "Tem que ter moeda de origem, moeda de conversão e o valor."
            );
            break;
          }
          let amount = parseInt(args[2]);
          try {
            let finalResult = await MoneyConversion.fromTo(
              args[0],
              args[1],
              amount
            );
            message.reply(
              amount.toString() + " pra " + args[1] + " é " + finalResult
            );
          } catch (e) {
            message.reply("Ocorreu um erro: " + e);
          }

        case "qrcode":
          let arg = message.content.replace(prefix + messageCommand + " ", "");
          if (arg == "" || arg == prefix + messageCommand + " ") {
            message.reply("tu tem que informar um texto");
            break;
          }
          let rickrollChance = Math.floor(Math.random() * 10);
          if (rickrollChance == 6) {
            // * it's simple, if the random number is 1, soo you will get rickrolled >:)
            await QRCodeGenerator.generateQRCode(
              "https://youtu.be/dQw4w9WgXcQ?si=rJb9-oWRTqgpBvmh",
              "./resources/images/qrcodes/cache.png"
            );
          } else {
            await QRCodeGenerator.generateQRCode(
              arg,
              "./resources/images/qrcodes/cache.png"
            );
          }
          function wait(ms, value) {
            return new Promise((resolve) => setTimeout(resolve, ms, value));
          }
          await wait(2000, 1); // * wait 2 seconds (the time aproximally required to save the QRCode image)
          let qrcodeFile = fs.readFileSync(
            "./resources/images/qrcodes/cache.png"
          );
          let qrcodeAttachment = new AttachmentBuilder(qrcodeFile, {
            name: "qrcode.png",
          });
          message.reply(
            new MessagePayload(message, {
              content: "aqui:",
              files: [qrcodeAttachment],
            })
          );
          break;

        // ! ISN'T WORKING FOR NOW
        // case "tts":
        //   let textToTTS = message.content.replace(
        //     prefix + messageCommand + " ",
        //     ""
        //   );
        //   if (textToTTS == "") {
        //     message.reply("Vc precisa fornecer um texto");
        //     break;
        //   }
        //   if (message.member.voice.channel) {
        //     // * is in a voice channel
        //     TTS.createTTSFile(
        //       textToTTS,
        //       "pt-br",
        //       "./data/audios/tts/cache.mp3"
        //     );
        //     await DiscordCallHelper.joinAndPlayAudioOnVoiceChannel(
        //       message.member,
        //       message.guild,
        //       "./data/audios/tts/cache.mp3",
        //       true
        //     );
        //   } else {
        //     message.reply("Você precisa estar em uma call");
        //   }

        default:
          break;
      }
    }
  }
}

module.exports = MessageCreateEvent;

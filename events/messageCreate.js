const {
  Client,
  GatewayIntentBits,
  AttachmentBuilder,
  MessagePayload,
} = require("discord.js");
const ImageHelper = require("../utils/imageHelper.js").ImageHelper;
const ImageText = require("../utils/imageHelper.js").ImageText;
const path = require("path");
const fs = require("fs");
const MainSettings = require("../mainsettings.js");
const Config = require("../config.js");

class MessageCreateEvent {
  message = null;
  client = null;
  conf = new Config();
  constructor(message, client) {
    this.message = message;
    this.client = client;
    this.doMessageEvent(message);
  }

  async doMessageEvent(message) {
    if (message.author.bot) return;

    if (message.content === "!ping") {
      message.reply("Pong!");
    }

    if (message.content === "!hello") {
      message.reply("Olá! Como você está?");
    }

    if (message.content.toLowerCase().includes("gay")) {
      message.reply("foda");
    }

    if (
      (message.content.toLowerCase().includes("compreensível") ||
        message.content.toLowerCase().includes("compreensivel")) &&
      message.author.id == this.conf.predefinedUsersIDs["hades"]
    ) {
      message.reply(
        "aqui pra vc, ó\nhttps://tenor.com/view/trabalho-gif-25189190"
      );
    }

    // if (
    //   message.content.toLowerCase().includes("marcello") ||
    //   message.content.toLowerCase().includes("marcelo")
    // ) {
    //   message.delete();
    // }

    // if (message.content.toLowerCase().startsWith("no ")) {
    //   const megamindImg = await ImageHelper.writeTextFittedToImage(
    //     "images/megamindmeme/base.jpg",
    //     new ImageText(message.content + "?", "WHITE", 76),
    //     "images/megamindmeme/cache.jpg"
    //   );
    //   if (megamindImg) {
    //     const file = fs.readFileSync("./images/megamindmeme/cache.jpg");
    //     const attach = new AttachmentBuilder(file, {name: "megamind.jpg", description: "nothing here"});
    //     message.reply(new MessagePayload(message, { content: "e...", files: [attach]}));
    //   }
    // }
  }
}

module.exports = MessageCreateEvent;

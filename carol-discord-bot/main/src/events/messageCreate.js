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
const JsonReader = require("../utils/jsonReader.js");
const TXTReader = require("../utils/txtReader.js");

class MessageCreateEvent {
  message = null;
  client = null;
  expJson = {};
  constructor(message, client) {
    this.message = message;
    this.client = client;
    this.doMessageEvent(message);
  }

  async doMessageEvent(message) {
    if (message.author.bot) return;

    // ! ISN'T WORKING NOW
    // await this.updateExperienceAndLevel(message.author, message.guild);
    // console.log(__dirname);
    console.log(path.join(__dirname, `../data/experience/`));

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
  }

  // * json format: {
  // *    GUILD_ID: {
  // *      USER_ID: {
  // *        "xp": 0,
  // *        "level": 0
  // *      }
  // *    }
  // *  }
  async updateExperienceAndLevel(user, guild) {}
}

module.exports = MessageCreateEvent;

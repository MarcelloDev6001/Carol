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
  async updateExperienceAndLevel(user, guild) {
    this.expJson = {};
    this.expJson = await JsonReader.read(
      path.join(__dirname, "../../data/experience.json")
    );
    console.log(
      `Json File Path:${path.join(__dirname, "../../data/experience.json")}`
    );
    console.log(`expJson Content: ${this.expJson}`);
    if (this.expJson == undefined) {
      this.expJson = {
        // * just using my own template :)
        0: {
          0: {
            xp: 0,
            level: 0,
          },
        },
        0: {
          0: {
            xp: 0,
            level: 0,
          },
        },
      };
    }
    // console.log(this.expJson);

    if (!(guild.id in this.expJson)) {
      this.expJson[guild.id] = {};
    }

    if (!(user.id in this.expJson[guild.id])) {
      this.expJson[guild.id][user.id] = {
        xp: 1,
        level: 0,
      };
    } else {
      this.expJson[guild.id][user.id] = {
        xp: this.expJson[guild.id][user.id]["xp"] + 1,
        level: 0,
      };
    }
    console.log(this.expJson);
    JsonReader.save(
      path.join(__dirname, "../../data/experience.json"),
      this.expJson
    );
  }
}

module.exports = MessageCreateEvent;

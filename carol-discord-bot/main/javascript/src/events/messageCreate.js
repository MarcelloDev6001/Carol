const { EmbedBuilder } = require("discord.js");
const JsonReader = require("../utils/jsonReader.js");
const { prefix } = require("../../config.json");

class MessageCreateEvent {
  message = null;
  client = null;
  // expJson = {};
  constructor(message, client) {
    this.message = message;
    this.client = client;
    this.doMessageEvent(message);
  }

  async doMessageEvent(message) {
    if (message.author.bot) return;

    // * why that was too complex at the first time?
    let expJson = await this.updateExperienceAndLevel(
      message.author,
      message.guild,
      message.channel,
      1,
      0
    );

    if (message.content.toLowerCase().includes("gay")) {
      message.reply("foda");
    }

    if (message.content == prefix + "level") {
      let userXP = expJson[message.guild.id][message.author.id]["xp"];
      let userLevel = expJson[message.guild.id][message.author.id]["level"];
      message.reply(`Seu level é ${userLevel} (${userXP}xp)`);
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
  async getXP(user, guild, channel) {
    let expJson = JsonReader.read("./data/experience.json");
    if (!guild.id in expJson) {
      expJson[guild.id] = {};
    }
    if (!(user.id in expJson[guild.id])) {
      expJson[guild.id][user.id] = {
        xp: 0,
        level: 0,
      };
    }
    return expJson[guild.id][user.id]["xp"];
  }
  async getLevel(user, guild, channel) {
    // * basically the same code of getXP()
    let expJson = JsonReader.read("./data/experience.json");
    if (!guild.id in expJson) {
      expJson[guild.id] = {};
    }
    if (!(user.id in expJson[guild.id])) {
      expJson[guild.id][user.id] = {
        xp: 0,
        level: 0,
      };
    }
    return expJson[guild.id][user.id]["level"];
  }
  async updateExperienceAndLevel(user, guild, channel, xpToAdd, levelToAdd) {
    let expJson = JsonReader.read("./data/experience.json");
    if (expJson == undefined) {
      expJson = {};
    }
    if (!(guild.id in expJson)) {
      expJson[guild.id] = {};
    }
    if (user.id in expJson[guild.id]) {
      expJson[guild.id][user.id] = {
        xp: expJson[guild.id][user.id]["xp"] + xpToAdd,
        level: expJson[guild.id][user.id]["level"] + levelToAdd,
      };
    } else {
      expJson[guild.id][user.id] = {
        xp: 0,
        level: 0,
      };
    }
    if (
      expJson[guild.id][user.id]["xp"] - 1000 >
      expJson[guild.id][user.id]["level"] * 1000
    ) {
      // * level up
      expJson[guild.id][user.id]["level"] += 1;
      await this.sendLevelUpMessage(
        user,
        channel,
        expJson[guild.id][user.id]["level"],
        expJson[guild.id][user.id]["xp"]
      );
    }
    await JsonReader.save("./data/experience.json", expJson);
    return expJson;
  }

  async sendLevelUpMessage(user, channel, userLevel, userXP) {
    let levelUPEmbed = new EmbedBuilder()
      .setColor(0xffffff)
      .setTitle("Level UP!")
      .setAuthor({
        name: this.client.user.displayName,
        iconURL: this.client.user.avatarURL({ size: 1024 }),
        url: `https://Discordapp.com/users/${this.client.user.id.toString()}`,
      })
      .setDescription(
        `Parabens <@${
          user.id
        }>, você acabou de evoluir para o level ${userLevel.toString()}! (${userXP.toString()} xp)`
      )
      .setThumbnail(user.avatarURL({ size: 1024 }));
    channel.send({
      content: `<@${user.id.toString()}>`,
      embeds: [levelUPEmbed],
    });
  }
}

module.exports = MessageCreateEvent;

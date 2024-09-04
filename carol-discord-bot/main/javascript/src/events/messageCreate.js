const { EmbedBuilder } = require("discord.js");
const JsonReader = require("../utils/jsonReader.js");
const { prefix } = require("../../config.json");

// spam system stuffs
const spamMap = new Map();
const LIMIT = 5;
const TIME = 9000;

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
    let expJson = await this.updateExperienceAndLevel(
      message.author,
      message.guild,
      message.channel,
      1,
      0
    );

    if (message.content == prefix + "level") {
      let userXP = expJson[message.guild.id][message.author.id]["xp"];
      let userLevel = expJson[message.guild.id][message.author.id]["level"];
      message.reply(`Seu level é ${userLevel} (${userXP}xp)`);
    }

    await this.checkForSpam(message.member, message);
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
    JsonReader.save("./data/experience.json", expJson);
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

  async checkForSpam(user, message) {
    if (spamMap.has(user.id)) {
      const userData = spamMap.get(user.id);
      const { lastMessage, timer } = userData;
      const difference =
        message.createdTimestamp - lastMessage.createdTimestamp;

      clearTimeout(timer);

      if (difference < TIME) {
        userData.msgCount += 1;
        if (userData.msgCount >= LIMIT) {
          try {
            user
              .timeout(60000, "Spammou demais") // * 60000 = 60 seconds
              .then(console.log(`Member timeouted: ${user.displayName}`));
          } catch (error) {
            // ! maybe the "spammer" is a modder, so you can't timeout him
            console.log(error);
          }
          message.reply(
            "Você está enviando mensagens muito rápido! Por favor, pare de spammar."
          );
          userData.msgCount = 0;
          return true;
        } else {
          userData.timer = setTimeout(() => {
            spamMap.delete(user.id);
          }, TIME);
          spamMap.set(user.id, userData);
        }
      } else {
        spamMap.set(user.id, {
          msgCount: 1,
          lastMessage: message,
          timer: setTimeout(() => {
            spamMap.delete(user.id);
          }, TIME),
        });
      }
    } else {
      const fn = setTimeout(() => {
        spamMap.delete(user.id);
      }, TIME);
      spamMap.set(user.id, {
        msgCount: 1,
        lastMessage: message,
        timer: fn,
      });
    }
    return false;
  }
}

module.exports = MessageCreateEvent;

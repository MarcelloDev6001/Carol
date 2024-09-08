const {
  EmbedBuilder,
  PermissionFlagsBits,
  DiscordAPIError,
} = require("discord.js");
const JsonReader = require("../utils/jsonReader.js");
const { prefix } = require("../../config.json");

// * simple json format: {
// *    GUILD_ID: {
// *      USER_ID: {
// *        "xp": 0,
// *        "level": 0
// *      }
// *    }
// *  }
class XPSystem {
  static async getXP(user, guild) {
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
  static async getLevel(user, guild) {
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
  static async updateExperienceAndLevel(
    user,
    guild,
    channel,
    xpToAdd,
    levelToAdd
  ) {
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
  static async getUsersRank(message, amount) {
    let expJson = JsonReader.read("./data/experience.json");
    let usersInExpJson = {};
    let users = [];
    if (!message.guild.id in expJson) {
      message.reply("Tem ninguém no rank de Level");
      return [];
    } else {
      usersInExpJson = expJson[message.guild.id];
    }
    let altIndex = 0;
    for (const index in usersInExpJson) {
      const memberLvl = usersInExpJson[index];
      let userKey = await Object.keys(usersInExpJson)[altIndex];
      users.push({
        memberID: userKey,
        xp: memberLvl["xp"],
        level: memberLvl["level"],
      });
      altIndex += 1;
      if (altIndex >= amount) {
        break;
      }
    }
    users.sort((a, b) => {
      let xpA = a["xp"];
      let xpB = b["xp"];
      return xpB - xpA;
    });
    return users;
  }
  static async getLevelUpEmbed(client, user, channel, userLevel, userXP) {
    let levelUPEmbed = new EmbedBuilder()
      .setColor(0xffffff)
      .setTitle("Level UP!")
      .setAuthor({
        name: client.user.displayName,
        iconURL: client.user.avatarURL({ size: 1024 }),
        url: `https://Discordapp.com/users/${client.user.id.toString()}`,
      })
      .setDescription(
        `Parabens <@${
          user.id
        }>, você acabou de evoluir para o level ${userLevel.toString()}! (${userXP.toString()} xp)`
      )
      .setThumbnail(user.avatarURL({ size: 1024 }));
    return levelUPEmbed;
  }
}

module.exports = XPSystem;

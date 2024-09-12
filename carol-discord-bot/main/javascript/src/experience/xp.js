const { EmbedBuilder, MessagePayload, Message } = require("discord.js");
const JsonReader = require("../utils/jsonReader.js");
const fs = require("fs");
const { userId } = require("../../config.json");

// * new funny format: USER_ID.JSON
// * {
// *   GUILD_ID: {
// *     xp: 0,
// *     level: 0
// *   }
// * }
class XPSystem {
  static async getXP(user, guild) {
    let expJson = JsonReader.read(`./data/usersdata/${user.id}.json`);
    if (!guild.id in expJson) {
      expJson[guild.id] = {
        xp: 0,
        level: 0,
      };
    }
    return expJson[guild.id]["xp"];
  }
  static async getLevel(user, guild) {
    // * basically the same code of getXP()
    let expJson = JsonReader.read(`./data/usersdata/${user.id}.json`);
    if (!guild.id in expJson) {
      expJson[guild.id] = {
        xp: 0,
        level: 0,
      };
    }
    return expJson[guild.id]["level"];
  }
  static async updateExperienceAndLevel(
    user,
    guild,
    channel,
    xpToAdd,
    levelToAdd,
    client,
    message
  ) {
    let expJson = {};
    try {
      expJson = JsonReader.read(`./data/usersdata/${user.id}.json`);
    } catch (error) {
      expJson = {};
    }
    if (!(guild.id in expJson)) {
      expJson[guild.id] = {
        xp: 0,
        level: 0,
      };
    }
    expJson[guild.id]["xp"] += 1;
    if (expJson[guild.id]["xp"] - 1000 > expJson[guild.id]["level"] * 1000) {
      expJson[guild.id]["level"] += 1;
      let levelUPEmbed = await XPSystem.getLevelUpEmbed(
        await guild.members.fetch({
          user: [userId],
          force: true,
        }),
        user,
        channel,
        expJson[guild.id]["level"],
        expJson[guild.id]["xp"]
      );
      channel.send(
        new MessagePayload(message, {
          content: `<@${user.id}>`,
          embeds: [levelUPEmbed],
        })
      );
    }
    JsonReader.save(`./data/usersdata/${user.id}.json`, expJson);
    return expJson;
  }
  static async getUsersRank(message, amount) {
    let usersInFolder = fs.readdirSync("./data/usersdata/");
    let users = [];
    for (let index = 0; index < usersInFolder.length; index++) {
      const element = JsonReader.read(
        `./data/usersdata/${usersInFolder[index]}`
      );
      if (message.guild.id in element) {
        users.push({
          memberID: usersInFolder[index].replace(".json", ""),
          xp: element[message.guild.id]["xp"],
          level: element[message.guild.id]["level"],
        });
      }
    }
    let altIndex = 0;
    for (const index in users) {
      const memberLvl = users[index];
      let userKey = Object.keys(users)[altIndex];
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
  static async getLevelUpEmbed(selfUser, user, channel, userLevel, userXP) {
    let levelUPEmbed = new EmbedBuilder()
      .setColor(0xffffff)
      .setTitle("Level UP!")
      // .setAuthor({
      //   name: selfUser["nickname"],
      //   iconURL: `https://cdn.discordapp.com/avatars/${selfUser.user.id}/${selfUser.user.avatar}`,
      //   url: `https://Discordapp.com/users/${selfUser.user.id.toString()}`,
      // })
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

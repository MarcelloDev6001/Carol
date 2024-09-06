const XPSystem = require("../experience/xp.js");

class LevelMessageCommand {
  static async level(message, prefix, messageCommand) {
    let expJson = await XPSystem.updateExperienceAndLevel(
      message.author,
      message.guild,
      message.channel,
      1,
      0
    );
    let userXP = expJson[message.guild.id][message.author.id]["xp"];
    let userLevel = expJson[message.guild.id][message.author.id]["level"];
    message.reply(`Seu level é ${userLevel} (${userXP}xp)`);
  }
  static async levelRank(message, prefix, messageCommand) {
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
  }
}

module.exports = LevelMessageCommand;

const { MessagePayload } = require("discord.js");
const XPSystem = require("../experience/xp.js");

// * just shows you level (or the level of another member) and shows the level rank of a specific guild
class LevelMessageCommand {
  static async level(message, prefix, messageCommand) {
    let userXP = await XPSystem.getXP(message.author, message.guild);
    let userLevel = await XPSystem.getLevel(message.author, message.guild);
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
    message.reply(
      new MessagePayload(message, {
        content: finalMessageResult,
      })
    );
  }
}

module.exports = LevelMessageCommand;
